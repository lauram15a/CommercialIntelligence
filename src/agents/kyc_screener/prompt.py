"""
src/agents/kyc_screener/prompt.py
===================================
Carga el system prompt del KYC Screener Agent desde:
  plugins/agent-plugins/kyc-screener/agents/kyc-screener.md
  plugins/agent-plugins/kyc-screener/skills/kyc-doc-parse/SKILL.md
  plugins/agent-plugins/kyc-screener/skills/kyc-rules/SKILL.md
"""

from prompt_loader import build_system_prompt


def get_system_prompt(extra: str = "") -> str:
    return build_system_prompt(
        agent_slug="kyc-screener",
        skill_names=["kyc-doc-parse", "kyc-rules"],
        extra_instructions=extra,
    )