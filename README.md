# Data

`results_summary.csv` holds the end-of-run values (t = 1800 s) for the four battery arrangements.

| Column | Meaning | Source |
|---|---|---|
| `peak_battery_temp_K` | Maximum cell surface temperature | Fluent contour legend (max), Fig. 5.1 of the thesis |
| `min_battery_temp_K` | Minimum cell surface temperature | Fluent contour legend (min), Fig. 5.1 |
| `battery_temp_spread_K` | Peak minus minimum: a measure of temperature non-uniformity across the module | Derived |
| `mean_liquid_fraction` | Volume-averaged PCM liquid fraction, i.e. share of latent capacity already used | Fluent report, Table 5.1 / Fig. 5.6 |
| `max_local_liquid_fraction` | Highest local liquid fraction in the PCM | Fluent contour legend (max), Fig. 5.3 |

## Adding the raw Fluent report files

If you have the original Fluent report-definition output files (`*.out`), place them in
`data/fluent_reports/` and plot the full time histories with:

```bash
python scripts/fluent_reports.py data/fluent_reports/*.out --out figures/time_histories_raw.png
```
