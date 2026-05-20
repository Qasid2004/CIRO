"""
action_planner.py — Agent 3
Reads detected crisis from state,
generates a coordinated response plan
including routing, alerts, and resource deployment.
"""

from core.llm_client import call_llm
from core.state import crisis_state


# ── Main Agent Function ──────────────────────────────────────────
def run_action_planner():
    crisis_state.add_log("Agent 3", "Starting action planning...")

    # 1. Read Agent 2 output from state
    crisis   = crisis_state.detected_crisis
    traffic  = crisis_state.raw_signals["traffic"]
    resources = crisis_state.raw_signals["resources"]

    # 2. Prepare available resources summary
    available_units = [
        f'{u["unit_id"]} ({u["type"]}) — {u["current_location"]} — {u["distance_to_G10_km"]}km away'
        for u in resources["units"]
        if u["status"] == "AVAILABLE"
    ]

    # 3. Prepare alternate routes
    alternate_routes = [
        f'{r["name"]} — Status: {r["status"]} — Speed: {r["average_speed_kmh"]}km/h'
        for r in traffic["routes"]
        if r["status"] == "CLEAR"
    ]

    prompt = f"""
You are Action Planner Agent for CIRO, a crisis response system in Pakistan.
A crisis has been detected. Generate a coordinated response plan.

DETECTED CRISIS:
- Type      : {crisis['type']}
- Location  : {crisis['location']}
- Severity  : {crisis['severity']}
- Confidence: {crisis['confidence']}
- Explanation: {crisis['explanation']}
- Affected routes: {', '.join(crisis['affected_routes'])}

AVAILABLE EMERGENCY RESOURCES:
{chr(10).join(available_units)}

AVAILABLE ALTERNATE ROUTES:
{chr(10).join(alternate_routes)}

Your task:
Generate a realistic, coordinated response plan with:
1. 3-5 specific response actions (be specific, mention unit IDs and route names)
2. Which resources to deploy and where
3. Which alternate routes to activate
4. A public alert message in both English and Roman Urdu
5. Priority level (IMMEDIATE / HIGH / MEDIUM)

Respond in this exact format:
ACTIONS: action1 | action2 | action3 | action4 | action5
RESOURCES: unit_id1 to location1 | unit_id2 to location2
ALTERNATE_ROUTES: route1 | route2
ALERT_EN: english alert message here
ALERT_UR: roman urdu alert message here
PRIORITY: your answer
"""

    crisis_state.add_log("Agent 3", "Generating response plan with Gemini...")
    response = call_llm(prompt)

    # 4. Check for errors
    if response.startswith("ERROR"):
        crisis_state.add_log("Agent 3", f"LLM Error: {response}")
        # Fallback
        crisis_state.action_plan = {
            "actions": [
                "Close G-10 Main Boulevard and redirect all traffic",
                "Deploy Rescue Team RES-02 to G-10 immediately",
                "Dispatch Ambulance AMB-07 via G-11 Link Road",
                "Deploy Water Pump Truck PUMP-01 to G-10 drainage point",
                "Station Traffic Police POLICE-G10 at G-10 entry points"
            ],
            "resources_to_deploy": [
                "RES-02 → G-10 Main Boulevard",
                "AMB-07 → G-10 via G-11 Link Road",
                "PUMP-01 → G-10 Drainage Point",
                "POLICE-G10 → G-10 Entry Points"
            ],
            "alternate_routes": [
                "Islamabad Expressway",
                "G-11 Link Road"
            ],
            "alert_message": {
                "en": "EMERGENCY ALERT: Severe flooding in G-10 Islamabad. Avoid G-10 Main Boulevard. Use Islamabad Expressway or G-11 Link Road as alternate routes. Emergency services deployed.",
                "ur": "ZARURI ITLAA: G-10 Islamabad mein shadeed saili. G-10 Main Boulevard se bachein. Islamabad Expressway ya G-11 Link Road use karein. Emergency services aa rahi hain."
            },
            "priority": "IMMEDIATE"
        }
        crisis_state.add_log("Agent 3", "Used fallback action plan due to LLM error.")
        crisis_state.pipeline_status["agent_3_done"] = True
        return

    # 5. Parse response
    actions          = []
    resources        = []
    alternate_routes = []
    alert_en         = ""
    alert_ur         = ""
    priority         = ""

    for line in response.splitlines():
        line = line.strip()
        if line.startswith("ACTIONS:"):
            actions = [a.strip() for a in line.replace("ACTIONS:", "").split("|")]
        elif line.startswith("RESOURCES:"):
            resources = [r.strip() for r in line.replace("RESOURCES:", "").split("|")]
        elif line.startswith("ALTERNATE_ROUTES:"):
            alternate_routes = [r.strip() for r in line.replace("ALTERNATE_ROUTES:", "").split("|")]
        elif line.startswith("ALERT_EN:"):
            alert_en = line.replace("ALERT_EN:", "").strip()
        elif line.startswith("ALERT_UR:"):
            alert_ur = line.replace("ALERT_UR:", "").strip()
        elif line.startswith("PRIORITY:"):
            priority = line.replace("PRIORITY:", "").strip()

    # 6. Save to state
    crisis_state.action_plan = {
        "actions"            : actions,
        "resources_to_deploy": resources,
        "alternate_routes"   : alternate_routes,
        "alert_message"      : {"en": alert_en, "ur": alert_ur},
        "priority"           : priority
    }

    crisis_state.add_log("Agent 3", f"Priority: {priority}")
    crisis_state.add_log("Agent 3", f"Actions planned: {len(actions)}")
    for i, action in enumerate(actions, 1):
        crisis_state.add_log("Agent 3", f"  Action {i}: {action}")
    crisis_state.add_log("Agent 3", f"Alternate routes: {', '.join(alternate_routes)}")
    crisis_state.pipeline_status["agent_3_done"] = True
    crisis_state.add_log("Agent 3", "✅ Done. Passing to Agent 4.")