"""
simulator.py — Simulation Display
Formats and displays the full simulation
results in a clean, readable way in the terminal.
This is what gets sent to the UI later.
"""

import json
from core.state import crisis_state


# ── Display Route Simulation ─────────────────────────────────────
def display_routes():
    print("\n🗺️  ROUTE SIMULATION")
    print("─" * 60)

    routes = crisis_state.simulation.get("routes", {})

    if not routes:
        print("  No route data available.")
        return

    for route_id, route in routes.items():
        print(f"\n  📍 {route['name']}")
        print(f"     BEFORE → Status: {route['before_status']} | "
              f"Congestion: {route['before_congestion']}% | "
              f"Speed: {route['before_speed']} km/h")
        print(f"     AFTER  → Status: {route['after_status']} | "
              f"Congestion: {route['after_congestion']}% | "
              f"Speed: {route['after_speed']} km/h")


# ── Display Emergency Tickets ────────────────────────────────────
def display_tickets():
    print("\n🎫  EMERGENCY TICKETS")
    print("─" * 60)

    tickets = crisis_state.simulation.get("tickets", [])

    if not tickets:
        print("  No tickets created.")
        return

    for ticket in tickets:
        print(f"\n  🚨 Ticket ID  : {ticket['id']}")
        print(f"     Unit      : {ticket['unit_id']} ({ticket['type']})")
        print(f"     From      : {ticket['from']}")
        print(f"     To        : {ticket['to']}")
        print(f"     Status    : {ticket['status']}")
        print(f"     ETA       : {ticket['eta_mins']} minutes")
        print(f"     Created At: {ticket['created_at']}")


# ── Display Alerts ───────────────────────────────────────────────
def display_alerts():
    print("\n📢  ALERTS SENT")
    print("─" * 60)

    alerts = crisis_state.simulation.get("alerts", [])

    if not alerts:
        print("  No alerts sent.")
        return

    for alert in alerts:
        print(f"\n  📣 Channel  : {alert['channel']}")
        print(f"     Message  : {alert['message']}")
        print(f"     Sent To  : {alert['sent_to']}")
        print(f"     Status   : {alert['status']}")
        print(f"     Time     : {alert['timestamp']}")


# ── Display Before vs After Outcome ─────────────────────────────
def display_outcome():
    print("\n📊  OUTCOME — BEFORE vs AFTER")
    print("─" * 60)

    outcome = crisis_state.outcome

    before = outcome.get("congestion_before", 0)
    after  = outcome.get("congestion_after",  0)
    reduction = before - after

    # Visual bar chart in terminal
    def bar(percent):
        filled = int(percent / 5)
        empty  = 20 - filled
        return f"[{'█' * filled}{'░' * empty}] {percent}%"

    print(f"\n  Congestion BEFORE: {bar(before)}")
    print(f"  Congestion AFTER : {bar(after)}")
    print(f"  Reduction        : ↓ {reduction}% improvement")
    print(f"\n  ⏱️  First Responder ETA : {outcome.get('response_time_minutes', '?')} minutes")
    print(f"  🚑  Units Deployed      : {outcome.get('units_deployed', 0)}")
    print(f"  📢  Alerts Sent         : {outcome.get('alerts_sent', 0)}")
    print(f"  🗺️   Routes Updated      : {outcome.get('routes_updated', 0)}")
    print(f"\n  📝  Summary: {outcome.get('summary', 'N/A')}")


# ── Export Full State as JSON ────────────────────────────────────
def export_state_json():
    """Export full crisis state as JSON for the UI to consume."""
    state_dict = {
        "crisis": crisis_state.detected_crisis,
        "actions": crisis_state.action_plan["actions"],
        "simulation": {
            "routes": crisis_state.simulation["routes"],
            "tickets": crisis_state.simulation["tickets"],
            "alerts": crisis_state.simulation["alerts"]
        },
        "outcome": crisis_state.outcome,
        "logs": crisis_state.logs
    }

    with open("simulation_output.json", "w", encoding="utf-8") as f:
        json.dump(state_dict, f, indent=2, ensure_ascii=False)

    print("\n💾  Simulation exported to simulation_output.json")
    return state_dict


# ── Run Full Simulation Display ──────────────────────────────────
def run_simulation_display():
    print("\n" + "=" * 60)
    print("🎬  CIRO SIMULATION RESULTS")
    print("=" * 60)

    display_routes()
    display_tickets()
    display_alerts()
    display_outcome()
    export_state_json()

    print("\n" + "=" * 60)
    print("✅  Simulation complete.")
    print("=" * 60 + "\n")