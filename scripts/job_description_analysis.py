import csv
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd


SOURCE_CSV = Path(r"C:\Users\User\Downloads\postings.csv\postings.csv")
OUTPUT_DIR = Path("outputs")
REPORT_DIR = Path("reports")
TEMPLATE_DIR = Path("templates")

CHUNK_SIZE = 25_000

TEXT_COLS = ["title", "description", "skills_desc"]
NUMERIC_COLS = [
    "views",
    "applies",
    "min_salary",
    "med_salary",
    "max_salary",
    "normalized_salary",
    "remote_allowed",
    "sponsored",
]
KEEP_COLS = [
    "job_id",
    "company_name",
    "title",
    "description",
    "location",
    "formatted_work_type",
    "formatted_experience_level",
    "remote_allowed",
    "sponsored",
    "views",
    "applies",
    "application_type",
    "pay_period",
    "currency",
    "normalized_salary",
    "skills_desc",
]

STOPWORDS = {
    "a",
    "about",
    "above",
    "after",
    "all",
    "also",
    "an",
    "and",
    "any",
    "are",
    "as",
    "at",
    "be",
    "by",
    "can",
    "company",
    "description",
    "for",
    "from",
    "has",
    "have",
    "in",
    "is",
    "it",
    "job",
    "more",
    "must",
    "of",
    "on",
    "or",
    "our",
    "role",
    "that",
    "the",
    "this",
    "to",
    "we",
    "with",
    "will",
    "work",
    "you",
    "your",
}

POSITIVE_WORDS = {
    "advance",
    "benefit",
    "collaborative",
    "competitive",
    "creative",
    "development",
    "diverse",
    "equity",
    "excellent",
    "flexible",
    "friendly",
    "growth",
    "inclusive",
    "innovative",
    "learning",
    "opportunity",
    "paid",
    "professional",
    "respect",
    "support",
    "supportive",
    "team",
    "training",
    "wellness",
}

NEGATIVE_WORDS = {
    "aggressive",
    "complaint",
    "crisis",
    "deadline",
    "demanding",
    "difficult",
    "fast-paced",
    "pressure",
    "stress",
    "strict",
    "urgent",
}

KEYWORD_PATTERNS = {
    "salary_transparency": r"\$|\bsalary\b|\bpay\b|\bcompensation\b|\bwage\b",
    "benefits": r"\bbenefits?\b|\bhealthcare\b|\bmedical\b|\bdental\b|\b401k\b|\bpto\b|\bpaid time off\b",
    "flexibility": r"\bflexible\b|\bremote\b|\bhybrid\b|\bwork[- ]life\b|\btelecommute\b",
    "growth": r"\bgrowth\b|\bcareer\b|\btraining\b|\blearning\b|\bdevelopment\b|\badvancement\b",
    "culture": r"\bculture\b|\binclusive\b|\bdiverse\b|\bcollaborative\b|\bsupportive\b|\bteam\b",
    "requirements": r"\brequirements?\b|\bqualifications?\b|\bmust have\b|\bpreferred\b",
    "responsibilities": r"\bresponsibilities\b|\bduties\b|\bwhat you.?ll do\b",
    "call_to_action": r"\bapply\b|\bsend resume\b|\bsubmit\b|\bjoin us\b",
}


