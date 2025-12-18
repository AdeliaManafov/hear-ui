# Tables Folder

Use this folder to keep reusable LaTeX table snippets and optional data sources.

## Recommended Pattern
- Create small `.tex` files per table (keeps main paper clean):
  - `coverage_summary.tex` — overall test/coverage summary
  - `api_endpoints.tex` — REST endpoints overview
  - `patient_validation.tex` — 5-case validation results
  - `coverage_by_module.tex` — module-level coverage breakdown
- Include in `FINAL_REPORT.tex` with:
```latex
% Example
\input{tables/coverage_summary}
```

## Optional: CSV Sources
If you prefer to generate tables from CSV files:
- Put CSVs here (e.g., `coverage_by_module.csv`)
- Use `csvsimple` or `pgfplotstable` packages in LaTeX to render.

## Example Snippet
Create `coverage_summary.tex` with:
```latex
\begin{table}[h]
\centering
\caption{Testing Coverage}
\label{tab:testing}
\begin{tabular}{@{}lll@{}}
\toprule
\textbf{Level} & \textbf{Tests} & \textbf{Coverage} \\
\midrule
Unit Tests & 202 & 72\% \\
Integration Tests & 48 & API + DB \\
E2E Tests (Playwright) & 18 & Frontend \\
\textbf{Total} & \textbf{268} & \textbf{72\%} \\
\bottomrule
\end{tabular}
\end{table}
```

Keep tables focused, single-purpose, and referenced from the text.