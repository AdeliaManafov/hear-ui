# XTab-CDS Architecture Diagrams

## Hauptarchitektur (für Paper)

### Mermaid-Code (bevorzugt für wissenschaftliche Papers)

```mermaid
graph TB
    subgraph "Klinischer Benutzer"
        User[👨‍⚕️ Arzt/Klinikpersonal]
    end
    
    subgraph "Frontend Layer (Vue.js)"
        UI[Benutzeroberfläche]
        PatientForm[Patienteneingabe]
        PredView[Vorhersage-Anzeige]
        ExplView[Erklärungen & Visualisierung]
        Feedback[Feedback-Formular]
    end
    
    subgraph "Backend Layer (FastAPI Python)"
        API[REST API Endpunkte]
        
        subgraph "Core Module - Adapter-Architektur"
            DataAdapter[📊 Dataset Adapter<br/>Datenvorverarbeitung<br/>Feature Engineering]
            ModelAdapter[🤖 Model Adapter<br/>ML-Modell Wrapper<br/>Vorhersagen]
            ExplainerAdapter[💡 Explainer Adapter<br/>SHAP/LIME<br/>Erklärungen]
        end
        
        CRUD[Patient Management]
        PredAPI[Prediction Service]
        FeedbackAPI[Feedback Service]
    end
    
    subgraph "Datenbank Layer"
        DB[(PostgreSQL<br/>Patienten<br/>Vorhersagen<br/>Feedback)]
    end
    
    subgraph "Deployment"
        Docker[🐳 Docker Container<br/>Reproduzierbare Umgebung]
    end
    
    User -->|Interaktion| UI
    UI --> PatientForm
    PatientForm -->|Patientendaten| API
    API --> CRUD
    CRUD --> DB
    
    API --> DataAdapter
    DataAdapter -->|Vorverarbeitete Features| ModelAdapter
    ModelAdapter -->|Vorhersage| PredAPI
    PredAPI -->|Vorhersage + Daten| ExplainerAdapter
    ExplainerAdapter -->|Erklärung| PredView
    
    PredView -->|Anzeige| UI
    ExplView -->|Anzeige| UI
    
    Feedback -->|Klinisches Feedback| FeedbackAPI
    FeedbackAPI --> DB
    
    DB -.->|Monitoring & Retraining| ModelAdapter
    
    Docker -.->|Container| Frontend Layer
    Docker -.->|Container| Backend Layer
    Docker -.->|Container| Datenbank Layer
    
    style DataAdapter fill:#e1f5ff
    style ModelAdapter fill:#fff4e1
    style ExplainerAdapter fill:#f0e1ff
    style User fill:#d4edda
    style DB fill:#f8d7da
```

---

## Vereinfachte Version (ohne Emojis, für formelle Papers)

```mermaid
graph TB
    User[Klinischer Benutzer]
    
    subgraph Frontend["Presentation Layer"]
        UI[Web Interface<br/>Vue.js + TypeScript]
        Forms[Data Entry]
        Viz[Visualization]
    end
    
    subgraph Backend["Application Layer"]
        API[REST API<br/>FastAPI]
        
        subgraph Adapters["Modular Adapter Architecture"]
            DA[Dataset Adapter]
            MA[Model Adapter]
            EA[Explainer Adapter]
        end
        
        Services[Business Logic]
    end
    
    subgraph Data["Data Layer"]
        DB[(PostgreSQL)]
    end
    
    User --> UI
    UI --> API
    API --> DA
    DA --> MA
    MA --> EA
    API --> Services
    Services --> DB
    EA --> Viz
    
    style DA fill:#e3f2fd
    style MA fill:#fff3e0
    style EA fill:#f3e5f5
```

---

## Adapter-fokussierte Ansicht (Detail der Kern-Architektur)

```mermaid
graph LR
    subgraph Input["Input Data"]
        Raw[Raw Patient Data<br/>Various Formats]
    end
    
    subgraph DatasetAdapter["Dataset Adapter"]
        Valid[Validation]
        FE[Feature Engineering]
        Norm[Normalization]
        Encode[Encoding]
    end
    
    subgraph ModelAdapter["Model Adapter"]
        Load[Model Loading]
        Pred[Prediction]
        Prob[Probability Estimation]
    end
    
    subgraph ExplainerAdapter["Explainer Adapter"]
        SHAP[SHAP]
        LIME[LIME]
        Captum[Captum]
        Quantus[Quantus]
    end
    
    subgraph Output["Output"]
        Result[Prediction + Explanation]
        Viz[Visual Attribution]
    end
    
    Raw --> Valid
    Valid --> FE
    FE --> Norm
    Norm --> Encode
    Encode --> Load
    Load --> Pred
    Pred --> Prob
    Prob --> SHAP
    SHAP --> Result
    LIME --> Result
    Captum --> Result
    Quantus --> Result
    Result --> Viz
    
    style DatasetAdapter fill:#e1f5ff
    style ModelAdapter fill:#fff4e1
    style ExplainerAdapter fill:#f0e1ff
```

