# Informe de riesgo - Acme Componentes SL

## Resumen ejecutivo
Acme Componentes SL (NIF B50123987) presenta documentación societaria y estados financieros 2022–2024 completos, con consistencia de nombre legal entre documentos (según KYC Screener Agent). En KYC, el principal gap es la ausencia de documento de identidad (DNI) en el paquete, lo que impide cerrar la verificación de personas físicas (KYC-001: FAIL). Financiera y operativamente, el desempeño mejora: EBITDA 3,8M→5,8M y ventas 32,0M→42,0M (2022–2024), con apalancamiento estable ~2,1x y coberturas de intereses >8x (según Valuation Reviewer Agent). El screening no arroja hits, pero el propio agente indica que el “fichero de sanciones no encontrado”, por lo que el resultado no es concluyente y requiere re-screening con fuentes actualizadas. No se identifican señales externas negativas en búsquedas abiertas (según Market Researcher Agent).

## Validación KYC
- **KYC-001 – Documento de identidad presente: FAIL**. Evidencia: “no se encontró ningún documento tipo ‘dni’” (KYC Screener Agent).  
  - **Implicación:** no se puede completar la identificación/verificación de administradores y/o titular real persona física (p. ej., Roberto Acme Jiménez); requiere subsanación antes de cierre KYC.
- **KYC-003 – Consistencia de nombre legal entre documentos: PASS**. Evidencia: nombres encontrados `['Acme Componentes SL']` (KYC Screener Agent).
- **KYC-004 – Titular real identificado: PASS**. Evidencia: “titulares reales presentes” (KYC Screener Agent; escritura 2003-07-10 identifica Roberto Acme Jiménez y Acme Europe Holding GmbH).
- **KYC-005 – Información financiera presente: PASS**. Evidencia: “balance/PyG encontrado” (KYC Screener Agent; balances 2022–2024).

## Análisis financiero
- **Modelo financiero normalizado:** 3 periodos disponibles (2022, 2023, 2024) con EBITDA, deuda financiera, activo/pasivo corriente, patrimonio neto, ingresos y gastos financieros completos; **sin audit_flags** (según Model Builder Agent).
- **Ratios clave y evolución (según Valuation Reviewer Agent):**
  - **Debt/EBITDA:** 2,11x (2022) → 2,14x (2023) → 2,07x (2024). Apalancamiento estable con ligera mejora en 2024.
  - **Liquidez corriente (Activo corriente/Pasivo corriente):** 1,32 → 1,36 → 1,48. Tendencia positiva; holgura creciente en corto plazo.
  - **Cobertura de intereses (EBITDA/Gastos financieros):** 8,44x → 9,42x → 9,51x. Capacidad cómoda de servicio de deuda.
- **Interpretación integrada:** el crecimiento de deuda (8,0M→12,0M) queda compensado por el aumento de EBITDA (3,8M→5,8M), sosteniendo el apalancamiento y mejorando métricas de liquidez y cobertura. Se reporta historial con el banco con 5 operaciones desde 2022 sin impagos y con incidencias operativas menores ya subsanadas (según Valuation Reviewer Agent); se sugiere mantener seguimiento documental, más que una señal de estrés financiero.

## Screening (sanciones / PEP / adverse media)
Resultados (según KYC Screener Agent; **nota: “fichero de sanciones no encontrado” en todos los casos, por lo que el screening no es concluyente**):
- **Acme Componentes SL:** sin hits; confianza limitada por falta de fichero/fuente.
- **Acme Europe Holding GmbH:** sin hits; confianza limitada por falta de fichero/fuente.
- **Klaus Meier:** sin hits; confianza limitada por falta de fichero/fuente.
- **Roberto Acme Jiménez:** sin hits; confianza limitada por falta de fichero/fuente.  
**Requiere revisión manual / re-screening** con listas de sanciones/PEP/adverse media actualizadas y trazables (proveedor y fecha de consulta).

## Señales externas
Según Market Researcher Agent, **no se encontraron señales externas relevantes** (noticias negativas, litigios, sanciones regulatorias, concurso) para Acme Componentes SL ni para Acme Europe Holding GmbH, Klaus Meier o Roberto Acme Jiménez en las búsquedas realizadas. Se indica explícitamente que esto puede reflejar limitación de información recuperable, no ausencia de riesgo.

## Recomendaciones
- **Subsanar KYC-001 (prioritario):** solicitar y validar **DNI/NIE/pasaporte** vigente de Roberto Acme Jiménez (y de cualquier administrador/persona física relevante), y dejar evidencia de verificación.
- **Re-screening completo:** repetir screening de **sanciones/PEP/adverse media** para entidad, titular real corporativo y personas físicas, con **fuente/proveedor, fecha/hora y listas** documentadas (dado el “fichero de sanciones no encontrado” reportado).
- **Clarificar estructura de titularidad:** aportar documentación de **Acme Europe Holding GmbH** (registro mercantil, UBOs, organigrama) para trazabilidad de beneficiario final último, si aplica.
- **Seguimiento financiero:** mantener covenants/monitorización interna sobre **Debt/EBITDA (~2,1x)** y **cobertura de intereses (>8x)**, y solicitar estados 2025 cuando estén disponibles para confirmar tendencia.
- **Control documental:** reforzar checklist de entregables (por las incidencias documentales históricas menores reportadas por Valuation Reviewer Agent) y fijar plazos de entrega de cuentas/auditoría si aplica.  

Estas recomendaciones son propuestas; la decisión final corresponde al analista y al comité de riesgos.