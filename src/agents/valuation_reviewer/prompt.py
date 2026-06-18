"""
src/agents/valuation_reviewer/prompt.py
==========================================
Carga el system prompt del Valuation Reviewer Agent desde:
  plugins/agent-plugins/valuation-reviewer/agents/valuation-reviewer.md
  plugins/agent-plugins/valuation-reviewer/skills/returns-analysis/SKILL.md
  plugins/agent-plugins/valuation-reviewer/skills/ic-memo/SKILL.md
  plugins/agent-plugins/valuation-reviewer/skills/portfolio-monitoring/SKILL.md
"""

from prompt_loader import build_system_prompt


def get_system_prompt(extra: str = "") -> str:
    return build_system_prompt(
        agent_slug="valuation-reviewer",
        skill_names=["returns-analysis", "ic-memo", "portfolio-monitoring"],
        extra_instructions=extra,
    )