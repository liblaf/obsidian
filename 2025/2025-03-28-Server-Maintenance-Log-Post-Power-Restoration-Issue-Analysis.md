---
date: 2025-03-28T19:15:42+08:00
modified: 2025-09-20T18:37:28+08:00
tags:
  - Laboratory
  - PhD
  - Server
  - Ubuntu
title: "Server Maintenance Log: Post-Power Restoration Issue Analysis"
---

Following the resumption of power after campus-wide circuit maintenance, several server-related issues emerged during system checks. Below is a detailed breakdown of the problems encountered and their resolutions.

---

### 1. Intermittent Server Monitoring Failures

###### Symptoms

The monitoring system (polling server status via `nvidia-smi` every 15 seconds) frequently timed out.

###### Root Cause

NVIDIA GPUs default to **non-persistent mode**. When idle, `nvidia-smi` response latency increases significantly, causing monitoring script timeouts.

###### Solutions

1. **Temporary Persistence Mode Activation**

   ```bash  
   nvidia-smi --persistence-mode=1  
   ```  

2. **Permanent Daemon Configuration**

   ```bash  
   sudo systemctl enable --now nvidia-persistenced.service  
   ```  

> Reference: [NVIDIA/Tips and tricks - ArchWiki](https://wiki.archlinux.org/title/NVIDIA/Tips_and_tricks#Driver_persistence)

---

### 2. Unstable SSH Connectivity

###### Symptoms

SSH connections intermittently failed despite successful pings, occasionally triggering public key mismatches.

###### Diagnosis

- Unauthorized devices from other departments were connected to the same switch.
- IP conflicts caused SSH requests to route to incorrect hosts.

###### Immediate Actions

- Physically inspected switch ports and removed unauthorized devices.
- Enforced MAC address binding and revised IP allocation policies.

###### Long-Term Proposal

Implementing centralized SSH certificate signing for server authentication (deferred due to promotion complexity).

---

### 3. Post-Reboot NVIDIA Driver Failure

###### Symptoms

GPU drivers failed to load after reboot.

###### Cause Analysis

- A prior kernel update had not been applied until reboot.
- The new kernel version lacked compatible NVIDIA driver modules.

###### Resolution

1. Rebuilt drivers via DKMS:

   ```bash  
   sudo dkms autoinstall  
   ```  

2. Verified functionality:

   ```bash  
   nvidia-smi  
   ```  

###### Key Takeaway

Validate driver compatibility immediately after kernel updates. DKMS automation is strongly recommended.
