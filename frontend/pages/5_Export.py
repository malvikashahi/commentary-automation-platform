# frontend/pages/5_Export.py

import streamlit as st
import os
import time
from datetime import datetime

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
.export-card {
    background: white;
    border: 1px solid #DDE1E7;
    border-radius: 10px;
    padding: 20px 24px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(0,75,73,0.06);
}
.format-badge-docx {
    background: #E8F4FD; color: #1A6FB0;
    padding: 3px 10px; border-radius: 99px;
    font-size: 0.75rem; font-weight: 700;
    display: inline-block; margin: 6px 0;
}
</style>
""", unsafe_allow_html=True)

# ── Page Header ──────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#004B49,#0c3635);
            padding:24px 28px;border-radius:10px;
            margin-bottom:20px;border-left:5px solid #00A99D;">
    <div style="color:white;font-size:1.5rem;font-weight:800;">
        📤 Export Center
    </div>
    <div style="color:rgba(255,255,255,0.6);
                margin:6px 0 0 0;font-size:0.85rem;">
        Download generated commentaries as Word documents
    </div>
</div>
""", unsafe_allow_html=True)

# ── Check session state ──────────────────────────────────────
has_commentary = "generated_commentary" in st.session_state
has_approved   = False
account_id     = ""
strategy_id    = ""
period         = ""
sections       = []

if has_commentary:
    _data        = st.session_state["generated_commentary"] or {}
    _comm        = _data.get("commentary") or {}
    account_id   = _comm.get("account_id")  or ""
    strategy_id  = _comm.get("strategy_id") or ""
    period       = _comm.get("period")      or "4Q25"
    sections     = _comm.get("sections")    or []
    has_approved = _comm.get("status") == "APPROVED"

# ── Status Overview ──────────────────────────────────────────
st.subheader("📊 Export Status")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric(
        "Commentary Ready",
        "✅ Yes" if has_commentary else "❌ No"
    )
with c2:
    st.metric(
        "Approval Status",
        "✅ Approved" if has_approved else "⏳ Pending"
    )
with c3:
    st.metric("Account", account_id or "—")
with c4:
    st.metric("Period", period or "—")

st.markdown("---")

# ── Guard ────────────────────────────────────────────────────
if not has_commentary:
    st.warning(
        "⚠️ No commentary available. "
        "Please complete "
        "**Upload → Validation → Processing → Review** first."
    )
    st.stop()

if not has_approved:
    st.warning(
        "⚠️ Commentary not yet approved. "
        "Please go to **Review** and click "
        "**Approve Commentary** first."
    )
    st.info("💡 You can still export a **draft** version below.")

st.subheader("📎 Export Options")

# ── Format Card — DOCX Only ──────────────────────────────────
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("""
    <div class="export-card">
        <div style="font-size:2rem;">📝</div>
        <div style="font-weight:700;color:#004B49;
                    font-size:1rem;margin-top:6px;">
            Word Document
        </div>
        <span class="format-badge-docx">.DOCX</span>
        <div style="font-size:0.8rem;color:#9AA3AF;
                    margin-top:6px;">
            Editable Microsoft Word format.<br/>
            Best for review, editing and distribution.
        </div>
    </div>
    """, unsafe_allow_html=True)
    export_docx = st.button(
        "📥 Export as DOCX",
        type="primary",
        use_container_width=True,
        key="btn_docx"
    )

st.markdown("---")


# ════════════════════════════════════════════════════════════
# DOCX BUILDER FUNCTION
# ════════════════════════════════════════════════════════════

