# EchoPulse AI: Executive Voice & NLP Analytics Dashboard

> **Wispr Flow Shortlisting Task Submission**  
> Built entirely using voice-driven development with **[Wispr Flow](https://ref.wisprflow.ai/hhg)**.

---

## 📌 Overview

**EchoPulse AI** is an interactive, voice-native Executive Analytics & Natural Language Processing (NLP) intelligence platform. It bridges unstructured speech and strategic executive decision-making by turning customer voice memos, support call transcripts, and spoken team updates into real-time KPI metrics, sentiment trajectories, and actionable insights.

---

## 🚀 Key Features

* **🎙️ Wispr Flow Voice Integration**:
  * Real-time customer voice-note ingestion simulator.
  * Live **Wispr Flow Sandbox** for testing voice dictation with instantaneous NLP parsing, sentiment polarity, and readability metrics.
* **🧠 Core NLP Engine**:
  * **Sentiment & Polarity Scoring**: Real-time polarity analysis with confidence metrics.
  * **Semantic Topic Modeling**: Categorizes feedback into Voice Accuracy, Speed/Latency, UI/UX, Pricing, and Integrations.
  * **Urgency & Friction Detection**: Automatically flags P0/P1 blockers, escalations, and critical customer issues.
  * **Readability & Speech Estimation**: Measures Flesch Reading Ease and estimated spoken audio duration.
* **📊 Executive KPI Ribbon**:
  * Net Sentiment Index with sparkline trajectory.
  * Volume of analyzed transcripts with historical bar sparklines.
  * Critical friction & escalations tracker.
  * CSAT / Satisfaction score index.
* **💬 "Ask Executive AI" (Natural Language Voice Q&A)**:
  * Leadership can speak or type complex business questions in plain English (e.g. *"What are customers saying about Wispr Flow dictation speed?"*).
  * Automatically retrieves relevant voice transcripts and synthesizes key findings, grounded customer quotes, and strategic action plans.
* **📥 One-Click Executive Briefing Export**:
  * Download structured markdown briefings ready for board reviews and executive meetings.

---

## 🛠️ Architecture & Tech Stack

* **Frontend & Dashboard**: [Streamlit](https://streamlit.io/) with customized Slate theme (`.streamlit/config.toml`)
* **Data Processing & Analytics**: Pandas, NumPy, Altair
* **NLP Pipeline**: Pure Python, zero external cloud model dependencies required for local execution
* **Development Methodology**: 100% Voice-driven development via **Wispr Flow**

---

## ⚡ Quick Start (with `uv`)

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/echopulse-voice-nlp.git
cd echopulse-voice-nlp
```

### 2. Run immediately with `uv`
No manual virtualenv management required; `uv` handles dependency resolution automatically:
```bash
uv run streamlit run app.py
```

*(Alternatively, if you prefer an isolated sync environment)*:
```bash
uv sync
uv run streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🗣️ Voice-Driven Development Process

This project was conceived, architected, and built using **Wispr Flow** for hands-free, voice-driven coding:
1. **Architecture Formulation**: Spoken prompts dictating data model requirements and NLP taxonomy.
2. **Component Implementation**: Dictating Streamlit layouts, responsive metric ribbons, and sparkline configurations.
3. **NLP Logic Generation**: Voice-directing the sentiment polarity thresholds and urgency trigger regex patterns.
4. **Live Iteration**: Using Wispr Flow to test the Sandbox tab by speaking direct voice notes into the app.

See [`VOICE_DEMO_SCRIPT.md`](./VOICE_DEMO_SCRIPT.md) for the exact voice prompts used in the video demo.

---

## 📝 Submission Checklist
- [x] Account created via mandatory referral link: [`https://ref.wisprflow.ai/hhg`](https://ref.wisprflow.ai/hhg)
- [x] Functional codebase demonstrating voice-driven development
- [x] Demo video recording Wispr Flow voice coding session
- [x] Form submission: [`https://forms.gle/Lv9wF8gYVHdEqfJW8`](https://forms.gle/Lv9wF8gYVHdEqfJW8)
