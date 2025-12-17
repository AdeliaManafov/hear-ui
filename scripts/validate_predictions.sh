#!/bin/bash
# Validation Script - Überprüft Predictions für alle Patienten

echo "=================================================="
echo "  HEAR-UI Prediction Validation Script"
echo "=================================================="
echo ""

BASE_URL="http://localhost:8000"
COMPOSE_CMD="docker compose -f docker/docker-compose.yml -f docker/docker-compose.override.yml --env-file .env"

# Farben für Output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "📊 Teste alle Patienten in der Datenbank..."
echo ""

# Hole alle Patient IDs
PATIENT_IDS=$($COMPOSE_CMD exec -T db psql -U postgres -d hear_db -t -c "SELECT id FROM patient ORDER BY created_at;")

counter=0
success=0
failed=0

for PID in $PATIENT_IDS; do
    PID=$(echo $PID | xargs)  # Trim whitespace
    if [ ! -z "$PID" ]; then
        counter=$((counter + 1))
        
        # Zeige Patient Info
        echo "Patient $counter (ID: ${PID:0:8}...)"
        
        # Test Prediction Endpoint
        RESPONSE=$(curl -s "$BASE_URL/api/v1/patients/$PID/predict")
        PREDICTION=$(echo $RESPONSE | jq -r '.prediction')
        
        if [ "$PREDICTION" != "null" ] && [ ! -z "$PREDICTION" ]; then
            PERCENT=$(echo "scale=1; $PREDICTION * 100" | bc)
            echo -e "  ${GREEN}✓${NC} Prediction: ${PERCENT}% Erfolgswahrscheinlichkeit"
            success=$((success + 1))
            
            # Test Explainer Endpoint
            EXPL_RESPONSE=$(curl -s "$BASE_URL/api/v1/patients/$PID/explainer")
            EXPL_PRED=$(echo $EXPL_RESPONSE | jq -r '.prediction')
            
            if [ "$PREDICTION" == "$EXPL_PRED" ]; then
                echo -e "  ${GREEN}✓${NC} Explainer: Konsistent mit Prediction"
            else
                echo -e "  ${RED}✗${NC} Explainer: INKONSISTENT! (${EXPL_PRED})"
            fi
            
            # Zeige Top 3 Features
            echo "    Top Features:"
            echo $EXPL_RESPONSE | jq -r '.top_features[0:3] | .[] | "      • \(.feature | split("_")[0]): \(.importance | tostring | .[0:6])"'
            
        else
            echo -e "  ${RED}✗${NC} Prediction fehlgeschlagen (null oder leer)"
            failed=$((failed + 1))
            
            # Validiere Patient Daten
            VALIDATION=$(curl -s "$BASE_URL/api/v1/patients/$PID/validate")
            IS_OK=$(echo $VALIDATION | jq -r '.ok')
            
            if [ "$IS_OK" == "false" ]; then
                echo -e "    ${YELLOW}⚠${NC} Fehlende Features:"
                echo $VALIDATION | jq -r '.missing_features | .[] | "      • \(.)"'
            else
                echo -e "    ${YELLOW}⚠${NC} Daten vollständig, aber Preprocessing fehlgeschlagen"
                # Zeige verfügbare Feature-Keys
                FEATURE_COUNT=$(echo $VALIDATION | jq -r '.features_count')
                echo "      Verfügbare Features: $FEATURE_COUNT"
            fi
        fi
        
        echo ""
    fi
done

echo "=================================================="
echo "  Zusammenfassung"
echo "=================================================="
echo "Gesamt:       $counter Patienten"
echo -e "Erfolgreich:  ${GREEN}$success${NC}"
echo -e "Fehlgeschlagen: ${RED}$failed${NC}"
echo ""

if [ $failed -gt 0 ]; then
    echo -e "${YELLOW}💡 Empfehlung:${NC} Überprüfe die fehlgeschlagenen Patienten:"
    echo "   1. Validiere fehlende Features mit /api/v1/patients/{id}/validate"
    echo "   2. Prüfe Backend-Logs: docker compose logs backend | grep ERROR"
    echo "   3. Teste Preprocessing: curl http://localhost:8000/api/v1/utils/prepare-input/"
    exit 1
else
    echo -e "${GREEN}✓ Alle Predictions erfolgreich!${NC}"
    exit 0
fi
