## 1. Resumen ejecutivo

Acme Componentes SL presenta un **perfil financiero sólido** en 2022–2024, con **crecimiento sostenido de ingresos y EBITDA**, mejora de márgenes y **cobertura de intereses holgada**, coherente con un comportamiento bancario sin impagos y un **rating interno A-** (fuentes: *balance_2022.txt, balance_2023.txt, balance_2024.txt*; Valuation Reviewer). El principal foco de riesgo no es financiero sino de **Cumplimiento/KYC**, dado que el **screening de sanciones/PEP/adverse media no está documentado** y existen **lagunas en identificación de UBO** (DOB/ID del UBO persona física y transparencia del UBO entidad alemana) (fuente: KYC Screener, reglas **SCREEN-01, UBO-02, UBO-03**). Adicionalmente, se requiere **reconciliar la deuda financiera neta 2024 (12,0m€)** con la exposición activa reportada en el banco (~6,5m€), lo que sugiere posible deuda en otras entidades o instrumentos no reflejados (fuente: Valuation Reviewer). Se recomienda **APROBAR CON CONDICIONES** o **ESCALAR** a Cumplimiento según política interna, condicionando la formalización a cierre de brechas KYC y a la entrega de información de deuda/plan 2025 por expansión en Polonia (fuentes: KYC Screener; Valuation Reviewer; notas internas).

---

## 2. Identificación de la empresa

- **Razón social:** Acme Componentes SL (fuente: KYC Screener; Model Builder)  
- **Forma jurídica:** **Sociedad de Responsabilidad Limitada** (fuente: *escritura_constitucion.txt*)  
- **NIF/CIF:** **B50123987** (fuente: *escritura_constitucion.txt*)  
- **Fecha de constitución:** **2003-07-10** (fuente: *escritura_constitucion.txt*)  
- **Domicilio social:** Polígono Malpica, Calle E nº 18, 50016 Zaragoza, ES (fuente: *escritura_constitucion.txt*)  
- **Jurisdicción:** España (UBO adicional con jurisdicción Alemania) (fuente: KYC Screener; Model Builder)  
- **Actividad / CNAE:** **2562 – Tratamiento y revestimiento de metales** (Sector: Industrial) (fuente: KYC Screener; Model Builder)  
- **Capital social:** **800.000 €** (fuente: KYC Screener; Model Builder)  
- **Empleados:** **310** (fuente: KYC Screener; Model Builder)  
- **Relación con el banco:** desde **2021** (Valuation Reviewer: 2021-03-15; KYC Screener: “relationship_since 2021”)  

**Administración / control (declarado):**
- **Roberto Acme Jiménez** – Consejero Delegado (fuente: *escritura_constitucion.txt*)  
- **Klaus Meier** – Consejero (representante Acme Europe) (fuente: *escritura_constitucion.txt*)  

**Titulares reales (UBO) declarados:**
- **Roberto Acme Jiménez** – 65% (persona física; base: ownership) (fuente: *escritura_constitucion.txt*)  
- **Acme Europe Holding GmbH** – 35% (entidad; jurisdicción alemana; base: ownership) (fuente: *escritura_constitucion.txt*)  

---

## 3. Hallazgos KYC (resultado de reglas y screening)

### 3.1. Inventario documental revisado
- Escritura de constitución: *escritura_constitucion.txt* (2003-07-10)  
- EEFF: *balance_2022.txt, balance_2023.txt, balance_2024.txt* (fuente: KYC Screener; Model Builder)

