# 🛡️ Agentic AI Intrusion Detection & Threat Intelligence Platform

> A multi-agent AI cybersecurity platform that combines machine learning intrusion detection with AI-driven threat analysis, risk classification, incident response recommendation, and SOC-style reporting.

---

# 📌 Project Overview

This project implements an **Agentic AI workflow for cybersecurity operations**.

The platform extends a traditional machine learning Intrusion Detection System (IDS) by integrating multiple AI agents that simulate the workflow of a modern Security Operations Centre (SOC).

The system combines:

- Machine learning-based intrusion detection
- AI-driven threat analysis
- Risk classification
- Incident response recommendation
- SOC-style incident reporting

This project was developed for:

**CI7526 – Cyber and Artificial Intelligence (Applications)**

---

# 🚀 Key Features

## 🔍 Machine Learning IDS

- RandomForest-based intrusion detection
- NSL-KDD dataset
- Binary and multi-class attack detection
- Feature importance analysis

---

## 🤖 Multi-Agent AI Workflow

The platform uses multiple specialised AI agents:

| Agent | Responsibility |
|---|---|
| Threat Analysis Agent | Analyses suspicious activity |
| Risk Classification Agent | Evaluates severity and impact |
| Response Recommendation Agent | Generates incident response actions |
| SOC Report Generator Agent | Produces SOC-style incident reports |

---

## 🛡️ Cybersecurity Capabilities

- AI-assisted threat intelligence
- SOC workflow simulation
- Incident response recommendation
- Human-readable security reporting
- Explainable AI considerations

---

# 🧠 System Architecture

```text
Network Traffic
        ↓
Machine Learning IDS
(RandomForest)
        ↓
Threat Analysis Agent
        ↓
Risk Classification Agent
        ↓
Response Recommendation Agent
        ↓
SOC Report Generator Agent
        ↓
SOC Incident Report
```

---

# 🖥️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core development |
| Scikit-learn | Machine learning |
| RandomForest | Intrusion detection |
| Streamlit | User interface |
| FastAPI | Inference API |
| OpenAI API | Multi-agent AI workflow |
| Pandas | Data processing |
| Joblib | Model persistence |

---

# 📂 Project Structure

```text
ids-ml-project/
│
├── src/
│   ├── app.py
│   ├── agents.py
│   ├── prompts.py
│   ├── api_server.py
│   ├── predict.py
│   ├── train_model.py
│   └── train_model_advanced.py
│
├── samples/
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## Clone repository

```bash
git clone https://github.com/Diaoziyi/agentic-ai-ids-platform.git
cd agentic-ai-ids-platform
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configure OpenAI API key

Create a `.env` file:

```text
OPENAI_API_KEY=your_api_key_here
```

---

## Run Streamlit application

```bash
python3 -m streamlit run src/app.py
```

---

# 🧪 Example Usage

## IDS Prediction

```text
attack
```

## Attack Type

```text
Probe
```

## Network Traffic Context

```text
Multiple failed login attempts and unusual outbound traffic were observed from a host.
```

---

# 📊 Example Outputs

The platform generates:

- Threat analysis
- Risk classification
- Response recommendations
- SOC-style incident reports

---

# 🔐 Security Considerations

The project discusses:

- AES encryption
- RSA secure communication
- SHA-256 integrity verification
- TLS 1.3
- Access control
- AI-assisted monitoring
- Explainable AI

---

# ⚖️ Legal & Ethical Considerations

The project considers:

- GDPR compliance
- Ethical monitoring
- AI bias
- False positives
- Human oversight
- Responsible AI deployment

The system is designed to assist SOC analysts rather than replace human judgement.

---

# 📈 Explainable AI

To improve transparency and trust, the project includes:

- Feature importance analysis
- Human-readable reports
- Risk justification
- Analyst review recommendations

---

# ⚠️ Limitations

- Dependency on NSL-KDD dataset
- OpenAI API dependency
- No real-time packet capture
- Possible AI hallucinations
- No live SIEM integration

---

# 🔮 Future Improvements

- Real-time traffic monitoring
- SIEM integration
- SHAP explainability
- SOAR integration
- Local LLM deployment
- Automated firewall response

---

# 👨‍💻 Human-in-the-Loop Security

This platform follows a human-in-the-loop cybersecurity approach.

AI assists SOC analysts by automating:

- threat interpretation
- risk assessment
- incident reporting

However, final security decisions remain under human control.

---

# 📚 Academic Context

This project was developed for:

**CI7526 – Cyber and Artificial Intelligence (Applications)**

Focus areas:

- Agentic AI
- AI co-production
- Cybersecurity workflows
- Security operations automation

---

# 🤝 Acknowledgement of Generative AI

Generative AI tools were used for:

- ideation
- workflow structuring
- debugging assistance
- grammar refinement

All core implementation, analysis, reasoning, and final design decisions were completed independently.
