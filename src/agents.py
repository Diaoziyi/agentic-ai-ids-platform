import os
from openai import OpenAI

from prompts import (
    THREAT_ANALYSIS_PROMPT,
    RISK_CLASSIFICATION_PROMPT,
    RESPONSE_RECOMMENDATION_PROMPT,
    SOC_REPORT_PROMPT
)


def run_agent(system_prompt, user_input):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


def threat_analysis_agent(ids_context):
    return run_agent(THREAT_ANALYSIS_PROMPT, ids_context)


def risk_classification_agent(threat_analysis):
    return run_agent(RISK_CLASSIFICATION_PROMPT, threat_analysis)


def response_recommendation_agent(risk_classification):
    return run_agent(RESPONSE_RECOMMENDATION_PROMPT, risk_classification)


def soc_report_agent(ids_context, threat_analysis, risk_classification, recommendations):
    combined_input = f"""
IDS Context:
{ids_context}

Threat Analysis:
{threat_analysis}

Risk Classification:
{risk_classification}

Recommendations:
{recommendations}
"""
    return run_agent(SOC_REPORT_PROMPT, combined_input)