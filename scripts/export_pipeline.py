"""
Template script to export a trained scikit-learn Pipeline to a joblib file that the backend can load.
Usage (in your training environment):

  python export_pipeline.py --in model.pkl --out ../hear-ui/backend/app/models/logreg_best_pipeline.pkl

Adjust the --in path to point to your trained pipeline object or training script that returns `pipeline`.
This script expects that you either already have a `pipeline` variable in a file that can be imported, or you can adapt it to load your model object and re-save.
"""
from pathlib import Path
import argparse
from joblib import dump

parser = argparse.ArgumentParser()
parser.add_argument("--in", dest="infile", required=True, help="Path to a Python file that creates a variable `pipeline` when executed (optional).")
parser.add_argument("--out", dest="outfile", required=True, help="Destination joblib file path to write the pipeline to.")
args = parser.parse_args()

infile = Path(args.infile)
outfile = Path(args.outfile)

# Simple behaviour: import a module from the provided path and look for `pipeline` object.
# If your training code doesn't expose this, modify this script to load the model object differently.

import importlib.util
spec = importlib.util.spec_from_file_location("_train_module", str(infile))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

if not hasattr(mod, "pipeline"):
    raise SystemExit("The provided module does not expose a `pipeline` variable. Edit the script or your module.")

pipeline = getattr(mod, "pipeline")

# Dump pipeline
outfile.parent.mkdir(parents=True, exist_ok=True)
dump(pipeline, str(outfile))
print(f"Wrote pipeline to {outfile}")
