---
category:
- Course Work
title: 'Bomb Lab: strings not equal'
date: '2022-04-04T00:00:00+08:00'
tags:
- Bomb Lab
- Computer Organization and Architecture
---

```assembly
0000000000401893 <strings_not_equal>:
  401893:	41 54                	push   %r12
  401895:	55                   	push   %rbp
  401896:	53                   	push   %rbx
  401897:	48 89 fb             	mov    %rdi,%rbx
  40189a:	48 89 f5             	mov    %rsi,%rbp
  40189d:	e8 d4 ff ff ff       	callq  401876 <string_length>
  4018a2:	41 89 c4             	mov    %eax,%r12d
  4018a5:	48 89 ef             	mov    %rbp,%rdi
  4018a8:	e8 c9 ff ff ff       	callq  401876 <string_length>
  4018ad:	ba 01 00 00 00       	mov    $0x1,%edx
  4018b2:	41 39 c4             	cmp    %eax,%r12d
  4018b5:	75 3c                	jne    4018f3 <strings_not_equal+0x60>
  4018b7:	0f b6 03             	movzbl (%rbx),%eax
  4018ba:	84 c0                	test   %al,%al
  4018bc:	74 22                	je     4018e0 <strings_not_equal+0x4d>
  4018be:	3a 45 00             	cmp    0x0(%rbp),%al
  4018c1:	74 07                	je     4018ca <strings_not_equal+0x37>
  4018c3:	eb 22                	jmp    4018e7 <strings_not_equal+0x54>
  4018c5:	3a 45 00             	cmp    0x0(%rbp),%al
  4018c8:	75 24                	jne    4018ee <strings_not_equal+0x5b>
  4018ca:	48 83 c3 01          	add    $0x1,%rbx
  4018ce:	48 83 c5 01          	add    $0x1,%rbp
  4018d2:	0f b6 03             	movzbl (%rbx),%eax
  4018d5:	84 c0                	test   %al,%al
  4018d7:	75 ec                	jne    4018c5 <strings_not_equal+0x32>
  4018d9:	ba 00 00 00 00       	mov    $0x0,%edx
  4018de:	eb 13                	jmp    4018f3 <strings_not_equal+0x60>
  4018e0:	ba 00 00 00 00       	mov    $0x0,%edx
  4018e5:	eb 0c                	jmp    4018f3 <strings_not_equal+0x60>
  4018e7:	ba 01 00 00 00       	mov    $0x1,%edx
  4018ec:	eb 05                	jmp    4018f3 <strings_not_equal+0x60>
  4018ee:	ba 01 00 00 00       	mov    $0x1,%edx
  4018f3:	89 d0                	mov    %edx,%eax
  4018f5:	5b                   	pop    %rbx
  4018f6:	5d                   	pop    %rbp
  4018f7:	41 5c                	pop    %r12
  4018f9:	c3                   	retq
```

## 分割 `BasicBlock`

```assembly
0000000000401893 <strings_not_equal>:
b0:
  401893:	41 54                	push   %r12
  401895:	55                   	push   %rbp
  401896:	53                   	push   %rbx
  401897:	48 89 fb             	mov    %rdi,%rbx
  40189a:	48 89 f5             	mov    %rsi,%rbp
  40189d:	e8 d4 ff ff ff       	callq  401876 <string_length>
  4018a2:	41 89 c4             	mov    %eax,%r12d
  4018a5:	48 89 ef             	mov    %rbp,%rdi
  4018a8:	e8 c9 ff ff ff       	callq  401876 <string_length>
  4018ad:	ba 01 00 00 00       	mov    $0x1,%edx
  4018b2:	41 39 c4             	cmp    %eax,%r12d
  4018b5:	75 3c                	jne    4018f3 <strings_not_equal+0x60>
  4018b7:	0f b6 03             	movzbl (%rbx),%eax
  4018ba:	84 c0                	test   %al,%al
  4018bc:	74 22                	je     4018e0 <strings_not_equal+0x4d>
  4018be:	3a 45 00             	cmp    0x0(%rbp),%al
  4018c1:	74 07                	je     4018ca <strings_not_equal+0x37>
  4018c3:	eb 22                	jmp    4018e7 <strings_not_equal+0x54>
b1:
  4018c5:	3a 45 00             	cmp    0x0(%rbp),%al
  4018c8:	75 24                	jne    4018ee <strings_not_equal+0x5b>
b2:
  4018ca:	48 83 c3 01          	add    $0x1,%rbx
  4018ce:	48 83 c5 01          	add    $0x1,%rbp
  4018d2:	0f b6 03             	movzbl (%rbx),%eax
  4018d5:	84 c0                	test   %al,%al
  4018d7:	75 ec                	jne    4018c5 <strings_not_equal+0x32>
  4018d9:	ba 00 00 00 00       	mov    $0x0,%edx
  4018de:	eb 13                	jmp    4018f3 <strings_not_equal+0x60>
b3:
  4018e0:	ba 00 00 00 00       	mov    $0x0,%edx
  4018e5:	eb 0c                	jmp    4018f3 <strings_not_equal+0x60>
b4:
  4018e7:	ba 01 00 00 00       	mov    $0x1,%edx
  4018ec:	eb 05                	jmp    4018f3 <strings_not_equal+0x60>
b5:
  4018ee:	ba 01 00 00 00       	mov    $0x1,%edx
b6:
  4018f3:	89 d0                	mov    %edx,%eax
  4018f5:	5b                   	pop    %rbx
  4018f6:	5d                   	pop    %rbp
  4018f7:	41 5c                	pop    %r12
  4018f9:	c3                   	retq
```

## 翻译为 C

```c
void strings_not_equal() {
b0:
  // push r12 rbp rbx
  rbx = rdi;
  rbp = rsi;
  rax = string_length(rdi);
  r12 = rax;  // 32-bit
  rdi = rbp;
  rax = string_length(rdi);
  rdx = 1;         // 32-bit
  if (r12 != rax)  // 32-bit
    goto b6;
  rax = *rbx;    // 32-bit
  if (rax == 0)  // 8-bit
    goto b3;
  if (rax == *rbp)  // 8-bit
    goto b2;
  goto b4;
b1:
  if (rax != *rbp)  // 8-bit
    goto b5;
b2:
  ++rbx;
  ++rbp;
  rax = *rbx;    // 32-bit
  if (rax != 0)  // 8-bit
    goto b1;
  rdx = 0;  // 32-bit
  goto b6;
b3:
  rdx = 0;  // 32-bit
  goto b6;
b4:
  rdx = 1;  // 32-bit
  goto b6;
b5:
  rdx = 1;  // 32-bit
b6:
  rax = rdx;  // 32-bit
  // pop rbx rbp r12
  return;
}
```

## xxxxxxxxxx5 1int string_length(char* rdi) {2 char* rdx = rdi;3 while (\*rdx) ++rdi;4 return rdx - rdi; // rax5}c

```c
int strings_not_equal(char* rdi, char* rsi) {
  if (string_length(rdi) != string_length(rsi)) return 1;
  for (char *rbx = rdi, *rbp = rsi; *rbx; ++rbx, ++rbp) {
    if (*rbx != *rbp) return 1;
  }
  return 0;
}
```
