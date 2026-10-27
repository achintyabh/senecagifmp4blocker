# Seneca Learning GIF & MP4 Blocker

**You will still be able to watch the topic videos that pop up in each assignment, as they are YouTube videos, not raw .mp4 or raw .gifs. Please note that this will block GIPHY GIFs not only on Seneca Learning, but across your whole system! So you can't use GIPHY GIFs anymore. If you are OK with this trade-off, then you may proceed with running the Python script.**

A safe, lightweight, cross-platform utility designed to help students eliminate distracting animations, GIFs, and memes on Seneca Learning without breaking access to core assignments, text, or quizzes.

Standard browser extensions often fail to filter these properly due to Manifest V3 limitations, and running background local DNS proxies can clash with system network ports. The safest, most efficient method is updating your operating system's local `hosts` configuration file for both IPv4 and IPv6 protocols so the targeted media delivery servers hit an instant dead end.

This application automatically handles file paths, requests administrative/root privileges using your OS's native password prompt windows, and provides an interactive menu to block or unblock the domains safely.

## Targeted Domains
The application maps the following explicit distribution subdomains to local loopback endpoints (`127.0.0.1` and `::1`), cutting off both standard animated files and hidden background MP4 streaming payloads:
* media.giphy.com
* media0.giphy.com to media8.giphy.com
* i.giphy.com
* clip.giphy.com
* gif.app.senecalearning.com (Only isolates the animation folder; app.senecalearning.com remains fully open)

## Installation & Usage

### Running via Python 3
Clone this repository and run:

* **Windows (Admin PowerShell):** `python senecagifmp4blocker.py` (or `py senecagifmp4blocker.py`)
* **macOS (Terminal):** `sudo python3 senecagifmp4blocker.py`
* **Linux (Terminal):** `sudo python3 senecagifmp4blocker.py`

When executed, the script will show system warnings and present an interactive prompt:
1) Block GIFs and MP4 videos
2) Unblock GIFs and MP4 videos (Uninstall)
3) Exit

## Troubleshooting
* **Permission Error / Write Block:** Windows Defender or third-party antivirus suites actively guard the system hosts file to prevent malicious hijacking. If the script encounters a write block, temporarily disable **Real-Time Protection** in your security settings, run the utility, and re-enable it immediately after.
* **GIFs/Videos are still showing up:** Web browsers aggressively store image and routing profiles inside their own persistent runtime cache. Completely close all browser windows, open a fresh window profile, or press `Ctrl + F5` while on the Seneca Learning portal to force a deep layout update.
