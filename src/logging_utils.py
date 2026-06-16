"""
src/logging_utils.py
=====================
Centraliza el logging de toda la app en app.log dentro de cada carpeta
de ejecución.

Esquema de outputs:
    outputs/YYYYMMDDHHMMSS_KYC_NombreEmpresa/
    outputs/YYYYMMDDHHMMSS_DEAL_NombreSector/

Uso:
    from src.logging_utils import setup_run_logging
    run_id, logger, run_dir = setup_run_logging(use_case="kyc", entity="Empresa Ejemplo SL")
"""

import logging
import re
from datetime import datetime
from pathlib import Path

OUTPUTS_DIR = Path(__file__).resolve().parent.parent / "outputs"


def _safe_name(name: str) -> str:
    """Convierte un nombre a formato seguro para carpeta (sin espacios ni caracteres raros)."""
    name = name.strip()
    # Reemplaza espacios y caracteres no alfanumericos por guion bajo
    name = re.sub(r"[^\w\-]", "_", name, flags=re.UNICODE)
    name = re.sub(r"_+", "_", name)
    return name[:60] or "sin_nombre"


def setup_run_logging(
    run_id: str | None = None,
    use_case: str = "kyc",
    entity: str = "sin_nombre",
) -> tuple[str, logging.Logger, Path]:
    """
    Crea outputs/YYYYMMDDHHMMSS_KYC_empresa/ o outputs/YYYYMMDDHHMMSS_DEAL_sector/
    y configura el logger raíz para que escriba en app.log además de en consola.

    Devuelve (run_id, logger, run_dir).
    """
    if run_id is None:
        run_id = datetime.now().strftime("%Y%m%d%H%M%S")

    entity_safe = _safe_name(entity)
    folder_name = f"{run_id}_{use_case.upper()}_{entity_safe}"
    run_dir = OUTPUTS_DIR / folder_name
    run_dir.mkdir(parents=True, exist_ok=True)

    logger_name = f"{use_case}_intelligence"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    fh = logging.FileHandler(run_dir / "app.log", encoding="utf-8")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.propagate = False
    return run_id, logger, run_dir


def get_logger(use_case: str = "kyc") -> logging.Logger:
    """Devuelve el logger ya configurado por setup_run_logging."""
    return logging.getLogger(f"{use_case}_intelligence")