# Task 1 — User Behaviour & Viewer Category Analytics
### تحليل سلوك المشاهدة وفئات المشاهدين

> Stage 1 of 3 · Input: `stc TV Data Set_T1.xlsb` (1,048,575 viewing events) · Output: 27 analytical tables + 3 models
> Project overview: [../README.md](../README.md)

---

## 1. What this stage is for

The raw viewing log is one row per **play event** — unvalidated, with corrupted titles, stuck streams and no session timestamps. Nothing in it can be trusted as a KPI until it is cleaned.

This folder is where we turned that log into a trustworthy analytical asset and then answered four business questions:

1. How do **Movies** and **Series** differ commercially?
2. What actually drives the **HD / SD** quality choice?
3. Which users are **about to leave**, and why?
4. What should the platform **do** about it?

The notebook follows the four levels of analytics — descriptive (§3–4), diagnostic (§5–6), predictive (§7), prescriptive (§9) — plus an anomaly / UBA watchlist (§8).

---

## 2. What we did, step by step

### ① Data cleaning & preprocessing (§2)

| Step | What we did | Result |
|---|---|---|
| Working copy | Never mutate the raw frame — all work happens on `df_copy` | Raw log stays reproducible |
| Missing values | `program_desc` nulls reconstructed from title metadata where possible | 14,038 nulls (1.34%) handled |
| **Title repair** | The source export dropped the capital **S** from many titles (`treets` → `Streets`, `murfs` → `Smurfs`). We wrote a rule-based restorer with a lower-case stop-word guard (`a, an, the, of, in, …`) so genuinely lower-case words are never "repaired" | Validated at **99.3% (143/144)** against independent ground-truth show names |
| Duplicates | Exact-duplicate log rows detected and reported (`DROP_EXACT_DUPLICATES` switch) | Reported, not silently dropped |
| Stuck streams | Plays longer than **12 h** treated as a device left playing, excluded from watch-time KPIs | 2,677 rows excluded |
| Bounces | Plays under **60 s** flagged as browsing — **kept** in reach metrics, excluded from depth metrics | 27.4% of all plays |

### ② Feature engineering (§2.5)

`watch_minutes`, `watch_hours`, `content_type`, `asset_key`, `episode_code`, `is_bounce`, `is_implausible`, `is_weekend`, plus per-user aggregates: `tenure_days`, `active_days`, `recency_days`, `genres_explored`, `hd_share`, `movie_share`, `views_per_active_day`.

### ③ Descriptive analytics (§3–4)

Headline KPI board, raw-vs-clean summary statistics (so the effect of cleaning is visible), Movies-vs-Series profiling, series depth (shows / seasons / episodes) and every Top-10 ranking table.

### ④ Diagnostic analytics (§5–6)

Reach-vs-depth correlation, genre mix, consumption over time, and the HD/SD split tested for significance with a **Mann-Whitney U** test — session lengths are heavily skewed, so a non-parametric test is the correct choice, not a t-test.

### ⑤ Segmentation (§6.3)

Three independent axes per user: **quality** (SD-Only → HD-Only), **engagement** (Light → Power), **content** (Movie Lover / Series Binger / Mixed).

### ⑥ Predictive modelling (§7)

| Model | Algorithm | Target | Performance |
|---|---|---|---|
| Demand forecast | Linear Regression (trend + day-of-week dummies) | Daily watch hours | **MAPE 10.9%** on a 30-day hold-out |
| Churn risk | Logistic Regression **and** Gradient Boosting | 30 days of inactivity | **ROC-AUC 0.878 / 0.888** |
| HD propensity | Logistic Regression (standardised) | HD vs SD play | **ROC-AUC 0.825** |

### ⑦ Anomaly watchlist — UBA (§8)

Four rules: daily plays above the 99.9th percentile (154/day), more than 24 h of playback in one day, ≥5 stuck sessions, and >90% bounce with >100 views. **128 users (1.11%)** raised 2 or more flags.

### ⑧ Data storytelling (§9)

Diagnostic findings converted into prescriptive actions, then every table exported to `outputs/`.

---

## 3. Files in this folder