### 3.2. Motor de reglas KYC (KYC Screener)
- **DOC-ENTITY-01 (constitución/forma jurídica): PASS** — evidencia: *escritura_constitucion.txt*  
- **DOC-ENTITY-02 (NIF/CIF válido): PASS** — evidencia: *escritura_constitucion.txt*  
- **UBO-01 (identificar UBO ≥25% con % y base): PARTIAL** — UBOs declarados, pero con carencias posteriores (evidencia: *escritura_constitucion.txt*)  
- **UBO-02 (UBO persona física: DOB + ID): FAIL** — falta **fecha de nacimiento** y **documento identificativo** de Roberto Acme Jiménez (fuente: KYC Screener)  
- **UBO-03 (UBO entidad: transparencia hasta persona física): FAIL** — falta desglose de beneficiario final de **Acme Europe Holding GmbH (35%)** (fuente: KYC Screener)  
- **CTRL-01 (administradores/controladores): PASS** — evidencia: *escritura_constitucion.txt*  
- **ADDR-01 (prueba de domicilio reciente si aplica): PARTIAL** — domicilio en escritura, sin prueba reciente en el paquete (fuente: KYC Screener)  
- **SOF-01 (fuente de fondos): PARTIAL** — coherente con actividad y EEFF 2022–2024; falta declaración formal si política lo exige (fuente: KYC Screener)  
- **TAX-01 (formularios fiscales CRS/W-8/W-9): FAIL** — no aportados (fuente: KYC Screener)  
- **SCREEN-01 (screening sanciones/PEP/adverse media): FAIL** — **no hay resultados documentados** para entidad, UBOs y administradores (fuente: KYC Screener)

### 3.3. Screening (sanciones/PEP/adverse media)
- **Conclusión:** **NO_CONCLUYENTE** por ausencia de ejecución/documentación de screening (fuente: KYC Screener: *screening_conclusion*).  
- **Trigger de escalado:**  
  - **UBO entidad sin transparencia** (UBO-03)  
  - **Screening no realizado/documentado** (SCREEN-01)  
  (fuente: KYC Screener: *escalation_triggers*)

### 3.4. Evaluación KYC agregada
- **Recomendación KYC Screener:** **riesgo medio**, principalmente por estructura con UBO entidad no transparentada y ausencia de screening/PEP verificado (fuente: KYC Screener: *risk_assessment_recommendation*).

---

## 4. Análisis financiero (FY 2022–2024)

> Base: modelo normalizado (Model Builder) a partir de *balance_2022.txt, balance_2023.txt, balance_2024.txt*. Limitaciones: no hay detalle de CAPEX, amortizaciones, impuestos, flujo de caja, vencimientos ni composición de deuda (fuente: Valuation Reviewer: *limitations/noted_gaps*).

### 4.1. Crecimiento y rentabilidad
- **Ingresos:** 32,0m€ (2022) → 38,0m€ (2023) → 42,0m€ (2024)  
  - Crecimiento YoY: **+18,8%** (2023/2022) y **+10,5%** (2024/2023) (fuente: Model Builder; Valuation Reviewer)  
- **EBITDA:** 3,8m€ → 4,9m€ → 5,8m€  
  - Crecimiento YoY: **+28,9%** y **+18,4%** (fuente: Model Builder; Valuation Reviewer)  
- **Margen EBITDA:** **11,9%** (2022) → **12,9%** (2023) → **13,8%** (2024)  
  - Mejora acumulada ~**+190 pb** 2022–2024 (fuente: Model Builder; Valuation Reviewer)

**Lectura de riesgo:** mejora de eficiencia y capacidad de absorción de costes; desaceleración del crecimiento en 2024 vs 2023 a monitorizar (fuente: Valuation Reviewer).

### 4.2. Apalancamiento y servicio de deuda
- **Deuda financiera neta:** 8,0m€ (2022) → 10,5m€ (2023) → 12,0m€ (2024) (fuente: Model Builder)  
- **Deuda neta / EBITDA:** **2,11x** → **2,14x** → **2,07x** (estable ~2,1x) (fuente: Model Builder; Valuation Reviewer)  
- **Gastos financieros:** 0,45m€ → 0,52m€ → 0,61m€ (fuente: Model Builder)  
- **Cobertura de intereses (EBITDA / gastos financieros):** **8,44x** → **9,42x** → **9,51x** (fuente: Model Builder)

**Lectura de riesgo:** apalancamiento contenido y cobertura holgada; el incremento de deuda neta sugiere inversión/crecimiento, pero falta evidencia de generación de caja y calendario de vencimientos (fuente: Valuation Reviewer).

