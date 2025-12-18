# HEAR-UI Literaturverzeichnis & Referenzen

> **Projekt:** Cochlear Implant Success Prediction System  
> **Zweck:** Dokumentation aller verwendeten Technologien, Frameworks, wissenschaftlicher Arbeiten und Methoden  
> **Stand:** 18. Dezember 2025

---

## Inhaltsverzeichnis

1. [Wissenschaftliche Grundlagen](#wissenschaftliche-grundlagen)
2. [Machine Learning & Explainable AI](#machine-learning--explainable-ai)
3. [Backend-Technologien](#backend-technologien)
4. [Frontend-Technologien](#frontend-technologien)
5. [Datenbank & Persistenz](#datenbank--persistenz)
6. [Testing & Qualitätssicherung](#testing--qualitätssicherung)
7. [DevOps & CI/CD](#devops--cicd)
8. [Standards & Best Practices](#standards--best-practices)
9. [Online-Ressourcen & Tutorials](#online-ressourcen--tutorials)

---

## 1. Wissenschaftliche Grundlagen

### Explainable AI (XAI)

**Lundberg, S. M., & Lee, S.-I. (2017)**  
*A Unified Approach to Interpreting Model Predictions*  
In: Advances in Neural Information Processing Systems 30 (NIPS 2017)  
URL: https://arxiv.org/abs/1705.07874  
**Verwendung:** SHAP (SHapley Additive exPlanations) als Basis für Feature-Importance-Analyse in HEAR-UI

**Molnar, C. (2022)**  
*Interpretable Machine Learning: A Guide for Making Black Box Models Explainable* (2nd Edition)  
URL: https://christophm.github.io/interpretable-ml-book/  
**Verwendung:** Theoretische Grundlage für Explainability-Strategien

**Ribeiro, M. T., Singh, S., & Guestrin, C. (2016)**  
*"Why Should I Trust You?": Explaining the Predictions of Any Classifier*  
In: Proceedings of the 22nd ACM SIGKDD (KDD '16)  
DOI: 10.1145/2939672.2939778  
**Verwendung:** LIME als alternative Erklärungsmethode (evaluiert, aber nicht implementiert)

---

### Medizinische Informatik & Clinical Decision Support

**Shortliffe, E. H., & Sepúlveda, M. J. (2018)**  
*Clinical Decision Support in the Era of Artificial Intelligence*  
JAMA, 320(21), 2199–2200  
DOI: 10.1001/jama.2018.17163  
**Verwendung:** Konzeptionelle Grundlage für klinische Entscheidungsunterstützungssysteme

**Topol, E. J. (2019)**  
*High-performance medicine: the convergence of human and artificial intelligence*  
Nature Medicine, 25(1), 44–56  
DOI: 10.1038/s41591-018-0300-7  
**Verwendung:** Vision für AI-gestützte Medizin, Ethik-Überlegungen

---

### Cochlear Implant Research

**Wilson, B. S., & Dorman, M. F. (2008)**  
*Cochlear implants: A remarkable past and a brilliant future*  
Hearing Research, 242(1-2), 3–21  
DOI: 10.1016/j.heares.2008.06.005  
**Verwendung:** Domain-Knowledge für Cochlea-Implantate

**Lenarz, T. (2018)**  
*Cochlear Implant – State of the Art*  
GMS Current Topics in Otorhinolaryngology, Head and Neck Surgery, 16  
DOI: 10.3205/cto000154  
**Verwendung:** Medizinischer Kontext für Erfolgsvorhersage-Modelle

---

## 2. Machine Learning & Explainable AI

### SHAP (SHapley Additive exPlanations)

**Lundberg, S. M. (2024)**  
*SHAP: A game theoretic approach to explain the output of machine learning models*  
GitHub Repository: https://github.com/shap/shap  
Version: 0.46.0 (verwendet in HEAR-UI)  
**Verwendung:** Feature-Importance-Berechnung in `/api/v1/explainer` Endpoint

**Python Package:**
```python
import shap
# Verwendung in: backend/app/core/shap_explainer.py
```

**Dokumentation:**
- Official Docs: https://shap.readthedocs.io/
- Tutorials: https://shap-lrjball.readthedocs.io/en/latest/examples.html

---

### Scikit-learn

**Pedregosa, F., et al. (2011)**  
*Scikit-learn: Machine Learning in Python*  
Journal of Machine Learning Research, 12, 2825–2830  
URL: https://jmlr.org/papers/v12/pedregosa11a.html  
**Verwendung:** LogisticRegression Modell, Pipeline, Preprocessing

**Buitinck, L., et al. (2013)**  
*API design for machine learning software: experiences from the scikit-learn project*  
In: ECML PKDD Workshop: Languages for Data Mining and Machine Learning  
arXiv: 1309.0238  
**Verwendung:** Model-Wrapper Design-Pattern in `app/core/model_wrapper.py`

**Python Package:**
```python
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
# Version: 1.5.2 (pinned in requirements.txt)
```

---

### Model Calibration

**Platt, J. (1999)**  
*Probabilistic Outputs for Support Vector Machines and Comparisons to Regularized Likelihood Methods*  
In: Advances in Large Margin Classifiers  
**Verwendung:** Kalibrierte Wahrscheinlichkeiten in Prediction-Outputs

**Niculescu-Mizil, A., & Caruana, R. (2005)**  
*Predicting Good Probabilities With Supervised Learning*  
In: Proceedings of the 22nd ICML  
DOI: 10.1145/1102351.1102430  
**Verwendung:** Validierung der Modell-Kalibrierung (0-100% Wahrscheinlichkeit)

---

## 3. Backend-Technologien

### FastAPI

**Ramírez, S. (2024)**  
*FastAPI: Modern, fast (high-performance), web framework for building APIs with Python*  
GitHub: https://github.com/fastapi/fastapi  
Version: 0.115.5 (verwendet in HEAR-UI)  
**Verwendung:** REST API für Predictions, Explainer, Patienten-Management

**Dokumentation:**
- Official Docs: https://fastapi.tiangolo.com/
- Tutorial: https://fastapi.tiangolo.com/tutorial/

**Key Features:**
- Automatische OpenAPI-Dokumentation (Swagger UI)
- Pydantic-basierte Request/Response-Validierung
- Async Support für performante API-Calls

**Python Package:**
```python
from fastapi import FastAPI, Depends, HTTPException
# Version: 0.115.5
```

---

### Pydantic

**Colvin, S., et al. (2024)**  
*Pydantic: Data validation using Python type annotations*  
GitHub: https://github.com/pydantic/pydantic  
Version: 2.10.3 (Pydantic v2)  
**Verwendung:** Data Models für API-Requests/Responses

**Migration Guide:**
- v1 → v2: https://docs.pydantic.dev/latest/migration/
- Breaking Changes dokumentiert in: `backend/README.md`

**Python Package:**
```python
from pydantic import BaseModel, Field, ConfigDict
# Version: 2.10.3 (Pydantic v2)
```

---

### SQLModel

**Ramírez, S. (2024)**  
*SQLModel: SQL databases in Python, designed for simplicity, compatibility, and robustness*  
GitHub: https://github.com/fastapi/sqlmodel  
Version: 0.0.22  
**Verwendung:** ORM für PostgreSQL-Datenbank, Pydantic-kompatible DB-Models

**Dokumentation:**
- Official Docs: https://sqlmodel.tiangolo.com/
- Tutorial: https://sqlmodel.tiangolo.com/tutorial/

**Python Package:**
```python
from sqlmodel import SQLModel, Field, Session, create_engine
# Version: 0.0.22
```

---

### Alembic

**Bayer, M. (2024)**  
*Alembic: Database migrations for SQLAlchemy*  
GitHub: https://github.com/sqlalchemy/alembic  
Version: 1.14.0  
**Verwendung:** Versionierte Datenbank-Migrationen

**Dokumentation:**
- Official Docs: https://alembic.sqlalchemy.org/
- Tutorial: https://alembic.sqlalchemy.org/en/latest/tutorial.html

**Python Package:**
```python
# Usage: backend/app/alembic/
# Config: backend/alembic.ini
```

---

## 4. Frontend-Technologien

### Vue.js 3

**You, E., et al. (2024)**  
*Vue.js: The Progressive JavaScript Framework*  
GitHub: https://github.com/vuejs/core  
Version: 3.5.13  
**Verwendung:** Frontend-Framework für HEAR-UI Web-Interface

**Dokumentation:**
- Official Docs: https://vuejs.org/
- Composition API: https://vuejs.org/guide/extras/composition-api-faq.html
- TypeScript Guide: https://vuejs.org/guide/typescript/overview.html

**NPM Package:**
```json
"vue": "^3.5.13"
```

**Key Features:**
- Composition API für modulare Komponenten
- Single-File Components (`.vue`)
- Reaktives Data-Binding
- TypeScript-First Design

---

### TypeScript

**Microsoft Corporation (2024)**  
*TypeScript: JavaScript with syntax for types*  
GitHub: https://github.com/microsoft/TypeScript  
Version: 5.6.3  
**Verwendung:** Type-Safe Frontend-Entwicklung

**Dokumentation:**
- Official Docs: https://www.typescriptlang.org/docs/
- Handbook: https://www.typescriptlang.org/docs/handbook/intro.html

**NPM Package:**
```json
"typescript": "~5.6.2"
```

---

### Vite

**You, E., et al. (2024)**  
*Vite: Next Generation Frontend Tooling*  
GitHub: https://github.com/vitejs/vite  
Version: 6.0.1  
**Verwendung:** Build-Tool & Development-Server

**Dokumentation:**
- Official Docs: https://vite.dev/
- Vue Plugin: https://github.com/vitejs/vite-plugin-vue

**NPM Package:**
```json
"vite": "^6.0.1"
```

**Vorteile:**
- Instant Hot Module Replacement (HMR)
- Optimiertes Production-Build
- Native ES-Modules Support

---

### Vuetify

**Leider, J., et al. (2024)**  
*Vuetify: Material Design Component Framework for Vue.js*  
GitHub: https://github.com/vuetifyjs/vuetify  
Version: 3.7.5  
**Verwendung:** UI-Komponenten-Bibliothek

**Dokumentation:**
- Official Docs: https://vuetifyjs.com/
- Components: https://vuetifyjs.com/en/components/all/

**NPM Package:**
```json
"vuetify": "^3.7.5"
```

---

## 5. Datenbank & Persistenz

### PostgreSQL

**PostgreSQL Global Development Group (2024)**  
*PostgreSQL: The World's Most Advanced Open Source Relational Database*  
Official Website: https://www.postgresql.org/  
Version: 12 (verwendet in HEAR-UI)  
**Verwendung:** Relationale Datenbank für Patienten, Predictions, Feedback

**Dokumentation:**
- Official Docs: https://www.postgresql.org/docs/12/
- SQL Reference: https://www.postgresql.org/docs/12/sql.html

**Docker Image:**
```yaml
image: postgres:12
```

**Key Features:**
- JSONB für semi-strukturierte Daten
- Full-Text-Search (trigram, unaccent)
- ACID-Compliance

---

### psycopg (PostgreSQL Adapter)

**Di Gregorio, F., et al. (2024)**  
*psycopg: PostgreSQL database adapter for Python*  
GitHub: https://github.com/psycopg/psycopg  
Version: 3.2.3  
**Verwendung:** Python-DB-Connector (async-fähig)

**Python Package:**
```python
import psycopg
# Version: 3.2.3
```

---

## 6. Testing & Qualitätssicherung

### pytest

**Krekel, H., et al. (2024)**  
*pytest: A mature full-featured Python testing tool*  
GitHub: https://github.com/pytest-dev/pytest  
Version: 8.3.4  
**Verwendung:** Unit- & Integration-Tests für Backend

**Dokumentation:**
- Official Docs: https://docs.pytest.org/
- Fixtures: https://docs.pytest.org/en/stable/fixture.html

**Python Package:**
```python
import pytest
# Version: 8.3.4
# Usage: backend/app/tests/
```

**Test-Statistics:**
- 268 Tests (98.5% Pass-Rate)
- 72% Code Coverage (produktiver Code)

---

### pytest-cov (Coverage)

**Benedikt Böhm, et al. (2024)**  
*pytest-cov: Coverage plugin for pytest*  
GitHub: https://github.com/pytest-dev/pytest-cov  
Version: 6.0.0  
**Verwendung:** Test-Coverage-Reporting

**Python Package:**
```python
# Usage: pytest --cov=app --cov-report=html
# Config: backend/.coveragerc
```

---

### Playwright

**Microsoft Corporation (2024)**  
*Playwright: Fast and reliable end-to-end testing for modern web apps*  
GitHub: https://github.com/microsoft/playwright  
Version: 1.48.2  
**Verwendung:** E2E-Tests für Frontend

**Dokumentation:**
- Official Docs: https://playwright.dev/
- Python Guide: https://playwright.dev/python/

**NPM Package:**
```json
"@playwright/test": "^1.48.2"
```

**Test-Statistics:**
- 18 E2E Tests (API + Frontend)

---

### Vitest

**Patak, A., et al. (2024)**  
*Vitest: Blazing Fast Unit Test Framework*  
GitHub: https://github.com/vitest-dev/vitest  
Version: 2.1.8  
**Verwendung:** Frontend Unit-Tests

**Dokumentation:**
- Official Docs: https://vitest.dev/
- API Reference: https://vitest.dev/api/

**NPM Package:**
```json
"vitest": "^2.1.8"
```

---

### Ruff (Python Linter)

**Astral (2024)**  
*Ruff: An extremely fast Python linter, written in Rust*  
GitHub: https://github.com/astral-sh/ruff  
Version: 0.8.3  
**Verwendung:** Python Code-Linting & Formatting

**Dokumentation:**
- Official Docs: https://docs.astral.sh/ruff/

**Python Package:**
```python
# Config: backend/pyproject.toml
# Usage: ruff check . && ruff format .
```

---

### Biome (JavaScript/TypeScript Linter)

**Biome Team (2024)**  
*Biome: Toolchain of the web*  
GitHub: https://github.com/biomejs/biome  
Version: 1.9.4  
**Verwendung:** Frontend Code-Linting & Formatting

**Dokumentation:**
- Official Docs: https://biomejs.dev/

**NPM Package:**
```json
"@biomejs/biome": "^1.9.4"
```

---

## 7. DevOps & CI/CD

### Docker

**Docker, Inc. (2024)**  
*Docker: Accelerated Container Application Development*  
Official Website: https://www.docker.com/  
**Verwendung:** Containerisierung von Backend, Frontend, DB

**Dokumentation:**
- Official Docs: https://docs.docker.com/
- Compose Reference: https://docs.docker.com/compose/

**Docker Compose Version:** 2.x

**Key Files:**
- `docker/docker-compose.yml`
- `backend/Dockerfile`
- `frontend/Dockerfile`

---

### GitHub Actions

**GitHub, Inc. (2024)**  
*GitHub Actions: Automate your workflow*  
Official Docs: https://docs.github.com/en/actions  
**Verwendung:** CI/CD-Pipeline für Tests, Linting, Build

**Workflows:**
- `ci.yml` - Linting + Unit-Tests + Build
- `playwright.yml` - E2E-Tests (18 Tests)
- `test-backend.yml` - Backend-Tests isoliert
- `labeler.yml` - Auto-Labeling
- `add-to-project.yml` - GitHub Projects Integration

**Dokumentation:**
- Workflow Syntax: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions

---

### uv (Python Package Installer)

**Astral (2024)**  
*uv: An extremely fast Python package installer and resolver*  
GitHub: https://github.com/astral-sh/uv  
Version: 0.5.11  
**Verwendung:** Schnellere Dependency-Installation in CI

**Dokumentation:**
- Official Docs: https://docs.astral.sh/uv/

---

## 8. Standards & Best Practices

### REST API Design

**Fielding, R. T. (2000)**  
*Architectural Styles and the Design of Network-based Software Architectures*  
Doctoral Dissertation, University of California, Irvine  
URL: https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm  
**Verwendung:** REST-Prinzipien für API-Design

**Richardson, L., & Ruby, S. (2007)**  
*RESTful Web Services*  
O'Reilly Media  
ISBN: 978-0596529260  
**Verwendung:** Best Practices für REST API-Endpunkte

---

### OpenAPI Specification

**OpenAPI Initiative (2024)**  
*OpenAPI Specification v3.1.0*  
Official Spec: https://spec.openapis.org/oas/v3.1.0  
**Verwendung:** Automatische API-Dokumentation via FastAPI

**Tools:**
- Swagger UI: https://swagger.io/tools/swagger-ui/
- ReDoc: https://github.com/Redocly/redoc

---

### Semantic Versioning

**Preston-Werner, T. (2024)**  
*Semantic Versioning 2.0.0*  
Official Spec: https://semver.org/  
**Verwendung:** Versionierung (geplant für zukünftige Releases)

**Format:** `MAJOR.MINOR.PATCH` (z.B. `v0.3.0`)

---

### Conventional Commits

**Conventional Commits (2024)**  
*A specification for adding human and machine readable meaning to commit messages*  
Official Spec: https://www.conventionalcommits.org/  
**Verwendung:** Strukturierte Commit-Messages

**Format:**
```
<type>(scope): <description>

feat(backend): add SHAP explainer endpoint
fix(frontend): repair patient form validation
docs(readme): update setup instructions
```

---

## 9. Online-Ressourcen & Tutorials

### FastAPI Tutorials

- **Official Tutorial:** https://fastapi.tiangolo.com/tutorial/
- **Async Programming:** https://fastapi.tiangolo.com/async/
- **Dependency Injection:** https://fastapi.tiangolo.com/tutorial/dependencies/

### Vue.js Learning Resources

- **Official Guide:** https://vuejs.org/guide/
- **Composition API:** https://vuejs.org/guide/extras/composition-api-faq.html
- **Vue School:** https://vueschool.io/ (kostenpflichtig)

### SHAP Tutorials

- **Official Examples:** https://shap.readthedocs.io/en/latest/example_notebooks.html
- **Interpretable ML Book:** https://christophm.github.io/interpretable-ml-book/shap.html

### Docker Best Practices

- **Official Best Practices:** https://docs.docker.com/develop/dev-best-practices/
- **Multi-Stage Builds:** https://docs.docker.com/build/building/multi-stage/

### Testing Best Practices

- **pytest Documentation:** https://docs.pytest.org/en/stable/goodpractices.html
- **Testing FastAPI:** https://fastapi.tiangolo.com/tutorial/testing/
- **Playwright Best Practices:** https://playwright.dev/docs/best-practices

---

## Zusätzliche Referenzen

### Python Style Guides

**van Rossum, G., Warsaw, B., & Coghlan, N. (2001)**  
*PEP 8 – Style Guide for Python Code*  
Python Enhancement Proposals  
URL: https://peps.python.org/pep-0008/  
**Verwendung:** Code-Style-Richtlinien (via Ruff)

**van Rossum, G. (2015)**  
*PEP 484 – Type Hints*  
Python Enhancement Proposals  
URL: https://peps.python.org/pep-0484/  
**Verwendung:** Type-Annotations in Backend-Code

---

### Web Accessibility (WCAG)

**W3C (2018)**  
*Web Content Accessibility Guidelines (WCAG) 2.1*  
URL: https://www.w3.org/TR/WCAG21/  
**Verwendung:** Accessibility-Richtlinien für Frontend (teilweise implementiert)

---

### Security Best Practices

**OWASP Foundation (2021)**  
*OWASP Top Ten 2021*  
URL: https://owasp.org/www-project-top-ten/  
**Verwendung:** Security-Checkliste für API-Design

**OWASP Foundation (2024)**  
*OWASP API Security Top 10*  
URL: https://owasp.org/www-project-api-security/  
**Verwendung:** API-Security-Best-Practices

---

## Software-Versionen (Vollständige Liste)

### Backend (Python)
```txt
python==3.12
fastapi[standard]==0.115.5
pydantic==2.10.3
sqlmodel==0.0.22
alembic==1.14.0
psycopg[binary,pool]==3.2.3
scikit-learn==1.5.2
shap==0.46.0
pytest==8.3.4
pytest-cov==6.0.0
ruff==0.8.3
```

### Frontend (Node.js)
```json
{
  "vue": "^3.5.13",
  "typescript": "~5.6.2",
  "vite": "^6.0.1",
  "vuetify": "^3.7.5",
  "@playwright/test": "^1.48.2",
  "vitest": "^2.1.8",
  "@biomejs/biome": "^1.9.4"
}
```

### Infrastructure
- Docker: 24.0+
- Docker Compose: 2.x
- PostgreSQL: 12
- Node.js: 22.x (LTS)

---

## Zitationsformat

Dieses Dokument folgt dem **APA 7th Edition** Zitationsstil für wissenschaftliche Arbeiten und dem **IEEE Format** für technische Referenzen.

**Beispiel APA:**
```
Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. 
In Advances in Neural Information Processing Systems 30 (NIPS 2017). 
https://arxiv.org/abs/1705.07874
```

**Beispiel IEEE:**
```
[1] S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," 
in Advances in Neural Information Processing Systems 30, 2017. [Online]. 
Available: https://arxiv.org/abs/1705.07874
```

---

## Danksagungen

Besonderer Dank an:
- **FastAPI Community** für exzellente Dokumentation und Support
- **SHAP Maintainers** für das mächtige Explainability-Framework
- **Vue.js Team** für das progressive Framework
- **Open-Source Community** für alle verwendeten Tools

---

**Letzte Aktualisierung:** 18. Dezember 2025  
**Dokument-Version:** 1.0  
**Kontakt:** Siehe [PROJECT_HISTORY.md](PROJECT_HISTORY.md)

---

## Anhang: BibTeX-Einträge

Für LaTeX-Nutzer (z.B. Thesis/Paper):

```bibtex
@inproceedings{lundberg2017shap,
  title={A unified approach to interpreting model predictions},
  author={Lundberg, Scott M and Lee, Su-In},
  booktitle={Advances in Neural Information Processing Systems},
  volume={30},
  year={2017}
}

@article{pedregosa2011scikit,
  title={Scikit-learn: Machine learning in Python},
  author={Pedregosa, Fabian and Varoquaux, Ga{\"e}l and Gramfort, Alexandre and others},
  journal={Journal of Machine Learning Research},
  volume={12},
  pages={2825--2830},
  year={2011}
}

@misc{ramirez2024fastapi,
  title={FastAPI},
  author={Ram{\'i}rez, Sebasti{\'a}n},
  year={2024},
  howpublished={\url{https://github.com/fastapi/fastapi}}
}

@misc{you2024vue,
  title={Vue.js: The Progressive JavaScript Framework},
  author={You, Evan and contributors},
  year={2024},
  howpublished={\url{https://vuejs.org/}}
}
```

---

**Ende des Literaturverzeichnisses**
