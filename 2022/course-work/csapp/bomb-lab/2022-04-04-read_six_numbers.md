---
category:
- Course Work
date: '2022-04-04T00:00:00+08:00'
tags:
- Bomb_Lab
- Computer_Organization_and_Architecture
title: 'Bomb Lab: read six numbers'
---

## Assembly

```assembly
0000000000401b98 <read_six_numbers>:
b0:
  401b98:	48 83 ec 18          	sub    $0x18,%rsp
  401b9c:	48 89 f2             	mov    %rsi,%rdx
  401b9f:	48 8d 4e 04          	lea    0x4(%rsi),%rcx
  401ba3:	48 8d 46 14          	lea    0x14(%rsi),%rax
  401ba7:	48 89 44 24 08       	mov    %rax,0x8(%rsp)
  401bac:	48 8d 46 10          	lea    0x10(%rsi),%rax
  401bb0:	48 89 04 24          	mov    %rax,(%rsp)
  401bb4:	4c 8d 4e 0c          	lea    0xc(%rsi),%r9
  401bb8:	4c 8d 46 08          	lea    0x8(%rsi),%r8
  401bbc:	48 8d 35 66 18 00 00 	lea    0x1866(%rip),%rsi        # 403429 <array.3354+0x249>
  401bc3:	b8 00 00 00 00       	mov    $0x0,%eax
  401bc8:	e8 63 f5 ff ff       	callq  401130 <__isoc99_sscanf@plt>
  401bcd:	83 f8 05             	cmp    $0x5,%eax
  401bd0:	7f 05                	jg     401bd7 <read_six_numbers+0x3f>
  401bd2:	e8 85 ff ff ff       	callq  401b5c <explode_bomb>
b1:
  401bd7:	48 83 c4 18          	add    $0x18,%rsp
  401bdb:	c3                   	retq
```

## 翻译为 C

```c
void read_six_numbers() {
b0:
  rsp -= 0x18;
  rdx = rsi;
  rcx = rsi + 0x4;
  rax = rsi + 0x14;
  *(rsp + 0x8) = rax;
  rax = rsi + 0x10;
  *rsp = rax;
  r9 = rsi + 0xc;
  r8 = rsi + 0x8;
  rsi = 0x403429; // 403429 <array.3354+0x249>
  rax = 0;  // 32-bit
  rax = __isoc99_sscanf @plt();
  if (rax > 0x5) goto b1;
  explode_bomb();
b1:
  rsp += 0x18;
  return;
}
```

## Optimize

```c
void read_six_numbers(char* rdi, int* rsi) {
  int rax = 0;  // 32-bit
  rax = __isoc99_sscanf(rdi, "%d %d %d %d %d %d", rsi, rsi + 1, rsi + 2,
                        rsi + 3, rsi + 4, rsi + 5);
  if (!(rax > 5)) explode_bomb();
}
```

## Hack

```
(gdb) x/s 0x403429
0x403429:       "%d %d %d %d %d %d"
```
