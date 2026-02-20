import pandas as pd
from parser import parse_csv
from graph_builder import build_graph
from detectors.cycle import detect_cycles
from detectors.smurf import detect_smurfing
from detectors.shell import detect_shell_chains
from scoring_engine import calculate_suspicion_scores
from ring_builder import build_rings_and_assign_ids
from final_json_builder import build_final_json


# =====================================================
# MAIN PIPELINE FUNCTION  🔥 VERY IMPORTANT
# =====================================================
def run_pipeline(filepath, start_time):

    # STEP 1 — PARSE CSV
    df = parse_csv(filepath)

    # STEP 2 — COUNT UNIQUE ACCOUNTS
    total_accounts = len(
        set(df["sender_id"]).union(
        set(df["receiver_id"]))
    )

    # STEP 3 — BUILD GRAPH
    G = build_graph(df)

    # STEP 4 — DETECT PATTERNS
    raw_cycles = detect_cycles(G)
    smurf = detect_smurfing(df)
    raw_shell = detect_shell_chains(G, raw_cycles)

    detections = {
        "cycles": [{"members": c["members"]} for c in raw_cycles],
        "fan_in": [{"members": c["members"]} for c in smurf["fan_in"]],
        "fan_out": [{"members": c["members"]} for c in smurf["fan_out"]],
        "shell_chains": [{"members": c["members"]} for c in raw_shell]
    }

    # STEP 5 — SCORING
    suspicious_accounts = calculate_suspicion_scores(
        detections,
        df
    )

    # STEP 6 — BUILD RINGS
    suspicious_accounts, fraud_rings = build_rings_and_assign_ids(
        detections,
        suspicious_accounts
    )

    # STEP 7 — FINAL JSON
    final_json = build_final_json(
        suspicious_accounts,
        fraud_rings,
        total_accounts,
        start_time
    )

    return suspicious_accounts, fraud_rings, final_json

from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import os

from main import run_pipeline
from final_json_builder import save_json

app = Flask(__name__)
CORS(app)   # 🔥 VERY IMPORTANT

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/analyze", methods=["POST"])
def analyze():

    start_time = time.time()

    if "file" not in request.files:
        return jsonify({"error": "No CSV uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        _, _, final_json = run_pipeline(filepath, start_time)

        save_json(final_json)

        return jsonify(final_json)

    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


if __name__ == "__main__":
    app.run(debug=True)