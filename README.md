# Talk to Your Data Research

A lightweight research repository to measure how data modelling and semantic context affect the correctness of natural-language analytics answers in Databricks.

## Research design

Configurations:
- V0: raw tables
- V1: clean analytical model
- V2: descriptions + joins
- V3: governed KPIs + vocabulary
- V4: example SQL + functions

Recommended benchmark: 40 business intents, 3 phrasings each, with repeated runs for the baseline and target configuration.

## Accuracy framework

Each answer is scored across five dimensions:

| Dimension | Weight |
|---|---:|
| Interpretation | 25% |
| Query logic | 30% |
| Result accuracy | 30% |
| Presentation | 10% |
| Transparency | 5% |

Scores are entered from 0 to 100 for each dimension. A critical error (wrong metric, population, time period, major join duplication, or fabricated value) forces `strict_correct = false`.

Headline metrics:
- **Strict accuracy** = fully correct answers / total answers
- **Weighted quality** = weighted average of the five dimensions
- **Consistent accuracy** = intents where every repeated run is strictly correct / intents tested
- **Safe-response rate** = correct clarification/refusal / ambiguous or unanswerable answers
- **Coverage** = appropriately answered valid questions / valid questions

Run: `python src/compute_accuracy.py benchmark/sample_results.csv --out results/summary.csv`

Tests: `python -m unittest discover -s tests -v`

## Benchmark workflow

1. Freeze dataset snapshot and benchmark before tuning.
2. Store one row per prompt execution in `benchmark/results.csv` using the template.
3. Keep gold SQL/results under version control where confidentiality allows.
4. Run scoring after each configuration.
5. Preserve a holdout set that is not used while tuning.

## Result schema

See `benchmark/results_template.csv` and `benchmark/SCORING_GUIDE.md`.
