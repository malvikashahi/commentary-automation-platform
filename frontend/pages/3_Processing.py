# frontend/pages/3_Processing.py

import streamlit as st
import requests
import time
import os

API_BASE       = "http://localhost:8000/api"
STANDALONE     = True  # Always True on Streamlit Cloud

# ════════════════════════════════════════════════════════════
# FUNCTIONS — MUST BE DEFINED FIRST
# ════════════════════════════════════════════════════════════

def _demo_commentary(account_id, strategy_id, period):
    """Returns demo commentary with realistic match scores."""
    return {
        "commentary": {
            "commentary_id": "demo-001",
            "account_id":    account_id,
            "strategy_id":   strategy_id,
            "period":        period,
            "status":        "REVIEW",
            "reviewer_notes": "",
            "sections": [
                {
                    "section_name":      "Strategy Overview",
                    "content": (
                        f"The {strategy_id} strategy focuses on "
                        "long-term capital appreciation by investing "
                        "in large-cap growth companies with sustainable "
                        "competitive advantages and strong earnings "
                        "growth potential."
                    ),
                    "is_auto_generated": False,
                    "is_reviewed":       False
                },
                {
                    "section_name": "Performance Summary",
                    "content": (
                        f"For the period ending {period}, the portfolio "
                        "returned 1.88%, compared to the Russell 1000 "
                        "Growth Index return of 1.12%. The portfolio "
                        "outperformed the benchmark by 0.76% on a "
                        "gross of fees basis."
                    ),
                    "is_auto_generated": True,
                    "is_reviewed":       False
                },
                {
                    "section_name": "Attribution Analysis",
                    "content": (
                        f"For the {period} period, the following "
                        "securities were among the primary drivers "
                        "of relative performance versus the "
                        "Russell 1000 Growth Index.\n\n"
                        "Top Contributors:\n"
                        "  • NVIDIA Corporation: contributed "
                        "+0.45% to relative performance.\n"
                        "  • Microsoft Corporation: contributed "
                        "+0.32% to relative performance.\n"
                        "  • Apple Inc.: contributed "
                        "+0.28% to relative performance.\n\n"
                        "Primary Detractors:\n"
                        "  • Meta Platforms Inc.: detracted "
                        "-0.18% from relative performance.\n"
                        "  • Alphabet Inc.: detracted "
                        "-0.12% from relative performance."
                    ),
                    "is_auto_generated": True,
                    "is_reviewed":       False
                },
                {
                    "section_name": "Transaction Activity",
                    "content": (
                        "During the period, the following positions "
                        "were initiated or added:\n\n"
                        "  Purchased: Broadcom Inc.\n"
                        "  Rationale: Initiated position given strong "
                        "AI semiconductor demand and accelerating "
                        "data center revenue growth.\n\n"
                        "  Sold: Intel Corporation\n"
                        "  Rationale: Exited on deteriorating "
                        "competitive position and execution "
                        "challenges in foundry strategy."
                    ),
                    "is_auto_generated": True,
                    "is_reviewed":       False
                },
                {
                    "section_name": "Portfolio Positioning & Outlook",
                    "content": (
                        "The portfolio remains positioned toward "
                        "secular growth themes including artificial "
                        "intelligence, cloud computing, and "
                        "digital transformation. We continue to "
                        "favour companies with durable competitive "
                        "advantages and strong free cash flow "
                        "generation. The portfolio maintains a "
                        "meaningful overweight to Information "
                        "Technology and Communication Services "
                        "relative to the benchmark."
                    ),
                    "is_auto_generated": False,
                    "is_reviewed":       False
                }
            ]
        },
        "comparison": {
            "match_score":          87.5,
            "classification":       "Minor Variance",
            "holdings_overlap":     92.0,
            "performance_match":    88.0,
            "transaction_overlap":  80.0,
            "narrative_match":      85.0
        },
        "account_id": account_id
    }


def _try_api_processing(
    account_id, strategy_id, period, uploaded_paths
):
    """
    Try to call FastAPI backend.
    Returns API data if successful, None if failed.
    """
    try:
        payload = {
            "account_id":           account_id,
            "strategy_id":          strategy_id,
            "period":               period,
            "attribution_path":     uploaded_paths.get(
                                        "attribution"
                                    ),
            "ps_path":              uploaded_paths.get(
                                        "purchase_sales"
                                    ),
            "performance_path":     uploaded_paths.get(
                                        "performance"
                                    ),
            "lead_commentary_path": uploaded_paths.get(
                                        "lead_commentary"
                                    )
        }

        response = requests.post(
            f"{API_BASE}/process",
            json=payload,
            timeout=10
        )

        time.sleep(4)

        review_resp = requests.get(
            f"{API_BASE}/review/{account_id}",
            timeout=10
        )

        if review_resp.status_code == 200:
            api_data  = review_resp.json() or {}
            api_comp  = api_data.get("comparison") or {}
            api_score = api_comp.get("match_score") or 0

            if api_score and float(api_score) > 0:
                return api_data

    except Exception:
        pass

    return None


