# Job Description Optimization Analysis

Analyze job posting effectiveness using a raw LinkedIn-style postings dataset. The project cleans job descriptions, extracts NLP-based text features, identifies high-performing wording patterns, and generates practical reports, templates, and writing guidelines.

## Project Overview

This is a data analysis project focused on improving job description quality and application performance.

The analysis answers four main questions:

| Question | Output |
|---|---|
| Which job descriptions generate the most applications? | Top postings by applications and apply rate |
| Which keywords and phrases appear in high-performing postings? | Effective keyword lift analysis |
| How readable and clear are the descriptions? | Readability, grade-level proxy, clarity score |
| What tone and structure work best? | Sentiment, section flags, writing recommendations |

## Repository Structure

```text
Improve-job-posting-effectiveness/
|
+-- scripts/
|   +-- job_description_analysis.py
|
+-- reports/
|   +-- job_description_effectiveness_report.md
|   +-- writing_guidelines.md
|
+-- templates/
|   +-- optimized_templates_library.md
|
+-- outputs/
|   +-- effective_keywords.csv
|   +-- feature_correlations.csv
|   +-- keyword_feature_performance.csv
|   +-- length_performance.csv
|   +-- segment_performance.csv
|   +-- top_posts_by_applications.csv
|   +-- top_posts_by_apply_rate.csv
|   +-- cleaned_postings.csv        # generated locally, ignored by Git
|
+-- README.md
+-- .gitignore
```

## Dataset

The raw dataset is expected at:

```text
C:\Users\User\Downloads\postings.csv\postings.csv
```

The source CSV contains job posting fields such as:

- `job_id`
- `company_name`
- `title`
- `description`
- `views`
- `applies`
- `location`
- `formatted_work_type`
- `formatted_experience_level`
- `remote_allowed`
- `sponsored`
- `normalized_salary`
- `skills_desc`

## Important CSV Note

The generated cleaned dataset is:

```text
outputs/cleaned_postings.csv
```

This file is large, around hundreds of MB, so it is intentionally excluded from Git using `.gitignore`.

Do not commit `outputs/cleaned_postings.csv` to GitHub. GitHub blocks normal pushes with files over 100 MB. The file can be regenerated anytime by running the analysis script.

Tracked files should include:

- analysis script
- reports
- templates
- smaller summary CSV outputs
- README
- `.gitignore`

## Pipeline Flow

```text
Raw postings.csv
      |
      v
Load data in chunks
      |
      v
Clean text and numeric fields
      |
      v
Remove invalid rows and duplicate job IDs
      |
      v
Generate NLP-style features
      |
      v
Analyze applications, apply rate, keywords, tone, and readability
      |
      v
Write cleaned data, CSV summaries, reports, templates, and guidelines
```

## Features Created

The script adds analysis fields such as:

| Feature | Description |
|---|---|
| `apply_rate` | Applications divided by views |
| `word_count` | Number of words in the description |
| `sentence_count` | Estimated sentence count |
| `flesch_reading_ease` | Readability ease proxy |
| `flesch_kincaid_grade` | Estimated grade-level proxy |
| `sentiment_score` | Positive vs negative tone score |
| `clarity_score` | Combined clarity/readability structure score |
| `has_salary_language` | Detects salary, pay, compensation language |
| `has_benefits` | Detects benefits-related language |
| `has_flexibility` | Detects remote, hybrid, flexible work language |
| `has_growth_language` | Detects growth, learning, development language |
| `has_culture_language` | Detects culture and team language |
| `has_requirements_section` | Detects requirements/qualification wording |
| `has_responsibilities_section` | Detects duties/responsibility wording |
| `has_call_to_action` | Detects apply/submit/send resume language |

## Requirements

Python is required.

The script uses:

- `pandas`
- built-in Python libraries: `csv`, `math`, `re`, `collections`, `pathlib`

Install pandas if needed:

```powershell
pip install pandas
```

Check Python:

```powershell
python --version
```

## How To Run

Open PowerShell in the project folder:

```powershell
cd "D:\GR - Intern\Improve-job-posting-effectiveness"
python scripts/job_description_analysis.py
```

If `outputs/cleaned_postings.csv` already exists, the script reuses it and regenerates reports faster. If it does not exist, the script reads the raw CSV and creates the cleaned dataset from scratch.

## Expected Output

A successful run should show output similar to:

```text
Using existing cleaned file: outputs\cleaned_postings.csv
Loaded cleaned chunk 1: 25,000 rows
Loaded cleaned chunk 2: 50,000 rows
Loaded cleaned chunk 3: 75,000 rows
Loaded cleaned chunk 4: 100,000 rows
Loaded cleaned chunk 5: 123,842 rows
Processed 123,849 raw rows.
Wrote 123,842 cleaned postings to outputs\cleaned_postings.csv.
Reports and templates are ready.
```

## Main Deliverables

### Job Description Effectiveness Report

```text
reports/job_description_effectiveness_report.md
```

Includes:

- cleaning summary
- top postings by total applications
- top postings by apply rate
- effective keywords and phrases
- readability, clarity, sentiment, and tone findings
- recommendations for better job descriptions

### Optimized Templates Library

```text
templates/optimized_templates_library.md
```

Includes reusable templates for:

- general professional roles
- technical roles
- entry-level or internship roles

### Writing Guidelines

```text
reports/writing_guidelines.md
```

Includes practical guidance for:

- structure
- readability
- tone
- inclusive wording
- keyword usage
- final quality checks

## Supporting CSV Outputs

| File | Purpose |
|---|---|
| `outputs/effective_keywords.csv` | Terms more common in high-application postings |
| `outputs/feature_correlations.csv` | Correlations between text features, applications, and apply rate |
| `outputs/keyword_feature_performance.csv` | Performance of salary, benefits, flexibility, growth, culture, and CTA signals |
| `outputs/length_performance.csv` | Application performance by description length |
| `outputs/segment_performance.csv` | Performance by work type, experience level, remote flag, and sponsorship |
| `outputs/top_posts_by_applications.csv` | Highest total application postings |
| `outputs/top_posts_by_apply_rate.csv` | Highest apply-rate postings with a visibility threshold |

These files can be opened in Excel, Power BI, Tableau, or any spreadsheet tool.

## Current Results Summary

The latest generated analysis produced:

```text
Raw records processed: 123,849
Cleaned postings:      123,842
Removed records:       7
Duplicate job IDs:     0
```

Key finding examples:

- Shorter job descriptions had stronger average apply rates.
- Views are strongly related to total applications, so apply rate is used as a quality-adjusted metric.
- Flexible work language was associated with higher average applications and apply rate.
- The report recommends concise structure, clear responsibilities, realistic requirements, benefits, flexibility, growth language, and a direct call to action.

## GitHub / Version Control Notes

`outputs/cleaned_postings.csv` is ignored because it is too large for GitHub.

The repository should store reproducible code and lightweight deliverables. Large generated data should stay local or be stored using another large-file solution such as Git LFS, cloud storage, or a shared drive.

Recommended commit scope:

```text
scripts/job_description_analysis.py
reports/
templates/
outputs/*.csv except outputs/cleaned_postings.csv
README.md
.gitignore
```

## Project Type

This is not a web application. Running the project generates data analysis artifacts: cleaned data, summary tables, reports, templates, and writing guidelines.

