#!/usr/bin/env python3
import os
import sys
import platform
import subprocess

# THE CLEAN LIST OF DOMAINS TO BLOCK (No browser prefixes, no typos)
DOMAINS = [
    "media.giphy.com",
    "media0.giphy.com",
    "media1.giphy.com",
    "media2.giphy.com",
    "media3.giphy.com",
    "media4.giphy.com",
    "media5.giphy.com",
    "media6.giphy.com",
    "media7.giphy.com",
    "media8.giphy.com",
    "i.giphy.com",
    "clip.giphy.com",
    "gif.app.senecalearning.com"
]

def elevate_privileges():
    """
    Checks for admin/root access. If missing, it automatically spawns 
    a native GUI password prompt depending on the operating system platform.
    """
    system = platform.system()
    script_path = os.path.abspath(sys.argv)
    
    if system == "Windows":
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("Requesting Administrator privileges...")
            params = " ".join(sys.argv[1:])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script_path}" {params}', None, 1)
            sys.exit(0)
            
    elif system in ["Linux", "Darwin"]:
        if os.getuid() != 0:
            print("Requesting root/administrator privileges...")
            
            if system == "Darwin": # macOS native GUI pop-up
                osa_command = f'do shell script "python3 \\"{script_path}\\"" with administrator privileges'
                subprocess.run(["osascript", "-e", osa_command])
                sys.exit(0)
            else: # Linux graphical environment prompts
                # Try pkexec first, fall back to legacy gexec, fallback to terminal sudo
                try:
                    os.execvp("pkexec", ["pkexec", "python3", script_path] + sys.argv[1:])
                except FileNotFoundError:
                    try:
                        os.execvp("gexec", ["gexec", "python3", script_path] + sys.argv[1:])
                    except FileNotFoundError:
                        os.execvp("sudo", ["sudo", "python3", script_path] + sys.argv[1:])

def get_hosts_path():
    """Determines the path to the hosts configuration file based on the OS."""
    system = platform.system()
    if system == "Windows":
        return os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32', 'drivers', 'etc', 'hosts')
    return "/etc/hosts"

def flush_dns(system):
    """Flushes the system network DNS resolver cache cleanly across platforms."""
    print("Flushing network DNS cache...")
    try:
        if system == "Windows":
            subprocess.run(["ipconfig", "/flushdns"], stdout=subprocess.DEVNULL)
        elif system == "Darwin":
            subprocess.run(["dscacheutil", "-flushcache"], stdout=subprocess.DEVNULL)
            subprocess.run(["killall", "-HUP", "mDNSResponder"], stdout=subprocess.DEVNULL)
        elif system == "Linux":
            res = subprocess.run(["systemctl", "is-active", "--quiet", "systemd-resolved"])
            if res.returncode == 0:
                subprocess.run(["systemctl", "restart", "systemd-resolved"])
            else:
                subprocess.run(["systemctl", "restart", "NetworkManager"], stdout=subprocess.DEVNULL)
        print("Success: DNS cache flushed successfully.")
    except Exception as e:
        print(f"Warning: Could not automatically flush DNS cache: {e}")

def main():
    elevate_privileges()
    
    system = platform.system()
    hosts_path = get_hosts_path()
    modified = False
    newline = "\r\n" if system == "Windows" else "\n"
    encoding_type = "utf-8-sig" if system == "Windows" else "utf-8"
    
    try:
        with open(hosts_path, "r", encoding=encoding_type, errors="ignore") as f:
            content = f.read()
            
        new_entries = []
        for domain in DOMAINS:
            ipv4_entry = f"127.0.0.1 {domain}"
            ipv6_entry = f"::1 {domain}"
            
            if ipv4_entry not in content:
                print(f"Preparing IPv4 block for: {domain}")
                new_entries.append(ipv4_entry)
                modified = True
                
            if ipv6_entry not in content:
                print(f"Preparing IPv6 block for: {domain}")
                new_entries.append(ipv6_entry)
                modified = True
                
        if modified:
            with open(hosts_path, "a", encoding="utf-8") as f:
                for entry in new_entries:
                    f.write(f"{newline}{entry}")
                f.write(newline)
                
            print(f"Success: New block layout appended to {hosts_path}.")
            flush_dns(system)
            print("\nImportant: Please restart your web browser entirely to drop older image cache memory.")
        else:
            print("Status: All domains are already securely blocked. No changes made.")
            
    except Exception as e:
        print(f"Critical Error editing hosts file: {e}")
        input("\nPress Enter to close...")
        sys.exit(1)

if __name__ == "__main__":
    main()
