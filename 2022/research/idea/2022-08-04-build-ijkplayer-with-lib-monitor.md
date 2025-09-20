---
category:
  - Research
date: 2022-08-04T08:00:00+08:00
modified: 2025-09-20T23:07:39+08:00
tags:
  - Android
  - Clang
  - ijkplayer
  - NDK
title: Build ijkplayer with lib-monitor
---

## Environment Setup

- `ijkplayer`: [liblaf/ijkplayer: Android/iOS video player based on FFmpeg n3.4, with MediaCodec, VideoToolbox support.](https://github.com/liblaf/ijkplayer)
- `lib-monitor`: [liblaf/lib-monitor](https://github.com/liblaf/lib-monitor)
- `LLVM@9`: [llvm@9 — Homebrew Formulae](https://formulae.brew.sh/formula/llvm@9)
- `NDK-r14b`: [android-ndk-r14b-linux-x86_64.zip](https://dl.google.com/android/repository/android-ndk-r14b-linux-x86_64.zip)
- `NDK-r21e`: [android-ndk-r21e-linux-x86_64.zip](https://dl.google.com/android/repository/android-ndk-r21e-linux-x86_64.zip)
- `Android Studio 2.3.3`: [android-studio-ide-162.4069837-linux.zip](https://redirector.gvt1.com/edgedl/android/studio/ide-zips/2.3.3.0/android-studio-ide-162.4069837-linux.zip)

1. prepare the environment as shown above
2. follow instructions [below](#get-missing-parts-of-ndk) to get missing parts of `NDK`
3. configure variables in `ijkplayer/build.sh` and `lib-monitor/inserter/Makefile` according to your setup
4. click `AVD Manager` and create a device with the following system image:

| Release Name | API Level | ABI           | Target                      |
| ------------ | --------- | ------------- | --------------------------- |
| Nougat       | 25        | `armeabi-v7a` | Android 7.1.1 (Google APIs) |

### Get Missing Parts of `NDK`[^1]

::: info

We are going to use `NDK-r21e`.

:::

Version information is in file `${ANDROID_NDK}/toolchains/llvm/prebuilt/linux-x86_64/AndroidVersion.txt`.

```
9.0.9
based on r365631c3
```

1. visit the corresponding source at [clang-r365631c3 - platform/prebuilts/clang/host/linux-x86 - Git at Google](https://android.googlesource.com/platform/prebuilts/clang/host/linux-x86/+/refs/tags/ndk-r21e/clang-r365631c3/) and download [tgz](https://android.googlesource.com/platform/prebuilts/clang/host/linux-x86/+archive/refs/tags/ndk-r21e/clang-r365631c3.tar.gz)
2. extract the downloaded file and merge it with `${ANDROID_NDK}/toolchains/llvm/prebuilt/linux-x86_64`.

::: tip

You may want to remove `clang.real` and `clang++.real` under `${ANDROID_NDK}/toolchains/llvm/prebuilt/linux-x86_64/bin/`.

:::

## Build

1. launch Android Studio, select `android/ijkplayer/` and import
2. install dependencies according to logs from Android Studio
3. run the following scripts:

```bash
bash init-android.sh
bash build.sh
```

::: note

We choose to use `NDK-r21e` for `ffmpeg` and `NDK-r14b` for anything else. There are both `c` and `c++` sources elsewhere. However, the `-std=c99` option ( configured in `Android.mk` ) will cause an error in `NDK-r21e` ( with newer `clang++` ) but simply a warning in `NDK-r14b`.

:::

## Run

1. click `Run selected configuration` or press `shift + F10` in Android Studio
2. click `Sample` in Android Emulator
3. choose a video from the list and click

::: tip

When sliding the video list, the simulator may treat the wheel scroll as a click event, so the safe way is to hold down the mouse and drag.

:::

::: info

Sometimes the player would crash. Just try to reopen the video from the list. I'm currently working for a solution.

:::

## Debug

### ADB

By default, you may find the executable `adb` at `"${HOME}/Android/Sdk/platform-tools/adb"`. Here are some commonly used `adb` commands:

```bash
./adb devices [-l] # list connected devices (-l for long output)
./adb shell # run remote shell command (interactive shell if no command given)
```

You can enter interactive shell and `cd` to `/sdcard/` to see whether `recorder.cov` has been created.

### logcat

In Android Studio, click `6: Android Monitor` and click `logcat` tab to view `logcat`. In addition, you can change the level of logging and use the search box ( for example `"lib-monitor"` ) to filter logs.

## Reference

[^1]: [史上最优雅的 NDK 加载 pass 方案 - 先知社区](https://xz.aliyun.com/t/6643)
