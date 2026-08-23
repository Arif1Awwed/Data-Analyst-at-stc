"""stc tv - user viewing behaviour analysis (simple version).

Reads the raw viewing log, cleans it, and reports engagement KPIs,
Movies vs Series performance, Top-10 rankings and HD vs SD preferences.
"""

import re

import matplotlib.pyplot as plt
import pandas as pd

DATA_FILE = "stc TV Data Set_T1.xlsb"
SHEET_NAME = "Final_Dataset"
TOP_N = 10
MAX_SESSION_HOURS = 12          # longer plays are stuck streams, not real viewing
BOUNCE_SECONDS = 60             # shorter plays are browsing, not viewing

# Words that are genuinely lower-case in a title, so they must not be "repaired".
LOWERCASE_WORDS = {"a", "an", "and", "the", "of", "in", "on", "at", "to", "for",
                   "with", "from", "by", "or", "vs", "de", "la", "le", "el", "al"}


# ---------------------------------------------------------------- loading

def load_data():
    """Read the raw viewing log from the binary Excel file."""
    print(f"Loading {DATA_FILE} ...")
    data = pd.read_excel(DATA_FILE, sheet_name=SHEET_NAME, engine="pyxlsb")
    print(f"Loaded {len(data):,} rows and {data.shape[1]} columns.\n")
    return data


# ---------------------------------------------------------------- cleaning

def restore_dropped_s(name):
    """Put back the capital 'S' the source export dropped from titles.

    These titles are Title-Cased, so a lower-case word that is not a small
    linking word means the leading capital was lost: "treets" -> "Streets".
    """
    if not isinstance(name, str):
        return name

    words = []
    for word in name.split(" "):
        if word.startswith(".") and len(word) > 1 and word[1].isupper():
            words.append("S" + word)          # ".H.I.E.L.D." -> "S.H.I.E.L.D."
        elif re.match(r"^[a-z][A-Z]", word):
            words.append(word)                # "iCarly" is spelled correctly
        elif word.lower() in LOWERCASE_WORDS:
            words.append(word)
        elif re.match(r"^[a-z]", word):
            words.append("S" + word)
        else:
            words.append(word)
    return " ".join(words)


def repair_titles(titles):
    """Apply the title repair once per distinct title, then map it back."""
    repairs = {title: restore_dropped_s(title) for title in titles.dropna().unique()}
    return titles.map(repairs).fillna(titles)


def title_from_description(description):
    """Pull the correctly spelled title out of the program description."""
    if not isinstance(description, str) or not description.strip():
        return None
    title = re.sub(r"^.*?(?:Movie|Series|Episode)", "", description, count=1)
    title = re.sub(r"\s*\((?:HD|SD)\)\s*$", "", title.strip())
    return title.strip() or None


def clean_data(raw):
    """Clean the raw log and add the columns the analysis needs."""
    data = raw.copy()

    text_columns = data.select_dtypes(include="object").columns
    for column in text_columns:
        data[column] = data[column].str.replace(r"\s+", " ", regex=True).str.strip()

    data["date"] = pd.to_datetime(data["date_"], unit="D", origin="1899-12-30")
    data["month"] = data["date"].dt.to_period("M").dt.to_timestamp()
    data["watch_minutes"] = data["duration_seconds"] / 60
    data["watch_hours"] = data["duration_seconds"] / 3600

    data["content_type"] = data["program_class"].str.startswith("MOVIE")
    data["content_type"] = data["content_type"].map({True: "Movie", False: "Series"})
    data["quality"] = data["hd"].map({1: "HD", 0: "SD"})
    data["program_genre"] = data["program_genre"].replace(
        {"NOT_DEFINED_IN_UMS": "Undefined", "SERIES_NOT_ADDED_UNDER_ANY_GENRE": "Undefined"})

    # For a series, original_name is the show; program_name also holds the episode title.
    show = data["original_name"].str.replace(r"\s*\(T\)\s*$", "", regex=True).str.strip()
    data["show_name"] = repair_titles(show)

    # For a movie, the clean spelling survives in the description.
    from_description = data["program_desc"].map(title_from_description)
    data["movie_title"] = from_description.fillna(repair_titles(data["program_name"]))

    # An episode is only a distinct episode when it carries an episode number.
    is_episode = data["content_type"].eq("Series") & data["episode"].gt(0)
    data["episode_name"] = (data["show_name"]
                            + " S" + data["season"].astype(str).str.zfill(2)
                            + "E" + data["episode"].astype(str).str.zfill(2)).where(is_episode)

    data["is_hd"] = data["quality"].eq("HD")
    data["is_bounce"] = data["duration_seconds"] < BOUNCE_SECONDS
    data["is_valid_session"] = data["watch_hours"] <= MAX_SESSION_HOURS

    print(f"Cleaned {len(data):,} rows.")
    print(f"Date range: {data['date'].min():%Y-%m-%d} to {data['date'].max():%Y-%m-%d}")
    print(f"Stuck sessions over {MAX_SESSION_HOURS}h excluded from watch time: "
          f"{(~data['is_valid_session']).sum():,}\n")
    return data


