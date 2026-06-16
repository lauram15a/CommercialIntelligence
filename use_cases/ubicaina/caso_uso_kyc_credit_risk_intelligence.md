# Caso de uso 1: KYC + Credit Risk Intelligence (documentación exhaustiva)

## 1. Resumen ejecutivo técnico-funcional
Este caso de uso implementa un pipeline multiagente para preparar un expediente de riesgo de crédito sobre cliente corporativo, con foco en:

1. Validación documental KYC.
2. Screening de listas (sanciones/PEP/adverse media).
3. Normalización financiera multi-período.
4. Análisis cuantitativo de riesgo (ratios + tendencia).
5. Síntesis en informe final para comité.

No hay decisión automática de aprobación/denegación. La salida es una recomendación analítica trazable para revisión humana.

## 2. Arquitectura real en ejecución

### 2.1. Capa de presentación
- Flask sirve formularios, estados de pipeline y vistas de resultados.
- Entrada KYC: `GET /kyc/`.
- Lanzamiento: `POST /kyc/solicitudes/nueva`.
- Seguimiento asíncrono: `GET /kyc/api/runs/<run_id>/status`.

### 2.2. Capa de orquestación
- `app.py` lanza un hilo background por solicitud.
- El hilo llama a `kyc_orchestrator.run_multiagent_pipeline(...)`.
- El orquestador controla la secuencia de los 5 agentes y persiste artefactos por paso.

### 2.3. Capa de agentes
Agentes ejecutados y responsabilidad principal:
1. `kyc_screener`: ingesta + reglas KYC + screening.
2. `model_builder`: normalización financiera y auditoría básica de calidad.
3. `market_researcher`: señales externas.
4. `valuation_reviewer`: cálculo de ratios + interpretación de riesgo.
5. `credit_risk_report`: síntesis final en markdown.

### 2.4. Capa de datos
Fuente principal unificada:
- `data/bbdd.json`.

Fuentes legacy de fallback si faltan secciones:
- `data/empresas_kyc.json`
- `data/historial.json`
- `data/listas_sanciones.json`
- `data/noticias_empresas.json` / `data/noticias_mock.json`

### 2.5. Capa de LLM y autenticación
- Cliente LLM en `src/azure_client.py`.
- Autenticación vía `DefaultAzureCredential` o `ManagedIdentityCredential`.
- Perfil usado por agentes: `gpt52`.

## 3. Flujo end-to-end (paso a paso, con responsables)

### 3.1. Recepción de solicitud
Entrada de usuario:
- `entity_name` (obligatorio)
- `entity_notes` (opcional)

Lógica:
1. Buscar empresa en KYC (`_get_empresa_kyc`).
2. Si no existe, intentar en Deal (`_get_empresa_deal`) y mapear (`_deal_to_kyc_entity`).
3. Construir documentos internos con `_build_kyc_documents`.
4. Crear `provisional_run_id`, registrar estado y lanzar hilo.

Resultado:
- UI de progreso disponible inmediatamente sin bloquear la petición.

### 3.2. Construcción de documentos de expediente
No se inyecta texto estático fijo: los documentos se generan a partir de BBDD.

Documentos generados:
1. `escritura_constitucion.txt`.
2. `balance_<periodo>.txt` por cada período disponible.
3. `expediente_basico.txt` como último fallback.

Campos utilizados para la redacción:
- Identificación: nombre legal, NIF, forma jurídica, domicilio, fecha constitución.
- Estructura societaria: titulares reales, administradores.
- Riesgo previo: alertas KYC, observaciones.
- Finanzas: ingresos, EBITDA, gastos financieros, activo/pasivo corriente, deuda, patrimonio.

### 3.3. Ejecución orquestada
`kyc_orchestrator.run_multiagent_pipeline(...)` ejecuta secuencialmente:
1. KYC Screener.
2. Model Builder.
3. Market Researcher.
4. Valuation Reviewer.
5. Credit Risk Report.

En cada paso:
- Se emite callback `started/completed`.
- Se persiste output intermedio en subcarpeta numerada.

## 4. Agente por agente: qué hace, en qué se basa y qué decisiones toma

### 4.1. KYC Screener Agent
Archivo principal:
- `src/agents/kyc_screener/agent.py`

Subcomponentes:
- `src/agents/kyc_screener/doc_reader.py`
- `src/agents/kyc_screener/screening.py`

Proceso interno:
1. Parsea documentos en estructura JSON por documento (`run_doc_reader`).
2. Ejecuta reglas deterministas (`evaluate_kyc_rules`).
3. Construye sujetos de screening (entidad + UBO + administradores).
4. Ejecuta screening por sujeto (`run_screening_tool`).

Reglas deterministas implementadas:
- KYC-001: documento identidad presente.
- KYC-002: antigüedad del documento de identidad.
- KYC-003: consistencia del nombre legal entre documentos.
- KYC-004: titular real identificado.
- KYC-005: información financiera presente.

