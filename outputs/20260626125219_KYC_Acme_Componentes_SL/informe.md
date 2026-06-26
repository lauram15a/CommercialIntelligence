## 1) Resumen ejecutivo
Acme Componentes SL presenta un desempeño financiero **sólido y en mejora** en 2022–2024 (crecimiento de ingresos y EBITDA, margen al alza, cobertura de intereses elevada) y un **historial bancario limpio** (0 impagos; operaciones vigentes al corriente), consistente con un perfil interno **A-**. No obstante, existen **gaps KYC materiales**: **screening de sanciones/PEP/adverse media no documentado**, **UBO individual sin identificación/DOB**, y **UBO corporativo extranjero (Alemania) sin documentación registral ni transparencia aguas arriba**, además de **origen de fondos** y **formularios fiscales** no aportados. En señales externas, **no se han recibido fuentes verificables** (BORME/Registro Mercantil/prensa/litigios), por lo que el riesgo reputacional/legal externo queda **no evaluado** con evidencia. Recomendación técnica: **APROBAR CON CONDICIONES** (cierre previo de KYC crítico y reconciliación de deuda neta), dejando la decisión final al analista humano.  
**Nivel de riesgo consolidado propuesto:** **Medio** (por KYC/data gaps), con **riesgo crediticio financiero bajo–medio** (por métricas y comportamiento).

---

## 2) Identificación de la empresa
- **Razón social:** Acme Componentes SL  
- **Forma jurídica:** **Sociedad de Responsabilidad Limitada**  
- **NIF:** **B50123987**  
- **Jurisdicción:** **España**  
- **Domicilio social:** Polígono Malpica, Calle E nº 18, 50016 Zaragoza (ES)  
- **Fecha de constitución:** 2003-07-10  
- **Actividad / CNAE:** **2562 – Tratamiento y revestimiento de metales** (sector Industrial)  
- **Capital social:** 800.000 EUR  
- **Empleados:** 310  
**Fuente:** KYC Screener → `extracted_entities.applicant` (evidencia: `escritura_constitucion.txt` para datos registrales).

**Administración / control (declarado):**
- **Roberto Acme Jiménez** — Consejero Delegado  
- **Klaus Meier** — Consejero (representante Acme Europe)  
**Fuente:** KYC Screener → `extracted_entities.controllers`.

**Titulares reales (UBO ≥25%):**
- **Roberto Acme Jiménez** — 65% (persona física; base: propiedad)  
- **Acme Europe Holding GmbH** — 35% (persona jurídica; jurisdicción: Alemania; base: propiedad)  
**Fuente:** KYC Screener → `extracted_entities.beneficial_owners` (evidencia: `escritura_constitucion.txt`).

---

## 3) Hallazgos KYC (resultado de reglas y screening)
### 3.1 Resultado por regla (rules engine)
- **R-ENT-01 (Identificación/verificación entidad): PASS**  
  - Evidencia: `escritura_constitucion.txt` con nombre, NIF, forma jurídica, domicilio, fecha constitución.  
  - **Fuente:** KYC Screener → `kyc_results.rules_engine.rule_outcomes`.

- **R-UBO-01 (Identificar UBOs ≥25%): PASS**  
  - Evidencia: UBOs listados con 65% y 35% en `escritura_constitucion.txt`.  
  - **Fuente:** KYC Screener.

- **R-UBO-02 (Verificar UBO persona física): FAIL — ALERTA ALTA**  
  - Falta **DOB** y **documento de identidad** de Roberto Acme Jiménez.  
  - **Fuente:** KYC Screener → `rule_outcomes` + Model Builder → `data_gaps`.

- **R-UBO-03 (UBO corporativo: registro/estructura): FAIL — ALERTA ALTA**  
  - Acme Europe Holding GmbH sin **nº registro**, **domicilio**, ni documentación registral; sin transparencia de propiedad aguas arriba.  
  - **Fuente:** KYC Screener → `rule_outcomes` y `escalation_flags`.

