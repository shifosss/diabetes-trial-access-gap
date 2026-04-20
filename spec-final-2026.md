# Final Project Spec — JSC370 2026

## Source
`final-2026.pdf` (due **April 26, 2026**).

## Grading Weights
| Component | Weight |
|---|---:|
| 5-minute recorded presentation | 10% |
| GitHub website | 10% |
| Written report (on website + downloadable PDF) | 80% |

Report target length: **6–7 pages single-spaced**, including figures and tables.

## What the Assignment Requires

### 1. Content and Scope
- **Dataset:** continue with the midterm dataset (Option C — Type 2 diabetes clinical trial access). No switch notification is needed.
- **Modeling requirement:** at least one predictive or inferential method from the course — **XGBoost, Random Forest, GAM, or LDA** — is mandatory. Methods learned elsewhere (deep learning, k-means, PCA) are allowed only if compared against a course method.
- **Prediction workflows must include:**
  - Feature engineering (variable creation).
  - Variable/feature importance.
  - Train/test splits (i.e., honest generalization estimates).
- **Statistical detail:** for each model, describe briefly what it is, its hyperparameters, the train/validation/test protocol, and the evaluation metrics (R², RMSE, MAE, ROC/AUC, etc.).
- **Forbidden in the report:** raw code chunks and unformatted output. Tables and figures must be captioned, numbered, and publication-ready.

### 2. Required Report Sections
1. **Introduction** — background, narrative, formulated question(s) / hypothesis(es). References are not required but a narrative is.
2. **Methods** — data provenance, cleaning, wrangling, EDA tooling, model descriptions, train/test protocol, evaluation statistics.
3. **Results** — final publication-ready tables and figures; may refer the reader to the website for interactive versions.
4. **Conclusions and Summary** — interpretation, bigger-picture framing, limitations.

### 3. Deliverables
1. **5-minute recorded video** walking through the website and main findings. Upload to Quercus or link from the website.
2. **GitHub repo + GitHub website** — the website must host:
   - `index.html` project summary (or full project).
   - Interactive visualizations (HW5, 3 plots, with captions). Inline or a separate `viz.html`.
   - A "Download the report" link to the PDF.
   - A link to the GitHub repo.
3. **Written report** — embedded tables and figures, also downloadable as PDF. If the full report lives on the website, a simpler PDF is acceptable but must be present and link back to the website.
4. **README.md** in the repo root with:
   - A link to the website.
   - Brief description / title.
   - Link(s) to the API(s) and any data sources.
5. **Data folder** (`data/`) if shipping saved data. If only using APIs, API usage must be clearly instructed in code.
6. **Reproducibility:** no paths to files not in the repo; full pipeline must run end-to-end for a grader.

### 4. Website Must Visibly Work
Figures and interactive plots must actually render on the public URL (not just locally).

## Current State of the Repo (inventory)

**Already done:**
- Pipeline report: `option-c-trial-access/product/option-c.qmd` — full 8-section workflow (acquisition → flattening → enrichment → state coverage → county extension → EDA → modeling).
- Written report: `writing-report.qmd` — has Introduction, Methods, Preliminary Results, Summary, References. Two formulated aims (descriptive + modeling).
- Model-ready datasets exported: `state_modeling_final.csv`, `county_modeling_final.csv`.
- Modeling already run in the pipeline: Elastic Net, Random Forest, XGBoost with 5-fold CV and SHAP.
- Static figures for the report (tile maps, coverage residuals, county distance histogram, SHAP summary, permutation importance, Elastic Net coefficients, model comparison CV).
- README exists with project description, data sources, reproduction steps.