Decisiones en este agente:
- Determina PASS/WARN/FAIL por regla.
- Determina qué personas/entidades se envían a screening.
- No toma decisión final de riesgo.

Salida:
- `extracted_entities`
- `kyc_results`
- `screening_results`

### 4.2. Model Builder Agent
Archivo:
- `src/agents/model_builder/agent.py`

Entrada:
- `extracted_entities` del paso anterior.

Proceso:
1. Extrae bloques `datos_financieros` válidos.
2. Solicita al LLM un JSON normalizado por período.
3. Exige salida `json_object`.

Qué debe resolver el modelo (según prompt de tarea):
- Agrupar por período.
- Fusionar campos no nulos cuando hay duplicidad de año.
- Orden cronológico.
- `audit_flags` por saltos >100% y plausibilidad.
- `data_gaps` por campos faltantes.

Decisiones en este agente:
- Priorización y consolidación de datos heterogéneos.
- Identificación de calidad de dato.
- No calcula recomendación crediticia.

Salida:
- `periodos`
- `audit_flags`
- `resumen`

### 4.3. Market Researcher Agent
Archivo:
- `src/agents/market_researcher/agent.py`

Entrada:
- `entity_name`
- `related_names` (administradores/titulares reales)

Proceso:
1. Configura tool `web_search` como function-calling.
2. Itera hasta `max_tool_calls` (por defecto 4).
3. Cada llamada resuelve con `run_web_search_tool`.
4. En entorno actual, `real_web_search` usa BBDD local (no API externa real).

Datos consultados:
- Primario: `bbdd.json -> noticias_empresas`.
- Fallback: `noticias_empresas.json` / `noticias_mock.json`.

Decisiones en este agente:
- Qué búsquedas disparar y con qué términos.
- Qué hallazgos resumir como señal externa relevante.
- No decide aprobación/denegación.

Salida:
- Texto resumen (no JSON estructurado).

### 4.4. Valuation Reviewer Agent
Archivo:
- `src/agents/valuation_reviewer/agent.py`

Entrada:
- Modelo financiero normalizado.
- Historial interno cliente (`load_historial`).

Proceso híbrido:
1. Cálculo determinista Python (`compute_financial_ratios`).
2. Interpretación cualitativa LLM (`interpret_financial_ratios`).

Ratios calculados en código:
- `debt_ebitda`
- `liquidez_corriente`
- `cobertura_intereses`

Variaciones interanuales:
- EBITDA, deuda financiera, ingresos (si hay datos consecutivos).

Decisiones en este agente:
- Cuantificación y tendencia del riesgo financiero.
- Narrativa de riesgo en tono comité.
- No decisión final de concesión.

Salida:
- `ratios`
- `interpretacion`

### 4.5. Credit Risk Report Agent
Archivo:
- `src/agents/credit_risk_report/agent.py`

Entrada:
- Output completo de los 4 agentes previos.

Proceso:
1. Construye prompt con estructura de informe obligatoria.
2. Inyecta resultados por secciones (KYC, financiero, screening, señales externas).
3. Genera markdown final.

Decisiones en este agente:
- Síntesis y priorización narrativa de hallazgos.
- Recomendaciones operativas de mitigación/documentación.
- Prohibición explícita de decisión final automática.

Salida:
- `informe.md`
- Integración en `result.json`.

## 5. Estado de ejecución, trazabilidad y recuperación

### 5.1. Estado en memoria
Estructuras:
- `_RUNS_STATE`
- `_RUNS_LOCK`

Campos de estado por run:
- `status` (`running`, `done`, `error`)
- `current_step`
- `completed_steps`
- `error`
- `real_run_id`
- `run_dir`

### 5.2. Progreso en UI
- El callback de orquestador actualiza `current_step` y completados.
- `run_progress.html` consume estado por polling al endpoint de status.

### 5.3. Persistencia en disco
Nombre de carpeta:
- `outputs/YYYYMMDDhhmmss_KYC_<Entidad>`

Artefactos típicos:
- `1_kyc_screener/output.json`
- `2_model_builder/output.json`
- `3_valuation_reviewer/output.json`
- `4_market_researcher/output.txt`
- `informe.md`
- `result.json`
- `app.log`

## 6. Plugins, prompts, skills y cookbooks: qué se usa de verdad

### 6.1. Pregunta clave: ¿se usan los agentes markdown de plugins?
Sí, parcialmente y de forma explícita en runtime Python.

`src/skill_loader.py` carga prompts base desde:
- `plugins/agent-plugins/kyc-screener/agents/kyc-screener.md`
- `plugins/agent-plugins/model-builder/agents/model-builder.md`
- `plugins/agent-plugins/valuation-reviewer/agents/valuation-reviewer.md`
- `plugins/agent-plugins/market-researcher/agents/market-researcher.md`

