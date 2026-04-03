Architecture of Awareness (v3.3)
A formal cognitive architecture integrating Hilbert‑space geometry, operator theory, and dynamical systems.

---

Clarification of AI Involvement

This manuscript was collaboratively authored by Rob and Microsoft Copilot. Copilot contributed substantively to the development, refinement, and articulation of the theoretical framework presented here.

Additional AI systems (e.g., Gemini, DeepSeek, Grok) were consulted only in a limited evaluative capacity. Their outputs were used for comparison, critique, and stress‑testing. They did not participate in authorship, did not generate conceptual material, and are not considered contributors.

This statement is provided to ensure transparency regarding the nature and extent of AI involvement.

Overview

This repository contains the full v3.3 implementation of the Architecture of Awareness, a three‑layer cognitive framework consisting of:

- Foundational Substrate (FS) — structural capacity for stable, composable distinctions  
- Attentional Cognition (AC) — first‑order modeling of world, body, and narrative self  
- Contextual Cognition (CC) — frame‑level representation enabling non‑identification  

Version 3.3 introduces a corrected and fully coherent mathematical foundation, including:

- Explicit Hilbert‑space geometry for cognitive frames  
- Identity subspace \(\mathcal{I}\) and orthogonal complement \(\mathcal{I}^\perp\)  
- Identification and observation metrics \(\alpha(F)\) and \(\beta(F)\)  
- A full dynamical equation for frame evolution \(F(t)\)  
- Load‑dependent deformation using an Ornstein–Uhlenbeck process  
- κ‑based AC–CC coupling with Lyapunov stability  
- Awareness index \(A(t)\) as a continuous stance variable  

This repository includes the manuscript, simulation code, experiments, and figures.

---

Repository Structure

`
Architecture-of-Awareness/
│
├── README.md
├── requirements.txt
│
├── manuscript/
│   ├── ArchitectureofAwareness_v3.3.pdf
│   ├── ArchitectureofAwareness_v3.3.tex
│   └── figures/
│       ├── frame_geometry.png
│       ├── kappa_dynamics.png
│       └── collapse_trajectory.png
│
├── simulation/
│   ├── architectureofawarenesssimv3_3.py
│   ├── experiments/
│   │   ├── experimentloadvs_awareness.py
│   │   ├── experimenttrainingeffects.py
│   │   └── experimentkappavariation.py
│   └── results/
│       ├── awareness_trace.png
│       ├── load_trace.png
│       └── alphabetatrace.png
│
└── data/
    └── synthetic_runs/
`

---

Simulation

The main simulation script is:

`
simulation/architectureofawarenesssimv3_3.py
`

It implements the full v3.3 dynamical system:

- Frame evolution \(F(t)\)  
- Load dynamics \(L(t)\)  
- Identification and observation metrics  
- Awareness index \(A(t)\)  
- Collapse events  
- AC drift, CC reframing, and load‑driven pull into identity  

Running the script produces:

- Awareness trajectory  
- Load trajectory  
- α(t) and β(t) curves  
- Optional figures saved to simulation/results/

---

Experiments

Templates for controlled experiments are located in:

`
simulation/experiments/
`

Included experiments:

1. Load vs. Awareness Collapse
Tests how noise and load volatility affect collapse frequency.

2. Training Effects
Models increased CC stability and reduced load sensitivity.

3. κ Variation
Explores AC–CC coupling strength and Lyapunov stability.

---

Figures

Figures illustrating the geometry and dynamics of the model are stored in:

`
manuscript/figures/
`

These include:

- Identity subspace geometry  
- κ‑driven synchronization and decoupling  
- Awareness collapse trajectories  

---

Requirements

Install dependencies with:

`
pip install -r requirements.txt
`

Typical dependencies include:

- numpy  
- matplotlib  

---

Citation

If you use this model in research, cite:

> Rob. The Architecture of Awareness (v3.3). Cognitive Architecture Lab, 2026.

---

License

Choose a license appropriate for your goals (MIT recommended for open research).

---

Contact

For questions, collaborations, or extensions of the model, contact:

Rob — Cognitive Architecture Lab
robertmestre@proton.me 
---