- **R-CTRL-01 (Verificar controladores): FAIL — ALERTA**  
  - Controladores listados sin documentación de identidad (Roberto Acme Jiménez, Klaus Meier).  
  - **Fuente:** KYC Screener → `rule_outcomes`.

- **R-SCREEN-01 (Screening sanciones/PEP/adverse media): FAIL — ALERTA ALTA**  
  - El expediente solo indica “Sin alertas registradas” en notas internas, pero **no hay reporte verificable** (fecha, listas consultadas, parámetros, resultado).  
  - **Fuente:** KYC Screener → `rule_outcomes` y `screening_results.note`.

- **R-SOF-01 (Origen de fondos/origen de riqueza): FAIL — ALERTA**  
  - No hay declaración ni evidencia de **SoF/SoW**; balances no sustituyen SoF.  
  - **Fuente:** KYC Screener → `rule_outcomes`.

- **R-TAX-01 (Formularios fiscales CRS/FATCA/autocertificación): FAIL**  
  - No se aportan formularios fiscales aplicables.  
  - **Fuente:** KYC Screener → `rule_outcomes`.

- **R-ADDR-01 (Verificación domicilio): N/A**  
  - Domicilio consta en escritura, pero no se aporta evidencia adicional ni política aplicable en el expediente.  
  - **Fuente:** KYC Screener → `rule_outcomes`.

### 3.2 Screening (sanciones/PEP/adverse media)
- **Estado:** **NO CONCLUYENTE / no documentado** (no ejecutado con evidencia en este expediente).  
- **Partes a cribar:** Acme Componentes SL; Roberto Acme Jiménez; Klaus Meier; Acme Europe Holding GmbH.  
**Fuente:** KYC Screener → `kyc_results.screening_results` (status `not_performed_in_this_run`).

### 3.3 Flags de escalado KYC
- **Gap severidad alta:** UBO corporativo extranjero sin documentación ni transparencia aguas arriba.  
- **Gap severidad alta:** Screening no documentado para entidad/partes relacionadas.  
- **Gap severidad media:** Origen de fondos no documentado.  
**Fuente:** KYC Screener → `kyc_results.rules_engine.escalation_flags`.

---

## 4) Análisis financiero (ratios clave y tendencias)
**Fuente financiera:** “Sistemas contables del banco (datos remitidos por la empresa y validados internamente)” para 2022–2024.  
**Fuente:** KYC Screener → `extracted_entities.financials` y Model Builder → `financials_normalized`.

### 4.1 Evolución de resultados
- **Ingresos:** 32,0m (2022) → 38,0m (2023) → 42,0m (2024)  
  - Crecimiento YoY: **+18,8%** (2023) y **+10,5%** (2024)  
  - CAGR 2022–2024: **~14,6%**  
- **EBITDA:** 3,8m → 4,9m → 5,8m  
  - Crecimiento YoY: **+28,9%** y **+18,4%**  
  - CAGR 2022–2024: **~23,5%**  
- **Margen EBITDA:** **11,9% → 12,9% → 13,8%** (mejora sostenida)  
**Fuente:** Model Builder → `derived_metrics` y `yoy`; Valuation Reviewer → `trend_analysis`.

### 4.2 Apalancamiento, cobertura y liquidez
- **Deuda financiera neta (NFD):** 8,0m → 10,5m → 12,0m  
- **NFD/EBITDA:** **2,11x → 2,14x → 2,07x** (estable; nivel aceptable)  
- **Gastos financieros:** 0,45m → 0,52m → 0,61m (al alza)  
- **Cobertura de intereses (EBITDA/financieros):** **8,44x → 9,42x → 9,51x** (fuerte)  
- **Liquidez (Current ratio):** **1,32x → 1,36x → 1,48x** (mejora)  
**Fuente:** Model Builder → `derived_metrics`; Valuation Reviewer → `metrics_by_year`.

