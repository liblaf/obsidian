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
title: Linux Device Drivers | Time, Delays, and Deferred Work
---

## Timekeeping

###### <linux/param.h>

```c
HZ
```

The `HZ` symbol specifies the number of clock ticks generated per second.

###### <linux/jiffies.h>

```c
volatile unsigned long jiffies
u64 jiffies_64
```

The `jiffies_64` variable is incremented once for each clock tick; thus, it's incremented `HZ` times per second. Kernel code most often refers to `jiffies`, which is the same as `jiffies_64` on 64-bit platforms and the least significant half of it on 32-bit platforms.

```c
int time_after(unsigned long a, unsigned long b);
int time_before(unsigned long a, unsigned long b);
int time_after_eq(unsigned long a, unsigned long b);
int time_before_eq(unsigned long a, unsigned long b);
```

These Boolean expressions compare jiffies in a safe way, without problems in case of counter overflow and without the need to access `jiffies_64`.

```c
u64 get_jiffies_64(void);
```

Retrieves `jiffies_64` without race conditions.

###### <linux/time.h>

```c
unsigned long timespec_to_jiffies(struct timespec *value);
void jiffies_to_timespec(unsigned long jiffies, struct timespec *value);
unsigned long timeval_to_jiffies(struct timeval *value);
void jiffies_to_timeval(unsigned long jiffies, struct timeval *value);
```

Converts time representations between jiffies and other representations.

###### <asm/msr.h>

```c
rdtsc(low32,high32);
rdtscl(low32);
rdtscll(var64);
```

x86-specific macros to read the timestamp counter. They read it as two 32-bit halves, read only the lower half, or read all of it into a `long long` variable.

###### <linux/timex.h>

```c
cycles_t get_cycles(void);
```

Returns the timestamp counter in a platform-independent way. If the CPU offers no timestamp feature, `0` is returned.

###### <linux/time.h>

```c
unsigned long mktime(year, mon, day, h, m, s);
```

Returns the number of seconds since the Epoch, based on the six `unsigned int` arguments.

```c
void do_gettimeofday(struct timeval *tv);
```

Returns the current time, as seconds and microseconds since the Epoch, with the best resolution the hardware can offer. On most platforms the resolution is one microsecond or better, although some platforms offer only jiffies resolution.

```c
struct timespec current_kernel_time(void);
```

Returns the current time with the resolution of one jiffy.

## Delays

###### <linux/wait.h>

```c
long wait_event_interruptible_timeout(wait_queue_head_t *q, condition, signed long timeout);
```

Puts the current process to sleep on the wait queue, installing a timeout value expressed in jiffies. Use `schedule_timeout` (below) for non-interruptible sleeps.

###### <linux/sched.h>

```c
signed long schedule_timeout(signed long timeout);
```

Calls the scheduler after ensuring that the current process is awakened at timeout expiration. The caller must invoke `set_current_state` first to put itself in an interruptible or non-interruptible sleep state.

###### <linux/delay.h>

```c
void ndelay(unsigned long nsecs);
void udelay(unsigned long usecs);
void mdelay(unsigned long msecs);
```

Introduces delays of an integer number of nanoseconds, microseconds, and milliseconds. The delay achieved is at least the requested value, but it can be more. The argument to each function must not exceed a platform-specific limit (usually a few thousands).

```c
void msleep(unsigned int millisecs);
unsigned long msleep_interruptible(unsigned int millisecs);
void ssleep(unsigned int seconds);
```

Puts the process to sleep for the given number of milliseconds (or seconds, in the case of `ssleep`).

## Kernel Timers

###### <asm/hardirq.h>

```c
int in_interrupt(void);
int in_atomic(void);
```

Returns a Boolean value telling whether the calling code is executing in interrupt context or atomic context. Interrupt context is outside of a process context, either during hardware or software interrupt processing. Atomic context is when you can't schedule either an interrupt context or a process's context with a spinlock held.

