import streamlit as st
import json
import glob
import os

st.set_page_config(page_title="Agent-Sec Dashboard", layout="wide")
st.title("Agent-Sec — Security Audit Dashboard")

report_files = sorted(glob.glob("reports/report_*.json"), reverse=True)

if not report_files:
    st.warning("No reports found yet. Run the graph first to generate one.")
else:
    reports = []
    for path in report_files:
        with open(path) as f:
            data = json.load(f)
            data["_filename"] = os.path.basename(path)
            reports.append(data)

    st.subheader(f"Run History ({len(reports)} total)")

    table_rows = [
        {
            "File": r["_filename"],
            "Vulnerable": r["is_vulnerable"],
            "Confidence": r["confidence_score"],
            "Vulnerability Type": r["vulnerability_type"],
            "Iterations Used": r["iteration"],
        }
        for r in reports
    ]
    st.dataframe(table_rows, width='stretch')

    st.subheader("Inspect a Run")
    selected_filename = st.selectbox(
        "Choose a report to view in detail:",
        options=[r["_filename"] for r in reports]
    )
    selected_report = next(r for r in reports if r["_filename"] == selected_filename)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Vulnerable", str(selected_report["is_vulnerable"]))
        st.metric("Confidence", selected_report["confidence_score"])
    with col2:
        st.metric("Iterations Used", f"{selected_report['iteration']} / {selected_report['max_iterations']}")
        st.metric("Vulnerability Type", selected_report["vulnerability_type"])

    st.markdown("**Final System Prompt:**")
    st.text(selected_report["system_prompt"])

    st.markdown("**Reasoning:**")
    st.write(selected_report["reasoning"])

    st.markdown("**Attempt History:**")
    for i, attempt in enumerate(selected_report["attempt_history"], start=1):
        status = "SUCCEEDED" if attempt["is_vulnerable"] else "BLOCKED"
        with st.expander(f"Attempt {i} — {status}"):
            st.write(attempt["attack_payload"])
            st.caption(f"Type: {attempt['vulnerability_type']}")