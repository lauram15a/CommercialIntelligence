# Informe de riesgo - Datalyx Iberia SL

## Resumen ejecutivo
Datalyx Iberia SL presenta una situación financiera en expansión en 2022–2024, con crecimiento de ingresos y EBITDA y mejora gradual de apalancamiento, liquidez y cobertura de intereses (según Model Builder y Valuation Reviewer). En KYC, el nombre legal es consistente y los titulares reales están identificados, pero falta documentación de identidad (DNI) en el paquete, lo que impide cierre KYC sin subsanación (según KYC Screener). El screening no arroja hits, pero es **no concluyente** al basarse en una fuente local de demo y requiere repetición en listas operativas (UE/OFAC/ONU/HMT/proveedor interno). Externamente, se observan señales de fortalecimiento corporativo (entrada de Nordic Capital y nuevos contratos), sin hallazgos negativos concluyentes en las búsquedas realizadas (según Market Researcher).

## Validación KYC
- **KYC-001 – Documento de identidad presente: FAIL**. Evidencia: “no se encontró ningún documento tipo ‘dni’” (según KYC Screener Agent).
  - **Implicación:** no se puede completar la verificación de identidad de personas físicas relevantes (administradores/UBOs) y debe solicitarse documentación antes de cierre.
- **KYC-003 – Consistencia de nombre legal entre documentos: PASS**. Evidencia: nombres encontrados: `['Datalyx Iberia SL']` (según KYC Screener Agent).
- **KYC-004 – Titular real identificado: PASS**. Evidencia: “titulares reales presentes” (según KYC Screener Agent; escritura 14/02/2018).
- **KYC-005 – Información financiera presente: PASS**. Evidencia: “balance/PyG encontrado” (según KYC Screener Agent; balances 2022–2024).

## Análisis financiero
- **Modelo financiero normalizado:** 3 periodos **2022–2024** con EBITDA, deuda financiera, activo/pasivo corriente, patrimonio neto, ingresos y gastos financieros completos; **sin gaps** por periodo (según Model Builder Agent).  
  - **Audit flags:** chequeos de plausibilidad OK; no se detectan saltos >100% interanuales (según Model Builder Agent).
- **Ratios clave y evolución (según Valuation Reviewer Agent):**
  - **Debt/EBITDA:** 2022 **1,36x** → 2023 **1,27x** → 2024 **1,25x** (mejora ligera).
  - **Liquidez corriente (AC/PC):** 2022 **2,33x** → 2023 **2,56x** → 2024 **2,95x** (holgura creciente).
  - **Cobertura de intereses (EBITDA/gastos fin.):** 2022 **12,94x** → 2023 **15,00x** → 2024 **16,55x** (resiliencia creciente).
- **Interpretación integrada:** el aumento de deuda (2022–2024) se acompaña de crecimiento superior de EBITDA, manteniendo el apalancamiento contenido y reforzando la capacidad de servicio de deuda; la liquidez y la cobertura de intereses muestran tendencia positiva (según Valuation Reviewer Agent). Adicionalmente, el historial con el banco reporta **2 operaciones vigentes** (circulante **700k** e inversión **400k**) **al corriente**, con **impagos 0** e **incidencias 0** (según Valuation Reviewer Agent).

## Screening (sanciones / PEP / adverse media)
Resultados (según KYC Screener Agent; **fuente local_db demo**, confianza **non_conclusive** en todos los casos; requiere repetición en fuente operativa):
- **Datalyx Iberia SL:** sin hits (non_conclusive) → **requiere re-screening**.
- **Sofía Datalyx Ferrer:** sin hits (non_conclusive) → **requiere re-screening**.
- **Marc Ribera Vidal:** sin hits (non_conclusive) → **requiere re-screening**.
- **Nordic Capital Iberia BV:** sin hits (non_conclusive) → **requiere re-screening**.  
**Revisión manual:** no hay coincidencias que revisar, pero el resultado no es concluyente por limitación de fuente.

## Señales externas
- Señales positivas: noticia de **entrada de Nordic Capital (35%)** con **valoración 42 M€** (*Expansión*, 20/11/2025) y **contratos con tres entidades financieras españolas**, con mención a superar **20 M€ de ingresos recurrentes anuales** en 2026 (*CincoDías*, 05/03/2026) (según Market Researcher Agent).
- Señales negativas: no se encontraron resultados de **concurso/preconcurso** en la búsqueda específica; tampoco **litigios o sanciones regulatorias concluyentes** en el feed consultado (según Market Researcher Agent). Se sugiere contraste en **BOE/BORME/CENDOJ** si aplica.

## Recomendaciones
- Solicitar y verificar **documentos de identidad (DNI/NIE/pasaporte)** de **administradores y titulares reales** (al menos Sofía Datalyx Ferrer y Marc Ribera Vidal) para subsanar **KYC-001 FAIL** (según KYC Screener Agent).
- Repetir **screening sanciones/PEP/adverse media** en fuentes operativas actualizadas (UE/OFAC/ONU/HMT y/o proveedor interno) para convertir el resultado **non_conclusive** en concluyente (según KYC Screener Agent).
- Pedir soporte documental del hito corporativo: evidencia de la **estructura accionarial actual** y, si procede, documentación de la **entrada de Nordic Capital** (cap table actualizado / escritura o certificación) para alinear KYC con señales externas (según Market Researcher Agent vs. escritura 2018 del KYC Screener Agent).
- Mantener el análisis de capacidad de repago apoyado en los ratios 2022–2024; si la operación implica incremento material de deuda, solicitar escenario de sensibilidad (p. ej., caída de EBITDA y subida de coste financiero) dado que el crecimiento reciente es fuerte (según Model Builder + Valuation Reviewer).
- Verificación externa adicional (si procede por política): contraste en **BORME/BOE/CENDOJ** para confirmar ausencia de incidencias societarias/judiciales relevantes (según Market Researcher Agent).
- Considerar, en estructuración, covenants informativos básicos (entrega de EEFF anuales, endeudamiento) coherentes con el perfil de crecimiento y el uso de líneas (según Valuation Reviewer Agent: operaciones vigentes y al corriente).  

Estas recomendaciones son propuestas; la decisión final corresponde al analista y al comité de riesgos.