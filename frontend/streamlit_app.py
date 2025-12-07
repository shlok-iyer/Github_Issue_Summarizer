import os
import json
import requests
import streamlit as st

st.set_page_config(page_title="GitHub Issue Assistant", page_icon="🪴", layout="centered")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("🪴 AI-Powered GitHub Issue Assistant")
st.caption("Powered by Google Gemini • Seedling Labs craft case")

with st.form("input"):
    repo_url = st.text_input("Public GitHub Repository URL", placeholder="https://github.com/facebook/react")
    issue_number = st.number_input("Issue Number", min_value=1, step=1, value=1)
    submitted = st.form_submit_button("Analyze Issue")

if submitted:
    if not repo_url:
        st.error("Please provide a valid repo URL.")
    else:
        with st.spinner("Analyzing with Gemini..."):
            try:
                resp = requests.post(
                    f"{BACKEND_URL}/analyze",
                    json={"repo_url": repo_url, "issue_number": int(issue_number)},
                    timeout=60,
                )
                if resp.status_code != 200:
                    st.error(f"Error: {resp.status_code} – {resp.text}")
                else:
                    data = resp.json()

                    st.success("Analysis complete.")
                    st.markdown(f"**Repository:** `{data['repo']}`  \n**Issue:** [{data['issue_number']}]({data['issue_url']})")

                    analysis = data["analysis"]

                    # Cards
                    st.subheader("Summary")
                    st.write(analysis["summary"])

                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Type", analysis["type"])
                    with col2:
                        st.metric("Priority", analysis["priority_score"].split(" - ")[0])
                        st.caption(analysis["priority_score"])

                    st.subheader("Suggested Labels")
                    st.write(", ".join(analysis["suggested_labels"]))

                    st.subheader("Potential Impact")
                    st.write(analysis["potential_impact"])

                    # Raw JSON + copy
                    st.subheader("Raw JSON")
                    st.code(json.dumps(analysis, indent=2))
                    st.download_button(
                        "Download JSON",
                        data=json.dumps(analysis, indent=2),
                        file_name=f"issue_{data['issue_number']}_analysis.json",
                        mime="application/json",
                    )
            except requests.RequestException as e:
                st.error(f"Network error: {e}")

st.divider()

