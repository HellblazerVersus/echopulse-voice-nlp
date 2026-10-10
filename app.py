"""
EchoPulse: Executive Voice & NLP Analytics Dashboard
A real-time executive intelligence dashboard built with voice-driven development (Wispr Flow).
Analyzes customer voice notes, support transcripts, sentiment trajectories, and key topic drivers.
"""

import datetime
import pandas as pd
import numpy as np
import streamlit as st

import nlp_engine

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="EchoPulse | Executive Voice & NLP Analytics",
    page_icon=":material/analytics:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Codecademy-style Light Mode CSS overrides
# ---------------------------------------------------------
st.html("""
<style>
  /* ── Force JetBrains Mono on every element ── */
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap');
  html, body, [class*="st-"], button, input, select, textarea, label,
  [data-testid], .stMarkdown, .stMetric, .stDataFrame {
      font-family: 'JetBrains Mono', monospace !important;
  }

  /* ── Light canvas ── */
  .stApp { background-color: #FFFFFF !important; }
  [data-testid="stSidebar"] {
      background-color: #F4F0FA !important;
      border-right: 1px solid #D6CCF0 !important;
  }
  [data-testid="stHeader"] {
      background-color: #FFFFFF !important;
      border-bottom: 1px solid #D6CCF0 !important;
  }

  /* ── Primary button — solid purple with lift shadow ── */
  button[kind="primary"], [data-testid="stBaseButton-primary"] {
      background: linear-gradient(135deg, #7B2FBE 0%, #5A1F9A 100%) !important;
      border: none !important;
      box-shadow: 0 2px 12px rgba(123, 47, 190, 0.35) !important;
      color: #FFFFFF !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-weight: 600 !important;
      letter-spacing: 0.02em !important;
      transition: box-shadow 0.2s ease, transform 0.15s ease !important;
  }
  button[kind="primary"]:hover, [data-testid="stBaseButton-primary"]:hover {
      box-shadow: 0 4px 20px rgba(123, 47, 190, 0.55) !important;
      transform: translateY(-1px) !important;
  }

  /* ── Secondary button — outlined purple ── */
  button[kind="secondary"], [data-testid="stBaseButton-secondary"] {
      background: transparent !important;
      border: 1.5px solid #7B2FBE !important;
      color: #7B2FBE !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-weight: 500 !important;
  }
  button[kind="secondary"]:hover, [data-testid="stBaseButton-secondary"]:hover {
      background: rgba(123, 47, 190, 0.07) !important;
  }

  /* ── Links — purple ── */
  a, a:visited { color: #7B2FBE !important; text-decoration: none !important; }
  a:hover { text-decoration: underline !important; color: #5A1F9A !important; }

  /* ── Cards — white with lavender border, purple glow on hover ── */
  [data-testid="stVerticalBlockBorderWrapper"] {
      border: 1px solid #D6CCF0 !important;
      border-radius: 8px !important;
      background-color: #FAFAFA !important;
      box-shadow: 0 1px 4px rgba(123, 47, 190, 0.06) !important;
      transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
  }
  [data-testid="stVerticalBlockBorderWrapper"]:hover {
      border-color: #7B2FBE !important;
      box-shadow: 0 4px 16px rgba(123, 47, 190, 0.18) !important;
  }

  /* ── Metric labels — purple uppercase ── */
  [data-testid="stMetricLabel"] {
      color: #7B2FBE !important;
      font-size: 11px !important;
      letter-spacing: 0.08em !important;
      text-transform: uppercase !important;
  }
  [data-testid="stMetricValue"] { color: #1A1A2E !important; font-weight: 700 !important; }
  [data-testid="stMetricDelta"] { font-size: 12px !important; }

  /* ── Tabs — active tab underlined in purple ── */
  [data-testid="stTabs"] button {
      color: #5C5F7A !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-weight: 500 !important;
      border-bottom: 2px solid transparent !important;
      transition: color 0.2s, border-color 0.2s !important;
  }
  [data-testid="stTabs"] button[aria-selected="true"] {
      color: #1A1A2E !important;
      border-bottom: 2px solid #7B2FBE !important;
  }

  /* ── Sidebar title ── */
  [data-testid="stSidebar"] h1 {
      color: #1A1A2E !important;
      font-size: 20px !important;
      font-weight: 700 !important;
      letter-spacing: 0.04em !important;
      border-bottom: 2px solid #7B2FBE;
      padding-bottom: 8px;
  }

  /* ── Dividers ── */
  hr { border-color: #D6CCF0 !important; }

  /* ── Dataframe headers — purple uppercase on lavender ── */
  [data-testid="stDataFrame"] thead th {
      background-color: #EDE8F5 !important;
      color: #7B2FBE !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 12px !important;
      letter-spacing: 0.05em !important;
      text-transform: uppercase !important;
  }

  /* ── Expander ── */
  [data-testid="stExpander"] summary {
      color: #7B2FBE !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-weight: 600 !important;
  }

  /* ── Custom scrollbar ── */
  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: #F4F0FA; }
  ::-webkit-scrollbar-thumb { background: #D6CCF0; border-radius: 4px; }
  ::-webkit-scrollbar-thumb:hover { background: #7B2FBE; }
</style>
""")

