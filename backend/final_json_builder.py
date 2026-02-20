import json
import time
import os


# ====================================================
# BUILD FINAL JSON
# ====================================================
def build_final_json(suspicious_accounts, fraud_rings, total_accounts, start_time):

    suspicious_accounts = sorted(
        suspicious_accounts,
        key=lambda x: x["suspicion_score"],
        reverse=True
    )

    summary = {
        "total_accounts_analyzed": total_accounts,
        "suspicious_accounts_flagged": len(suspicious_accounts),
        "fraud_rings_detected": len(fraud_rings),
        "processing_time_seconds": round(time.time() - start_time, 2)
    }

    final_json = {
        "suspicious_accounts": suspicious_accounts,
        "fraud_rings": fraud_rings,
        "summary": summary
    }

    return final_json


# ====================================================
# SAVE JSON (DOWNLOAD BUTTON USES THIS)
# ====================================================
def save_json(final_json, path="outputs/result.json"):

    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(path, "w") as f:
        json.dump(final_json, f, indent=2)
