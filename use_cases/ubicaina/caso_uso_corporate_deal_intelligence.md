# Caso de uso 2: Corporate & Deal Intelligence (documentación exhaustiva)

## 1. Resumen ejecutivo técnico-funcional
Este caso de uso automatiza la preparación comercial de oportunidades corporativas, desde la identificación de targets por sector hasta la generación de propuesta y pitchbook.

Objetivos operativos:
1. Detectar empresas con señal comercial accionable.
2. Priorizar oportunidades por relevancia.
3. Construir contexto financiero y de reunión.
4. Producir propuesta comercial trazable.
5. Entregar un artefacto listo para revisión humana (markdown + PPTX).

No automatiza contacto a cliente ni decisión comercial final: la revisión y personalización es humana.

## 2. Arquitectura real en ejecución

### 2.1. Capa de presentación
- Entrada de formulario: `GET /deal/`.
- Lanzamiento de solicitud: `POST /deal/solicitudes/nueva`.
- Progreso asíncrono: `GET /deal/api/runs/<run_id>/status`.
- Vista detalle: `GET /deal/runs/<run_id>`.
- Descarga PPTX: `GET /deal/runs/<run_id>/pitchbook.pptx`.

### 2.2. Capa de orquestación
- `app.py` lanza thread background para no bloquear UI.
- El hilo ejecuta `deal_orchestrator.run_deal_intelligence_pipeline(...)`.
- Cada paso notifica `started/completed` para pintar pipeline en frontend.

### 2.3. Capa de agentes
Secuencia real de pasos en orquestador:
1. Opportunity Researcher.
2. Earnings Reviewer.
3. Deal Model Builder (opcional).
4. Meeting Preparer.
5. Pitch Builder.

Nota importante:
- La secuencia efectiva en código no coincide con algunos documentos antiguos que ponían Model Builder antes de Earnings Reviewer.

### 2.4. Capa de datos
Fuente principal unificada:
- `data/bbdd.json`.

Secciones relevantes para Deal:
- `empresas_deal`.
- `noticias_empresas` (si se reutiliza Market Researcher en otros escenarios).

Fallbacks legacy:
- `data/empresas_deal.json`.
- `data/empresas_mock.json`.

### 2.5. Capa LLM y autenticación
- Cliente unificado en `src/azure_client.py`.
- `chat_completion(..., profile="gpt52")` en agentes Deal.
- Auth por identidad de Azure, sin API key hardcodeada en código.

## 3. Flujo end-to-end (paso a paso)

### 3.1. Recepción de solicitud
Datos recibidos por `POST /deal/solicitudes/nueva`:
- `sector` (obligatorio).
- `company_name` (opcional; empresa concreta).
- `doc_name[]` + `doc_text[]` (documentación financiera opcional de usuario).

Lógica de arranque:
1. Validación de sector.
2. Construcción de `financial_documents` desde formulario.
3. Alta de estado provisional en `_DEAL_RUNS_STATE`.
4. Lanzamiento de hilo `_run_deal_pipeline_background(...)`.

### 3.2. Ejecución del orquestador
Función:
- `deal_orchestrator.run_deal_intelligence_pipeline(...)`.

Decisiones de orquestación:
1. Crea carpeta de outputs desde el inicio con `entity=sector`.
2. Persiste output de cada paso en subcarpetas numeradas.
3. Selecciona empresa objetivo:
	- Si usuario indicó `company_name`, intenta match exacto case-insensitive.
	- Si no, toma la primera oportunidad priorizada.
4. Si no hay documentos financieros de entrada, genera `senal_oportunidad.txt` sintético para no frenar el pipeline.

## 4. Agente por agente: función, bases y decisiones

### 4.1. Opportunity Researcher Agent
Archivo:
- `src/agents/opportunity_researcher/agent.py`.

Qué hace:
1. Consulta empresas por sector (`local_company_lookup`).
2. Envía al LLM listado de empresas con descripción, señal, ingresos, empleados.
3. Pide JSON estricto con priorización y motivo.

Datos y fallback:
- Primario: `bbdd.json -> empresas_deal`.
- Fallback: `empresas_deal.json` o `empresas_mock.json`.

Decisiones que toma:
- Prioridad `alta/media/baja` por empresa.
- Orden de oportunidades.
- Resumen sectorial.

Salida:
- `1_opportunity_researcher/output.json`.

Observación técnica relevante:
- El prompt base cargado es `market-researcher` (por implementación actual), al que se le añade prompt de tarea específico de opportunity research.