###### <linux/timer.h>

```c
void init_timer(struct timer_list * timer);
struct timer_list TIMER_INITIALIZER(_function, _expires, _data);
```

This function and the static declaration of the timer structure are the two ways to initialize a `timer_list` data structure.

```c
void add_timer(struct timer_list * timer);
```

Registers the timer structure to run on the current CPU.

```c
int mod_timer(struct timer_list *timer, unsigned long expires);
```

Changes the expiration time of an already scheduled timer structure. It can also act as an alternative to `add_timer`.

```c
int timer_pending(struct timer_list * timer);
```

Macro that returns a Boolean value stating whether the timer structure is already registered to run.

```c
void del_timer(struct timer_list * timer);
void del_timer_sync(struct timer_list * timer);
```

Removes a timer from the list of active timers. The latter function ensures that the timer is not currently running on another CPU.

## Tasklets

###### <linux/interrupt.h>

```c
DECLARE_TASKLET(name, func, data);
DECLARE_TASKLET_DISABLED(name, func, data);
void tasklet_init(struct tasklet_struct *t, void (*func)(unsigned long), unsigned long data);
```

The first two macros declare a tasklet structure, while the `tasklet_init` function initializes a tasklet structure that has been obtained by allocation or other means. The second `DECLARE` macro marks the tasklet as disabled.

```c
void tasklet_disable(struct tasklet_struct *t);
void tasklet_disable_nosync(struct tasklet_struct *t);
void tasklet_enable(struct tasklet_struct *t);
```

Disables and reenables a tasklet. Each `disable` must be matched with an `enable` (you can disable the tasklet even if it's already disabled). The function `tasklet_disable` waits for the tasklet to terminate if it is running on another CPU. The `nosync` version doesn't take this extra step.

```c
void tasklet_schedule(struct tasklet_struct *t);
void tasklet_hi_schedule(struct tasklet_struct *t);
```

Schedules a tasklet to run, either as a "normal" tasklet or a high-priority one. When soft interrupts are executed, high-priority tasklets are dealt with first, while normal tasklets run last.

```c
void tasklet_kill(struct tasklet_struct *t);
```

Removes the tasklet from the list of active ones, if it's scheduled to run. Like `tasklet_disable`, the function may block on SMP systems waiting for the tasklet to terminate if it's currently running on another CPU.

## Workqueues

###### <linux/workqueue.h>

```c
struct workqueue_struct;
struct work_struct;
```

The structures representing a workqueue and a work entry, respectively.

```c
struct workqueue_struct *create_workqueue(const char *name);
struct workqueue_struct *create_singlethread_workqueue(const char *name);
void destroy_workqueue(struct workqueue_struct *queue);
```

Functions for creating and destroying workqueues. A call to `create_workqueue` creates a queue with a worker thread on each processor in the system; instead, `create_singlethread_workqueue` creates a workqueue with a single worker process.

```c
DECLARE_WORK(name, void (*function)(void *), void *data);
INIT_WORK(struct work_struct *work, void (*function)(void *), void *data);
PREPARE_WORK(struct work_struct *work, void (*function)(void *), void *data);
```

Macros that declare and initialize workqueue entries.

```c
int queue_work(struct workqueue_struct *queue, struct work_struct *work);
int queue_delayed_work(struct workqueue_struct *queue, struct work_struct *work, unsigned long delay);
```

Functions that queue work for execution from a workqueue.

```c
int cancel_delayed_work(struct work_struct *work);
void flush_workqueue(struct workqueue_struct *queue);
```

Use `cancel_delayed_work` to remove an entry from a workqueue; `flush_workqueue` ensures that no workqueue entries are running anywhere in the system.

```c
int schedule_work(struct work_struct *work);
int schedule_delayed_work(struct work_struct *work, unsigned long delay);
void flush_scheduled_work(void);
```

Functions for working with the shared workqueue.
