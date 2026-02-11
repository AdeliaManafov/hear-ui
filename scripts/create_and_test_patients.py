#!/usr/bin/env python3
import csv
import json
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

BASE = "http://localhost:8000/api/v1"
CSV = "patientsData/sample_patients.csv"


def post_json(path, payload):
    url = f"{BASE}{path}"
    data = json.dumps(payload).encode("utf-8")
    req = Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(req, timeout=20) as resp:
            resp_data = resp.read().decode("utf-8")
            return json.loads(resp_data)
    except HTTPError as e:
        print(f"HTTP Error {e.code} for {url}: {e.reason}")
        try:
            body = e.read().decode()
            print(body)
        except Exception:
            pass
    except URLError as e:
        print(f"URL Error for {url}: {e}")
    except Exception as e:
        print(f"Request failed for {url}: {e}")
    return None


def get_json(path):
    url = f"{BASE}{path}"
    req = Request(url, headers={"Accept": "application/json"})
    try:
        with urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"GET failed {url}: {e}")
        return None


def summarize_explainer(resp):
    if not resp:
        return "(no explainer response)"
    pred = resp.get("prediction")
    top = resp.get("top_features") or []
    lines = [f"prediction={pred}", "top:"]
    for f in top[:5]:
        name = f.get("name") or f.get("feature") or str(f)
        imp = f.get("importance") if f.get("importance") is not None else f.get("value")
        lines.append(f"  {name}: {imp}")
    return "\n".join(lines)


def main():
    created = []
    with open(CSV, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for i, row in enumerate(reader, start=1):
            row_payload = {k: v for k, v in row.items() if k != "ID"}
            # remove empty strings
            input_features = {k: v for k, v in row_payload.items() if v != ""}
            display_name = f"Sample-{i}-{input_features.get('Geschlecht','?')}-{input_features.get('Alter [J]','?')}"

            payload = {"display_name": display_name, "input_features": input_features}
            # create patient
            print(f"\nCreating Patient #{i} ({display_name})")
            resp = post_json("/patients/", payload)
            if not resp:
                print("Failed to create patient")
                continue
            pid = resp.get("id")
            print(f"  Created ID: {pid}")
            created.append(pid)

            # call patient predict
            p_pred = get_json(f"/patients/{pid}/predict")
            print("  /patients/{}/predict -> {}".format(pid, json.dumps(p_pred)))

            # call patient explainer
            p_expl = get_json(f"/patients/{pid}/explainer")
            print("  /patients/{}/explainer -> {}".format(pid, summarize_explainer(p_expl)))

    print("\nSummary: created %d patients" % len(created))

if __name__ == "__main__":
    main()