### 4.3 Observaciones de calidad/reconciliación
- **Reconciliación de deuda neta requerida (ALERTA DE CONTROL):** la NFD contable 2024 (12,0m) **no se concilia** con el detalle de deuda bancaria visible (p.ej., préstamo corporativo 5,2m + circulante dispuesto 1,3m) sin incorporar CAPEX, leasing, otras entidades, caja y derivados.  
**Fuente:** Valuation Reviewer → `reconciliation_points.net_debt_bridge_needed`.

---

## 5) Señales externas (noticias, litigios, cambios societarios)
- **Estado de evidencias externas:** no se han aportado ni constan en el extracto recibido **fuentes externas verificables** (BORME/Registro Mercantil, BOE, prensa, litigios, sanciones administrativas, ratings, etc.).  
- En consecuencia, el riesgo reputacional/legal externo queda **no evaluado con evidencia** en este informe y debe completarse antes de una decisión definitiva si la política lo exige.  
**Fuente:** Market Researcher → sección “Disponibilidad de señales externas” (y evidencia KYC Screener → `evidencias` id `MKT-001`).

---

## 6) Evaluación de riesgo (riesgos, mitigantes, comparativa con historial)
### 6.1 Riesgos identificados
**Riesgo KYC/AML (material) — severidad media/alta**
- **UBO corporativo extranjero (DE) sin documentación registral ni UBOs aguas arriba** → riesgo de opacidad de propiedad/control.  
  **Fuente:** KYC Screener → `R-UBO-03 fail` + `escalation_flags (high)`.
- **Screening no documentado** para entidad/UBOs/controladores → riesgo de incumplimiento procedimental y de exposición a sanciones/PEP/adverse media no detectada.  
  **Fuente:** KYC Screener → `R-SCREEN-01 fail` + `screening_results.note`.
- **Identificación incompleta** de UBO/controladores (IDs/DOB) y **SoF/SoW** no documentado.  
  **Fuente:** KYC Screener → `R-UBO-02 fail`, `R-CTRL-01 fail`, `R-SOF-01 fail`.

**Riesgo financiero (moderado, controlado)**
- **Deuda neta en aumento nominal** (8,0m → 12,0m) aunque apalancamiento estable por crecimiento de EBITDA.  
  **Fuente:** Model Builder/Valuation Reviewer.
- **Gastos financieros al alza**; aunque la cobertura mejora, conviene separar intereses vs comisiones/coberturas.  
  **Fuente:** Valuation Reviewer → `interest_expense_vs_debt`.

**Riesgo de ejecución/expansión**
- Nota interna de **expansión con nueva planta en Polonia en 2025**: potencial incremento de CAPEX y circulante; riesgo de ramp-up.  
  **Fuente:** KYC Screener → `bank_internal_notes.observations`; Valuation Reviewer → `operational_notes`.

**Riesgo reputacional/legal externo (no cuantificado por falta de evidencia)**
- Sin fuentes externas aportadas, no se puede confirmar ausencia/presencia de litigios, sanciones administrativas o incidencias registrales.  
  **Fuente:** Market Researcher.

### 6.2 Mitigantes
- **Historial bancario positivo:** 0 impagos; operaciones vigentes al corriente; incidencias documentales menores resueltas.  
  **Fuente:** Valuation Reviewer → `banking_history_review`.
- **Métricas de servicio de deuda fuertes:** cobertura de intereses ~9,5x (2024) y apalancamiento ~2,1x.  
  **Fuente:** Model Builder/Valuation Reviewer.
- **Mejora de liquidez y margen:** current ratio 1,48x (2024) y margen EBITDA 13,8%.  
  **Fuente:** Model Builder.

### 6.3 Comparativa con historial / rating interno
- **Rating interno:** **A-**; tendencia financiera 2022–2024 y comportamiento de pago **consistentes** con dicho perfil.  
- La principal desviación frente a un perfil A- es **procedimental/KYC** (gaps de identificación, screening y SoF) y la **reconciliación de deuda neta**.  
**Fuente:** Valuation Reviewer → `entity.internal_rating` y `comparison_summary.key_takeaways`.

