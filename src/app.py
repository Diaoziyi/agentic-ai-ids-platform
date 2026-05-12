import streamlit as st
from dotenv import load_dotenv

from agents import (
    threat_analysis_agent,
    risk_classification_agent,
    response_recommendation_agent,
    soc_report_agent
)

load_dotenv()

st.set_page_config(
    page_title="Agentic AI IDS Platform",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Agentic AI Intrusion Detection & Threat Intelligence Platform")

st.write("""
This platform extends a machine-learning intrusion detection system with a
multi-agent AI workflow for threat analysis, risk classification, incident
response recommendation, and SOC-style reporting.
""")

st.subheader("IDS Detection Context")

ids_prediction = st.selectbox(
    "IDS prediction:",
    ["attack", "normal"]
)

attack_type = st.text_input(
    "Predicted / suspected attack type:",
    placeholder="Example: DoS, Probe, R2L, U2R, unknown"
)

traffic_context = st.text_area(
    "Network traffic context:",
    height=180,
    placeholder="Example: Multiple failed login attempts and unusual outbound traffic were observed from a host."
)

if st.button("Generate SOC Threat Intelligence Report"):

    if not traffic_context.strip():
        st.warning("Please enter network traffic context.")

    else:
        ids_context = f"""
IDS Prediction: {ids_prediction}
Suspected Attack Type: {attack_type if attack_type else "Not specified"}
Network Traffic Context: {traffic_context}
"""

        with st.spinner("Threat Analysis Agent is analysing the IDS result..."):
            threat_analysis = threat_analysis_agent(ids_context)

        with st.spinner("Risk Classification Agent is evaluating severity..."):
            risk_classification = risk_classification_agent(threat_analysis)

        with st.spinner("Response Recommendation Agent is preparing actions..."):
            recommendations = response_recommendation_agent(risk_classification)

        with st.spinner("SOC Report Agent is generating final report..."):
            final_report = soc_report_agent(
                ids_context,
                threat_analysis,
                risk_classification,
                recommendations
            )

        st.success("SOC report generated successfully.")

        tab1, tab2, tab3, tab4 = st.tabs([
            "Threat Analysis",
            "Risk Classification",
            "Recommendations",
            "SOC Report"
        ])

        with tab1:
            st.markdown(threat_analysis)

        with tab2:
            st.markdown(risk_classification)

        with tab3:
            st.markdown(recommendations)

        with tab4:
            st.markdown(final_report)

        st.download_button(
            label="Download SOC Report",
            data=final_report,
            file_name="soc_incident_report.md",
            mime="text/markdown"
        )