# Informe de riesgo - Grupo Caldas Infraestructuras SA

## Resumen ejecutivo
Grupo Caldas Infraestructuras SA presenta documentación societaria consistente y estados financieros para 2022–2024, pero con una carencia KYC material: falta documentación de identidad (según KYC Screener Agent, regla KYC-001 en FAIL). En lo financiero, se observa deterioro significativo en 2024: caída de EBITDA (-35,4% vs 2023) con aumento de deuda (+10,0%), elevando el apalancamiento hasta 8,87x Debt/EBITDA (según Valuation Reviewer Agent). La liquidez corriente cae por debajo de 1x en 2024 (0,94), sugiriendo tensión de circulante (según Valuation Reviewer Agent y audit_flag del Model Builder Agent). En screening no hay hits, pero el propio motor indica limitación operativa (“fichero de sanciones no encontrado”), por lo que el resultado no es concluyente (según KYC Screener Agent). Externamente no se identifican señales negativas en fuentes consultadas (según Market Researcher Agent), con la salvedad de que es “ausencia de resultados”, no prueba de ausencia de riesgo.

## Validación KYC
- **KYC-001 – Documento de identidad presente: FAIL**. Evidencia: “no se encontró ningún documento tipo ‘dni’” (según KYC Screener Agent).  
  - **Implicación:** expediente incompleto para identificación/verificación de administradores/representantes; requiere subsanación antes de cierre KYC y, en su caso, antes de formalización.
- **KYC-003 – Consistencia de nombre legal entre documentos: PASS**. Evidencia: nombre único “Grupo Caldas Infraestructuras SA” (según KYC Screener Agent).
- **KYC-004 – Titular real identificado: PASS**. Evidencia: titulares reales presentes: **Grupo Caldas Holding SA (75%)** e **Infraestructuras del Norte SL (25%)** (según KYC Screener Agent, escritura 2001-06-20).  
- **KYC-005 – Información financiera presente: PASS**. Evidencia: balances con EBITDA, deuda, circulante, patrimonio neto, ingresos y gastos financieros (según KYC Screener Agent y Model Builder Agent).

## Análisis financiero
- **Modelo financiero normalizado:** 3 periodos **2022–2024** con campos completos (EBITDA, deuda financiera, activo/pasivo corriente, patrimonio neto, ingresos, gastos financieros), sin *data_gaps* (según Model Builder Agent).  
  - **Audit_flag relevante:** **Activo corriente < pasivo corriente en 2024 (16,8M vs 17,9M)** → posible tensión de liquidez o error de extracción; revisar (según Model Builder Agent).
- **Ratios clave y evolución (según Valuation Reviewer Agent):**
  - **Debt/EBITDA:** 4,23x (2022) → 5,21x (2023) → **8,87x (2024)**.
  - **Liquidez corriente (AC/PC):** 1,14 (2022) → 1,04 (2023) → **0,94 (2024)**.
  - **Cobertura de intereses (EBITDA/Gastos financieros):** 5,31x (2022) → 4,36x (2023) → **2,30x (2024)**.
- **Interpretación (basada en Valuation Reviewer Agent, con énfasis en trazabilidad):**
  - El deterioro 2024 combina **caída de EBITDA (-35,4%)** con **incremento de deuda (+10,0%)**, elevando el apalancamiento y reduciendo capacidad de repago vía generación operativa.  
  - La **liquidez <1x** en 2024 es consistente con el *audit_flag* del modelo y sugiere **riesgo de tensiones de circulante** (o necesidad de validar la extracción/criterio contable).  
  - La **cobertura de intereses** cae a 2,30x, reduciendo el colchón ante subidas de tipos o volatilidad operativa.  
  - **Señales internas de comportamiento:** “retraso puntual en pagos en 2023” y “1 impago registrado en el banco” (según KYC Screener Agent, alertas extraídas de la escritura/alertas internas), coherentes con un perfil más sensible a estrés de caja.

## Screening (sanciones / PEP / adverse media)
Resultados (según KYC Screener Agent; **nota: “fichero de sanciones no encontrado” → screening no concluyente**):
- **Grupo Caldas Infraestructuras SA:** sin hits reportados (fuente: local_db; limitación por fichero no encontrado).  
- **Grupo Caldas Holding SA (75%):** sin hits reportados (fuente: local_db; limitación por fichero no encontrado).  
- **Infraestructuras del Norte SL (25%):** sin hits reportados (fuente: local_db; limitación por fichero no encontrado).  
- **Pedro Caldas Fuentes (Consejero Delegado):** sin hits reportados (fuente: local_db; limitación por fichero no encontrado).  
- **María Jesús Prieto Valls (Consejera):** sin hits reportados (fuente: local_db; limitación por fichero no encontrado).  

**Revisión manual:** recomendada por limitación técnica del screening (no hay nivel de confianza cuantificado; requiere re-ejecución en listas actualizadas/proveedor oficial).

## Señales externas
No se han encontrado resultados en fuentes consultadas sobre noticias negativas, litigios, sanciones regulatorias, eventos operativos relevantes ni concurso/preconcurso para la sociedad; tampoco menciones relevantes para Pedro Caldas Fuentes y María Jesús Prieto Valls (según Market Researcher Agent). Se indica explícitamente que es **ausencia de resultados**, no confirmación de ausencia de riesgo.

## Recomendaciones
- **Subsanar KYC (prioritario):** aportar **documento de identidad** del/los representante(s) y/o administradores que firmen (DNI/NIE/pasaporte) para cerrar KYC-001 (según KYC Screener Agent).
- **Re-ejecutar screening** en herramienta/listas de sanciones/PEP/adverse media actualizadas (el screening actual no es concluyente por “fichero de sanciones no encontrado”; según KYC Screener Agent).
- **Validación financiera 2024:** confirmar composición de **activo/pasivo corriente** y explicar la **liquidez <1x** (0,94) y el *audit_flag* (según Model Builder Agent y Valuation Reviewer Agent).
- **Mitigantes de riesgo crediticio a considerar:** solicitar **plan de mejora de márgenes/EBITDA** y **plan de caja/circulante**; valorar **covenants** (p.ej., límite de apalancamiento y/o cobertura de intereses) y/o **garantías** si se incrementa exposición, dado el salto a **8,87x Debt/EBITDA** y cobertura **2,30x** (según Valuation Reviewer Agent).
- **Revisión de comportamiento interno:** analizar causas del **retraso 2023** y del **impago** y su recurrencia (según KYC Screener Agent, alertas internas), y ajustar condiciones (importe/plazo/estructura) en función de conclusiones.
- **Escalado:** elevar a comité/compliance cualquier conclusión tras screening actualizado y la subsanación documental KYC, especialmente si aparecen hits o inconsistencias.

Estas recomendaciones son propuestas; la decisión final corresponde al analista y al comité de riesgos.