---
category:
  - Research
title: How To Filter JNI Interface in LLVM IR
date: "2022-08-11T00:00:00+08:00"
tags:
  - C_Cpp
  - JNI
  - Java
  - LLVM
---

`JNIEnv` ( aka `const struct JNINativeInterface*`, defined in `jni.h` ) provides a rich interface for accessing Java variables and methods in C/C++. All interfaces are members of `struct.JNINativeInterface`. You can read `jni.h` for more details.

## Use `JNIEnv` in C/C++

::: info

The `jni.h` bundled in the `NDK LLVM toolchain` is usually located at `${ANDROID_NDK}/toolchains/llvm/prebuilt/linux-x86_64/sysroot/usr/include/jni.h`.

:::

Here is a simple example showing how to use `JNIEnv`. In the example below, you need to pass the Class ID and Method ID to the interface so that `JNI` will call the appropriate method for you.

```c
jfloat J4AC_android_media_AudioTrack__getMaxVolume(JNIEnv *env) {
  return (*env)->CallStaticFloatMethod(
      env, class_J4AC_android_media_AudioTrack.id,
      class_J4AC_android_media_AudioTrack.method_getMaxVolume);
}
```

## How `JNIEnv` Is Called in `LLVM IR`

After translating the example to `LLVM IR` with `-O0` option ( no optimization ), we get

```llvm
; Function Attrs: noinline nounwind sspstrong uwtable
define float @J4AC_android_media_AudioTrack__getMaxVolume(%struct.JNINativeInterface**) #0 !dbg !1243 {
  %2 = alloca %struct.JNINativeInterface**, align 4
  store %struct.JNINativeInterface** %0, %struct.JNINativeInterface*** %2, align 4
  call void @llvm.dbg.declare(metadata %struct.JNINativeInterface*** %2, metadata !1246, metadata !DIExpression()), !dbg !1247
  %3 = load %struct.JNINativeInterface**, %struct.JNINativeInterface*** %2, align 4, !dbg !1248
  %4 = load %struct.JNINativeInterface*, %struct.JNINativeInterface** %3, align 4, !dbg !1249
  %5 = getelementptr inbounds %struct.JNINativeInterface, %struct.JNINativeInterface* %4, i32 0, i32 135, !dbg !1250
  %6 = load float (%struct.JNINativeInterface**, i8*, %struct._jmethodID*, ...)*, float (%struct.JNINativeInterface**, i8*, %struct._jmethodID*, ...)** %5, align 4, !dbg !1250
  %7 = load %struct.JNINativeInterface**, %struct.JNINativeInterface*** %2, align 4, !dbg !1251
  %8 = load i8*, i8** getelementptr inbounds (%struct.J4AC_android_media_AudioTrack, %struct.J4AC_android_media_AudioTrack* @class_J4AC_android_media_AudioTrack, i32 0, i32 0), align 4, !dbg !1252
  %9 = load %struct._jmethodID*, %struct._jmethodID** getelementptr inbounds (%struct.J4AC_android_media_AudioTrack, %struct.J4AC_android_media_AudioTrack* @class_J4AC_android_media_AudioTrack, i32 0, i32 3), align 4, !dbg !1253
  %10 = call float (%struct.JNINativeInterface**, i8*, %struct._jmethodID*, ...) %6(%struct.JNINativeInterface** %7, i8* %8, %struct._jmethodID* %9), !dbg !1254
  ret float %10, !dbg !1255
}
```

`%10` is a `CallInst` which calls the `CallStaticFloatMethod` function. The called operand is a `LoadInst`, `%6`, which loads the function from the pointer `%5`. `%5` is a pointer to the element in `struct.JNINativeInterface`. The last operand of the `GetElementPtrInst` `%5` is `i32 135`. With an alignment of 4 ( usually on 32-bit machines ), it means an offset of `135 * 4 = 540`.

Therefore, we can obtain the index of `struct` members like this:

```cpp
auto call_inst = dyn_cast<CallInst>(&instruction);
if (!call_inst) continue;
outs() << "CallInst: " << *call_inst << "\n";
auto load_inst = dyn_cast<LoadInst>(call_inst->getCalledOperand());
if (!load_inst) continue;
outs() << "LoadInst: " << *load_inst << "\n";
auto get_element_ptr_inst =
    dyn_cast<GetElementPtrInst>(load_inst->getPointerOperand());
if (!get_element_ptr_inst) continue;
outs() << "GemElementPtrInst: " << *get_element_ptr_inst << "\n";
auto jni_native_interface =
    dyn_cast<StructType>(get_element_ptr_inst->getSourceElementType());
if (!jni_native_interface) continue;
outs() << "StructName: " << jni_native_interface->getStructName() << "\n";
if (jni_native_interface->getStructName() != "struct.JNINativeInterface")
  continue;
if (get_element_ptr_inst->getNumIndices() != 2) continue;
if (!(get_element_ptr_inst->hasAllConstantIndices())) continue;
auto index = dyn_cast<ConstantInt>(get_element_ptr_inst->idx_begin() + 1);
outs() << "offset_in_alignment: " << index->getSExtValue() << "\n";
```

## Reference

[^1]: <https://stackoverflow.com/questions/47949969/llvm-get-the-offset-of-inside-struct>
