import pandas as pd
import numpy as np
import random
import uuid

ROWS = 350000
USERS = 80_000

def generate_dataset(file_name, laundering=True):
    data = []

    for i in range(ROWS):
        user_id = f"USER_{random.randint(1, USERS)}"
        factors = []

        amount = np.random.exponential(scale=20000)
        tx_per_day = random.randint(1, 15)
        night_tx = random.randint(0, 3)
        same_receiver = random.randint(0, 4)
        kyc = random.choice([0, 1])
        location_risk = random.choice([0, 1])

        # --- Risk Factors ---
        if amount > 150000: factors.append("High transaction amount")
        if tx_per_day > 10: factors.append("Rapid multiple transactions")
        if night_tx > 1: factors.append("Night transactions")
        if same_receiver > 2: factors.append("Same receiver pattern")
        if kyc == 0: factors.append("KYC not verified")
        if location_risk == 1: factors.append("High risk location")

        # --- Risk Score ---
        score = (
            (amount / 2000) +
            tx_per_day * 3 +
            night_tx * 5 +
            same_receiver * 4 +
            (20 if kyc == 0 else 0) +
            (25 if location_risk else 0)
        )
        score = min(int(score), 100)

        # --- Apply laundering control ---
        if not laundering:
            if score > 70:
                score -= random.randint(20, 40)
                factors = factors[:1]

        # --- Risk Type ---
        if score >= 75 and len(factors) >= 3:
            risk = "HIGH"
        elif score >= 50:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        alert_status = "OPEN" if risk == "HIGH" else "CLOSED"

        data.append([
            f"AML_{uuid.uuid4().hex[:8]}",
            user_id,
            risk,
            score,
            round(min(95, score + random.uniform(-10, 10)), 2),
            ", ".join(factors) if factors else "Normal transaction pattern",
            alert_status
        ])

    df = pd.DataFrame(data, columns=[
        "alert_id", "user_id", "risk_type",
        "risk_score", "ml_confidence",
        "risk_reason", "alert_status"
    ])

    df.to_csv(file_name, index=False)
    print(f"✅ Created {file_name}")

# --- Generate datasets ---
for i in range(1, 26):
    generate_dataset(f"aml_positive_{i}.csv", laundering=True)

for i in range(1, 31):
    generate_dataset(f"aml_clean_{i}.csv", laundering=False)
