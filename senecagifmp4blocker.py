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
    script_path = os.path.abspath(sys.argv[0])
    
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

def display_warnings():
    """Displays user warning rules upfront before allowing modification selections."""
    print("===============================================================================")
    print("WARNING:")
    print("You will still be able to watch the topic videos that pop up in each")
    print("assignment, as they are YouTube videos, not raw .mp4 or raw .gifs.")
    print("Please note that this will block GIPHY GIFs not only on Seneca Learning,")
    print("but across your whole system! So you can't use GIPHY GIFs anymore.")
    print("===============================================================================")

def main():
    elevate_privileges()
    display_warnings()
    
    print("\nWhat would you like to do?")
    print("1) Block GIFs and MP4 videos")
    print("2) Unblock GIFs and MP4 videos (Uninstall)")
    print("3) Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    if choice not in ["1", "2"]:
        print("Exiting. No changes made.")
        sys.exit(0)
        
    system = platform.system()
    hosts_path = get_hosts_path()
    newline = "\r\n" if system == "Windows" else "\n"
    encoding_type = "utf-8-sig" if system == "Windows" else "utf-8"
    
    try:
        with open(hosts_path, "r", encoding=encoding_type, errors="ignore") as f:
            lines = f.readlines()
            
        modified = False
        updated_lines = []
        
        # Build strict matching templates of targets to evaluate
        targets_to_remove = []
        for domain in DOMAINS:
            targets_to_remove.append(f"127.0.0.1 {domain}")
            targets_to_remove.append(f"::1 {domain}")
            
        if choice == "1":
            # BLOCK MODE: Filter existing configurations to keep file clean
            existing_content = "".join(lines)
            new_entries = []
            
            for domain in DOMAINS:
                ipv4_entry = f"127.0.0.1 {domain}"
                ipv6_entry = f"::1 {domain}"
                
                if ipv4_entry not in existing_content:
                    print(f"Preparing IPv4 block for: {domain}")
                    new_entries.append(ipv4_entry)
                    modified = True
                    
                if ipv6_entry not in existing_content:
                    print(f"Preparing IPv6 block for: {domain}")
                    new_entries.append(ipv6_entry)
                    modified = True
                    
            if modified:
                # Strip trailing clean whitespace at the file tail first
                content_str = "".join(lines).rstrip()
                with open(hosts_path, "w", encoding="utf-8") as f:
                    f.write(content_str)
                    for entry in new_entries:
                        f.write(f"{newline}{entry}")
                    f.write(newline)
                print(f"Success: New block layout appended to {hosts_path}.")
                flush_dns(system)
                print("\nImportant: Please restart your web browser entirely to drop older image cache memory.")
            else:
                print("Status: All domains are already securely blocked. No changes made.")
                
        elif choice == "2":
            # UNBLOCK MODE (UNINSTALLER): Read line by line, dropping exact block fragments
            for line in lines:
                stripped_line = line.strip()
                if stripped_line in targets_to_remove:
                    print(f"Removing rule block line: {stripped_line}")
                    modified = True
                else:
                    updated_lines.append(line)
                    
            if modified:
                # Clean up any trailing excessive double newlines left from editing
                cleaned_output = "".join(updated_lines).rstrip() + newline
                with open(hosts_path, "w", encoding="utf-8") as f:
                    f.write(cleaned_output)
                print(f"Success: Block lines successfully removed from {hosts_path}.")
                flush_dns(system)
                print("\nImportant: Please restart your web browser entirely to restore normal media loading.")
            else:
                print("Status: No active block rules found in hosts file. Nothing to uninstall.")
                
    except Exception as e:
        print(f"Critical Error editing hosts file: {e}")
        input("\nPress Enter to close...")
        sys.exit(1)

if __name__ == "__main__":
    main()
