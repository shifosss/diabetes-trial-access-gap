# JSC370 Final Project — Clinical Trial Access Gap for Type 2 Diabetes

**Live website:** <https://shifosss.github.io/JSC370-Midterm-Proj/>

- **Report:** <https://shifosss.github.io/JSC370-Midterm-Proj/writing-report.html>
- **Interactive visualizations (HW5 deliverable):** <https://shifosss.github.io/JSC370-Midterm-Proj/viz.html> — Figures 1, 2, and 3 on that page are interactive.
- **About / data sources:** <https://shifosss.github.io/JSC370-Midterm-Proj/about.html>

*The project started as the JSC370 midterm and is being extended into the final deliverable. The repository name (`JSC370-Midterm-Proj`) is preserved to keep URLs stable; the content below is the final-project version.*

## Files To Grade

This repository is centered on **Option C: Clinical Trial Access Gap for Type 2 Diabetes**.

**Written report (source):** `writing-report.qmd`

**Written report (rendered):** `writing-report.html`

**Pipeline source file:** `option-c-trial-access/product/option-c.qmd`

**Pipeline rendered HTML:** `option-c-trial-access/product/option-c.html`

If the HTML needs to be regenerated, run:

```bash
quarto render writing-report.qmd
quarto render option-c-trial-access/product/option-c.qmd
```

## Project Focus

The active workstream in this repository is **Option C**. It studies U.S. Type 2 diabetes clinical trial access by linking ClinicalTrials.gov trial-site data with diabetes burden, socioeconomic context, rurality, Medicaid expansion, and healthcare infrastructure proxies.

The pipeline report (`option-c.qmd`) is an end-to-end workflow that:

1. pulls and flattens U.S. Type 2 diabetes studies and site records from ClinicalTrials.gov,
2. enriches them with CDC PLACES and Census/ACS context,
3. constructs state-level coverage alignment measures,
4. extends the analysis to counties (geocoding sites to FIPS, computing distances),
5. exports model-ready state and county datasets, and
6. fits county-level burden models using Elastic Net, Random Forest, and XGBoost.

The written report (`writing-report.qmd`) summarizes the research question, methods, and preliminary results in a narrative format.

Other option directories in this repository are archived reference material and are not part of the active submission.

## Repository Layout

```
.
├── writing-report.qmd              # Written deliverable report
├── writing-report.html             # Rendered written report
├── jsc370.full.yml                 # Conda environment specification
├── option-c-trial-access/
│   ├── discover/
│   │   ├── data_acquiring/         # Jupyter notebook for API pulls
│   │   │   └── api_call_data_grabbing.ipynb
│   │   ├── modified_data/          # Intermediate CSVs from discovery
│   │   ├── results/                # EDA plots (PNG)
│   │   ├── County_level_data_documentation.md
│   │   ├── State_level_data_documentation.md
│   │   └── EDA_Summary_and_Interpretation.md
│   └── product/
│       ├── option-c.qmd            # Pipeline report (main deliverable)
│       ├── option-c.html           # Rendered pipeline report
│       ├── option-c.ipynb          # Notebook precursor
│       ├── data/
│       │   ├── raw/                # Raw API responses (gitignored)
│       │   └── modified/
│       │       ├── state_modeling_final.csv
│       │       ├── county_modeling_final.csv
│       │       └── temp/           # Intermediate tables from render
│       └── results/                # Model output plots
│           ├── elastic_net_actual_vs_predicted.png
│           ├── elastic_net_coefficients.png
│           ├── model_comparison_cv.png
│           ├── rf_permutation_importance.png
│           ├── shap_summary_plot.png
│           └── shap_group_importance.png
└── option-d-conflicts-of-interest/ # Archived, gitignored
```

## What The Reports Contain

### Pipeline Report (`option-c.qmd`)

1. **ClinicalTrials.gov Acquisition and Flattening** — pulls and flattens nested JSON into trial and site records
2. **Burden and Context Enrichment** — joins CDC PLACES, ACS, rurality, Medicaid, NPI data
3. **State Coverage Alignment Assembly** — coverage residuals and quartile classification
4. **State Modeling Exports** — `state_modeling_final.csv`
5. **County Extension** — geocodes sites to county FIPS, computes Haversine distances
6. **Final-Dataset EDA** — correlation heatmaps, distributions, missingness
7. **Ready for Modeling** — `county_modeling_final.csv`
8. **Modeling: County Diabetes Burden** — Elastic Net, Random Forest, XGBoost with SHAP

### Written Report (`writing-report.qmd`)

- Introduction, background, and research question
- Methods (data acquisition, cleaning, wrangling)
- Preliminary results with figures and tables

## Main Data Sources

- **ClinicalTrials.gov API**: U.S. Type 2 diabetes studies and site locations
- **CDC PLACES**: diabetes burden and related population health measures (state and county)
- **ACS / Census**: socioeconomic and demographic county/state covariates
- **2022 Census Gazetteer**: place-level lat/lon for city-to-county geocoding
- **FCC Census API**: reverse geocoding to 5-digit county FIPS codes
- **NPI Registry**: endocrinologist density and academic medical center presence
- **Census rurality data**: rural population context
- **Medicaid expansion status**: state policy context

## How To Reproduce

1. Create and activate the conda environment:

```bash
conda env create -f jsc370.full.yml
conda activate jsc370
```

2. Create a `.env` file at the repo root with your Census API key:

```
CENSUS_API_KEY=<your_key>
```

3. Render the reports:

```bash
quarto render option-c-trial-access/product/option-c.qmd
quarto render writing-report.qmd
```

For live preview while editing:

```bash
quarto preview option-c-trial-access/product/option-c.qmd
```

## Notes For Grading

- The written report source is `writing-report.qmd`; the rendered submission is `writing-report.html`.
- The pipeline source is `option-c-trial-access/product/option-c.qmd`; the rendered version is `option-c-trial-access/product/option-c.html`.
- The final model-ready datasets are:
  - `option-c-trial-access/product/data/modified/state_modeling_final.csv`
  - `option-c-trial-access/product/data/modified/county_modeling_final.csv`
- Figures produced by the pipeline are saved under `option-c-trial-access/product/results/`.
- Figures produced during discovery EDA are under `option-c-trial-access/discover/results/`.