### 4.2. Earnings Reviewer Agent
Archivo:
- `src/agents/earnings_reviewer/agent.py`.

Qué hace:
1. Lee textos financieros aportados (o documento sintético del orquestador).
2. Genera análisis de tendencias (ingresos, margen, CAPEX, endeudamiento).
3. Produce texto narrativo para consumo de pasos posteriores.

Decisiones que toma:
- Qué tendencias destacar y con qué evidencia cuantitativa.
- Qué limitaciones de datos declarar.

Salida:
- `2_earnings_reviewer/output.txt`.

Observación técnica relevante:
- Intenta cargar prompt base de `earnings-reviewer`.
- `src/skill_loader.py` no define hoy ese agent key en `AGENT_PROMPTS`, por lo que cae a `_fallback_prompt()`.

### 4.3. Deal Model Builder Agent (opcional)
Archivo:
- `src/agents/deal_model_builder/agent.py`.

Qué hace:
1. Si hay `earnings_summary`, extrae indicadores y tendencias estructurales.
2. Genera interpretación financiera de alto nivel en JSON.

Comportamiento opcional:
- Si `earnings_summary` viene vacío, devuelve `disponible=False` y el pipeline sigue.

Decisiones que toma:
- Qué indicadores son más representativos para construcción de caso.
- Qué interpretación financiera aportar al briefing comercial.

Salida:
- `3_model_builder/output.json`.

### 4.4. Meeting Preparer Agent
Archivo:
- `src/agents/meeting_preparer/agent.py`.

Qué hace:
1. Integra contexto de oportunidad + earnings + model output (si existe).
2. Devuelve briefing estructurado:
	- `perfil`
	- `situacion_actual`
	- `necesidades_potenciales`
	- `riesgos`
	- `talking_points`

Decisiones que toma:
- Qué mensajes son accionables para reunión.
- Qué riesgos deben abrir conversación comercial.

Salida:
- `4_meeting_preparer/output.json`.

Observación técnica relevante:
- Intenta prompt base `meeting-prep-agent`, pero también cae a fallback por ausencia de key en `AGENT_PROMPTS`.

### 4.5. Pitch Builder Agent
Archivo:
- `src/agents/pitch_builder/agent.py`.

Qué hace:
1. Integra oportunidad, earnings, briefing y modelo opcional.
2. Genera JSON de propuesta comercial (título, argumentos, comparables, próximos pasos, narrativa markdown).
3. Construye PPTX con `build_pitch_deck(...)`.

Decisiones que toma:
- Estructura narrativa comercial.
- Encaje de productos/servicios.
- Secuencia de próximos pasos.

Salidas:
- `5_pitch_builder/output.json`
- `5_pitch_builder/pitchbook.pptx`
- `propuesta.md` (raíz del run, desde `narrativa_markdown`)

Observación técnica relevante:
- Igual que en los dos agentes previos, intenta `pitch-agent` y cae a fallback porque no está en `AGENT_PROMPTS`.

## 5. Estado, persistencia y trazabilidad

### 5.1. Estado asíncrono
Diccionario de estado:
- `_DEAL_RUNS_STATE`.

Campos relevantes:
- `status`, `current_step`, `completed_steps`, `error`, `real_run_id`.

### 5.2. Carpeta de salida
Formato:
- `outputs/YYYYMMDDhhmmss_DEAL_<SectorNormalizado>`.

Generada por:
- `src/logging_utils.setup_run_logging(use_case="deal", entity=sector)`.

### 5.3. Artefactos de salida
Estructura típica:
1. `1_opportunity_researcher/output.json`
2. `2_earnings_reviewer/output.txt`
3. `3_model_builder/output.json`
4. `4_meeting_preparer/output.json`
5. `5_pitch_builder/output.json`
6. `5_pitch_builder/pitchbook.pptx`
7. `propuesta.md`
8. `result.json`
9. `app.log`

### 5.4. Visualización y descarga
- `deal_run_detail` carga `result.json`, `propuesta.md` y `2_earnings_reviewer/output.txt`.
- `deal_download_pitchbook` toma `pitch_output.pptx_path` desde `result.json` y fuerza descarga.

## 6. Plugins, skills y managed-agent-cookbooks: realidad de uso

### 6.1. ¿Usa plugins/agent-plugins?
Sí, pero con matiz:
1. El runtime Python usa `src/skill_loader.py`.
2. `AGENT_PROMPTS` solo define 4 prompts base:
	- `kyc-screener`
	- `model-builder`
	- `valuation-reviewer`
	- `market-researcher`
