"""
NLP Engine for EchoPulse: Executive Voice & Text Intelligence Dashboard.
Provides self-contained natural language processing algorithms:
- Sentiment & Polarity Scoring
- Topic & Theme Extraction
- Action-Item & Urgency Detection
- Executive Natural Language Query Engine
- Mock Dataset Generation for Executive Analytics
"""

import re
import datetime
import random
from typing import Dict, List, Any, Tuple
import pandas as pd
import numpy as np

# Lexicons for high-accuracy local NLP scoring without heavy dependencies
POSITIVE_WORDS = {
    "love", "great", "excellent", "fast", "accurate", "reliable", "smooth", 
    "fantastic", "intuitive", "helpful", "amazing", "productive", "seamless",
    "clean", "powerful", "best", "superb", "brilliant", "delighted", "efficient",
    "saved", "game-changer", "impressive", "outstanding", "flawless", "clear"
}

NEGATIVE_WORDS = {
    "slow", "bug", "broken", "lag", "latency", "confusing", "error", "fails",
    "failed", "difficult", "poor", "freeze", "crash", "expensive", "bad",
    "frustrated", "unusable", "terrible", "horrible", "delay", "disconnect",
    "inaccurate", "misunderstood", "dropped", "stuck", "annoying", "glitch"
}

URGENCY_TRIGGERS = [
    "urgent", "asap", "immediately", "critical", "blocking", "cannot access",
    "revenue impact", "customer lost", "escalate", "down", "p0", "p1", "cancelled"
]

TOPICS_TAXONOMY = {
    "Voice Accuracy": ["voice", "dictation", "accuracy", "speech", "misunderstood", "pronunciation", "accent", "whisper", "wispr", "transcription", "hallucination"],
    "Speed & Latency": ["slow", "fast", "lag", "latency", "response", "speed", "realtime", "instant", "freeze", "stall", "delay"],
    "UI & Experience": ["interface", "ui", "ux", "design", "navigation", "layout", "button", "theme", "clean", "cluttered", "dashboard"],
    "Pricing & Plans": ["price", "cost", "subscription", "expensive", "billing", "tier", "plan", "discount", "renewal", "invoice", "quota"],
    "Integrations & API": ["api", "integration", "slack", "notion", "webhook", "export", "connect", "browser", "extension", "sdk"],
    "Audio Quality": ["microphone", "mic", "background", "noise", "audio", "clarity", "sound", "headset", "disconnect", "disconnects", "distorted"]
}

SAMPLE_VOICE_TRANSCRIPTS = [
    ("Wispr Flow's dictation accuracy on technical jargon and variable names is nothing short of breathtaking. Saved me 3 hours of typing today.", "Wispr Flow Voice Notes", "Global", 5),
    ("The new voice latency is under 200 milliseconds, feeling practically instantaneous during my executive standup summaries.", "Wispr Flow Voice Notes", "North America", 5),
    ("Encountering random audio disconnects during long zoom calls. Need this fixed ASAP as it interrupts board meetings.", "Customer Support Calls", "EMEA", 1),
    ("Our sales team switched to voice notes for CRM updates; sales cycle documentation velocity improved by 40%.", "Product Reviews", "North America", 5),
    ("Subscription renewal pricing for the enterprise tier feels steep given that mobile voice synchronization sometimes lags.", "Customer Support Calls", "EMEA", 2),
    ("The UI is extremely clean, but I really wish we had a dark mode toggle on the desktop dashboard.", "Product Reviews", "APAC", 3),
    ("Voice recognition struggles slightly when two people speak simultaneously in conference room settings.", "Customer Support Calls", "APAC", 2),
    ("Critical issue: Latency spiked to 8 seconds during live customer demo. P0 blocking issue for our deployment team.", "Customer Support Calls", "North America", 1),
    ("We replaced keyboard documentation with voice dictation for our engineering incident reviews. Phenomenal developer productivity boost.", "Wispr Flow Voice Notes", "North America", 5),
    ("Critical issue: Voice export webhook failed during quarter-end reporting. Please escalate to the on-call engineer immediately.", "Customer Support Calls", "North America", 1),
    ("Loving the accurate punctuation insertion and filler word removal. My spoken memos now look polished and professional.", "Wispr Flow Voice Notes", "Global", 5),
    ("Urgent billing blocker: Enterprise invoice payment failed and our organization voice quota has been suspended.", "Customer Support Calls", "EMEA", 1),
    ("Customer support response was prompt and resolved our API authentication glitch within 20 minutes.", "Customer Support Calls", "EMEA", 4),
    ("The background noise cancellation while dictating from busy coffee shops is genuinely best in class.", "Product Reviews", "Global", 5),
    ("Severe accuracy degradation on accented speech during quarterly board recording. Needs urgent model tuning.", "Customer Support Calls", "APAC", 1),
    ("API rate limit error 429 when processing high-volume voice transcripts batch runs. Need documentation on enterprise quota increases.", "Customer Support Calls", "North America", 2),
    ("Very intuitive onboarding experience. New team members were voice-dictating sprint tickets in under 5 minutes.", "Product Reviews", "APAC", 5),
    ("Noticeable latency spike during peak US East hours between 2 PM and 4 PM EST.", "Customer Support Calls", "North America", 2),
    ("Wispr Flow voice shortcut integration with Cursor and VS Code makes hands-free coding surprisingly viable.", "Wispr Flow Voice Notes", "Global", 5),
]

