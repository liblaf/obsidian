---
category:
- Posts
title: Run Tencent Meeting on Ubuntu 22.04
date: '2022-07-20T00:00:00+08:00'
tags:
- Linux
- Tencent Meeting
- Ubuntu
- Ubuntu 22.04
---

## Environment

| Name            | Value              |
| --------------- | ------------------ |
| OS              | Ubuntu 22.04 LTS   |
| Tencent Meeting | 3.9.0.1 2022-07-20 |

## Problem

```shell-session
检测到窗口系统采用wayland协议，腾讯会议暂不兼容，程序即将退出！
```

## Solution

### Login with Ubuntu on Xorg

To login to Ubuntu 22.04 using Xorg click on the gear button and select `Ubuntu on Xorg` option before you login.

![Login to Ubuntu 22.04 using Wayland display server](https://linuxconfig.org/wp-content/uploads/2022/01/02-how-to-enable-disable-wayland-on-ubuntu-22-04-desktop.png)

### Disable Wayland[^1]

#### Step 1

The default display manager for the GNOME desktop environment is GDM3. Therefore, we will edit the `/etc/gdm3/custom.conf` file to either disable or enable Wayland. [Open a command line terminal](https://linuxconfig.org/how-to-open-a-terminal-on-ubuntu-xenial-xerus-16-04-linux) and use nano or your favorite text editor to open this file with [root permissions](https://linuxconfig.org/how-to-login-as-root-user-on-ubuntu-xenial-xerus-16-04-linux-desktop).

```shell-session
$ sudo vim /etc/gdm3/custom.conf
```

#### Step 2

Within this file, look for the line that says `#WaylandEnable=false`. You can uncomment this line and either set it to true or false, depending on whether you want Wayland enabled or not.

##### Enable Wayland

```ini
WaylandEnable=true
```

##### Disable Wayland

```ini
WaylandEnable=false
```

![Editing the Wayland settings inside the GDM3 configuration file](https://linuxconfig.org/wp-content/uploads/2022/01/01-how-to-enable-disable-wayland-on-ubuntu-22-04-desktop.png "Editing the Wayland settings inside the GDM3 configuration file")

#### Step 3

After you have made the desired changes, save this file and exit it. You will need to restart GDM3 or reboot your Ubuntu 22.04 desktop for the changes to take effect.

```shell-session
$ sudo systemctl restart gdm3
```

## Reference

[^1]: [How to enable/disable wayland on Ubuntu 22.04 Desktop - Linux Tutorials - Learn Linux Configuration](https://linuxconfig.org/how-to-enable-disable-wayland-on-ubuntu-22-04-desktop)
