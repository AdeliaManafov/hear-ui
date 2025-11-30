#!/usr/bin/env bash
# Save representative API responses to docs/demo-fallback
set -euo pipefail

OUT_DIR="docs/demo-fallback"
mkdir -p "$OUT_DIR"

echo "Saving predict response..."
curl -sS -X POST "http://localhost:8000/api/v1/predict/" \
  -H "Content-Type: application/json" \
  -d '{"age":55, "hearing_loss_duration":12.5, "implant_type":"type_b"}' > "$OUT_DIR/predict_response.json"

PATIENT_ID="dc9aff90-eec9-4cfe-bc34-9346ab90636a"
echo "Saving patient SHAP response for $PATIENT_ID..."
curl -sS "http://localhost:8000/api/v1/patients/$PATIENT_ID/shap" > "$OUT_DIR/patient_shap_response.json" || true

echo "Creating feedback example..."
RESP=$(curl -sS -X POST "http://localhost:8000/api/v1/feedback/" -H "Content-Type: application/json" -d '{"input_features":{"age":55},"prediction":0.23,"accepted":true}')
echo "$RESP" > "$OUT_DIR/feedback_response.json"
ID=$(echo "$RESP" | jq -r '.id' 2>/dev/null || echo "")
if [ -n "$ID" ]; then
  curl -sS "http://localhost:8000/api/v1/feedback/$ID" > "$OUT_DIR/feedback_readback.json" || true
fi

echo "Saved responses to $OUT_DIR"
#!/usr/bin/env bash
set -euo pipefail

# Save live demo responses into this folder for fallback during presentations.
# Usage:
#   BASE_URL="http://localhost:8000/api/v1" PATIENT_ID=<uuid> ./docs/demo-fallback/save-responses.sh

BASE_URL=${BASE_URL:-http://localhost:8000/api/v1}
PATIENT_ID=${PATIENT_ID:-dc9aff90-eec9-4cfe-bc34-9346ab90636a}
OUT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Saving demo responses into $OUT_DIR"
echo "BASE_URL=$BASE_URL PATIENT_ID=$PATIENT_ID"

echo "POST /predict/ -> $OUT_DIR/predict_response.json"
curl -sS "$BASE_URL/predict/" -H "Content-Type: application/json" \
  -d '{"age":55,"hearing_loss_duration":12.5,"implant_type":"type_b"}' \
  -o "$OUT_DIR/predict_response.json" || true

echo "GET /patients/{id}/shap -> $OUT_DIR/patient_shap_response.json"
curl -sS "$BASE_URL/patients/$PATIENT_ID/shap" -o "$OUT_DIR/patient_shap_response.json" || true

echo "POST /feedback/ -> $OUT_DIR/feedback_response.json"
curl -sS -X POST "$BASE_URL/feedback/" -H "Content-Type: application/json" \
  -d '{"input_features":{"age":55},"prediction":0.23,"accepted":true}' \
  -o "$OUT_DIR/feedback_response.json" || true

echo "Saved files:"
ls -lh "$OUT_DIR"/*.json || true

echo "Done. If files contain error objects, inspect them to see server messages."