---

## 7) Recomendación (para decisión del analista)
**Recomendación:** **APROBAR CON CONDICIONES** (condiciones suspensivas de cumplimiento y control), dado que:
- El **riesgo crediticio financiero** es razonable (crecimiento, margen, cobertura, historial sin impagos). **Fuente:** Model Builder + Valuation Reviewer.
- Pero existen **alertas KYC altas** (screening no documentado; UBO corporativo extranjero sin soporte; IDs/DOB faltantes; SoF y fiscalidad no aportadas) que deben cerrarse para cumplir política AML/KYC. **Fuente:** KYC Screener + Valuation Reviewer.

> La decisión final corresponde al analista humano y a Cumplimiento, especialmente por los gaps KYC de severidad alta.

---

## 8) Condiciones y próximos pasos
### 8.1 Condiciones KYC/Compliance (previas a formalización o a incremento de riesgo, según política)
- **Completar verificación UBO persona física (Roberto Acme Jiménez, 65%)**: DNI/NIE/pasaporte vigente + **fecha de nacimiento**.  
  **Fuente:** KYC Screener → `missing_documents` + `R-UBO-02 fail`.
- **Completar UBO corporativo (Acme Europe Holding GmbH, 35%)**: extracto registral alemán (HRB), nº registro, domicilio, representantes y **organigrama hasta UBO final** (transparencia aguas arriba).  
  **Fuente:** KYC Screener → `R-UBO-03 fail` + `escalation_flags (high)`.
- **Identificación de controladores**: ID vigente de Klaus Meier y, si aplica por política, verificación reforzada.  
  **Fuente:** KYC Screener → `R-CTRL-01 fail`.
- **Ejecutar y archivar screening** (UE/OFAC/ONU/UK + PEP + adverse media) para entidad/UBOs/controladores, con evidencia (fecha, listas, parámetros, resultado).  
  **Fuente:** KYC Screener → `R-SCREEN-01 fail` + `screening_results.note`.
- **Origen de fondos/origen de riqueza (SoF/SoW)**: declaración firmada y evidencia proporcional (p.ej., explicación de flujos operativos, contratos/facturación, estados bancarios, dividendos, etc.).  
  **Fuente:** KYC Screener → `R-SOF-01 fail`.
- **Formularios fiscales** (CRS/FATCA/autocertificación) según aplicabilidad.  
  **Fuente:** KYC Screener → `R-TAX-01 fail`.

### 8.2 Condiciones financieras / información adicional
- **Bridge de deuda neta 2024 y 2025 YTD**: detalle por instrumento (banco y otros), leasing (IFRS16 si aplica), caja, derivados/coberturas (MTM) y calendario de amortización/covenants.  
  **Fuente:** Valuation Reviewer → `reconciliation_points.net_debt_bridge_needed`.
- **Reporting 2025 YTD + presupuesto/plan de la planta en Polonia** para estimar impacto en apalancamiento, liquidez y necesidades de circulante.  
  **Fuente:** Valuation Reviewer → `reviewer_conclusion.recommended_next_steps` + notas internas.

### 8.3 Señales externas (para cerrar gap reputacional/legal)
- Solicitar/autorizar consulta y anexar evidencias de: **Registro Mercantil/BORME**, litigios públicos, sanciones administrativas y prensa relevante (con fechas y enlaces/capturas).  
  **Fuente:** Market Researcher → “Disponibilidad de señales externas / checklist”.

--- 

**Anexos de trazabilidad (inputs utilizados):**
- KYC Screener Agent: `escritura_constitucion.txt`, reglas R-ENT/R-UBO/R-CTRL/R-SCREEN/R-SOF/R-TAX, inventario documental y flags.  
- Model Builder Agent: estados normalizados 2022–2024 y ratios derivados.  
- Valuation Reviewer Agent: rating interno A-, historial bancario, productos activos, reconciliación NFD y conclusiones.  
- Market Researcher Agent: declaración de ausencia de fuentes externas verificables en el extracto recibido.