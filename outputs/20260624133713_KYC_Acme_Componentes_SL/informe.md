## 1. Resumen ejecutivo

Acme Componentes SL presenta un desempeño financiero **positivo** en 2022–2024, con **crecimiento de ingresos**, **expansión de margen EBITDA** y **apalancamiento moderado** (ND/EBITDA ~2,1x) con **cobertura de intereses holgada** (>8x). El historial con el banco es **favorable** (sin impagos; operaciones vigentes al corriente), coherente con el perfil financiero observado. No obstante, existen **brechas KYC materiales** y un resultado de screening **NO CONCLUYENTE**: **no se ha realizado/documentado screening de sanciones/PEP/adverse media** y falta transparencia/soporte del **UBO entidad** (Acme Europe Holding GmbH), además de documentación de poderes y fiscalidad. En consecuencia, el nivel de riesgo consolidado se considera **MEDIO**, con necesidad de **condicionar** cualquier avance crediticio a la regularización KYC y a completar información de caja/deuda para evaluar capacidad de repago.

**Fuentes:** KYC Screener Agent (rules_engine, required_document_check, screening_conclusion, internal_notes); Model Builder Agent (métricas 2022–2024); Valuation Reviewer Agent (conclusiones, gaps, historial bancario); Market Researcher Agent (ausencia de señales internas registradas).

---

## 2. Identificación de la empresa

- **Razón social:** Acme Componentes SL  
- **Forma jurídica:** **Sociedad de Responsabilidad Limitada**  
- **NIF/CIF:** **B50123987**  
- **Fecha de constitución:** 2003-07-10  
- **Jurisdicción:** España  
- **Domicilio social:** Polígono Malpica, Calle E nº 18, 50016 Zaragoza  
- **Actividad / CNAE:** **2562 – Tratamiento y revestimiento de metales** (Sector industrial)  
- **Capital social:** 800.000 EUR  
- **Empleados:** 310  

**Administración / control (declarado):**
- **Roberto Acme Jiménez** — **Consejero Delegado**
- **Klaus Meier** — **Consejero** (representante Acme Europe)

**Titulares reales (UBO) declarados:**
- **Roberto Acme Jiménez** — 65% (base: propiedad)
- **Acme Europe Holding GmbH** (Alemania) — 35% (base: propiedad)

**Fuentes:** KYC Screener Agent (`extracted_entities.applicant`, `controllers`, `beneficial_owners`, `addresses`).

---

## 3. Hallazgos KYC (resultado de reglas y alertas)

### 3.1 Resultado del motor de reglas KYC
- **Recomendación de rating KYC:** **medium**  
- **Disposición recomendada:** **request-docs**  
- **Triggers de escalado:**  
  - **Screening no realizado/documentado** (**KYC-SCR-01**)  
  - **UBO entidad sin transparencia hasta beneficiario final** (**KYC-UBO-03**)  

**Fuentes:** KYC Screener Agent (`kyc_results.rules_engine.risk_rating_recommendation`, `disposition_recommendation`, `escalation_triggers`).

### 3.2 Cumplimiento por regla (trazabilidad)
- **KYC-ENT-01 (Nombre legal y NIF/CIF):** **PASS** — evidencia: escritura_constitucion.txt (NIF/CIF B50123987)  
- **KYC-ENT-02 (Domicilio social):** **PASS** — evidencia: escritura_constitucion.txt (domicilio Zaragoza)  
- **KYC-UBO-01 (Identificar UBOs con % y base):** **PASS_PARTIAL** — UBOs listados con %; base implícita por propiedad  
- **KYC-UBO-02 (Verificar UBO individual con ID y DOB):** **FAIL** — **no consta ID ni fecha de nacimiento** de Roberto Acme Jiménez  
- **KYC-UBO-03 (UBO entidad: doc corporativa + UBO final):** **FAIL** — Acme Europe Holding GmbH sin documentación ni UBO final  
- **KYC-CTRL-01 (Controladores y autoridad de firma):** **FAIL** — administradores listados sin poderes/acta/mandato ni verificación  
- **KYC-SOF-01 (Fuente de fondos/riqueza):** **FAIL_PARTIAL** — hay balances 2022–2024, pero falta declaración formal SoF/SoW  
- **KYC-SCR-01 (Screening sanciones/PEP/adverse media):** **FAIL** — **no hay resultados de screening** (solo “sin alertas en BBDD del banco”)  
- **KYC-TAX-01 (CRS/FATCA y formularios fiscales):** **FAIL** — no consta documentación fiscal  

