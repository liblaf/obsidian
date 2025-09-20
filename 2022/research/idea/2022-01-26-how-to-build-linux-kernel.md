---
category:
- Research
date: '2022-01-26T00:00:00+08:00'
tags:
- C/C++
- Clang
- LLVM
- Linux_Kernel
title: How to Build Linux Kernel
---

|         Environment          |                                                                         Version                                                                          |
| :--------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------: |
|        Host Processor        |                                                    Intel(R) Core(TM) i7-10710U CPU @ 1.10GHz 1.61 GHz                                                    |
|           Host OS            |                                                              Windows 11 Pro Education 21H2                                                               |
| VMware(R) Workstation 16 Pro |                                                                  16.2.2 build-19200509                                                                   |
|      Virtual Machine OS      | [Ubuntu 20.04.3 (amd64, Desktop LiveDVD) (tsinghua.edu.cn)](https://mirrors.tuna.tsinghua.edu.cn/ubuntu-releases/focal/ubuntu-20.04.3-desktop-amd64.iso) |

## Download the Source Code

Visit the [official kernel website](https://www.kernel.org/) and download the [linux-5.13.tar.gz (kernel.org)](https://mirrors.edge.kernel.org/pub/linux/kernel/v5.x/linux-5.13.tar.gz). The downloaded file contains a compressed source code.

## Extract the Source Code

```bash
tar --extract --gzip --file linux-5.13.tar.gz
```

## Install Required Packages

Install additional packages before building a kernel. To do so, run this command:[^1][^2]

```bash
sudo apt install build-essential flex bison libelf-dev libssl-dev dwarves zstd
```

The command we used above installs the following packages:

|               **Package**                |                                                **Package description**                                                |
| :--------------------------------------: | :-------------------------------------------------------------------------------------------------------------------: |
|                  `git`                   | Tracks and makes a record of all changes during development in the source code. It also allows reverting the changes. |
|                `fakeroot`                |                                 Packaging tool that makes the fake root environment.                                  |
|            `build-essential`             |                               Installs development tools such as C, C++, gcc, and g++.                                |
|              `ncurses-dev`               |                          Programming library that provides API for the text-based terminals.                          |
|                `xz-utils`                |                                   Provides fast file compression and decompression.                                   |
|               `libssl-dev`               |                    Supports SSL and TSL that encrypt data and make the internet connection secure.                    |
|         `bc` (Basic Calculator)          |               A mathematical scripting language that supports the interactive execution of statements.                |
| `flex` (Fast Lexical Analyzer Generator) |                           Generates lexical analyzers that convert characters into tokens.                            |
|               `libelf-dev`               |             Issues a shared library for managing ELF files (executable files, core dumps and object code)             |
|                 `bison`                  |                        GNU parser generator that converts grammar description to a C program.                         |

## Configure Kernel

The Linux kernel source code comes with the default configuration. However, you can adjust it to your needs. To do so, follow the steps below:

Navigate to the `linux-5.13.0`. directory using the `cd` command:

```bash
cd linux-5.13.0
```

To make changes to the configuration file, run the `make` command:

```bash
make menuconfig
```

If no `.config` file exists, defaults found in `/boot/config-$(uname -r)` will be used. The command launches several scripts, which then open the configuration menu.

The configuration menu includes options such as firmware, file system, network, and memory settings. Use the arrows to make a selection or choose **Help** to learn more about the options. When you finish making the changes, select **Save**, and then exit the menu.

> **Note:** Changing settings for some options can lead to a non-functional kernel. If you are unsure what to change, leave the default settings.

In your kernel configuration file you will find this line:[^3]

```properties
CONFIG_SYSTEM_TRUSTED_KEYS="debian/canonical-certs.pem"
```

Change it to this:

```properties
CONFIG_SYSTEM_TRUSTED_KEYS=""
```

Depending on your source structure you might be able to do it via command line. Examples:

```bash
scripts/config --disable SYSTEM_TRUSTED_KEYS
```

or

```bash
scripts/config --set-str SYSTEM_TRUSTED_KEYS ""
```

Another key has been added to the default Canonical kernel configuration since this answer was posted:

```properties
CONFIG_SYSTEM_REVOCATION_KEYS="debian/canonical-revoked-certs.pem"
```

So, it also needs to be dealt with for user kernel compiles to complete:

```bash
scripts/config --disable SYSTEM_REVOCATION_KEYS
```

## Build the Kernel

Start building the kernel by running the following command:

```bash
make --jobs=$(nproc --all)
```

LLVM has substitutes for GNU binutils utilities. Kbuild supports `LLVM=1` to enable them.[^4]

```bash
make LLVM=1
```

They can be enabled individually. The full list of the parameters:

```bash
make CC=clang-12 LD=ld.lld-12 AR=llvm-ar-12 NM=llvm-nm-12 STRIP=llvm-strip-12 \
  OBJCOPY=llvm-objcopy-12 OBJDUMP=llvm-objdump-12 READELF=llvm-readelf-12 \
  HOSTCC=clang-12 HOSTCXX=clang++-12 HOSTAR=llvm-ar-12 HOSTLD=ld.lld-12
```

> **Note:** The version of kernel and compiler matters!!! If you cannot pass compilation, try another release of kernel or compiler.

The process of building and compiling the Linux kernel takes some time to complete.

The terminal lists all Linux kernel components: memory management, hardware device drivers, filesystem drivers, network drivers, and process management.

Install the required modules with this command:

```bash
sudo make modules_install
```

Finally, install the kernel by typing:

```bash
sudo make install
```

## Change the Default Boot Kernel

You may press `Esc` to enter the boot menu when staring up, but that's a bit troublesome. Instead, use the following commands to list GRUB's menu entries:

```bash
awk -F\' '$1=="menuentry " || $1=="submenu " {print i++ " : " $2}; /\tmenuentry / {print "\t" i-1">"j++ " : " $2};' /boot/grub/grub.cfg
```

For example, I got the output:

```
0 : Ubuntu
1 : Advanced options for Ubuntu
        1>0 : Ubuntu, with Linux 5.13.0-30-generic
        1>1 : Ubuntu, with Linux 5.13.0-30-generic (recovery mode)
        1>2 : Ubuntu, with Linux 5.13.0
        1>3 : Ubuntu, with Linux 5.13.0 (recovery mode)
        1>4 : Ubuntu, with Linux 5.11.0-27-generic
        1>5 : Ubuntu, with Linux 5.11.0-27-generic (recovery mode)
2 : Memory test (memtest86+)
3 : Memory test (memtest86+, serial console 115200)
```

For me, the desired default kernel to boot from is `1>2 : Ubuntu, with Linux 5.13.0`. Open the `/etc/default/grub` file and change the value of `GRUB_DEFAULT` to `"1>2"`, like this:[^5]

```properties
GRUB_DEFAULT="1>2"
```

- `1` in `1>2` indicates the **second** entry of the main menu.
- `2` in `1>2` indicates the **third** entry of the submenu.
- There is **no space** before and after the greater-than sign (`>`) in `1>2`.
- Use a set of quotation marks to enclose `1>2`.

Run `update-grub` afterwards to update `/boot/grub/grub.cfg`:

```bash
sudo update-grub
```

If you stuck on `Loading inital ramdisk...` after reboot, try adding `IUCODE_TOOL_INITRAMFS=no` to `/etc/default/intel-microcode` and then re-running `update-initramfs -u` to remove the microcode bits from the `initramfs` image.[^6]

## Reference

[^1]: [How To Build Linux Kernel {Step-By-Step} \| phoenixNAP KB](https://phoenixnap.com/kb/build-linux-kernel)
[^2]: [compilation - BTF: .tmp_vmlinux.btf: pahole (pahole) is not available - Stack Overflow](https://stackoverflow.com/questions/61657707/btf-tmp-vmlinux-btf-pahole-pahole-is-not-available)
[^3]: [Compiling the kernel 5.11.11 - Ask Ubuntu](https://askubuntu.com/questions/1329538/compiling-the-kernel-5-11-11)
[^4]: [Building Linux with Clang/LLVM — The Linux Kernel documentation](https://www.kernel.org/doc/html/v5.13/kbuild/llvm.html)
[^5]: [How Do I Change the Default Boot Kernel in Ubuntu?\_Elastic Cloud Server_Troubleshooting_Linux Issues_HUAWEI CLOUD](https://support.huaweicloud.com/intl/en-us/trouble-ecs/ecs_trouble_0327.html)
[^6]: [boot - Stuck on "Loading initial ramdisk..." after upgrading - Ask Ubuntu](https://askubuntu.com/questions/1145535/stuck-on-loading-initial-ramdisk-after-upgrading)
