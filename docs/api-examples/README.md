# Demo fallback artifacts

This folder contains fallback artifacts for the live demo. If the live demo fails, show these pre-captured responses and a short screencast instead.

Files:
- `predict_response.json` — example response from the `POST /api/v1/predict/` endpoint
- `patient_shap_response.json` — example response from `GET /api/v1/patients/<id>/shap`
- `feedback_response.json` — example response from creating feedback
- `feedback_readback.json` — readback of created feedback
- `adminer_screenshot.png` — (optionally) screenshot of Adminer UI

Helper:
- `save-responses.sh` — script to capture live responses into this folder. Run:

```bash
chmod +x docs/demo-fallback/save-responses.sh
./docs/demo-fallback/save-responses.sh
```

Notes:
- The script will try to fetch the SHAP response for a hard-coded example patient ID (`dc9aff90-eec9-4cfe-bc34-9346ab90636a`). Edit the script to use another ID if needed.
- Keep these artifacts in the repo (or copy them to a USB key) so you can present them if networking or model loading fails during the live demo.
