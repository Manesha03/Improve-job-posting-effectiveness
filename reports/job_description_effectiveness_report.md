# Job Description Effectiveness Report

## Dataset Cleaning Summary

- Source file: `C:\Users\User\Downloads\postings.csv\postings.csv`
- Raw rows processed: 123,849
- Cleaned unique postings with usable descriptions: 123,842
- Removed rows: 7 (missing key fields, missing descriptions, or duplicate job IDs)
- Cleaned output: `outputs/cleaned_postings.csv`

Cleaning steps applied:
- Standardized empty text fields and repaired replacement characters where possible.
- Converted numeric fields such as `views`, `applies`, compensation, remote flag, and sponsorship flag.
- Removed duplicate `job_id` values.
- Kept records with a valid job ID and non-empty description.
- Added NLP-derived fields for word count, sentence count, readability, grade level, sentiment, keyword flags, and clarity score.

## What Generates The Most Applications

The highest-application postings tend to have strong visibility, so `views` is still the dominant driver. To avoid confusing exposure with quality, the analysis also reviews apply rate (`applies / views`) for postings with at least 100 views.

Top postings by total applications:

| Rank | Title | Company | Views | Applies | Apply Rate |
|---:|---|---|---:|---:|---:|
| 1 | Care Coordinator | Somnea Health | 2337 | 967 | 0.414 |
| 2 | Administrative Specialist - Remote | Archer | 2413 | 729 | 0.302 |
| 3 | UI/UX Designer | Sparkle Dryclean | 1197 | 625 | 0.522 |
| 4 | Senior Data Engineer | ChabezTech LLC | 959 | 566 | 0.590 |
| 5 | Sr Professional Recruiter (Remote) - RPO Consultant | ManpowerGroup | 1130 | 530 | 0.469 |
| 6 | Associate Software Engineer | Run A Better Set (RABS) | 1156 | 508 | 0.439 |
| 7 | SQL Developer | Equity Staffing Group | 900 | 493 | 0.548 |
| 8 | Social Media Manager | Tarte Cosmetics | 4378 | 472 | 0.108 |
| 9 | Data Engineer | Gardner Resources Consulting, LLC | 830 | 470 | 0.566 |
| 10 | Full Stack Engineer | Dealers United | 991 | 465 | 0.469 |

Top postings by apply rate among jobs with at least 100 views:

| Rank | Title | Company | Views | Applies | Apply Rate |
|---:|---|---|---:|---:|---:|
| 1 | Azure Data Engineer | Unknown | 110 | 74 | 0.673 |
| 2 | Senior Data Engineer | Revature | 144 | 91 | 0.632 |
| 3 | Data Analyst | Avant-garde Health | 330 | 207 | 0.627 |
| 4 | Cloud AWS Engineer | Unknown | 261 | 159 | 0.609 |
| 5 | Data Analyst-WA | ATC | 104 | 63 | 0.606 |
| 6 | Java Developer Contract | Trinity Technology Solutions LLC | 125 | 75 | 0.600 |
| 7 | Senior Data Engineer | ChabezTech LLC | 959 | 566 | 0.590 |
| 8 | Quality Assurance Automation Engineer | Acro Service Corp | 109 | 64 | 0.587 |
| 9 | Frontend Developer | Unknown | 368 | 214 | 0.582 |
| 10 | Sr DevOps Engineer `100% remote | Irvine Technology Corporation | 157 | 91 | 0.580 |

## Effective Keywords And Phrases

These terms appeared more often in the top quartile of postings by applications than in the bottom quartile. Lift above 1.0 means the term is more common in high-application postings.

| Term | High-Application Posts | Low-Application Posts | Lift |
|---|---:|---:|---:|
| experience restful | 25 | 0 | 28.655 |
| figma sketch | 25 | 0 | 28.655 |
| snowflake data | 25 | 0 | 28.655 |
| week intercontinental | 25 | 0 | 28.655 |
| frameworks libraries | 24 | 0 | 27.553 |
| languages java | 24 | 0 | 27.553 |
| hadoop spark | 23 | 0 | 26.451 |
| home flexibility | 41 | 1 | 23.145 |
| gcp experience | 20 | 0 | 23.145 |
| below additional | 20 | 0 | 23.145 |
| stack engineer | 36 | 1 | 20.389 |
| extract transform | 51 | 2 | 19.103 |
| services azure | 33 | 1 | 18.736 |
| building deploying | 33 | 1 | 18.736 |
| schedule offers | 31 | 1 | 17.634 |
| fullstack | 31 | 1 | 17.634 |
| sdet | 31 | 1 | 17.634 |
| title java | 28 | 1 | 15.981 |
| dax | 28 | 1 | 15.981 |
| engineer programmer | 28 | 1 | 15.981 |

## Readability, Clarity, Sentiment, And Tone

- Average description length: 516 words.
- Average readability ease proxy: -53.0. Higher is easier to scan.
- Average estimated grade level: 25.5.
- Average sentiment score: 0.403. Positive values mean more supportive/opportunity-oriented language.
- Best word-count band by apply rate: (0, 150].

Feature performance:

| Feature | Posts With Feature | Avg Applies With | Avg Applies Without | Avg Apply Rate With | Avg Apply Rate Without |
|---|---:|---:|---:|---:|---:|
| has_flexibility | 43064 | 2.75 | 1.59 | 0.0403 | 0.0301 |
| has_growth_language | 92642 | 1.93 | 2.18 | 0.0325 | 0.0372 |
| has_culture_language | 98429 | 1.89 | 2.4 | 0.0324 | 0.0388 |
| has_requirements_section | 103458 | 1.8 | 2.96 | 0.0314 | 0.0453 |
| has_responsibilities_section | 83977 | 1.65 | 2.73 | 0.0302 | 0.0411 |
| has_salary_language | 72432 | 1.5 | 2.69 | 0.0266 | 0.0437 |
| has_call_to_action | 46576 | 1.48 | 2.31 | 0.027 | 0.0377 |
| has_benefits | 80761 | 1.42 | 3.08 | 0.0252 | 0.0497 |

Most relevant correlations with total applications and apply rate:

| Feature | Corr. With Applies | Corr. With Apply Rate |
|---|---:|---:|
| applies | 1.000 | 0.456 |
| views | 0.526 | 0.209 |
| apply_rate | 0.456 | 1.000 |
| flesch_kincaid_grade | 0.061 | 0.136 |
| has_flexibility | 0.042 | 0.057 |
| sentiment_score | -0.001 | -0.011 |
| has_growth_language | -0.008 | -0.024 |
| has_culture_language | -0.015 | -0.030 |
| has_call_to_action | -0.030 | -0.061 |
| has_requirements_section | -0.032 | -0.060 |
| has_responsibilities_section | -0.038 | -0.060 |
| has_salary_language | -0.044 | -0.099 |

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
