# ✅ PRD Product Requirements Document

---

## 1. Title
**Representative Weather Year Finder – Python App**

---

## 2. Purpose / Objective

We aim to identify a **Representative Weather Year (RWY)** — a 365-day window that serves as a proxy for long-term weather conditions.
The detailed methodology is described in Section 8.

------

## 3. Background / Context

Currently, simulations are run using a legacy weather year 
that hasn't been reviewed for a long time.

---

## 4. Users / Personas

- Energy market analysts (internal Markets/Analysis team)
- Power price forecasters
- Model developers maintaining SRMC simulations

---

## 5. Scope

### ✅ In Scope
- Output a ranked list of the most representative 365-day windows
- Export the top 1 RWY, reordered to start on Jan 1
- Identify RWYs for:
  - Full period: 1980–2022
  - Recent history: 2013–2022

### ❌ Out of Scope
- GUI or web interface
- Precipitation, humidity, or other meteorological data
- Integration with downstream modeling tools

---

## 6. Requirements

### 🔧 Functional Requirements
- Input:
  - Load hourly weather data from a `.parquet` file
  - Read global weighting factors from a `.csv` file
- Output:
  - Top 1 represenative weather years (RWY) for:
    - Full period (1980–2022)
    - Recent history (2013–2022)
  - Metadata summary (e.g., window score, start date, end date)
  - Parquet/CSV of reordered year
  - Scorecard for all candidates

### ⚙️ Non-Functional Requirements
- Simple Python 3.12 script w/o CLI
- Use **pandas** for data manipulation
- Modular, testable codebase
- Unit tests written using **pytest**
- Windows platform
---

## 7. Data Requirements

### ✅ Weather Data Input Format
- Format: `.parquet`
- File: `weather_history.parquet`
- Structure: `DatetimeIndex` called `timestamp`, 
  timezone-naive, no leap years
  43 years x 24 hours x 365 days = 376,680 hourly entries
  from 1980–01–01 to 2022–12–31
- Columns:
  - `Temperature:` temperature_{de,nl,uk}
  - `Solar:` solar_load_factor_{de,nl,uk}
  - `Wind (Onshore):` onwind_load_factor_{de,nl,uk}
  - `Wind (Offshore):` offwind_load_factor_{de,nl,uk}

### ✅ Weather Metrics Weights Input Format
- Format: `.csv`
- File: `weather_metric_weights.csv`
- Structure: 1 row per country, 1 column per variable
- Columns:
  - `country`: DE, NL, UK
  - `solar`: weight for solar generation
  - `onwind`: weight for onshore wind generation
  - `offwind`: weight for offshore wind generation
  - `temperature`: weight for temperature impact on demand

---

## 8. Representative Weather Year (RWY) Methodology

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
| Standardise before weighting | Keep units comparable so weights take effect   |
| Apply weights to z-scores        | Push high-impact variables to drive similarity |
| PCA on weighted space            | Remove redundant information                   |
| Euclidean distance in PC space   | One metric combines all effects                |
| Pick minimum-distance window     | Select statistically most representative year  |

---

### Notes

* Weight factors can be re-tuned when the energy mix changes (e.g. 2030 scenario).
* If extreme-condition years are also needed, repeat the procedure with a distance metric targeted at tails rather than means.

---

## 9. Success Criteria
- Select RWYs for:
  - Full period (1980–2022)
  - Recent period (2013–2022)
- Process data in under 1 minute
- Output includes:
  - Top ranked RWY (reordered)
  - All candidate windows with scores
  - Summary stats (means, variances, trends)

---

## 10. Risks & Challenges
- Climate trends may bias RWY selection
- Reordering from arbitrary start date to Jan 1 may introduce edge artifacts, especially if beginning and end weather conditions differ significantly.
