"""
main.py — CIRO Pipeline
Multiple crisis inputs — ranks by criticality first.
"""

import importlib
from agents.priority_ranker import rank_by_priority, display_priority_ranking


def print_banner():
    print("""
╔══════════════════════════════════════════════════════════╗
║     CIRO — Crisis Intelligence & Response Orchestrator   ║
║     Islamabad Emergency Response System                  ║
╚══════════════════════════════════════════════════════════╝
    """)


def run_pipeline(user_input: str = ""):
    # Reset state
    import core.state as state_module
    from core.state import CrisisState
    state_module.crisis_state = CrisisState()

    importlib.reload(importlib.import_module("agents.signal_collector"))
    importlib.reload(importlib.import_module("agents.crisis_detector"))
    importlib.reload(importlib.import_module("agents.action_planner"))
    importlib.reload(importlib.import_module("agents.executor"))
    importlib.reload(importlib.import_module("simulation.simulator"))

    from agents.signal_collector import run_signal_collector
    from agents.crisis_detector import run_crisis_detector
    from agents.action_planner import run_action_planner
    from agents.executor import run_executor
    from simulation.simulator import run_simulation_display

    print("─" * 60)
    print(f"📨 Processing: {user_input}")
    print("─" * 60)

    print("\n🔵 AGENT 1 — Signal Collector")
    run_signal_collector(user_input)

    print("\n🟡 AGENT 2 — Crisis Detector")
    run_crisis_detector()

    print("\n🟠 AGENT 3 — Action Planner")
    run_action_planner()

    print("\n🔴 AGENT 4 — Executor")
    run_executor()

    print("\n✅ Pipeline complete!\n")

    from core.state import crisis_state
    crisis_state.print_summary()
    run_simulation_display()


def run_multi_pipeline(user_inputs: list):
    print_banner()

    if len(user_inputs) == 1:
        run_pipeline(user_inputs[0])
        return

    print("📊 Ranking crisis reports by criticality...\n")
    ranked = rank_by_priority(user_inputs)
    display_priority_ranking(ranked)

    for i, item in enumerate(ranked):
        print(f"\n{'='*60}")
        print(f"🔥 CRISIS {i+1} of {len(ranked)} — Priority #{item['priority']} | {item['severity']}")
        print(f"{'='*60}")
        run_pipeline(item["input"])


if __name__ == "__main__":
    crisis_reports = [
        "G-10 mein pani bhar gaya hai, gaariyan phans gayi hain!",
        "F-7 mein bohot tez garmi hai, 3 log heat stroke se hospital gaye",
        "I-8 mein bijli ka khamba gir gaya hai, live wires hain road pe"
    ]
    run_multi_pipeline(crisis_reports)