| File | What it is | How it was produced |
|---|---|---|
| [stc TV_T1.ipynb](stc%20TV_T1.ipynb) | **The main deliverable.** 35 cells, 9 sections, fully executed — cleaning → KPIs → diagnostics → models → recommendations, with Matplotlib and Plotly figures embedded | Written for Google Colab; cell 0 installs `pyxlsb` automatically |
| [stc TV Data Set_T1.xlsb](stc%20TV%20Data%20Set_T1.xlsb) | Raw source data (40.8 MB binary Excel), sheet `Final_Dataset` — one row per viewing event | Provided extract — never modified |
| [stc_tv_user_behavior_analysis.py](stc_tv_user_behavior_analysis.py) | The **full pipeline as a script** (~1,300 lines, `# %%` cell format). Same logic as the notebook, runnable headlessly | Exported from the notebook and kept in sync |
| [stc_tv_simple_analysis.py](stc_tv_simple_analysis.py) | A **lightweight variant** (~330 lines): load → clean → KPIs → Movies vs Series → Top-10 → HD/SD → 4 charts. No models, no `outputs/` | The readable/reviewable version of the same cleaning logic |
| [stc_cleaned_data.csv](stc_cleaned_data.csv) | The **cleaned analytical table** (255 MB, 21 engineered columns) — the single source of truth every later table derives from | §9.3 of the notebook |
| [stc_cleaned_data_sample.csv](stc_cleaned_data_sample.csv) | First 1,000 rows of the same table — quick inspection without moving 255 MB | Sampled from the cleaned export |
| [top10_movies.csv](top10_movies.csv) | Top 10 movies by views, with unique users, watch hours, avg minutes, HD share | §4.3 |
| [top10_series.csv](top10_series.csv) | Top 10 shows by views, with episode count and genre | §4.3 |
| [top10_episodes.csv](top10_episodes.csv) | Top 10 individual episodes by views | §4.3 (also written by the simple script) |
| [stc TV Data Set_T2 - Sheet1.csv](stc%20TV%20Data%20Set_T2%20-%20Sheet1.csv) | Copy of the small T2 daily-watch-time extract, kept here as a cross-check reference for the demand forecast | Provided extract — the working copy lives in [../stc_TV_T2/](../stc_TV_T2/) |
| [outputs/](outputs/) | 27 numbered analytical tables + churn scores + user segments + one Excel workbook — see [outputs/README.md](outputs/README.md) | §9.3 export block |

> The three headline deliverables (`stc_cleaned_data.csv`, `top10_movies.csv`, `top10_series.csv`) sit **next to the notebook** for easy pickup; every supporting table goes into `outputs/` to keep this folder readable.

---

## 4. Key findings from this stage

**Headline KPIs**

| KPI | Value |
|---|---|
| Total views | 1,048,575 |
| Unique users | 11,578 |
| Total watch time | 290,861 h |
| Watch hours per user | 25.1 |
| Avg / median session | 16.7 min / **1.9 min** |
| HD share of views | 38.6% |
| **Bounce rate (<60 s)** | **27.4%** |

**Two products wearing one app**

| Metric | Movies | Series |
|---|---|---|
| Unique users | 11,355 | **3,901** (33.7%) |
| Watch hours | 84,772 (29.2%) | **206,089 (70.9%)** |
| Hours per user | 7.47 | **52.83** |
| Bounce rate | **38.1%** | 18.1% |
| Median session | 1.28 min | 18.63 min |

> **The finding that drives the whole project:** series generate 70.9% of watch time but reach only a third of users. The retention engine already exists — the product never routes users to it.

**The quality paradox** — HD is a *browsing* signature, not a viewing one. HD-Only users are 41.9% of the base but produce **1.1%** of watch time; SD-Leaning users are 16.5% of the base and produce **69.4%**.

**Churn is a recency problem** — `recency_days` dominates every other coefficient (**+1.497**), while `active_days` (−0.691) and `genres_explored` (−0.260) protect. 68.8% of users sit in the Critical band, yet the 930 Low-risk users hold **131,223 hours** — more than the entire Critical tail puts at risk.

---

## 5. How to re-run this stage

```bash
# Notebook (recommended)
jupyter notebook "stc TV_T1.ipynb"          # ~8–12 min, needs 8 GB RAM

# Or headless
python stc_tv_user_behavior_analysis.py     # full pipeline + all exports
python stc_tv_simple_analysis.py            # lightweight KPI-only variant
```

**Dependencies:** `pandas numpy scikit-learn scipy matplotlib plotly pyxlsb openpyxl`
(`pyxlsb` is mandatory — the source file is binary Excel, not `.xlsx`.)

**Config switches** live in the `CONFIG` dict at the top of the notebook / script:

| Key | Default | Effect |
|---|---|---|
| `DATA_PATH` / `SHEET_NAME` | `stc TV Data Set_T1.xlsb` / `Final_Dataset` | Where to read from |
| `MAX_PLAUSIBLE_SESSION_HOURS` | `12` | Stuck-stream cut-off |
| `BOUNCE_SECONDS` | `60` | Bounce threshold |
| `DROP_EXACT_DUPLICATES` | `False` | Report duplicates vs remove them |
| `EXPORT_RESULTS` / `OUTPUT_DIR` | `True` / `outputs` | Write every table to disk |
| `RANDOM_STATE` | `42` | Reproducible model splits |

---

## 6. Limits declared for this stage

`date_` is **date-only** — no hour component, so day-of-week peaks are provable but "peak hours" are not. There is **no clickstream, no demographics and no device field**. "Churn" here means *30 days of inactivity modelled from behaviour* — not an observed cancellation. Every UX conclusion drawn downstream from this stage is a behavioural proxy and is labelled as such.
