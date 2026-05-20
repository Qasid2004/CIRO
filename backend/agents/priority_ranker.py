"""
priority_ranker.py — Crisis Priority Ranker
Takes multiple social media inputs, ranks them by criticality,
and returns the most critical one first for processing.
"""

from core.llm_client import call_llm


def rank_by_priority(inputs: list) -> list:
    """
    Takes a list of crisis reports and ranks them
    from most critical to least critical.
    Returns sorted list with priority scores.
    """

    if not inputs:
        return []

    if len(inputs) == 1:
        return [{"input": inputs[0], "priority": 1, "severity": "Unknown", "reason": "Only input"}]

    # Build prompt
    inputs_text = "\n".join([f"{i+1}. {inp}" for i, inp in enumerate(inputs)])

    prompt = f"""
You are a crisis prioritization system for Pakistani cities.
Rank the following crisis reports from MOST CRITICAL to LEAST CRITICAL.

Crisis Reports:
{inputs_text}

Ranking criteria (in order of importance):
- Life threatening situations (highest priority)
- Infrastructure failures blocking emergency services
- Large scale flooding or disasters
- Traffic accidents with injuries
- Road blockages without injuries
- Minor incidents (lowest priority)

Respond in this EXACT format for each report (one per line):
RANK|ORIGINAL_NUMBER|SEVERITY|REASON
Example:
1|3|Critical|Flash flood blocking emergency vehicles
2|1|High|Road accident with possible injuries
3|2|Medium|Minor traffic congestion

Respond with ONLY the ranked lines, nothing else.
"""

    response = call_llm(prompt)

    if response.startswith("ERROR"):
        # Fallback — return as is without ranking
        return [{"input": inp, "priority": i+1, "severity": "Unknown", "reason": "Ranking unavailable"} 
                for i, inp in enumerate(inputs)]

    # Parse response
    ranked = []
    for line in response.strip().splitlines():
        line = line.strip()
        if not line or "|" not in line:
            continue
        parts = line.split("|")
        if len(parts) >= 4:
            try:
                rank          = int(parts[0].strip())
                original_num  = int(parts[1].strip()) - 1  # convert to 0-index
                severity      = parts[2].strip()
                reason        = parts[3].strip()

                if 0 <= original_num < len(inputs):
                    ranked.append({
                        "input"   : inputs[original_num],
                        "priority": rank,
                        "severity": severity,
                        "reason"  : reason
                    })
            except:
                continue

    # If parsing failed fallback
    if not ranked:
        return [{"input": inp, "priority": i+1, "severity": "Unknown", "reason": "Ranking unavailable"}
                for i, inp in enumerate(inputs)]

    # Sort by priority
    ranked.sort(key=lambda x: x["priority"])
    return ranked


def display_priority_ranking(ranked: list):
    """Display the priority ranking in terminal."""
    print("\n" + "="*60)
    print("🚨 CRISIS PRIORITY RANKING")
    print("="*60)

    for item in ranked:
        emoji = "🔴" if item["severity"] == "Critical" else \
                "🟠" if item["severity"] == "High" else \
                "🟡" if item["severity"] == "Medium" else "🟢"

        print(f"\n  Priority #{item['priority']} {emoji}")
        print(f"  Severity : {item['severity']}")
        print(f"  Input    : {item['input']}")
        print(f"  Reason   : {item['reason']}")

    print("\n" + "="*60)
    print(f"▶ Processing most critical first: {ranked[0]['input']}")
    print("="*60 + "\n")