3. En Deal, tres agentes intentan keys no registradas (`earnings-reviewer`, `meeting-prep-agent`, `pitch-agent`) y caen a prompt fallback interno.

Conclusión:
- En Deal, hoy se usan plenamente skills y prompts de tarea interna.
- El prompt base de plugin no se usa para esos tres agentes salvo que se amplíe `AGENT_PROMPTS`.

### 6.2. ¿Se usan skills de plugins en Deal?
Sí.

Skills invocadas en código Deal:
- Opportunity Researcher: `sector-overview`.
- Earnings Reviewer: `audit-xls`.
- Deal Model Builder: `3-statement-model`.
- Meeting Preparer: `portfolio-monitoring`.
- Pitch Builder: `sector-overview`.

### 6.3. ¿Se usa managed-agent-cookbooks en runtime Flask?
No.

Papel real de `managed-agent-cookbooks/*`:
1. Plantillas YAML para despliegue de Claude Managed Agents.
2. Definición de tool policies y callable subagents para entornos gestionados.
3. Referencia de arquitectura y handoffs (`scripts/orchestrate.py`).

La app web local no invoca esos YAML directamente para ejecutar pipelines.

## 7. Decisiones de diseño (argumentario técnico)

1. Pipeline secuencial para trazabilidad completa por etapa.
2. Persistencia de cada salida para auditoría y troubleshooting.
3. Paso de model builder en Deal marcado como opcional para no bloquear flujo comercial.
4. Generación de documento sintético cuando falta información financiera para resiliencia operativa.
5. Separación estricta entre propuesta IA y validación humana previa a cliente.

## 8. Preguntas difíciles y respuesta rápida

### 8.1. “¿De dónde sale la priorización de oportunidades?”
Del `Opportunity Researcher`, alimentado por `empresas_deal` y prompt de priorización en JSON estricto.

### 8.2. “¿Por qué a veces el tono del agente no coincide con el markdown del plugin?”
Porque para `earnings-reviewer`, `meeting-prep-agent` y `pitch-agent` se usa fallback prompt al no estar esas keys en `AGENT_PROMPTS`.

### 8.3. “¿Qué parte es determinista y cuál generativa?”
En Deal, la mayor parte es generativa LLM; determinista son orquestación, selección de target, persistencia y controles de flujo.

### 8.4. “¿La carpeta managed-agent-cookbooks interviene en cada run de Flask?”
No. Es un blueprint de despliegue administrado, no el runtime ejecutado por `app.py`.

### 8.5. “¿Qué garantiza que se pueda descargar el PPTX?”
El `Pitch Builder` intenta construirlo y guarda `pptx_path`; la ruta de descarga valida existencia física antes de enviar archivo.

## 9. Riesgos y límites actuales

1. Dependencia de calidad textual de documentos financieros de entrada.
2. Uso de fallback prompt en tres agentes Deal (alineación parcial con plugin docs).
3. Selección de empresa por primera oportunidad si no hay match explícito.
4. Cobertura local de datos limitada al contenido disponible en BBDD.

## 10. Archivos de referencia para defensa completa

### Runtime aplicación
- `app.py`
- `deal_orchestrator.py`
- `src/logging_utils.py`
- `src/azure_client.py`

### Agentes Deal
- `src/agents/opportunity_researcher/agent.py`
- `src/agents/earnings_reviewer/agent.py`
- `src/agents/deal_model_builder/agent.py`
- `src/agents/meeting_preparer/agent.py`
- `src/agents/pitch_builder/agent.py`
- `src/agents/pitch_builder/pptx_builder.py`

### Loader prompts/skills
- `src/skill_loader.py`
- `plugins/agent-plugins/market-researcher/agents/market-researcher.md`
- `plugins/agent-plugins/model-builder/agents/model-builder.md`
- `plugins/agent-plugins/earnings-reviewer/agents/earnings-reviewer.md`
- `plugins/agent-plugins/meeting-prep-agent/agents/meeting-prep-agent.md`
- `plugins/agent-plugins/pitch-agent/agents/pitch-agent.md`

### Datos y UI
- `data/bbdd.json`
- `templates/deal_index.html`
- `templates/deal_run_detail.html`

### Managed cookbooks (blueprint, no runtime Flask)
- `managed-agent-cookbooks/README.md`
- `managed-agent-cookbooks/market-researcher/agent.yaml`
- `managed-agent-cookbooks/meeting-prep-agent/agent.yaml`
- `managed-agent-cookbooks/pitch-agent/agent.yaml`
