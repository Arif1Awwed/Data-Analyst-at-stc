# stc TV Analytics & Consumer Behavioural Insights

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-2.x-150458?logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.x-F7931E?logo=scikitlearn&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-sparse%20%26%20stats-8CAAE6?logo=scipy&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-interactive-3F4F75?logo=plotly&logoColor=white)
![Colab](https://img.shields.io/badge/Google%20Colab-ready-F9AB00?logo=googlecolab&logoColor=white)
![Decks](https://img.shields.io/badge/Decks-EN%20%2B%20AR-5B1E8C)
![License](https://img.shields.io/badge/Use-Educational%20%2F%20Portfolio-6E6579)

An end-to-end analytics portfolio built on **1,048,575 real viewing events** from the stc TV (Jawwy TV) streaming platform — from raw binary Excel logs through cleaning, diagnostic analytics, predictive modelling and a production-grade recommender, ending in two executive presentation decks in English and Arabic.

---

## 1. Executive Summary

### Problem statement

stc TV holds a large VOD catalogue and a broad subscriber base, but the raw viewing log alone answers none of the questions that actually drive the business: *Who watches what, and for how long? What is quietly killing retention? Which titles should we put in front of which user?*

This project answers those questions across three progressive analytical tasks, then translates the findings into a boardroom-ready strategy.

### The headline finding

> **stc TV does not have a content problem — it has a routing problem.**
>
> Series generate **70.9%** of all watch time but are watched by only **33.7%** of users. A series viewer is worth **52.8 watch hours**; a movie viewer is worth **7.5**. The platform's retention engine already exists — the product simply never routes users to it.

### Business objectives

| # | Objective | Task |
|---|---|---|
| 1 | Establish trustworthy baseline KPIs from a messy, unvalidated log | T1 |
| 2 | Explain *why* engagement metrics look the way they do (diagnostic analytics) | T1 |
| 3 | Predict demand, churn risk and quality preference | T1 |
| 4 | Forecast platform demand for capacity and campaign planning | T2 |
| 5 | Build and validate a personalised recommendation engine | T3 |
| 6 | Convert all of the above into executive strategy in two languages | Decks |

### Dataset description

| Attribute | Value |
|---|---|
| Source | stc TV / Jawwy TV viewing log extract |
| Reporting window | **2017-03-14 → 2018-04-30** (413 days) |
| Raw rows | **1,048,575** viewing events |
| Unique users | **11,578** (anonymised integer IDs) |
| Distinct assets | **11,324** (1,557 movies + 9,616 episodes across 253 shows) |
| Total watch time | **290,861 hours** (12,119 days) |
| Genres | 16 |

**Schema (T1, the master extract):**

| Column | Type | Description |
|---|---|---|
| `user_id_maped` | int64 | Anonymised user identifier |
| `date_` | int64 | Excel serial date (**no time component**) |
| `program_name` | object | Title of the movie or episode |
| `program_class` | object | `MOVIE` or `SERIES` |
| `program_genre` | object | Primary genre |
| `program_desc` | object | Free-text description (1.34% missing) |
| `duration_seconds` | int64 | Length of the viewing event |
| `season`, `episode` | int64 | Series positioning (0 for movies) |
| `hd` | int64 | 1 = HD stream, 0 = SD |
| `series_title`, `original_name` | object | Title metadata |

> [!IMPORTANT]
> **Declared limits of this dataset.** There is **no clickstream** (no screen events, navigation steps or search queries), **no hour-level timestamp** (`date_` is date-only, so only *day-of-week* peaks are provable — never "peak hours"), **no demographics** (age, gender, region), and **no device or app-version field**. "Churn" throughout this project means *30 days of inactivity*, modelled from behaviour — **not** an observed contract cancellation. Every UX conclusion in this repository is reconstructed from behavioural proxies and is labelled as such.

---

## 2. Repository & Folder Structure

```
محلل بيانات في stc/
│
├── README.md                                  ← you are here
│
├── stc TV_T1/                                 ── TASK 1 · Behavioural analytics & prediction
│   ├── stc TV Data Set_T1.xlsb                   Raw binary Excel log (39 MB, sheet: Final_Dataset)
│   ├── stc TV_T1.ipynb                           Main notebook — 35 cells, 9 analytical sections
│   ├── stc_tv_user_behavior_analysis.py          Full pipeline as a script (~1,300 lines)
│   ├── stc_tv_simple_analysis.py                 Lightweight KPI-only variant
│   ├── stc_cleaned_data.csv                      Cleaned + feature-engineered export (255 MB)
│   ├── stc_cleaned_data_sample.csv               1,000-row sample for quick inspection
│   ├── top10_movies.csv                          Top-10 movies by views
│   ├── top10_series.csv                          Top-10 series by views
│   ├── top10_episodes.csv                        Top-10 individual episodes
│   └── outputs/                                  27 numbered analytical deliverables
│       ├── 01_schema.csv          … 03_summary_clean.csv       Data profiling
│       ├── 04_kpi_scorecard.csv   … 06_series_depth.csv        Headline KPIs
│       ├── 07–11_top_*.csv                                     Ranking tables
│       ├── 12_reach_depth_corr.csv … 15_genre_performance.csv  Content diagnostics
│       ├── 16_quality_scorecard.csv … 18_genre_quality.csv     HD vs SD analysis
│       ├── 19_user_profiles.csv   … 22_segment_crosstab.csv    Segmentation
│       ├── 23_demand_forecast.csv                              14-day forecast
│       ├── 24_churn_drivers.csv   … 26_hd_drivers.csv          Model coefficients
│       ├── 27_anomaly_watchlist.csv                            UBA anomaly flags
│       ├── churn_scores.csv                                    Per-user churn probability
│       ├── user_segments.csv                                   Per-user segment assignment
│       └── stc_tv_analysis_report.xlsx                         All tables, one workbook
│
├── stc_TV_T2/                                 ── TASK 2 · Demand forecasting
│   ├── stc_tv_dataset_t2.csv                     411 daily observations (4 columns)
│   ├── stc TV Data Set_T2 - Sheet1.csv            86-day watch-hour extract
│   └── stc_TV_T2.ipynb                           Peak-day analysis + 60-day forecast
│
├── stc TV_T3/                                 ── TASK 3 · Recommendation engine
│   ├── stc TV Data Set_T3.xlsx                   Ratings dataset (36 MB)
│   ├── stc TV_T3.ipynb                           Assignment notebook (TODO cells completed)
│   ├── stc_TV_T3_Recommender.ipynb               Full Colab notebook — 34 cells, EN
│   └── stc_tv_recommendations_sample.csv         Sample engine output for 10 users
│
├── stc_TV_Deck_A_English.pptx                 ── Executive deck · English · 7 slides
└── stc_TV_Deck_B_Arabic.pptx                  ── Executive deck · Arabic (RTL) · 7 slides
```

---

## 3. Task Breakdown

### 🎬 Task 1 — User Behaviour & Viewer Category Analytics

> **Directory:** `stc TV_T1/`  ·  **Notebook:** `stc TV_T1.ipynb`  ·  **Sections:** 9

#### Objective

Turn an unvalidated 1.05M-row viewing log into a trustworthy analytical asset, then answer: how do Movies and Series differ commercially, what drives video-quality choice, which users are about to leave, and what should the platform do about it?

#### Methodology & key steps

**① Data cleaning & preprocessing**

| Step | Treatment |
|---|---|
| Missing values | `program_desc` — 14,038 nulls (1.34%); reconstructed from title metadata where possible |
| **Title corruption repair** | The source export dropped the capital letter **S** from many titles (`treets` → `Streets`, `murfs` → `Smurfs`). A rule-based restorer with a lower-case stop-word guard was validated at **99.3% accuracy (143/144)** against independent ground-truth show names |
| Duplicate log rows | Exact-duplicate events identified and removed |
| Implausible sessions | Plays > **12 hours** treated as stuck streams (device left playing) and excluded from watch-time KPIs — 2,677 rows |
| Bounce flagging | Plays < **60 seconds** flagged as browsing, retained but excluded from depth metrics |

**② Feature engineering** — `watch_minutes`, `watch_hours`, `content_type`, `asset_key`, `is_bounce`, `is_implausible`, `is_weekend`, per-user aggregates (`tenure_days`, `active_days`, `recency_days`, `genres_explored`, `hd_share`, `movie_share`, `views_per_active_day`).

**③ Diagnostic analytics** — headline KPI board, Movies vs Series profiling, reach-vs-depth correlation, genre mix, consumption-over-time, HD/SD split with a **Mann-Whitney U** significance test.

**④ Segmentation** — three independent axes: *quality* (SD-Only → HD-Only), *engagement* (Light → Power), *content* (Movie Lover / Series Binger / Mixed).

**⑤ Predictive modelling**

| Model | Algorithm | Target | Performance |
|---|---|---|---|
| Demand forecast | Linear Regression (trend + day-of-week dummies) | Daily watch hours | **MAPE 10.9%** on a 30-day hold-out · in-sample R² 0.064 |
| Churn risk | Logistic Regression **and** Gradient Boosting | 30-day inactivity | **ROC-AUC 0.878 / 0.888** · accuracy 0.873 |
| HD propensity | Logistic Regression (standardised) | HD vs SD play | **ROC-AUC 0.825** |

**⑥ Anomaly detection (UBA)** — a 4-flag rule set (daily plays above the 99.9th percentile = 154/day, >24h playback in one day, ≥5 stuck sessions, >90% bounce with >100 views). **128 users (1.11%)** raised 2+ flags.

#### Key findings & metrics

**Headline KPIs**

| KPI | Value |
|---|---|
| Total views | 1,048,575 |
| Unique users | 11,578 |
| Total watch time | 290,861 h |
| Views per user | 90.6 |
| Watch hours per user | 25.1 |
| Avg / median session | 16.7 min / **1.9 min** |
| HD share of views | 38.6% |
| **Bounce rate (<60s)** | **27.4%** |

**Movies vs Series — two products in one app**

| Metric | Movies | Series |
|---|---|---|
| Total views | 488,401 | 560,174 |
| **Unique users** | **11,355** | **3,901** |
| Distinct assets | 1,557 | 9,771 |
| Watch hours | 84,772 (29.2%) | **206,089 (70.9%)** |
| Watch hours per user | 7.47 | **52.83** |
| Bounce rate | **38.1%** | 18.1% |
| Median session | 1.28 min | 18.63 min |
| HD share | 67.9% | 13.1% |

**The quality paradox** — HD is a *browsing* signature, not a viewing one:

| Segment | Users | % of users | % of watch time | Avg session | Bounce |
|---|---|---|---|---|---|
| HD-Only | 4,850 | **41.9%** | **1.1%** | 4.5 min | 47.9% |
| HD-Leaning | 2,413 | 20.8% | 7.6% | 9.0 min | 42.2% |
| Balanced | 1,831 | 15.8% | 21.1% | 12.5 min | 42.4% |
| **SD-Leaning** | 1,906 | 16.5% | **69.4%** | 20.4 min | 29.2% |
| SD-Only | 578 | 5.0% | 0.8% | 11.1 min | 45.7% |

**Churn drivers** (standardised coefficients, 11,342 modelled users, 79.1% base churn rate)

| Driver | Coefficient | Direction |
|---|---|---|
| `recency_days` | **+1.497** | 🔺 Raises risk |
| `distinct_assets` | +0.419 | 🔺 Raises risk |
| `avg_minutes` | +0.184 | 🔺 Raises risk |
| `genres_explored` | −0.260 | 🛡️ Protects |
| `total_views` | −0.224 | 🛡️ Protects |
| `active_days` | **−0.691** | 🛡️ Protects |

| Risk band | Users | Actual churn | Watch hours at risk |
|---|---|---|---|
| Low | 930 | 8.8% | 131,223 |
| Medium | 1,264 | 44.2% | 41,413 |
| High | 1,345 | 72.3% | 23,784 |
| **Critical** | **7,803** (68.8%) | **94.3%** | 76,708 |

> [!NOTE]
> **The asymmetry worth acting on:** 930 Low-risk users hold **131,223 hours** — more than the 7,803 Critical users put at risk (76,708 h). Defending the core is worth more than rescuing the tail, and costs far less.

**Content concentration (long tail)**

- Top **1%** of the catalogue (80 titles) → **28.7%** of all views
- Top **5%** (400 titles) → 51.8% · Top **20%** (1,602 titles) → 78.1%
- Only **1,762 titles (22%)** generate 80% of views
- **1,496 titles (18.7%)** received fewer than 10 views in 413 days

**Genre economics** — Animation dominates volume (401,730 views) but Drama Series converts time best (31.26 avg min). *Friends* alone drove **12,841 hours from just 718 viewers**.

**Demand trend** — watch time fell **38.5% year over year** (Apr-17: 28,814 h → Apr-18: 17,733 h), with movies down **58.5%** and series down 27.7%.

#### Deliverables

`outputs/01`–`27_*.csv` · `churn_scores.csv` · `user_segments.csv` · `stc_tv_analysis_report.xlsx` · `top10_{movies,series,episodes}.csv` · `stc_cleaned_data.csv` · Matplotlib + Plotly figures embedded in the notebook.

---

### 📈 Task 2 — Peak Viewing Days & 60-Day Demand Forecast

> **Directory:** `stc_TV_T2/`  ·  **Notebook:** `stc_TV_T2.ipynb`

#### Objective

Identify the platform's peak viewing day and forecast total views for the next 60 days to support capacity planning and campaign scheduling.

#### Methodology & key steps

1. Load the aggregated daily series (411 observations × 4 columns: `date_`, `daily_views`, `daily_watch_hours`, `unique_users`).
2. Derive `day_of_week` and compute average daily views per weekday.
3. Identify the peak day with `idxmax()`.
4. **Forecast approach — deliberately simple and explainable:** restrict history to the **last 12 weeks** (84 days) because volume trends downward over the period, compute a weekday mean within that window, and project it forward 60 days.
5. Visualise: weekday bar chart (peak highlighted) and a history-vs-forecast line chart.

> [!TIP]
> Restricting to a 12-week window is the analytically important decision here. Using the full 411-day history would have inflated the forecast by anchoring on 2017 volumes that the platform no longer achieves.

#### Key findings & metrics

**Average daily views by weekday (full period vs last 12 weeks)**

| Day | Full period | Last 12 weeks |
|---|---|---|
| **Saturday** | **2,770** 🥇 | **2,975** 🥇 |
| **Friday** | **2,696** 🥈 | **2,795** 🥈 |
| Monday | 2,540 | 2,529 |
| Tuesday | 2,523 | 2,424 |
| Wednesday | 2,475 | 2,359 |
| Thursday | 2,461 | 2,446 |
| Sunday | 2,396 | 2,389 |

- **Peak day: Saturday** — consistent with the Friday–Saturday Saudi weekend during this period.
- Weekend uplift: Saturday runs **+24.6%** above the Wednesday trough in recent data.

**60-day forecast (2018-05-01 → 2018-06-29)**

| Period | Expected views |
|---|---|
| Month 1 | 76,451 |
| Month 2 | 76,909 |
| **60-day total** | **153,360** |

*T1 cross-check:* an independent Linear Regression with trend + day-of-week features projected **8,729 watch hours over 14 days (≈624 h/day)** at **MAPE 10.9%** on hold-out — the two forecasts are mutually consistent.

#### Deliverables

`stc_TV_T2.ipynb` (Colab-ready) · `stc_tv_dataset_t2.csv` · weekday bar chart · history-vs-forecast line chart · bilingual summary block.

---

### 🎯 Task 3 — Collaborative Filtering Recommendation Engine

> **Directory:** `stc TV_T3/`  ·  **Notebooks:** `stc_TV_T3_Recommender.ipynb` (full, 34 cells) · `stc TV_T3.ipynb` (assignment)

#### Objective

Build a recommender that suggests programmes to a user based on the viewing behaviour of users who share their taste — then produce the **top 5 recommendations for people who watched *Moana***.

#### Methodology & key steps

**① Interaction matrix construction**

The raw file holds **one row per viewing event**, so a user appears many times for the same title. Events were aggregated into one row per `(user, program)` pair carrying `watch_count` and `avg_rating`.

**② Cold-start filtering** — users and programmes with fewer than 5 interactions were removed:

| | Before | After |
|---|---|---|
| Users | 11,578 | **6,700** |
| Programmes | 8,013 | **6,927** |
| Interactions | 440,237 | **428,022** |
| Matrix density | — | **0.92%** |

**③ Two models trained**

- **User-Based CF** — cosine similarity between user vectors, top-**50** nearest neighbours retained, programme score = sum of neighbour similarities.
- **Item-Based CF** — cosine similarity between programme vectors ("watched X → also watched Y").

**④ Evaluation** — 20% of each user's history held out; **Precision@5** and **Recall@5** measured against a **popularity baseline**.

#### Key findings & metrics

**Model performance**

| Model | Precision@5 | Recall@5 | Lift vs baseline |
|---|---|---|---|
| Popularity (baseline) | 0.0858 | 0.1191 | 1.00× |
| User-Based CF (k=50) | 0.2585 | 0.2385 | **3.01×** |
| **Item-Based CF** | **0.2756** | **0.2482** | **3.21×** |
| SVD (k=50, tested) | 0.2467 | 0.2118 | 2.88× |

> Matrix factorisation (TruncatedSVD) was evaluated at k = 50 / 100 / 200 and consistently **underperformed** neighbourhood methods on this sparse, implicit-feedback matrix — so it was excluded from the final notebook rather than included for show.

**🎯 Top 5 recommendations for viewers of *Moana*** (1,817 Moana watchers)

| # | Programme | Genre | Cosine similarity |
|---|---|---|---|
| 1 | Trolls | Animation | 0.6386 |
| 2 | Surf's Up: WaveMania | Animation | 0.6048 |
| 3 | The Mermaid Princess | Animation | 0.5585 |
| 4 | The Jetsons & WWE: Robo-WrestleMania! | Animation | 0.5180 |
| 5 | The Boss Baby | Animation | 0.5105 |

All five are Animation titles — a coherent result for a family/kids audience, produced by an engine that was **never told what a genre is**.

**The cold-start problem, quantified**

Precision degrades sharply with shorter user history — the single most important caveat for deployment:

| User history (titles) | Users | Precision@5 |
|---|---|---|
| 3 – 5 | 944 | **0.079** ⚠️ *worse than popularity* |
| 6 – 10 | 1,431 | 0.099 |
| 11 – 30 | 1,865 | 0.195 |
| 31 – 100 | 1,502 | 0.413 |
| 101+ | 958 | **0.673** |

**46.7%** of all users have ≤5 titles of history, and **18.3%** have exactly one. Collaborative filtering is effectively useless for them — which is why an onboarding taste picker is a hard prerequisite, not a nice-to-have.

**Sample output** — the engine independently learned episode continuity within series:

```text
user  51 (94 titles)  → Vikings: Scarred | The Lord's Prayer | Warrior's Fate | Boneless | Blood Eagle
user 183 (110 titles) → Friends: The One After The Superbowl II | The One With The Prom Video | ...
user 259 (35 titles)  → Blaze And The Monster Machines: Blaze Of Glory | Stuntmania! | Epic Fail | ...
user 205 (125 titles) → The Smurfs | Howard Lovecraft | The Little Vampire | Alvin and the Chipmunks | Cars
```

#### Deliverables

`stc_TV_T3_Recommender.ipynb` (34 cells, fully executed end-to-end) · `stc TV_T3.ipynb` (assignment TODOs completed) · `stc_tv_recommendations_sample.csv` · reusable functions `recommend_user_based()`, `recommend_item_based()`, `similar_programs()`.

---

## 4. Presentation Decks

Two **independent** 7-slide executive decks, generated programmatically with `python-pptx` (16:9, native editable charts, full speaker notes on every slide).

| File | Language | Direction | Slides |
|---|---|---|---|
| `stc_TV_Deck_A_English.pptx` | English | LTR | 7 |
| `stc_TV_Deck_B_Arabic.pptx` | Arabic (فصحى مهنية) | **RTL** — 190/190 paragraphs bidi-marked | 7 |

### Slide architecture

| # | Slide | Visual asset |
|---|---|---|
| 1 | **The Retention Engine We Already Own** | Dark title slide · 14-month watch-hour line chart · 4 KPI tiles |
| 2 | **Method: Three Datasets, One User Story** | T1/T2/T3 provenance cards · *Declared Limits* callout box |
| 3 | **Two Products Wearing One App** | Movies-vs-Series clustered column chart · weekday seasonality chart |
| 4 | **Where Discovery Breaks Down** | Catalogue-concentration chart · 4 alert tiles · proxy-derived badge |
| 5 | **Churn Is a Recency Problem** | Tornado chart of standardised coefficients · risk-band table |
| 6 | **Seven Moves, Ranked by Evidence** | Recommendation table with Impact/Effort pills |
| 7 | **Roadmap, Priorities and the Numbers We Own** | 3×3 Impact-vs-Effort matrix · 3-phase timeline · KPI scorecard |

### From analysis to executive insight

The decks deliberately **do not** restate the notebooks. Three translation moves were applied:

1. **Metric → narrative.** "Series bounce = 18.1% vs movies 38.1%" becomes *"we already own the retention engine, we just never route users to it."*
2. **Coefficient → brief.** `recency_days = +1.497` becomes *"churn is driven by absence, not dissatisfaction"* — which turns an abstract model output into a shippable product requirement.
3. **Limitation → ask.** Rather than hiding the missing clickstream, Slide 2 declares it and Slide 7 converts it into the roadmap's highest-leverage Phase 1 item: **event instrumentation**.

> [!WARNING]
> Every UX friction figure in both decks is derived from behavioural proxies (<60s abandonment, catalogue concentration, movie-to-series conversion) and is labelled *proxy-derived* on the slide itself. No UI event data exists in this dataset, and the decks do not pretend otherwise.

---

## 5. Tech Stack & Dependencies

### Languages & platforms

| Category | Tools |
|---|---|
| Language | **Python 3.10+** |
| Notebooks | Jupyter · **Google Colab** (all notebooks are Colab-ready) |
| Presentation | Microsoft PowerPoint (`.pptx`, generated via `python-pptx`) |
| Formats | `.xlsb` (binary Excel) · `.xlsx` · `.csv` · `.parquet` (optional cache) |

### Python libraries

| Purpose | Library |
|---|---|
| Data manipulation | `pandas`, `numpy` |
| Excel I/O | `pyxlsb` (T1 binary), `openpyxl` (T3) |
| Machine learning | `scikit-learn` — `LinearRegression`, `LogisticRegression`, `GradientBoostingClassifier`, `TruncatedSVD`, `StandardScaler`, `train_test_split` |
| Sparse linear algebra | `scipy.sparse` (`csr_matrix`), `sklearn.preprocessing.normalize` |
| Statistics | `scipy.stats` — Mann-Whitney U significance testing |
| Visualisation | `matplotlib`, `plotly` (`express`, `graph_objects`, `subplots`) |
| Deck generation | `python-pptx` |

### Modelling techniques

`Collaborative Filtering (user-based & item-based)` · `Cosine Similarity` · `Matrix Factorisation (TruncatedSVD)` · `Logistic Regression` · `Gradient Boosting` · `Linear Regression with seasonal dummies` · `Rule-based anomaly detection (UBA)` · `Behavioural segmentation` · `Precision@K / Recall@K evaluation`

### Install

```bash
pip install pandas numpy scikit-learn scipy matplotlib plotly pyxlsb openpyxl python-pptx jupyter
```

---

## 6. Key Business Recommendations

Seven prioritised, evidence-backed moves. Each cites the specific finding that produced it.

| # | Recommendation | Evidence | Impact | Effort |
|---|---|---|---|---|
| **1** | **Series-first home rail** — put *Continue Watching* above the fold and surface episode continuity | Series retain **7×** the hours per user (52.8 vs 7.5) | 🔴 High | 🟢 Low |
| **2** | **Cold-start taste picker at signup** — a 30-second genre/title selector | **46.7%** of users have ≤5 titles; CF precision collapses to **0.079** there | 🔴 High | 🟢 Low |
| **3** | **Ship the Item-Based CF recommender** | **P@5 0.276** vs 0.086 popularity — **3.21× lift**, already validated on hold-out | 🔴 High | 🟠 Medium |
| **4** | **Recency-triggered win-back automation** — act on silence, not on sentiment | `recency_days` is the dominant churn coefficient (**+1.497**) | 🔴 High | 🟢 Low |
| **5** | **Rebuild the first 60 seconds** — instant preview, faster playback start | **27.4%** overall bounce, rising to **38.1%** on movies; median movie session **1.3 min** | 🔴 High | 🟠 Medium |
| **6** | **Long-tail discovery rails** — actively surface the catalogue outside the head | **6,251 titles** sit outside the top 22%; 1,496 got <10 views in 413 days | 🟠 Medium | 🟠 Medium |
| **7** | **Adaptive quality default** — stop defaulting the retention path to HD | Series are **86.9% SD**; HD-only users are 41.9% of the base but 1.1% of watch time | 🟠 Medium | 🔴 High |

### Impact vs effort

| | Low effort | Medium effort | High effort |
|---|---|---|---|
| **High impact** | ✅ **1** Series rail · ✅ **2** Taste picker · ✅ **4** Win-back | **3** CF recommender · **5** First 60 seconds | — |
| **Medium impact** | — | **6** Long-tail rails | **7** Adaptive quality |
| **Low impact** | — | — | — |

> [!IMPORTANT]
> **Recommendations 2 and 3 must ship together.** Launching the recommender without a cold-start solution under-delivers for the 46.7% of users whose history is too thin for collaborative filtering to work at all.

### Execution roadmap

| Phase | Window | Scope |
|---|---|---|
| **Phase 1** | 0–3 months | Taste picker · Continue Watching rail · win-back triggers · **event instrumentation** |
| **Phase 2** | 3–6 months | Recommender in production · first-60-seconds rebuild · long-tail rails |
| **Phase 3** | 6–12 months | Adaptive quality · segment-specific home screens · retrain on real clickstream |

### KPI scorecard

| Metric | Baseline (measured) | 12-month target | Source |
|---|---|---|---|
| Sessions abandoned <60s | 27.4% | 20.0% | T1 · `04_kpi_scorecard` |
| Users who start a series | 33.7% | 45.0% | T1 · `05_class_scorecard` |
| Watch hours per user | 25.1 | 30.0 | T1 · `04_kpi_scorecard` |
| Users in Critical risk band | 68.8% | 50.0% | T1 · `25_churn_risk_bands` |
| Recommender Precision@5 | 0.276 | 0.350 | T3 · hold-out evaluation |
| Catalogue driving 80% of views | 22.0% | 35.0% | T1 · concentration analysis |
| **Event instrumentation coverage** | **0%** | **100%** | ⚠️ Gap — not currently collected |

---

## 7. Setup & Execution Guide

### Prerequisites

| Requirement | Minimum |
|---|---|
| Python | 3.10+ |
| RAM | **8 GB** (T1 handles 1.05M rows; T3 builds a 6,927² dense similarity matrix ≈ 190 MB) |
| Disk | ~700 MB free (raw files + cleaned exports) |
| Optional | Google Colab account — all notebooks run there without local setup |

### Option A — Local environment

```bash
# 1 · Clone / open the project
cd "محلل بيانات في stc"

# 2 · Create an isolated environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 3 · Install dependencies
pip install pandas numpy scikit-learn scipy matplotlib plotly \
            pyxlsb openpyxl python-pptx jupyter

# 4 · Launch
jupyter notebook
```

### Option B — Google Colab

1. Upload the notebook and its dataset to Colab, **or** mount Google Drive:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   FILE_PATH = '/content/drive/MyDrive/stc TV Data Set_T3.xlsx'
   ```
2. Each notebook's first cell installs any missing dependency (`pyxlsb`) automatically.

### Execution order

> [!NOTE]
> The three tasks are **independent** — each reads its own dataset and can be run in isolation. The order below is the intended narrative sequence.

| Step | Run | Duration | Produces |
|---|---|---|---|
| **1** | `stc TV_T1/stc TV_T1.ipynb` | ~8–12 min | `outputs/` (27 CSVs + Excel report), `stc_cleaned_data.csv`, top-10 tables |
| **2** | `stc_TV_T2/stc_TV_T2.ipynb` | <1 min | Weekday chart, 60-day forecast |
| **3** | `stc TV_T3/stc_TV_T3_Recommender.ipynb` | ~5 min | `stc_tv_recommendations_sample.csv`, Moana top-5 |
| **4** | Open both `.pptx` decks | — | Executive presentation (use *Presenter View* for speaker notes) |

**Alternative for Task 1** — run the pipeline headlessly:

```bash
cd "stc TV_T1"
python stc_tv_user_behavior_analysis.py    # full pipeline, ~1,300 lines
python stc_tv_simple_analysis.py           # lightweight KPI-only variant
```

### Performance tips

```python
# T3: the 36 MB .xlsx takes ~53 s to parse. Cache it once as Parquet:
dataframe.to_parquet("t3.parquet")
dataframe = pd.read_parquet("t3.parquet")   # subsequent runs: <1 s
```

- **T1 config switches** live in the `CONFIG` dict at the top of the notebook: `DATA_PATH`, `SHEET_NAME` (`Final_Dataset`), `MAX_PLAUSIBLE_SESSION_HOURS` (12), `BOUNCE_SECONDS` (60), `RANDOM_STATE`.
- **T3 filtering threshold** is `MIN_INTERACTIONS = 5`; lowering it increases coverage but degrades precision — see the cold-start table above.

### Troubleshooting

| Error | Fix |
|---|---|
| `FileNotFoundError: stc- Jawwy TV Data Set_T3.xlsb` | The file is `stc TV Data Set_T3.xlsx` (`.xlsx`, not `.xlsb`) — check the exact filename |
| `Missing optional dependency 'pyxlsb'` | `pip install pyxlsb` — required only for the T1 `.xlsb` file |
| `MemoryError` in T3 | Raise `MIN_INTERACTIONS` to 10, or run on Colab |

---

## Author

**Arif** — Data Analyst · stc TV Analytics Project

> [!NOTE]
> This is an independent analytical work product built on an educational dataset extract. It is not an official stc communication, and all user identifiers in the source data are anonymised.
