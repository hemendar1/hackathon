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

    # =============================
    # 1. PARSE CSV
    # =============================
    df = parse_csv(filepath)

    # =============================
    # 2. TOTAL ACCOUNTS COUNT
    # 🔥 THIS WAS YOUR MAIN ERROR
    # =============================
    total_accounts = len(
        set(df["sender_id"]).union(
        set(df["receiver_id"]))
    )

    # =============================
    # 3. BUILD GRAPH
    # =============================
    G = build_graph(df)

    # =============================
    # 4. DETECT PATTERNS
    # =============================
    raw_cycles = detect_cycles(G)
    smurf = detect_smurfing(df)
    raw_shell = detect_shell_chains(G, raw_cycles)

    detections = {
        "cycles": [
            {"members": cycle["members"]}
            for cycle in raw_cycles
        ],
        "fan_in": [
            {"members": cluster["members"]}
            for cluster in smurf["fan_in"]
        ],
        "fan_out": [
            {"members": cluster["members"]}
            for cluster in smurf["fan_out"]
        ],
        "shell_chains": [
            {"members": chain["members"]}
            for chain in raw_shell
        ]
    }

    # =============================
    # 5. SCORE ACCOUNTS
    # =============================
    suspicious_accounts = calculate_suspicion_scores(detections)

    # =============================
    # 6. BUILD FRAUD RINGS
    # =============================
    suspicious_accounts, fraud_rings = build_rings_and_assign_ids(
        detections,
        suspicious_accounts
    )

    # =============================
    # 7. FINAL JSON
    # =============================
    final_json = build_final_json(
        suspicious_accounts,
        fraud_rings,
        total_accounts,
        start_time
    )

    return G, detections, final_json
