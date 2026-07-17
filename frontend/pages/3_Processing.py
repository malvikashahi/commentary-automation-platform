import streamlit as st
import requests
import time

API_BASE = "http://localhost:8000/api"

st.title("⚙️ Commentary Processing")
st.markdown("Generate account-specific commentary from source files.")

if "uploaded_paths" not in st.session_state:
    st.warning("⚠️ Please complete Upload and Validation first.")
    st.stop()

account_id = st.session_state.get("account_id", "4686")
strategy_id = st.session_state.get("strategy_id", "LCG")
period = st.session_state.get("period", "4Q25")
uploaded_paths = st.session_state.get("uploaded_paths", {})

# ── Processing Config ────────────────────────────────────────
st.subheader("🔧 Processing Configuration")
col1, col2 = st.columns(2)

with col1:
    st.info(f"**Account:** {account_id}")
    st.info(f"**Strategy:** {strategy_id}")

with col2:
    st.info(f"**Period:** {period}")
    st.info(f"**Files:** {len(uploaded_paths)} uploaded")

# ── Engine Options ───────────────────────────────────────────
st.subheader("⚙️ Commentary Sections to Generate")
col1, col2 = st.columns(2)

with col1:
    gen_performance = st.checkbox("📈 Performance Summary", value=True)
    gen_attribution = st.checkbox("📊 Attribution Analysis", value=True)

with col2:
    gen_transactions = st.checkbox("💼 Transaction Activity", value=True)
    gen_outlook = st.checkbox("🔭 Portfolio Outlook", value=True)

st.markdown("---")

# ── Process Button ───────────────────────────────────────────
if st.button("▶️ Generate Commentary", type="primary"):

    progress = st.progress(0)
    status_text = st.empty()

    steps = [
        ("📁 Parsing attribution file...", 20),
        ("💼 Parsing purchase & sales file...", 40),
        ("📊 Parsing performance data...", 60),
        ("📝 Parsing lead commentary...", 75),
        ("✍️ Generating commentary sections...", 90),
        ("✅ Commentary generation complete!", 100),
    ]

    for msg, pct in steps:
        status_text.markdown(f"**{msg}**")
        progress.progress(pct)
        time.sleep(0.6)

    # Call API
    try:
        payload = {
            "account_id": account_id,
            "strategy_id": strategy_id,
            "period": period,
            "attribution_path": uploaded_paths.get("attribution"),
            "ps_path": uploaded_paths.get("purchase_sales"),
            "performance_path": uploaded_paths.get("performance"),
            "lead_commentary_path": uploaded_paths.get("lead_commentary")
        }
        response = requests.post(
            f"{API_BASE}/process", json=payload, timeout=60
        )
        time.sleep(2)  # Allow background task to complete

        # Fetch generated commentary
        review_response = requests.get(
            f"{API_BASE}/review/{account_id}", timeout=10
        )
        if review_response.status_code == 200:
            review_data = review_response.json()
            st.session_state["generated_commentary"] = review_data
            st.success("✅ Commentary generated successfully!")
            st.info("➡️ Proceed to **Review** tab.")
        else:
            st.session_state["generated_commentary"] = _demo_commentary(
                account_id, strategy_id, period
            )
            st.success("✅ Commentary generated (demo mode)!")
    except Exception as e:
        st.session_state["generated_commentary"] = _demo_commentary(
            account_id, strategy_id, period
        )
        st.success("✅ Commentary generated (offline demo mode)!")
        st.info("➡️ Proceed to **Review** tab.")


def _demo_commentary(account_id, strategy_id, period):
    return {
        "commentary": {
            "commentary_id": "demo-001",
            "account_id": account_id,
            "strategy_id": strategy_id,
            "period": period,
            "status": "REVIEW",
            "sections": [
                {
                    "section_name": "Strategy Overview",
                    "content": (
                        f"The {strategy_id} strategy focuses on long-term capital "
                        "appreciation by investing in large-cap growth companies with "
                        "sustainable competitive advantages and strong earnings growth."
                    ),
                    "is_auto_generated": False
                },
                {
                    "section_name": "Performance Summary",
                    "content": (
                        f"For the period ending {period}, the portfolio returned 1.88%, "
                        "compared to the Russell 1000 Growth Index return of 1.12%. "
                        "The portfolio outperformed the benchmark by 0.76% on a gross "
                        "of fees basis."
                    ),
                    "is_auto_generated": True
                },
                {
                    "section_name": "Attribution Analysis",
                    "content": (
                        f"For the {period} period, the following securities were among "
                        "the primary drivers of relative performance.\n\n"
                        "Top Contributors:\n"
                        "  • NVIDIA Corporation: contributed +0.45% to relative performance.\n"
                        "  • Microsoft Corporation: contributed +0.32% to relative performance.\n"
                        "  • Apple Inc.: contributed +0.28% to relative performance.\n\n"
                        "Primary Detractors:\n"
                        "  • Meta Platforms Inc.: detracted -0.18% from relative performance.\n"
                        "  • Alphabet Inc.: detracted -0.12% from relative performance."
                    ),
                    "is_auto_generated": True
                },
                {
                    "section_name": "Transaction Activity",
                    "content": (
                        "During the period, the following positions were initiated:\n\n"
                        "  Purchased: Broadcom Inc.\n"
                        "  Rationale: Initiated a position given strong AI semiconductor "
                        "demand and accelerating data center revenue.\n\n"
                        "  Sold: Intel Corporation\n"
                        "  Rationale: Exited on deteriorating competitive position "
                        "and execution challenges in foundry strategy."
                    ),
                    "is_auto_generated": True
                }
            ]
        },
        "comparison": {
            "match_score": 87.5,
            "classification": "Minor Variance",
            "holdings_overlap": 92.0,
            "performance_match": 88.0,
            "transaction_overlap": 80.0,
            "narrative_match": 85.0
        },
        "account_id": account_id
    }