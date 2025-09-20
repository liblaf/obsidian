---
category:
  - Research
date: "2022-05-13T00:00:00+08:00"
isOriginal: false
tags:
  - C_Cpp
  - Linux
  - Linux_Device_Drivers
  - Linux_Kernel
title: Linux Device Drivers | Allocating Memory
---

###### <linux/slab.h>

```c
void *kmalloc(size_t size, int flags);
void kfree(void *obj);
```

The most frequently used interface to memory allocation.

###### <linux/mm.h>

```c
GFP_USER
GFP_KERNEL
GFP_NOFS
GFP_NOIO
GFP_ATOMIC
```

Flags that control how memory allocations are performed, from the least restrictive to the most. The `GFP_USER` and `GFP_KERNEL` priorities allow the current process to be put to sleep to satisfy the request. `GFP_NOFS` and `GFP_NOIO` disable filesystem operations and all I/O operations, respectively, while `GFP_ATOMIC` allocations cannot sleep at all.

```c
__GFP_DMA
__GFP_HIGHMEM
__GFP_COLD
__GFP_NOWARN
__GFP_HIGH
__GFP_REPEAT
__GFP_NOFAIL
__GFP_NORETRY
```

These flags modify the kernel's behavior when allocating memory.

###### <linux/malloc.h>

```c
kmem_cache_t *kmem_cache_create(char *name, size_t size, size_t offset, unsigned long flags, constructor(), destructor());
int kmem_cache_destroy(kmem_cache_t *cache);
```

Create and destroy a slab cache. The cache can be used to allocate several objects of the same size.

```c
SLAB_NO_REAP
SLAB_HWCACHE_ALIGN
SLAB_CACHE_DMA
```

Flags that can be specified while creating a cache.

```c
SLAB_CTOR_ATOMIC
SLAB_CTOR_CONSTRUCTOR
```

Flags that the allocator can pass to the constructor and the destructor functions.

```c
void *kmem_cache_alloc(kmem_cache_t *cache, int flags);
void kmem_cache_free(kmem_cache_t *cache, const void *obj);
```

Allocate and release a single object from the cache.

###### Files

```
/proc/slabinfo
```

A virtual file containing statistics on slab cache usage.

###### <linux/mempool.h>

```c
mempool_t *mempool_create(int min_nr, mempool_alloc_t *alloc_fn, mempool_free_t *free_fn, void *data);
void mempool_destroy(mempool_t *pool);
```

Functions for the creation of memory pools, which try to avoid memory allocation failures by keeping an "emergency list" of allocated items.

```c
void *mempool_alloc(mempool_t *pool, int gfp_mask);
void mempool_free(void *element, mempool_t *pool);
```

Functions for allocating items from (and returning them to) memory pools.

```c
unsigned long get_zeroed_page(int flags);
unsigned long __get_free_page(int flags);
unsigned long __get_free_pages(int flags, unsigned long order);
```

The page-oriented allocation functions. `get_zeroed_page` returns a single, zero-filled page. All the other versions of the call do not initialize the contents of the returned page(s).

```c
int get_order(unsigned long size);
```

Returns the allocation order associated to size in the current platform, according to `PAGE_SIZE`. The argument must be a power of two, and the return value is at least `0`.

```c
void free_page(unsigned long addr);
void free_pages(unsigned long addr, unsigned long order);
```

Functions that release page-oriented allocations.

```c
struct page *alloc_pages_node(int nid, unsigned int flags, unsigned int order);
struct page *alloc_pages(unsigned int flags, unsigned int order);
struct page *alloc_page(unsigned int flags);
```

All variants of the lowest-level page allocator in the Linux kernel.

```c
void __free_page(struct page *page);
void __free_pages(struct page *page, unsigned int order);
void free_hot_page(struct page *page);
void free_cold_page(struct page *page);
```

Various ways of freeing pages allocated with one of the forms of `alloc_page`.

###### <linux/vmalloc.h>

```c
void * vmalloc(unsigned long size);
void vfree(void * addr);
```

###### <asm/io.h>

```c
void * ioremap(unsigned long offset, unsigned long size);
void iounmap(void *addr);
```

Functions that allocate or free a contiguous virtual address space. `ioremap` accesses physical memory through virtual addresses, while `vmalloc` allocates free pages. Regions mapped with `ioremap` are freed with `iounmap`, while pages obtained from `vmalloc` are released with `vfree`.

###### <linux/percpu.h>

```c
DEFINE_PER_CPU(type, name);
DECLARE_PER_CPU(type, name);
```

Macros that define and declare per-CPU variables.

```c
per_cpu(variable, int cpu_id)
get_cpu_var(variable)
put_cpu_var(variable)
```

Macros that provide access to statically declared per-CPU variables.

```c
void *alloc_percpu(type);
void *__alloc_percpu(size_t size, size_t align);
void free_percpu(void *variable);
```

Functions that perform runtime allocation and freeing of per-CPU variables.

```c
int get_cpu();
void put_cpu();
per_cpu_ptr(void *variable, int cpu_id)
```

`get_cpu` obtains a reference to the current processor (therefore, preventing preemption and movement to another processor) and returns the ID number of the processor; `put_cpu` returns that reference. To access a dynamically allocated per-CPU variable, use `per_cpu_ptr` with the ID of the CPU whose version should be accessed. Manipulations of the current CPU's version of a dynamic, per-CPU variable should probably be surrounded by calls to `get_cpu` and `put_cpu`.

###### <linux/bootmem.h>

```c
void *alloc_bootmem(unsigned long size);
void *alloc_bootmem_low(unsigned long size);
void *alloc_bootmem_pages(unsigned long size);
void *alloc_bootmem_low_pages(unsigned long size);
void free_bootmem(unsigned long addr, unsigned long size);
```

Functions (which can be used only by drivers directly linked into the kernel) that perform allocation and freeing of memory at system bootstrap time.
