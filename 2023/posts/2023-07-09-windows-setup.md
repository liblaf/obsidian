---
category:
- Posts
date: '2023-07-09T00:00:00+08:00'
modified: 2025-09-20 21:48:51+08:00
title: Windows Setup (XPS 9320)
tags:
- Dell
- XPS 9320
---

::: info
Device: Dell Inc. XPS 9320
:::

## Prepare Ventoy

### Download Windows ISO

```powershell
wget https://github.com/pbatard/Fido/raw/master/Fido.ps1 -OutFile Fido.ps1
& .\Fido.ps1 -Lang English
```

### Prepare Packages

#### Clash for Windows

- Download [Clash for Windows](https://github.com/Fndroid/clash_for_windows_pkg/releases)
- `clash-config.txt`: Clash Subscription URL

#### Wi-Fi Controller Driver

- Download [Intel AX211 and Killer 1690/1675/1650 Wi-Fi Controller Driver and Killer Intelligence Center Application](https://www.dell.com/support/home/en-us/product-support/product/xps-13-9320-laptop/drivers)

#### KMS

- Download [KMS-Clangshui.net.bat](https://kms.cangshui.net)

```powershell
wget https://kms.cangshui.net/kms/KMS-Cangshui.net.bat -OutFile KMS-Cangshui.net.bat
```

## UTC in Microsoft Windows[^1]

```powershell
reg add "HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\TimeZoneInformation" /v RealTimeIsUniversal /d 1 /t REG_DWORD /f
```

[^1]: [UTC in Microsoft Windows - System time - ArchWiki](https://wiki.archlinux.org/title/System_time#UTC_in_Microsoft_Windows)

## Install Packages[^2]

```powershell
winget install --id="appmakes.Typora" --exact --accept-package-agreements --accept-source-agreements
winget install --id="Baidu.BaiduNetdisk" --exact --accept-package-agreements --accept-source-agreements
winget install --id="Bandisoft.Bandizip" --exact --accept-package-agreements --accept-source-agreements
winget install --id="CPUID.CPU-Z" --exact --accept-package-agreements --accept-source-agreements
winget install --id="DigitalScholar.Zotero" --exact --accept-package-agreements --accept-source-agreements
winget install --id="Fndroid.ClashForWindows" --exact --accept-package-agreements --accept-source-agreements
winget install --id="JohnMacFarlane.Pandoc" --exact --accept-package-agreements --accept-source-agreements
winget install --id="Microsoft.VisualStudioCode" --exact --accept-package-agreements --accept-source-agreements
winget install --id="PrimateLabs.Geekbench.6" --exact --accept-package-agreements --accept-source-agreements
winget install --id="Tencent.TencentMeeting" --exact --accept-package-agreements --accept-source-agreements
winget install --id="Tencent.WeChat" --exact --accept-package-agreements --accept-source-agreements
```

[^2]: [winstall - GUI for Windows Package Manager](https://winstall.app)

## Install Microsoft Office[^3]

```powershell
cd "${HOME}\Downloads"
wget "https://otp.landian.vip/redirect/download.php?type=runtime&site=yuntu" -OutFile "${HOME}\Downloads\office-tool.zip"
tar -x -f "${HOME}\Downloads\office-tool.zip"
& "${HOME}\Downloads\Office Tool\Office Tool Plus.exe"
```

[^3]: [Office Tool Plus Website - Easy to Deploy Office](https://otp.landian.vip)
