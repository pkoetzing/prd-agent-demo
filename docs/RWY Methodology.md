# 8. Representative Weather Year (RWY) Methodology

## Purpose

The RWY procedure selects one continuous 8 760-hour window whose weather statistics are most similar to the long-term (1980 – 2022) climate of Central Western Europe (Germany, Netherlands, United Kingdom).
Running power-system simulations on this single year preserves the bulk characteristics of 43 years of weather while cutting computation time.

## Input Data

* **Temporal range:** 1 Jan 1980 – 31 Dec 2022
* **Resolution:** hourly
* **Variables:** Temperature (°C), Solar PV load factor, Onshore & Offshore wind load factors
* **Countries:** DE, NL, UK

## Methodological Steps

### 8.1 Rolling-window feature calculation

* Slide a window of 8 760 h forward in 24-h steps.
* For every window, compute the **mean** (μ) and **standard deviation** (σ) of each weather variable.
   
  *Rationale:* The pair (μ, σ) captures both average conditions and intra-year volatility.

---

### 8.2 Per-feature standardisation

* Across all candidate windows, **z-score** each of the μ and σ columns:

$$
z_{j}=\frac{x_{j}-\bar{x}}{s_x}
$$

This places all features on a common, unit-variance scale **before any weighting**.
 
*Rationale:* Removes unit differences (°C vs. p.u.) and ensures later weights influence the similarity metric rather than being cancelled out.

---

### 8.3 Apply variable weighting based on energy-system impact

Multiply every standardised feature that belongs to variable *i* by its energy-system weight *w\_i*:

$$
z_{j}^{(\text{weighted})}=w_i\;z_{j}
$$

* **VRE variables (solar, onshore, offshore wind):**

  * $w_i$ = annual energy generation (MWh) of the technology in 2024.
* **Temperature:**

  * $w_i$ = demand-temperature sensitivity (MWh / °C) × standard deviation of annual mean temperature.

 
*Rationale:* Because weighting is applied **after** standardisation, the factors do **not** get cancelled; they genuinely tilt the distance metric toward variables that matter most for today’s power balance.

> **Implementation tip** If you want the weight to reflect variance contribution rather than amplitude, scale by $\sqrt{w_i}$.

---

### 8.4 Principal Component Analysis (PCA)

* Concatenate all weighted z-scores of a window into a feature vector.
* Perform PCA on this matrix to obtain uncorrelated principal components (PCs).
   
  *Rationale:* Removes collinearity (e.g. on- & offshore wind) so that correlated variables do not double-count in the distance metric.
  *Component retention rule:* keep PCs that together explain ≥ 95 % of total variance.

---

### 8.5 Distance calculation in PC space

* Let $\mathbf{y}_k$ be the PC vector for window *k* and $\bar{\mathbf{y}}$ the long-term climatology (the mean of all windows, typically ≈ 0).
* Compute the **Euclidean distance**

$$
d_k=\bigl\|\,\mathbf{y}_k-\bar{\mathbf{y}}\,\bigr\|_2
$$

*Rationale:* A single metric now integrates differences in both averages and variabilities, already weighted by energy importance and rid of redundancy.

---

### 8.6 RWY selection

Choose the window with the smallest distance $d_k$.
 
*Rationale:* This window is statistically the closest analogue to 43-year climatology once energy-system importance is honoured.

---

### 8.7 Post-processing

Rotate the chosen window so that it starts on **1 January 00:00** and ends on **31 December 23:00**.
 
*Rationale:* Ensures compatibility with power-system models that expect calendar-aligned years.

---

## Summary of key principles

| Step                             | Why it matters                                 |
| -------------------------------- | ---------------------------------------------- |
| Calculate μ & σ per window       | Capture level and volatility                   |
| **Standardise before weighting** | Keep units comparable so weights take effect   |
| Apply weights to z-scores        | Push high-impact variables to drive similarity |
| PCA on weighted space            | Remove redundant information                   |
| Euclidean distance in PC space   | One metric combines all effects                |
| Pick minimum-distance window     | Select statistically most representative year  |

---

### Notes

* Weight factors can be re-tuned when the energy mix changes (e.g. 2030 scenario).
* If extreme-condition years are also needed, repeat the procedure with a distance metric targeted at tails rather than means.
