---
category:
  - Research
title: How to Build Telegram for Android
date: "2022-09-21T00:00:00+08:00"
tags:
  - Android
  - NDK
  - Telegram
---

## TL;DR

Clone from [liblaf/Telegram](https://github.com/liblaf/Telegram) and you are good to go. I have had `release.keystore` and `google-services.json` prepared.

## Environment

### Recommended Environment

- Android Studio 3.4
- Android NDK rev.20
- Android SDK 8.1

### I am using

- Android Studio 2021.3.1.16
- Android NDK 21.4.7075529
- Android SDK 31.0.0

## Compilation Guide[^1]

1. Download the Telegram source code from https://github.com/DrKLO/Telegram ( git clone https://github.com/DrKLO/Telegram.git )
2. Copy your release.keystore into TMessagesProj/config
3. Fill out RELEASE_KEY_PASSWORD, RELEASE_KEY_ALIAS, RELEASE_STORE_PASSWORD in gradle.properties to access your release.keystore
4. Go to https://console.firebase.google.com/, create two android apps with application IDs org.telegram.messenger and org.telegram.messenger.beta, turn on firebase messaging and download google-services.json, which should be copied to the same folder as TMessagesProj.
5. Open the project in the Studio (note that it should be opened, NOT imported).
6. Fill out values in TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java – there's a link for each of the variables showing where and which data to obtain.
7. You are ready to compile Telegram.

## Generate `release.keystore`

In Android Studio

1. Find in Menu Bar: "Build" > "Generate Signed Bundle / APK ..."
2. Choose "APK" and click "Next"
3. Click "Create New ..." and fill in necessary fields
4. Whatever

## ASan compatibility

Telegram depends on some prebuilt static libraries. However, ASan requires a shared build.[^2] I haven't find a way to use ASan yet.

[^1]: [DrKLO/Telegram: Telegram for Android source](https://github.com/DrKLO/Telegram#compilation-guide)

[^2]: [Address Sanitizer | Android NDK | Android Developers](https://developer.android.com/ndk/guides/asan)
