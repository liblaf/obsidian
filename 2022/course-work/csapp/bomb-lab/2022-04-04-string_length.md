---
category:
  - Course Work
date: 2022-04-04T08:00:00+08:00
modified: 2025-09-20T23:07:39+08:00
tags:
  - Bomb_Lab
  - Computer_Organization_and_Architecture
title: "Bomb Lab: string length"
---

## Assembly

```assembly
0000000000401876 <string_length>:
b0:
  401876:	80 3f 00             	cmpb   $0x0,(%rdi)
  401879:	74 12                	je     40188d <string_length+0x17>
  40187b:	48 89 fa             	mov    %rdi,%rdx
b1:
  40187e:	48 83 c2 01          	add    $0x1,%rdx
  401882:	89 d0                	mov    %edx,%eax
  401884:	29 f8                	sub    %edi,%eax
  401886:	80 3a 00             	cmpb   $0x0,(%rdx)
  401889:	75 f3                	jne    40187e <string_length+0x8>
  40188b:	f3 c3                	repz retq
b2:
  40188d:	b8 00 00 00 00       	mov    $0x0,%eax
  401892:	c3                   	retq
```

## 翻译为 C

```c
void string_length() void string_length() {
b0:
  if (*rdi == 0) goto b2;
  rdx = rdi;
b1:
  ++rdx;
  rax = rdx;   // 32-bit
  rax -= rdi;  // 32-bit
  if (*rdx != 0) goto b1;
  return;
b2:
  rax = 0;  // 32-bit
  return;
}
```

## Optimize

```c
int string_length(char* rdi) {
  char* rdx = rdi;
  while (*rdx) ++rdi;
  return rdx - rdi;  // rax
}
```
