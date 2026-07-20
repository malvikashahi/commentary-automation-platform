import streamlit as st
import requests
import os

API_BASE = "http://localhost:8000/api"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.title("📁 File Upload Center")
st.markdown("Upload your strategy source files to begin commentary generation.")

# ── Strategy Selection ───────────────────────────────────────
try:
    strategies = requests.get(f"{API_BASE}/strategies", timeout=5).json()
    strategy_names = {s["strategy_name"]: s["strategy_id"] for s in strategies}
except Exception:
    strategy_names = {"Large-Cap Growth (LCG)": "LCG", "GPAR": "GPAR"}

col1, col2 = st.columns(2)

with col1:
    selected_strategy_name = st.selectbox(
        "📊 Select Strategy", list(strategy_names.keys())
    )
    strategy_id = strategy_names[selected_strategy_name]

with col2:
    account_id = st.text_input(
        "🏷️ Account ID",
        value="4686",
        help="Enter the account code (e.g. 4686, LCG)"
    )

period = st.text_input("📅 Reporting Period", value="2Q26")

st.markdown("---")

# ── File Upload Sections ─────────────────────────────────────
st.subheader("📎 Upload Source Files")

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Attribution", "💼 Purchase & Sales",
    "📊 Performance", "📝 Lead Commentary"
])

with tab1:
    st.markdown("**Attribution File** — Account-level sector and security attribution.")
    attr_file = st.file_uploader(
        "Upload Attribution (.xlsx)", type=["xlsx", "xls"],
        key="attribution"
    )
    if attr_file:
        st.success(f"✅ {attr_file.name} ready ({attr_file.size:,} bytes)")

with tab2:
    st.markdown("**Purchase & Sales File** — Transaction rationales for the period.")
    ps_file = st.file_uploader(
        "Upload P&S (.xlsx)", type=["xlsx", "xls"],
        key="ps"
    )
    if ps_file:
        st.success(f"✅ {ps_file.name} ready ({ps_file.size:,} bytes)")

with tab3:
    st.markdown("**Performance File** — Strategy-level returns vs benchmark.")
    perf_file = st.file_uploader(
        "Upload Performance (.xlsx)", type=["xlsx", "xls"],
        key="performance"
    )
    if perf_file:
        st.success(f"✅ {perf_file.name} ready ({perf_file.size:,} bytes)")

with tab4:
    st.markdown("**Lead Commentary** — Strategy-level Word document template.")
    lead_file = st.file_uploader(
        "Upload Lead Commentary (.docx)", type=["docx", "doc"],
        key="lead"
    )
    if lead_file:
        st.success(f"✅ {lead_file.name} ready ({lead_file.size:,} bytes)")

st.markdown("---")

# ── Upload Button ────────────────────────────────────────────
uploaded_files = {
    "attribution": attr_file,
    "purchase_sales": ps_file,
    "performance": perf_file,
    "lead_commentary": lead_file
}

ready_count = sum(1 for f in uploaded_files.values() if f is not None)
st.markdown(f"**Files ready:** {ready_count} / 4")

if st.button("🚀 Upload & Continue", disabled=ready_count == 0):
    saved_paths = {}

    with st.spinner("Uploading files..."):
        for ftype, fobj in uploaded_files.items():
            if fobj is not None:
                save_path = os.path.join(UPLOAD_DIR, f"{account_id}_{ftype}_{fobj.name}")
                with open(save_path, "wb") as f:
                    f.write(fobj.read())
                saved_paths[ftype] = save_path

    # Save to session state
    st.session_state["uploaded_paths"] = saved_paths
    st.session_state["account_id"] = account_id
    st.session_state["strategy_id"] = strategy_id
    st.session_state["period"] = period

    st.success(f"✅ {len(saved_paths)} files uploaded successfully!")
    st.info("➡️ Proceed to **Validation** tab to run data quality checks.")
  
