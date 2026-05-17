# Agentic AI Intrusion Detection & Threat Intelligence Platform

> A multi-agent AI cybersecurity platform that combines machine learning intrusion detection with AI-driven threat analysis, risk classification, incident response recommendation, and SOC-style reporting.

---

##  Project Overview

This project implements an **Agentic AI workflow for cybersecurity operations**.

The platform extends a traditional machine learning Intrusion Detection System (IDS) by integrating multiple AI agents that simulate the workflow of a modern Security Operations Centre (SOC).

The system combines:

- Machine learning-based intrusion detection (RandomForest)
- AI-driven threat analysis via a four-agent pipeline
- Risk classification and severity scoring
- Incident response recommendation
- SOC-style incident reporting
- Streamlit analyst interface and FastAPI inference API

This project was developed for:

**CI7526 – Cyber and Artificial Intelligence (Applications)**  
Kingston University London

---

##  Key Features

###  Machine Learning IDS

- RandomForest-based multi-class intrusion detection
- Trained on the NSL-KDD benchmark dataset (125,973 training samples, 22,544 test samples)
- 23 attack categories in training; evaluated against 39 categories in KDDTest+
- Preprocessing pipeline: StandardScaler + OneHotEncoder via sklearn ColumnTransformer
- Feature importance analysis for explainability (Top 20 features visualised)
- Three experiments conducted: baseline, class_weight balancing, SMOTE oversampling

###  Multi-Agent AI Workflow

The platform uses four specialised AI agents in a sequential pipeline:

| Agent | Responsibility |
|---|---|
| Threat Analysis Agent | Interprets ML classification and generates a natural-language threat narrative |
| Risk Classification Agent | Assigns severity level (Low / Medium / High / Critical) with justification |
| Response Recommendation Agent | Produces prioritised, actionable incident response steps |
| SOC Report Generator Agent | Compiles all agent outputs into a structured SOC incident report |

###  Cybersecurity Capabilities

- AI-assisted threat intelligence generation
- SOC workflow simulation and automation
- Human-in-the-loop incident response (all outputs require analyst review)
- Explainable AI via feature importance analysis
- Human-readable SOC-style incident reports

---

##  Model Performance

Three experiments were conducted to evaluate and improve classifier performance on KDDTest+.

### Experiment 1 — Baseline Model Comparison

| Model | Accuracy | Macro F1 | Train Time |
|---|---|---|---|
| RandomForest | 72.15% | 0.23 | ~4s |
| SVM | ~70% | ~0.22 | ~1300s |
| KNN | ~70% | ~0.24 | ~0.2s |

### Experiment 2 — Class Weight Balancing (`class_weight="balanced"`)

| Model | Accuracy | Macro F1 | Train Time |
|---|---|---|---|
| RandomForest + balanced | 72.15% | **0.2664** | 4.2s |
| SVM + balanced | 70.76% | 0.2281 | 1300.3s |
| KNN | 70.39% | 0.2452 | 0.2s |

### Experiment 3 — SMOTE Oversampling + RandomForest

| Metric | Value |
|---|---|
| Accuracy | 71.99% |
| Macro F1 | 0.2496 |
| Training samples after SMOTE | 1,414,203 |
| Train Time | 82.1s |

### Final Model Selection

**RandomForest with `class_weight="balanced"`** was selected as the final model:
- Highest macro F1 (0.2664) across all experiments
- Fastest training time (4.2s vs 1300s for SVM)
- Native feature importance for explainability

> **Note on macro F1:** The macro F1 of 0.27 reflects a known limitation of the NSL-KDD dataset: KDDTest+ deliberately contains attack categories absent from KDDTrain+ (e.g. apache2, mscan, processtable). This is a **covariate shift problem**, not a modelling failure. SMOTE cannot address distribution mismatch — only retraining on a modern dataset (e.g. CICIDS-2017) would resolve this. This finding is documented critically in the supplementary documentation.

### Top Feature Importances

