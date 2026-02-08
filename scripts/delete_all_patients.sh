set -euo pipefail

  API_BASE="${API_BASE:-http://localhost:8000}"
  LIMIT=200
  OFFSET=0

  while :; do
    resp="$(curl -sS "${API_BASE}/api/v1/patients/?paginated=true&limit=${LIMIT}&offset=${OFFSET}")"
    ids="$(echo "$resp" | jq -r '.items[].id')"

    if [[ -z "$ids" ]]; then
      break
    fi

    while IFS= read -r id; do
      [[ -z "$id" ]] && continue
      curl -sS -X DELETE "${API_BASE}/api/v1/patients/${id}" >/dev/null
      echo "Deleted ${id}"
    done <<< "$ids"

    total="$(echo "$resp" | jq -r '.total')"
    OFFSET=$((OFFSET + LIMIT))
    if (( OFFSET >= total )); then
      break
    fi
  done

  echo "Done."
