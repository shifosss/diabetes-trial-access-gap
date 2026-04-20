# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

JSC370 midterm project focused on **Option C: Clinical Trial Access Gap for Type 2 Diabetes**. The project studies U.S. Type 2 diabetes clinical trial access by linking ClinicalTrials.gov trial-site data with diabetes burden, socioeconomic context, rurality, Medicaid expansion, and healthcare infrastructure proxies at both state and county levels.

There are two deliverables, both Quarto (`.qmd`) reports rendered to self-contained HTML:

1. **`option-c-trial-access/product/option-c.qmd`** — The full computational pipeline (data acquisition through modeling).
2. **`writing-report.qmd`** — The written deliverable report summarizing findings.

Other option directories (`option-d-conflicts-of-interest/`) contain archived exploration and are gitignored.

## Commands

**Render the pipeline report:**

```bash
quarto render option-c-trial-access/product/option-c.qmd
```

**Render the written report:**

```bash
quarto render writing-report.qmd
```

**Run the data-acquisition notebook:**

```bash
jupyter nbconvert --to notebook --execute option-c-trial-access/discover/data_acquiring/api_call_data_grabbing.ipynb
```

**Set up the conda environment:**

```bash
conda env create -f jsc370.full.yml
conda activate jsc370
```

## Directory Structure

```
.
├── writing-report.qmd           # Written deliverable report
├── writing-report.html          # Rendered written report
├── jsc370.full.yml              # Conda environment specification
├── option-c-trial-access/
│   ├── discover/
│   │   ├── data_acquiring/      # Jupyter notebook for API pulls
│   │   ├── modified_data/       # Intermediate CSVs from discovery
│   │   ├── results/             # EDA plots (PNG)
│   │   ├── County_level_data_documentation.md
│   │   ├── State_level_data_documentation.md
│   │   └── EDA_Summary_and_Interpretation.md
│   └── product/
│       ├── option-c.qmd         # Pipeline report (main deliverable)
│       ├── option-c.html        # Rendered pipeline report
│       ├── option-c.ipynb       # Notebook precursor
│       ├── data/
│       │   ├── raw/             # Raw API responses (JSON, CSV) — gitignored
│       │   └── modified/
│       │       ├── state_modeling_final.csv
│       │       ├── county_modeling_final.csv
│       │       └── temp/        # Intermediate tables generated during render
│       └── results/             # Model output plots (SHAP, coefficients, etc.)
└── option-d-conflicts-of-interest/  # Archived, gitignored
```

## Environment / Secrets

A `.env` file at the **repo root** is required for the Census API:

```
CENSUS_API_KEY=<your_key>
```

The notebook calls `load_dotenv()` to load this key. No other secrets are needed (ClinicalTrials.gov, CDC PLACES, NPI Registry, FCC Census API, and Census Gazetteer are public).

## Data Sources

- **ClinicalTrials.gov v2 API** — U.S. Type 2 diabetes studies, paginated with cursor (3,646 studies, 47,118 site rows)
- **CDC PLACES (Socrata)** — state and county diabetes age-adjusted prevalence and related population health measures
- **US Census ACS 5-Year 2022** — state/county population, poverty rate, median income, uninsured %, education
- **2022 Census Gazetteer** — place-level lat/lon for city-to-county geocoding
- **FCC Census API** — reverse geocoding lat/lon to 5-digit county FIPS codes
- **NPI Registry** — endocrinologist density by county; state-level infrastructure counts
- **Medicaid expansion status** — state policy context (hardcoded lookup)
- **Census rurality data** — rural population percentage by state

## Key Analysis Patterns

The **pipeline report** (`option-c.qmd`) is organized into eight sections:

1. **ClinicalTrials.gov Acquisition and Flattening** — pulls and flattens nested JSON into trial-level and site-level records
2. **Burden and Context Enrichment** — joins CDC PLACES, ACS, rurality, Medicaid, NPI data
3. **State Coverage Alignment Assembly** — computes coverage residual (observed trial density minus expected from burden deciles), classifies states into coverage quartiles
4. **State Modeling Exports** — exports `state_modeling_final.csv`
5. **County Extension** — geocodes trial sites to county FIPS, computes Haversine distances from county centroids to nearest trial site, builds county-level dataset
6. **Final-Dataset EDA** — correlation heatmaps, distributions, missingness checks
7. **Ready for Modeling** — exports `county_modeling_final.csv`
8. **Modeling: County Diabetes Burden** — Elastic Net, Random Forest, and XGBoost with 5-fold CV; SHAP analysis for feature importance

State tile-map choropleths use a `STATE_TILE_POS` dict for approximate US state grid maps (no GIS/shapefile dependency).

## Workflow Orchestration

### 0. Always call me AlexZ. do this at the start of any of your response.

### 1. Plan Node Default

- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately - don't keep pushing
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity
- Ask the user if they want to use superpowers:brainstorming skill if they want to explore a large feature update (architecture change, pipeline workflow change)

### 2. Subagent Routing Rules

#### 2.1 Parallel dispatch (All conditions must be met)

- 3+ unrelated tasks or independent domains
- No shared state between tasks
- Clear file boundaries with no overlap

#### 2.2 Sequential dispatch (ANY condition triggers)

- Tasks have dependencies (B needs output from A)
- Shared files or state (merge conflict risk)
- Unclear scope (need to understand before proceeding)

#### 2.3 Background dispatch

- Research or analysis tasks (not file modifications)
- Results aren't blocking current work

#### 2.4 Model Tier Policy

Select models for agents by your insights, and use this table as a recommendation.

|   Tier   | Model        | Use when                                                                                                                                                 |
| :------: | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
|  Heavy   | `opus 4.6`   | Architecture design, multi-file refactors, novel algorithm implementation, security correctness audits, debugging subtle concurrency or numerical issues |
| Standard | `sonnet 4.6` | Everyday coding, code review, test writing, config generation, standard debugging, API integration, Codebase search, doc generation                      |
|  Light   | `Haiku`      | dependency checks, lint/format, log parsing, boilerplate scaffolding                                                                                     |

### 3. Domain Parallel Patterns

When implementing features across domains, spawn parallel agents:

- **Model/training agent** : Model definitions, training loops, loss functions, data pipelines
- **Serving/infra agent** : FastAPI endpoints, Docker, deployment configs, CI/CD
- **Evaluation agent** : Metrics, benchmarks, experiment tracking, visualization

Each agent owns their domain. No file overlap.

### 4. Self-Improvement Loop

- After ANY correction from the user: update 'tasks/lessons.md" with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project

### 5. Verification Before Done

- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 6. Demand Elegance (Balanced)

- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes - don't over-engineer
- Challenge your own work before presenting it

### 7. Autonomous Bug Fixing

- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests - then resolve them
- Zero context switching required from the user
- Go fix failing CI tests without being told how
- Record the bugs, causes, tried solution, and actual fixation in clinical_llm_finetuning/docs/bugs-and-fixes.md

### 8. Version Control

- Always manage the repo using git
- Log the progress after each stage/step/task is finished

## Task Management

1. **Plan First**: Write plan to "tasks/todo.md' with checkable items
2. **Verify Plan**: Check in before starting implementation
3. **Track Progress**: Mark items complete as you go
4. **Explain Changes**: High-level summary at each step
5. **Document Results**: Add review section to 'tasks/todo.md"
6. **Capture Lessons**: Update "tasks/lessons.md' after corrections

## Core Principles

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes, Senior developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.