# ---------------------------------------------------------------- analysis

def show_key_numbers(data):
    """Print the headline engagement KPIs."""
    valid = data[data["is_valid_session"]]

    print("KEY NUMBERS")
    print(f"  Total views            : {len(data):,}")
    print(f"  Unique users           : {data['user_id_maped'].nunique():,}")
    print(f"  Total watch hours      : {valid['watch_hours'].sum():,.0f}")
    print(f"  Views per user         : {len(data) / data['user_id_maped'].nunique():,.1f}")
    print(f"  Average session minutes: {valid['watch_minutes'].mean():,.1f}")
    print(f"  Median session minutes : {valid['watch_minutes'].median():,.1f}")
    print(f"  HD share of views      : {data['quality'].eq('HD').mean() * 100:,.1f}%")
    print(f"  Bounce rate (under 60s): {data['is_bounce'].mean() * 100:,.1f}%\n")


def summarise_numbers(data):
    """Mean, standard deviation, minimum and maximum of the numeric columns."""
    columns = ["duration_seconds", "watch_minutes", "season", "episode", "hd"]
    summary = pd.DataFrame({
        "mean": data[columns].mean(),
        "std": data[columns].std(),
        "min": data[columns].min(),
        "max": data[columns].max(),
    })
    print("NUMERIC SUMMARY")
    print(summary.round(2), "\n")
    return summary


def build_metrics(data, group_column):
    """Total views, unique users and watch hours for each group."""
    valid = data[data["is_valid_session"]]
    metrics = pd.DataFrame({
        "total_views": data.groupby(group_column).size(),
        "unique_users": data.groupby(group_column)["user_id_maped"].nunique(),
        "watch_hours": valid.groupby(group_column)["watch_hours"].sum().round(0),
    })
    metrics["avg_minutes"] = valid.groupby(group_column)["watch_minutes"].mean().round(1)
    metrics["hd_share_pct"] = (data.groupby(group_column)["is_hd"].mean() * 100).round(1)
    return metrics.fillna(0)


def compare_program_class(data):
    """Compare Movies against Series."""
    metrics = build_metrics(data, "content_type")
    metrics["share_of_views_pct"] = (metrics["total_views"] / len(data) * 100).round(1)
    print("MOVIES VS SERIES")
    print(metrics, "\n")
    return metrics


def compare_quality(data):
    """Compare HD against SD viewing."""
    metrics = build_metrics(data, "quality").drop(columns="hd_share_pct")
    print("HD VS SD")
    print(metrics, "\n")
    return metrics


def rank_top(data, name_column, label):
    """Rank the most watched titles by number of views."""
    ranked = build_metrics(data.dropna(subset=[name_column]), name_column)
    ranked = ranked.sort_values("total_views", ascending=False).head(TOP_N)
    ranked.index.name = label
    print(f"TOP {TOP_N} {label.upper()}")
    print(ranked, "\n")
    return ranked


