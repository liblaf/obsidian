---
category:
  - Research
title: How to Get the Field Name of members in struct
date: "2022-08-17T00:00:00+08:00"
tags:
  - C_Cpp
  - LLVM
---

## What is Debug Info

Read [Source Level Debugging with LLVM](https://llvm.org/docs/SourceLevelDebugging.html) for more details. If you do not have enough time, a few examples from the documentation should be enough.

## How to Generate Debug Info

Pass `-g` or `--debug` option to `clang`.

## How to Access Debug Info

> LLVM uses several intrinsic functions (name prefixed with `llvm.dbg`) to track source local variables through optimization and code generation.[^1]

Debug Info is arranged like a directed graph. However, LLVM does not provide a convenient way to traverse all `llvm::DINode`s. Therefore, we need an entry into debug info. Here we mainly focus on `llvm.dbg.declare` intrinsic, aka `llvm::DbgDeclareInst`, as the entry.

> ###### `llvm.dbg.addr`[^1]
>
> This intrinsic provides information about a local element (e.g., variable). The first argument is `metadata` holding the address of variable, typically a static `alloca` in the function entry block. The second argument is a [local variable](https://llvm.org/docs/LangRef.html#dilocalvariable) containing a description of the variable. The third argument is a [complex expression](https://llvm.org/docs/LangRef.html#diexpression). An `llvm.dbg.addr` intrinsic describes the _address_ of a source variable.
>
> ###### `llvm.dbg.declare`[^1]
>
> This intrinsic is identical to `llvm.dbg.addr`, except that there can only be one call to `llvm.dbg.declare` for a given concrete [local variable](https://llvm.org/docs/LangRef.html#dilocalvariable).

`dbg_declare_inst->getAddress()` gives the address (a `llvm::Value*`) of the variable. `dbg_declare_inst->getVariable()` returns a `llvm::DILocalVariable*`. The name of the variable can be obtained through `debug_info_local_variable->getName()`. The type of the variable can be found in `debug_info_local_variable->getType()`, which returns a `llvm::DIType*`.

## Type System in Debug Info

Besides `llvm::Type`, LLVM provides a similar type system with more details in debug info. `llvm::StructType` does not contain information about field names. However, debug info contains information about variable name, typedef, field names and more.

![Inheritance diagram for `llvm::DIType`](https://llvm.org/doxygen/classllvm_1_1DIType__inherit__graph.png)

`llvm::DIType` is arranged like a directed graph. You can use `getBaseType()` or `getElements()` to dive into the graph. `getTag()` method can be used to quickly determine the type of the `llvm::DIType`. For example, `getTag()` may return `llvm::dwarf::DW_TAG_pointer_type`, `llvm::dwarf::DW_TAG_structure_type`, etc. Most of the tags can be found in
file `llvm/BinaryFormat/Dwarf.def`.

### null

Nothing to say. Be careful with `nullptr`!

### pointer type

pointer types are `llvm::DIDerivedType`. `getBaseType()` returns its pointee type. For example, if `derived_type` represents `int*`, then `derived_type->getBaseType()` should be `int`. Under most circumstances, it will return a `llvm::DIType*`.

::: warning

`getBaseType()` can return `nullptr`!

:::

### member type

member types are `llvm::DIDerivedType` with tag `llvm::dwarf::DW_TAG_member`. Usually they are elements of a struct or a class. The field name can be obtained through `getName()` method.

### structure type

structure types are `llvm::DICompositeType` with tag `llvm::dwarf::DW_TAG_structure_type`. `getName()` returns its name.

::: note

The return value of `getName()` may defer from that of `llvm::StructType::getStructName()`. If you declare multiple structures with the same name but in different scopes (for example, two different structures named `A` in function `f` and `g`), `llvm::StructType::getStructName()` would produce something like `%struct.A` and `%struct.A.0` respectively, while `llvm::DICompositeType::getName()` will always give a `A`.

:::

`getElements()` returns all its fields. Under most circumstances, a field should be a `llvm::DIDerivedType` with tag `llvm::dwarf::DW_TAG_member`.

::: warning

The tag of an element can be something else from `llvm::dwarf::DW_TAG_member`! Especially in `c++`.

:::

### typedef

`llvm::DIDerivedType` with tag `llvm::dwarf::DW_TAG_typedef`. `getBaseType()` returns the type of the alias.

## How to Obtain Field Name in `struct`

::: note

`struct` Elements in `StructType` may defer from those in `DICompositeType` because of alignment. Compiler may add additional elements to `StructType` for alignment, but not for `DICompositeType`. Therefore, the better way to find corresponding elements in `StructType` and `DICompositeType` is by offset.

:::

The key point is to maintain mapping between `llvm::Type` and `llvm::DIType`, `llvm::Value` and `llvm::DINode`.

See [lib-monitor/inserter/field_name_extractor at main · liblaf/lib-monitor](https://github.com/liblaf/lib-monitor/tree/main/inserter/field_name_extractor) for implementation details.

## Strange Things about `getelementptr`

### Invalid element idx!

```c
const struct __attribute__((packed)) { uint32_t v; } *q = p;
uint32_t v;
__asm__ ("ldr  %0, %1" : "=r"(v) : "m"(*q));
```

```llvm
%struct.anon.0 = type { i32 }
...
%89 = load %struct.anon.0*, %struct.anon.0** %13, align 4, !dbg !3598
%90 = getelementptr inbounds %struct.anon.0, %struct.anon.0* %89, i32 1, !dbg !3598
%91 = call i64 asm "ldr   ${0:Q}, $1  \0A\09ldr   ${0:R}, $2  \0A\09", "=&r,*m,*m"(%struct.anon.0* %88, %struct.anon.0* %90) #7, !dbg !3599, !srcloc !3600
```

::: warning

Pay attention to the `GetElementPtrInst`!

:::

## Reference

[^1]: <https://llvm.org/docs/SourceLevelDebugging.html>
