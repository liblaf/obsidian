---
created: 2025-05-05T21:08:49+08:00
modified: 2025-05-18T15:55:26+08:00
tags:
  - Awesome_List
  - Experiment_Tracking
title: Awesome Experiment Tracking
---

|            | Self-Hostable |   Free Quota    | ANSI | Dark Mode | Live Console | Metadata | Uncommitted Changes | Artifacts | Nested Metric |
| :--------: | :-----------: | :-------------: | :--: | :-------: | :----------: | :------: | :-----------------: | :-------: | :-----------: |
| neptune.ai |       ❌       |      200GB      |  ❌   |     ❌     |      ✅       |    ✅     |          ✅          |     ✅     |       ✅       |
|   MLflow   |       ✅       |   self-hosted   |  ❌   |     ✅     |      ❌       |    ✅     |          ❌          |     ✅     |       ✅       |
|   Comet    |       ✅       |      500GB      |  ✅   |     ❌     |    ⚠️[^1]    |    ✅     |          ✅          |     ✅     |       ✅       |
|  ClearML   |     ✅[^2]     | 1GB metrics[^3] |  ✅   |     ✅     |    ✅[^4]     |    ✅     |          ✅          |     ✅     |       ✅       |
|    W&B     |       ❌       |      200GB      |  ✅   |     ❌     |    ✅[^4]     |    ❌     |          ❌          |     ✅     |       ✅       |

- **Live Console:** I can view the progress of my experiment from any device.

[^1]: Comet only shows the end of stdout / stderr.
[^2]: ClearML is complex and resource-consuming to self-host.
[^3]: 1GB metrics is far from enough. A typical Task requires about 5MB.
[^4]: ClearML, W&B do not distinguish between stdout and stderr.

### Self-Hostable

- **MLflow** is the easiest to self-host
- **ClearML** is complex and resource-consuming
