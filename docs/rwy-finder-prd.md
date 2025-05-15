# ✅ Product Requirements Document — Representative Weather Year Finder (rwy‑finder)

*Last updated: **11 May 2025***

---

## 1  Title

**Representative Weather Year Finder – Python Application**

---

## 2  Purpose / Objective

Determine one or more **Representative Weather Years (RWYs)** — contiguous 8 760‑hour windows that approximate long‑term (1980‑2022) weather conditions in Central Western Europe. The RWYs accelerate BID3 power‑market simulations while preserving statistical realism.

---

## 3  Background / Context

Studies currently rely on an outdated weather year. Updating this input promises more trustworthy spot‑price, adequacy, and dispatch analyses while cutting runtime.

---

## 4  Users / Personas

* Energy‑market analysts (Markets / Analysis team)
* Power‑price forecasters
* Model developers maintaining SRMC / BID3 simulations

---

## 5  Scope

### ✅ In scope

* Produce a **ranked list** of RWY candidates (distance metrics in §8)
* Export the **top 10** windows (markdown table with start/end dates + metrics)
* Export the **best** window reordered to start **01 Jan 00:00** (Parquet)
* Identify RWYs for two horizons

  * **Full period:** 1980 ‑ 2022
  * **Recent decade:** 2013 ‑ 2022

### ❌ Out of scope

* GUI or web interface
* Additional meteorological variables (precipitation, humidity, …)
* Direct integration with downstream tools (handled separately)

---

## 6  Requirements

### 6.1  Functional

| #   | Requirement |
|-----|-------------|
| F‑1 | **Input**: read hourly weather time‑series from `${DATA_PATH}/weather_history.parquet` (see §7) |
| F‑2 | **Input**: read weighting factors from `${DATA_PATH}/weather_metric_weights.csv` |
| F‑3 | Slide an 8 760‑hour window in 24‑hour steps over the data set (no leap‑day rows are present) |
| F‑4 | Compute features, weighting, PCA, and distance as in §8 (retain PCs explaining **≥ 95 %** variance) |
| F‑5 | Write **intermediate artefacts** to `${DATA_PATH}/YYYYMMDD_HHMM/` subfolder:<br>• feature matrices (Parquet)<br>• PCA loadings & explained‑variance **PNG**<br>• distance time‑series (Parquet) |
| F‑6 | A **Sankey diagram** is produced from the Varimax-rotated squared-loading matrix: the 24 weather features form the source nodes, the six rotated PCs form the target nodes, and link widths are proportional to each feature’s percentage contribution to each component (thresholded at ≥ 2 % for clarity). The graphic makes it visually obvious, e.g., that RPC 3 is nearly a pure ‘solar-mean’ axis while RPC 6 is dominated by ‘temperature variability’. |
| F‑7 | Write `rwy_candidates.parquet` to the same subfolder — Parquet table with Start/End (dates only) & three distances |
| F‑8 | Write `rwy_top10_full.md` and `rwy_top10_recent.md` — markdown tables (rank 1‑10, start\_ts, end\_ts, all three distances) for full and recent periods |
| F‑9 | Write `rwy_best_full.parquet` and `rwy_best_recent.parquet`: hourly series (8 760 rows × variables) reordered to calendar year |
| F‑10 | All exported Parquet files must have `timestamp` as index and follow the **8 760‑h, no‑leap‑day convention** used by BID3 |
| F‑11 | **Plot** the `rwy_candidates` time series: Euclidean distance vs. window start date, and save as `rwy_candidates.png` in the output folder |

### 6.2  Non‑functional

* Python ≥ 3.12, pandas, scikit‑learn, pytest
* Modular, unit‑tested codebase (≥ 90 % coverage goal)
* End‑to‑end runtime **≤ 60 s** on analyst‑grade hardware (Apple M2 / Intel i7) — confirmed acceptable
* Works cross‑platform (Windows, macOS, Linux CI)

---

## 7  Data Requirements

|  File                         |  Format  |  Rows × Cols  |  Notes                                                          |
| ----------------------------- | -------- | ------------- | --------------------------------------------------------------- |
|  `weather_history.parquet`    | Parquet  | 376 680 × 12  | Hourly 1980‑01‑01 → 2022‑12‑31, **no leap years**               |
|  `weather_metric_weights.csv` | CSV      | 3 × 5         | DE, NL, UK weights for temperature, solar, on‑ & off‑shore wind |

