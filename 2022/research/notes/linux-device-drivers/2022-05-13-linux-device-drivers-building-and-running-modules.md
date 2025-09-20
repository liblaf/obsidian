---
category:
- Research
isOriginal: false
title: Linux Device Drivers | Building and Running Modules
date: '2022-05-13T00:00:00+08:00'
tags:
- C/C++
- Linux
- Linux Device Drivers
- Linux Kernel
---

## Utilities

```bash
insmod
modprobe
rmmod
```

User-space utilities that load modules into the running kernels and remove them.

## <linux/init.h>

```c
module_init(init_function);
module_exit(cleanup_function);
```

Macros that designate a module's initialization and cleanup functions.

```c
__init
__initdata
__exit
__exitdata
```

Markers for functions (`__init` and `__exit`) and data (`__initdata` and `__exitdata`) that are only used at module initialization or cleanup time. Items marked for initialization may be discarded once initialization completes; the exit items may be discarded if module unloading has not been configured into the kernel. These markers work by causing the relevant objects to be placed in a special ELF section in the executable file.

## <linux/sched.h>

One of the most important header files. This file contains definitions of much of the kernel API used by the driver, including functions for sleeping and numerous variable declarations.

```c
struct task_struct *current;
```

The current process.

```c
current->pid
current->comm
```

The process ID and command name for the current process.

## Makefile

```makefile
obj-m
```

A makefile symbol used by the kernel build system to determine which modules should be built in the current directory.

## Files

```
/sys/module
/proc/modules
```

`/sys/module` is a sysfs directory hierarchy containing information on currently-loaded modules. `/proc/modules` is the older, single-file version of that information. Entries contain the module name, the amount of memory each module occupies, and the usage count. Extra strings are appended to each line to specify flags that are currently active for the module.

```
vermagic.o
```

An object file from the kernel source directory that describes the environment a module was built for.

## <linux/module.h>

Required header. It must be included by a module source.

## <linux/version.h>

A header file containing information on the version of the kernel being built.

```c
LINUX_VERSION_CODE
```

Integer macro, useful to `#ifdef` version dependencies.

```c
EXPORT_SYMBOL(symbol);
EXPORT_SYMBOL_GPL(symbol);
```

Macro used to export a symbol to the kernel. The second form limits use of the exported symbol to GPL-licensed modules.

```c
MODULE_AUTHOR(author);
MODULE_DESCRIPTION(description);
MODULE_VERSION(version_string);
MODULE_DEVICE_TABLE(table_info);
MODULE_ALIAS(alternate_name);
```

Place documentation on the module in the object file.

```c
MODULE_LICENSE(license);
```

Declare the license governing this module.

## <linux/moduleparam.h>

```c
module_param(variable, type, perm);
```

Macro that creates a module parameter that can be adjusted by the user when the module is loaded (or at boot time for built-in code). The type can be one of `bool`, `charp`, `int`, `invbool`, `long`, `short`, `ushort`, `uint`, `ulong`, or `intarray`.

## <linux/kernel.h>

```c
int printk(const char * fmt, ...);
```

The analogue of `printf` for kernel code.
