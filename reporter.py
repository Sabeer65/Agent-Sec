import os
import json
from datetime import datetime

def generate_report(final_state: dict) -> None:
    """
    Save the graph's final state as both a raw JSON log and a readable
    Markdown summary, timestamped so repeated runs don't overwrite each other.
    """
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    json_path = f"reports/report_{timestamp}.json"
    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(final_state, f, indent=2)

    md_path = f"reports/report_{timestamp}.md"
    with open(md_path, "w", encoding='utf-8') as f:
        f.write(build_markdown_report(final_state))

    print(f"\nReport saved: {json_path}")
    print(f"Report saved: {md_path}")


def build_markdown_report(final_state: dict) -> str:
    """Build a human-readable Markdown summary from the graph's final state."""
    lines = [
        "# Agent-Sec Security Report",
        f"**Generated:** {datetime.now().isoformat()}",
        "",
        "## Final Verdict",
        f"- **Vulnerable:** {final_state['is_vulnerable']}",
        f"- **Confidence:** {final_state['confidence_score']}",
        f"- **Vulnerability Type:** {final_state['vulnerability_type']}",
        f"- **Iterations Used:** {final_state['iteration']} / {final_state['max_iterations']}",
        "",
        "## Final System Prompt",
        "```",
        final_state["system_prompt"],
        "```",
        "",
        "## Attempt History",
    ]
    for i, attempt in enumerate(final_state["attempt_history"], start=1):
        status = "SUCCEEDED" if attempt["is_vulnerable"] else "BLOCKED"
        lines.append(f"### Attempt {i} — {status}")
        lines.append(f"- **Payload:** {attempt['attack_payload']}")
        lines.append(f"- **Type:** {attempt['vulnerability_type']}")
        lines.append("")

    return "\n".join(lines)