The dominant feature is `num_4` (connection duration, importance ≈ 0.11), followed by `num_28` (connection count to same host in past 2 seconds, ≈ 0.07) and `x2_SF` (service, ≈ 0.07). These volume and duration statistics explain the model's strong performance on DoS attacks (neptune F1=0.98, smurf F1=0.99) and poor performance on low-and-slow attacks (guess_passwd F1=0.00).

---

##  System Architecture

```
Network Traffic Features (41 NSL-KDD features)
        ↓
ML IDS (RandomForest via FastAPI /predict)
        ↓
Threat Analysis Agent (OpenAI GPT)
        ↓
Risk Classification Agent (OpenAI GPT)
        ↓
Response Recommendation Agent (OpenAI GPT)
        ↓
SOC Report Generator Agent (OpenAI GPT)
        ↓
SOC Incident Report → Streamlit UI
```

---

##  Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core development |
| scikit-learn | ML pipeline, RandomForest, preprocessing |
| imbalanced-learn | SMOTE oversampling (Experiment 3) |
| FastAPI | REST inference API (`/predict` endpoint) |
| Streamlit | Analyst-facing user interface |
| OpenAI API | Multi-agent AI workflow |
| Pandas / NumPy | Data processing |
| Matplotlib / Seaborn | Feature importance and confusion matrix visualisation |
| Joblib | Model persistence |

---

##  Project Structure

```
ids-ml-project/
│
├── src/
│   ├── app.py                    # Streamlit UI
│   ├── agents.py                 # Multi-agent orchestration
│   ├── prompts.py                # Agent prompt templates
│   ├── api_server_advanced.py    # FastAPI inference server
│   ├── predict.py                # Standalone prediction utilit
│   └── train_model_advanced.py  # Improved training script (class_weight + SMOTE)
│
├── models/
│   └── ids_model_advanced.pkl    # Trained model pipeline (generated)
│
├── figures/
│   ├── feature_importance_smote.png   # Top 20 feature importances
│   └── confusion_matrix_smote.png     # Confusion matrix (top 10 classes)
│
├── data/
│   └── nsl-kdd/
│       ├── KDDTrain+.txt
│       └── KDDTest+.txt
│
├── requirements.txt
├── .env                          # API key (not committed — see setup)
└── README.md
```

---

##  Installation & Setup

### 1. Clone repository

```bash
git clone https://github.com/Diaoziyi/agentic-ai-ids-platform.git
cd agentic-ai-ids-platform
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download NSL-KDD dataset

Download `KDDTrain+.txt` and `KDDTest+.txt` from the [NSL-KDD dataset page](https://www.unb.ca/cic/datasets/nsl.html) and place them in `data/nsl-kdd/`.

### 5. Configure OpenAI API key

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_api_key_here
```

> ⚠️ Never commit your `.env` file. It is included in `.gitignore`.

---

##  Running the Platform

> ⚠️ **The API server and Streamlit UI must run in two separate terminals simultaneously.**  
> The Streamlit frontend communicates with the FastAPI backend at runtime — starting only one will result in prediction errors.

### Step 1 — Train the model (one-time setup)

```bash
python3 src/train_model_improved.py
```

This trains the RandomForest model with `class_weight="balanced"` and runs all three experiments (baseline, class_weight balancing, SMOTE). The final model is saved to `models/ids_model_advanced.pkl`.

> **Dataset note:** Column 41 is the attack type label; column 42 is the difficulty score. The training script uses `iloc[:, 41]` — this was identified and corrected during development.

### Step 2 — Start the API server (Terminal 1)

```bash
uvicorn src.api_server_advanced:app --reload
```

- API available at: `http://localhost:8000`
- Interactive docs at: `http://localhost:8000/docs`

Keep this terminal running.

### Step 3 — Launch the Streamlit UI (Terminal 2, new window)

```bash
python3 -m streamlit run src/app.py
```

- UI available at: `http://localhost:8501`
- Network URL: `http://<your-ip>:8501`

Both processes must be running for the platform to function end-to-end.

---

##  API Reference

### `POST /predict`

