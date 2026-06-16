"""
core/skill_loader.py
=====================
Carga el contenido de los SKILL.md / agents/*.md del repo anthropics/financial-services
e inyecta su texto como instrucciones de sistema para GPT-5.

Mapeo agente -> skills:

    KYC Screener Agent       -> kyc-doc-parse, kyc-rules
    Model Builder Agent      -> clean-data-xls, 3-statement-model, audit-xls
    Valuation Reviewer Agent -> portfolio-monitoring
    Market Researcher Agent  -> sector-overview
    Credit Risk Report Agent -> (usa el system prompt de kyc-screener.md como base)
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

SKILLS_REPO_ROOT = Path(os.environ.get("SKILLS_REPO_ROOT", "."))

AGENT_PROMPTS = {
    "kyc-screener": SKILLS_REPO_ROOT
    / "plugins/agent-plugins/kyc-screener/agents/kyc-screener.md",
    "model-builder": SKILLS_REPO_ROOT
    / "plugins/agent-plugins/model-builder/agents/model-builder.md",
    "valuation-reviewer": SKILLS_REPO_ROOT
    / "plugins/agent-plugins/valuation-reviewer/agents/valuation-reviewer.md",
    "market-researcher": SKILLS_REPO_ROOT
    / "plugins/agent-plugins/market-researcher/agents/market-researcher.md",
}

SKILL_PATHS = {
    # --- KYC Screener Agent ---
    "kyc-doc-parse": SKILLS_REPO_ROOT
    / "plugins/agent-plugins/kyc-screener/skills/kyc-doc-parse/SKILL.md",
    "kyc-rules": SKILLS_REPO_ROOT
    / "plugins/agent-plugins/kyc-screener/skills/kyc-rules/SKILL.md",

    # --- Model Builder Agent ---
    "clean-data-xls": SKILLS_REPO_ROOT
    / "plugins/vertical-plugins/financial-analysis/skills/clean-data-xls/SKILL.md",
    "3-statement-model": SKILLS_REPO_ROOT
    / "plugins/agent-plugins/model-builder/skills/3-statement-model/SKILL.md",
    "audit-xls": SKILLS_REPO_ROOT
    / "plugins/agent-plugins/model-builder/skills/audit-xls/SKILL.md",

    # --- Valuation Reviewer Agent ---
    "portfolio-monitoring": SKILLS_REPO_ROOT
    / "plugins/agent-plugins/valuation-reviewer/skills/portfolio-monitoring/SKILL.md",

    # --- Market Researcher Agent ---
    "sector-overview": SKILLS_REPO_ROOT
    / "plugins/agent-plugins/market-researcher/skills/sector-overview/SKILL.md",
}


def _read(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(
            f"No se encuentra {path}. Revisa SKILLS_REPO_ROOT en .env "
            f"y que esa skill/agente exista en tu copia del repo."
        )
    return path.read_text(encoding="utf-8")


def load_skill(name: str) -> str:
    """Devuelve el contenido markdown de una skill por su nombre clave."""
    if name not in SKILL_PATHS:
        raise KeyError(f"Skill desconocida: {name}. Disponibles: {list(SKILL_PATHS)}")
    return _read(SKILL_PATHS[name])


def load_agent_prompt(agent_key: str) -> str:
    """Devuelve el system prompt original de un agente (agents/<agent>.md)."""
    if agent_key not in AGENT_PROMPTS:
        raise KeyError(f"Agente desconocido: {agent_key}. Disponibles: {list(AGENT_PROMPTS)}")
    return _read(AGENT_PROMPTS[agent_key])


def build_system_prompt(base_prompt: str, skill_names: list[str]) -> str:
    """
    Concatena un prompt base con el contenido de una o varias skills.
    Equivalente "manual" a lo que Claude Code hace automáticamente.
    """
    parts = [base_prompt.strip(), "\n\n---\n# Skills aplicables\n"]
    for name in skill_names:
        parts.append(f"\n## SKILL: {name}\n")
        parts.append(load_skill(name).strip())
    return "\n".join(parts)