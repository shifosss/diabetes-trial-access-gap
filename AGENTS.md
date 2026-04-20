# Repository Guidelines

## Project Structure & Module Organization
This repository is organized into four analysis tracks:
`option-a-drug-safety/`, `option-b-ed-timeliness/`, `option-c-trial-access/`, and `option-d-conflicts-of-interest/`.

Inside each option folder:
- `discover/data_acquiring/` contains API pull and exploratory notebooks.
- `discover/modified_data/` and `discover/results/` hold intermediate tables and figures.
- `product/option-<letter>.qmd` is the report source.
- `product/data/raw/` and `product/data/modified/` stage report inputs.
- `product/results/` stores report-ready outputs.

Use `docs/` for shared planning and research context:
- `docs/clinical_midterm_options.md` defines the four option specifications, from API calls and data acquisition through analysis and modeling plans.
- `docs/deep-research-report.md` captures background information, research completed so far, and project motivations.

## Build, Test, and Development Commands
- `quarto render option-b-ed-timeliness/product/option-b.qmd`  
  Render one option report to HTML.
- `for f in option-*/product/*.qmd; do quarto render "$f"; done`  
  Render all option reports.
- `jupyter nbconvert --to notebook --execute option-c-trial-access/discover/data_acquiring/api_call_data_grabbing.ipynb --inplace`  
  Re-run a notebook end-to-end to confirm acquisition/EDA still works.

## Coding Style & Naming Conventions
- Use 4-space indentation in Python code cells.
- Prefer `snake_case` for variables and data columns (for example, `df_analysis`, `state_abbr`).
- Keep filenames lowercase and descriptive, using hyphens for option directories and underscores in data artifacts.
- Preserve the `raw` -> `modified` -> `results` data flow in each option.

## Testing Guidelines
There is no formal automated test suite in this repository yet. Validate changes by:
- Executing the affected notebook(s) without cell errors.
- Confirming regenerated plots/tables in `discover/results/` or `product/results/`.
- Rendering the related `product/*.qmd` file and checking the HTML output.

## Commit & Pull Request Guidelines
Current history uses short, direct summaries (for example, `finished data acquiring process for option b and c`). Keep commits focused on one option or one pipeline step.

For pull requests, include:
- The option/research question affected.
- Key files and outputs changed.
- Exact commands used to reproduce outputs.
- Updated screenshots/figures when visual artifacts change.

## Security & Data Handling
Do not commit secrets or local environment files (`.env` is ignored). Large downloaded raw files are intentionally ignored; commit reproducible code, small derived outputs, and documentation instead.
