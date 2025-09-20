---
category:
  - Posts
date: 2022-09-10T08:00:00+08:00
modified: 2025-09-20T23:07:39+08:00
tags:
  - Dell
  - IRST
  - Windows
title: Windows Setup
---

::: info

Device: Dell XPS 9320

:::

## Install Windows

### Create Bootable USB Drive

1. Use [Rufus](http://rufus.ie/en/) to create bootable USB drive.
2. Download [Intel Rapid Storage Technology Driver and Application](https://dl.dell.com/FOLDER08107340M/4/Intel-Rapid-Storage-Technology-Driver-and-Application_0F5G4_WIN64_19.2.0.1003_A01_03.EXE) from [Dell Support](https://www.dell.com/support/) and extract to the USB drive, for example `E:\extra\Intel-Rapid-Storage-Technology-Driver-and-Application_0F5G4_WIN64_19.2.0.1003_A01_03\`.
3. Download [Intel AX211 and Killer 1690/1650/1675 Wi-Fi Controller Driver](https://dl.dell.com/FOLDER08667453M/4/Intel-AX211-and-Killer-1690-1650-1675-Wi-Fi-Controller_KHHGP_WIN_3.1222.614_A03_03.EXE) from [Dell Support](https://www.dell.com/support/) and save to the USB drive, for example `E:\extra\Intel-AX211-and-Killer-1690-1650-1675-Wi-Fi-Controller_55NTY_WIN_3.1122.1141.0_A02_02\`.
4. Download [KSM Script](https://kms.cangshui.net/) and save to the USB drive, for example, `E:\extra\KMS-Cangshui.net.bat`.
5. Download [Clash for Windows](https://github.com/Fndroid/clash_for_windows_pkg/releases/) and save the installer to the USB drive, for example, `E:\extra\Clash.for.Windows.Setup.0.19.26.exe`.
6. Download [Support Assist](https://www.dell.com/support/contents/en-us/article/product-support/self-support-knowledgebase/software-and-downloads/supportassist) and save the installer to the USB drive, for example, `E:\extra\SupportAssistInstaller.exe`.

### Install Windows

1. Boot from the USB drive.
2. If no storage drivers can be found, load drivers from `E:\extra\Intel-Rapid-Storage-Technology-Driver-and-Application_0F5G4_WIN64_19.2.0.1003_A01_03\15063\Drivers\Drivers\VMD\`.[^1]
3. Delete all partitions and allocate three partitions: `512GB + 512GB + remaining = 524288MB + 524288MB + remaining`. The first two partitions are for windows, one for windows installation and one for data storage. The remaining partition is reserved for Ubuntu installation.

### Post Installation

1. Open `Device Manager`, manually update driver of `Network Controller`, search for drivers in the USB drive `E:\extra\Intel-AX211-and-Killer-1690-1650-1675-Wi-Fi-Controller_55NTY_WIN_3.1122.1141.0_A02_02\`.
2. Activate Windows with [KSM Script](https://kms.cangshui.net/) saved in USB drive.
3. Install [Support Assist](https://www.dell.com/support/contents/en-us/article/product-support/self-support-knowledgebase/software-and-downloads/supportassist) with the installer from USB drive.

## Essential Software

1. [沧水的 KMS 服务 – Kms|Windows 激活|Office 激活|Windows 下载|Office 下载|搭建 KMS 服务器 (cangshui.net)](https://kms.cangshui.net/)
2. [Bandizip · Free zip, 7z, unzip, unrar Archiver · Fast and easy (bandisoft.com)](https://www.bandisoft.com/bandizip/)
3. [Windows Subsystem for Linux Documentation | Microsoft Docs](https://docs.microsoft.com/en-us/windows/wsl/)
4. [Visual Studio: IDE and Code Editor for Software Developers and Teams (microsoft.com)](https://visualstudio.microsoft.com/)
5. [Visual Studio Code - Code Editing. Redefined](https://code.visualstudio.com/)
6. [Typora — a markdown editor, markdown reader.](https://typora.io/)
7. [Office Tool Plus Website - Easy to Deploy Office (landian.vip)](https://otp.landian.vip/en-us/)
8. [VLC: Official site - Free multimedia solutions for all OS! - VideoLAN](https://www.videolan.org/)
9. From [GitHub](https://github.com/)
   1. [Rufus - Create bootable USB drives the easy way](http://rufus.ie/en/)
   2. [Fndroid/clash_for_windows_pkg: A Windows/macOS GUI based on Clash (github.com)](https://github.com/Fndroid/clash_for_windows_pkg)
   3. [microsoft/PowerToys: Windows system utilities to maximize productivity (github.com)](https://github.com/microsoft/PowerToys)
   4. [zhongyang219/TrafficMonitor: 这是一个用于显示当前网速、CPU 及内存利用率的桌面悬浮窗软件，并支持任务栏显示，支持更换皮肤。 (github.com)](https://github.com/zhongyang219/TrafficMonitor)
   5. [ciderapp/Cider: A new cross-platform Apple Music experience based on Electron and Vue.js written from scratch with performance in mind. 🚀 (github.com)](https://github.com/ciderapp/Cider)
10. [Pulse Secure](https://deny.tsinghua.edu.cn/)
11. [Adobe Series](https://weibo.com/vposy)
    1. Adobe Acrobat DC
12. [腾讯会议官方——腾讯会议 会开会 (tencent.com)](https://meeting.tencent.com/)
13. [WeChat for Windows (qq.com)](https://pc.weixin.qq.com/?lang=en_US)
14. [百度网盘-免费云盘丨文件共享软件丨超大容量丨存储安全 (baidu.com)](https://pan.baidu.com/)

## Optional Software

1. [CPU-Z | Softwares | CPUID](https://www.cpuid.com/softwares/cpu-z.html)
2. [HWMONITOR | Softwares | CPUID](https://www.cpuid.com/softwares/hwmonitor.html)
3. [Adobe Series](https://weibo.com/vposy)
   1. Adobe Premiere Pro
   2. Adobe Photoshop
   3. Adobe Illustrator
   4. Adobe Audition
4. [Open Broadcaster Software | OBS (obsproject.com)](https://obsproject.com/)
5. [Autodesk - Account](https://manage.autodesk.com/products)
   1. AutoCAD

## Reference

[^1]: [Intel 11th Generation Processors, No Drives Can Be Found During Windows 10 and Windows 11 Installation | Dell US](https://www.dell.com/support/kbdoc/en-us/000188116/intel-11th-generation-processors-no-drives-can-be-found-during-windows-10-installation)