def summarise_genres(data):
    """Rank genres by number of views."""
    genres = build_metrics(data, "program_genre").sort_values("total_views", ascending=False)
    print("GENRE PERFORMANCE")
    print(genres.head(TOP_N), "\n")
    return genres


def monthly_trend(data):
    """Watch hours and active users per month."""
    valid = data[data["is_valid_session"]]
    trend = pd.DataFrame({
        "watch_hours": valid.groupby("month")["watch_hours"].sum().round(0),
        "active_users": data.groupby("month")["user_id_maped"].nunique(),
    })
    print("MONTHLY TREND")
    print(trend, "\n")
    return trend


# ---------------------------------------------------------------- charts

def plot_program_class(metrics):
    figure, axes = plt.subplots(1, 2, figsize=(11, 4))
    metrics["total_views"].plot(kind="bar", ax=axes[0], color=["#4F008C", "#E5007D"])
    axes[0].set_title("Total views by program class")
    axes[0].set_ylabel("Views")
    metrics["watch_hours"].plot(kind="bar", ax=axes[1], color=["#4F008C", "#E5007D"])
    axes[1].set_title("Total watch hours by program class")
    axes[1].set_ylabel("Hours")
    for axis in axes:
        axis.tick_params(axis="x", rotation=0)
    figure.tight_layout()
    plt.show()


def plot_quality(metrics):
    figure, axes = plt.subplots(1, 2, figsize=(11, 4))
    metrics["total_views"].plot(kind="pie", ax=axes[0], autopct="%1.1f%%",
                                colors=["#00A19A", "#9E9E9E"])
    axes[0].set_title("Share of views: HD vs SD")
    axes[0].set_ylabel("")
    metrics["avg_minutes"].plot(kind="bar", ax=axes[1], color=["#00A19A", "#9E9E9E"])
    axes[1].set_title("Average minutes per view")
    axes[1].set_ylabel("Minutes")
    axes[1].tick_params(axis="x", rotation=0)
    figure.tight_layout()
    plt.show()


def plot_top_titles(top_movies, top_series):
    figure, axes = plt.subplots(1, 2, figsize=(13, 5))
    top_movies["total_views"].sort_values().plot(kind="barh", ax=axes[0], color="#4F008C")
    axes[0].set_title(f"Top {TOP_N} movies by views")
    top_series["total_views"].sort_values().plot(kind="barh", ax=axes[1], color="#E5007D")
    axes[1].set_title(f"Top {TOP_N} series by views")
    for axis in axes:
        axis.set_xlabel("Views")
        axis.set_ylabel("")
    figure.tight_layout()
    plt.show()


def plot_monthly_trend(trend):
    figure, axis = plt.subplots(figsize=(11, 4))
    axis.plot(trend.index, trend["watch_hours"], marker="o", color="#4F008C")
    axis.set_title("Total watch hours per month")
    axis.set_ylabel("Hours")
    axis.grid(alpha=0.3)
    figure.tight_layout()
    plt.show()


# ---------------------------------------------------------------- main

def main():
    raw = load_data()
    data = clean_data(raw)

    show_key_numbers(data)
    summarise_numbers(data)

    class_metrics = compare_program_class(data)
    quality_metrics = compare_quality(data)

    movies = data[data["content_type"].eq("Movie")]
    series = data[data["content_type"].eq("Series")]

    top_movies = rank_top(movies, "movie_title", "Movie")
    top_series = rank_top(series, "show_name", "TV Series")
    top_episodes = rank_top(series, "episode_name", "Episode")

    summarise_genres(data)
    trend = monthly_trend(data)

    plot_program_class(class_metrics)
    plot_quality(quality_metrics)
    plot_top_titles(top_movies, top_series)
    plot_monthly_trend(trend)

    data.to_csv("stc_cleaned_data.csv", index=False)
    top_movies.to_csv("top10_movies.csv")
    top_series.to_csv("top10_series.csv")
    top_episodes.to_csv("top10_episodes.csv")
    print("Saved: stc_cleaned_data.csv, top10_movies.csv, top10_series.csv, top10_episodes.csv")


if __name__ == "__main__":
    main()