Accepts a JSON body with 41 NSL-KDD network features and returns the predicted attack class, class probabilities, and top-3 most likely classes.

**Request:**
```json
{
  "features": [0, 1, 2, ..., 40]
}
```

**Response:**
```json
{
  "prediction": 3,
  "probabilities": {"0": 0.02, "1": 0.85, ...},
  "top_3_classes": {"1": 0.85, "3": 0.10, "0": 0.02}
}
```

**Error (wrong feature count):**
```json
{
  "error": "Expected 41 features, but got 40"
}
```

---

##  Security Considerations

For production deployment, the following controls are recommended:

| Control | Recommendation |
|---|---|
| API transport | TLS 1.3 with ECDHE (mandatory) |
| Secret management | HashiCorp Vault or AWS Secrets Manager (not .env) |
| Model integrity | SHA-256 signing of `ids_model_advanced.pkl` at training time; verify at load |
| API authentication | HMAC-SHA256 request signing between UI and API |
| Access control | Role-based authentication on Streamlit UI and API endpoint |
| Data retention | Define log retention policy; apply GDPR data minimisation principles |

---

##  Legal & Ethical Considerations

- **GDPR:** Network traffic metadata may constitute personal data. A Data Protection Impact Assessment (DPIA) is required before live deployment (UK GDPR Article 35).
- **Computer Misuse Act 1990:** This system must only be deployed on networks for which explicit authorisation has been obtained.
- **AI Bias:** The model fails to detect 25 of 39 attack classes in KDDTest+. Human analyst review of all outputs is mandatory before action is taken.
- **Human-in-the-Loop:** All AI agent outputs are advisory. No automated enforcement actions are taken by the platform.
- **AI Hallucination:** OpenAI GPT agents may produce plausible but incorrect recommendations. Analyst validation is required.

---

##  Known Limitations

| Limitation | Details |
|---|---|
| Dataset age | NSL-KDD is derived from 1999 data; modern attack vectors are not represented |
| Covariate shift | KDDTest+ contains attack classes absent from KDDTrain+; macro F1 is 0.27 as a result |
| No real-time capture | System requires pre-extracted 41-feature vectors; no live packet capture |
| OpenAI dependency | Agent pipeline fails if API is unavailable or quota exceeded |
| No authentication | Current implementation has no access control on UI or API endpoint |

---

##  Future Improvements

| Priority | Improvement | Rationale |
|---|---|---|
| High | Retrain on CICIDS-2017 or UNSW-NB15 | Address covariate shift; improve macro F1 |
| High | SHAP explainability | Per-prediction feature attribution for analyst trust |
| High | SMOTE with modern dataset | Oversampling effective when train/test share same distribution |
| Medium | Local LLM deployment (Ollama) | Remove OpenAI API dependency; enable air-gapped deployment |
| Medium | Real-time packet capture (scapy) | Enable live network monitoring |
| Medium | SIEM integration (Splunk / Elastic) | Production-ready alert management |
| Low | SOAR integration | Automated response workflow with human approval gate |

---

##  Acknowledgement of Generative AI

Generative AI tools were used during this project in accordance with Kingston University guidance on acceptable AI use.

| Tool | Usage | Extent |
|---|---|---|
| GitHub Copilot | Assisted with boilerplate code generation for FastAPI endpoints and sklearn workflows | Low — suggestions were reviewed, tested, and modified where necessary |
| ChatGPT | Assisted with structuring documentation sections, refining wording, and brainstorming prompt workflow ideas | Medium — outputs were adapted and critically reviewed before inclusion |
| Claude (Anthropic) | Used for reflective feedback on documentation structure and identifying potential coverage gaps | Low — used primarily as a review assistant |

All final implementation, experimental evaluation, system design decisions, security analysis, and conclusions represent the author’s own work and understanding. All AI-generated assistance was reviewed critically and integrated selectively.

---

##  Academic Context

**Module:** CI7526 – Cyber and Artificial Intelligence (Applications)  
**Focus areas:** Agentic AI, AI co-production, cybersecurity workflows, security operations automation
