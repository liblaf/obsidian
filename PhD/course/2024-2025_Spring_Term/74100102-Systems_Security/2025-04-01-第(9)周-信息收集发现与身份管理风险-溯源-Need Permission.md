---
created: 2025-04-01T00:00:00+08:00
modified: 2025-04-20T19:07:39+08:00
tags:
  - PhD/Course/Systems_Security
title: 第(9)周-信息收集发现与身份管理风险-溯源-Need Permission
---

> [!QUESTION]
> 请根据课堂上讲解的要求, 撰写溯源分析报告, 对于每条分析, 需包含: 日志条目的截图 / 文本、对此日志条目所代表的动作的描述、发生的时间.

**攻击方式:** 通过修改 Cookie 参数 `permission=guest` 为 `permission=admin`, 以管理员身份非法访问页面.

#### 1. 初始访问尝试 (探测行为)

**日志条目:**

```csv
...
ea7802ee-c93f-4d3e-9790-c718b4fecf5d,...,2025-04-14 19:33:47,...,GET,/admin,...,http_cookie=permission=guest
...
```  

**时间:** `2025-04-14 19:33:47`
**动作描述:** 攻击者首次尝试访问敏感路径 `/admin`, 但携带 `permission=guest` 的 Cookie, 表明此时尚未成功提权. 此行为可能是对后台路径的探测.

#### 2. 路径遍历探测

**日志条目:**

```csv
...
ea7802e...,2025-04-14 19:33:47,...,GET,/admi,...,http_cookie=permission=guest
ea7802e...,2025-04-14 19:33:47,...,GET,/ad,...,http_cookie=permission=guest
...
```  

**时间:** `2025-04-14 19:33:47`
**动作描述:** 攻击者尝试访问不完整路径 `/admi` 和 `/ad`, 可能是通过路径遍历探测服务器漏洞, 但 Cookie 仍为 `guest` 身份.

#### 3. 参数篡改尝试

**日志条目:**

```csv
...
ea7802e...,2025-04-14 19:33:47,...,GET,/?user=admin,...,http_cookie=permission=guest
...
```  

**时间:** `2025-04-14 19:33:47`
**动作描述:** 攻击者尝试通过 URL 参数注入 `user=admin`, 但未修改 Cookie, 服务器未响应提权.

#### 4. Cookie 篡改攻击 (关键步骤)

**日志条目:**

```csv
...
ea7802e...,2025-04-14 19:34:50,...,GET,/,...,http_cookie=permission=admin
User-Agent: curl/8.7.1
...
```  

**时间:** `2025-04-14 19:34:50`
**动作描述:** 攻击者将 Cookie 修改为 `permission=admin`, 并通过 `curl` 工具发起请求, 成功以管理员身份访问根路径 `/`. 此条目为首次提权成功的直接证据.

#### 5. 持续性访问 (攻击成功)

**日志条目:**

```csv
...
ea7802e...,2025-04-14 19:36:54,...,GET,/,...,http_cookie=permission=admin
User-Agent: curl/8.7.1
...
```  

**时间:** `2025-04-14 19:36:54`
**动作描述:** 攻击者在后续多次请求中持续使用 `permission=admin` 的 Cookie, 确认提权成功并维持管理员会话.

### 攻击链总结

1. **探测阶段** (19:33:47): 尝试访问敏感路径和参数注入, 使用 `guest` 身份.
2. **提权阶段** (19:34:50): 篡改 Cookie 为 `admin`, 工具化请求验证权限.
3. **维持访问** (19:36:54): 多次重复攻击以巩固权限.

**结论**: 攻击者通过修改 Cookie 参数绕过身份验证.

```mermaid
timeline
    title "攻击时间线 (2025-04-14)"
    section "探测阶段"
        {19:33:47} : "访问 /admin (Cookie: guest)"
        "19:33:47" : "路径遍历 (/admi, /ad)"
        "19:33:47" : "参数注入 (/?user=admin)"
    section "提权阶段"
        "19:34:50" : "首次篡改 Cookie (permission=admin)"
    section "维持访问"
        "19:36:54" : "重复提权请求 (3 次)"
```
