---
category:
  - Research
date: 2022-05-13T08:00:00+08:00
isOriginal: false
modified: 2025-09-20T23:07:39+08:00
tags:
  - C_Cpp
  - Linux
  - Linux_Device_Drivers
  - Linux_Kernel
title: Linux Device Drivers | Char Drivers
---

## <linux/types.h>

```c
dev_t
```

`dev_t` is the type used to represent device numbers within the kernel.

```c
int MAJOR(dev_t dev);
int MINOR(dev_t dev);
```

Macros that extract the major and minor numbers from a device number.

```c
dev_t MKDEV(unsigned int major, unsigned int minor);
```

Macro that builds a `dev_t` data item from the major and minor numbers.

## <linux/fs.h>

The "filesystem" header is the header required for writing device drivers. Many important functions and data structures are declared in here.

```c
int register_chrdev_region(dev_t first, unsigned int count, char *name)
int alloc_chrdev_region(dev_t *dev, unsigned int firstminor, unsigned int count, char *name)
void unregister_chrdev_region(dev_t first, unsigned int count);
```

Functions that allow a driver to allocate and free ranges of device numbers. `register_chrdev_region` should be used when the desired major number is known in advance; for dynamic allocation, use `alloc_chrdev_region` instead.

```c
int register_chrdev(unsigned int major, const char *name, struct file_operations *fops);
```

The old (pre-2.6) char device registration routine. It is emulated in the 2.6 kernel but should not be used for new code. If the major number is not 0, it is used unchanged; otherwise a dynamic number is assigned for this device.

```c
int unregister_chrdev(unsigned int major, const char *name);
```

Function that undoes a registration made with `register_chrdev`. Both `major` and the `name` string must contain the same values that were used to register the driver.

```c
struct file_operations;
struct file;
struct inode;
```

Three important data structures used by most device drivers. The `file_operations` structure holds a char driver's methods; `struct file` represents an open file, and `struct inode` represents a file on disk.

## <linux/cdev.h>

```c
struct cdev *cdev_alloc(void);
void cdev_init(struct cdev *dev, struct file_operations *fops);
int cdev_add(struct cdev *dev, dev_t num, unsigned int count);
void cdev_del(struct cdev *dev);
```

Functions for the management of `cdev` structures, which represent char devices within the kernel.

## <linux/kernel.h>

```c
container_of(pointer, type, field);
```

A convenience macro that may be used to obtain a pointer to a structure from a pointer to some other structure contained within it.

## <asm/uaccess.h>

This include file declares functions used by kernel code to move data to and from user space.

```c
unsigned long copy_from_user (void *to, const void *from, unsigned long count);
unsigned long copy_to_user (void *to, const void *from, unsigned long count);
```

Copy data between user space and kernel space.
