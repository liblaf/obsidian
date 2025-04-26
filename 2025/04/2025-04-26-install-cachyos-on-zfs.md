---
created: 2025-04-26T23:55:35+08:00
modified: 2025-04-27T00:00:28+08:00
tags:
  - OS/Linux/Arch
  - OS/Linux/Arch/CachyOS
title: Install CachyOS on ZFS
---

## How to disable zram?

- <https://askubuntu.com/a/1419240>

```sh
# /etc/default/grub
GRUB_CMDLINE_LINUX_DEFAULT="systemd.zram=0"
```
