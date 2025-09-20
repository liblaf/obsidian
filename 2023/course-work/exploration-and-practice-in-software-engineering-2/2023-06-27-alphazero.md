---
category:
  - Course Work
layout: Slide
title: AlphaZero 大作业展示
date: "2023-06-27T00:00:00+08:00"
tags:
  - Exploration and Practice in Software Engineering (2)
---

@slidestart

## AlphaZero 大作业展示

---

## 实现思路

--

### MCTS

```python
def get_action_probs(board, player):
    if training:
        repeat search num_sim times
    else:
        return policy predicted by NNet
```

```python
def search(board):
    if not visited:
        policy, value = NNet(board)
        update_statistics(board, probabilities, value)
        return -value
    action = argmax(mean-value)
    value = search(next(board, action))
    update_statistics(board, action, value)
    return -value
```

--

### Neural Network

- 示例网络
- 将 `Board` 分解为三个 channel, 分别表示 黑子, 空位, 白子

--

### Performance

- 并行对局, 独有 MCTS 实例, 共享 NNet 参数
- 训练网络时, 增大 Batch Size
- Processes: 16; CPU: 2014 年的 E5, GPU: RTX 3090
- 平均 26 min / iter, 每个 iter 包括 128 局自我对弈 + 8 Epochs 训练 + 100 局与 `last_net` 对弈 + (如果网络更新) 100 局与 Random 对弈
- GPU 利用率: ~10% --> 100%

---

## 训练结果

---

## 可能的问题

### Loss 函数有误

- Loss 函数已和同学交流确认过, 应该没有问题
- 计算 Loss 函数时已使用 `assert` 判断形状无误
- Loss 值与成功训练的同学的 Loss 值相近

--

### NNet 实现有误

- 测试使用的是未经修改的示例网络, 已有同学使用相同网络训练成功
- 网络 Loss 正常下降

--

### MCTS 实现有误

- 在小棋盘下, 随着同一 MCTS 实例对局次数的增加, 其理论实力会不断变强. 实际测试中, 使用随机的网络 + MCTS 与 Random 在 5x5 棋盘连续对局 100 局, 胜率总能超过 90%, 表明 MCTS 实现应该没有问题
- 对局过程中使用 `assert` 测试通过, 说明 MCTS 输出的 action 合法

@slideend
