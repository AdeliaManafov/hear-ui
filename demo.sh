#!/bin/bash
# HEAR Demo Script - Quick demonstration of the application
set -e

echo "╔══════════════════════════════════════════════════════════╗"
echo "║         HEAR - Cochlea Implant Prediction Demo          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BACKEND_URL="http://localhost:8000"
API_URL="${BACKEND_URL}/api/v1"

# Check if backend is running
check_backend() {
    echo -e "${BLUE}🔍 Checking if backend is running...${NC}"
    if curl -s "${API_URL}/utils/health-check/" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Backend is running!${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️  Backend not running. Starting it now...${NC}"
        docker-compose up -d backend
        echo "⏳ Waiting 10 seconds for backend to start..."
        sleep 10
        return 1
    fi
}

# Demo 1: Health Check
demo_health() {
    echo ""
    echo "=========================================="
    echo "Demo 1: Health Check"
    echo "=========================================="
    curl -s "${API_URL}/utils/health-check/" | python3 -m json.tool
}

# Demo 2: Model Info
demo_model_info() {
    echo ""
    echo "=========================================="
    echo "Demo 2: Model Information"
    echo "=========================================="
    curl -s "${API_URL}/utils/model-info/" | python3 -m json.tool
}

# Demo 3: Feature Names
demo_feature_names() {
    echo ""
    echo "=========================================="
    echo "Demo 3: Feature Name Mappings (first 5)"
    echo "=========================================="
    curl -s "${API_URL}/utils/feature-names/" | python3 -m json.tool | head -n 20
    echo "  ... (truncated)"
}

# Demo 4: Prediction - Good Prognosis
demo_prediction_good() {
    echo ""
    echo "=========================================="
    echo "Demo 4: Prediction - Good Prognosis"
    echo "=========================================="
    echo "Patient: 25 years, male, postlingual hearing loss"
    echo ""
    
    curl -s -X POST "${API_URL}/predict/" \
      -H "Content-Type: application/json" \
      -d '{
        "Alter [J]": 25,
        "Geschlecht": "m",
        "Primäre Sprache": "Deutsch",
        "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "postlingual",
        "Diagnose.Höranamnese.Ursache....Ursache...": "Unbekannt",
        "Symptome präoperativ.Tinnitus...": "nein",
        "Behandlung/OP.CI Implantation": "Cochlear"
      }' | python3 -c "
import sys, json
data = json.load(sys.stdin)
pred = data.get('prediction', 0)
print(f'Prediction: {pred:.4f} ({pred*100:.1f}%)')
"
}

# Demo 5: Prediction - Poor Prognosis
demo_prediction_poor() {
    echo ""
    echo "=========================================="
    echo "Demo 5: Prediction - Poor Prognosis"
    echo "=========================================="
    echo "Patient: 65 years, female, praelingual hearing loss, tinnitus"
    echo ""
    
    curl -s -X POST "${API_URL}/predict/" \
      -H "Content-Type: application/json" \
      -d '{
        "Alter [J]": 65,
        "Geschlecht": "w",
        "Primäre Sprache": "Deutsch",
        "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "praelingual",
        "Diagnose.Höranamnese.Ursache....Ursache...": "Unbekannt",
        "Symptome präoperativ.Tinnitus...": "ja",
        "Behandlung/OP.CI Implantation": "Med-El"
      }' | python3 -c "
import sys, json
data = json.load(sys.stdin)
pred = data.get('prediction', 0)
print(f'Prediction: {pred:.4f} ({pred*100:.1f}%)')
"
}

# Demo 6: SHAP Explanation
demo_shap() {
    echo ""
    echo "=========================================="
    echo "Demo 6: SHAP Explanation (Top Features)"
    echo "=========================================="
    echo "Patient: 45 years, female, postlingual, tinnitus"
    echo ""
    
    curl -s -X POST "${API_URL}/shap/explain" \
      -H "Content-Type: application/json" \
      -d '{
        "Alter [J]": 45,
        "Geschlecht": "w",
        "Primäre Sprache": "Deutsch",
        "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "postlingual",
        "Diagnose.Höranamnese.Ursache....Ursache...": "Unbekannt",
        "Symptome präoperativ.Tinnitus...": "ja",
        "Behandlung/OP.CI Implantation": "Cochlear"
      }' | python3 -c "
import sys, json
data = json.load(sys.stdin)
pred = data.get('prediction', 0)
top_features = data.get('top_features', [])

print(f'Prediction: {pred:.4f} ({pred*100:.1f}%)')
print('\nTop 3 Influential Features:')
for i, feat in enumerate(top_features[:3], 1):
    feature_name = feat.get('feature', 'Unknown')
    importance = feat.get('importance', 0)
    # Shorten feature name for display
    display_name = feature_name.replace('cat__', '').replace('num__', '')
    if len(display_name) > 40:
        display_name = display_name[:37] + '...'
    print(f'  {i}. {display_name}')
    print(f'     Impact: {importance:+.4f}')
"
}

# Demo 7: Documentation Links
demo_docs() {
    echo ""
    echo "=========================================="
    echo "Demo 7: Documentation & Links"
    echo "=========================================="
    echo "📖 API Documentation (Swagger): ${BACKEND_URL}/docs"
    echo "📖 Project Docs: docs/Projektdokumentation.md"
    echo "📊 Test Results: docs/TEST_RESULTS.md"
    echo "🔍 SHAP Integration: docs/SHAP_INTEGRATION.md"
    echo "📈 Model Calibration: docs/MODEL_CALIBRATION.md"
    echo ""
    echo "🌐 You can open these in your browser:"
    echo "  - Swagger UI: open ${BACKEND_URL}/docs"
}

# Main
main() {
    # Check backend
    check_backend
    
    # Run all demos
    demo_health
    demo_model_info
    demo_feature_names
    demo_prediction_good
    demo_prediction_poor
    demo_shap
    demo_docs
    
    echo ""
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                   Demo Complete! 🎉                      ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo ""
    echo "Next steps:"
    echo "  • Explore API: ${BACKEND_URL}/docs"
    echo "  • Run tests: python3 backend/scripts/test_all_patients.py"
    echo "  • Check docs: cat docs/Projektdokumentation.md"
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
