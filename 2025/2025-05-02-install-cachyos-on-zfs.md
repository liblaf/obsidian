---
date: 2025-05-02T22:08:56+08:00
modified: 2025-09-20T18:37:56+08:00
tags:
  - OS/Linux/Arch/CachyOS
  - ZFS
title: Install CachyOS on ZFS
---

## 1. Follow GUI Installer

## 2. Reboot Into Live ISO (Again)

## 3. Setup Custom ZFS Layout

By default, CachyOS Installer will create a ZFS layout with the following commands:

```sh
zpool create -f -o ashift=12 -o autotrim=on -o compatibility=grub2 -O mountpoint=none -O acltype=posixacl -O atime=off -O relatime=off -O xattr=sa -O normalization=formD zpcachyos /dev/disk/by-partuuid/f329b2e6-0022-4c8c-bdb5-c1422fb02ebe
zfs create -o compression=lz4 -o canmount=off -o mountpoint=none zpcachyos/ROOT
zfs create -o compression=lz4 -o canmount=off -o mountpoint=none zpcachyos/ROOT/cos
zfs create -o compression=lz4 -o canmount=noauto -o mountpoint=/ zpcachyos/ROOT/cos/root
zfs create -o compression=lz4 -o canmount=on -o mountpoint=/home zpcachyos/ROOT/cos/home
zfs create -o compression=lz4 -o canmount=on -o mountpoint=/var/cache zpcachyos/ROOT/cos/varcache
zfs create -o compression=lz4 -o canmount=on -o mountpoint=/var/log zpcachyos/ROOT/cos/varlog
```

Resulting a layout like:

```console
$ zfs list -o name,canmount,compression,mountpoint
NAME                         CANMOUNT  COMPRESS        MOUNTPOINT
zpcachyos                    on        on              none
zpcachyos/ROOT               off       lz4             none
zpcachyos/ROOT/cos           off       lz4             none
zpcachyos/ROOT/cos/home      on        lz4             /home
zpcachyos/ROOT/cos/root      on        lz4             /
zpcachyos/ROOT/cos/varcache  on        lz4             /var/cache
zpcachyos/ROOT/cos/varlog    on        lz4             /var/log
```

However, I want to setup a custom layout. Here are the steps:

```console
$ sudo zpool import -f -R /mnt zpcachyos
```

```sh
#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail

POOL="${1:-"rpool"}"

if ((EUID != 0)); then
  echo "This script must be run as root." >&2
  exit 1
fi

mkdir --parents --verbose /etc/zfs/zfs-list.cache
touch "/etc/zfs/zfs-list.cache/$POOL"

# zpool import -f -R /mnt zpcachyos "$POOL"

function zfs-config() {
  local filesystem="$1"
  shift
  if zfs list "$filesystem" &> /dev/null; then
    local exists="true"
  else
    local exists="false"
  fi
  if [[ $exists == "true" ]]; then
    if (($# > 0)); then zfs set "$@" "$filesystem"; fi
    for prop in canmount compression mountpoint; do
      if [[ $* =~ "$prop="* ]]; then continue; fi
      zfs inherit "$prop" "$filesystem"
    done
  else
    args=()
    for arg in "$@"; do args+=("-o" "$arg"); done
    zfs create "${args[@]}" "$filesystem"
  fi
}

zfs-config "$POOL/ROOT/cos/root" canmount=on mountpoint=/old
zfs-config "$POOL/ROOT/cos/home" canmount=on mountpoint=/old/home
zfs-config "$POOL/ROOT/cos/varcache" canmount=on mountpoint=/old/var/cache
zfs-config "$POOL/ROOT/cos/varlog" canmount=on mountpoint=/old/var/log

zfs-config "$POOL/ROOT/CachyOS" canmount=on compression=lz4 mountpoint=/
zfs-config "$POOL/ROOT/CachyOS/srv"
zfs-config "$POOL/ROOT/CachyOS/usr" canmount=off
zfs-config "$POOL/ROOT/CachyOS/usr/local"
zfs-config "$POOL/ROOT/CachyOS/var" canmount=off
zfs-config "$POOL/ROOT/CachyOS/var/lib"
zfs-config "$POOL/ROOT/CachyOS/var/lib/AccountsService"
zfs-config "$POOL/ROOT/CachyOS/var/lib/NetworkManager"
zfs-config "$POOL/ROOT/CachyOS/var/lib/pacman"
zfs-config "$POOL/ROOT/CachyOS/var/log"
zfs-config "$POOL/ROOT/CachyOS/var/spool"
zfs-config "$POOL/USERDATA" canmount=off mountpoint=none
zfs-config "$POOL/USERDATA/home" canmount=on mountpoint=/home
zfs-config "$POOL/USERDATA/root" canmount=on mountpoint=/root

zfs unmount -a
```

```sh
sudo zfs mount -a
# rsync: This rsync does not support --crtimes (-N)
sudo rsync --info="PROGRESS2" --archive --hard-links --acls --xattrs --atimes --partial /mnt/old/ /mnt/
sudo cp "/etc/zfs/zfs-list.cache/$POOL" "/mnt/etc/zfs/zfs-list.cache/$POOL"
```

```sh
sudo mount /dev/vda2 /mnt/boot
sudo mount /dev/vda1 /mnt/boot/efi
sudo arch-chroot /mnt
```

In chroot:

```sh
systemctl enable zfs.target
systemctl enable zfs-import.target
systemctl enable zfs-volumes.target
systemctl enable zfs-import-scan.service
systemctl enable zfs-zed.service
systemctl enable zfs-volume-wait.service
sed --in-place 's|zpcachyos/ROOT/cos/root|rpool/ROOT/CachyOS|g' /etc/default/grub
grub-mkconfig --output="/boot/grub/grub.cfg"
```

after exit from chroot:

```sh
sudo umount /mnt/boot/efi
sudo umount /mnt/boot
sudo zpool export -a
```
