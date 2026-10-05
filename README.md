# Passive Thermal Management of a Li-ion Battery Module with Phase Change Material

**Transient CFD study (ANSYS Fluent) comparing four arrangements of 12 cylindrical Li-ion cells embedded in a phase change material (PCM).**
B.Tech final-year project, Mechanical Engineering, PVP Siddhartha Institute of Technology, India (2023–2024).

![Cell surface temperature of the four arrangements at t = 1800 s](figures/battery_temperature_contours.png)
<sub>Cell surface temperature after 30 min of heat generation. Note that each panel has its own colour scale.</sub>

## Key results

| | Design 1 | **Design 2** | Design 3 | Design 4 |
|---|---|---|---|---|
| Peak cell temperature [K] | 315.1 | **315.0** | 315.5 | 315.7 |
| Cell temperature spread (max − min) [K] | 1.0 | **1.0** | 2.1 | 1.6 |
| Mean PCM liquid fraction [–] | 0.741 | **0.725** | 0.744 | 0.844 |

- **The PCM caps the temperature rise.** The cells heat up quickly (≈ 0.7 K/min) until the PCM starts melting at about 15 min. Once melting begins, latent heat absorption slows the rise to ≈ 0.3 K/min. After 30 min, every design sits inside the PCM melting window (311–316 K).
- **Arrangement matters less than the PCM itself.** At equal PCM volume, the four layouts differ by only 0.7 K in peak temperature.
- **Arrangement does matter for uniformity and reserve.** Design 3 has twice the cell-to-cell temperature spread of Designs 1 and 2. Design 4 has already melted 84 % of its PCM, compared with 73 % for Design 2, so it has the least latent capacity left and would saturate first under a longer load.
- **Design 2 (two staggered rows of six cells) performs best on all three metrics.** A likely reason is that the elongated layout puts more cells close to the cooled outer walls, which shortens the conduction path from each cell to the boundary.

![Summary metrics](figures/summary_metrics.png)

## Problem setup

| | |
|---|---|
| Geometry | 12 cylindrical Li-ion cells in a rectangular PCM block, built in ANSYS SpaceClaim; four arrangements with the same PCM volume (≈ 220 cm³) |
| Mesh | ANSYS Meshing, 2.23 M nodes / 435 k elements; ≈ 87 % of elements with orthogonal quality > 0.8 |
| Physics | 3D transient conjugate heat transfer; enthalpy–porosity solidification/melting model for the PCM; Fluent battery model with uniform volumetric heat generation of 50 kW/m³ |
| PCM | Composite PCM: latent heat 165 kJ/kg, solidus 311 K, liquidus 316 K, thermal conductivity 3 W/(m·K) |
| Boundary conditions | Initial temperature 300 K; natural-convection heat loss on the outer PCM walls (h = 5 W/(m²·K)) |
| Solver | ANSYS Fluent 2023 R1, pressure-based, laminar, first-order implicit in time; Δt = 60 s, 30 steps (1800 s) |

<details>
<summary>Governing equations and material properties</summary>

**Cell energy balance** (constant properties, uniform heat generation, radiation neglected):

$$\rho_b c_{p,b}\frac{\partial T}{\partial t} = \lambda_x\frac{\partial^2 T}{\partial x^2} + \lambda_y\frac{\partial^2 T}{\partial y^2} + \lambda_z\frac{\partial^2 T}{\partial z^2} + q_b$$

**PCM (enthalpy method):** the total enthalpy is the sensible part plus the liquid fraction β times the latent heat L:

$$\rho_{pcm}\frac{\partial H}{\partial t} = \lambda_{pcm}\nabla^2 T, \qquad H = h_{ref} + \int_{T_{ref}}^{T} c_{p}\,dT + \beta L$$

| Zone | Density [kg/m³] | c<sub>p</sub> [J/(kg·K)] | k [W/(m·K)] |
|---|---|---|---|
| Cell (active material) | 4450 | 790 | 17.2 |
| Positive terminal | 2100 | 710 | 15.11 |
| Negative terminal | 3600 | 740 | 0.687 |
| PCM | polynomial | polynomial | 3 |

</details>

![Computational mesh](figures/mesh.png)

## More results

**Transient response.** Melting starts at about 900 s. From that point, the temperature curves flatten while the liquid fraction rises almost linearly.

![Time histories](figures/time_histories.png)

**PCM liquid fraction.** Melting is furthest along between the central cells, where heat accumulates. The PCM next to the cooled outer walls has melted least.

![PCM liquid fraction](figures/pcm_liquid_fraction_contours.png)

<details>
<summary>PCM temperature contours and Design 2 geometry</summary>

![PCM temperature](figures/pcm_temperature_contours.png)
![Design 2 geometry](figures/design2_geometry.png)

</details>

## Limitations and next steps

These results come from a student project. The following points limit how far they can be trusted, and each one suggests a direction for further work:

- **No mesh or time-step independence study.** The study uses a single mesh and a coarse time step (60 s, at most 10 iterations per step). The minimum orthogonal quality is 0.04, in the negative-terminal zone. Differences below 1 K between designs should therefore be confirmed with refined runs.
- **Simplified heat source.** Heat generation is uniform and constant. A next step would be state-of-charge-dependent heat generation from an electrochemical (NTGK/ECM) model, together with a validation case against published experimental data.
- **Short time horizon.** The simulation covers only 30 min of heating. Repeated charge/discharge cycles would show which design saturates first, an effect hinted at by Design 4's higher melt fraction.
- **Design-space exploration.** A parametric sweep over cell spacing, PCM conductivity and heat load, combined with a surrogate model such as a Gaussian process, could map the whole design space rather than comparing four hand-picked layouts.

## Reproduce the figures

```bash
pip install -r requirements.txt
python scripts/plot_summary.py                      # figures/summary_metrics.png
python scripts/fluent_reports.py data/fluent_reports/*.out   # time histories from raw Fluent report files
```

The end-of-run values are in [`data/results_summary.csv`](data/results_summary.csv), and their sources are documented in [`data/README.md`](data/README.md).

## Repository structure

```
├── data/
│   ├── results_summary.csv     # end-of-run metrics for the four designs
│   └── README.md               # column definitions and sources
├── figures/                    # contour plots, time histories, summary chart
├── scripts/
│   ├── plot_summary.py         # comparison chart from results_summary.csv
│   └── fluent_reports.py       # parser + plotter for Fluent report (.out) files
└── requirements.txt
```

## Team and acknowledgements

This was a team project by V. Teja Siva Naga Sai, P. Divya, S. Gayatri Prasad and V. Karthik Reddy, supervised by Dr. P. Phani Prasanthi, Department of Mechanical Engineering, PVP Siddhartha Institute of Technology, Vijayawada.
<!-- TODO: add one line describing your own contribution, e.g. "My role: geometry, meshing, Fluent setup and post-processing." -->
