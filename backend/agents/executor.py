"""
executor.py — Agent 4
Reads action plan from state and simulates
the execution of all response actions.
Creates emergency tickets, sends alerts,
updates route statuses, and calculates outcome.
"""

import random
from datetime import datetime
from core.llm_client import call_llm
from core.state import crisis_state


# ── Ticket Counter ───────────────────────────────────────────────
ticket_counter = 1000


def generate_ticket_id():
    global ticket_counter
    ticket_counter += 1
    return f"EMG-{ticket_counter}"


# ── Simulate Route Updates ───────────────────────────────────────
def simulate_route_updates():
    crisis_state.add_log("Agent 4", "Updating route statuses...")

    traffic = crisis_state.raw_signals["traffic"]
    routes  = {}

    for route in traffic["routes"]:
        before_status = route["status"]
        before_speed  = route["average_speed_kmh"]

        # Apply simulation logic
        if route["status"] == "BLOCKED":
            after_status = "CLOSED — EMERGENCY RESPONSE ACTIVE"
            after_speed  = 0
        elif route["status"] == "SLOW":
            after_status = "MODERATE — TRAFFIC BEING DIVERTED"
            after_speed  = min(route["average_speed_kmh"] + 15, route["normal_speed_kmh"])
        elif route["status"] == "CLEAR":
            # Clear routes get more traffic as alternate
            if route["name"] in crisis_state.action_plan.get("alternate_routes", []):
                after_status = "ACTIVE ALTERNATE ROUTE"
                after_speed  = route["average_speed_kmh"]
            else:
                after_status = "CLEAR"
                after_speed  = route["average_speed_kmh"]

        routes[route["route_id"]] = {
            "name"        : route["name"],
            "before_status": before_status,
            "after_status" : after_status,
            "before_speed" : before_speed,
            "after_speed"  : after_speed,
            "before_congestion": route["congestion_score"],
            "after_congestion" : max(route["congestion_score"] - random.randint(20, 40), 0)
                                 if route["status"] != "BLOCKED"
                                 else route["congestion_score"]
        }

        crisis_state.add_log(
            "Agent 4",
            f"Route {route['name']}: {before_status} → {after_status}"
        )

    crisis_state.simulation["routes"] = routes


# ── Simulate Emergency Dispatch ──────────────────────────────────
def simulate_dispatch():
    crisis_state.add_log("Agent 4", "Dispatching emergency resources...")

    resources    = crisis_state.raw_signals["resources"]
    deployed     = []
    tickets      = []
    plan         = crisis_state.action_plan

    for unit in resources["units"]:
        if unit["status"] == "AVAILABLE":
            # Check if this unit is in the action plan
            unit_mentioned = any(
                unit["unit_id"] in r
                for r in plan.get("resources_to_deploy", [])
            )

            if unit_mentioned or unit["type"] in ["Rescue Team", "Water Pump Truck", "Traffic Police Unit"]:
                ticket_id = generate_ticket_id()
                timestamp = datetime.now().strftime("%H:%M:%S")

                ticket = {
                    "id"       : ticket_id,
                    "unit_id"  : unit["unit_id"],
                    "type"     : unit["type"],
                    "from"     : unit["current_location"],
                    "to"       : crisis_state.detected_crisis["location"],
                    "status"   : "DISPATCHED",
                    "eta_mins" : max(int(unit["distance_to_G10_km"] * 2), 3),
                    "created_at": timestamp
                }

                tickets.append(ticket)
                deployed.append(f"{unit['unit_id']} ({unit['type']})")

                crisis_state.add_log(
                    "Agent 4",
                    f"Ticket {ticket_id} created — {unit['type']} dispatched from {unit['current_location']}"
                )

    crisis_state.simulation["tickets"]            = tickets
    crisis_state.simulation["resources_deployed"] = deployed


