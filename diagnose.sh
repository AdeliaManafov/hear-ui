#!/bin/bash
# HEAR-UI System Diagnose Script

echo "======================================"
echo "HEAR-UI System Diagnose"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Container Status
echo "1. Container Status:"
echo "-------------------"
if docker compose -f docker/docker-compose.yml --env-file "$PWD/.env" ps | grep -q "Up"; then
    echo -e "${GREEN}OK${NC} - Container laufen"
    docker compose -f docker/docker-compose.yml --env-file "$PWD/.env" ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
else
    echo -e "${RED}FEHLER${NC} - Keine Container laufen"
    echo "Starte Container mit:"
    echo "  docker compose -f docker/docker-compose.yml -f docker/docker-compose.override.yml --env-file \"\$PWD/.env\" up -d"
    exit 1
fi
echo ""

# Test 2: Backend Health Check
echo "2. Backend Health Check:"
echo "------------------------"
HEALTH=$(curl -s http://localhost:8000/api/v1/utils/health-check/)
if echo "$HEALTH" | grep -q "ok"; then
    echo -e "${GREEN}OK${NC} - Backend ist erreichbar"
    echo "   Response: $HEALTH"
else
    echo -e "${RED}FEHLER${NC} - Backend antwortet nicht korrekt"
    echo "   Response: $HEALTH"
fi
echo ""

# Test 3: Backend Prediction
echo "3. Backend Prediction Test:"
echo "---------------------------"
PREDICT=$(curl -s -X POST http://localhost:8000/api/v1/predict/ \
  -H "Content-Type: application/json" \
  -d '{"Alter [J]": 45, "Geschlecht": "w"}')
if echo "$PREDICT" | grep -q "prediction"; then
    echo -e "${GREEN}OK${NC} - Vorhersage funktioniert"
    PRED_VALUE=$(echo "$PREDICT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f\"{d['prediction']:.2%}\")" 2>/dev/null || echo "N/A")
    echo "   Prediction: $PRED_VALUE"
else
    echo -e "${RED}FEHLER${NC} - Vorhersage fehlgeschlagen"
    echo "   Response: $PREDICT"
fi
echo ""

# Test 4: Database Connection
echo "4. Datenbank-Verbindung:"
echo "------------------------"
DB_TEST=$(docker compose -f docker/docker-compose.yml --env-file "$PWD/.env" exec -T db psql -U postgres -d hear_db -c "SELECT 1;" 2>&1)
if echo "$DB_TEST" | grep -q "1 row"; then
    echo -e "${GREEN}OK${NC} - Datenbank erreichbar"
else
    echo -e "${RED}FEHLER${NC} - Datenbank nicht erreichbar"
    echo "   Error: $DB_TEST"
fi
echo ""

# Test 5: Frontend
echo "5. Frontend:"
echo "------------"
FRONTEND=$(curl -s http://localhost:5173 2>&1)
if echo "$FRONTEND" | grep -q "html"; then
    echo -e "${GREEN}OK${NC} - Frontend ist erreichbar"
else
    echo -e "${RED}FEHLER${NC} - Frontend nicht erreichbar"
fi
echo ""

# Test 6: pgAdmin
echo "6. pgAdmin:"
echo "-----------"
PGADMIN=$(curl -s http://localhost:5051 2>&1)
if echo "$PGADMIN" | grep -q "pgAdmin"; then
    echo -e "${GREEN}OK${NC} - pgAdmin ist erreichbar"
else
    echo -e "${YELLOW}WARNING${NC} - pgAdmin nicht erreichbar (optional)"
fi
echo ""

# Test 7: CORS Test
echo "7. CORS-Test (Frontend → Backend):"
echo "-----------------------------------"
CORS=$(curl -s -H "Origin: http://localhost:5173" http://localhost:8000/api/v1/utils/health-check/ -v 2>&1 | grep -i "access-control")
if [ ! -z "$CORS" ]; then
    echo -e "${GREEN}OK${NC} - CORS ist konfiguriert"
    echo "   $CORS"
else
    echo -e "${YELLOW}WARNING${NC} - CORS Header nicht gefunden"
fi
echo ""

# Summary
echo "======================================"
echo "Zusammenfassung:"
echo "======================================"
echo ""
echo "URLs zum Testen:"
echo "  Backend API:  http://localhost:8000/docs"
echo "  Frontend:     http://localhost:5173"
echo "  pgAdmin:      http://localhost:5051"
echo "  Health Check: http://localhost:8000/api/v1/utils/health-check/"
echo ""
echo "Datenbank-Zugriff:"
echo "  Host:     localhost"
echo "  Port:     5434"
echo "  User:     postgres"
echo "  Database: hear_db"
echo "  Password: (siehe .env Datei)"
echo ""
echo "Wenn du Fehler siehst im Browser:"
echo "  1. Hard-Refresh: CMD+SHIFT+R (Mac) / CTRL+SHIFT+R (Linux/Win)"
echo "  2. Browser-Cache leeren"
echo "  3. Browser-Konsole öffnen (F12) und Fehler prüfen"
echo "  4. Netzwerk-Tab öffnen und API-Anfragen prüfen"
echo ""