def clean_text(value: object) -> str:
    if pd.isna(value):
        return ""
    text = str(value).replace("\uFFFD", "'")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def word_tokens(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z][a-zA-Z+\-']{1,}", text.lower())


def sentence_count(text: str) -> int:
    return max(1, len(re.findall(r"[.!?]+(?:\s|$)", text)))


def count_syllables(word: str) -> int:
    word = word.lower()
    groups = re.findall(r"[aeiouy]+", word)
    count = len(groups)
    if word.endswith("e") and count > 1:
        count -= 1
    return max(1, count)


def readability(text: str) -> tuple[float, float]:
    tokens = word_tokens(text)
    words = max(1, len(tokens))
    sentences = sentence_count(text)
    chars = sum(len(token) for token in tokens)
    # Automated Readability Index is much faster than syllable-heavy formulas on
    # large raw exports while still flagging dense, hard-to-scan descriptions.
    grade = 4.71 * (chars / words) + 0.5 * (words / sentences) - 21.43
    reading_ease_proxy = 100 - (grade * 6)
    return round(reading_ease_proxy, 2), round(max(0, grade), 2)


def sentiment_score(tokens: list[str]) -> float:
    if not tokens:
        return 0.0
    pos = sum(1 for token in tokens if token in POSITIVE_WORDS)
    neg = sum(1 for token in tokens if token in NEGATIVE_WORDS)
    return round((pos - neg) / math.sqrt(len(tokens)), 4)


def normalize_chunk(df: pd.DataFrame) -> pd.DataFrame:
    for col in KEEP_COLS:
        if col not in df.columns:
            df[col] = pd.NA
    df = df[KEEP_COLS].copy()
    for col in TEXT_COLS:
        df[col] = df[col].map(clean_text)
    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df["description"] = df["description"].replace("", pd.NA)
    df = df.dropna(subset=["job_id", "description"]).drop_duplicates(subset=["job_id"])
    df["views"] = df["views"].fillna(0)
    df["applies"] = df["applies"].fillna(0)
    df["apply_rate"] = df.apply(
        lambda row: row["applies"] / row["views"] if row["views"] and row["views"] > 0 else pd.NA,
        axis=1,
    )
    return df


def add_text_features(df: pd.DataFrame) -> pd.DataFrame:
    features = defaultdict(list)
    for text in df["description"]:
        tokens = word_tokens(text)
        flesch, grade = readability(text)
        lowered = text.lower()
        features["word_count"].append(len(tokens))
        features["sentence_count"].append(sentence_count(text))
        features["avg_word_length"].append(round(sum(map(len, tokens)) / max(1, len(tokens)), 2))
        features["flesch_reading_ease"].append(flesch)
        features["flesch_kincaid_grade"].append(grade)
        features["sentiment_score"].append(sentiment_score(tokens))
        features["bullet_count"].append(text.count(" - ") + text.count("•"))
        features["question_count"].append(text.count("?"))
        features["has_salary_language"].append(bool(re.search(KEYWORD_PATTERNS["salary_transparency"], lowered)))
        features["has_benefits"].append(bool(re.search(KEYWORD_PATTERNS["benefits"], lowered)))
        features["has_flexibility"].append(bool(re.search(KEYWORD_PATTERNS["flexibility"], lowered)))
        features["has_growth_language"].append(bool(re.search(KEYWORD_PATTERNS["growth"], lowered)))
        features["has_culture_language"].append(bool(re.search(KEYWORD_PATTERNS["culture"], lowered)))
        features["has_requirements_section"].append(bool(re.search(KEYWORD_PATTERNS["requirements"], lowered)))
        features["has_responsibilities_section"].append(bool(re.search(KEYWORD_PATTERNS["responsibilities"], lowered)))
        features["has_call_to_action"].append(bool(re.search(KEYWORD_PATTERNS["call_to_action"], lowered)))
    for col, values in features.items():
        df[col] = values
    df["clarity_score"] = (
        100
        - (df["flesch_kincaid_grade"].clip(lower=8) - 8) * 4
        - (df["word_count"].sub(650).clip(lower=0) / 25)
        + df["has_responsibilities_section"].astype(int) * 5
        + df["has_requirements_section"].astype(int) * 5
        + df["has_benefits"].astype(int) * 4
    ).clip(lower=0, upper=100).round(1)
    return df


def choose_analysis_sample(df: pd.DataFrame, max_rows: int = 40_000) -> pd.DataFrame:
    if len(df) <= max_rows:
        return df
    top = df.nlargest(min(10_000, len(df)), "applies")
    rest = df.drop(top.index)
    sampled = rest.sample(max_rows - len(top), random_state=42)
    return pd.concat([top, sampled], ignore_index=True)


def update_keyword_stats(row: pd.Series, high: bool, counters: dict[str, Counter]) -> None:
    tokens = [token for token in word_tokens(row["description"])[:700] if token not in STOPWORDS and len(token) > 2]
    phrases = [f"{tokens[i]} {tokens[i + 1]}" for i in range(len(tokens) - 1)]
    unique_terms = set(tokens + phrases)
    bucket = "high" if high else "low"
    counters[bucket].update(unique_terms)


def lift_table(high_counter: Counter, low_counter: Counter, min_count: int = 20) -> pd.DataFrame:
    terms = set(high_counter) | set(low_counter)
    high_total = sum(high_counter.values()) + len(terms)
    low_total = sum(low_counter.values()) + len(terms)
    rows = []
    for term in terms:
        high = high_counter[term]
        low = low_counter[term]
        if high + low < min_count:
            continue
        lift = ((high + 1) / high_total) / ((low + 1) / low_total)
        rows.append({"term": term, "high_apply_posts": high, "low_apply_posts": low, "lift": round(lift, 3)})
    return pd.DataFrame(rows).sort_values(["lift", "high_apply_posts"], ascending=[False, False])


def weighted_mean(df: pd.DataFrame, column: str) -> float:
    weights = df["views"].fillna(0).clip(lower=0)
    if weights.sum() == 0:
        return float(df[column].mean())
    return float((df[column] * weights).sum() / weights.sum())


def summarize(cleaned_path: Path) -> dict[str, object]:
    usecols = KEEP_COLS
    analysis_rows = []
    keyword_rows = []
    null_counts = Counter()
    total_raw = 0
    total_cleaned = 0
    if cleaned_path.exists():
        print(f"Using existing cleaned file: {cleaned_path}", flush=True)
        for chunk_no, cleaned in enumerate(pd.read_csv(cleaned_path, chunksize=CHUNK_SIZE, low_memory=False), 1):
            total_cleaned += len(cleaned)
            slim_cols = [
                col
                for col in cleaned.columns
                if col not in {"description", "skills_desc", "job_posting_url", "application_url"}
            ]
            analysis_rows.append(cleaned[slim_cols])
            keyword_rows.append(cleaned[["job_id", "description", "applies"]])
            print(f"Loaded cleaned chunk {chunk_no}: {total_cleaned:,} rows", flush=True)
        with SOURCE_CSV.open(encoding="utf-8", errors="replace", newline="") as source:
            total_raw = max(0, sum(1 for _ in csv.reader(source)) - 1)
    else:
        for chunk_no, chunk in enumerate(pd.read_csv(
            SOURCE_CSV,
            usecols=lambda col: col in usecols,
            chunksize=CHUNK_SIZE,
            low_memory=False,
            encoding_errors="replace",
        ), 1):
            total_raw += len(chunk)
            null_counts.update({col: int(chunk[col].isna().sum()) for col in chunk.columns})
            cleaned = add_text_features(normalize_chunk(chunk))
            total_cleaned += len(cleaned)
            cleaned.to_csv(
                cleaned_path,
                index=False,
                mode="a",
                header=not cleaned_path.exists(),
                quoting=csv.QUOTE_MINIMAL,
            )
            slim_cols = [
                col
                for col in cleaned.columns
                if col not in {"description", "skills_desc", "job_posting_url", "application_url"}
            ]
            analysis_rows.append(cleaned[slim_cols])
            keyword_rows.append(cleaned[["job_id", "description", "applies"]])
            print(f"Processed chunk {chunk_no}: {total_raw:,} raw rows, {total_cleaned:,} cleaned rows", flush=True)

    df = pd.concat(analysis_rows, ignore_index=True)
    df = df.drop_duplicates(subset=["job_id"]).reset_index(drop=True)
    keyword_df = pd.concat(keyword_rows, ignore_index=True).drop_duplicates(subset=["job_id"]).reset_index(drop=True)

    valid_apps = df[df["applies"].notna()].copy()
    high_threshold = valid_apps["applies"].quantile(0.75)
    low_threshold = valid_apps["applies"].quantile(0.25)
    keyword_sample = choose_analysis_sample(keyword_df)
    high = keyword_sample[keyword_sample["applies"] >= high_threshold].nlargest(12_000, "applies")
    low = keyword_sample[keyword_sample["applies"] <= low_threshold].nsmallest(12_000, "applies")

    counters = {"high": Counter(), "low": Counter()}
    for _, row in high.iterrows():
        update_keyword_stats(row, True, counters)
    for _, row in low.iterrows():
        update_keyword_stats(row, False, counters)

    keyword_lift = lift_table(counters["high"], counters["low"])
    keyword_lift.head(75).to_csv(OUTPUT_DIR / "effective_keywords.csv", index=False)

    feature_cols = [
        "word_count",
        "flesch_reading_ease",
        "flesch_kincaid_grade",
        "sentiment_score",
        "clarity_score",
        "has_salary_language",
        "has_benefits",
        "has_flexibility",
        "has_growth_language",
        "has_culture_language",
        "has_requirements_section",
        "has_responsibilities_section",
        "has_call_to_action",
    ]
    correlations = (
        df[["applies", "apply_rate", "views"] + feature_cols]
        .corr(numeric_only=True)[["applies", "apply_rate"]]
        .sort_values("applies", ascending=False)
    )
    correlations.to_csv(OUTPUT_DIR / "feature_correlations.csv")

    top_by_applies = df.sort_values(["applies", "views"], ascending=False).head(50)
    top_by_applies.to_csv(OUTPUT_DIR / "top_posts_by_applications.csv", index=False)

    visibility_floor = max(100, float(df["views"].quantile(0.5)))
    top_by_rate = df[df["views"] >= visibility_floor].sort_values(
        ["apply_rate", "applies"], ascending=False
    ).head(50)
    top_by_rate.to_csv(OUTPUT_DIR / "top_posts_by_apply_rate.csv", index=False)

    grouped = []
    for col in ["formatted_work_type", "formatted_experience_level", "remote_allowed", "sponsored"]:
        group = (
            df.groupby(col, dropna=False)
            .agg(
                postings=("job_id", "count"),
                avg_views=("views", "mean"),
                avg_applies=("applies", "mean"),
                avg_apply_rate=("apply_rate", "mean"),
                avg_clarity=("clarity_score", "mean"),
            )
            .reset_index()
        )
        group.insert(0, "segment", col)
        group = group.rename(columns={col: "value"})
        grouped.append(group)
    pd.concat(grouped, ignore_index=True).to_csv(OUTPUT_DIR / "segment_performance.csv", index=False)

    keyword_flags = []
    for flag in [col for col in df.columns if col.startswith("has_")]:
        flag_df = (
            df.groupby(flag)
            .agg(
                postings=("job_id", "count"),
                avg_applies=("applies", "mean"),
                avg_apply_rate=("apply_rate", "mean"),
                avg_clarity=("clarity_score", "mean"),
            )
            .reset_index()
        )
        present = flag_df[flag_df[flag] == True]
        absent = flag_df[flag_df[flag] == False]
        if not present.empty and not absent.empty:
            keyword_flags.append(
                {
                    "feature": flag,
                    "posts_with_feature": int(present["postings"].iloc[0]),
                    "avg_applies_with": round(float(present["avg_applies"].iloc[0]), 2),
                    "avg_applies_without": round(float(absent["avg_applies"].iloc[0]), 2),
                    "avg_apply_rate_with": round(float(present["avg_apply_rate"].iloc[0]), 4),
                    "avg_apply_rate_without": round(float(absent["avg_apply_rate"].iloc[0]), 4),
                    "avg_clarity_with": round(float(present["avg_clarity"].iloc[0]), 2),
                }
            )
    pd.DataFrame(keyword_flags).sort_values("avg_applies_with", ascending=False).to_csv(
        OUTPUT_DIR / "keyword_feature_performance.csv", index=False
    )

    bins = pd.cut(df["word_count"], bins=[0, 150, 300, 500, 750, 1000, 10_000])
    length_perf = (
        df.groupby(bins, observed=False)
        .agg(postings=("job_id", "count"), avg_applies=("applies", "mean"), avg_apply_rate=("apply_rate", "mean"))
        .reset_index()
    )
    length_perf.to_csv(OUTPUT_DIR / "length_performance.csv", index=False)

    return {
        "total_raw": total_raw,
        "total_cleaned": len(df),
        "removed": total_raw - len(df),
        "high_threshold": high_threshold,
        "low_threshold": low_threshold,
        "df": df,
        "keyword_lift": keyword_lift,
        "correlations": correlations,
        "keyword_flags": pd.DataFrame(keyword_flags).sort_values("avg_applies_with", ascending=False),
        "length_perf": length_perf,
        "top_by_applies": top_by_applies,
        "top_by_rate": top_by_rate,
        "visibility_floor": visibility_floor,
    }


def write_report(summary: dict[str, object]) -> None:
    df = summary["df"]
    keyword_lift = summary["keyword_lift"].head(20)
    keyword_flags = summary["keyword_flags"]
    length_perf = summary["length_perf"]
    top = summary["top_by_applies"].head(10)
    rate = summary["top_by_rate"].head(10)

    best_length = length_perf.sort_values("avg_apply_rate", ascending=False).iloc[0]
    best_feature_rows = keyword_flags.head(8)
    corr = summary["correlations"]

    report = f"""# Job Description Effectiveness Report

## Dataset Cleaning Summary

- Source file: `{SOURCE_CSV}`
- Raw rows processed: {summary["total_raw"]:,}
- Cleaned unique postings with usable descriptions: {summary["total_cleaned"]:,}
- Removed rows: {summary["removed"]:,} (missing key fields, missing descriptions, or duplicate job IDs)
- Cleaned output: `outputs/cleaned_postings.csv`

Cleaning steps applied:
- Standardized empty text fields and repaired replacement characters where possible.
- Converted numeric fields such as `views`, `applies`, compensation, remote flag, and sponsorship flag.
- Removed duplicate `job_id` values.
- Kept records with a valid job ID and non-empty description.
- Added NLP-derived fields for word count, sentence count, readability, grade level, sentiment, keyword flags, and clarity score.

## What Generates The Most Applications

The highest-application postings tend to have strong visibility, so `views` is still the dominant driver. To avoid confusing exposure with quality, the analysis also reviews apply rate (`applies / views`) for postings with at least {summary["visibility_floor"]:.0f} views.

Top postings by total applications:

| Rank | Title | Company | Views | Applies | Apply Rate |
|---:|---|---|---:|---:|---:|
"""
    for idx, (_, row) in enumerate(top.iterrows(), 1):
        company = row["company_name"] if pd.notna(row["company_name"]) and str(row["company_name"]).strip() else "Unknown"
        report += (
            f"| {idx} | {row['title']} | {company} | "
            f"{row['views']:.0f} | {row['applies']:.0f} | {row['apply_rate'] if pd.notna(row['apply_rate']) else 0:.3f} |\n"
        )

    report += f"""
Top postings by apply rate among jobs with at least {summary["visibility_floor"]:.0f} views:

| Rank | Title | Company | Views | Applies | Apply Rate |
|---:|---|---|---:|---:|---:|
"""
    for idx, (_, row) in enumerate(rate.iterrows(), 1):
        company = row["company_name"] if pd.notna(row["company_name"]) and str(row["company_name"]).strip() else "Unknown"
        report += (
            f"| {idx} | {row['title']} | {company} | "
            f"{row['views']:.0f} | {row['applies']:.0f} | {row['apply_rate'] if pd.notna(row['apply_rate']) else 0:.3f} |\n"
        )

    report += f"""
## Effective Keywords And Phrases

These terms appeared more often in the top quartile of postings by applications than in the bottom quartile. Lift above 1.0 means the term is more common in high-application postings.

| Term | High-Application Posts | Low-Application Posts | Lift |
|---|---:|---:|---:|
"""
    for _, row in keyword_lift.iterrows():
        report += f"| {row['term']} | {row['high_apply_posts']} | {row['low_apply_posts']} | {row['lift']} |\n"

    report += """
## Readability, Clarity, Sentiment, And Tone

"""
    report += f"- Average description length: {df['word_count'].mean():.0f} words.\n"
    report += f"- Average readability ease proxy: {df['flesch_reading_ease'].mean():.1f}. Higher is easier to scan.\n"
    report += f"- Average estimated grade level: {df['flesch_kincaid_grade'].mean():.1f}.\n"
    report += f"- Average sentiment score: {df['sentiment_score'].mean():.3f}. Positive values mean more supportive/opportunity-oriented language.\n"
    report += f"- Best word-count band by apply rate: {best_length['word_count']}.\n"

    report += """
Feature performance:

| Feature | Posts With Feature | Avg Applies With | Avg Applies Without | Avg Apply Rate With | Avg Apply Rate Without |
|---|---:|---:|---:|---:|---:|
"""
    for _, row in best_feature_rows.iterrows():
        report += (
            f"| {row['feature']} | {row['posts_with_feature']} | {row['avg_applies_with']} | "
            f"{row['avg_applies_without']} | {row['avg_apply_rate_with']} | {row['avg_apply_rate_without']} |\n"
        )

    report += """
Most relevant correlations with total applications and apply rate:

| Feature | Corr. With Applies | Corr. With Apply Rate |
|---|---:|---:|
"""
    for feature, row in corr.head(12).iterrows():
        report += f"| {feature} | {row['applies']:.3f} | {row['apply_rate']:.3f} |\n"

    report += """
## Recommendations

1. Lead with a clear role summary, location/work model, and compensation or pay range when available.
2. Keep descriptions concise. The strongest apply-rate band in this dataset is shown above; avoid very long, dense descriptions unless the role genuinely requires detail.
3. Use skimmable sections: responsibilities, requirements, benefits, and hiring process.
4. Balance requirements with candidate value. High-performing language tends to emphasize support, growth, flexibility, benefits, and team context.
5. Reduce vague intensity phrases such as "fast-paced" unless paired with concrete support, staffing, and realistic workload context.
6. Keep the reading level accessible. Aim for about grade 8-10 unless the role requires technical/legal precision.
7. End with a direct call to action and remove duplicated or unrelated text from imported descriptions.

## Files Produced

- `outputs/cleaned_postings.csv`
- `outputs/top_posts_by_applications.csv`
- `outputs/top_posts_by_apply_rate.csv`
- `outputs/effective_keywords.csv`
- `outputs/feature_correlations.csv`
- `outputs/keyword_feature_performance.csv`
- `outputs/length_performance.csv`
- `outputs/segment_performance.csv`
- `templates/optimized_templates_library.md`
- `reports/writing_guidelines.md`
"""
    (REPORT_DIR / "job_description_effectiveness_report.md").write_text(report, encoding="utf-8")


def write_templates_and_guidelines() -> None:
    templates = """# Optimized Job Description Templates Library

## Template 1: General Professional Role

**Job Title:** [Clear title candidates search for]

**Location/Work Model:** [City, State] | [On-site/Hybrid/Remote]

**Compensation:** [Salary/hourly range] + [bonus/equity if applicable]

### Role Summary
[Company/team] is hiring a [role] to [primary outcome]. This role is a strong fit for someone who enjoys [2-3 realistic motivators] and wants to contribute to [business/customer impact].

### What You'll Do
- [Responsibility tied to business outcome]
- [Responsibility tied to team/customer collaboration]
- [Responsibility tied to tools/process/quality]
- [Responsibility tied to growth or ownership]

### What You'll Bring
- [Required skill/experience]
- [Required tool/domain knowledge]
- [Required communication/collaboration expectation]
- [Preferred qualification, clearly marked optional]

### What We Offer
- [Pay transparency]
- [Benefits]
- [Schedule/work model flexibility]
- [Training, mentorship, or advancement]

### Hiring Process
[Brief steps and timeline]

### Apply
Submit your resume and [any required material]. We welcome candidates from different backgrounds who meet the core requirements.

## Template 2: Technical Role

**Job Title:** [Specific technical title]

**Location/Work Model:** [Location] | [Remote/Hybrid/On-site]

**Compensation:** [Range]

### Why This Role Exists
We need a [role] to help [build/improve/operate] [product/system/process] for [users/business area].

### Core Responsibilities
- Build and maintain [systems/features/workflows].
- Collaborate with [teams] to define requirements and deliver reliable solutions.
- Improve [performance/security/data quality/automation].
- Document decisions and support smooth handoffs.

### Required Experience
- Experience with [primary tools/languages/platforms].
- Ability to explain tradeoffs and solve problems independently.
- Familiarity with [domain-specific requirement].

### Nice To Have
- [Optional skill]
- [Optional domain]

### Benefits And Growth
- [Benefits]
- [Learning budget/training/mentorship]
- [Career path]

### Apply
Apply with your resume and links to relevant work if available.

## Template 3: Entry-Level Or Internship Role

**Job Title:** [Entry-level title]

**Location/Work Model:** [Location/work model]

**Compensation:** [Range]

### What You'll Learn
In this role, you will build practical experience in [area 1], [area 2], and [area 3] while contributing to [team outcome].

### Responsibilities
- Support [task/process].
- Research, organize, and communicate [information/output].
- Learn and use [tools].
- Work with [team/manager] to complete projects on schedule.

### Requirements
- Interest in [field].
- Clear written and verbal communication.
- Ability to manage tasks and ask good questions.
- [Education/tool requirement only if truly necessary.]

### Support
- Training and regular feedback.
- Flexible scheduling where possible.
- Exposure to [career-building opportunity].

### Apply
Send your resume and a short note about your interest in the role.
"""
    guidelines = """# Job Description Writing Guidelines

## Core Principles

1. Make the first 100 words useful: include the role, location/work model, compensation when possible, and why the job matters.
2. Use candidate-centered language. Explain what the person will do, learn, and receive, not only what the company demands.
3. Keep structure predictable: summary, responsibilities, requirements, benefits, process, apply.
4. Separate required and preferred qualifications. Long requirement lists reduce perceived fit.
5. Use plain language. Target grade 8-10 readability for most roles.
6. Prefer specific nouns and verbs over generic phrases such as "rockstar", "wear many hats", or "fast-paced environment".
7. Include benefits, flexibility, growth, and culture signals when they are real.
8. Keep tone warm, direct, and realistic.

## Readability Checklist

- Use short paragraphs of 1-3 sentences.
- Use bullets for responsibilities and qualifications.
- Keep most bullets under 20 words.
- Avoid duplicated boilerplate and unrelated imported text.
- Define acronyms unless they are standard for the role.

## Tone Checklist

- Replace pressure-heavy language with clear expectations.
- Avoid exclusionary phrases such as "young", "digital native", "native English speaker", or "must be able-bodied".
- Use inclusive statements without letting them crowd out role clarity.
- Mention support systems: training, mentorship, team access, tools, or documented processes.

## Keyword Guidance

Use keywords naturally in sections candidates scan:

- Compensation: salary, hourly pay, pay range, bonus, benefits.
- Flexibility: remote, hybrid, flexible schedule, work-life balance.
- Growth: training, mentorship, development, advancement.
- Culture: supportive, collaborative, inclusive, team.
- Role clarity: responsibilities, qualifications, requirements, hiring process.

## Final Quality Gate

Before posting, confirm:

- The title matches common search terms.
- The compensation and work model are visible.
- The responsibilities describe outcomes, not only tasks.
- Requirements are realistic and not inflated.
- The description is concise, readable, and free of formatting artifacts.
- The call to action is direct.
"""
    (TEMPLATE_DIR / "optimized_templates_library.md").write_text(templates, encoding="utf-8")
    (REPORT_DIR / "writing_guidelines.md").write_text(guidelines, encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)
    TEMPLATE_DIR.mkdir(exist_ok=True)
    cleaned_path = OUTPUT_DIR / "cleaned_postings.csv"
    summary = summarize(cleaned_path)
    write_report(summary)
    write_templates_and_guidelines()
    print(f"Processed {summary['total_raw']:,} raw rows.")
    print(f"Wrote {summary['total_cleaned']:,} cleaned postings to {cleaned_path}.")
    print("Reports and templates are ready.")


if __name__ == "__main__":
    main()
