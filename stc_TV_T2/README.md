# Task 2 — Peak Viewing Days & 60-Day Demand Forecast
### أيام الذروة والتنبؤ بالطلب لمدة 60 يومًا

> Stage 2 of 3 · Input: a 411-day daily series · Output: the platform's peak day + a 60-day view forecast
> Project overview: [../README.md](../README.md)

---

## 1. What this stage is for

Two questions, both operational:

1. **Which day of the week does the platform peak?** — capacity planning and campaign scheduling depend on it.
2. **How many views should we expect over the next 60 days?**

Task 1 answered *what happened and why*. This stage answers *what happens next*, and it is deliberately the simplest notebook in the project: a forecast an operations team can re-derive by hand is a forecast they will actually use.

---

## 2. What we did, step by step

| Step | What we did | Why |
|---|---|---|
| **1a–1b** | Loaded `stc_tv_dataset_t2.csv` — 411 daily rows × 4 columns | One row per day, already aggregated from the T1 event log |
| **1c** | Converted `date_` to real datetimes and printed the range: **2017-03-14 → 2018-04-30** | Guards against silent string-sorting of dates |
| **2a** | Derived `day_of_week` and took the mean of `daily_views` per weekday, reindexed **Saturday-first** | Saudi week order, not the pandas default |
| **2b** | Found the peak with `idxmax()` | **Saturday** |
| **3a** | **The key decision:** restricted the forecast history to the **last 12 weeks (84 days)** and recomputed the weekday means inside that window | Volume trends downward across the period — using all 411 days would anchor the forecast on 2017 levels the platform no longer reaches |
| **3b** | Generated the next 60 dates and mapped each one to its recent weekday average | A seasonal-naïve forecast: explainable, no black box |
| **3c** | Summed month 1, month 2 and the 60-day total | The number capacity planning needs |
| **4a** | Weekday bar chart with the peak highlighted in stc magenta | |
| **4b** | History-vs-forecast line chart | Shows the forecast sitting in the recent level, not the historical one |
| **Summary** | Bilingual (EN / عربي) findings and recommendations block | Matches the audience of the decks |

---

## 3. Files in this folder

| File | What it is | How it was produced |
|---|---|---|
| [stc_TV_T2.ipynb](stc_TV_T2.ipynb) | **The deliverable.** 22 cells (10 code), fully executed, Colab-ready — load → weekday profile → peak day → 60-day forecast → 2 charts → bilingual summary | Written for this stage |
| [stc_tv_dataset_t2.csv](stc_tv_dataset_t2.csv) | The working dataset: **411 rows** × `date_`, `daily_views`, `daily_watch_hours`, `unique_users` — the full daily series | Aggregated from the cleaned T1 log ([../stc TV_T1/](../stc%20TV_T1/)) |
| [stc TV Data Set_T2 - Sheet1.csv](stc%20TV%20Data%20Set_T2%20-%20Sheet1.csv) | The **provided** T2 extract: 85 rows, `date_` + `Total_watch_time_in_houres`, Jan–Mar 2018 only | Source extract — kept unmodified as a cross-check reference |

> **Why two datasets?** The provided extract carries watch *hours* for a 3-month window only. Rebuilding the daily series from the T1 event log gives 411 days and adds `daily_views` and `unique_users` — enough history to measure weekday seasonality and enough columns to forecast views. The provided file stays in place so the numbers can be traced back to source.

---

## 4. Key findings from this stage

**Average daily views by weekday**

| Day | Full period | Last 12 weeks |
|---|---|---|
| **Saturday** | **2,770** 🥇 | **2,975** 🥇 |
| **Friday** | **2,696** 🥈 | **2,795** 🥈 |
| Monday | 2,540 | 2,529 |
| Tuesday | 2,523 | 2,424 |
| Wednesday | 2,475 | 2,359 |
| Thursday | 2,461 | 2,446 |
| Sunday | 2,396 | 2,389 |

- **Peak day: Saturday** — consistent with the Friday–Saturday Saudi weekend during this period, and stable across both windows.
- Saturday runs **+24.6%** above the Wednesday trough in recent data.

**60-day forecast (2018-05-01 → 2018-06-29)**

| Period | Expected views |
|---|---|
| Month 1 | 76,451 |
| Month 2 | 76,909 |
| **60-day total** | **153,360** |

**Cross-check against Task 1:** an independent Linear Regression (trend + day-of-week dummies) in T1 §7 projected **≈624 watch hours/day** at **MAPE 10.9%** on hold-out. Two different methods, mutually consistent — which is the point of running both.

---

## 5. How to re-run this stage

```bash
jupyter notebook stc_TV_T2.ipynb    # <1 minute, pandas + matplotlib only
```

No modelling libraries are needed. To change the forecast window, edit one line in Step 3a:

```python
recent = data[data["date_"] > last_date - pd.Timedelta(days=84)]   # 84 = 12 weeks
```

---

## 6. Limits declared for this stage

The source `date_` is **date-only**, so this stage can prove *day-of-week* seasonality and nothing about hours of the day — "peak hours" is not a claim this data supports. The forecast is **seasonal-naïve**: it carries recent weekday levels forward and assumes no campaign, catalogue or pricing shock. It is a capacity-planning baseline, not a growth projection — the underlying trend over the 413-day window is **−38.5% year over year**, and the forecast reflects the recent level rather than trying to extrapolate that decline.
