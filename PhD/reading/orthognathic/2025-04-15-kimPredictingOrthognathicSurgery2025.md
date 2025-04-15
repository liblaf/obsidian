---
created: 2025-04-15T10:58:48+08:00
modified: 2025-04-15T11:17:55+08:00
tags:
  - Orthognathic
title: Predicting orthognathic surgery results as postoperative lateral cephalograms using graph neural networks and diffusion models
---

> Kim, I.-H., Jeong, J., Kim, J.-S., et al. 2025. Predicting orthognathic surgery results as postoperative lateral cephalograms using graph neural networks and diffusion models. *Nature Communications* *16*, 1, 2586.

## Abstract

> Orthognathic surgery, or corrective jaw surgery, is performed to correct severe dentofacial deformities and is increasingly sought for cosmetic purposes. Accurate prediction of surgical outcomes is essential for selecting the optimal treatment plan and ensuring patient satisfaction. Here, we present GPOSC-Net, a generative prediction model for orthognathic surgery that synthesizes post-operative lateral cephalograms from pre-operative data. GPOSC-Net consists of two key components: a landmark prediction model that estimates post-surgical cephalometric changes and a latent diffusion model that generates realistic synthesizes post-operative lateral cephalograms images based on predicted landmarks and segmented profile lines. We validated our model using diverse patient datasets, a visual Turing test, and a simulation study. Our results demonstrate that GPOSC-Net can accurately predict cephalometric landmark positions and generate high-fidelity synthesized postoperative lateral cephalogram images, providing a valuable tool for surgical planning. By enhancing predictive accuracy and visualization, our model has the potential to improve clinical decision-making and patient communication.

## Denotations

- **CFG** - Classifier-Free Guidance
- **DDS** - Doctor of Dental Surgery
- **FOV** - Field Of View
- **IASM** - Intended Amount of Surgical Movement
- **IEM** - Image Embedding Module
- **LTEM** - Landmark Topology Embedding Module
- **OD** - OrthoDontist
- **OGS** - OrthoGnathic Surgery
- **OMFS** - Oral and Maxillofacial Surgeon
- **post-ceph** - real post-op lateral cephalograms
- **post-op** - post-operational
- **pre-ceph** - pre-operational cephalogram
- **spost-cephs** - synthetic post-op lateral cephalograms
- **VTT** - Visual Turing Test