**Fuentes:** KYC Screener Agent (`kyc_results.rules_engine.rule_outcomes`, `required_document_check`, `internal_notes.bank_db_alerts`).

### 3.3 Documentación faltante (resumen)
- **ID + DOB** del UBO individual (Roberto Acme Jiménez)  
- Documentación corporativa de **Acme Europe Holding GmbH** + determinación de **UBO(s) final(es)**  
- **Poderes/acta** de nombramiento y **autorización de firma** de administradores/representantes  
- **Prueba de domicilio** de la entidad (≤ 3 meses)  
- Formulario KYC: **propósito** de la relación, actividad detallada, volumen esperado  
- Declaración de **Fuente de fondos/riqueza** + soporte  
- **CRS/FATCA** (y formularios aplicables)  
- **Resultados de screening** sanciones/PEP/adverse media (entidad, UBOs y administradores)

**Fuentes:** KYC Screener Agent (`missing_documents_summary`).

---

## 4. Análisis financiero (evolución de ratios clave)

> Nota de alcance: el modelo está construido con datos de ingresos, EBITDA, gastos financieros, activo/pasivo corriente, patrimonio neto y deuda financiera neta. **No** hay estado de flujos, CAPEX, caja ni deuda bruta, lo que limita el análisis de repago por caja y estructura de deuda.  
**Fuentes:** Model Builder Agent (`data_quality.missing_fields`); Valuation Reviewer Agent (`data_gaps_and_limitations`).

### 4.1 Crecimiento y rentabilidad
- **Ingresos:** 32,0M (2022) → 38,0M (2023) → 42,0M (2024)  
  - Crecimiento YoY: **+18,8% (2023)**; **+10,5% (2024)** (desaceleración)  
- **EBITDA:** 3,8M → 4,9M → 5,8M  
  - Crecimiento YoY: **+28,9% (2023)**; **+18,4% (2024)**  
- **Margen EBITDA:** **11,9% (2022)** → **12,9% (2023)** → **13,8% (2024)** (mejora ~+1,93 pp 2022–2024)

**Fuentes:** Model Builder Agent (`periods[].income_statement`, `derived_metrics`); Valuation Reviewer Agent (`trend_summary`).

### 4.2 Liquidez (proxy)
- **Current ratio:** **1,32x (2022)** → **1,36x (2023)** → **1,48x (2024)**  
- **Fondo de maniobra (proxy = Activo corriente – Pasivo corriente):** 2,3M → 3,2M → 4,7M (mejora del colchón de circulante)

**Fuentes:** Model Builder Agent (`derived_metrics.current_ratio`, balance); Valuation Reviewer Agent (`trend_summary.liquidity`).

### 4.3 Apalancamiento y servicio de deuda (aprox.)
- **Deuda financiera neta:** 8,0M → 10,5M → 12,0M (incremento asociado a crecimiento/CAPEX según revisión)  
- **ND/EBITDA:** **2,11x (2022)** → **2,14x (2023)** → **2,07x (2024)** (estable, ligera mejora en 2024)  
- **Cobertura de intereses (EBITDA/gastos financieros):** **8,44x** → **9,42x** → **9,51x** (holgada)  
- **Coste implícito aprox. (gastos financieros / deuda neta):** ~5,0%–5,6% (aproximación; puede distorsionarse por uso de deuda neta)

**Fuentes:** Model Builder Agent (`derived_metrics.net_debt_to_ebitda`, `interest_coverage_ebitda`); Valuation Reviewer Agent (`trend_summary.leverage_and_debt_service`).

