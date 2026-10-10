# 🎙️ Wispr Flow Video Demo Script & Recording Walkthrough

Use this guide to record your **Wispr Flow Shortlisting Submission Video**.

The submission requires demonstrating **voice-driven development** using **Wispr Flow** to build and interact with the project.

---

## ⏱️ Video Plan (Target: 2 to 3 minutes)

| Timestamp | Phase | What to Show on Screen | What to Say Aloud (via Wispr Flow) |
| :--- | :--- | :--- | :--- |
| **0:00 - 0:30** | **Intro & Setup** | IDE / AI Chat opened with Wispr Flow active | Introduce that you're building an Executive Voice & NLP Analytics Dashboard using Wispr Flow. |
| **0:30 - 1:15** | **Voice-Driven Development** | Dictating prompts into your editor / AI agent using Wispr Flow | Dictate Prompt 1 & Prompt 2 below to show hands-free code generation. |
| **1:15 - 2:00** | **Live App Walkthrough** | Terminal running `streamlit run app.py` -> Browser UI | Tour the KPI cards, sparklines, and sentiment trajectory charts. |
| **2:00 - 2:45** | **Live Voice Ingestion Demo** | Wispr Flow Sandbox tab in the browser | Dictate directly into the sandbox box using Wispr Flow to show instant NLP extraction. |
| **2:45 - 3:00** | **Wrap-Up** | Show executive briefing report download | Conclude highlighting hands-free velocity. |

---

## 📜 Voice Prompts to Dictate into Wispr Flow

### Prompt 1: Scaffolding the NLP Engine
> *"Using Wispr Flow, let's create a natural language processing engine for customer voice transcripts. We need sentiment polarity scoring, semantic topic classification for categories like voice accuracy and latency, urgency detection for high-priority bugs, and a function to calculate readability scores."*

### Prompt 2: Building the Executive UI
> *"Now let's build the Streamlit executive dashboard. We want a modern slate theme, a top KPI ribbon with metric cards and sparklines for net sentiment and CSAT, an interactive topic breakdown chart, and a dedicated tab for natural language executive queries."*

### Prompt 3: Adding the Live Voice Sandbox
> *"Let's add a fourth tab called Wispr Flow Live Voice Sandbox where an executive can dictate spoken audio notes directly. It should immediately extract sentiment, classify the topic, detect urgent blockers, and generate an executive summary."*

---

## 🖥️ Live Browser Demo Steps (Once App is Running)

1. **Open** `http://localhost:8501`.
2. **Show the Sidebar**: Click the `Ingest voice note` button to demonstrate live telemetry update.
3. **Show Tab 1 (Executive Overview)**: Highlight the net sentiment (+78%) and daily trajectory line chart.
4. **Show Tab 3 (Ask Executive AI)**: Click *"Voice accuracy feedback"* and hit *"Synthesize executive answer"*. Show how the NLP system extracts quotes and recommendations.
5. **Show Tab 4 (Wispr Flow Live Sandbox)**:
   - Click into the text area.
   - Hold your Wispr Flow voice shortcut and dictate:
     > *"Wispr Flow voice note: Customer feedback from enterprise clients indicates voice dictation accuracy has reduced documentation time by 40 percent."*
   - Watch the instant polarity score, topic detection, and speech duration update on screen!
6. **Download Briefing**: Click the `Download executive briefing (.md)` button at the bottom.

---

## 🚀 Pre-flight Recording Checklist
- [ ] Wispr Flow app is running with microphone active.
- [ ] Screen recording tool ready (OBS, Loom, QuickTime, or native screen recorder).
- [ ] Streamlit app launched (`uv run streamlit run app.py`).
- [ ] Keep browser window and IDE side-by-side or tab-switch smoothly.
