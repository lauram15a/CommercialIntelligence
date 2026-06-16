"""
config.py
==========
Configuracion "white-label" del frontend. Lee primero las variables de entorno
BANK_*, y como fallback carga config_clienteA.json (perfil activo por defecto).

Para cambiar de cliente: define BANK_CONFIG_FILE apuntando a otro JSON.
"""

import json
import os
from pathlib import Path

_BASE_DIR   = Path(__file__).resolve().parent
CONFIG_FILE = os.environ.get("BANK_CONFIG_FILE", str(_BASE_DIR / "config_clienteA.json"))

def _load_client_config() -> dict:
    path = Path(CONFIG_FILE)
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}

_cfg = _load_client_config()
_ui  = _cfg.get("ui", {})


class BankConfig:
    BANK_NAME          = os.environ.get("BANK_NAME",          _cfg.get("BANK_NAME",          "Bankinter"))
    BANK_LEGAL_NAME    = os.environ.get("BANK_LEGAL_NAME",    _cfg.get("BANK_LEGAL_NAME",    "Bankinter, S.A."))
    PLATFORM_NAME      = os.environ.get("PLATFORM_NAME",      _cfg.get("PLATFORM_NAME",      "Plataforma de Agentes IA"))
    PRODUCT_NAME       = os.environ.get("PRODUCT_NAME",       _cfg.get("PRODUCT_NAME",       "KYC & Credit Risk Intelligence"))
    PRODUCT_SHORT_NAME = os.environ.get("PRODUCT_SHORT_NAME", _cfg.get("PRODUCT_SHORT_NAME", "Risk Intelligence"))
    LOGO_FILENAME      = os.environ.get("BANK_LOGO_FILENAME", _cfg.get("LOGO_FILENAME",      ""))

    COLOR_PRIMARY       = os.environ.get("BANK_COLOR_PRIMARY",       _ui.get("COLOR_PRIMARY",       "#FF8D30"))
    COLOR_PRIMARY_DARK  = os.environ.get("BANK_COLOR_PRIMARY_DARK",  _ui.get("COLOR_PRIMARY_DARK",  "#C05600"))
    COLOR_PRIMARY_SOFT  = os.environ.get("BANK_COLOR_PRIMARY_SOFT",  _ui.get("COLOR_PRIMARY_SOFT",  "#FFF3E8"))
    COLOR_ACCENT        = os.environ.get("BANK_COLOR_ACCENT",        _ui.get("COLOR_ACCENT",        "#FED227"))
    COLOR_ACCENT_SOFT   = os.environ.get("BANK_COLOR_ACCENT_SOFT",   _ui.get("COLOR_ACCENT_SOFT",   "#FFFAE0"))
    COLOR_WARN          = os.environ.get("BANK_COLOR_WARN",          _ui.get("COLOR_WARN",          "#AF6200"))
    COLOR_WARN_SOFT     = os.environ.get("BANK_COLOR_WARN_SOFT",     _ui.get("COLOR_WARN_SOFT",     "#FFF0D6"))
    COLOR_DANGER        = os.environ.get("BANK_COLOR_DANGER",        _ui.get("COLOR_DANGER",        "#C05600"))
    COLOR_DANGER_SOFT   = os.environ.get("BANK_COLOR_DANGER_SOFT",   _ui.get("COLOR_DANGER_SOFT",   "#FFE8D6"))
    COLOR_OK            = os.environ.get("BANK_COLOR_OK",            _ui.get("COLOR_OK",            "#687B54"))
    COLOR_OK_SOFT       = os.environ.get("BANK_COLOR_OK_SOFT",       _ui.get("COLOR_OK_SOFT",       "#EFF3EA"))
    COLOR_BG            = os.environ.get("BANK_COLOR_BG",            _ui.get("COLOR_BG",            "#F9F9F9"))
    COLOR_SURFACE       = os.environ.get("BANK_COLOR_SURFACE",       _ui.get("COLOR_SURFACE",       "#FFFFFF"))
    COLOR_INK           = os.environ.get("BANK_COLOR_INK",           _ui.get("COLOR_INK",           "#212425"))
    COLOR_INK_MUTED     = os.environ.get("BANK_COLOR_INK_MUTED",     _ui.get("COLOR_INK_MUTED",     "#6B7280"))
    COLOR_BORDER        = os.environ.get("BANK_COLOR_BORDER",        _ui.get("COLOR_BORDER",        "#E5E7EB"))

    FOOTER_TEXT     = os.environ.get("BANK_FOOTER_TEXT",     _ui.get("FOOTER_TEXT",
        "Herramienta de apoyo al analista. Las recomendaciones generadas no "
        "constituyen una decision de aprobacion o denegacion de la operacion. "
        "La decision final corresponde al analista y al comite de riesgos."))
    DEPARTMENT_NAME_KYC  = os.environ.get("BANK_DEPARTMENT_NAME_KYC",  _ui.get("DEPARTMENT_NAME_KYC",  "Dirección de Riesgos - Onboarding KYC"))
    DEPARTMENT_NAME_DEAL = os.environ.get("BANK_DEPARTMENT_NAME_DEAL", _ui.get("DEPARTMENT_NAME_DEAL", "Banca Corporativa - Deal Intelligence"))

    @classmethod
    def logo_initials(cls) -> str:
        words = cls.BANK_NAME.split()
        if len(words) == 1:
            return words[0][:2].upper()
        return (words[0][0] + words[1][0]).upper()

    @classmethod
    def to_template_context(cls) -> dict:
        return {
            "bank_name":               cls.BANK_NAME,
            "bank_legal_name":         cls.BANK_LEGAL_NAME,
            "platform_name":           cls.PLATFORM_NAME,
            "product_name":            cls.PRODUCT_NAME,
            "product_short_name":      cls.PRODUCT_SHORT_NAME,
            "logo_filename":           cls.LOGO_FILENAME,
            "logo_initials":           cls.logo_initials(),
            "footer_text":             cls.FOOTER_TEXT,
            "department_name":         cls.DEPARTMENT_NAME_KYC,
            "department_name_kyc":     cls.DEPARTMENT_NAME_KYC,
            "department_name_deal":    cls.DEPARTMENT_NAME_DEAL,
            "colors": {
                "primary":       cls.COLOR_PRIMARY,
                "primary_dark":  cls.COLOR_PRIMARY_DARK,
                "primary_soft":  cls.COLOR_PRIMARY_SOFT,
                "accent":        cls.COLOR_ACCENT,
                "accent_soft":   cls.COLOR_ACCENT_SOFT,
                "warn":          cls.COLOR_WARN,
                "warn_soft":     cls.COLOR_WARN_SOFT,
                "danger":        cls.COLOR_DANGER,
                "danger_soft":   cls.COLOR_DANGER_SOFT,
                "ok":            cls.COLOR_OK,
                "ok_soft":       cls.COLOR_OK_SOFT,
                "bg":            cls.COLOR_BG,
                "surface":       cls.COLOR_SURFACE,
                "ink":           cls.COLOR_INK,
                "ink_muted":     cls.COLOR_INK_MUTED,
                "border":        cls.COLOR_BORDER,
            },
        }