---

## 5. Señales externas (noticias, litigios, cambios societarios)

- **Base interna de señales/noticias:** **sin registros** para Acme Componentes SL; no se observan “red flags” documentadas desde esa fuente.  
- **Limitación relevante:** la ausencia de registros internos **no equivale** a ausencia de riesgo; se requiere completar con barrido externo (prensa, litigios, sanciones, insolvencias, BORME/Registro Mercantil, etc.).  
- **Screening sanciones/PEP/adverse media:** **NO CONCLUYENTE / no realizado en este análisis** (pendiente para entidad y partes vinculadas: Acme Componentes SL, Roberto Acme Jiménez, Acme Europe Holding GmbH, Klaus Meier).

**Fuentes:** Market Researcher Agent (resumen); KYC Screener Agent (`screening.status`, `screening_conclusion`, `parties_to_screen`).

---

## 6. Evaluación de riesgo (riesgos, mitigantes, comparativa con historial)

### 6.1 Riesgos identificados
- **Riesgo de Cumplimiento/KYC (material):**  
  - **Falta de screening** sanciones/PEP/adverse media (**KYC-SCR-01 FAIL**) → riesgo de exposición a sanciones/reputacional no evaluado.  
  - **UBO entidad (35%) sin documentación ni UBO final** (**KYC-UBO-03 FAIL**) → riesgo de opacidad en estructura de propiedad.  
  - **Poderes/autoridad de firma no verificados** (**KYC-CTRL-01 FAIL**) → riesgo operativo/contractual.  
  - **SoF/SoW no formalizada** (**KYC-SOF-01 FAIL_PARTIAL**) y **CRS/FATCA ausente** (**KYC-TAX-01 FAIL**).  
  **Fuentes:** KYC Screener Agent (`rule_outcomes`, `missing_documents_summary`, `escalation_triggers`).

- **Riesgo de información financiera (calidad/alcance):**  
  - Falta de **caja**, **deuda bruta**, **CAPEX** y **cash flow** → no se puede estimar **DSCR** ni validar conversión de EBITDA a caja; tampoco evaluar estructura de vencimientos/garantías.  
  **Fuentes:** Model Builder Agent (`data_quality.missing_fields`); Valuation Reviewer Agent (`data_gaps_and_limitations.impact`).

- **Riesgo de crecimiento / normalización de demanda (bajo-medio):**  
  - Desaceleración de crecimiento de ingresos en 2024 vs 2023 (18,8% → 10,5%); requiere seguimiento para descartar pérdida de demanda o presión competitiva.  
  **Fuentes:** Valuation Reviewer Agent (`trend_summary.revenue.commentary`, `risk_flags_and_monitoring_points.flags`).

- **Riesgo de refinanciación (a confirmar):**  
  - Nota interna: “**Revisar vencimientos de deuda 2027 y necesidad de refinanciación parcial**.” Sin calendario de deuda no es evaluable en esta fase.  
  **Fuentes:** KYC Screener Agent (`internal_notes.analyst_note`); Valuation Reviewer Agent (gap de vencimientos).

### 6.2 Mitigantes / factores positivos
- **Evolución financiera favorable:** crecimiento y mejora de margen; apalancamiento estable ~2,1x y cobertura de intereses >8x.  
  **Fuentes:** Model Builder Agent (ratios); Valuation Reviewer Agent (trend_summary).

- **Historial bancario positivo:** relación desde 2022, **0 impagos**, operaciones recurrentes y vigentes al corriente (CAPEX, leasing, confirming, cobertura de tipos).  
  **Fuentes:** Valuation Reviewer Agent (`banking_history_review`).

- **Gestión de riesgo de tipos:** existencia de **cobertura de tipo de interés** (notional 12,0M) consistente con perfil de deuda relevante (pendiente evaluar términos/efectividad).  
  **Fuentes:** Valuation Reviewer Agent (`products_and_operations` y `potential_mismatches_or_questions`).

