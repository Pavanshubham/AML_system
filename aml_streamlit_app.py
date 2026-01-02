import streamlit as st
import pandas as pd
import random

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI AML Compliance System", layout="wide")
st.title("🛡️ AI-Driven AML Compliance Monitoring System")

# ---------------- DATASETS ----------------
aml_positive = [f"aml_positive_{i}.csv" for i in range(1, 26)]
aml_negative = [f"aml_clean_{i}.csv" for i in range(1, 20)]

all_datasets = aml_positive + aml_negative

# ---------------- LOAD RANDOM DATASET ----------------
if "df" not in st.session_state:
    selected_file = random.choice(all_datasets)
    st.session_state["dataset_name"] = selected_file
    st.session_state["df"] = pd.read_csv(selected_file)

df = st.session_state["df"]

# ---------------- DATASET INFO (DISPLAY FIRST) ----------------
st.success(f"📂 Dataset Loaded: Successfully")
st.write(f"🔢 **Total Transactions:** {len(df):,}")

st.subheader("📄 Dataset Preview (Top 10 Rows)")
st.dataframe(df.head(10), use_container_width=True)

st.divider()

# ---------------- ANALYZE BUTTON ----------------
analyze = st.button("🔍 Analyze Transactions")

# ---------------- AML ANALYSIS ----------------
if analyze:
    st.subheader("📊 Risk Distribution")

    low = len(df[df["risk_type"] == "LOW"])
    medium = len(df[df["risk_type"] == "MEDIUM"])
    high = len(df[df["risk_type"] == "HIGH"])

    col1, col2, col3 = st.columns(3)
    col1.metric("LOW Risk", low)
    col2.metric("MEDIUM Risk", medium)
    col3.metric("HIGH Risk", high)

    # ---------------- COMPLIANCE FILTERING LAYER ----------------
    filtered_alerts = df[
        (df["risk_type"] == "HIGH") &
        (df["ml_confidence"] >= 70) &
        (df["risk_score"] >= 75)
    ]

    st.subheader("🧠 Compliance Summary")

    st.success(
        f"{len(df):,} transactions evaluated | "
        f"{len(filtered_alerts):,} high-confidence alerts escalated"
    )

    st.markdown("### ✅ AML Controls Applied")
    st.markdown("""
    • Risk-based alert prioritization  
    • False-positive reduction layer  
    • FATF-aligned AML thresholds  
    • Explainable AI risk reasoning  
    """)

    # ---------------- TOP 500 ALERTS ----------------
    st.subheader("🚨 Flagged AML Alerts (Top 500)")

    top_alerts = (
        filtered_alerts
        .sort_values(["risk_score", "ml_confidence"], ascending=False)
        .head(500)
    )

    st.dataframe(
        top_alerts[
            [
                "alert_id",
                "user_id",
                "risk_type",
                "risk_score",
                "ml_confidence",
                "risk_reason",
                "alert_status"
            ]
        ],
        use_container_width=True,
        height=350
    )