def build_docx(suffix=""):
    """Build and save a DOCX file. Returns (file_path, filename)."""
    from docx import Document as DocxDocument
    from docx.shared import Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    doc = DocxDocument()

    # ── Cover page ───────────────────────────────────────────
    title = doc.add_heading('Portfolio Commentary', 0)
    if title.runs:
        title.runs[0].font.color.rgb = RGBColor(0x00, 0x4B, 0x49)
        title.runs[0].font.size      = Pt(22)

    doc.add_paragraph(f"Account:   {account_id}")
    doc.add_paragraph(f"Strategy:  {strategy_id}")
    doc.add_paragraph(f"Period:    {period}")
    doc.add_paragraph(
        f"Generated: "
        f"{datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
    )
    doc.add_paragraph(
        f"Status:    "
        f"{'APPROVED' if has_approved else 'DRAFT'}"
    )

    disc = doc.add_paragraph(
        "FOR INSTITUTIONAL USE ONLY — NOT FOR PUBLIC DISTRIBUTION"
    )
    if disc.runs:
        disc.runs[0].italic = True
        disc.runs[0].font.size = Pt(8)
        disc.runs[0].font.color.rgb = RGBColor(0x9A, 0xA3, 0xAF)

    doc.add_page_break()

    # ── Commentary sections ──────────────────────────────────
    for section in sections:
        sname   = section.get("section_name") or "Section"
        content = section.get("content")      or ""
        is_auto = section.get("is_auto_generated", True)

        heading = doc.add_heading(sname, level=2)
        if heading.runs:
            heading.runs[0].font.color.rgb = RGBColor(
                0x00, 0x4B, 0x49
            )
            heading.runs[0].font.size = Pt(12)
            heading.runs[0].bold      = True

        if is_auto:
            lbl = doc.add_paragraph("[ Auto-Generated ]")
            if lbl.runs:
                lbl.runs[0].italic = True
                lbl.runs[0].font.size = Pt(8)
                lbl.runs[0].font.color.rgb = RGBColor(
                    0x9A, 0xA3, 0xAF
                )

        for line in content.split('\n'):
            if line.strip():
                p = doc.add_paragraph(line.strip())
                p.paragraph_format.space_after  = Pt(4)
                p.paragraph_format.space_before = Pt(0)
                if p.runs:
                    p.runs[0].font.size = Pt(10.5)

        doc.add_paragraph()

    # ── Footer ───────────────────────────────────────────────
    sec_obj = doc.sections[0]
    footer  = sec_obj.footer
    fp      = footer.paragraphs[0]
    fp.text = (
        f"Acuity Analytics | {strategy_id} | "
        f"{period} | Confidential | "
        f"Generated {datetime.now().strftime('%d %b %Y')}"
    )
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if fp.runs:
        fp.runs[0].font.size = Pt(8)
        fp.runs[0].font.color.rgb = RGBColor(0x9A, 0xA3, 0xAF)

    # ── Save ─────────────────────────────────────────────────
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = (
        f"{account_id}_{strategy_id}_{period}_"
        f"Commentary_{timestamp}{suffix}.docx"
    )
    file_path = os.path.join(OUTPUT_DIR, filename)
    doc.save(file_path)

    return file_path, filename


# ════════════════════════════════════════════════════════════
# DOCX EXPORT
# ════════════════════════════════════════════════════════════
if export_docx:
    with st.spinner("📝 Generating Word document..."):
        try:
            file_path, filename = build_docx()
            time.sleep(0.3)

            st.success(f"✅ DOCX generated: **{filename}**")

            with open(file_path, "rb") as f:
                docx_bytes = f.read()

            st.download_button(
                label="📥 Click Here to Download DOCX",
                data=docx_bytes,
                file_name=filename,
                mime=(
                    "application/vnd.openxmlformats-"
                    "officedocument.wordprocessingml.document"
                ),
                use_container_width=True,
                key="dl_docx"
            )

            if "export_history" not in st.session_state:
                st.session_state["export_history"] = []
            st.session_state["export_history"].append({
                "filename":  filename,
                "format":    "DOCX",
                "account":   account_id,
                "period":    period,
                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "path": file_path
            })

        except Exception as e:
            st.error(f"❌ DOCX Export failed: {str(e)}")
            st.exception(e)


st.markdown("---")

# ════════════════════════════════════════════════════════════
# EXPORT HISTORY
# ════════════════════════════════════════════════════════════
st.subheader("📋 Export History")

history = st.session_state.get("export_history", [])

if not history:
    st.info(
        "No exports yet. "
        "Click Export as DOCX above to generate a file."
    )
else:
    for i, item in enumerate(reversed(history)):
        fmt = item.get("format", "DOCX")
        st.markdown(f"""
        <div class="export-card">
            <div style="display:flex;
                        justify-content:space-between;
                        align-items:center;">
                <div>
                    <span class="format-badge-docx">DOCX</span>
                    <span style="font-weight:700;
                                 color:#004B49;
                                 margin-left:8px;
                                 font-size:0.9rem;">
                        {item.get("filename", "Unknown")}
                    </span>
                </div>
                <div style="font-size:0.78rem;color:#9AA3AF;">
                    {item.get("timestamp", "")}
                </div>
            </div>
            <div style="font-size:0.78rem;color:#9AA3AF;
                        margin-top:6px;">
                Account: <b>{item.get("account", "")}</b>
                &nbsp;|&nbsp;
                Period: <b>{item.get("period", "")}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

        fp = item.get("path", "")
        if fp and os.path.exists(fp):
            with open(fp, "rb") as f:
                fb = f.read()
            st.download_button(
                label="📥 Re-download DOCX",
                data=fb,
                file_name=item.get(
                    "filename", "export.docx"
                ),
                mime=(
                    "application/vnd.openxmlformats-"
                    "officedocument.wordprocessingml.document"
                ),
                key=f"redl_{i}_{item.get('timestamp', i)}"
            )

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