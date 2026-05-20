"""
signal_collector.py — Agent 1
Reads all mock data sources, normalizes them,
and summarizes the signals for Agent 2.
"""

import json
import os
from core.llm_client import call_llm
from core.state import crisis_state


# ── Load Mock Data ───────────────────────────────────────────────
def load_mock_data():
    base = os.path.join(os.path.dirname(__file__), '..', 'data')

    with open(os.path.join(base, 'mock_social.json'),    encoding='utf-8') as f:
        social = json.load(f)
    with open(os.path.join(base, 'mock_weather.json'),   encoding='utf-8') as f:
        weather = json.load(f)
    with open(os.path.join(base, 'mock_traffic.json'),   encoding='utf-8') as f:
        traffic = json.load(f)
    with open(os.path.join(base, 'mock_resources.json'), encoding='utf-8') as f:
        resources = json.load(f)

    return social, weather, traffic, resources


# ── Main Agent Function ──────────────────────────────────────────
def run_signal_collector(user_input: str = ""):
    crisis_state.add_log("Agent 1", "Starting signal collection...")
    crisis_state.user_message = user_input

    # 1. Load all mock data
    social, weather, traffic, resources = load_mock_data()
    crisis_state.user_message = user_input

    # 2. Save raw signals to state
    crisis_state.raw_signals["social_posts"] = social["posts"]
    crisis_state.raw_signals["weather"]      = weather["weather_alert"]
    crisis_state.raw_signals["traffic"]      = traffic["traffic_report"]
    crisis_state.raw_signals["resources"]    = resources["emergency_resources"]

    # 3. Build the prompt for Gemini
    social_texts = "\n".join(
        [f'- [{p["platform"]}] {p["text"]} (location: {p["location"]})' 
         for p in social["posts"]]
    )

    weather_summary = (
        f"Alert: {weather['weather_alert']['alerts'][0]['type']} | "
        f"Severity: {weather['weather_alert']['alerts'][0]['severity']} | "
        f"Rainfall: {weather['weather_alert']['current_conditions']['rainfall_mm_per_hour']}mm/hr | "
        f"Flood Risk: {weather['weather_alert']['forecast_next_3hrs']['flood_risk']}"
    )

    traffic_summary = "\n".join(
        [f'- Route: {r["name"]} | Status: {r["status"]} | '
         f'Congestion: {r["congestion_score"]}% | Incident: {r["incident"]}'
         for r in traffic["traffic_report"]["routes"]]
    )

    user_signal = f"\nUser reported: {user_input}" if user_input else ""

    prompt = f"""
You are Signal Collector Agent for CIRO, a crisis response system in Pakistan.
Analyze the following signals from multiple sources and extract key information.

SOCIAL MEDIA POSTS (may contain Roman Urdu, Urdu, or English):
{social_texts}
{user_signal}

WEATHER DATA:
{weather_summary}

TRAFFIC DATA:
{traffic_summary}

Your task:
1. Identify all crisis-related keywords (e.g. flood, pani, blocked, stranded)
2. Identify all locations mentioned
3. Count total number of signals
4. Write a 2-3 sentence summary of what is happening

Respond in this exact format:
KEYWORDS: keyword1, keyword2, keyword3
LOCATIONS: location1, location2
TOTAL_SIGNALS: number
SUMMARY: your summary here
"""

    crisis_state.add_log("Agent 1", "Sending signals to Gemini for analysis...")
    response = call_llm(prompt)

    # 4. Check for errors
    if response.startswith("ERROR"):
        crisis_state.add_log("Agent 1", f"LLM Error: {response}")
        # Fallback — fill state manually without LLM
        user_text = user_input.lower()

        if "wire" in user_text or "khamba" in user_text or "bijli" in user_text:
            crisis_state.collected_signals = {
                "total_signals": 3,
                "social_count": 1,
                "keywords_found": ["wire", "khamba", "bijli", "danger"],
                "locations_mentioned": ["I-8", "Islamabad"],
                "summary": "Reports of fallen electric pole and live wires in I-8 Islamabad."
    }

        elif "garmi" in user_text or "heat" in user_text:
            crisis_state.collected_signals = {
                "total_signals": 3,
                "social_count": 1,
                "keywords_found": ["heatwave", "garmi", "heat stroke"],
                "locations_mentioned": ["F-7", "Islamabad"],
                "summary": "Extreme heatwave conditions reported in F-7 Islamabad."
    }

        elif "flood" in user_text or "pani" in user_text or "barish" in user_text:
            user_text = user_input.lower()

            if "i-8" in user_text or "wire" in user_text or "bijli" in user_text:
                crisis_state.collected_signals = {
                    "total_signals": 3,
                    "social_count": 1,
                    "keywords_found": ["wire", "bijli", "khamba"],
                    "locations_mentioned": ["I-8", "Islamabad"],
                    "summary": "Electric pole collapse reported in I-8 Islamabad with dangerous live wires."
                }

            elif "g-10" in user_text or "flood" in user_text or "pani" in user_text:
                crisis_state.collected_signals = {
                    "total_signals": 6,
                    "social_count": 5,
                    "keywords_found": ["flood", "pani", "blocked", "stranded"],
                    "locations_mentioned": ["G-10", "Islamabad"],
                    "summary": "Urban flooding reported in G-10 Islamabad."
                }

            else:
                crisis_state.collected_signals = {
                    "total_signals": 1,
                    "social_count": 1,
                    "keywords_found": ["unknown"],
                    "locations_mentioned": ["Unknown"],
                    "summary": user_input
                }

        else:
            crisis_state.collected_signals = {
                "total_signals": 1,
                "social_count": 1,
                "keywords_found": ["unknown"],
        "locations_mentioned": ["Unknown"],
        "summary": user_input
    }
        crisis_state.add_log("Agent 1", "Used fallback data due to LLM error.")
        crisis_state.pipeline_status["agent_1_done"] = True
        return

    # 5. Parse the response
    keywords  = []
    locations = []
    total     = 0
    summary   = ""

    for line in response.splitlines():
        line = line.strip()
        if line.startswith("KEYWORDS:"):
            keywords = [k.strip() for k in line.replace("KEYWORDS:", "").split(",")]
        elif line.startswith("LOCATIONS:"):
            locations = [l.strip() for l in line.replace("LOCATIONS:", "").split(",")]
        elif line.startswith("TOTAL_SIGNALS:"):
            try:
                total = int(line.replace("TOTAL_SIGNALS:", "").strip())
            except:
                total = len(social["posts"]) + 1
        elif line.startswith("SUMMARY:"):
            summary = line.replace("SUMMARY:", "").strip()

    # 6. Save to state
    crisis_state.collected_signals = {
        "total_signals"      : total,
        "social_count"       : len(social["posts"]),
        "keywords_found"     : keywords,
        "locations_mentioned": locations,
        "summary"            : summary
    }

    crisis_state.add_log("Agent 1", f"Collected {total} signals. Keywords: {', '.join(keywords)}")
    crisis_state.add_log("Agent 1", f"Summary: {summary}")
    crisis_state.pipeline_status["agent_1_done"] = True
    crisis_state.add_log("Agent 1", "✅ Done. Passing to Agent 2.")