# JSC370 — HW5 + Final Project Concrete Plan (revised)

Both are due **April 26, 2026 (11:59 pm)**. Today is April 19, 2026 — **7 days out**.

> Revision history: initial plan drafted and self-checked; 8 resolutions applied below (explicit `render` allowlist, CV CSV round-trip, self-contained removal, dual-format orchestration, figure cross-ref correction, Fig 2 control locked, stale HTML cleanup, time budget adjusted).

## Strategy / Ordering Rationale

HW5 *requires* a live GitHub Pages website to host the 3 interactive plots. So although the task says "finish HW5, then finish the final project," in practice the build order interleaves:

1. **Phase 0–2 = HW5 deliverable.** Minimum viable website + 3 Plotly figures + deploy. Once live, HW5 is submittable.
2. **Phase 3–7 = Final project layering.** Expand written report, generate PDF, polish landing page, record presentation, submit.

This keeps HW5 unblockable early in the week and leaves the heavier writing/modeling work for the later days.

## Decisions locked in (flag if you disagree)

- **Repo name stays `JSC370-Midterm-Proj`.** Live URL: `https://shifosss.github.io/JSC370-Midterm-Proj/`. Renaming creates churn and doesn't change correctness.
- **GitHub Pages source: `main` branch, `/docs` folder.** Single-branch workflow, easier than `gh-pages` publish. Matches standard Quarto website with `output-dir: docs`.
- **Theme: `darkly`** (match professor's example for visual consistency).
- **Interactive plots live on a dedicated `viz.qmd` page**, not inline in the report. Keeps the downloadable PDF clean. Spec explicitly allows either placement.
- **PDF strategy:** `writing-report.qmd` declares both `html` and `pdf` formats. Report figures are already static PNGs from the pipeline — no Kaleido required. `viz.qmd` stays HTML-only.
- **Site `render` scope is an explicit allowlist** in `_quarto.yml`: `[index.qmd, writing-report.qmd, viz.qmd, about.qmd]`. `option-c.qmd` is NOT rendered into the site (it lives on GitHub as the full pipeline and is linked, not served).
- **HTML format on the site is NOT `self-contained`.** A multi-page Quarto site needs shared `site_libs/`; `self-contained: true` inlines assets and breaks navigation. The downloadable PDF is inherently standalone.
- **Figure 2 filter control = state dropdown** (more intuitive than rural-pop slider; maps cleanly to the diabetes-belt narrative).

---

## Phase 0 — Website scaffolding  *(≈1 h)*

**Goal: a multi-page Quarto site renders locally and the skeleton is ready to host HW5.**

- [x] Create `_quarto.yml` at repo root:
  - `project.type: website`
  - `project.output-dir: docs`
  - `project.render: [index.qmd, writing-report.qmd, viz.qmd, about.qmd]` *(explicit allowlist so `option-c.qmd` does not auto-render into the site)*
  - `website.title: "JSC370: Clinical Trial Access Gap for Type 2 Diabetes"`
  - Navbar left: Home / Report / Interactive Viz / About
  - Navbar right: GitHub icon → repo URL
  - Page footer with copyright
  - `format.html`: theme `darkly`, `toc: true`, `toc-depth: 3`, `css: styles.css` *(no `self-contained`)*
- [x] Create `index.qmd` stub (filled in later): title, 1-paragraph abstract, placeholder buttons for Report / Interactive Viz / PDF / Presentation / GitHub.
- [x] Create `about.qmd`: Chen Zhang (AlexZ), JSC370, project context, data sources, acknowledgements.
- [x] Create `styles.css` adapted from professor's example (heading sizes, centered images).
- [x] Add to `.gitignore`: `.quarto/`, `/_site/` (safety). **Keep `docs/` tracked.**
- [x] Git-rm the stale root-level HTML renders: `writing-report.html` and `option-c-trial-access/product/option-c.html` *(will be regenerated into `docs/` or linked via GitHub instead)*.
- [x] Local verify: `quarto render` → `docs/index.html` opens cleanly; navbar links all work.

## Phase 1 — HW5 interactive figures (`viz.qmd`)  *(≈3–4 h)*

Spec'd in `spec-hw5.md`. Data already on disk.

- [x] Create `viz.qmd` with header note: *"Figures 1, 2, 3 on this page are interactive."* (required for the Quercus submission line).
- [x] **Figure 1 — Choropleth (map).** Plotly `choropleth` on US states, dropdown toggling color layer: diabetes age-adjusted prevalence / trials per 100k / coverage residual / industry-sponsor share. Hover shows all four metrics + counts. Data: `state_modeling_final.csv`. Caption + 2–3 sentence description beneath.
- [x] **Figure 2 — Histogram (distribution).** Plotly histogram of nearest-site distance (km) for zero-site counties, with a **state dropdown** filter. Data: `county_modeling_final.csv` filtered to zero-site rows. Caption + 2–3 sentence description.
- [x] **Figure 3 — Scatter (bivariate).** Plotly scatter of county diabetes prevalence (y) vs. log distance to nearest site (x), colored by poverty rate, sized by log population, with Medicaid-expansion filter. Hover: county, state, FIPS, prevalence, distance, poverty, endocrinologist density. Caption + 2–3 sentence description.
- [x] Use `execute.echo: false` so no code chunks appear in rendered output.
- [x] Local render; verify interactivity (hover, dropdown, filter).

## Phase 2 — GitHub Pages deploy  *(≈30 min)* — **HW5 goes live here**

- [x] Commit `docs/` output on `main`.
- [x] GitHub → Settings → Pages → source = `main` / `/docs`. Save.
- [x] Wait ~2–5 min, visit `https://shifosss.github.io/JSC370-Midterm-Proj/`.
- [x] Sanity check (incognito): all three Plotly figures render, hovers and dropdowns work, captions present, "Figures 1, 2, 3 are interactive" note visible.
- [x] Update `README.md` top: live URL, "HW5 interactive figures live at `/viz.html`."
- [x] **HW5 is now submittable.** Capture: live URL + interactive-figure line for Quercus.

## Phase 3 — Expand `writing-report.qmd` to final structure  *(≈6–8 h)*

Current state: Introduction, Methods, Preliminary Results, Summary (preliminary), References. Missing **final Results** and **Conclusions and Summary** per the spec.

### 3a — Unblock the CV comparison table (data provenance)

Verified: `option-c.qmd` (lines 2534–2565) already computes the SES-only vs. Full CV comparison; numbers are `print`'d and drawn into `model_comparison_cv.png` but **never saved as CSV**.

- [x] In `option-c.qmd`, add one line after `model_comparison = pd.DataFrame(...)`:
  ```python
  model_comparison.to_csv(TEMP / "model_comparison_cv.csv", index=False)
  ```
- [x] Re-render `option-c.qmd` once to produce the CSV.

### 3b — Rewrite report content

- [x] Rename "Preliminary Results" to **"Results"**; keep descriptive Aim 1 content (state maps, coverage residual, Tables 1–3, county distance, endocrinologist vs. trials).
- [x] Add **Aim 2 modeling results** subsection:
  - Silent Python chunk loads `product/data/modified/temp/model_comparison_cv.csv` and renders a publication-ready Markdown table (Elastic Net / RF / XGBoost × SES-only vs. Full, with R² / RMSE / MAE and deltas).
  - Embed `model_comparison_cv.png`, `shap_summary_plot.png`, `shap_group_importance.png`, `rf_permutation_importance.png`, `elastic_net_coefficients.png` with captions.
  - Narrative: does adding trial-access features measurably improve prediction? (Hypothesis said no.)
- [x] Replace "For the final deliverable, the plan is…" with a **Conclusions and Summary** section: hypothesis verdict, mechanistic framing (infrastructure-driven placement, SES redundancy), limitations (cross-sectional, ecological, zero-inflated county trial density, cumulative registry vs. cross-sectional burden, Haversine ≠ drive time), bigger-picture takeaway.
- [x] Set `execute: { echo: false, warning: false, message: false }` globally so no raw code/output leaks into the rendered report.
- [~] Trim to **6–7 single-spaced pages**. _Current state: 13 pages after rewrite + one trim pass (dropped endo-trial scatter, collapsed columns → `layout-ncol=2`). The overage is driven by single-column image layout with 6 figures + 4 tables; content density matches a publication-ready report. Flagged; grader-dependent whether to trim further._
- [x] Verify image paths resolve from the new rendered location (`docs/writing-report.html` → paths still relative to repo root).
- [x] Add top-of-report note linking to interactive versions:
  > *"Interactive versions of Figure 1 (choropleth), Figure 3 (county distance), and Figure 4 (endocrinologist vs. trials) are available on the [Interactive Visualizations page](viz.html)."*

## Phase 4 — PDF rendering  *(≈1 h)*

- [x] Add dual format in `writing-report.qmd` frontmatter (HTML is **not** self-contained; PDF is standalone by nature):
  ```yaml
  format:
    html:
      toc: true
      toc-depth: 3
      css: styles.css
    pdf:
      documentclass: article
      geometry: margin=1in
      fig-pos: "H"
  ```
- [x] Dual render sequence (single command):
  ```bash
  quarto render writing-report.qmd --to all
  ```
  *(the plain `quarto render` used for the site only produces the first format; `--to all` on the report file forces both HTML and PDF.)*
- [x] Confirm both `docs/writing-report.html` and `docs/writing-report.pdf` land in place.
- [x] Link PDF from `index.qmd` as a "Download the report (PDF)" button.

## Phase 5 — Landing page + repo hygiene  *(≈1 h)*

- [x] Flesh out `index.qmd`:
  - Project title + one-paragraph abstract (~150 words).
  - 3–4 headline findings as bullets (e.g., "73.4% of U.S. counties host no diabetes trial site; median travel distance 58.4 km").
  - Card/button row: Read full report | Interactive visualizations | Download PDF | Watch presentation | GitHub repo.
  - Short "Full computational pipeline" link → `option-c.qmd` raw file on GitHub (keeps it accessible without putting it on the site).
- [x] Update `README.md`:
  - Live website URL at the top.
  - One-sentence project description.
  - API / data source links (ClinicalTrials.gov v2, CDC PLACES/Socrata, Census ACS 2022, FCC Census API, NPI Registry, Census Gazetteer).
  - Reproduction steps: clone → `conda env create -f jsc370.full.yml` → add `.env` with `CENSUS_API_KEY` → `quarto render` (site) → `quarto render writing-report.qmd --to all` (PDF).
  - Link to the HW5 interactive page and the PDF.
- [x] Reproducibility spot-check: fresh clone to `/tmp`, follow README, confirm site renders end-to-end with no absolute paths.
- [x] Confirm `option-c-trial-access/product/data/modified/*.csv` is tracked in git (checklist item 5). Raw API pulls stay gitignored; reproduction instructions live in the notebook.

## Phase 6 — 5-minute recorded presentation  *(≈2–3 h) — **needs AlexZ***

Blocking: voice + screen recording is yours. Once the file exists I will embed the link.

- [ ] Script (target ~5:00): summary (30s) → research questions (30s) → methods highlights (60s) → Aim 1 descriptive results (60s) → Aim 2 modeling results (60s) → interactive viz demo (45s) → conclusions + limitations (15s).
- [ ] Screen-record a walkthrough of the live site in a clean browser window. QuickTime or OBS. Keep cursor visible.
- [ ] Upload as unlisted YouTube video (easiest embedding + no Quercus size limits).
- [ ] Embed the link in `index.qmd` ("Watch presentation") and add to `README.md`.

## Phase 7 — Submission  *(≈30 min) — **needs AlexZ***

Blocking: Quercus submission uses your credentials.

- [ ] Final `quarto render` on the whole site; then `quarto render writing-report.qmd --to pdf` to refresh the download; commit `docs/` and push `main`.
- [ ] Incognito-tab verify: homepage, Report, Interactive Viz, About, PDF download, video link.
- [ ] Quercus (final project): repo URL, website URL, video link.
- [ ] Quercus (HW5): website URL (specifically `viz.html`) + line "Figures 1, 2, 3 on the Interactive Visualizations page are interactive."

---

## Figure cross-reference (report ↔ HW5)

| Written report | HW5 interactive analogue |
|---|---|
| Fig 1 — state prevalence / trial-density tile maps | HW5 Fig 1 — choropleth toggle |
| Fig 2 — coverage residual outlier bars | *(static only; not duplicated on viz page)* |
| Fig 3 — county distance histogram | HW5 Fig 2 — histogram with state dropdown |
| Fig 4 — endocrinologist vs. trial density scatter | HW5 Fig 3 — scatter with poverty/Medicaid filter |

## Risks & open questions

1. **Page count creep.** Adding Results + Conclusions to a report that's already ~4 pages may push past 7. Phase 3 has an explicit trim step — budget for it.
2. **GitHub Pages propagation.** First deploy can take 5–15 min. Don't leave this to the last hour.
3. **Plotly in PDF.** Solved by design: interactives live on HTML-only `viz.qmd`; the PDF report uses existing static PNGs.
4. **Kaleido not installed.** Only matters if we later decide to embed Plotly in the PDF. Not on the critical path.
5. **Video hosting.** Unlisted YouTube is the default — confirm you're OK with that vs. a Google Drive link or direct Quercus upload.
6. **PDF engine presence.** `quarto render --to pdf` needs a LaTeX stack (TinyTeX is fine). If absent, `quarto install tinytex` on first PDF render.

## Status at handoff (2026-04-20)

**Live and verified:** <https://shifosss.github.io/JSC370-Midterm-Proj/>

- ✅ Phases 0–5 complete and deployed (scaffold → HW5 figures → Pages → report → PDF → landing/README).
- ⏸️ Phase 6 waits on AlexZ's screen-recording + YouTube upload. Once you have the unlisted URL, tell me and I will embed it in `index.qmd` + `README.md` and push.
- ⏸️ Phase 7 waits on the Quercus submission (your credentials).

**HW5 submission line for Quercus** (ready to paste):
> Link: <https://shifosss.github.io/JSC370-Midterm-Proj/viz.html>
> Figures 1, 2, and 3 on the Interactive Visualizations page are interactive.

**Final-project submission fields for Quercus** (ready once Phase 6 is recorded):
> Repo: <https://github.com/shifosss/JSC370-Midterm-Proj>
> Website: <https://shifosss.github.io/JSC370-Midterm-Proj/>
> Video: _[your unlisted YouTube link]_

**One residual trade-off flagged:** the PDF is 13 pages against a spec target of "about 6–7". The content is publication-dense (6 figures, 4 tables, four sections) and single-column. Shrinking further would mean either (a) cutting Aim 2 figures, or (b) moving to a two-column LaTeX template — both are risk/reward trade-offs I held off on without your sign-off.

## Total time budget

~14–18 hours spread across 5–6 active days. Still comfortable margin against April 26.
