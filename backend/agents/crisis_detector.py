"""
crisis_detector.py — Agent 2
Reads collected signals from state,
combines all sources to detect crisis type,
location, severity and confidence level.
"""

from datetime import datetime
from core.llm_client import call_llm
from core.state import crisis_state


# ── Main Agent Function ──────────────────────────────────────────
def run_crisis_detector():
    crisis_state.add_log("Agent 2", "Starting crisis detection...")

    # 1. Read Agent 1 output from state
    signals   = crisis_state.collected_signals
    weather   = crisis_state.raw_signals["weather"]
    traffic   = crisis_state.raw_signals["traffic"]

    # 2. Build prompt
    blocked_routes = [
        r["name"] for r in traffic["routes"]
        if r["status"] in ["BLOCKED", "SLOW"]
    ]

    clear_routes = [
        r["name"] for r in traffic["routes"]
        if r["status"] == "CLEAR"
    ]

    prompt = f"""
You are Crisis Detector Agent for CIRO, a crisis response system in Pakistan.
Analyze the following combined intelligence and identify the crisis.

SIGNAL SUMMARY FROM AGENT 1:
- Total signals: {signals['total_signals']}
- Keywords found: {', '.join(signals['keywords_found'])}
- Locations mentioned: {', '.join(signals['locations_mentioned'])}
- Summary: {signals['summary']}

WEATHER INTELLIGENCE:
- Alert type: {weather['alerts'][0]['type']}
- Severity: {weather['alerts'][0]['severity']}
- Rainfall: {weather['current_conditions']['rainfall_mm_per_hour']}mm/hr
- Flood risk: {weather['forecast_next_3hrs']['flood_risk']}
- Affected areas: {', '.join(weather['alerts'][0]['affected_areas'])}

TRAFFIC INTELLIGENCE:
- Blocked/slow routes: {', '.join(blocked_routes)}
- Clear routes: {', '.join(clear_routes)}

Your task:
1. Identify the type of crisis (Urban Flooding / Heatwave / Road Blockage / Accident / Infrastructure Failure)
2. Pinpoint the exact location
3. Assess severity (Low / Medium / High / Critical)
4. Assess confidence (Low / Medium / High)
5. List affected routes
6. Write a clear explanation of why you concluded this

Respond in this exact format:
CRISIS_TYPE: your answer
LOCATION: your answer
SEVERITY: your answer
CONFIDENCE: your answer
AFFECTED_ROUTES: route1, route2
EXPLANATION: your explanation here
"""

    crisis_state.add_log("Agent 2", "Analyzing combined signals with Gemini...")
    response = call_llm(prompt)

    # 3. Check for errors
    if response.startswith("ERROR"):
        crisis_state.add_log("Agent 2", f"LLM Error: {response}")
        # Fallback
        crisis_state.detected_crisis = {
            "type"            : "Urban Flooding",
            "location"        : "G-10, Islamabad",
            "severity"        : "Critical",
            "confidence"      : "High",
            "explanation"     : "5 social media posts + heavy rainfall alert (42mm/hr) + G-10 Main Boulevard fully blocked with 34 stranded vehicles all point to severe urban flooding in G-10.",
            "affected_routes" : ["G-10 Main Boulevard", "G-9 Kanal Road"],
            "detected_at"     : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        crisis_state.add_log("Agent 2", "Used fallback crisis data due to LLM error.")
        crisis_state.pipeline_status["agent_2_done"] = True
        return

    # 4. Parse response
    crisis_type      = ""
    location         = ""
    severity         = ""
    confidence       = ""
    affected_routes  = []
    explanation      = ""

    for line in response.splitlines():
        line = line.strip()
        if line.startswith("CRISIS_TYPE:"):
            crisis_type = line.replace("CRISIS_TYPE:", "").strip()
        elif line.startswith("LOCATION:"):
            location = line.replace("LOCATION:", "").strip()
        elif line.startswith("SEVERITY:"):
            severity = line.replace("SEVERITY:", "").strip()
        elif line.startswith("CONFIDENCE:"):
            confidence = line.replace("CONFIDENCE:", "").strip()
        elif line.startswith("AFFECTED_ROUTES:"):
            affected_routes = [r.strip() for r in line.replace("AFFECTED_ROUTES:", "").split(",")]
        elif line.startswith("EXPLANATION:"):
            explanation = line.replace("EXPLANATION:", "").strip()

    # 5. Save to state
    crisis_state.detected_crisis = {
        "type"           : crisis_type,
        "location"       : location,
        "severity"       : severity,
        "confidence"     : confidence,
        "explanation"    : explanation,
        "affected_routes": affected_routes,
        "detected_at"    : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    crisis_state.add_log("Agent 2", f"Crisis identified: {crisis_type} at {location}")
    crisis_state.add_log("Agent 2", f"Severity: {severity} | Confidence: {confidence}")
    crisis_state.add_log("Agent 2", f"Explanation: {explanation}")
    crisis_state.pipeline_status["agent_2_done"] = True
    crisis_state.add_log("Agent 2", "✅ Done. Passing to Agent 3.")