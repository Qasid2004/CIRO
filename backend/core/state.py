"""
state.py — Shared Crisis State
This is the single source of truth for the entire CIRO pipeline.
Every agent reads from and writes to this object.
"""

from datetime import datetime


class CrisisState:
    def __init__(self):
        # ── Raw Inputs ──────────────────────────────────────────
        self.raw_signals = {
            "social_posts": [],
            "weather": {},
            "traffic": {},
            "resources": {}
        }

        # ── Agent 1 Output: Collected Signals ───────────────────
        self.collected_signals = {
            "total_signals": 0,
            "social_count": 0,
            "keywords_found": [],
            "locations_mentioned": [],
            "summary": ""
        }

        # ── Agent 2 Output: Detected Crisis ─────────────────────
        self.detected_crisis = {
            "type": None,           # e.g. "Urban Flooding"
            "location": None,       # e.g. "G-10, Islamabad"
            "severity": None,       # "Low" / "Medium" / "High" / "Critical"
            "confidence": None,     # "Low" / "Medium" / "High"
            "explanation": "",
            "affected_routes": [],
            "detected_at": None
        }

        # ── Agent 3 Output: Action Plan ─────────────────────────
        self.action_plan = {
            "actions": [],          # list of action strings
            "resources_to_deploy": [],
            "alternate_routes": [],
            "alert_message": "",
            "priority": None        # "IMMEDIATE" / "HIGH" / "MEDIUM"
        }

        # ── Agent 4 Output: Simulation Results ──────────────────
        self.simulation = {
            "routes": {},           # before/after route status
            "tickets": [],          # emergency tickets created
            "alerts": [],           # alerts sent
            "resources_deployed": []
        }

        # ── Final Outcome ────────────────────────────────────────
        self.outcome = {
            "congestion_before": 0,
            "congestion_after": 0,
            "response_time_minutes": 0,
            "status": "PENDING"     # "PENDING" / "IN_PROGRESS" / "RESOLVED"
        }

        # ── Agent Logs ───────────────────────────────────────────
        self.logs = []

        # ── Pipeline Status ──────────────────────────────────────
        self.pipeline_status = {
            "agent_1_done": False,
            "agent_2_done": False,
            "agent_3_done": False,
            "agent_4_done": False
        }

    # ── Helper: Add a log entry ──────────────────────────────────
    def add_log(self, agent: str, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {agent}: {message}"
        self.logs.append(log_entry)
        print(log_entry)  # also print to terminal in real time

    # ── Helper: Print full state summary ────────────────────────
    def print_summary(self):
        print("\n" + "="*60)
        print("CIRO — CRISIS STATE SUMMARY")
        print("="*60)

        print(f"\n📡 SIGNALS COLLECTED: {self.collected_signals['total_signals']}")
        print(f"   Keywords: {', '.join(self.collected_signals['keywords_found'])}")
        print(f"   Locations: {', '.join(self.collected_signals['locations_mentioned'])}")

        print(f"\n🚨 CRISIS DETECTED:")
        print(f"   Type      : {self.detected_crisis['type']}")
        print(f"   Location  : {self.detected_crisis['location']}")
        print(f"   Severity  : {self.detected_crisis['severity']}")
        print(f"   Confidence: {self.detected_crisis['confidence']}")
        print(f"   Explanation: {self.detected_crisis['explanation']}")

        print(f"\n📋 ACTION PLAN:")
        for i, action in enumerate(self.action_plan['actions'], 1):
            print(f"   {i}. {action}")

        print(f"\n🎬 SIMULATION:")
        print(f"   Tickets Created : {len(self.simulation['tickets'])}")
        print(f"   Alerts Sent     : {len(self.simulation['alerts'])}")
        print(f"   Routes Updated  : {len(self.simulation['routes'])}")

        print(f"\n📊 OUTCOME:")
        print(f"   Congestion Before : {self.outcome['congestion_before']}%")
        print(f"   Congestion After  : {self.outcome['congestion_after']}%")
        print(f"   Response Time     : {self.outcome['response_time_minutes']} minutes")

        print(f"\n📝 AGENT LOGS:")
        for log in self.logs:
            print(f"   {log}")
        print("="*60 + "\n")


# ── Single shared instance used by all agents ────────────────────
crisis_state = CrisisState()