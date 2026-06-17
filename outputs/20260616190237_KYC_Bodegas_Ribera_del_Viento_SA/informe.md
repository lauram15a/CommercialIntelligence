# Informe de riesgo - Bodegas Ribera del Viento SA

## Resumen ejecutivo
La información recibida para **Bodegas Ribera del Viento SA** es insuficiente para un análisis de riesgo crediticio completo: el paquete documental contiene esencialmente una **escritura** sin campos clave (según KYC Screener Agent). En KYC, fallan requisitos críticos (identificación, titularidad real y estados financieros), lo que impide cerrar la debida diligencia. En el plano financiero, **no hay periodos ni estados** para construir modelo ni ratios (según Model Builder y Valuation Reviewer). En señales externas, no se observan incidencias públicas concluyentes en las fuentes consultadas, pero la búsqueda no pudo extenderse a administradores/titulares por falta de identificación (según Market Researcher). Se requiere completar documentación y re-screening en fuentes operativas antes de elevar una propuesta de estructura crediticia.

## Validación KYC
- **KYC-001 – Documento de identidad presente: FAIL**  
  **Evidencia:** “no se encontró ningún documento tipo ‘dni’” (KYC Screener Agent).  
  **Implicación:** no es posible verificar identidad de intervinientes/personas físicas vinculadas (administradores/representantes/UBO), bloqueando el onboarding.
- **KYC-003 – Consistencia de nombre legal entre documentos: PASS**  
  **Evidencia:** nombres encontrados: `['Bodegas Ribera del Viento SA']` (KYC Screener Agent).  
  **Implicación:** coherencia nominal básica, pero no suple la falta de identificadores (NIF) y datos registrales.
- **KYC-004 – Titular real identificado: FAIL**  
  **Evidencia:** “no se identifica titular real” (KYC Screener Agent).  
  **Implicación:** incumplimiento de requisito esencial AML/CTF; no puede determinarse estructura de control ni riesgo PEP/sanciones asociado a UBO.
- **KYC-005 – Información financiera presente: FAIL**  
  **Evidencia:** “faltan estados financieros” (KYC Screener Agent).  
  **Implicación:** no se puede evaluar capacidad de repago, covenanting ni dimensionar exposición.

## Análisis financiero
- **Modelo financiero normalizado:** no disponible.  
  **Periodos disponibles:** ninguno (`periodos: []`).  
  **Audit flags:** “Entrada vacía: no se recibieron objetos 'datos_financieros'…” (Model Builder Agent).
- **Ratios clave y evolución:** no calculables por ausencia de datos (Valuation Reviewer Agent).  
  - **Debt/EBITDA:** N/D (sin deuda ni EBITDA por periodo/LTM).  
  - **Liquidez corriente:** N/D (sin activo/pasivo corriente).  
  - **Cobertura de intereses:** N/D (sin gasto financiero/EBIT).
- **Interpretación (Valuation Reviewer Agent, ajustada):** coincide la imposibilidad de concluir sobre apalancamiento, liquidez y servicio de deuda por falta total de inputs. Adicionalmente, se indica **sin relación histórica con el banco (0 operaciones)** y **sin incidencias/impagos (0)**, pero con valor predictivo limitado por ausencia de historial (Valuation Reviewer Agent).

## Screening (sanciones / PEP / adverse media)
- **Bodegas Ribera del Viento SA:** **sin hits** en fuente `local_db`, **confianza: non_conclusive** (KYC Screener Agent).  
  **Requiere revisión manual / repetición:** sí, el propio resultado indica repetir screening en **fuentes operativas actualizadas (UE/OFAC/ONU/HMT y/o proveedor interno)** para cierre concluyente (KYC Screener Agent).
- **Administradores / Titulares reales / Representantes:** **no screeneados** por no constar identificados en la documentación (KYC Screener Agent).

## Señales externas
Según Market Researcher Agent, **no aparecen incidencias públicas concluyentes** (concursos, sanciones o litigios) para la entidad en las fuentes consultadas; el contenido hallado es genérico/sectorial (DeepResearch Mock Feed 2026-04-10 y 2026-05-20; fuentes_externas.json 2026-06-16). No se encontraron referencias específicas a **concurso de acreedores** ni **litigios** asociados. La búsqueda **no pudo ampliarse a personas** por falta de administradores/titulares identificados. Se recomienda contraste en **BORME/Registro Mercantil, BOE y CENDOJ** si se requiere evidencia documental (Market Researcher Agent).

## Recomendaciones
- Solicitar y verificar **NIF/CIF**, **domicilio social**, **fecha de constitución** y **datos registrales** completos; la escritura aportada no contiene los campos necesarios (según KYC Screener Agent, “ausencia de datos clave”).
- Recabar **identificación de administradores/representantes** y **documentos de identidad** correspondientes (DNI/NIE/pasaporte) para cumplir KYC-001 (KYC Screener Agent).
- Obtener **declaración y evidencia de titularidad real (UBO)** y documentación soporte para cumplir KYC-004; posteriormente, **screening PEP/sanciones/adverse media** de UBO y administradores.
- Solicitar **estados financieros** (idealmente auditados) y/o **impuesto de sociedades**, además de **deuda total**, **EBITDA LTM**, **gasto financiero**, **activo/pasivo corriente** para construir modelo y ratios (Model Builder + Valuation Reviewer).
- Repetir **screening en listas operativas actualizadas** (UE/OFAC/ONU/HMT o proveedor interno) dado el resultado **non_conclusive** en base local (KYC Screener Agent).
- Si se pretende avanzar en estructuración, condicionar cualquier propuesta a **entrega de información financiera mínima** y, en su caso, considerar **garantías** y/o **importe/plazo conservadores** hasta disponer de métricas (recomendación operativa derivada de la ausencia total de ratios; Valuation Reviewer + Model Builder).
- Escalar a **Compliance** para cierre de gaps KYC (FAILs) y validación de screening concluyente antes de cualquier paso posterior del onboarding (KYC Screener Agent).

Estas recomendaciones son propuestas; la decisión final corresponde al analista y al comité de riesgos.