### 4.3. Liquidez y circulante
- **Current ratio:** **1,32** (2022) → **1,36** (2023) → **1,48** (2024) (fuente: Model Builder)  
- **Fondo de maniobra:** 2,3m€ → 3,2m€ → 4,7m€ (fuente: Model Builder)

**Lectura de riesgo:** mejora de liquidez contable; compatible con mayor actividad y uso de instrumentos de circulante (fuente: Valuation Reviewer).

### 4.4. Capitalización
- **Fondos propios:** 6,8m€ → 8,2m€ → 9,9m€ (fuente: Model Builder)

**Lectura de riesgo:** refuerzo patrimonial progresivo, mitigante ante escenarios de estrés (fuente: Model Builder; Valuation Reviewer).

---

## 5. Señales externas (noticias, litigios, cambios societarios)

- **Noticias/alertas internas registradas:** no hay noticias registradas en la base interna; esto **no equivale a ausencia de riesgo**, sino a ausencia de señales capturadas (fuente: Market Researcher).  
- **Marco de señales a verificar en fuentes públicas (mercantil/judicial/regulatorio):**
  - Depósito de cuentas y puntualidad, cambios de administradores/apoderados, modificaciones estatutarias (fuente: Market Researcher).
  - Procedimientos concursales, litigios relevantes, embargos (fuente: Market Researcher).
  - Sanciones administrativas (laborales/medioambientales/PRL) por naturaleza industrial (fuente: Market Researcher).
- **Nota operativa interna:** “**Expansión con nueva planta en Polonia en 2025**” (fuente: KYC Screener: *internal_notes.other*; Valuation Reviewer lo trata como foco de seguimiento).

---

## 6. Evaluación de riesgo (riesgos, mitigantes, comparativa con historial)

### 6.1. Riesgos identificados (principales)
- **Riesgo de Cumplimiento/KYC (medio):**
  - **Screening no documentado** para entidad/UBOs/administradores (**SCREEN-01: FAIL**) (fuente: KYC Screener).
  - **UBO incompleto**: falta DOB/ID del UBO persona física (**UBO-02: FAIL**) y falta transparencia del UBO entidad alemana (**UBO-03: FAIL**) (fuente: KYC Screener).
  - **PEP status “unknown”** por no declaración y sin verificación (fuente: Model Builder; KYC Screener).
- **Riesgo de apalancamiento/estructura de deuda (watch):**
  - Deuda neta crece a 12,0m€; aunque el ratio ND/EBITDA se mantiene, falta detalle de **deuda bruta, caja y vencimientos** (fuente: Valuation Reviewer; Model Builder).
  - **Posible desalineación** entre deuda neta del modelo (12,0m€) y operaciones activas reportadas en el banco (~6,5m€), sugiriendo deuda en otras entidades o instrumentos no reflejados (fuente: Valuation Reviewer: *potential_mismatches_or_questions*).
- **Riesgo de ejecución 2025 (medio):**
  - Expansión en Polonia 2025 no incorporada en el modelo FY 2022–2024; potencial impacto en CAPEX, circulante y covenants (fuente: KYC Screener notas internas; Valuation Reviewer).

### 6.2. Mitigantes
- **Comportamiento bancario positivo:** relación activa, **0 impagos**, incidencias menores subsanadas (fuente: Valuation Reviewer: *behavioral_summary/incidents*).
- **Fortaleza operativa-financiera:** crecimiento de ventas/EBITDA, margen al alza, **cobertura de intereses >8x**, liquidez contable mejorando (fuente: Model Builder; Valuation Reviewer).
- **Gestión de riesgo de tipos:** existencia de **cobertura de tipo de interés** con nocional ~12,0m€ (a confirmar estructura/efectividad) (fuente: Valuation Reviewer).

### 6.3. Comparativa con historial bancario
- **Coherencia global alta** entre evolución financiera y productos contratados (CAPEX/leasing/confirming) (fuente: Valuation Reviewer: *coherence_assessment*).
- **Alertas históricas menores:** retraso de 10 días en entrega de cuentas auditadas 2022; discrepancia documental puntual en poderes (subsanada) (fuente: Valuation Reviewer: *incidents*).

