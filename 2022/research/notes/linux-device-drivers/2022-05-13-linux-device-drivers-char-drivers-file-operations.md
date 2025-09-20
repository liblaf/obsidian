---
category:
- Research
isOriginal: false
title: Linux Device Drivers | Char Drivers | File Operations
date: '2022-05-13T00:00:00+08:00'
tags:
- C/C++
- Char Drivers
- Linux
- Linux Device Drivers
- Linux Kernel
---

```c
#include <linux/fs.h>
struct file_operations { ... };
```

## owner

```c
struct module *owner
```

The first `file_operations` field is not an operation at all; it is a pointer to the module that "owns" the structure. This field is used to prevent the module from being unloaded while its operations are in use. Almost all the time, it is simply initialized to `THIS_MODULE`, a macro defined in `<linux/module.h>`.

## llseek

```c
loff_t (*llseek) (struct file *, loff_t, int);
```

The `llseek` method is used to change the current read/write position in a file, and the new position is returned as a (positive) return value. The `loff_t` parameter is a "long offset" and is at least 64 bits wide even on 32-bit platforms. Errors are signaled by a negative return value. If this function pointer is `NULL`, seek calls will modify the position counter in the `file` structure (described in the section "The file Structure") in potentially unpredictable ways.

## read

```c
ssize_t (*read) (struct file *, char __user *, size_t, loff_t *);
```

Used to retrieve data from the device. A null pointer in this position causes the read system call to fail with `-EINVAL` ("Invalid argument"). A nonnegative return value represents the number of bytes successfully read (the return value is a "signed size" type, usually the native integer type for the target platform).

## aio_read

```c
ssize_t (*aio_read)(struct kiocb *, char __user *, size_t, loff_t);
```

Initiates an asynchronous read --- a read operation that might not complete before the function returns. If this method is `NULL`, all operations will be processed (synchronously) by read instead.

## write

```c
ssize_t (*write) (struct file *, const char __user *, size_t, loff_t *);
```

Sends data to the device. If `NULL`, `-EINVAL` is returned to the program calling the write system call. The return value, if nonnegative, represents the number of bytes successfully written.

## aio_write

```c
ssize_t (*aio_write) (struct kiocb *, const char __user *, size_t, loff_t *);
```

Initiates an asynchronous write operation on the device.

## readdir

```c
int (*readdir) (struct file *, void *, filldir_t);
```

This field should be `NULL` for device files; it is used for reading directories and is useful only for filesystems.

## poll

```c
unsigned int (*poll) (struct file *, struct poll_table_struct *);
```

The `poll` method is the back end of three system calls: `poll`, `epoll`, and `select`, all of which are used to query whether a read or write to one or more file descriptors would block. The poll method should return a bit mask indicating whether nonblocking reads or writes are possible, and, possibly, provide the kernel with information that can be used to put the calling process to sleep until I/O becomes possible. If a driver leaves its poll method `NULL`, the device is assumed to be both readable and writable without blocking.

## ioctl

```c
int (*ioctl) (struct inode *, struct file *, unsigned int, unsigned long);
```

The `ioctl` system call offers a way to issue device-specific commands (such as formatting a track of a floppy disk, which is neither reading nor writing). Additionally, a few `ioctl` commands are recognized by the kernel without referring to the `fops` table. If the device doesn't provide an `ioctl` method, the system call returns an error for any request that isn't predefined (`-ENOTTY`, "No such `ioctl` for device").

## mmap

```c
int (*mmap) (struct file *, struct vm_area_struct *);
```

`mmap` is used to request a mapping of device memory to a process's address space. If this method is `NULL`, the `mmap` system call returns `-ENODEV`.

## open

```c
int (*open) (struct inode *, struct file *);
```

Though this is always the first operation performed on the device file, the driver is not required to declare a corresponding method. If this entry is `NULL`, opening the device always succeeds, but your driver isn't notified.

## flush

```c
int (*flush) (struct file *);
```

The `flush` operation is invoked when a process closes its copy of a file descriptor for a device; it should execute (and wait for) any outstanding operations on the device. This must not be confused with the `fsync` operation requested by user programs. Currently, `flush` is used in very few drivers; the SCSI tape driver uses it, for example, to ensure that all data written makes it to the tape before the device is closed. If `flush` is `NULL`, the kernel simply ignores the user application request.

## release

```c
int (*release) (struct inode *, struct file *);
```

This operation is invoked when the file structure is being released. Like open, release can be `NULL`.[^*]

[^*]: Note that `release` isn't invoked every time a process calls `close`. Whenever a `file` structure is shared (for example, after a `fork` or a `dup`), `release` won't be invoked until all copies are closed. If you need to flush pending data when any copy is closed, you should implement the `flush` method.

## fsync

```c
int (*fsync) (struct file *, struct dentry *, int);
```

This method is the back end of the `fsync` system call, which a user calls to flush any pending data. If this pointer is `NULL`, the system call returns `-EINVAL`.

## aio_fsync

```c
int (*aio_fsync)(struct kiocb *, int);
```

This is the asynchronous version of the `fsync` method.

## fasync

```c
int (*fasync) (int, struct file *, int);
```

This operation is used to notify the device of a change in its `FASYNC` flag. Asynchronous notification is an advanced topic and is described in Chapter 6. The field can be `NULL` if the driver doesn't support asynchronous notification.

## lock

```c
int (*lock) (struct file *, int, struct file_lock *);
```

The `lock` method is used to implement file locking; locking is an indispensable feature for regular files but is almost never implemented by device drivers.

## readv

```c
ssize_t (*readv) (struct file *, const struct iovec *, unsigned long, loff_t *);
ssize_t (*writev) (struct file *, const struct iovec *, unsigned long, loff_t *);
```

These methods implement scatter/gather read and write operations. Applications occasionally need to do a single read or write operation involving multiple memory areas; these system calls allow them to do so without forcing extra copy operations on the data. If these function pointers are left `NULL`, the `read` and `write` methods are called (perhaps more than once) instead.

## sendfile

```c
ssize_t (*sendfile)(struct file *, loff_t *, size_t, read_actor_t, void *);
```

This method implements the read side of the `sendfile` system call, which moves the data from one file descriptor to another with a minimum of copying. It is used, for example, by a web server that needs to send the contents of a file out a network connection. Device drivers usually leave `sendfile` `NULL`.

## sendpage

```c
ssize_t (*sendpage) (struct file *, struct page *, int, size_t, loff_t *, int);
```

`sendpage` is the other half of `sendfile`; it is called by the kernel to send data, one page at a time, to the corresponding file. Device drivers do not usually implement `sendpage`.

## get_unmapped_area

```c
unsigned long (*get_unmapped_area)(struct file *, unsigned long, unsigned long, unsigned long, unsigned long);
```

The purpose of this method is to find a suitable location in the process's address space to map in a memory segment on the underlying device. This task is normally performed by the memory management code; this method exists to allow drivers to enforce any alignment requirements a particular device may have. Most drivers can leave this method `NULL`.

## chech_flags

```c
int (*check_flags) (int);
```

This method allows a module to check the flags passed to an `fcntl(F_SETFL...)` call.

## dir_notify

```c
int (*dir_notify) (struct file *, unsigned long);
```

This method is invoked when an application uses `fcntl` to request directory change notifications. It is useful only to filesystems; drivers need not implement `dir_notify`.
