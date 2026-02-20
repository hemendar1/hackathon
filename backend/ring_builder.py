def build_rings_and_assign_ids(detections, suspicious_accounts):

    ring_counter = 1
    fraud_rings = []
    account_to_ring = {}

    def get_ring_id():
        nonlocal ring_counter
        rid = f"RING_{ring_counter:03}"
        ring_counter += 1
        return rid

    # =============================
    # 1. NORMAL RING DETECTIONS
    # =============================

    for cycle in detections.get("cycles", []):
        ring_id = get_ring_id()
        members = cycle["members"]

        for acc in members:
            account_to_ring[acc] = ring_id

        fraud_rings.append({
            "ring_id": ring_id,
            "member_accounts": members,
            "pattern_type": "cycle",
            "risk_score": 95.0
        })

    for cluster in detections.get("fan_in", []):
        ring_id = get_ring_id()
        members = cluster.get("members", [])

        for acc in members:
            account_to_ring[acc] = ring_id

        fraud_rings.append({
            "ring_id": ring_id,
            "member_accounts": members,
            "pattern_type": "fan_in",
            "risk_score": 85.0
        })

    for cluster in detections.get("fan_out", []):
        ring_id = get_ring_id()
        members = cluster.get("members", [])

        for acc in members:
            account_to_ring[acc] = ring_id

        fraud_rings.append({
            "ring_id": ring_id,
            "member_accounts": members,
            "pattern_type": "fan_out",
            "risk_score": 85.0
        })

    for chain in detections.get("shell_chains", []):
        ring_id = get_ring_id()
        members = chain.get("members", [])

        for acc in members:
            account_to_ring[acc] = ring_id

        fraud_rings.append({
            "ring_id": ring_id,
            "member_accounts": members,
            "pattern_type": "shell_chain",
            "risk_score": 75.0
        })

    # =====================================================
    # ⭐⭐ MOST IMPORTANT FIX FOR SMALL DATASET ⭐⭐
    # ADD SOLO ACCOUNTS IF NO PATTERN DETECTED
    # =====================================================

    if len(fraud_rings) == 0:

        for acc in suspicious_accounts:

            solo_ring = get_ring_id()

            fraud_rings.append({
                "ring_id": solo_ring,
                "member_accounts": [acc["account_id"]],
                "pattern_type": "isolated_account",
                "risk_score": acc["suspicion_score"]
            })

            account_to_ring[acc["account_id"]] = solo_ring

    # =============================
    # 3. ASSIGN RING ID BACK
    # =============================

    for acc in suspicious_accounts:
        acc["ring_id"] = account_to_ring.get(
            acc["account_id"],
            "RING_UNKNOWN"
        )

    return suspicious_accounts, fraud_rings
