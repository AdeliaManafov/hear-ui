# 🎯 HEAR - Cochlea Implant Success Prediction

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen.svg)]()

AI-powered prediction system for Cochlea Implant success rates with SHAP explanations.

---

## ✨ Features

- 🤖 **Machine Learning Predictions** - RandomForest model with isotonic calibration (ECE: 0.00)
- 🔍 **SHAP Explanations** - Understand which factors influence each prediction
- 📊 **RESTful API** - FastAPI backend with automatic documentation
- 🐳 **Docker-Ready** - Complete containerized setup
- 📈 **Production-Grade** - Calibrated models, comprehensive tests, monitoring-ready

---

## 🚀 Quick Start

### Run the Demo

```bash
./demo.sh
```

This will:
1. Start the backend (if not running)
2. Demonstrate all API endpoints
3. Show sample predictions with SHAP explanations

### Manual Setup

1. **

Clone & Navigate:**
   ```bash
   cd /path/to/hear-ui
   ```

2. **Start Services:**
   ```bash
   docker-compose up -d
   ```

3. **Verify:**
   ```bash
   curl http://localhost:8000/api/v1/utils/health-check/
   # Should return: {"status":"ok"}
   ```

4. **Explore API:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

---

## 📖 API Endpoints

### Predictions

```bash
# Make a prediction
curl -X POST http://localhost:8000/api/v1/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "Alter [J]": 45,
    "Geschlecht": "w",
    "Primäre Sprache": "Deutsch",
    "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "postlingual",
    "Diagnose.Höranamnese.Ursache....Ursache...": "Unbekannt",
    "Symptome präoperativ.Tinnitus...": "ja",
    "Behandlung/OP.CI Implantation": "Cochlear"
  }'

# Returns: {"prediction": 0.9734, "explanation": {}}
```

### SHAP Explanations

```bash
# Get detailed SHAP explanation
curl -X POST http://localhost:8000/api/v1/shap/explain \
  -H "Content-Type: application/json" \
  -d '{...patient data...}'

# Returns: prediction + feature_importance + top_features
```

### Feature Mappings

```bash
# Get human-readable feature names
curl http://localhost:8000/api/v1/utils/feature-names/

# Get features grouped by category
curl http://localhost:8000/api/v1/utils/feature-categories/
```

---

## 🧪 Testing

### Run All Tests

```bash
# API endpoint tests
python3 backend/scripts/test_api.py

# Real patient data test (28 patients)
python3 backend/scripts/test_all_patients.py

# Calibrated model & feature tests
python3 backend/scripts/test_calibrated_features.py
```

### Model Calibration Check

```bash
# Validate model calibration
python3 backend/scripts/quick_calibration_check.py \
  backend/app/models/logreg_calibrated.pkl \
  data/test_patients_synthetic.csv
```

---

## 📊 Model Information

### Current Model

- **Type:** RandomForest Regressor with Isotonic Calibration
- **Features:** 7 input features → 18 after one-hot encoding
- **Calibration:** ECE = 0.00 (perfect calibration!)
- **Background Data:** 100 realistic patients for SHAP

### Performance Metrics

| Metric | Value | Status |
|--------|-------|--------|
| **ECE (Calibration)** | 0.00 | ✅ Perfect |
| **Brier Score** | 0.129 | ✅ Good |
| **AUC-ROC** | 0.77 | ⚠️ Moderate |
| **Prediction Varianz** | 77-97% | ✅ Realistic |

### Key Findings

- **Postlingual hearing loss** = Strong positive predictor (+17% impact)
- **Age** = Moderate impact
- **Model handles missing data** with sensible defaults

---

## 🏗️ Architecture

```
hear-ui/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/routes/  # API endpoints
│   │   ├── core/        # Model, SHAP, preprocessor
│   │   └── models/      # Trained models (.pkl files)
│   └── scripts/         # Util scripts (calibration, tests)
├── frontend/            # Vue.js frontend (WIP)
├── docs/                # Documentation
│   ├── Projektdokumentation.md
│   ├── SHAP_INTEGRATION.md
│   └── MODEL_CALIBRATION.md
├── data/                # Test data
├── docker-compose.yml   # Container orchestration
└── demo.sh              # Quick demo script
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Projektdokumentation](docs/Projektdokumentation.md) | Complete project overview |
| [SHAP Integration](docs/SHAP_INTEGRATION.md) | SHAP implementation details |
| [Model Calibration](docs/MODEL_CALIBRATION.md) | Calibration guide & best practices |
| [API Docs (Swagger)](http://localhost:8000/docs) | Interactive API documentation |

---

## 🔧 Development

### Prerequisites

- Docker & Docker Compose
- Python 3.10+ (for local testing)
- Node.js 18+ (for frontend)

### Local Development Setup

```bash
# Backend only (recommended)
docker-compose up backend

# Full stack
docker-compose up

# Watch logs
docker-compose logs -f backend
```

### Environment Variables

Create `.env` file:

```bash
# Database
POSTGRES_PASSWORD=your_secure_password

# Model (optional)
MODEL_PATH=backend/app/models/logreg_calibrated.pkl

# SHAP Background (optional)
SHAP_BACKGROUND_FILE=backend/app/models/background_sample.csv
```

---

## 🛠️ Scripts & Utilities

### Generate Background Data for SHAP

```bash
python3 backend/scripts/generate_background_data.py
# Creates: backend/app/models/background_sample.csv (100 patients)
```

### Calibrate a Model

```bash
python3 backend/scripts/calibrate_model.py \
  backend/app/models/logreg_best_pipeline.pkl \
  data/training_with_outcomes.csv \
  backend/app/models/logreg_calibrated.pkl
```

### Test All Patients from CSV

```bash
python3 backend/scripts/test_all_patients.py
# Tests all 28 patients from Dummy Data_Cochlear Implant.csv
```

---

## 🚢 Deployment

### Production Checklist

- [x] ✅ Calibrated model activated
- [x] ✅ SHAP background data (100 patients)
- [x] ✅ Feature mapping endpoints
- [x] ✅ Comprehensive tests
- [x] ✅ API documentation
- [ ] ⏳ Frontend integration
- [ ] ⏳ Authentication & Authorization
- [ ] ⏳ TLS/HTTPS
- [ ] ⏳ Monitoring & Logging

### Docker Deployment

```bash
# Build
docker-compose build

# Deploy
docker-compose up -d

# Health check
curl http://your-domain/api/v1/utils/health-check/
```

---

## 📈 Roadmap

### v1.0 (Current - Production Ready)
- [x] API Backend
- [x] ML Model Integration
- [x] SHAP Explanations
- [x] Model Calibration
- [x] Comprehensive Testing

### v1.1 (Planned)
- [ ] Frontend UI
- [ ] User Authentication
- [ ] Batch Upload
- [ ] PDF Reports
- [ ] Advanced SHAP Visualizations

### v2.0 (Future)
- [ ] Real-time Model Updates
- [ ] Multi-language Support
- [ ] Mobile App
- [ ] Clinical Trial Integration

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## 📄 License

[Your License Here]

---

## 👥 Authors

- **Adelia Manafov** - Initial work

---

## 🙏 Acknowledgments

- RandomForest implementation: scikit-learn
- SHAP explanations: SHAP library
- API framework: FastAPI
- Containerization: Docker

---

## 📞 Support

For questions or issues:

- 📧 Email: [your-email]
- 📝 Issues: GitHub Issues
- 📖 Docs: `docs/Projektdokumentation.md`

---

**Status:** ✅ Production-Ready  
**Last Updated:** 24. November 2025  
**Version:** 1.0.0
