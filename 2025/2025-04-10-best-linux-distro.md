---
created: 2025-04-10T19:19:58+08:00
modified: 2025-09-19T15:19:32+08:00
tags:
  - Dotfiles
  - OS/Linux
  - OS/Linux/Arch
  - OS/Linux/Arch/CachyOS
title: Best Linux Distro
---

- **Mirror:** 🟢 in TUNA, 🟡 no in TUNA, but in CERNET, 🔴 not in CERNET
- **GUI:** offer GUI installer
- **ZFS:** easy to install on ZFS root filesystem

|                Distro                | Mirror | GUI | ZFS | Hardware Detection |
| :----------------------------------: | :----: | :-: | :-: | :----------------: |
| [Arch Linux](https://archlinux.org/) |   🟢   | 🔴  | 🔴  |         🔴         |
|               CachyOS                |   🟡   | 🟢  | 🟢  |         🟢         |
|             EndeavourOS              |   🟢   | 🟢  | 🔴  |                    |
|            Manjaro Linux             |   🟢   | 🟢  | 🔴  |         🟢         |
|             Garuda Linux             |   🟢   | 🟢  | 🔴  |                    |
|            Bluestar Linux            |   🔴   |     |     |                    |
|              ArcoLinux               |   🔴   |     |     |                    |
|           Ultimate Edition           |   🔴   |     |     |                    |
|            ArchBang Linux            |   🔴   |     |     |                    |
|              Archcraft               |   🔴   |     |     |                    |
|               RebornOS               |   🔴   |     |     |                    |
|             Artix Linux              |   🟢   |     |     |                    |
|               blendOS                |   🔴   |     |     |                    |
|                SDesk                 |   🔴   |     |     |                    |
|            Archman Linux             |   🔴   |     |     |                    |
|             SystemRescue             |   🔴   |     |     |                    |
|           Ditana GNU/Linux           |   🔴   |     |     |                    |
|              Snal Linux              |   🔴   |     |     |                    |
|           BlackArch Linux            |   🟢   |     |     |                    |
|              Athena OS               |   🔴   |     |     |                    |
|       Parabola GNU/Linux-libre       |   🟡   |     |     |                    |
|                Obarun                |   🔴   |     |     |                    |
|                 UBOS                 |   🔴   |     |     |                    |
|                Zenned                |   🔴   |     |     |                    |

## Why didn't I choose ...?

### Why didn't I choose "Windows"?

What can I say?

### Why didn't I choose "Ubuntu"?

While Ubuntu offers a considerable number of packages, it still lacks many of the tools I regularly rely on, such as `pixi`, `uv`, `micromamba`, `3dslicer`, `xh`, `yazi`, `bun`, and many others. As of 2025-09-19, [Repology](https://repology.org/repositories/statistics) data indicates that [Ubuntu 24.04](https://repology.org/repository/ubuntu_24_04) provides 36,956 packages, but only 12,024 (40.6%) of them are up-to-date. Many essential packages --- including Microsoft Edge and VirtualBox --- require adding third-party PPAs or manual installation, which quickly becomes a maintenance nightmare.

In contrast, [Arch Linux](https://repology.org/repository/arch), though offering fewer total packages (11,625), includes many of the applications I need daily, with 9,243 (83.8%) of them being up-to-date. The [Arch User Repository (AUR)](https://repology.org/repository/aur) further expands this with 79,585 packages, 24,297 (72.6%) of which are the newest. Arch has a smaller but highly active community that values simplicity and user control.

That said, Arch Linux does come with trade-offs: it sacrifices some stability in exchange for newer software, makes it nearly impossible to install older versions of packages, and introduces potential security risks through the AUR. Nonetheless, for my use case, the benefits outweigh these drawbacks.

### Why didn't I choose "Arch Linux"?

CachyOS offers a more user-friendly graphical installation interface, and convenient packages, including but not limited to:

- [cachyos-snapper-support](https://github.com/CachyOS/CachyOS-PKGBUILDS/tree/master/cachyos-snapper-support)
- [grub-btrfs-support](https://github.com/CachyOS/CachyOS-PKGBUILDS/tree/master/grub-btrfs-support)

### Why didn't I choose "Artix Linux"?

Artix Linux features **the OpenRC init software**. In other words, **no systemd**.

### Why didn't I choose "BlackArch Linux"?

BlackArch Linux is designed for **penetration testers and security researchers**.

### Why didn't I choose "Parabola GNU/Linux-libre"?

Parabola GNU/Linux-libre aims to provide a **fully free (as in freedom)** distribution.
