"""
src/agents/model_builder/prompt.py
=====================================
Carga el system prompt del Model Builder Agent desde:
  plugins/agent-plugins/model-builder/agents/model-builder.md
  plugins/agent-plugins/model-builder/skills/3-statement-model/SKILL.md
  plugins/agent-plugins/model-builder/skills/audit-xls/SKILL.md
  plugins/agent-plugins/model-builder/skills/comps-analysis/SKILL.md
"""

from prompt_loader import build_system_prompt


def get_system_prompt(extra: str = "") -> str:
    return build_system_prompt(
        agent_slug="model-builder",
        skill_names=["3-statement-model", "audit-xls", "comps-analysis"],
        extra_instructions=extra,
    )