---

## 7. Recomendación (para decisión del analista)

**Recomendación:** **APROBAR CON CONDICIONES** (o **ESCALAR** a Cumplimiento si la política exige cierre previo de screening/UBO).  

**Racional:** el **riesgo de crédito financiero** es actualmente **moderado-bajo** por métricas sólidas y buen comportamiento (fuentes: Model Builder; Valuation Reviewer), pero el expediente presenta **brechas KYC materiales** (screening no realizado/documentado y UBO no transparentado) que deben cerrarse antes de elevar exposición o formalizar determinadas operaciones (fuente: KYC Screener: *SCREEN-01, UBO-02, UBO-03; escalation_triggers*). Además, es necesario **reconciliar deuda neta total** y evaluar el impacto del **plan 2025** para evitar un incremento de riesgo no capturado en FY 2022–2024 (fuente: Valuation Reviewer).

> La decisión final corresponde al analista humano y, en su caso, a Cumplimiento/Riesgos conforme a la política interna.

---

## 8. Condiciones y próximos pasos (si aplica)

### 8.1. Condiciones KYC/Cumplimiento (previas a formalización o incremento de límites, según política)
- **Ejecutar y documentar screening** sanciones/PEP/adverse media para:
  - Acme Componentes SL, Roberto Acme Jiménez, Acme Europe Holding GmbH, Klaus Meier  
  (fuente: KYC Screener: **SCREEN-01 FAIL**).
- **Completar identificación UBO persona física (65%)**:
  - **DNI/pasaporte** y **fecha de nacimiento** de Roberto Acme Jiménez (fuente: KYC Screener: **UBO-02 FAIL**).
- **Transparencia UBO de la entidad alemana (35%)**:
  - organigrama y/o declaración UBO y/o extracto registral hasta persona física (fuente: KYC Screener: **UBO-03 FAIL**).
- **Formularios fiscales** (CRS/autocertificación; y/o W-8/W-9 si aplica) (fuente: KYC Screener: **TAX-01 FAIL**).
- **Evidencia de domicilio actualizada** si la política exige prueba reciente (fuente: KYC Screener: **ADDR-01 PARTIAL**).
- **Declaración formal de fuente de fondos/fuente de riqueza** si requerida por política (base actual: EEFF 2022–2024) (fuente: KYC Screener: **SOF-01 PARTIAL**).

### 8.2. Condiciones de información financiera / riesgo (para cierre de análisis y/o covenants)
- **Reconciliación deuda neta 2024 (12,0m€):**
  - detalle de **deuda bruta por instrumento y entidad**, **leasing/confirming/factoring**, y **caja y equivalentes** a cierre 2024 (fuente: Valuation Reviewer: *required_follow_up*).
- **Calendario de vencimientos 2025–2029** y mapa de tipo fijo/variable (fuente: Valuation Reviewer).
- **Documentación de cobertura de tipos** (term sheet/confirmación; tipo de instrumento, vencimiento, amortización) y % de deuda cubierta (fuente: Valuation Reviewer).
- **Plan 2025–2027 por expansión en Polonia**:
  - presupuesto (ventas/margen), CAPEX, necesidades de circulante y plan de financiación; sensibilidad de ramp-up (fuente: Valuation Reviewer; nota interna KYC).

### 8.3. Sugerencia de covenants / seguimiento (si se aprueba)
- **Covenant de información:** entrega de EEFF auditados dentro de un plazo definido (p.ej., X días tras cierre), dado el antecedente de retraso (fuente: Valuation Reviewer: *incidents*).
- **Covenant de apalancamiento (orientativo):** mantener **Deuda neta/EBITDA** en torno a niveles actuales (~2,1x) con umbral a definir por política y estructura final (base: Model Builder; Valuation Reviewer).
- **Revisión anual KYC reforzada** hasta cierre de transparencia del UBO entidad y estabilización de screening/documentación (fuente: KYC Screener: *escalation_triggers*).