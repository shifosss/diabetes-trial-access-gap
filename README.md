# JSC370 Final Project — Clinical Trial Access Gap for Type 2 Diabetes

**Live website:** <https://shifosss.github.io/diabetes-trial-access-gap/>

- **Landing page** (summary + findings): <https://shifosss.github.io/diabetes-trial-access-gap/>
- **Full report**: <https://shifosss.github.io/diabetes-trial-access-gap/writing-report.html>
- **Downloadable PDF of the report**: <https://shifosss.github.io/diabetes-trial-access-gap/writing-report.pdf>
- **Interactive visualizations (HW5 deliverable)**: <https://shifosss.github.io/diabetes-trial-access-gap/viz.html> — **Figures 1, 2, and 3 on that page are interactive.**
- **5-minute presentation**: <https://youtu.be/wbvBLSPmb5k>
- **About / data sources**: <https://shifosss.github.io/diabetes-trial-access-gap/about.html>

_The project began as the JSC370 midterm and is extended into the final deliverable. The repository name (`diabetes-trial-access-gap`) is preserved to keep URLs stable; the content below is the final-project version._

## What this project studies

U.S. Type 2 diabetes clinical-trial access, at the state and county level. We link the ClinicalTrials.gov registry with diabetes burden, socioeconomic context, Medicaid expansion, rurality, and healthcare-infrastructure proxies to ask:

1. **Descriptive aim** — how aligned is the geographic distribution of U.S. Type 2 diabetes trial sites with disease burden? Where are the largest access gaps?
2. **Modeling aim** — once county-level socioeconomic and demographic structure is in the feature set, do trial-access features (local trial density, distance to the nearest site) add independent predictive signal for county-level diabetes prevalence?

See the [full report](https://shifosss.github.io/diabetes-trial-access-gap/writing-report.html) for the methods, results, and conclusions.

## Repository layout

```
.
├── _quarto.yml                      # Site project config
├── index.qmd                        # Landing page
├── writing-report.qmd               # Full report (HTML + PDF)
├── viz.qmd                          # Interactive visualizations (HW5)
├── about.qmd                        # Author / data sources / acknowledgements
├── styles.css                       # Site styles
├── docs/                            # Rendered site (served by GitHub Pages)
├── jsc370.full.yml                  # Conda environment specification
├── option-c-trial-access/
│   ├── discover/                    # Midterm-era exploration and EDA
│   │   ├── data_acquiring/          # Jupyter notebook for initial API pulls
│   │   └── results/                 # Static EDA figures (PNG)
│   └── product/
│       ├── option-c.qmd             # Full computational pipeline
│       ├── _regenerate_cv_comparison.py   # Standalone re-runner for Aim 2 CV
│       ├── data/
│       │   ├── raw/                 # Raw API responses (gitignored)
│       │   └── modified/
│       │       ├── state_modeling_final.csv
│       │       ├── county_modeling_final.csv
│       │       └── temp/            # Intermediate tables incl. model_comparison_cv.csv
│       └── results/                 # Modeling output figures (PNG)
├── tasks/                           # Project todos and lessons
└── spec-*.md                        # Digested assignment specs
```

## Data sources

All data are obtained via public APIs. No restricted or human-subject data is used.

| Source | Purpose | Access |
|---|---|---|
| [ClinicalTrials.gov v2 API](https://clinicaltrials.gov/api/v2) | U.S. Type 2 diabetes trials and sites | Public, no key |
| [CDC PLACES (Socrata)](https://chronicdata.cdc.gov/) | Age-adjusted diabetes prevalence and related measures | Public, no key |
| [U.S. Census ACS 5-Year 2022](https://www.census.gov/data/developers/data-sets/acs-5year.html) | Socioeconomic and demographic covariates | API key required |
| [FCC Census API](https://geo.fcc.gov/api/census/) | Reverse geocoding lat/lon → 5-digit county FIPS | Public, no key |
| [2022 Census Gazetteer](https://www.census.gov/geographies/reference-files/time-series/geo/gazetteer-files.html) | Place-level lat/lon for city-to-county geocoding | Public download |
| [NPI Registry](https://npiregistry.cms.hhs.gov/api-page) | Endocrinologist density and academic medical center presence | Public, no key |
| 2020 Census Decennial | State-level rural population share | Public download |
| Hardcoded Medicaid expansion lookup | State policy context (as of January 2024) | Curated |

## Reproducing the pipeline and site

### 1. Environment

```bash
conda env create -f jsc370.full.yml
conda activate jsc370
```

### 2. Census API key

Create a `.env` file at the repo root:

```
CENSUS_API_KEY=<your_key>
```

You can request a free key at <https://api.census.gov/data/key_signup.html>.

### 3. Regenerate the data

The full pipeline (API pulls → geocoding → merges → modeling → figures) runs from the pipeline notebook:

```bash
quarto render option-c-trial-access/product/option-c.qmd
```

End-to-end this takes roughly 30 minutes, depending on network speed and CPU. Intermediate and final CSVs land in `option-c-trial-access/product/data/modified/` (and `temp/`).

To regenerate **only** the Aim 2 CV comparison table used in the written report (about 60 seconds):

```bash
python option-c-trial-access/product/_regenerate_cv_comparison.py
```

### 4. Build the site

```bash
quarto render                                   # HTML for index, report, viz, about
quarto render writing-report.qmd --to pdf       # Downloadable PDF of the report
```

The rendered site lands in `docs/`. GitHub Pages serves `docs/` from the `main` branch at <https://shifosss.github.io/diabetes-trial-access-gap/>.

## Key pipeline outputs (tracked in git)

- `option-c-trial-access/product/data/modified/state_modeling_final.csv` — state-level modeling dataset (51 rows × 53 columns).
- `option-c-trial-access/product/data/modified/county_modeling_final.csv` — county-level modeling dataset (3,221 rows × 42 columns).
- `option-c-trial-access/product/data/modified/temp/model_comparison_cv.csv` — CV metrics for the Aim 2 comparison table.
- `option-c-trial-access/product/results/*.png` — Aim 2 modeling figures (SHAP, permutation importance, Elastic Net coefficients, model comparison, etc.).
- `option-c-trial-access/discover/results/*.png` — Aim 1 descriptive figures (state tile maps, coverage residual, county distance, etc.).

## License

See `LICENSE`.
