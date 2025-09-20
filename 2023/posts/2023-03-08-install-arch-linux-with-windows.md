---
category:
  - Posts
date: 2023-03-08T08:00:00+08:00
modified: 2025-09-20T23:07:39+08:00
tags:
  - Arch_Linux
  - Linux
  - Windows
title: Install Arch Linux with Windows
---

## BIOS Setup

- change hard drive mode from "RAID" to "ACHI/NVME"

## Partitioning for EFI System

- disable "Secure Boot"
- boot Arch Linux ISO

### [Optional] Connect from Another Device

```shell-session
root@archiso ~ # passwd
New password:
Retype new password:
passwd: password updated succesfully
root@archiso ~ # systemctl start sshd
root@archiso ~ # systemctl status sshd
● sshd.service - OpenSSH Daemon
     Loaded: loaded (/usr/lib/systemd/system/sshd.service; enabled; preset: disabled)
     Active: active (running) since Wed 2023-03-08 06:08:32 UTC; 1min 36s ago
   Main PID: 508 (sshd)
      Tasks: 1 (limit: 19074)
     Memory: 4.2M
        CPU: 145ms
     CGroup: /system.slice/sshd.service
             └─508 "sshd: /usr/bin/sshd -D [listener] 0 of 10-100 startups"

Mar 08 06:08:32 archiso systemd[1]: Started OpenSSH Daemon.
Mar 08 06:08:33 archiso sshd[508]: Server listening on 0.0.0.0 port 22.
Mar 08 06:08:33 archiso sshd[508]: Server listening on :: port 22.
root@archiso ~ # ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:12:bc:70 brd ff:ff:ff:ff:ff:ff
    inet 10.0.2.15/24 metric 100 brd 10.0.2.255 scope global dynamic enp0s3
       valid_lft 86284sec preferred_lft 86284sec
    inet6 fe80::a00:27ff:fe12:bc70/64 scope link
       valid_lft forever preferred_lft forever
```

###### SSH from Another Device

> I'm using Port Forwarding in this example.

```shell-session
$ ssh -p 22222 root@127.0.0.1
root@127.0.0.1's password:
To install Arch Linux follow the installation guide:
https://wiki.archlinux.org/title/Installation_guide

For Wi-Fi, authenticate to the wireless network using the iwctl utility.
For mobile broadband (WWAN) modems, connect with the mmcli utility.
Ethernet, WLAN and WWAN interfaces using DHCP should work automatically.

After connecting to the internet, the installation guide can be accessed
via the convenience script Installation_guide.


Last login: Wed Mar  8 06:09:54 2023 from 10.0.2.2
root@archiso ~ #
```

### Partitioning

```shell-session
root@archiso ~ # fdisk -l
Disk /dev/sda: 256 GiB, 274877906944 bytes, 536870912 sectors
Disk model: VBOX HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes


Disk /dev/loop0: 688.47 MiB, 721911808 bytes, 1409984 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
root@archiso ~ # cfdisk
```

- select label type: `gpt`

```
                                 Disk: /dev/sda
              Size: 256 GiB, 274877906944 bytes, 536870912 sectors
          Label: gpt, identifier: 1355000F-BBCD-634E-82AD-5AA1BCB6064A

    Device               Start           End      Sectors     Size Type
>>  /dev/sda1             2048       2099199      2097152       1G EFI System
    Free space         2099200     536870878    534771679     255G









 ┌────────────────────────────────────────────────────────────────────────────┐
 │Partition UUID: AD8D5ED1-76CF-CF49-A736-89782BC63BCF                        │
 │Partition type: EFI System (C12A7328-F81F-11D2-BA4B-00A0C93EC93B)           │
 └────────────────────────────────────────────────────────────────────────────┘
     [ Delete ]  [ Resize ]  [  Quit  ]  [  Type  ]  [  Help  ]  [  Write ]
     [  Dump  ]

            Write partition table to disk (this might destroy data)
```

- `Write`
- `Quit`

###### Double Check Partition

