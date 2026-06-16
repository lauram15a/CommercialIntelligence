# Informe de riesgo - Constructora Bermejo e Hijos SL

## Resumen ejecutivo
Constructora Bermejo e Hijos SL presenta un expediente de onboarding con **información crítica incompleta** (según KYC Screener Agent: faltan identificación, titularidad real y estados financieros). El screening disponible **no arroja hits**, pero está limitado por incidencias de fuente (“fichero de sanciones no encontrado”). No se dispone de **modelo financiero ni ratios** por ausencia total de magnitudes/periodos (según Model Builder y Valuation Reviewer). Como señal de negocio, se menciona una **adjudicación de contrato de rehabilitación urbana por 12M EUR** con necesidad de **línea de avales y financiación de circulante** (según documento “escritura” en KYC Screener). En señales externas, **no se encontraron noticias negativas**, aunque la ausencia de resultados no permite descartar eventos adversos (según Market Researcher).

## Validación KYC
- **KYC-001 – Documento de identidad presente: FAIL**  
  **Evidencia:** “no se encontró ningún documento tipo ‘dni’” (KYC Screener Agent).  
  **Implicación:** no es posible verificar identidad de personas físicas relevantes (administradores/representantes/UBO), impidiendo completar diligencia debida.
- **KYC-003 – Consistencia de nombre legal entre documentos: PASS**  
  **Evidencia:** nombres encontrados: “Constructora Bermejo e Hijos SL” (KYC Screener Agent).  
  **Implicación:** coherencia nominal básica, pero no suple carencias de identificación/estructura.
- **KYC-004 – Titular real identificado: FAIL**  
  **Evidencia:** “no se identifica titular real” (KYC Screener Agent).  
  **Implicación:** incumplimiento de requisito esencial AML (UBO), requiere obtención y verificación antes de avanzar.
- **KYC-005 – Información financiera presente: FAIL**  
  **Evidencia:** “faltan estados financieros” (KYC Screener Agent).  
  **Implicación:** no se puede evaluar capacidad de repago ni dimensionar riesgo para avales/circulante.

## Análisis financiero
- **Modelo financiero normalizado:** no disponible.  
  **Periodos disponibles:** ninguno (según Model Builder Agent: `periodos: []`).  
  **Audit_flags:** “Entrada vacía: no se recibieron objetos 'datos_financieros', por lo que no es posible normalizar ni auditar periodos.” (Model Builder).
- **Ratios clave y evolución:** no calculables por falta de datos (según Valuation Reviewer Agent: `ratios_por_periodo: []`).  
  - Debt/EBITDA: N/D  
  - Liquidez corriente: N/D  
  - Cobertura de intereses: N/D
- **Interpretación (Valuation Reviewer):** el análisis cuantitativo está **materialmente limitado** por ausencia de métricas financieras y **sin historial previo** en el banco; se requiere al menos Debt/EBITDA (≥2 periodos y %YoY), liquidez corriente y cobertura de intereses, además de detalle de deuda, vencimientos y coste financiero.

## Screening (sanciones / PEP / adverse media)
- **Constructora Bermejo e Hijos SL:**  
  - **Hits:** ninguno (según KYC Screener Agent).  
  - **Limitación relevante:** “fichero de sanciones no encontrado” (fuente: `local_db`).  
  - **Revisión manual:** recomendable repetir screening con fuentes operativas completas (sanciones/PEP/adverse media) y extender a **administradores y titulares reales** cuando se identifiquen (actualmente no constan).

## Señales externas
Según Market Researcher Agent, **no aparecieron resultados públicos** sobre noticias relevantes/negativas, concurso/preconcurso, litigios/demandas, sanciones o multas. Se indica explícitamente que, al no devolver información las fuentes consultadas, **no es posible confirmar ni descartar** eventos adversos por esta vía.

## Recomendaciones
- **Completar KYC esencial (bloqueante):**
  - Aportar **DNI/NIE/pasaporte** de administradores/representantes y verificación de poderes (KYC-001 FAIL).
  - Identificar y documentar **titular(es) real(es) (UBO)** con soporte (estructura accionarial, declaración UBO, y documentación identificativa) (KYC-004 FAIL).
  - Completar **identificador fiscal (NIF)** y **domicilio social** verificado (según “No consta en BBDD KYC” y “dirección: No consta” en extracción KYC).
- **Completar información financiera (bloqueante para análisis de riesgo):**
  - Solicitar **cuentas anuales** (mínimo 2 ejercicios), **balance y PyG recientes**, y **detalle de deuda** (importe, entidades, vencimientos, garantías, coste) para poder construir modelo y ratios (KYC-005 FAIL; Model Builder/Valuation Reviewer sin datos).
- **Screening y controles:**
  - Re-ejecutar screening con **fuentes de sanciones/PEP/adverse media disponibles** (incidencia: “fichero de sanciones no encontrado”) y realizar screening de **todas las personas físicas** una vez identificadas.
- **Análisis de la operación (por la señal de contrato 12M EUR):**
  - Solicitar documentación del **contrato adjudicado** (pliegos, hitos de cobro, penalizaciones), **plan de obra**, **presupuesto**, y **necesidades de circulante/avales** para dimensionar límites y estructura (según alerta extraída por KYC Screener).
  - Considerar **condiciones de mitigación** sujetas a análisis: garantías/contragarantías para avales, covenants de información financiera periódica y control de vencimientos.
- **Escalado:**
  - Elevar a **Compliance** por FAILs KYC y por limitación de screening; elevar a **Comité de Riesgos** una vez completada la información mínima para cuantificar capacidad de repago y estructura de la operación.

Estas recomendaciones son propuestas; la decisión final corresponde al analista y al comité de riesgos.