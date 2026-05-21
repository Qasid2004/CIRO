---

## What CIRO Does

CIRO ingests signals from multiple sources (social media, weather, traffic), detects emerging crises, generates coordinated response plans, and simulates execution — all without human intervention after the initial input.

**Example:** User types *"G-10 mein pani bhar gaya hai"* → CIRO detects Urban Flooding → deploys rescue teams, pump trucks, police → sends alerts in Urdu and English → reduces congestion from 53% to 17%.

---

## System Architecture

```
Input Layer
├── Social media posts (Roman Urdu / Urdu / English)
├── Weather API (mock - PMD alerts)
├── Traffic API (mock - route congestion data)
└── Emergency resources (mock - available units)

Agent Pipeline
├── Agent 0: Priority Ranker   → ranks multiple crises by severity
├── Agent 1: Signal Collector  → normalizes and summarizes all signals
├── Agent 2: Crisis Detector   → identifies crisis type, location, severity
├── Agent 3: Action Planner    → generates coordinated response plan
└── Agent 4: Executor          → simulates tickets, alerts, route updates

Shared State (state.py)
└── Single source of truth passed between all agents

Output Layer
├── Emergency tickets (EMG-XXXX)
├── Public alerts (SMS, WhatsApp, Traffic App)
├── Route updates (before/after)
├── Outcome metrics (congestion reduction %)
└── simulation_output.json (consumed by UI)
```

---

## How Google Antigravity (ADK) Is Used

CIRO uses **Google Agent Development Kit (ADK)** — the programmatic interface to Google Antigravity — for multi-agent orchestration.

### File: `antigravity.py`

```python
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
```

The 4 CIRO agents are registered as **ADK tools**:

```python
ciro_agent = Agent(
    name="CIRO_Orchestrator",
    model="gemini-2.0-flash",
    tools=[
        collect_signals,    # Agent 1
        detect_crisis,      # Agent 2
        plan_actions,       # Agent 3
        execute_response    # Agent 4
    ]
)
```

**How it works:**
- User provides crisis input
- Gemini reads the input and **decides** which tool to call
- ADK **executes** that tool call
- Gemini reads the result and decides the next tool
- This continues until all 4 agents have run
- ADK returns a final summarized response

This satisfies the requirement: Anitgravity must be used to: orchestrate multi-agents workflows, plan and execute decisions, integrate tools, simulate coordinated actions.

---

## Agentic Features

### 1. Autonomous Priority Ranking
Multiple crisis reports are automatically ranked by severity before processing:
```
Input:  3 crisis reports
Output: Electricity pole (Critical) → Heatwave (Critical) → Flood (High)
```
No human intervention — AI decides the order.

### 2. Multi-Source Signal Fusion
Agent 1 combines social posts + weather + traffic into one coherent summary.

### 3. Intelligent Crisis Detection
Agent 2 explains its reasoning:
> *"G-10 Main Boulevard blocked by 2ft water + HEAVY_RAINFALL alert + ambulance cannot pass = Urban Flooding, Critical, High Confidence"*

### 4. Context-Aware Action Planning
Agent 3 picks the right resources for each crisis type:
- Flood → Pump trucks + Rescue teams
- Heatwave → Medical teams + Cooling units
- Electricity → IESCO teams + Police cordon

### 5. Automatic API Key Failover
When one Gemini API key hits quota, system automatically switches to backup key without interruption.

---

## Tools & APIs Used

| Tool | Purpose |
|---|---|
| Google Gemini 2.5 Flash | LLM for all agent reasoning |
| Google ADK (Antigravity) | Multi-agent orchestration |
| google-genai SDK | Gemini API calls |
| Python 3.14 | Backend runtime |
| Mock JSON APIs | Weather, traffic, resources data |

---

## Project Structure

```
CIRO/
├── agents/
│   ├── signal_collector.py   # Agent 1 — signal normalization
│   ├── crisis_detector.py    # Agent 2 — crisis identification
│   ├── action_planner.py     # Agent 3 — response planning
│   ├── executor.py           # Agent 4 — simulation execution
│   └── priority_ranker.py   # Agent 0 — crisis prioritization
├── core/
│   ├── llm_client.py         # Gemini API wrapper (auto key switching)
│   └── state.py              # Shared crisis state
├── data/
│   ├── mock_social.json      # Simulated social media posts
│   ├── mock_weather.json     # Simulated PMD weather alerts
│   ├── mock_traffic.json     # Simulated traffic data
│   └── mock_resources.json   # Available emergency units
├── simulation/
│   └── simulator.py          # Simulation display + JSON export
├── antigravity.py            # Google ADK orchestration
├── main.py                   # Direct pipeline runner
└── simulation_output.json   # Output consumed by UI
```

---

## How to Run

### Install dependencies
```bash
pip install google-genai google-adk
```

### Add API Key
Open `core/llm_client.py` and add your Gemini API key:
```python
API_KEYS = ["YOUR_GEMINI_API_KEY"]
```

### Run the pipeline
```bash
python main.py
```

### Run with Antigravity orchestration
```bash
python antigravity.py
```

---

## Input Format

Edit the `crisis_reports` list in `main.py`:

```python
crisis_reports = [
    "G-10 mein pani bhar gaya hai, gaariyan phans gayi hain!",
    "F-7 mein bohot tez garmi hai, 3 log heat stroke se hospital gaye",
    "I-8 mein bijli ka khamba gir gaya hai, live wires hain road pe"
]
```

Supports English, Roman Urdu, and mixed language input.

---

## Output

Each run produces:
- Terminal logs showing agent reasoning in real time
- `simulation_output.json` — full structured output for UI

```json
{
  "crisis": { "type": "Urban Flooding", "severity": "Critical", "confidence": "High" },
  "actions": ["Deploy RES-02...", "Dispatch PUMP-01..."],
  "simulation": { "tickets": [...], "alerts": [...], "routes": {...} },
  "outcome": { "congestion_before": 53, "congestion_after": 17 },
  "logs": ["Agent 1: Collected 11 signals...", "Agent 2: Crisis identified..."]
}
```

---

## Assumptions

- Weather, traffic, and resource data are simulated via mock JSON files
- Real PMD, traffic, and dispatch APIs would replace mock data in production
- Gemini free tier used with automatic key rotation for quota management
- Emergency unit locations and ETAs are approximate simulations

---

## Team

Built for Google Antigravity Hackathon — Challenge 3: Crisis Intelligence & Response Orchestrator