Luego concatena skills (`build_system_prompt`) con contenido SKILL.md.

### 6.2. Pregunta clave: ¿se usan skills de plugins?
Sí. Se inyectan en tiempo de ejecución desde rutas configuradas en `SKILL_PATHS`.

Skills activadas en este caso de uso:
- KYC Screener: `kyc-doc-parse`, `kyc-rules`.
- Model Builder: `clean-data-xls`, `3-statement-model`, `audit-xls`.
- Valuation Reviewer: `portfolio-monitoring`.
- Market Researcher: `sector-overview`.
- Credit Risk Report: no concatena skills; usa prompt base de `kyc-screener` y prompt de tarea.

### 6.3. Pregunta clave: ¿se usa managed-agent-cookbooks en la ejecución Flask?
No en la ruta runtime del proyecto web.

Detalles:
1. Flask ejecuta agentes Python locales en `src/agents/*`.
2. Los cookbooks bajo `managed-agent-cookbooks/*` son plantillas de despliegue para Claude Managed Agents (`POST /v1/agents`) y referencia de arquitectura.
3. Esos YAML/README se usan para despliegue externo con scripts dedicados, no para invocación directa desde `app.py`.

### 6.4. ¿Para qué sirven entonces los managed-agent-cookbooks aquí?
Sirven para:
1. Documentar topología de workers y límites de herramientas.
2. Definir manifests de despliegue en plataformas gestionadas.
3. Reutilizar el mismo prompt/skills del plugin como source of truth.

No sirven (en esta app Flask local) para ejecutar automáticamente los pasos del pipeline.

## 7. Decisiones de diseño relevantes (para defensa técnica)

1. Pipeline secuencial por simplicidad de trazabilidad y depuración.
2. Cálculo de ratios crítico hecho en Python determinista, no solo LLM.
3. Salidas intermedias persistidas por paso para auditoría y post-mortem.
4. Uso de fallback de datos para robustez operativa durante transición a BBDD unificada.
5. Restricción explícita en prompts de no automatizar decisión final de riesgo.
6. Separación de “research señal” y “decisión de riesgo” para gobernanza.

## 8. Preguntas complicadas frecuentes y respuesta corta

### 8.1. “¿Este pipeline llama a MCP de screening real?”
Actualmente, no de forma externa en la app Flask: `real_screening_lookup` delega en lookup local. Está preparada la interfaz para conectar proveedor real.

### 8.2. “¿Si falta empresa en KYC, se rompe?”
No. Intenta resolver en Deal y mapea a esquema mínimo KYC para que el flujo continúe.

### 8.3. “¿Dónde se ve la evidencia por regla?”
En `1_kyc_screener/output.json` dentro de `kyc_results` con `rule_id`, estado y evidencia textual.

### 8.4. “¿Se puede auditar qué dato originó la conclusión?”
Sí. Se conserva salida por paso y `result.json` agregado por ejecución.

### 8.5. “¿Los cookbooks mandan sobre la app?”
No. Los cookbooks son blueprint de despliegue gestionado; la app ejecuta módulos `src/agents`.

## 9. Riesgos técnicos y límites actuales

1. Dependencia de consistencia en nombres de empresa para joins simples.
2. Parte de conectores “real_*” siguen en modo local (placeholder operativo).
3. Calidad de extracción documental condiciona toda la cadena posterior.
4. Si falta configuración de paths/skills, `skill_loader` puede lanzar `FileNotFoundError`/`KeyError`.

## 10. Archivos de referencia obligada para auditoría completa

### Backend y orquestación
- `app.py`
- `kyc_orchestrator.py`
- `src/logging_utils.py`
- `src/azure_client.py`

### Agentes KYC pipeline
- `src/agents/kyc_screener/agent.py`
- `src/agents/kyc_screener/doc_reader.py`
- `src/agents/kyc_screener/screening.py`
- `src/agents/model_builder/agent.py`
- `src/agents/market_researcher/agent.py`
- `src/agents/valuation_reviewer/agent.py`
- `src/agents/credit_risk_report/agent.py`

### Carga de prompts/skills
- `src/skill_loader.py`
- `plugins/agent-plugins/kyc-screener/agents/kyc-screener.md`
- `plugins/agent-plugins/model-builder/agents/model-builder.md`
- `plugins/agent-plugins/market-researcher/agents/market-researcher.md`
- `plugins/agent-plugins/valuation-reviewer/agents/valuation-reviewer.md`

### Datos
- `data/bbdd.json`

### Plantillas UI
- `templates/index.html`
- `templates/run_progress.html`
- `templates/run_detail.html`

### Managed cookbooks (solo blueprint, no runtime Flask)
- `managed-agent-cookbooks/README.md`
- `managed-agent-cookbooks/kyc-screener/agent.yaml`
- `managed-agent-cookbooks/kyc-screener/README.md`