---

## Datenfluss-Diagramm (User Journey)

```mermaid
sequenceDiagram
    participant User as Arzt
    participant UI as Web Interface
    participant API as Backend API
    participant DA as Dataset Adapter
    participant MA as Model Adapter
    participant EA as Explainer Adapter
    participant DB as Database
    
    User->>UI: Gibt Patientendaten ein
    UI->>API: POST /api/v1/predict
    API->>DA: Validiert & transformiert Daten
    DA->>MA: Vorverarbeitete Features
    MA->>MA: Führt Vorhersage aus
    MA->>EA: Vorhersage + Features
    EA->>EA: Generiert Erklärung (SHAP)
    EA->>API: Vorhersage + Erklärung
    API->>DB: Speichert Vorhersage (optional)
    API->>UI: Vorhersage + Visualisierung
    UI->>User: Zeigt Ergebnis mit Feature Attribution
    User->>UI: Gibt Feedback
    UI->>API: POST /api/v1/feedback
    API->>DB: Speichert Feedback
    DB->>MA: Ermöglicht Monitoring & Retraining
```

---

## Deployment-Architektur

```mermaid
graph TB
    subgraph Docker["Docker Compose Orchestration"]
        subgraph Frontend_C["Frontend Container"]
            Nginx[Nginx]
            Vue[Vue.js SPA]
        end
        
        subgraph Backend_C["Backend Container"]
            FastAPI[FastAPI Server]
            Workers[Uvicorn Workers]
        end
        
        subgraph DB_C["Database Container"]
            PG[PostgreSQL]
        end
        
        subgraph Admin_C["Admin Container"]
            PGA[pgAdmin]
        end
    end
    
    Users[Klinische Nutzer] --> Nginx
    Nginx --> Vue
    Vue --> FastAPI
    FastAPI --> PG
    PGA --> PG
    
    style Frontend_C fill:#e8f5e9
    style Backend_C fill:#e3f2fd
    style DB_C fill:#fff3e0
```

---

## Empfehlungen für Paper-Integration

### Option 1: Mermaid direkt (wenn LaTeX-unterstützt)
Viele moderne LaTeX-Pakete unterstützen Mermaid:
- `mermaid-latex` Package
- Konvertierung mit `mmdc` (Mermaid CLI)

### Option 2: Export als PNG/SVG
```bash
# Mermaid CLI installieren
npm install -g @mermaid-js/mermaid-cli

# Diagramm exportieren
mmdc -i architecture.mmd -o architecture.png -w 1920 -H 1080
mmdc -i architecture.mmd -o architecture.svg
```

### Option 3: Online-Tools
1. **Mermaid Live Editor**: https://mermaid.live/
   - Code eingeben → als PNG/SVG exportieren
   
2. **Draw.io**: https://app.diagrams.net/
   - Für mehr Kontrolle über Design
   - Export als PNG, PDF, SVG

3. **Figma/Inkscape**:
   - Für publication-quality Diagramme

### Option 4: LaTeX TikZ
Für höchste Qualität in wissenschaftlichen Papers - ich kann auch TikZ-Code generieren.

---

## Beschreibungstext für Paper (Vorschlag)

**Figure X: XTab-CDS Framework Architecture Overview**

The framework implements a three-tier architecture consisting of:
1. **Presentation Layer**: Vue.js-based web interface enabling clinician interaction
2. **Application Layer**: FastAPI backend with modular adapter architecture
3. **Data Layer**: PostgreSQL database for persistent storage

The core innovation lies in the modular adapter architecture (center), which decouples:
- **Dataset Adapters**: Handle data preprocessing, validation, and feature engineering
- **Model Adapters**: Wrap ML models with unified prediction interfaces
- **Explainer Adapters**: Provide pluggable explanation methods (SHAP, LIME, etc.)

This separation enables the same infrastructure to support different clinical prediction tasks through configuration changes alone, without modifying the core application code. The feedback loop (bottom) enables continuous monitoring and model improvement based on clinician input.

---

## Legende/Glossar für Nicht-Informatiker

| Begriff | Erklärung |
|---------|-----------|
| **Frontend** | Die Benutzeroberfläche, die Ärzte sehen und bedienen |
| **Backend** | Die Logik im Hintergrund, die Berechnungen durchführt |
| **API** | Schnittstelle, die Frontend und Backend verbindet |
| **Adapter** | Austauschbare Module für verschiedene Datenquellen/Modelle |
| **SHAP/LIME** | Erklärungsmethoden, die zeigen, welche Faktoren die Vorhersage beeinflussen |
| **Docker Container** | Isolierte Umgebung, die überall gleich läuft |
| **PostgreSQL** | Datenbanksystem zur Speicherung von Patientendaten |
| **REST API** | Standard-Kommunikationsprotokoll zwischen Systemen |
| **Feature Engineering** | Aufbereitung von Rohdaten für das ML-Modell |