```shell-session
root@archiso ~ # fdisk -l
Disk /dev/sda: 256 GiB, 274877906944 bytes, 536870912 sectors
Disk model: VBOX HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 1355000F-BBCD-634E-82AD-5AA1BCB6064A

Device     Start     End Sectors Size Type
/dev/sda1   2048 2099199 2097152   1G EFI System


Disk /dev/loop0: 688.47 MiB, 721911808 bytes, 1409984 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
```

```shell-session
root@archiso ~ # shutdown now
```

## Install Windows

- [if not bypass Windows 11 hardware check] enable "Secure Boot"
- boot Windows ISO

### Partitioning

![Before Partitioning](https://cdn.liblaf.me/img/2023/2023-03-08T062206Z.png)

![After Partitioning](https://cdn.liblaf.me/img/2023/2023-03-08T062232Z.png)

## Install Arch Linux

- disable "Secure Boot"
- boot Arch Linux ISO

### [Optional] Connect from Another Device

### Partitioning

```shell-session
root@archiso ~ # fdisk -l
Disk /dev/sda: 256 GiB, 274877906944 bytes, 536870912 sectors
Disk model: VBOX HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 1355000F-BBCD-634E-82AD-5AA1BCB6064A

Device       Start       End   Sectors  Size Type
/dev/sda1     2048   2099199   2097152    1G EFI System
/dev/sda2  2099200   2131967     32768   16M Microsoft reserved
/dev/sda3  2131968 268437503 266305536  127G Microsoft basic data


Disk /dev/loop0: 688.47 MiB, 721911808 bytes, 1409984 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
root@archiso ~ # cfdisk
```

```
                                 Disk: /dev/sda
              Size: 256 GiB, 274877906944 bytes, 536870912 sectors
          Label: gpt, identifier: 1355000F-BBCD-634E-82AD-5AA1BCB6064A

    Device             Start         End    Sectors   Size Type
    /dev/sda1           2048     2099199    2097152     1G EFI System
    /dev/sda2        2099200     2131967      32768    16M Microsoft reserved
    /dev/sda3        2131968   268437503  266305536   127G Microsoft basic data
>>  /dev/sda4      268437504   536868863  268431360   128G Linux filesystem







 ┌────────────────────────────────────────────────────────────────────────────┐
 │Partition UUID: A5CE280D-AE22-AB4D-BB35-3A08BC98B95C                        │
 │Partition type: Linux filesystem (0FC63DAF-8483-4772-8E79-3D69D8477DE4)     │
 └────────────────────────────────────────────────────────────────────────────┘
     [ Delete ]  [ Resize ]  [  Quit  ]  [  Type  ]  [  Help  ]  [  Write ]
     [  Dump  ]

            Write partition table to disk (this might destroy data)
```

- `Write`
- `Quit`

```shell-session
root@archiso ~ # fdisk -l
Disk /dev/sda: 256 GiB, 274877906944 bytes, 536870912 sectors
Disk model: VBOX HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 1355000F-BBCD-634E-82AD-5AA1BCB6064A

Device         Start       End   Sectors  Size Type
/dev/sda1       2048   2099199   2097152    1G EFI System
/dev/sda2    2099200   2131967     32768   16M Microsoft reserved
/dev/sda3    2131968 268437503 266305536  127G Microsoft basic data
/dev/sda4  268437504 536868863 268431360  128G Linux filesystem


Disk /dev/loop0: 688.47 MiB, 721911808 bytes, 1409984 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
```

### archinstall

```shell-session
root@archiso ~ # archinstall
```

```
Set/Modify the below options

  Archinstall language           set: English (100%)
  Keyboard layout                set: us
  Mirror region                  set: []
  Locale language                set: en_US
  Locale encoding                set: UTF-8
  Drive(s)                       set: 1 Drive(s)
> Disk layout                    set: 4 Partitions
  Disk encryption
  Bootloader                     set: grub-install
  Swap                           set: True
  Hostname                       set: XPS-9320
  Root password                  set: None
  User account                   set: 1 User(s)
  Profile                        set: Profile(desktop)
  Audio                          set: pipewire
  Kernels                        set: ['linux', 'linux-lts', 'linux-zen']
  Additional packages            set: ['git', 'neovim']
  Network configuration          set: Use NetworkManager
  Timezone                       set: Asia/Shanghai
  Automatic time sync (NTP)      set: True
  Optional repositories          set: []

  Save configuration
  Install
  Abort
(Press "/" to search)
┌── Info ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Device: /dev/sda                                                                                                                    │
│                                                                                                                                     │
│    type  |               PARTUUID               |  wipe |  boot |  ESP  | mountpoint | encrypted |   start   |    size   | format   │
│ ----------------------------------------------------------------------------------------------------------------------------------- │
│  primary | ad8d5ed1-76cf-cf49-a736-89782bc63bcf | False |  True |  True |    /boot   |   False   |    2048   |  2097152  |  vfat    │
│  primary | ad5fd8af-9b3c-4c5e-b8dc-0aeb2a933dee | False | False | False |    None    |   False   |  2099200  |   32768   |  None    │
│  primary | 535b265a-fd89-44f3-aa5b-3252cd27a4ec | False | False | False |    None    |   False   |  2131968  | 266305536 |  ntfs    │
│  primary | 48dbcbd5-85ab-9d40-98c3-5b4c0473b8a8 |  True | False | False |      /     |   False   | 268437504 | 268431360 |  ext4    │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

- wait for the installation to complete

### Change Boot Order

## Post Installation

### Enable Secure Boot for Arch Linux

#### Install `yay`

```shell-session
$ sudo pacman --sync --needed git
$ git clone https://aur.archlinux.org/yay.git
$ cd yay
$ makepkg --install --syncdeps
```

#### Install Dependencies

```shell-session
$ yay --sync --needed sbctl sbsigntools shim-signed
```

#### Default `/boot` Layout

```shell-session
boot/
├── EFI/
│   ├── Boot/
│   │   └── bootx64.efi
│   └── Microsoft/
│       ├── Boot/
│       └── Recovery/
├── grub/
│   ├── fonts/
│   │   └── unicode.pf2
│   ├── grub.cfg
│   ├── grubenv
│   ├── locale/
│   │   └── *.mo
│   ├── themes/
│   │   └── starfield/
│   └── x86_64-efi/
│       └── *.mod
├── initramfs-linux-fallback.img
├── initramfs-linux-lts-fallback.img
├── initramfs-linux-lts.img
├── initramfs-linux-zen-fallback.img
├── initramfs-linux-zen.img
├── initramfs-linux.img
├── vmlinuz-linux
├── vmlinuz-linux-lts
└── vmlinuz-linux-zen
```

#### Remove Old Boot

::: danger

KNOW WHAT YOU ARE DOING !!!

KNOW WHAT YOU ARE DOING !!!

KNOW WHAT YOU ARE DOING !!!

:::

```shell-session
$ sudo rm --recursive /boot/EFI/Boot /boot/grub
```

#### Install GRUB

##### List All GRUB Modules

```shell-session
$ find /usr/lib/grub/x86_64-efi/ -name '*.mod' -type f -printf '%f\n' | cut --delimiter='.' --fields=1 | sort | tr '\n' ' '
acpi adler32 affs afs afsplitter ahci all_video aout appleldr archelp ata at_keyboard backtrace bfs bitmap bitmap_scale blocklist boot boottime bsd bswap_test btrfs bufio cacheinfo cat cbfs cbls cbmemc cbtable cbtime chain cmdline_cat_test cmp cmp_test configfile cpio cpio_be cpuid crc64 crypto cryptodisk cs5536 ctz_test date datehook datetime disk diskfilter div div_test dm_nv echo efifwsetup efi_gop efinet efitextmode efi_uga ehci elf eval exfat exfctest ext2 extcmd f2fs fat file fixvideo font fshelp functional_test gcry_arcfour gcry_blowfish gcry_camellia gcry_cast5 gcry_crc gcry_des gcry_dsa gcry_idea gcry_md4 gcry_md5 gcry_rfc2268 gcry_rijndael gcry_rmd160 gcry_rsa gcry_seed gcry_serpent gcry_sha1 gcry_sha256 gcry_sha512 gcry_tiger gcry_twofish gcry_whirlpool geli gettext gfxmenu gfxterm gfxterm_background gfxterm_menu gptsync gzio halt hashsum hdparm hello help hexdump hfs hfsplus hfspluscomp http iorw iso9660 jfs jpeg json keylayouts keystatus ldm legacycfg legacy_password_test linux linux16 loadbios loadenv loopback ls lsacpi lsefi lsefimmap lsefisystab lsmmap lspci lssal luks luks2 lvm lzopio macbless macho mdraid09 mdraid09_be mdraid1x memdisk memrw minicmd minix minix2 minix2_be minix3 minix3_be minix_be mmap morse mpi msdospart mul_test multiboot multiboot2 nativedisk net newc nilfs2 normal ntfs ntfscomp odc offsetio ohci part_acorn part_amiga part_apple part_bsd part_dfly part_dvh part_gpt part_msdos part_plan part_sun part_sunpc parttool password password_pbkdf2 pata pbkdf2 pbkdf2_test pcidump pgp plainmount play png priority_queue probe procfs progress raid5rec raid6rec random rdmsr read reboot regexp reiserfs relocator romfs scsi search search_fs_file search_fs_uuid search_label serial setjmp setjmp_test setpci sfs shift_test signature_test sleep sleep_test smbios spkmodem squash4 strtoull_test syslinuxcfg tar terminal terminfo test test_blockarg testload testspeed tftp tga time tpm tr trig true udf ufs1 ufs1_be ufs2 uhci usb usb_keyboard usbms usbserial_common usbserial_ftdi usbserial_pl2303 usbserial_usbdebug usbtest video video_bochs video_cirrus video_colors video_fb videoinfo videotest videotest_checksum wrmsr xfs xnu xnu_uuid xnu_uuid_test xzio zfs zfscrypt zfsinfo zstd
```

##### Install GRUB

```shell-session
$ sudo grub-install --target=x86_64-efi --efi-directory=/boot --modules="all_video boot btrfs cat chain configfile echo efifwsetup efinet ext2 fat font gettext gfxmenu gfxterm gfxterm_background gzio halt help hfsplus iso9660 jpeg keystatus loadenv loopback linux ls lsefi lsefimmap lsefisystab lssal memdisk minicmd normal ntfs part_apple part_msdos part_gpt password_pbkdf2 png probe reboot regexp search search_fs_uuid search_fs_file search_label sleep smbios squash4 test true video xfs zfs zfscrypt zfsinfo play cpuid tpm cryptodisk luks lvm mdraid09 mdraid1x raid5rec raid6rec" --sbat /usr/share/grub/sbat.csv
Installing for x86_64-efi platform.
Installation finished. No error reported.
```

```shell-session
boot/
├── EFI/
│   ├── arch/
│   │   └── grubx64.efi
│   └── Microsoft/
│       ├── Boot/
│       └── Recovery/
├── grub/
│   ├── fonts/
│   │   └── unicode.pf2
│   ├── grubenv/
│   ├── locale/
│   │   └── *.mo
│   ├── themes/
│   │   └── starfield/
│   └── x86_64-efi/
│       └── *.mod
├── initramfs-linux-fallback.img
├── initramfs-linux-lts-fallback.img
├── initramfs-linux-lts.img
├── initramfs-linux-zen-fallback.img
├── initramfs-linux-zen.img
├── initramfs-linux.img
├── vmlinuz-linux
├── vmlinuz-linux-lts
└── vmlinuz-linux-zen
```

#### Create a Machine Owner Key[^1]

```shell-session
$ openssl req -newkey rsa:4096 -nodes -keyout MOK.key -new -x509 -sha256 -days 3650 -subj "/CN=my Machine Owner Key/" -out MOK.crt
$ openssl x509 -outform DER -in MOK.crt -out MOK.cer
```

```shell-session
$ sudo find /boot -maxdepth 1 -name 'vmlinuz-*' -exec bash -c 'if ! sbverify --list {} 2> /dev/null | grep -q "signature certificates"; then sbsign --key MOK.key --cert MOK.crt --output {} {}; fi' ';'
Signing Unsigned original image
Signing Unsigned original image
Signing Unsigned original image
$ sudo bash -c 'if ! sbverify --list /boot/EFI/arch/grubx64.efi 2> /dev/null | grep -q "signature certificates"; then sbsign --key MOK.key --cert MOK.crt --output /boot/EFI/arch/grubx64.efi /boot/EFI/arch/grubx64.efi; fi'
Signing Unsigned original image
```

[^1]: [Unified Extensible Firmware Interface/Secure Boot - ArchWiki](https://wiki.archlinux.org/title/Unified_Extensible_Firmware_Interface/Secure_Boot#shim_with_key)

#### Make GRUB Config

##### Edit `/etc/default/grub`

```diff
diff --git a/etc/default/grub.0 b/etc/default/grub
index caa8772..5840abb 100644
--- a/etc/default/grub.0
+++ b/etc/default/grub
@@ -1,6 +1,6 @@
 # GRUB boot loader configuration

-GRUB_DEFAULT=0
+GRUB_DEFAULT=saved
 GRUB_TIMEOUT=5
 GRUB_DISTRIBUTOR="Arch"
 GRUB_CMDLINE_LINUX_DEFAULT="loglevel=3 quiet"
@@ -51,13 +51,13 @@ GRUB_DISABLE_RECOVERY=true

 # Uncomment to make GRUB remember the last selection. This requires
 # setting 'GRUB_DEFAULT=saved' above.
-#GRUB_SAVEDEFAULT=true
+GRUB_SAVEDEFAULT=true

 # Uncomment to disable submenus in boot menu
-#GRUB_DISABLE_SUBMENU=y
+GRUB_DISABLE_SUBMENU=y

 # Probing for other operating systems is disabled for security reasons. Read
 # documentation on GRUB_DISABLE_OS_PROBER, if still want to enable this
 # functionality install os-prober and uncomment to detect and include other
 # operating systems.
-#GRUB_DISABLE_OS_PROBER=false
+GRUB_DISABLE_OS_PROBER=false
```

```shell-session
$ sudo grub-mkconfig --output=/boot/grub/grub.cfg
```

#### Install Everything

```shell-session
$ sudo mkdir --parents /boot/EFI/Boot
$ sudo cp /boot/EFI/arch/grubx64.efi /boot/EFI/Boot/grubx64.efi
$ sudo cp /usr/share/shim-signed/shimx64.efi /boot/EFI/Boot/bootx64.efi
$ sudo cp /usr/share/shim-signed/mmx64.efi /boot/EFI/Boot/mmx64.efi
```

```shell-session
$ sudo efibootmgr --unicode --disk /dev/sda --part 1 --create --label "shim" --loader /boot/EFI/Boot/bootx64.efi
```

#### My `/boot` Layout

```
boot/
├── EFI/
│   ├── arch/
│   │   └── grubx64.efi
│   ├── Boot/
│   │   ├── bootx64.efi
│   │   ├── grubx64.efi
│   │   └── mmx64.efi
│   └── Microsoft/
│       ├── Boot/
│       └── Recovery/
├── grub/
│   ├── fonts/
│   │   └── unicode.pf2
│   ├── grub.cfg
│   ├── grubenv
│   ├── locale/
│   │   └── *.mo
│   ├── themes/
│   │   └── starfield/
│   └── x86_64-efi/
│       └── *.mod
├── initramfs-linux-fallback.img
├── initramfs-linux-lts-fallback.img
├── initramfs-linux-lts.img
├── initramfs-linux-zen-fallback.img
├── initramfs-linux-zen.img
├── initramfs-linux.img
├── MOK.cer
├── vmlinuz-linux
├── vmlinuz-linux-lts
└── vmlinuz-linux-zen
```
