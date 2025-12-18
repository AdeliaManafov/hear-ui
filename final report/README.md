# HEAR-UI Final Report

This directory contains the ACL conference-style Final Report for the HEAR-UI project.

## Files

### Main Document
- **FINAL_REPORT.tex** - Complete LaTeX source for the final report
- **acl.sty** - ACL conference style file (required)
- **acl_natbib.bst** - Bibliography style for ACL format (required)
- **custom.bib** - Bibliography with all cited references

### Compiled Documents
- **FINAL_REPORT.pdf** - Compiled final report (generate with pdflatex)

### Folders
- **figures/** - Contains figures and diagrams for the report
- **tables/** - Reusable LaTeX table snippets (e.g., `api_endpoints.tex`, `coverage_summary.tex`). Include via `\input{tables/coverage_summary}`.

## Compilation Instructions

### Prerequisites
```bash
# Install LaTeX distribution
# macOS:
brew install --cask mactex

# Ubuntu/Debian:
sudo apt-get install texlive-full
```

### Compile the Report

#### Using pdflatex (Recommended)
```bash
cd "final report"

# Run pdflatex sequence
pdflatex FINAL_REPORT.tex
bibtex FINAL_REPORT
pdflatex FINAL_REPORT.tex
pdflatex FINAL_REPORT.tex

# View the PDF
open FINAL_REPORT.pdf  # macOS
```

#### Using latexmk (Automated)
```bash
latexmk -pdf -pvc FINAL_REPORT.tex
```

### Clean Auxiliary Files
```bash
rm -f *.aux *.log *.bbl *.blg *.out *.toc *.synctex.gz
```

## Report Structure

1. **Abstract** (100-200 words)
2. **Introduction** (Problem statement, RQs, contributions)
3. **Related Work** (XAI, AI in healthcare, cochlear implants)
4. **System Architecture** (Backend, Frontend, Database)
5. **Data and Preprocessing** (Dataset, features, pipeline)
6. **Machine Learning Method** (Model selection, SHAP)
7. **Evaluation** (Testing, CI/CD, validation)
8. **Results and Discussion** (Findings, limitations)
9. **Deployment** (Docker, reproducibility)
10. **Conclusion** (Summary, future work)

## Statistics Included

- **268 tests** (202 backend, 48 API, 18 E2E)
- **72% code coverage**
- **17 REST API endpoints**
- **68 ML features**
- **5 validated test patients**
- **80+ git commits**
- **7 CI/CD workflows**
- **< 200ms prediction latency**

## Citations

13+ key references including Lundberg & Lee (2017) SHAP, Rudin (2019), Topol (2019), Wilson & Dorman (2008), Lenarz (2018), and more.

All citations in custom.bib with APA/ACL formatting.

## Contact

- Adelia Manafov - manafova@students.uni-marburg.de
- Artem Mozharov - mozharoa@students.uni-marburg.de