# ---------------------------------------------------------
# State Initialization & Cached Data Loading
# ---------------------------------------------------------
@st.cache_data(ttl=60)
def load_base_data() -> pd.DataFrame:
    return nlp_engine.generate_analytics_dataset(n_samples=280)

if "custom_transcripts" not in st.session_state:
    st.session_state["custom_transcripts"] = []

if "selected_query_preset" not in st.session_state:
    st.session_state["selected_query_preset"] = ""

# Merge base data with any live ingested items
base_df = load_base_data()
if st.session_state["custom_transcripts"]:
    custom_df = pd.DataFrame(st.session_state["custom_transcripts"])
    data_df = pd.concat([custom_df, base_df], ignore_index=True)
else:
    data_df = base_df.copy()

# ---------------------------------------------------------
# Sidebar Controls & Slicers
# ---------------------------------------------------------
with st.sidebar:
    st.title("EchoPulse")
    st.caption("Voice-Driven NLP Intelligence Hub")
    
    st.markdown("### Filters and segments")
    
    # Date Range Filter
    min_date = data_df["date"].min().date()
    max_date = data_df["date"].max().date()
    selected_dates = st.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    
    # Channel Filter
    all_channels = sorted(data_df["channel"].unique().tolist())
    selected_channels = st.multiselect(
        "Channels",
        options=all_channels,
        default=all_channels,
        help="Select customer voice & feedback touchpoints"
    )
    
    # Region Filter
    all_regions = sorted(data_df["region"].unique().tolist())
    selected_regions = st.multiselect(
        "Market regions",
        options=all_regions,
        default=all_regions,
        help="Filter by geographical operating region"
    )
    
    # Sentiment Slicer
    st.markdown("### Sentiment focus")
    sentiment_filter = st.segmented_control(
        "Sentiment filter",
        options=["All", "Positive", "Neutral", "Negative"],
        default="All",
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Quick Ingest Voice Note Demo Action
    with st.container(border=True):
        st.markdown("**Simulate Wispr Flow voice note**")
        st.caption("Inject a real-time transcribed audio snippet into the live executive telemetry.")
        if st.button("Ingest voice note", icon=":material/mic:", type="secondary", width="stretch"):
            new_note_text = "Wispr Flow voice note: Just concluded executive Q3 review with enterprise client. Dictation speed cut report turnaround time in half."
            sentiment_res = nlp_engine.analyze_sentiment(new_note_text)
            topics = nlp_engine.classify_topics(new_note_text)
            new_record = {
                "id": f"TRX-LIVE-{len(st.session_state['custom_transcripts']) + 1}",
                "date": pd.to_datetime(datetime.date.today()),
                "transcript": new_note_text,
                "channel": "Wispr Flow Voice Notes",
                "region": "Global",
                "rating": 5,
                "sentiment": sentiment_res["label"],
                "polarity": sentiment_res["polarity"],
                "primary_topic": topics[0][0],
                "urgency": "Normal",
                "has_action_item": False,
                "word_count": len(new_note_text.split()),
            }
            st.session_state["custom_transcripts"].insert(0, new_record)
            st.toast("Voice note ingested successfully!", icon=":material/check_circle:")
            st.rerun()

    st.caption("Built with Wispr Flow Voice-Driven Development")

# ---------------------------------------------------------
# Apply Filtering to Dataset
# ---------------------------------------------------------
filtered_df = data_df.copy()

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_d, end_d = selected_dates
    filtered_df = filtered_df[
        (filtered_df["date"].dt.date >= start_d) & 
        (filtered_df["date"].dt.date <= end_d)
    ]

if selected_channels:
    filtered_df = filtered_df[filtered_df["channel"].isin(selected_channels)]

if selected_regions:
    filtered_df = filtered_df[filtered_df["region"].isin(selected_regions)]

if sentiment_filter and sentiment_filter != "All":
    filtered_df = filtered_df[filtered_df["sentiment"] == sentiment_filter]

# ---------------------------------------------------------
# Header & Wispr Flow Integration Badge
# ---------------------------------------------------------
with st.container(horizontal=True, horizontal_alignment="distribute"):
    st.title("EchoPulse: Executive Voice & NLP Analytics")
    with st.container(horizontal=True, horizontal_alignment="right"):
        st.badge("Wispr Flow Integrated", icon=":material/record_voice_over:")
        st.badge("NLP Pipeline Active", icon=":material/bolt:")

st.markdown(
    "Synthesizing customer voice notes, support audio transcripts, and sentiment telemetry "
    "into actionable executive intelligence. Built with voice-driven development via **Wispr Flow**."
)

# ---------------------------------------------------------
# KPI Metric Ribbon with Sparklines
# ---------------------------------------------------------
total_records = len(filtered_df)
pos_count = (filtered_df["sentiment"] == "Positive").sum()
neg_count = (filtered_df["sentiment"] == "Negative").sum()
net_sentiment = round(((pos_count - neg_count) / max(total_records, 1)) * 100, 1)
urgent_escalations = (filtered_df["urgency"] == "High").sum()
avg_rating = round(filtered_df["rating"].mean(), 2) if total_records > 0 else 0.0

# Generate sparklines from 7-day trend
trend_days = 7
if not filtered_df.empty:
    daily_stats = (
        filtered_df.groupby(filtered_df["date"].dt.date)
        .agg(
            pos=("sentiment", lambda s: (s == "Positive").sum()),
            neg=("sentiment", lambda s: (s == "Negative").sum()),
            count=("id", "count")
        )
        .tail(trend_days)
    )
    sentiment_spark = ((daily_stats["pos"] - daily_stats["neg"]) / np.maximum(daily_stats["count"], 1) * 100).tolist()
    volume_spark = daily_stats["count"].tolist()
    escalation_spark = [max(1, int(x * 0.15)) for x in volume_spark]
    rating_spark = [min(5.0, max(3.5, 4.2 + (x * 0.05))) for x in range(len(volume_spark))]
else:
    sentiment_spark = [50, 52, 58, 64, 71, 74, 78]
    volume_spark = [20, 24, 28, 32, 38, 42, 45]
    escalation_spark = [6, 5, 4, 4, 3, 3, 2]
    rating_spark = [4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7]

with st.container(horizontal=True):
    st.metric(
        label="Net sentiment index",
        value=f"{'+' if net_sentiment >= 0 else ''}{net_sentiment}%",
        delta="+4.8% vs last cycle",
        border=True,
        chart_data=sentiment_spark,
        chart_type="line",
    )
    st.metric(
        label="Transcripts analyzed",
        value=f"{total_records:,}",
        delta="+14.2% volume",
        border=True,
        chart_data=volume_spark,
        chart_type="bar",
    )
    st.metric(
        label="Critical escalations",
        value=f"{urgent_escalations}",
        delta="-32% resolution velocity",
        delta_color="inverse",
        border=True,
        chart_data=escalation_spark,
        chart_type="line",
    )
    st.metric(
        label="Customer satisfaction (CSAT)",
        value=f"{avg_rating} / 5.0",
        delta="+0.3 rating points",
        border=True,
        chart_data=rating_spark,
        chart_type="line",
    )

st.divider()

# ---------------------------------------------------------
# Tabbed Workspace
# ---------------------------------------------------------
tab_overview, tab_nlp, tab_ask_ai, tab_sandbox = st.tabs([
    ":material/dashboard: Executive overview",
    ":material/psychology: NLP topic & sentiment intelligence",
    ":material/mic: Ask executive AI (Voice Q&A)",
    ":material/record_voice_over: Wispr Flow live voice sandbox"
])

# =========================================================
# TAB 1: EXECUTIVE OVERVIEW
# =========================================================
with tab_overview:
    # Executive AI Synthesis Banner
    with st.container(border=True):
        st.subheader("Automated executive synthesis", anchor=False)
        st.markdown(
            f"""
            - **Overall Health**: Customer sentiment trajectory is **strong (+{net_sentiment}%)**, led primarily by high satisfaction in **Wispr Flow voice dictation accuracy** and meeting productivity.
            - **Key Growth Driver**: Engineering and Product users report saving **2 to 3 hours daily** by dictating code reviews, standup updates, and bug reports.
            - **Action Required**: **{urgent_escalations} high-urgency escalations** detected around peak-time latency and enterprise webhook reliability. Engineering triage recommended.
            """
        )
    
    # Visualization Row
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        with st.container(border=True):
            st.subheader("Daily sentiment trajectory", anchor=False)
            if not filtered_df.empty:
                daily_trend = (
                    filtered_df.groupby(filtered_df["date"].dt.date)["polarity"]
                    .mean()
                    .reset_index()
                    .rename(columns={"date": "Date", "polarity": "Average Polarity"})
                )
                st.line_chart(daily_trend, x="Date", y="Average Polarity")
            else:
                st.info("No data available for the selected filters.")

    with col_chart2:
        with st.container(border=True):
            st.subheader("Feedback volume by topic", anchor=False)
            if not filtered_df.empty:
                topic_dist = (
                    filtered_df["primary_topic"]
                    .value_counts()
                    .reset_index()
                    .rename(columns={"primary_topic": "Topic", "count": "Volume"})
                )
                st.bar_chart(topic_dist, x="Topic", y="Volume")
            else:
                st.info("No data available for the selected filters.")

    # High-Priority Escalations
    with st.container(border=True):
        st.subheader("High-urgency action queue", anchor=False)
        urgent_df = filtered_df[filtered_df["urgency"] == "High"][
            ["id", "date", "channel", "primary_topic", "transcript"]
        ]
        if not urgent_df.empty:
            st.dataframe(
                urgent_df,
                hide_index=True,
                width="stretch",
                column_config={
                    "id": st.column_config.TextColumn("Ticket ID", width="small"),
                    "date": st.column_config.DateColumn("Ingestion Date", format="YYYY-MM-DD", width="small"),
                    "channel": st.column_config.TextColumn("Touchpoint", width="medium"),
                    "primary_topic": st.column_config.TextColumn("Topic", width="medium"),
                    "transcript": st.column_config.TextColumn("Transcribed Voice Content", width="large"),
                }
            )
            with st.expander("Inspect full transcript details & triage notes", expanded=False):
                for _, row in urgent_df.head(5).iterrows():
                    st.markdown(f"**[{row['id']}] {row['primary_topic']}** • *{row['channel']}* (`{row['date'].strftime('%Y-%m-%d')}`)")
                    st.info(f"\"{row['transcript']}\"")
        else:
            st.success("No high-urgency friction items currently flagged.")

# =========================================================
# TAB 2: NLP TOPIC & SENTIMENT INTELLIGENCE
# =========================================================
with tab_nlp:
    col_kpi1, col_kpi2 = st.columns([1, 2])
    
    with col_kpi1:
        with st.container(border=True):
            st.subheader("Sentiment breakdown", anchor=False)
            sentiment_summary = filtered_df["sentiment"].value_counts().reset_index()
            sentiment_summary.columns = ["Sentiment", "Count"]
            st.bar_chart(sentiment_summary, x="Sentiment", y="Count")
            
            st.markdown("#### Sentiment metrics")
            pos_ratio = (pos_count / max(total_records, 1)) * 100
            neg_ratio = (neg_count / max(total_records, 1)) * 100
            st.write(f"• **Positive Share:** {pos_ratio:.1f}%")
            st.write(f"• **Negative Share:** {neg_ratio:.1f}%")
            st.write(f"• **Net Promoter Indicator:** {pos_ratio - neg_ratio:+.1f}")

    with col_kpi2:
        with st.container(border=True):
            st.subheader("Topic sentiment distribution", anchor=False)
            if not filtered_df.empty:
                topic_sentiment = (
                    pd.crosstab(filtered_df["primary_topic"], filtered_df["sentiment"])
                    .reset_index()
                )
                st.bar_chart(topic_sentiment, x="primary_topic")
            else:
                st.info("No data available.")

    # Ingested Transcript Explorer
    with st.container(border=True):
        st.subheader("Voice transcript explorer & semantic tagging", anchor=False)
        st.dataframe(
            filtered_df[["id", "date", "channel", "rating", "sentiment", "primary_topic", "urgency", "transcript"]],
            hide_index=True,
            column_config={
                "id": st.column_config.TextColumn("ID", width="small"),
                "date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
                "rating": st.column_config.NumberColumn("Rating", format="%d ⭐"),
                "sentiment": st.column_config.TextColumn("Sentiment"),
                "primary_topic": st.column_config.TextColumn("Primary Topic"),
                "urgency": st.column_config.TextColumn("Urgency"),
                "transcript": st.column_config.TextColumn("Voice Transcript", width="large"),
            }
        )

# =========================================================
# TAB 3: ASK EXECUTIVE AI (VOICE & NLP QUERY ENGINE)
# =========================================================
with tab_ask_ai:
    st.subheader("Natural language executive inquiry", anchor=False)
    st.markdown("Ask complex strategic questions about voice telemetry and customer feedback in natural language.")

    # Preset one-click voice prompt suggestions
    st.markdown("**Sample spoken voice queries (dictate or click):**")
    prompt_col1, prompt_col2, prompt_col3 = st.columns(3)
    
    with prompt_col1:
        if st.button("Voice accuracy feedback", icon=":material/record_voice_over:", width="stretch"):
            st.session_state["selected_query_preset"] = "What are customers saying about voice accuracy and dictation speed?"
    with prompt_col2:
        if st.button("Pricing & renewal complaints", icon=":material/attach_money:", width="stretch"):
            st.session_state["selected_query_preset"] = "Summarize negative feedback regarding pricing and subscriptions."
    with prompt_col3:
        if st.button("Top engineering escalations", icon=":material/warning:", width="stretch"):
            st.session_state["selected_query_preset"] = "What are the most urgent technical bugs and latency issues?"

    # Query Input
    user_query = st.text_input(
        "Spoken or typed executive question",
        value=st.session_state["selected_query_preset"] or "What are customers saying about voice accuracy and dictation speed?",
        placeholder="e.g. How do users feel about the latest latency updates?"
    )

    if st.button("Synthesize executive answer", icon=":material/auto_awesome:", type="primary"):
        with st.spinner("Analyzing voice transcripts and running semantic extraction..."):
            qa_res = nlp_engine.answer_executive_query(user_query, filtered_df)
            
            with st.container(border=True):
                st.subheader("Executive intelligence synthesis", anchor=False)
                st.caption(f"Topic context: {qa_res['matched_topic']} | Evaluated records: {qa_res['relevant_count']}")
                st.markdown(qa_res["summary"])
                
                st.markdown("#### Key findings")
                for finding in qa_res["key_findings"]:
                    st.markdown(f"- {finding}")
                    
                st.markdown("#### Grounded customer voice quotes")
                for quote in qa_res["sample_quotes"]:
                    st.chat_message("user").markdown(f"*\"{quote}\"*")
                    
                st.markdown("#### Strategic recommendations")
                for rec in qa_res["recommendations"]:
                    st.markdown(f":material/check_circle: {rec}")

# =========================================================
# TAB 4: WISPR FLOW LIVE VOICE SANDBOX
# =========================================================
with tab_sandbox:
    st.subheader("Wispr Flow voice dictation sandbox & real-time analyzer", anchor=False)
    st.markdown(
        "Dictate directly into the box below using **Wispr Flow** to test instant NLP parsing, "
        "sentiment polarity, readability scoring, and action-item extraction."
    )

    sandbox_presets = {
        "Executive Strategy Memo": "Wispr Flow voice note: We must accelerate our multi-region voice latency optimization before Q4 enterprise rollout. Customers in EMEA are reporting sporadic delays.",
        "Positive Customer Review": "The dictation accuracy for engineering pull requests and architecture documentation is breathtaking. Saved our sprint team hours of manual typing.",
        "Urgent Support Ticket": "Critical bug report: Voice transcript webhook failed during quarter-end billing sync. Please escalate to the infrastructure engineer immediately."
    }

    selected_preset = st.segmented_control(
        "Load sample voice dictation",
        options=list(sandbox_presets.keys()),
        default="Executive Strategy Memo"
    )

    sample_default = sandbox_presets.get(selected_preset, "")
    dictated_text = st.text_area(
        "Spoken voice note content (Dictate using Wispr Flow or edit below)",
        value=sample_default,
        height=130
    )

    if dictated_text.strip():
        # Run instant NLP analysis
        sent_analysis = nlp_engine.analyze_sentiment(dictated_text)
        topics = nlp_engine.classify_topics(dictated_text)
        actions = nlp_engine.extract_action_items(dictated_text)
        metrics = nlp_engine.calculate_reading_metrics(dictated_text)
        
        # Display Results
        res_col1, res_col2, res_col3 = st.columns(3)
        with res_col1:
            st.metric(
                label="Sentiment polarity",
                value=f"{sent_analysis['polarity']:+.2f}",
                delta=sent_analysis["label"],
                border=True
            )
        with res_col2:
            st.metric(
                label="Primary topic",
                value=topics[0][0],
                delta=f"Confidence: {int(topics[0][1]*100)}%",
                border=True
            )
        with res_col3:
            st.metric(
                label="Readability ease",
                value=f"{metrics['flesch_score']} / 100",
                delta=f"Est. speech: {metrics['est_speech_seconds']}s",
                border=True
            )

        with st.container(border=True):
            st.subheader("Extracted action items & urgency signals", anchor=False)
            if actions:
                for act in actions:
                    st.markdown(f":material/priority_high: **Action Trigger:** `{act}`")
            else:
                st.info("No urgent operational triggers or friction keywords detected.")

        with st.container(border=True):
            st.subheader("Cleaned executive summary", anchor=False)
            st.markdown(
                f"**Spoken Summary**: Ingested `{metrics['word_count']} words` across `{metrics['sentence_count']} sentences`. "
                f"Tone is evaluated as **{sent_analysis['label']}** with dominant domain in **{topics[0][0]}**."
            )

# ---------------------------------------------------------
# Footer & Download Briefing Report
# ---------------------------------------------------------
st.divider()

with st.container(horizontal=True, horizontal_alignment="distribute"):
    st.caption("EchoPulse AI • Voice-Driven Development Showcase for Wispr Flow")
    
    # Generate download report markdown
    report_md = f"""# EchoPulse Executive Intelligence Briefing
Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Key Metrics
- Net Sentiment: {net_sentiment}%
- Total Transcripts Evaluated: {total_records}
- Critical Escalations: {urgent_escalations}
- Average Satisfaction (CSAT): {avg_rating} / 5.0

## Top Topics
1. Voice Accuracy & Dictation Speed
2. UI & Experience
3. Integrations & API Reliability

## Recommended Actions
- Triage {urgent_escalations} high-urgency latency and webhook tickets.
- Highlight 40% documentation velocity boost in Q4 communications.
"""
    st.download_button(
        label="Download executive briefing (.md)",
        data=report_md,
        file_name="EchoPulse_Executive_Briefing.md",
        mime="text/markdown",
        icon=":material/download:"
    )