**Not yet done / gaps:**
- No GitHub Pages website. README links to the repo but no live site URL.
- No `index.html` / `index.qmd` landing page.
- No interactive visualizations (HW5).
- No downloadable PDF of the report (currently only the self-contained HTML).
- No 5-minute recorded presentation.
- Written report stops at "Preliminary Results" + a "For the final deliverable, the plan is…" section — the **Results** (final) and **Conclusions** sections have not been written from the modeling outputs that now exist. The report needs to be expanded/rewritten from a midterm-style write-up into the final structure required above.
- README does not link to a live website (it can't until one exists).

## Plan

### Phase 1 — Finalize written report content
1. **Absorb modeling outputs into the Results section.** The pipeline has already produced SHAP, permutation importance, Elastic Net coefficients, and CV comparison plots. Rewrite the current "Preliminary Results + For the final deliverable, the plan is…" closer into:
   - **Results:** baseline-vs-augmented comparison table (CV R² / RMSE / MAE for SES-only vs. SES+trial-access, across Elastic Net / RF / XGBoost); feature importance figures; the main answer to Aim 2.
   - **Conclusions and Summary:** interpret whether trial-access features add predictive signal beyond SES (hypothesis said they would not), mechanistic discussion, limitations (cross-sectional, ecological inference, trial registry is cumulative, zero-inflated county trial density).
2. **Trim for 6–7 single-spaced pages.** Current content is close but needs editing once the new Results/Conclusions land.
3. **Publication-ready tables and figures.** Keep Tables 1–3 (coverage extremes, county access summary). Add a CV comparison table and a feature-importance figure or table from Aim 2.
4. **Strip any remaining code chunks / raw output** from the rendered report output (QMD can still contain code cells but they must be `echo: false`).

### Phase 2 — Convert to a Quarto website
1. Add `_quarto.yml` at repo root with `project: { type: website }`, output dir `docs/` or `_site/`.
2. Create `index.qmd` — short summary, photo/plot, links to full report, interactive viz, PDF download, GitHub repo.
3. Include `writing-report.qmd` as the full report page.
4. Create `viz.qmd` for the three HW5 interactive plots (see `spec-hw5.md`).
5. Produce `writing-report.pdf` via `format: pdf` (or render once as PDF), place it under `docs/` and link from `index.qmd` as "Download the report."

### Phase 3 — GitHub Pages + repo hygiene
1. Enable GitHub Pages serving from `/docs` on `main` (or use `quarto publish gh-pages`).
2. Update `README.md` with: live website URL, brief project description, API links (ClinicalTrials.gov v2, CDC PLACES/Socrata, Census ACS, FCC Census API, NPI Registry, Census Gazetteer), link to the PDF.
3. Confirm the `data/` layout matches the spec — model-ready CSVs live under `option-c-trial-access/product/data/modified/`; raw API pulls are gitignored but reproducible via the notebook, which is acceptable under checklist item 5 as long as API instructions are in the code.
4. Verify reproducibility: fresh checkout + `conda env create` + `.env` with `CENSUS_API_KEY` + `quarto render` on every page. No absolute paths.

### Phase 4 — Record the presentation
1. Walk through the website live for ~5 minutes: project summary → research questions → methods highlights → headline results → interactive figure demo → conclusions.
2. Host the video (unlisted YouTube, Google Drive, or upload directly to Quercus).
3. Add the video link to `index.qmd`.

### Phase 5 — Submission
- Quercus: repo URL, website URL, interactive-figure statement (for HW5), and the video link/file.
- Verify live website loads, figures render, "Download the report" link works, and README is current.

## Deliverables Checklist

- [ ] Rewritten `writing-report.qmd` with final Results + Conclusions sections.
- [ ] Report compiled to both HTML (on website) and downloadable PDF.
- [ ] `index.qmd` landing page with summary, links, and download button.
- [ ] `viz.qmd` (or inline) with three interactive figures (HW5 deliverable).
- [ ] `_quarto.yml` configured for a multi-page website.
- [ ] GitHub Pages enabled; live URL verified.
- [ ] `README.md` updated with website URL, description, API links.
- [ ] 5-minute recorded presentation uploaded, link embedded.
- [ ] Repo reproducible end-to-end (no hardcoded absolute paths, env setup documented).
- [ ] Quercus submission: website URL, repo URL, video link, HW5 interactive-figure note.

## Risks and Open Questions

- **Trimming to 6–7 pages.** Current written report already runs long once the Results and Conclusions are expanded. Expect to cut some methods detail and move it to the pipeline report, which lives on the website and is linked rather than submitted.
- **PDF of a report with Plotly figures.** Plotly renders to static PNG in PDF by default (via Kaleido). Either accept static versions in the PDF and keep interactivity for the HTML page, or maintain two source variants; recommended: static in PDF, interactive on website, captions identical.
- **Video hosting.** Confirm whether a Quercus upload or an external link is preferred; default to an unlisted YouTube link embedded on `index.qmd`.
- **Website URL format.** `https://shifosss.github.io/JSC370-Midterm-Proj/` is the default; decide whether to rename the repo (e.g., `JSC370-finalproject`) or keep the midterm name and document clearly.
