# frontend/app.py

import streamlit as st
from datetime import datetime

# ── Dynamic Current Quarter ──────────────────────────────────
def get_current_quarter():
    now     = datetime.now()
    year    = now.year
    month   = now.month
    quarter = (month - 1) // 3 + 1
    return f"Q{quarter} {year}"

CURRENT_QUARTER = get_current_quarter()

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Commentary Automation Platform",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stAppDeployButton {visibility: hidden;}
[data-testid="stAppViewMain"] {
    padding-top: 0rem !important;
}
.main .block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
    max-width: 100% !important;
}

header {
    background-color: transparent !important;
    height: 0px !important;
}
header [data-testid="stHeaderActionElements"] {
    visibility: hidden !important;
}
header [data-testid="stSidebarCollapseAction"] {
    visibility: visible !important;
    background-color: #004B49 !important;
    border-radius: 4px !important;
    margin-left: 10px !important;
    position: fixed !important;
    top: 12px !important;
    z-index: 999999 !important;
}
header [data-testid="stSidebarCollapseAction"] svg {
    fill: white !important;
    color: white !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,#004B49,#0d3060
    ) !important;
}
[data-testid="stSidebar"] * {
    color: white !important;
}
.stButton > button {
    background-color: #00A99D !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
}
.stButton > button:hover {
    background-color: #007F76 !important;
}
[data-testid="metric-container"] {
    background: white !important;
    border: 1px solid #DDE1E7 !important;
    border-radius: 8px !important;
    box-shadow: 0 2px 8px rgba(0,75,73,0.08) !important;
}
h1, h2, h3 {color: #004B49 !important;}
</style>
""", unsafe_allow_html=True)

# ── Top Nav Bar ──────────────────────────────────────────────
st.markdown("""
<div style="background:#004B49;padding:16px 28px;
            border-radius:8px;margin-bottom:20px;
            border-bottom:3px solid #00A99D;
            display:flex;align-items:center;
            justify-content:flex-start;">
    <div>
        <div style="color:white;font-size:1.3rem;
                    font-weight:800;letter-spacing:0.04em;
                    text-transform:uppercase;line-height:1;">
            Acuity Analytics
        </div>
        <div style="color:rgba(255,255,255,0.7);
                    font-size:0.65rem;letter-spacing:0.12em;
                    text-transform:uppercase;
                    margin-top:4px;line-height:1;">
            Intelligence &middot; Insight &middot; Impact
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:16px 0 10px 0;">
        <div style="color:white;font-size:1.15rem;
                    font-weight:800;letter-spacing:0.04em;
                    text-transform:uppercase;">
            Acuity Analytics
        </div>
        <div style="color:rgba(255,255,255,0.8);
                    font-size:0.85rem;font-weight:600;
                    margin-top:6px;">
            Commentary Platform
        </div>
        <div style="color:#00A99D;font-size:0.6rem;
                    letter-spacing:0.12em;
                    text-transform:uppercase;
                    margin-top:3px;">
            Automation Suite v1.0
        </div>
    </div>
    <hr style="border:none;border-top:1px solid
               rgba(255,255,255,0.15);margin:8px 0 12px 0;"/>
    <div style="font-size:0.62rem;
                color:rgba(255,255,255,0.4);
                letter-spacing:0.1em;
                text-transform:uppercase;
                margin-bottom:6px;padding:0 4px;">
        Navigation
    </div>
    """, unsafe_allow_html=True)

# ── Hero Banner — Dynamic Quarter ───────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,#004B49,#0c3635);
            padding:32px 36px;border-radius:12px;
            margin-bottom:24px;border-left:5px solid #00A99D;
            box-shadow:0 4px 20px rgba(0,75,73,0.20);">
    <div style="color:white;font-size:1.8rem;font-weight:800;
                margin-bottom:8px;">
        📝 Commentary Automation Platform
    </div>
    <div style="color:rgba(255,255,255,0.8);font-size:0.95rem;
                line-height:1.6;margin-bottom:16px;
                font-weight:400;font-family:sans-serif;">
        Automated portfolio commentary generation
        for Client Investment Strategies
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;">
        <span style="background:rgba(0,169,157,0.18);
                     color:#00A99D;padding:4px 12px;
                     border-radius:99px;font-size:0.72rem;
                     font-weight:700;
                     border:1px solid rgba(0,169,157,0.35);">
            2 Strategies
        </span>
        <span style="background:rgba(0,169,157,0.18);
                     color:#00A99D;padding:4px 12px;
                     border-radius:99px;font-size:0.72rem;
                     font-weight:700;
                     border:1px solid rgba(0,169,157,0.35);">
            260 Accounts
        </span>
        <span style="background:rgba(200,169,81,0.18);
                     color:#C8A951;padding:4px 12px;
                     border-radius:99px;font-size:0.72rem;
                     font-weight:700;
                     border:1px solid rgba(200,169,81,0.35);">
            {CURRENT_QUARTER} Active Period
        </span>
        <span style="background:rgba(255,255,255,0.10);
                     color:rgba(255,255,255,0.8);
                     padding:4px 12px;border-radius:99px;
                     font-size:0.72rem;font-weight:700;
                     border:1px solid rgba(255,255,255,0.20);">
            Powered by Acuity Analytics
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Stats ────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Strategies", "2",   delta="Active")
with col2:
    st.metric("👥 Accounts",  "260",  delta="+12 this quarter")
with col3:
    st.metric("✅ Generated", "0",    delta="Ready to process")
with col4:
    st.metric("📤 Exported",  "0",    delta="Pending")

st.markdown("---")

# ── Sidebar Cache Clear Button ───────────────────────────────
with st.sidebar:
    st.markdown(
        "<hr style='border:none;border-top:1px solid "
        "rgba(255,255,255,0.15);margin:12px 0;'/>",
        unsafe_allow_html=True
    )
    if st.button("🔄 Clear Cache & Restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.cache_data.clear()
        st.rerun()

# ── Workflow Steps ───────────────────────────────────────────
st.markdown(
    "<h3 style='color:#004B49;'>"
    "🚀 Get Started — Follow the Workflow</h3>",
    unsafe_allow_html=True
)

steps = [
    ("1", "📁 Upload",
     "Select strategy and upload Attribution, P&S, "
     "Performance and Lead Commentary files."),
    ("2", "✅ Validate",
     "Run the 5-layer validation engine to check "
     "data quality and file integrity."),
    ("3", "⚙️ Process",
     "Generate account-specific commentary "
     "using the automation engine."),
    ("4", "🔍 Review",
     "Review generated commentary side-by-side "
     "with match score analysis."),
    ("5", "📤 Export",
     "Approve and download commentary as DOCX."),
]

for num, title, desc in steps:
    st.markdown(
        "<div style='background:white;"
        "border:1px solid #DDE1E7;"
        "border-left:4px solid #00A99D;"
        "border-radius:8px;"
        "padding:12px 16px;margin-bottom:8px;'>"
        "<div style='display:flex;align-items:center;gap:12px;'>"
        "<div style='background:#004B49;color:white;"
        "min-width:26px;height:26px;border-radius:50%;"
        "display:flex;align-items:center;"
        "justify-content:center;"
        "font-size:0.78rem;font-weight:800;'>"
        + num +
        "</div><div>"
        "<span style='font-weight:700;color:#004B49;"
        "font-size:0.92rem;'>" + title + "</span>"
        "<span style='color:#5A6472;font-size:0.83rem;"
        "margin-left:6px;'>&mdash; " + desc + "</span>"
        "</div></div></div>",
        unsafe_allow_html=True
    )

st.markdown("---")

# ── Footer ───────────────────────────────────────────────────
st.markdown(
    "<div style='text-align:center;padding:10px 0 4px 0;'>"
    "<span style='color:#9AA3AF;font-size:0.75rem;'>"
    "Powered by "
    "<strong style='color:#004B49;'>Acuity Analytics</strong>"
    " &middot; Commentary Automation Platform v1.0"
    " &middot; Confidential"
    "</span></div>",
    unsafe_allow_html=True
)