def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Computes sentiment polarity (-1.0 to +1.0), subjectivity score, and sentiment label.
    """
    words = re.findall(r"\b\w+\b", text.lower())
    if not words:
        return {"polarity": 0.0, "label": "Neutral", "positive_count": 0, "negative_count": 0, "confidence": 0.5}

    pos_count = sum(1 for w in words if w in POSITIVE_WORDS)
    neg_count = sum(1 for w in words if w in NEGATIVE_WORDS)
    total_sentiment_words = pos_count + neg_count

    if total_sentiment_words == 0:
        polarity = 0.0
        label = "Neutral"
        confidence = 0.70
    else:
        polarity = (pos_count - neg_count) / max(total_sentiment_words, 1)
        # Smooth between -1.0 and 1.0
        polarity = round(max(-1.0, min(1.0, polarity)), 2)
        if polarity > 0.15:
            label = "Positive"
        elif polarity < -0.15:
            label = "Negative"
        else:
            label = "Neutral"
        confidence = round(min(0.98, 0.65 + (total_sentiment_words * 0.06)), 2)

    return {
        "polarity": polarity,
        "label": label,
        "positive_count": pos_count,
        "negative_count": neg_count,
        "confidence": confidence
    }

def classify_topics(text: str) -> List[Tuple[str, float]]:
    """
    Scores and returns relevant topics with confidence weights using word boundaries.
    """
    text_lower = text.lower()
    scores = {}
    for topic, keywords in TOPICS_TAXONOMY.items():
        hits = 0
        for kw in keywords:
            pattern = r"\b" + re.escape(kw) + r"\b"
            if re.search(pattern, text_lower):
                hits += 1
        if hits > 0:
            scores[topic] = round(min(1.0, hits * 0.35 + 0.3), 2)
    
    if not scores:
        scores["General Feedback"] = 0.50
        
    sorted_topics = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_topics

def extract_action_items(text: str) -> List[str]:
    """
    Detects actionable requests, bug signals, or critical user demands.
    """
    sentences = re.split(r"[.!?]+", text)
    action_items = []
    
    action_cues = ["need", "must", "please", "issue", "failed", "bug", "wish", "struggles", "escalate", "fix", "improve"]
    
    for sentence in sentences:
        s = sentence.strip()
        if not s:
            continue
        lower_s = s.lower()
        if any(cue in lower_s for cue in action_cues) or any(urg in lower_s for urg in URGENCY_TRIGGERS):
            action_items.append(s)
            
    return action_items

def calculate_reading_metrics(text: str) -> Dict[str, Any]:
    """
    Calculates readability, word count, character count, and estimated speaking duration.
    """
    words = re.findall(r"\b\w+\b", text)
    word_count = len(words)
    char_count = len(text)
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    num_sentences = max(len(sentences), 1)
    
    # Simple Flesch Reading Ease estimate
    avg_words_per_sentence = word_count / num_sentences
    syllable_estimate = sum(max(1, len(re.findall(r"[aeiouy]+", w.lower()))) for w in words)
    avg_syllables_per_word = (syllable_estimate / max(word_count, 1))
    
    flesch_score = round(206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word), 1)
    flesch_score = max(0, min(100, flesch_score))
    
    # Speaking duration (assuming average 140 words per minute for natural speech)
    est_speech_seconds = round((word_count / 140) * 60, 1) if word_count else 0
    
    return {
        "word_count": word_count,
        "char_count": char_count,
        "sentence_count": num_sentences,
        "flesch_score": flesch_score,
        "est_speech_seconds": est_speech_seconds
    }

def generate_analytics_dataset(n_samples: int = 240) -> pd.DataFrame:
    """
    Generates a rich, realistic customer voice transcript analytics dataset spanning 30 days.
    """
    random.seed(42)
    np.random.seed(42)
    
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=29)
    
    records = []
    
    for i in range(n_samples):
        # Pick base template and add variations
        base_text, channel, region, base_rating = random.choice(SAMPLE_VOICE_TRANSCRIPTS)
        
        # Add random date in past 30 days
        days_ago = random.randint(0, 29)
        date = end_date - datetime.timedelta(days=days_ago)
        
        # Calculate NLP features
        sentiment_res = analyze_sentiment(base_text)
        topics = classify_topics(base_text)
        actions = extract_action_items(base_text)
        urgency = "High" if any(u in base_text.lower() for u in URGENCY_TRIGGERS) else ("Medium" if sentiment_res["label"] == "Negative" else "Normal")
        
        records.append({
            "id": f"TRX-{1000 + i}",
            "date": pd.to_datetime(date),
            "transcript": base_text,
            "channel": channel,
            "region": region,
            "rating": base_rating,
            "sentiment": sentiment_res["label"],
            "polarity": sentiment_res["polarity"],
            "primary_topic": topics[0][0],
            "urgency": urgency,
            "has_action_item": len(actions) > 0,
            "word_count": len(base_text.split()),
        })
        
    df = pd.DataFrame(records)
    df = df.sort_values(by="date", ascending=True).reset_index(drop=True)
    return df

def answer_executive_query(query: str, df: pd.DataFrame) -> Dict[str, Any]:
    """
    Processes natural language queries from leadership, retrieves matching data context,
    and returns a structured executive briefing.
    """
    query_lower = query.lower()
    
    # 1. Detect target topic
    matched_topic = None
    for topic, keywords in TOPICS_TAXONOMY.items():
        if topic.lower() in query_lower or any(kw in query_lower for kw in keywords):
            matched_topic = topic
            break
            
    # 2. Filter relevant transcripts
    relevant_df = df.copy()
    if matched_topic:
        relevant_df = relevant_df[relevant_df["primary_topic"] == matched_topic]
        
    if "negative" in query_lower or "complaint" in query_lower or "issue" in query_lower or "friction" in query_lower:
        relevant_df = relevant_df[relevant_df["sentiment"] == "Negative"]
    elif "positive" in query_lower or "praise" in query_lower or "delight" in query_lower:
        relevant_df = relevant_df[relevant_df["sentiment"] == "Positive"]
        
    if len(relevant_df) == 0:
        relevant_df = df.sample(min(5, len(df)))
        
    sample_quotes = relevant_df["transcript"].drop_duplicates().head(3).tolist()
    
    # Compute metrics
    pos_pct = round((df["sentiment"] == "Positive").mean() * 100, 1)
    neg_pct = round((df["sentiment"] == "Negative").mean() * 100, 1)
    top_topic = df["primary_topic"].value_counts().index[0]
    urgent_count = (df["urgency"] == "High").sum()
    
    # Synthesize intelligent answer
    summary = f"Based on analysis of {len(df)} ingested voice and customer transcripts across the selected period:"
    key_findings = [
        f"**Sentiment Distribution**: Overall customer sentiment remains robust at **{pos_pct}% Positive** versus **{neg_pct}% Negative**.",
        f"**Primary Driver**: The dominant discussion category is **'{matched_topic or top_topic}'**, representing high engagement from enterprise voice users.",
        f"**Critical Alerts**: Identified **{urgent_count} high-urgency escalations** requiring engineering and customer success triage."
    ]
    
    recommendations = [
        "Prioritize latency optimization for peak traffic windows to maintain voice dictation responsiveness.",
        "Empower support team with automated Wispr Flow transcript summaries to resolve tickets 30% faster.",
        "Highlight hands-free coding and voice note productivity metrics in upcoming Q4 investor updates."
    ]
    
    return {
        "query": query,
        "matched_topic": matched_topic or "Cross-Functional Overview",
        "sample_quotes": sample_quotes,
        "summary": summary,
        "key_findings": key_findings,
        "recommendations": recommendations,
        "relevant_count": len(relevant_df)
    }