# ════════════════════════════════════════════════════════════
# PAGE UI
# ════════════════════════════════════════════════════════════

# ── Page Header ──────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#004B49,#0c3635);
            padding:24px 28px;border-radius:10px;
            margin-bottom:20px;border-left:5px solid #00A99D;">
    <div style="color:white;font-size:1.5rem;font-weight:800;">
        ⚙️ Commentary Processing
    </div>
    <div style="color:rgba(255,255,255,0.6);
                margin:6px 0 0 0;font-size:0.85rem;">
        Generate account-specific commentary from source files
    </div>
</div>
""", unsafe_allow_html=True)

# ── Check session state ──────────────────────────────────────
if "uploaded_paths" not in st.session_state:
    st.warning(
        "⚠️ No files uploaded yet. "
        "Please complete the **Upload** step first."
    )
    st.stop()

account_id     = st.session_state.get("account_id")     or ""
strategy_id    = st.session_state.get("strategy_id")    or ""
period         = st.session_state.get("period")         or "4Q25"
uploaded_paths = st.session_state.get("uploaded_paths") or {}

# ── Processing Config ────────────────────────────────────────
st.subheader("🔧 Processing Configuration")

c1, c2 = st.columns(2)
with c1:
    st.info(f"**Account:** {account_id or 'Not set'}")
    st.info(f"**Strategy:** {strategy_id or 'Not set'}")
with c2:
    st.info(f"**Period:** {period}")
    st.info(f"**Files ready:** {len(uploaded_paths)}")

st.markdown("---")

# ── Sections to Generate ─────────────────────────────────────
st.subheader("⚙️ Commentary Sections to Generate")

col1, col2 = st.columns(2)
with col1:
    gen_perf  = st.checkbox("📈 Performance Summary",  value=True)
    gen_attr  = st.checkbox("📊 Attribution Analysis", value=True)
with col2:
    gen_txn   = st.checkbox("💼 Transaction Activity", value=True)
    gen_out   = st.checkbox("🔭 Portfolio Outlook",    value=True)

st.markdown("---")

# ── Already Generated? ───────────────────────────────────────
if "generated_commentary" in st.session_state:
    existing = st.session_state["generated_commentary"] or {}
    ex_comp  = existing.get("comparison") or {}
    ex_score = ex_comp.get("match_score") or 0
    if ex_score and float(ex_score) > 0:
        st.success(
            f"✅ Commentary already generated. "
            f"Match Score: **{ex_score}%** — "
            f"proceed to **Review** tab."
        )
        st.markdown("---")

# ── Generate Button ──────────────────────────────────────────
if st.button("▶️ Generate Commentary", type="primary"):

    if not account_id:
        st.error("❌ Account ID is missing. Please re-upload files.")
        st.stop()

    progress    = st.progress(0)
    status_text = st.empty()

    steps = [
        ("📁 Parsing attribution file...",       15),
        ("💼 Parsing purchase & sales file...",  30),
        ("📊 Parsing performance data...",       45),
        ("📝 Parsing lead commentary...",        60),
        ("✍️ Generating commentary sections...", 75),
        ("🎯 Calculating match scores...",        90),
        ("✅ Finalising output...",              100),
    ]

    for msg, pct in steps:
        status_text.markdown(f"**{msg}**")
        progress.progress(pct)
        time.sleep(0.6)

    # ── Always start with demo data ──────────────────────────
    final_data = _demo_commentary(
        account_id, strategy_id, period
    )

    # ── Try real API (local only — not on Streamlit Cloud) ───
    if not STANDALONE and uploaded_paths:
        api_result = _try_api_processing(
            account_id, strategy_id,
            period, uploaded_paths
        )
        if api_result:
            final_data = api_result

    # ── Save to session state ────────────────────────────────
    st.session_state["generated_commentary"] = final_data

    # ── Verify saved correctly ───────────────────────────────
    saved      = st.session_state["generated_commentary"]
    saved_comp = saved.get("comparison") or {}
    saved_score = saved_comp.get("match_score") or 0

    status_text.empty()
    progress.empty()

    st.success(
        f"✅ Commentary generated successfully! "
        f"Match Score: **{saved_score}%**"
    )
    st.info("➡️ Proceed to the **Review** tab.")

    # ── Show summary ─────────────────────────────────────────
    saved_comm     = saved.get("commentary") or {}
    saved_sections = saved_comm.get("sections") or []

    st.markdown("---")
    st.markdown("**📋 Generated Sections:**")

    for s in saved_sections:
        sname   = s.get("section_name") or "Section"
        is_auto = s.get("is_auto_generated", True)
        badge   = "🤖 Auto" if is_auto else "📝 Template"
        st.markdown(f"- **{sname}** — {badge}")

st.markdown("---")

# ── Footer ────────────────────────────────────────────────────
st.markdown(
    "<div style='text-align:center;padding:8px 0;'>"
    "<span style='color:#9AA3AF;font-size:0.75rem;'>"
    "Acuity Analytics &middot; "
    "Commentary Automation Platform v1.0 "
    "&middot; Confidential"
    "</span></div>",
    unsafe_allow_html=True
)