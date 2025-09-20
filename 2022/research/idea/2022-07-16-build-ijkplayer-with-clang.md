---
category:
  - Research
date: 2022-07-16T08:00:00+08:00
modified: 2025-09-20T23:07:39+08:00
tags:
  - Android
  - Clang
  - ijkplayer
  - NDK
title: Build ijkplayer with Clang
---

## How to Build ijkplayer

### Before Build

1. Download NDK: [Unsupported Downloads · android/ndk Wiki](https://github.com/android/ndk/wiki/Unsupported-Downloads)
2. Download Android Studio: [Android Studio download archives \| Android Developers](https://developer.android.com/studio/archive)

### Configure Environment

```bash
export ANDROID_SDK=~/Android/Sdk
export ANDROID_NDK=~/programs/ndk/r14b
```

### Build

If no argument is pass to `compile-ffmpeg.sh` and `compile-ijk.sh`, only `armv7a` target will be build instead of all targets including `armv5`, `armv7a`, `arm64`, `x86`, `x86_64`.

```bash
./init-android.sh

# build ffmpeg
cd android/contrib
./compile-ffmpeg.sh clean
./compile-ffmpeg.sh # compile armv7a only

# build ijkplayer
cd ..
./compile-ijk.sh clean
./compile-ijk.sh # compile armv7a only

# Android Studio:
# Select android/ijkplayer/ and import
```

## Build ffmpeg with Clang

`compile-ffmpeg.sh` calls `tools/do-compile-ffmpeg.sh` to do the real compilation job, thus the main build process is present in `tools/do-compile-ffmpeg.sh`.

### Make NDK Standalone Toolchain

`do-compile-ffmpeg.sh` calls `$ANDROID_NDK/build/tools/make-standalone-toolchain.sh` to make toolchain on [line 202](https://github.com/bilibili/ijkplayer/blob/30eb9441945da795079492041a791c121d2b8206/android/contrib/tools/do-compile-ffmpeg.sh#L202). `make-standalone-toolchain.sh` then calls `$ANDROID_NDK/build/tools/make-standalone-toolchain.py` to install toolchain under `android/contrib/build/ffmpeg-armv7a/toolchain/`.

Under `android/contrib/build/ffmpeg-armv7a/toolchain/bin/`, you will find `clang`, `clang38`, `arm-linux-androideabi-clang`. `clang` and `arm-linux-androideabi-clang` are identical, both of which are shell script wrapper ( see below ) for `clang38`, a binary program.

```bash
#!/bin/bash
if [ "$1" != "-cc1" ]; then
    `dirname $0`/clang38 -target armv7a-none-linux-androideabi --sysroot `dirname $0`/../sysroot "$@"
else
    # target/triple already spelled out.
    `dirname $0`/clang38 "$@"
fi
```

`clang38` is directly copied from `$ANDROID_NDK`. In the python script `make-standalone-toolchain.py`, we can find the following function on line 133:

```python
def get_clang_path_or_die(host_tag):
    """Return the Clang path for our host or die."""
    clang_toolchain_path = os.path.join(
        NDK_DIR, 'toolchains/llvm/prebuilt', host_tag)
    if not os.path.exists(clang_toolchain_path):
        sys.exit('Could not find Clang: {}'.format(clang_toolchain_path))
    return clang_toolchain_path
```

That is to say, `clang38` probably comes from `$ANDROID_NDK/toolchains/llvm/prebuilt/linux-x86_64/`. And in fact, that's **true**! If we compare `clang38` and `$ANDROID_NDK/toolchains/llvm/prebuilt/clang`:

```bash
cmp $ANDROID_NDK/toolchains/llvm/prebuilt/linux-x86_64/bin/clang android/contrib/build/ffmpeg-armv7a/toolchain/bin/clang38
```

> The two compilers are **identical**!

### configurate ffmpeg

This step is quite short in `do-compile-ffmpeg.sh`, staring from [line 300](https://github.com/bilibili/ijkplayer/blob/30eb9441945da795079492041a791c121d2b8206/android/contrib/tools/do-compile-ffmpeg.sh#L300):

```bash
cd $FF_SOURCE
if [ -f "./config.h" ]; then
    echo 'reuse configure'
else
    which $CC
    ./configure $FF_CFG_FLAGS \
        --extra-cflags="$FF_CFLAGS $FF_EXTRA_CFLAGS" \
        --extra-ldflags="$FF_DEP_LIBS $FF_EXTRA_LDFLAGS"
    make clean
fi
```

`configure` is a bash script under `android/contrib/ffmpeg-armv7a/`. Help messages can be found in function `show_help()` on line 59. Toolchain options starts from line 331. By default, `arm-linux-androideabi-gcc` is used as C compiler ( `$cc` ). To use clang, we need to pass `--cc=clang` or `--cc=arm-linux-androideabi-clang` to `./configure`. The two clang wrapper are identical.

```diff
--- a/android/contrib/tools/do-compile-ffmpeg.sh
+++ b/android/contrib/tools/do-compile-ffmpeg.sh
@@ -214,7 +214,7 @@ echo "[*] check ffmpeg env"
 echo "--------------------"
 export PATH=$FF_TOOLCHAIN_PATH/bin/:$PATH
 #export CC="ccache ${FF_CROSS_PREFIX}-gcc"
-export CC="${FF_CROSS_PREFIX}-gcc"
+export CC="${FF_CROSS_PREFIX}-clang"
 export LD=${FF_CROSS_PREFIX}-ld
 export AR=${FF_CROSS_PREFIX}-ar
 export STRIP=${FF_CROSS_PREFIX}-strip
@@ -303,6 +303,8 @@ if [ -f "./config.h" ]; then
 else
     which $CC
     ./configure $FF_CFG_FLAGS \
+        --cc='clang' \
+        --host-cc='clang38' \
         --extra-cflags="$FF_CFLAGS $FF_EXTRA_CFLAGS" \
         --extra-ldflags="$FF_DEP_LIBS $FF_EXTRA_LDFLAGS"
     make clean
```

However, you would probably get an error message like this:

```shell-session
GNU assembler not found, install/update gas-preprocessor
```

Here is the reason. By default, `./configure` uses `$cc` as the assembler ( `$as` ). However, Clang 3.8 is somewhat incompatible with GNU when it comes to assembly code.

> Even if I skip the assembler test ( `function check_as()` ) in `configure`, it will fail when compiling.

One possible solution is to add `-fno-integrated-as` to Clang flags.[^1]

```diff
+        --cc='clang -fno-integrated-as' \
```

Or, explicitly tell `configure` to use `gcc` as assembler:

```diff
+        --as='arm-linux-androideabi-gcc' \
+        --cc='clang' \
```

> It **works**!

### Suppress Warnings

Clang generates lots of warnings. To suppress them, add the following flags to Clang flags.

#### Suppress "deprecated declarations"

Add `-Wno-deprecated-declarations` to Clang flags.

#### Suppress "unknown warning option"

Add `-Wno-unknown-warning-option` to Clang flags.

#### Suppress "unused function"

Add `-Wno-unused-function` to Clang flags. I tried to add the flag directly in `do-compile-ffmpeg.sh` as following, but didn't work. Perhaps `-Wunused-function` is added back somewhere else in `configure`.

```diff
--- a/android/contrib/tools/do-compile-ffmpeg.sh
+++ b/android/contrib/tools/do-compile-ffmpeg.sh
@@ -214,7 +214,7 @@ echo "[*] check ffmpeg env"
 echo "--------------------"
 export PATH=$FF_TOOLCHAIN_PATH/bin/:$PATH
 #export CC="ccache ${FF_CROSS_PREFIX}-gcc"
-export CC="${FF_CROSS_PREFIX}-gcc"
+export CC="${FF_CROSS_PREFIX}-clang"
 export LD=${FF_CROSS_PREFIX}-ld
 export AR=${FF_CROSS_PREFIX}-ar
 export STRIP=${FF_CROSS_PREFIX}-strip
@@ -303,6 +303,8 @@ if [ -f "./config.h" ]; then
 else
     which $CC
     ./configure $FF_CFG_FLAGS \
+        --cc='clang -fno-integrated-as -Wno-deprecated-declarations -Wno-unknown-warning-option -Wno-unused-function' \
+        --host-cc='clang38' \
         --extra-cflags="$FF_CFLAGS $FF_EXTRA_CFLAGS" \
         --extra-ldflags="$FF_DEP_LIBS $FF_EXTRA_LDFLAGS"
     make clean
```

## Upgrade Clang to Higher Version

The version of Clang which NDK r14b uses is `3.8`. It's a little bit **old**. I failed to compile ffmpeg with NDK r15 or higher. Instead, I find a tricky method to use later version of Clang.

As mentioned in the previous, the Clang used to compile ffmpeg comes from NDK toolchain. If we replace the Clang in NDK, we may be able to use a different version of Clang. NDK r25 comes with Clang 14, so I can:

```shell-session
(base) liblaf@xps:~/programs/ndk/r14b/toolchains/llvm/prebuilt/linux-x86_64/bin$ mv clang clang.old # backup clang
(base) liblaf@xps:~/programs/ndk/r14b/toolchains/llvm/prebuilt/linux-x86_64/bin$ ln --symbolic ~/programs/ndk/r25/toolchains/llvm/prebuilt/linux-x86_64/bin/clang clang # link clang in NDK r14 to clang in NDK r25
```

> Do Not Copy! That won't work! **Link** Instead!

Even better, Clang 14 is compatible with GNU assembler, so `-fno-integrated-as` is unnecessary any more.

## Compatibility Test

| SDK    | NDK  | Gradle | Android Studio | compile ffmpeg     | compile ijk        | Emulator           |
| ------ | ---- | ------ | -------------- | ------------------ | ------------------ | ------------------ |
| 25.0.3 | r10e | 2.14.1 | 2.3.2          | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| 25.0.3 | r11c | 2.14.1 | 2.3.2          | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| 25.0.3 | r12b | 2.14.1 | 2.3.2          | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| 25.0.3 | r13b | 2.14.1 | 2.3.2          | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| 25.0.3 | r14b | 2.14.1 | 2.3.2          | :o:                | :white_check_mark: | :white_check_mark: |
| 25.0.3 | r15c | 2.14.1 | 2.3.2          | :x:                |                    |                    |
| 28.0.3 | r14b | 2.14.1 | 3.6.3          | :white_check_mark: | :x:                |                    |
| 25.0.3 | r21e | 2.14.1 | 2.3.3          | :o:                | :white_check_mark: | poor performance   |

When building with NDK r14b, you may encounter an error like this:

```shell-session
BFD: libncurses.so.5: cannot open shared object file: No such file or directory
```

The solution is to install the corresponding dependency:[^2]

```bash
sudo apt install libncurses5
```

### Discussion on GitHub

Here are some discussions on [GitHub](https://github.com/bilibili/ijkplayer). I tried some of their methods but it didn't work.

1. [编译出错 · Issue #3378 · bilibili/ijkplayer](https://github.com/bilibili/ijkplayer/issues/3378)
2. [You need the NDKr10e or later · Issue #2752 · bilibili/ijkplayer](https://github.com/bilibili/ijkplayer/issues/2752)

## Reference

[^1]: [c - Unknown directive .altmacro error happens when using android-ndk standalone toolchain - Stack Overflow](https://stackoverflow.com/questions/47938599/unknown-directive-altmacro-error-happens-when-using-android-ndk-standalone-tool)

[^2]: [linux - error while loading shared libraries: libncurses.so.5: - Stack Overflow](https://stackoverflow.com/questions/17005654/error-while-loading-shared-libraries-libncurses-so-5)
