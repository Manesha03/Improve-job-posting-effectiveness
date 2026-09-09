# Job Description Optimization

This project analyzes a raw job postings dataset to understand which job descriptions generate more applications and what writing patterns improve posting effectiveness.

## Project Goals

- Clean the raw job postings dataset.
- Identify job descriptions that receive the most applications.
- Find effective keywords and phrases used in high-performing postings.
- Use NLP-style text features to assess readability, clarity, sentiment, and tone.
- Produce practical templates and writing guidelines for better job descriptions.

## Dataset

The source dataset used by the analysis script is:

```text
C:\Users\User\Downloads\postings.csv\postings.csv
```

The raw dataset contains job posting fields such as title, company name, description, views, applies, work type, salary information, remote status, and skills description.

## How To Run

Open PowerShell in the project folder:

```powershell
cd "D:\GR - Intern\Improve-job-posting-effectiveness"
python scripts/job_description_analysis.py
```

If the cleaned dataset already exists, the script reuses it and regenerates the report files. If it does not exist, the script reads the raw CSV, cleans it, creates NLP features, and writes all outputs.

## Expected Terminal Output

A successful run should look similar to this:

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

### 1. Job Description Effectiveness Report

```text
reports/job_description_effectiveness_report.md
```

Includes:

- Dataset cleaning summary.
- Top job postings by total applications.
- Top job postings by apply rate.
- Effective keywords and phrases.
- Readability, clarity, sentiment, and tone analysis.
- Recommendations for improving job descriptions.

### 2. Cleaned Dataset

```text
outputs/cleaned_postings.csv
```

Contains cleaned postings with additional analysis fields, including:

- `apply_rate`
- `word_count`
- `sentence_count`
- `flesch_reading_ease`
- `flesch_kincaid_grade`
- `sentiment_score`
- `clarity_score`
- keyword flags such as salary, benefits, flexibility, growth, culture, requirements, responsibilities, and call-to-action language

### 3. Optimized Templates Library

```text
templates/optimized_templates_library.md
```

Includes reusable templates for:

- General professional roles.
- Technical roles.
- Entry-level or internship roles.

### 4. Writing Guidelines

```text
reports/writing_guidelines.md
```

Provides practical guidance for writing clearer and more effective job descriptions.

## Supporting Analysis Outputs

The `outputs/` folder also includes:

```text
outputs/effective_keywords.csv
outputs/feature_correlations.csv
outputs/keyword_feature_performance.csv
outputs/length_performance.csv
outputs/segment_performance.csv
outputs/top_posts_by_applications.csv
outputs/top_posts_by_apply_rate.csv
```

These files support the main report and can be opened in Excel, Power BI, Tableau, or any spreadsheet tool.

## Method Summary

The script performs the following steps:

1. Loads the raw CSV in chunks so the large file can be processed safely.
2. Cleans text fields and numeric columns.
3. Removes rows with missing key fields and duplicate job IDs.
4. Calculates application rate using `applies / views`.
5. Extracts text features from job descriptions.
6. Scores readability, clarity, and sentiment.
7. Compares high-application postings against low-application postings to identify effective terms.
8. Generates CSV outputs, a Markdown report, a templates library, and writing guidelines.

## Requirements

Python is required. The script uses:

- `pandas`
- standard Python libraries: `csv`, `math`, `re`, `collections`, and `pathlib`

Install pandas if needed:

```powershell
pip install pandas
```

## Notes

This is a data analysis project, not a web application. Running the project generates cleaned data files and report documents.

