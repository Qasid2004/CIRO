"""
antigravity.py — Google ADK Orchestrator
Uses Google Agent Development Kit (ADK) to orchestrate
all CIRO agents as a proper multi-agent pipeline.
This satisfies the mandatory Antigravity requirement.
"""

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from core.state import crisis_state
from agents.signal_collector import run_signal_collector
from agents.crisis_detector import run_crisis_detector
from agents.action_planner import run_action_planner
from agents.executor import run_executor
from simulation.simulator import run_simulation_display

import os

# ── API Key ──────────────────────────────────────────────────────
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"  # Replace with your key
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

# ── Define Agent Tools ───────────────────────────────────────────
# Each function below is a "tool" that ADK can call

def collect_signals(user_input: str) -> str:
    """Agent 1: Collects and normalizes signals from all sources."""
    run_signal_collector(user_input)
    signals = crisis_state.collected_signals
    return (
        f"Signals collected: {signals['total_signals']} total. "
        f"Keywords: {', '.join(signals['keywords_found'])}. "
        f"Locations: {', '.join(signals['locations_mentioned'])}. "
        f"Summary: {signals['summary']}"
    )


def detect_crisis() -> str:
    """Agent 2: Detects crisis type, location, severity and confidence."""
    run_crisis_detector()
    crisis = crisis_state.detected_crisis
    return (
        f"Crisis detected: {crisis['type']} at {crisis['location']}. "
        f"Severity: {crisis['severity']}. "
        f"Confidence: {crisis['confidence']}. "
        f"Explanation: {crisis['explanation']}"
    )


def plan_actions() -> str:
    """Agent 3: Plans coordinated response actions."""
    run_action_planner()
    plan = crisis_state.action_plan
    actions_str = " | ".join(plan['actions'])
    return (
        f"Action plan created. Priority: {plan['priority']}. "
        f"Actions: {actions_str}. "
        f"Alternate routes: {', '.join(plan['alternate_routes'])}"
    )


def execute_response() -> str:
    """Agent 4: Simulates execution of all response actions."""
    run_executor()
    outcome = crisis_state.outcome
    sim     = crisis_state.simulation
    return (
        f"Execution complete. "
        f"Tickets created: {len(sim['tickets'])}. "
        f"Alerts sent: {len(sim['alerts'])}. "
        f"Congestion reduced from {outcome['congestion_before']}% "
        f"to {outcome['congestion_after']}%. "
        f"Response time: {outcome['response_time_minutes']} minutes."
    )


# ── Build the ADK Agent ──────────────────────────────────────────
ciro_agent = Agent(
    name="CIRO_Orchestrator",
    model="gemini-2.0-flash",
    description=(
        "CIRO — Crisis Intelligence and Response Orchestrator. "
        "A multi-agent system that detects urban crises in Pakistani cities "
        "and coordinates emergency response actions."
    ),
    instruction=(
        "You are CIRO, an emergency response orchestration system for Pakistani cities. "
        "When given a crisis report or signal, you must:\n"
        "1. Call collect_signals to gather and analyze all input signals\n"
        "2. Call detect_crisis to identify the crisis type, location and severity\n"
        "3. Call plan_actions to generate a coordinated response plan\n"
        "4. Call execute_response to simulate execution of all actions\n"
        "5. Summarize the complete response in a clear, professional manner\n"
        "Always follow this exact sequence. Never skip a step."
    ),
    tools=[
        collect_signals,
        detect_crisis,
        plan_actions,
        execute_response
    ]
)

# ── Run the ADK Pipeline ─────────────────────────────────────────
def run_antigravity(user_input: str = ""):
    print("""
╔══════════════════════════════════════════════════════════╗
║     CIRO — Powered by Google ADK (Antigravity)           ║
║     Crisis Intelligence & Response Orchestrator          ║
╚══════════════════════════════════════════════════════════╝
    """)

    # Set up ADK session
    session_service = InMemorySessionService()
    session = session_service.create_session(
        app_name="CIRO",
        user_id="operator_01"
    )

    runner = Runner(
        agent=ciro_agent,
        app_name="CIRO",
        session_service=session_service
    )

    # Prepare the input message
    if not user_input:
        user_input = "G-10 mein pani bhar gaya hai, gaariyan phans gayi hain!"

    message = types.Content(
        role="user",
        parts=[types.Part(text=user_input)]
    )

    print(f"📨 Input: {user_input}\n")
    print("🤖 ADK Orchestrator running...\n")
    print("─" * 60)

    # Run the agent
    for event in runner.run(
        user_id="operator_01",
        session_id=session.id,
        new_message=message
    ):
        if event.is_final_response():
            final = event.content.parts[0].text
            print("\n🎯 CIRO Final Response:")
            print("─" * 60)
            print(final)

    # Show full simulation display
    print("\n🎥 Running Simulation Display...")
    run_simulation_display()


# ── Entry Point ──────────────────────────────────────────────────
if __name__ == "__main__":
    user_report = "G-10 mein pani bhar gaya hai, gaariyan phans gayi hain!"
    run_antigravity(user_input=user_report)