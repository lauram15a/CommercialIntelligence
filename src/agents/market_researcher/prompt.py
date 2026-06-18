"""
src/agents/market_researcher/prompt.py
=========================================
Carga el system prompt del Market Researcher Agent desde:
  plugins/agent-plugins/market-researcher/agents/market-researcher.md
  plugins/agent-plugins/market-researcher/skills/competitive-analysis/SKILL.md
  plugins/agent-plugins/market-researcher/skills/sector-overview/SKILL.md
"""

from prompt_loader import build_system_prompt


def get_system_prompt(extra: str = "") -> str:
    return build_system_prompt(
        agent_slug="market-researcher",
        skill_names=["competitive-analysis", "sector-overview"],
        extra_instructions=extra,
    )