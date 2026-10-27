# Seneca Learning GIF & MP4 Blocker

A small, open-source script for each major operating system that stops the animated GIFs and short looping videos in Seneca Learning from loading, so they are less distracting while you study.

It works by adding a clearly labelled block of entries to your computer's `hosts` file. Those entries point the GIF servers that Seneca uses at your own machine (`127.0.0.1` and `::1`), so the files simply never arrive. Everything else on Seneca (text, quizzes, assignments) keeps working.

> **Unofficial project.** This is not made by, or affiliated with, Seneca Learning, GIPHY or Tenor.

## Read this before you run it

- **It blocks GIPHY and Tenor on your whole computer, not just on Seneca.** Any website or app that loads GIFs from those services (chat apps, GIF keyboards and pickers, social media) will stop showing them until you unblock.
- **Seneca's topic videos still work.** They are hosted on YouTube, not the servers blocked here.
- **It needs administrator rights**, because the `hosts` file is a protected system file. Only run it on a computer you own or are allowed to change. On a school or work computer, check that the rules permit it first.
- **It is easy to undo.** Run the same script again and choose option 2.

## Which file do I need?

| Your system | File to run |
|---|---|
| Windows 10 / 11 | `senecagifmp4blockerforwindows.bat` (launcher) and `senecagifmp4blockerforwindows.ps1` (the script itself). Keep both files in the same folder. |
| macOS | `senecagifmp4blockerformacos.sh` |
| Linux | `senecagifmp4blockerforlinux.sh` |
| FreeBSD, OpenBSD, NetBSD, DragonFly BSD | `senecagifmp4blockerforbsd.sh` |

## How to run it

**Windows**
1. Double-click `senecagifmp4blockerforwindows.bat`.
2. Click **Yes** on the Windows permission prompt.
3. Pick an option from the menu in the window that opens.

If Windows SmartScreen shows "Windows protected your PC", choose **More info → Run anyway**. You can read the files first, since they are plain text. You can also right-click the `.ps1` file and choose **Run with PowerShell**.

**macOS**
```sh
sh senecagifmp4blockerformacos.sh
```
Enter your Mac password in the dialog that appears.

**Linux**
```sh
sh senecagifmp4blockerforlinux.sh
```
On a desktop you'll get a graphical password prompt. Otherwise the script uses `sudo`.

**BSD**
```sh
sh senecagifmp4blockerforbsd.sh
```
The script uses `sudo` or `doas` if installed, and otherwise asks for the root password through `su`.

On every system the script shows a short warning and then this menu:

```
1) Block GIFs and MP4 videos
2) Unblock GIFs and MP4 videos (Uninstall)
3) Exit
```

When it finishes, **close your browser completely and reopen it** so it forgets any GIFs it already cached.

## What gets blocked

Each domain is blocked for both IPv4 (`127.0.0.1`) and IPv6 (`::1`).

| Service | Domains |
|---|---|
| GIPHY | `media.giphy.com`, `media0.giphy.com` to `media8.giphy.com`, `i.giphy.com`, `clip.giphy.com` |
| Tenor | `media.tenor.com`, `media1.tenor.com`, `c.tenor.com`, `t.tenor.com` |
| Seneca | `gif.app.senecalearning.com` (only the GIF folder; `app.senecalearning.com` stays fully open) |

Seneca's own help centre says its GIFs are served from `media.giphy.com` and `media.tenor.com`. The other hostnames are the additional servers those services use. Some entries (`media5` to `media8`, `t.tenor.com`) may not be in active use. Blocking a hostname that doesn't exist does no harm.

## What the script changes

- It adds one block to your `hosts` file, wrapped in marker comments:
  ```
  # BEGIN seneca-blocker
  127.0.0.1 media.giphy.com
  ::1 media.giphy.com
  ...
  # END seneca-blocker
  ```
- Unblocking removes that block and nothing else. Your own entries and comments are left alone.
- Before the first change it saves a copy of your original file as `hosts.seneca.bak` in the same folder.
- Running **Block** again is safe. It won't create duplicates, and it adds any domains missing from an older version of the block.
- If you used the earlier single Python script, these scripts can remove its entries too.

The `hosts` file lives at `C:\Windows\System32\drivers\etc\hosts` on Windows and at `/etc/hosts` on macOS, Linux and the BSDs.

## Troubleshooting

**The GIFs still show up.**
Browsers keep their own cache. Close every browser window and reopen it, or press `Ctrl + F5` (`Cmd + Shift + R` on a Mac) on the Seneca page. If it still shows GIFs, check that your browser or a VPN isn't using its own DNS settings that bypass the system `hosts` file.

**Windows says the file couldn't be written, or my antivirus raised an alert.**
Some security software protects the `hosts` file, because malware often edits it. Open your antivirus or **Windows Security → Virus & threat protection → Protection history**, allow the blocked action, then run the script again. There is no need to turn off real-time protection, and it's best to leave it on.

**I can't use a GIF keyboard or GIF picker in another app.**
That is the expected side effect of blocking GIPHY and Tenor. Run the script and choose **2) Unblock** to turn them back on.

**"This script is for ..." error.**
You ran the script for a different operating system. Use the file from the table above that matches yours.

**Unblocking didn't restore the GIFs right away.**
Run the unblock option, then fully restart your browser. If nothing changes, restart the computer.

## Uninstalling

Run your system's script again and choose **2) Unblock GIFs and MP4 videos**. Then delete the script files. The backup `hosts.seneca.bak` is yours to keep or delete.

## License

See the `LICENSE` file.
