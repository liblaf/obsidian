---
created: 2025-04-27T00:21:27+08:00
modified: 2025-04-27T00:37:51+08:00
tags:
  - Dotfiles
  - Hardware/NVIDIA
  - OS/Linux/Arch
  - OS/Linux/Arch/CachyOS
title: GPU has fallen off the bus.
---

## Hardware

```console
$ lspci -k -d ::03xx
01:00.0 VGA compatible controller: NVIDIA Corporation AD107M [GeForce RTX 4060 Max-Q / Mobile] (rev a1)
        Subsystem: Lenovo Device 3b53
        Kernel driver in use: nvidia
        Kernel modules: nouveau, nvidia_drm, nvidia
```

## Error

```log
kernel: NVRM: GPU at PCI:0000:01:00: GPU-4f667a85-72a7-4605-2197-8f6a16b663a1
kernel: NVRM: Xid (PCI:0000:01:00): 79, pid=22434, name=gnome-character, GPU has fallen off the bus.
kernel: NVRM: GPU 0000:01:00.0: GPU has fallen off the bus.
kernel: NVRM: kgspRcAndNotifyAllChannels_IMPL: RC all channels for critical error 79.
kernel: NVRM: _threadNodeCheckTimeout: API_GPU_ATTACHED_SANITY_CHECK failed!
kernel: NVRM: _threadNodeCheckTimeout: API_GPU_ATTACHED_SANITY_CHECK failed!
...
```

## Solution

- <https://bbs.archlinux.org/viewtopic.php?pid=2230533#p2230533>
- <https://github.com/NVIDIA/open-gpu-kernel-modules/issues/820#issuecomment-2769571555>

Add the following to disable GSP firmware with the proprietary [nvidia-lts](https://archlinux.org/packages/extra/x86_64/nvidia-lts/).

> The open kernel modules unconditionally require GSP firmware. You cannot disable GSP when using the open kernel modules.

```sh
# /etc/modprobe.d/nvidia.conf
options nvidia NVreg_EnableGpuFirmware=0
```
