# Informe de riesgo - Acme Componentes SL

## Resumen ejecutivo
Acme Componentes SL presenta un perfil financiero en mejora 2022–2024: crecimiento de ingresos (32,0M€ → 42,0M€) y EBITDA (3,8M€ → 5,8M€), con apalancamiento estable (~2,1x Debt/EBITDA) y cobertura de intereses alta (>8x). En KYC, el nombre legal y la identificación de titulares reales constan en la escritura, pero falta documentación de identidad (DNI) en el paquete, lo que impide cierre KYC completo. El screening no arroja hits, pero es **no concluyente** al basarse en una fuente local y requiere repetición en listas operativas actualizadas. Señales externas: noticias de expansión (planta en Polonia) y contratos hasta 2027, sin indicios negativos concluyentes en el alcance consultado.

## Validación KYC
- **KYC-001 – Documento de identidad presente: FAIL**. Evidencia: “no se encontró ningún documento tipo ‘dni’” (según KYC Screener Agent).
  - **Implicación:** no se puede verificar formalmente la identidad de las personas físicas relevantes (p. ej., administrador/titular real), por lo que el alta/renovación debe quedar condicionada a aportar documentación válida.
- **KYC-003 – Consistencia de nombre legal entre documentos: PASS**. Evidencia: nombres encontrados: “Acme Componentes SL” (KYC Screener Agent; escritura y balances).
- **KYC-004 – Titular real identificado: PASS**. Evidencia: titulares reales presentes (KYC Screener Agent; escritura 10/07/2003): **Roberto Acme Jiménez** y **Acme Europe Holding GmbH**.
- **KYC-005 – Información financiera presente: PASS**. Evidencia: balances con magnitudes completas 2022–2024 (KYC Screener Agent; documentos “balance”).

## Análisis financiero
- **Modelo financiero normalizado (Model Builder Agent):** 3 periodos disponibles **2022–2024**, con EBITDA, deuda financiera, activo/pasivo corriente, patrimonio neto, ingresos y gastos financieros completos; **sin audit_flags** y sin gaps reportados.
- **Ratios clave y evolución (Valuation Reviewer Agent):**
  - **Debt/EBITDA:** 2,11x (2022) → 2,14x (2023) → 2,07x (2024). Estable con ligera mejora en 2024.
  - **Liquidez corriente (Activo corriente/Pasivo corriente):** 1,32x → 1,36x → 1,48x. Tendencia positiva (mayor holgura de corto plazo).
  - **Cobertura de intereses (EBITDA/Gastos financieros):** 8,44x → 9,42x → 9,51x. Nivel alto y creciente.
- **Interpretación (ajustada a los datos):** el crecimiento de EBITDA (3,8M€ → 5,8M€) compensa el aumento de deuda (8,0M€ → 12,0M€), manteniendo el apalancamiento alrededor de ~2,1x. La mejora de liquidez y la cobertura de intereses sugieren capacidad de servicio de deuda robusta ante escenarios de estrés moderado. Según Valuation Reviewer Agent, el historial con el banco incluye 5 operaciones desde 2022 sin impagos y con incidencias operativas/documentales (no crediticias), recomendándose seguimiento de disciplina de reporting.

## Screening (sanciones / PEP / adverse media)
Resultados (KYC Screener Agent; fuente **local_db**, **confidence: non_conclusive** en todos los casos; requiere re-screening en fuentes operativas UE/OFAC/ONU/HMT o proveedor interno):
- **Acme Componentes SL:** sin hits; **no concluyente** → requiere revisión/actualización de screening.
- **Acme Europe Holding GmbH:** sin hits; **no concluyente** → requiere revisión/actualización de screening.
- **Klaus Meier:** sin hits; **no concluyente** → requiere revisión/actualización de screening.
- **Roberto Acme Jiménez:** sin hits; **no concluyente** → requiere revisión/actualización de screening.

## Señales externas
Según Market Researcher Agent: dos noticias corporativas positivas/neutral (planta en Polonia; ampliación/renovación de contratos con fabricantes alemanes con ingresos comprometidos hasta 2027). No se identifican señales negativas concluyentes (insolvencia, sanciones regulatorias, litigios públicos) para Acme Componentes SL en el alcance consultado. Para Acme Europe Holding GmbH, Klaus Meier y Roberto Acme Jiménez no se hallaron resultados verificables relevantes; se sugiere contraste en fuentes oficiales (BORME/BOE/CENDOJ) si se requiere validación formal.

## Recomendaciones
- Solicitar y verificar **documento de identidad** vigente (DNI/NIE/pasaporte según aplique) de las personas físicas relevantes (al menos **Roberto Acme Jiménez** y, si procede por rol, **Klaus Meier**) para cerrar el **FAIL KYC-001** (según KYC Screener Agent).
- Repetir **screening sanciones/PEP/adverse media** en fuentes operativas actualizadas (UE/OFAC/ONU/HMT y/o proveedor interno) para convertir el resultado **non_conclusive** en concluyente (según KYC Screener Agent).
- Mantener covenants/seguimiento de **reporting financiero** dada la mención de incidencias documentales históricas (Valuation Reviewer Agent), y solicitar calendario de entrega de cuentas/auditoría si aplica.
- En análisis de crédito, considerar que el perfil 2022–2024 muestra **apalancamiento ~2,1x**, **liquidez 1,48x** y **cobertura de intereses ~9,5x** (Valuation Reviewer Agent), y usar estos niveles como base para dimensionar importe/plazo y posibles garantías (sin prejuzgar decisión).
- Si el comité requiere validación externa formal, contrastar cambios societarios/litigios en **BORME/BOE/CENDOJ** (según Market Researcher Agent).
  
Estas recomendaciones son propuestas; la decisión final corresponde al analista y al comité de riesgos.