Both live under the directory given by the **`DATA_PATH` environment variable**.

---

## 8  Methodology

### 8.1  Feature calculation

For each 8 760‑h window compute **mean** μ and **standard deviation** σ per weather variable.

### 8.2  Standardisation

Z‑score every μ and σ across all windows:
$z_j = \frac{x_j - \bar{x}}{s_x}$

### 8.3  Energy weighting

Multiply each standardised feature by its technology weight $w_i$:
$z_j^{(\text w)} = w_i \, z_j$

### 8.4  Principal‑Component Analysis

Perform PCA on the weighted matrix. **Retain PCs that jointly explain ≥ 95 % total variance**.

**Decode the abstract PCs** into plain language labels following these steps
- Derive relevant PCs from the weighted-standardised feature matrix.
- Square-and-normalise loadings → % contribution table.
- Label each PC by its top drivers (≥ 10 % share or |loading| ≥ 0.30).
- Perform Varimax rotation to sharpen interpretation; recompute contributions.
- Report rotated PCs, driver tables and visual aids; retain the name “RPC k” in downstream documentation.
- Use the Python factor_analyzer package for rotation.

### 8.5  Distance metrics

For every window *k* compute three distances in PC‑space:

* **Euclidean**:  $d_k^{(E)} = \lVert \mathbf y_k - \bar{\mathbf y} \rVert_2$
* **Mahalanobis** (diagonal covariance in PC‑space equals $\mathbf I$ so equivalent to χ²):
  $d_k^{(M)} = \sqrt{ \sum_i \frac{y_{k,i}^2}{\lambda_i} }$
* **Cosine** similarity converted to distance:
  $d_k^{(C)} = 1 - \cos(\theta_k) = 1 - \frac{\mathbf y_k \cdot \bar{\mathbf y}}{\lVert\mathbf y_k\rVert \, \lVert\bar{\mathbf y}\rVert}$

### 8.6  RWY selection & post‑processing

Rank windows by Euclidean distance (primary), with Mahalanobis and cosine reported for comparison. Rotate the best window so it starts on **01 Jan 00:00** before exporting.

---

## 9  Outputs Overview

|  Artefact                    |  Format  |  Path (relative to `DATA_PATH`)  |  Description                                     |
| ---------------------------- | -------- | -------------------------------- | ------------------------------------------------ |
| `features.parquet`           | Parquet  | `YYYYMMDD_HHMM/`                 | Window‑level μ & σ (weighted)                    |
| `pca_components.parquet`     | Parquet  | `YYYYMMDD_HHMM/`                 | PCA loadings & singular values                   |
| `pca_explained_variance.png` | PNG      | `YYYYMMDD_HHMM/`                 | Scree plot                                       |
| `distance_series.parquet`    | Parquet  | `YYYYMMDD_HHMM/`                 | Distance per window (all 3 metrics)              |
| `rwy_candidates.parquet`     | Parquet  | `YYYYMMDD_HHMM/`                 | **All** windows with Start/End (dates only) + three distances |
| `rwy_candidates.png`         | PNG      | `YYYYMMDD_HHMM/`                 | Plot: Euclidean distance vs. window start date   |
| `rwy_top10_full.md`          | Markdown | `YYYYMMDD_HHMM/`                 | **Top 10** windows (rank & metrics, full period) |
| `rwy_top10_recent.md`        | Markdown | `YYYYMMDD_HHMM/`                 | **Top 10** windows (rank & metrics, recent decade)|
| `rwy_best_full.parquet`      | Parquet  | `YYYYMMDD_HHMM/`                 | Reordered hourly RWY 1980‑2022                   |
| `rwy_best_recent.parquet`    | Parquet  | `YYYYMMDD_HHMM/`                 | Reordered hourly RWY 2013‑2022                   |

---

## 10  Success Criteria

* Top 10 RWYs identified with Euclidean, Mahalanobis, and cosine metrics
* Artefacts saved under `${DATA_PATH}/YYYYMMDD_HHMM/` with naming above
* End‑to‑end run ≤ 60 s; unit tests pass in CI

---

## 11  Risks & Mitigations

|  Risk                         |  Mitigation                                              |
| ----------------------------- | -------------------------------------------------------- |
| Climate‑trend bias            | Detrend inputs or choose horizon‑specific climatology    |
| Edge artefacts after rotation | Visual QC & optional smoothing guard band                |
| Weight obsolescence           | Keep weights external; rerun when technology mix changes |
