---
created: 2025-04-26T23:55:35+08:00
modified: 2025-04-27T00:37:56+08:00
tags:
  - Dotfiles
  - OS/Linux/Arch
  - OS/Linux/Arch/CachyOS
title: Install CachyOS on ZFS
---

## Partitioning

```console
$ lsblk --output NAME,FSTYPE,LABEL,PARTTYPENAME,SIZE,MOUNTPOINT
NAME        FSTYPE     LABEL     PARTTYPENAME          SIZE MOUNTPOINT
nvme0n1                                                3.7T
├─nvme0n1p1 vfat       EFI       EFI System              1G /boot/efi
├─nvme0n1p2 vfat       Boot      Microsoft basic data    3G /boot
└─nvme0n1p3 zfs_member zpcachyos Linux filesystem      3.7T
```

- <https://wiki.archlinux.org/title/GRUB/Tips_and_tricks#Recall_previous_entry>

`GRUB_SAVEDEFAULT=true` will only work if `/boot/grub` is not on btrfs / ZFS, because GRUB cannot write to btrfs / ZFS.

## How to disable zram?

- <https://askubuntu.com/a/1419240>

```sh
# /etc/default/grub
GRUB_CMDLINE_LINUX_DEFAULT="systemd.zram=0"
```

## Specifying boot ID has no effect, no persistent journal was found.

- <https://discourse.practicalzfs.com/t/psa-systemd-journal-persistence-settings-and-race-condition-between-zfs-mount-service-and-systemd-journald-service/1929>

> With your persistent journal being stored on a ZFS filesystem, there is now a race condition on startup beween `zfs-mount.service`, which will mount your `/var/log` directory, and `systemd-journald.service`, which will try to write to it before it's been mounted. This can cause `systemd-journald` to fall back to using an in-memory journal, or result in unpredictable loging behaviour
>
> The fix is to create a dependency for `systemd-journald.service` on `zfs-mount.service`:

```ini
# /etc/systemd/system/systemd-journald.service.d/zfs.conf
[Unit]
After    = zfs-mount.service
Requires = zfs-mount.service
```