# ── Simulate Alert Sending ───────────────────────────────────────
def simulate_alerts():
    crisis_state.add_log("Agent 4", "Sending public alerts...")

    alert_plan = crisis_state.action_plan.get("alert_message", {})
    timestamp  = datetime.now().strftime("%H:%M:%S")

    alerts = [
        {
            "channel"   : "SMS Broadcast",
            "message"   : alert_plan.get("en", "Emergency alert issued."),
            "sent_to"   : "5,200 users in G-10 area",
            "status"    : "SENT",
            "timestamp" : timestamp
        },
        {
            "channel"   : "WhatsApp Broadcast",
            "message"   : alert_plan.get("ur", "Zaruri itlaa jaari."),
            "sent_to"   : "3,800 users in G-10 area",
            "status"    : "SENT",
            "timestamp" : timestamp
        },
        {
            "channel"   : "Traffic App Notification",
            "message"   : f"ROAD CLOSED: G-10 Main Boulevard. Use alternate routes.",
            "sent_to"   : "12,500 active app users",
            "status"    : "SENT",
            "timestamp" : timestamp
        }
    ]

    crisis_state.simulation["alerts"] = alerts

    for alert in alerts:
        crisis_state.add_log(
            "Agent 4",
            f"Alert sent via {alert['channel']} to {alert['sent_to']}"
        )


# ── Calculate Outcome ────────────────────────────────────────────
def calculate_outcome():
    crisis_state.add_log("Agent 4", "Calculating outcome...")

    traffic = crisis_state.raw_signals["traffic"]

    # Before — average congestion across all routes
    congestion_before = int(
        sum(r["congestion_score"] for r in traffic["routes"]) /
        len(traffic["routes"])
    )

    # After — simulate reduction due to response
    congestion_after = max(congestion_before - random.randint(25, 40), 15)

    # Response time — based on nearest unit
    resources = crisis_state.raw_signals["resources"]
    available = [u for u in resources["units"] if u["status"] == "AVAILABLE"]
    if available:
        nearest_km       = min(u["distance_to_G10_km"] for u in available)
        response_time    = max(int(nearest_km * 2), 3)
    else:
        response_time    = 10

    crisis_state.outcome = {
        "congestion_before"      : congestion_before,
        "congestion_after"       : congestion_after,
        "response_time_minutes"  : response_time,
        "units_deployed"         : len(crisis_state.simulation["tickets"]),
        "alerts_sent"            : len(crisis_state.simulation["alerts"]),
        "routes_updated"         : len(crisis_state.simulation["routes"]),
        "status"                 : "IN_PROGRESS"
    }

    crisis_state.add_log(
        "Agent 4",
        f"Congestion reduced: {congestion_before}% → {congestion_after}%"
    )
    crisis_state.add_log(
        "Agent 4",
        f"First responder ETA: {response_time} minutes"
    )


# ── Generate LLM Outcome Summary ────────────────────────────────
def generate_outcome_summary():
    outcome  = crisis_state.outcome
    crisis   = crisis_state.detected_crisis
    sim      = crisis_state.simulation

    prompt = f"""
You are the Executor Agent for CIRO, a crisis response system in Pakistan.
Summarize the outcome of the emergency response in 3-4 sentences.
Be specific, confident, and professional.

Crisis: {crisis['type']} at {crisis['location']}
Units deployed: {outcome['units_deployed']}
Alerts sent to: {sum(int(a['sent_to'].split()[0].replace(',','')) for a in sim['alerts'])} people
Congestion reduced from {outcome['congestion_before']}% to {outcome['congestion_after']}%
Response time: {outcome['response_time_minutes']} minutes

Write the outcome summary:
"""

    response = call_llm(prompt)

    if response.startswith("ERROR"):
        summary = (
            f"Emergency response successfully initiated for {crisis['type']} in {crisis['location']}. "
            f"{outcome['units_deployed']} units deployed with first responder ETA of {outcome['response_time_minutes']} minutes. "
            f"Traffic congestion reduced from {outcome['congestion_before']}% to {outcome['congestion_after']}% "
            f"through alternate route activation. Public alerts dispatched to over 21,000 residents."
        )
    else:
        summary = response.strip()

    crisis_state.outcome["summary"] = summary
    crisis_state.add_log("Agent 4", f"Outcome: {summary}")


# ── Main Agent Function ──────────────────────────────────────────
def run_executor():
    crisis_state.add_log("Agent 4", "Starting execution simulation...")

    simulate_route_updates()
    simulate_dispatch()
    simulate_alerts()
    calculate_outcome()
    generate_outcome_summary()

    crisis_state.pipeline_status["agent_4_done"] = True
    crisis_state.add_log("Agent 4", "✅ Done. Full pipeline complete.")