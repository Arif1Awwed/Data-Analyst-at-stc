# Task 3 — Collaborative Filtering Recommendation Engine
### محرك التوصيات بالترشيح التعاوني

> Stage 3 of 3 · Input: `stc TV Data Set_T3.xlsx` (viewing events with ratings) · Output: two trained CF models + a validated top-5 for *Moana*
> Project overview: [../README.md](../README.md)

---

## 1. What this stage is for

Build a recommender that suggests programmes to a user based on the behaviour of users who share their taste, then answer the assignment question: **what are the top 5 recommendations for people who watched *Moana*?**

The bar we set: the engine has to **beat a popularity baseline on held-out data**. Anything that only looks plausible in a demo does not ship.

---

## 2. What we did, step by step

### ① Interaction matrix (§3)

The raw file holds **one row per viewing event**, so a single user appears many times against the same title. We aggregated events into one row per `(user, program)` pair carrying `watch_count` and `avg_rating`, then built a **sparse** `csr_matrix` — a dense 11,578 × 8,013 matrix would be wasteful at 0.9% density.

### ② Cold-start filtering (§3)

Users and programmes with fewer than **5 interactions** were dropped, because a similarity computed from 1–2 data points is noise:

| | Before | After |
|---|---|---|
| Users | 11,578 | **6,700** |
| Programmes | 8,013 | **6,927** |
| Interactions | 440,237 | **428,022** |
| Density | — | **0.92%** |

### ③ Two models trained (§4–5)

- **User-Based CF** — cosine similarity between user vectors, top **k = 50** nearest neighbours retained; a programme's score is the sum of the similarities of neighbours who watched it.
- **Item-Based CF** — cosine similarity between programme vectors: *"users who watched X also watched Y"*.

### ④ Evaluation (§6)

20% of each user's history held out, then **Precision@5** and **Recall@5** measured against a **popularity baseline** — the honest comparison, since recommending the five most-watched titles to everyone is what a platform gets for free.

We also tested **TruncatedSVD** at k = 50 / 100 / 200. It consistently **underperformed** the neighbourhood methods on this sparse implicit-feedback matrix, so it was **excluded from the final notebook** rather than kept in for show.

### ⑤ The Moana answer (§7)

Two readings of the question, both produced: (a) titles most similar to *Moana* itself, and (b) the aggregate top 5 across all **1,817** users who watched it, with *Moana* itself masked out of its own recommendations.

### ⑥ Sample output & conclusion (§8–9)

Recommendations generated for a sample of users and exported, plus the cold-start analysis that qualifies the whole result.

---

## 3. Files in this folder

| File | What it is | How it was produced |
|---|---|---|
| [stc_TV_T3_Recommender.ipynb](stc_TV_T3_Recommender.ipynb) | **The main deliverable.** 34 cells across 9 sections, fully executed end to end — matrix build, both models, hold-out evaluation, Moana answer, cold-start analysis. Exposes the reusable functions `recommend_user_based()`, `recommend_item_based()` and `similar_programs()` | Written for this stage |
| [stc TV_T3.ipynb](stc%20TV_T3.ipynb) | The **assignment notebook** as supplied, with every `TODO` completed in place — the graded artefact, kept separate so the provided scaffolding stays recognisable | Provided template + our implementation |
| [stc TV Data Set_T3.xlsx](stc%20TV%20Data%20Set_T3.xlsx) | Raw source data (36 MB `.xlsx`, **not** `.xlsb` despite the assignment text) — viewing events with `user_id_maped`, `program_name` and `rating` | Provided extract — never modified |
| [stc_tv_recommendations_sample.csv](stc_tv_recommendations_sample.csv) | 10 sample users with their history size and their top-5 recommendations, as a readable audit of what the engine actually returns | §8 of the recommender notebook |

---

## 4. Key findings from this stage

**Model performance (hold-out)**

| Model | Precision@5 | Recall@5 | Lift vs baseline |
|---|---|---|---|
| Popularity (baseline) | 0.0858 | 0.1191 | 1.00× |
| User-Based CF (k=50) | 0.2585 | 0.2385 | 3.01× |
| **Item-Based CF** | **0.2756** | **0.2482** | **3.21×** |
| SVD (k=50, tested) | 0.2467 | 0.2118 | 2.88× |

**🎯 Top 5 for viewers of *Moana*** (1,817 watchers)

| # | Programme | Genre | Cosine similarity |
|---|---|---|---|
| 1 | Trolls | Animation | 0.6386 |
| 2 | Surf's Up: WaveMania | Animation | 0.6048 |
| 3 | The Mermaid Princess | Animation | 0.5585 |
| 4 | The Jetsons & WWE: Robo-WrestleMania! | Animation | 0.5180 |
| 5 | The Boss Baby | Animation | 0.5105 |

All five are Animation titles — a coherent family/kids result from an engine that was **never told what a genre is**. It also learned episode continuity inside series without being told what an episode is: a *Vikings* viewer gets the next *Vikings* episodes, a *Friends* viewer gets the next *Friends* episodes.

**The cold-start problem, quantified** — the single most important caveat for deployment:

| User history (titles) | Users | Precision@5 |
|---|---|---|
| 3 – 5 | 944 | **0.079** ⚠️ *worse than popularity* |
| 6 – 10 | 1,431 | 0.099 |
| 11 – 30 | 1,865 | 0.195 |
| 31 – 100 | 1,502 | 0.413 |
| 101+ | 958 | **0.673** |

**46.7%** of all users have ≤5 titles of history and **18.3%** have exactly one. Collaborative filtering is effectively useless for them — which is why an onboarding taste picker is a hard prerequisite for shipping this, not a nice-to-have.

---
