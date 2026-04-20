# HW5 Spec — Interactive Visualizations

## Source
`hw5-2026.pdf` (due **April 26, 2026, 11:59 pm** — bundled with final project).

## What the Assignment Requires (15 pts)

1. **Three different interactive visualizations** built with week-11 tools (Plotly/Leaflet/etc.). "Different" is emphasized — not three flavors of the same chart. Suggested variety: a map, a histogram, a boxplot (the PDF's own examples).
2. **Data source:** must use the final-project dataset (i.e., Option C — Type 2 diabetes clinical trial access).
3. **Hosted on GitHub Pages.** The figures must render on the live website, not only locally.
4. **Each figure needs:**
   - A caption.
   - A brief summary describing what it shows.
   - Graded on **visual style, caption, and description**.
5. **Placement:** either embedded inside the final report OR on a separate page (e.g., `viz.html`).
6. **Quercus submission:**
   - Link to where the plots live on the website.
   - A line stating which figures are interactive (e.g., "Figures 1, 2, 3 are interactive").

## Inputs Already Available in This Repo

- `option-c-trial-access/product/data/modified/state_modeling_final.csv` — state-level, one row per state, has burden / trial density / coverage residual / industry share.
- `option-c-trial-access/product/data/modified/county_modeling_final.csv` — 3,221 counties with FIPS, diabetes prevalence, trial density, log distance to nearest site, SES covariates.
- Static EDA PNGs (`discover/results/*.png`) — these are the non-interactive analogues the interactive plots should supersede or complement.
- Model outputs (SHAP, permutation importance, Elastic Net coefficients) under `product/results/`.

## Plan — Three Interactive Figures

Picked to be structurally different (map, distribution, bivariate) and to map cleanly onto the report's Aim 1 / Aim 2 narrative.

### Figure 1 — State Choropleth: Burden vs. Trial Density (Map)
- **Type:** Plotly `choropleth` on US states, with a dropdown or toggle to switch the color variable between: diabetes age-adjusted prevalence, trials per 100k, coverage residual, industry-sponsor share.
- **Source:** `state_modeling_final.csv`.
- **Hover:** state name, all four metrics, trial count, site count.
- **Caption:** "State-level comparison of diabetes burden and trial-site density. Switch layers to see where high burden coincides with low trial coverage."
- **Purpose:** interactive replacement for the two side-by-side tile maps in the written report (Aim 1 descriptive result).

### Figure 2 — County Histogram with Subgroup Filter (Distribution)
- **Type:** Plotly histogram of distance to nearest trial site (km) for counties with no local site, with a state filter (dropdown or slider on rural-population share).
- **Source:** `county_modeling_final.csv` subset to zero-site counties.
- **Hover:** bin range, count, mean distance in bin.
- **Caption:** "Distance from a no-site county to the nearest diabetes trial. Filter by state or rurality to see how access gaps shift."
- **Purpose:** interactive version of the existing `county_distance_histogram.png`; surfaces the 58.4 km median / 24% > 100 km headline stat.

### Figure 3 — County Scatter / Bivariate with Brushing (Bivariate)
- **Type:** Plotly scatter of county diabetes prevalence (y) vs. log distance to nearest site (x), colored by poverty rate, sized by population, filter by Medicaid expansion status.
- **Source:** `county_modeling_final.csv`.
- **Hover:** county name, state, FIPS, prevalence, distance, poverty rate, endocrinologists per 100k.
- **Caption:** "Does distance to the nearest trial track county diabetes burden once poverty is accounted for? Hover and filter to explore."
- **Purpose:** motivates Aim 2 (does access add predictive signal?) and replaces the static `county_endo_vs_trials.png`.

## Implementation Plan

1. **Add a viz chunk** to either a new `viz.qmd` (separate page) or a new `## Interactive Visualizations` section in `writing-report.qmd`. Prefer a separate `viz.qmd` so the main report PDF (required by the final-project spec) stays clean.
2. **Code strategy:** Plotly Python (`plotly.express` + `plotly.graph_objects`). For the choropleth, use `locationmode="USA-states"`; for the county map option, use the Plotly-bundled GeoJSON keyed by FIPS.
3. **Figure captions and summaries** must live in the QMD below each figure; 2–3 sentences each, describing what the reader is looking at and the headline takeaway.
4. **Quarto publishing:** convert the project to a Quarto website (`_quarto.yml` with `project: { type: website }`), rendering `index.qmd` (summary), `writing-report.qmd` (main report), and `viz.qmd` (interactive page).
5. **GitHub Pages:** publish the rendered `_site/` via `quarto publish gh-pages` OR the `docs/` branch pattern. Verify the live URL loads all three plots.
6. **Sanity check:** open the deployed URL in an incognito window — confirm plots render (no broken CDN, no missing data paths), confirm captions are visible, and confirm the "Figures X, Y, Z are interactive" note is present.

## Deliverables Checklist

- [ ] Three distinct interactive figures (map, histogram, scatter) with captions + summaries.
- [ ] Figures rendered on a public GitHub Pages URL.
- [ ] Report/page identifies which figures are interactive.
- [ ] Quercus submission contains the live URL and the interactive-figure list.

## Open Questions

- Whether to put interactive plots inline in `writing-report.qmd` or on a dedicated `viz.qmd` — the final-project spec explicitly allows either; recommend a dedicated page so the downloadable PDF stays slim.
- Whether county-level map (choropleth on 3,221 counties) should replace or supplement the state map — county map is high-value but Plotly render time is significant; keep state map as primary, add county map only if time permits.