### 6.3 Comparativa con historial (coherencia)
- El aumento de deuda neta 2022–2024 es **coherente** con préstamo CAPEX (2023) y leasing (2023), y con herramientas de circulante/confirming (2024).  
- Comportamiento de pago sin incidencias es consistente con ratios de apalancamiento moderado y cobertura holgada.

**Fuentes:** Valuation Reviewer Agent (`comparison_model_vs_banking_history.alignment`, `banking_history_review`).

---

## 7. Recomendación (para decisión del analista)

**Recomendación:** **ESCALAR** (a Cumplimiento/KYC) y, en paralelo, **APROBAR CON CONDICIONES** *solo si* se completa satisfactoriamente el paquete KYC y la información financiera mínima para repago.

**Racional (trazable):**
- **Condición necesaria previa:** el expediente KYC presenta **fallos** en reglas críticas (screening, UBO entidad, poderes) y screening **NO CONCLUYENTE**, lo que impide una conclusión de cumplimiento.  
  **Fuente:** KYC Screener Agent (`rule_outcomes`, `screening_conclusion`, `escalation_triggers`).
- **Capacidad financiera preliminar:** métricas 2022–2024 soportan un perfil de riesgo operativo razonable (margen al alza, ND/EBITDA ~2,1x, cobertura >8x) y el historial bancario es positivo.  
  **Fuentes:** Model Builder Agent; Valuation Reviewer Agent.

> La decisión final corresponde al analista humano y queda supeditada a la validación de Cumplimiento y a la completitud de información financiera.

---

## 8. Condiciones y próximos pasos (si aplica)

### 8.1 Condiciones KYC/Cumplimiento (previas a disposición)
- **Completar screening** sanciones/PEP/adverse media para: **Acme Componentes SL, Roberto Acme Jiménez, Acme Europe Holding GmbH, Klaus Meier**, con evidencia archivada.  
  **Fuente:** KYC Screener Agent (`KYC-SCR-01 fail`, `parties_to_screen`).
- Aportar **ID + DOB** del UBO individual (Roberto Acme Jiménez).  
  **Fuente:** KYC Screener Agent (`KYC-UBO-02 fail`).
- Aportar documentación corporativa de **Acme Europe Holding GmbH** y determinar **UBO(s) final(es)** (cadena de titularidad).  
  **Fuente:** KYC Screener Agent (`KYC-UBO-03 fail`).
- Aportar **poderes/acta** y verificación de **autoridad de firma** de administradores/representantes.  
  **Fuente:** KYC Screener Agent (`KYC-CTRL-01 fail`).
- Aportar **prueba de domicilio** (≤ 3 meses), **CRS/FATCA** y formulario KYC de propósito/volúmenes esperados.  
  **Fuente:** KYC Screener Agent (`missing_documents_summary`).

### 8.2 Información financiera mínima adicional (para cierre de análisis de crédito)
- **Caja y equivalentes** y **deuda bruta** por instrumento; conciliación con **gastos financieros** (intereses vs comisiones).  
- **Calendario de vencimientos** (incl. foco 2027) y condiciones (tipo fijo/variable, covenants, garantías).  
- **CAPEX 2022–2024** y **plan 2025** (incl. expansión/planta en Polonia mencionada internamente) y **cash flow operativo / FCF**.  
- Detalle de **circulante** (clientes, inventario, proveedores) para validar consumo/generación de caja.

**Fuentes:** Valuation Reviewer Agent (`data_gaps_and_limitations`, `potential_mismatches_or_questions`); KYC Screener Agent (`internal_notes.observations`, `internal_notes.analyst_note`).

### 8.3 KPIs de seguimiento recomendados
- **Net Debt / EBITDA**, **Interest coverage**, **EBITDA margin**, **Current ratio** y evolución de circulante neto  
- **CAPEX y FCF** (cuando se disponga)  
- **Cumplimiento de reporting** (timeliness de auditadas y paquetes periódicos)

**Fuente:** Valuation Reviewer Agent (`monitoring_kpis_recommended`).