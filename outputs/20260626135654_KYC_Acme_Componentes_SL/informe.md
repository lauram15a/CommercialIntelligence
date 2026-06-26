## 1) Resumen ejecutivo

Acme Componentes SL presenta un perfil **financiero sólido** con **crecimiento sostenido** (ingresos 2022–2024 CAGR ~**14,6%**) y mejora de rentabilidad (margen EBITDA **11,9% → 13,8%**), manteniendo un apalancamiento estable (**ND/EBITDA ~2,1x**) y **cobertura de intereses holgada** (~**9,5x** en 2024) (fuente: *balance_2022.txt, balance_2023.txt, balance_2024.txt; Model Builder*). El comportamiento bancario histórico es **positivo** (0 impagos; operaciones al corriente), con incidencias documentales menores ya cerradas (fuente: *Valuation Reviewer*).  
No obstante, el expediente presenta **alertas KYC relevantes**: **cadena UBO incompleta** para el socio corporativo (**Acme Europe Holding GmbH 35%**), **ausencia de verificación de identidad** de administradores/UBO PF, **sin prueba de domicilio**, **sin formularios fiscales**, **sin SoF/SoW** y **screening PEP/sanciones no concluyente** por falta de resultados en el expediente (fuente: *KYC Screener*). En señales externas, se observa **expansión con CAPEX** (planta en Polonia, inversión **€9m**) y **concentración comercial** en automoción alemana con contratos hasta 2027, lo que incrementa complejidad operativa y riesgo de ejecución (fuente: *Market Researcher: Expansión 2025-05-15; El Economista 2025-12-01*).  
**Nivel de riesgo propuesto:** **medio** (financiero verde-amarillo; calidad de datos amarillo; KYC con gaps materiales) (fuente: *Valuation Reviewer; KYC Screener*).

---

## 2) Identificación de la empresa

- **Razón social:** **Acme Componentes SL** (fuente: *escritura_constitucion.txt; KYC Screener extracted_entities*).  
- **NIF/CIF:** **B50123987** (fuente: *Model Builder normalized_financials.entity.identifier; Valuation Reviewer*).  
- **Jurisdicción:** **España (ES)** (fuente: *Model Builder*).  
- **Segmento bancario:** **Corporate Industrial** (fuente: *Valuation Reviewer*).  
- **Cliente desde:** **2021-03-15** (fuente: *Valuation Reviewer*).  
- **Administración / control (roles):**
  - **Roberto Acme Jiménez** – **Consejero Delegado** (fuente: *escritura_constitucion.txt; KYC Screener R-CTRL-01*).
  - **Klaus Meier** – **Consejero** (fuente: *escritura_constitucion.txt; KYC Screener R-CTRL-01*).
- **Titulares reales (UBO) declarados:**
  - **Roberto Acme Jiménez** – **65%** (nacionalidad española indicada) (fuente: *escritura_constitucion.txt; KYC Screener R-OWN-01; extracted_entities*).
  - **Acme Europe Holding GmbH** – **35%** (sociedad alemana) (fuente: *escritura_constitucion.txt; KYC Screener R-OWN-01; extracted_entities*).

---

## 3) Hallazgos KYC (resultado por regla y alertas)

**Resultado global KYC:** expediente **no apto para cierre KYC** sin subsanaciones (por fallos en UBO corporativo, ID, domicilio, fiscalidad, SoF/SoW y PEP/sanciones) (fuente: *KYC Screener kyc_results*).

- **R-ENT-01 Identificación completa entidad:** **PASS** (fuente: *escritura_constitucion.txt; KYC Screener*).
- **R-OWN-01 Declaración UBO con %:** **PASS** (fuente: *escritura_constitucion.txt; KYC Screener*).
- **R-OWN-02 Cadena de titularidad UBO corporativo:** **FAIL**  
  - **Alerta:** falta identificar beneficiario(s) final(es) de **Acme Europe Holding GmbH (35%)** o justificar exención (fuente: *KYC Screener R-OWN-02*).
- **R-CTRL-01 Administradores/controladores:** **PASS** (fuente: *escritura_constitucion.txt; KYC Screener*).
- **R-ID-01 Verificación identidad administradores/UBO PF:** **FAIL**  
  - **Alerta:** no constan documentos de identidad vigentes en el expediente (fuente: *KYC Screener R-ID-01*).
- **R-ADDR-01 Verificación domicilio:** **FAIL**  
  - **Alerta:** no consta prueba de domicilio; solo domicilio declarado en escritura (fuente: *KYC Screener R-ADDR-01*).
- **R-TAX-01 Formularios fiscales (CRS/FATCA u otros):** **FAIL** (fuente: *KYC Screener R-TAX-01*).
- **R-SOF-01 Fuente de fondos/riqueza y propósito:** **FAIL**  
  - **Alerta:** balances aportan contexto, pero falta declaración/soporte explícito de **SoF/SoW** y propósito de relación (fuente: *KYC Screener R-SOF-01*).
- **R-FIN-01 Información financiera reciente:** **PASS** (fuente: *balance_2022.txt, balance_2023.txt, balance_2024.txt; KYC Screener*).
- **R-PEP-01 Declaración PEP y screening PEP/sanciones:** **FAIL**  
  - **Alerta:** no consta declaración PEP ni resultados de screening; **screening_conclusion = NO_CONCLUYENTE** (fuente: *KYC Screener R-PEP-01; screening_conclusion*).

**Screening:** sin entidades revisadas en el expediente; por tanto **no concluyente** y requiere ejecución/validación manual por Cumplimiento (fuente: *KYC Screener screening_resumen; screening_conclusion*).

---

## 4) Análisis financiero (ratios clave y tendencias)

**Base de datos:** estados 2022–2024 con partidas parciales (sin total activos, caja, deuda bruta, resultado neto, impuestos, capex ni flujos), por lo que el análisis se centra en márgenes, liquidez corriente y apalancamiento neto reportado (fuente: *Model Builder data_quality.notes*).

### 4.1 Crecimiento y rentabilidad
- **Ingresos:** €32,0m (2022) → €38,0m (2023) → €42,0m (2024); **CAGR 2022–2024 ~14,6%** (fuente: *Model Builder; Valuation Reviewer*).
- **EBITDA:** €3,8m → €4,9m → €5,8m; **CAGR ~23,6%** (fuente: *Model Builder; Valuation Reviewer*).
- **Margen EBITDA:** **11,9% → 12,9% → 13,8%** (mejora sostenida, +1,93 pp 2022–2024) (fuente: *Model Builder derived_metrics; Valuation Reviewer*).

### 4.2 Capacidad de servicio de deuda (proxy por intereses)
- **Gastos financieros:** €0,45m → €0,52m → €0,61m (fuente: *Model Builder income_statement.financial_expenses*).
- **Cobertura de intereses (EBITDA/financieros):** **8,44x → 9,42x → 9,51x** (holgada en todo el periodo) (fuente: *Model Builder derived_metrics; Valuation Reviewer*).

### 4.3 Liquidez y circulante
- **Capital circulante (CA–CL):** €2,3m → €3,2m → €4,7m (mejora de holgura operativa) (fuente: *Model Builder derived_metrics; Valuation Reviewer*).
- **Current ratio:** **1,32x → 1,36x → 1,48x** (cómodo y en mejora) (fuente: *Model Builder derived_metrics; Valuation Reviewer*).

### 4.4 Apalancamiento y estructura (limitaciones)
- **Deuda financiera neta (ND):** €8,0m → €10,5m → €12,0m (incremento +€4,0m 2022–2024) (fuente: *Model Builder balance_sheet.net_financial_debt; Valuation Reviewer*).
- **ND/EBITDA:** **2,11x → 2,14x → 2,07x** (estable ~2,1x; el EBITDA compensa el aumento de deuda) (fuente: *Model Builder derived_metrics; Valuation Reviewer*).
- **ND/Equity:** **1,18x → 1,28x → 1,21x** (moderado) (fuente: *Model Builder derived_metrics; Valuation Reviewer*).
- **Equity:** €6,8m → €8,2m → €9,9m (refuerzo patrimonial +€3,1m) (fuente: *Model Builder balance_sheet.equity; Valuation Reviewer*).

**Punto de control (reconciliación):** la **ND 2024 (€12,0m)** excede el principal explícito de operaciones activas listadas en el banco, sugiriendo deuda adicional, tratamiento contable (leasing/confirming) o efecto caja no informado; requiere conciliación de deuda bruta y caja (fuente: *Valuation Reviewer tensiones_o_puntos_a_validar*).

---

## 5) Señales externas (noticias, litigios, cambios societarios)

- **Expansión internacional / nueva planta en Polonia (Wroclaw):**
  - **Hecho:** inauguración primera planta; **inversión €9m**; capacidad **120 empleados**.
  - **Riesgos asociados:** ejecución (ramp-up), presión de caja/endeudamiento, riesgos laborales/regulatorios y de cadena de suministro transfronteriza (fuente: *Market Researcher; Expansión 2025-05-15*).

- **Concentración de clientes / automoción alemana:**
  - **Hecho:** renovación/ampliación con dos OEM alemanes; contratos con visibilidad **>€15m hasta 2027**.
  - **Riesgos asociados:** concentración, ciclo automoción, riesgo contractual (calidad/entrega, revisiones de precio), exposición a Alemania y exigencias de capacidad (fuente: *Market Researcher; El Economista 2025-12-01*).

*Nota de trazabilidad:* no se aportan en los inputs referencias a litigios, sanciones o procedimientos; la lectura reputacional se limita a las fuentes citadas por Market Researcher y al estado **NO_CONCLUYENTE** del screening interno por falta de ejecución/documentación (fuente: *Market Researcher; KYC Screener*).

---

## 6) Evaluación de riesgo (riesgos, mitigantes, comparativa con historial)

### 6.1 Riesgos identificados
- **Riesgo de Cumplimiento/KYC (material):**
  - **UBO corporativo sin cadena final** (35%).
  - **Sin verificación de identidad** de administradores/UBO PF.
  - **Sin prueba de domicilio**, **sin formularios fiscales**, **sin SoF/SoW**, **sin PEP/sanciones** documentado; screening **NO_CONCLUYENTE** (fuente: *KYC Screener*).
- **Riesgo de ejecución y CAPEX (operativo/financiero):**
  - Arranque de planta en Polonia con inversión relevante; potencial presión de caja y necesidad de alcanzar volúmenes (fuente: *Market Researcher; Expansión 2025-05-15*).
- **Riesgo de concentración y ciclo sectorial:**
  - Dependencia de OEMs alemanes y del ciclo de automoción; riesgo de presión de precios y penalizaciones por calidad/entrega (fuente: *Market Researcher; El Economista 2025-12-01*).
- **Riesgo de transparencia financiera / calidad de datos (medio):**
  - Falta de cash flow, capex, caja y detalle de deuda impide estimar **DSCR/FCF** y estructura de vencimientos; además, **ND 2024** requiere reconciliación (fuente: *Model Builder data_quality.notes; Valuation Reviewer tensiones*).
- **Riesgo de refinanciación (prospectivo):**
  - Nota de gestor sobre posible necesidad de optimizar estructura de deuda en 2027 (fuente: *Valuation Reviewer alertas*).

### 6.2 Mitigantes y fortalezas
- **Fortaleza operativa:** crecimiento y mejora de margen (fuente: *Model Builder; Valuation Reviewer*).
- **Servicio de deuda (proxy intereses) holgado:** cobertura >8x todo el periodo (fuente: *Model Builder; Valuation Reviewer*).
- **Liquidez corriente en mejora:** current ratio ~1,48x en 2024 (fuente: *Model Builder*).
- **Refuerzo patrimonial:** equity +€3,1m (2022–2024) (fuente: *Model Builder*).
- **Comportamiento bancario positivo:** 0 impagos; operaciones activas al corriente; incidencias menores cerradas (fuente: *Valuation Reviewer historial_bancario_y_comportamiento*).
- **Mitigación de tipos:** cobertura de tipo de interés contratada (notional 12,0m) (fuente: *Valuation Reviewer consistencias*).

### 6.3 Comparativa con historial bancario
- La mejora de EBITDA y cobertura de intereses es **consistente** con el buen comportamiento (sin impagos) (fuente: *Valuation Reviewer consistencias*).
- El aumento de deuda neta es **coherente** con financiación de CAPEX y expansión, pero requiere **detalle** para confirmar composición y vencimientos (fuente: *Valuation Reviewer consistencias y tensiones*).

---

## 7) Recomendación (para decisión del analista)

**Recomendación:** **ESCALAR** a Cumplimiento/KYC y, en paralelo, **APROBAR CON CONDICIONES** desde el punto de vista financiero **solo si** se cierran previamente los gaps KYC y se completa la información financiera crítica.  
- **Argumentos a favor (financiero/comportamiento):** crecimiento, márgenes al alza, apalancamiento estable ~2,1x, cobertura de intereses ~9,5x y buen historial bancario (fuente: *Model Builder; Valuation Reviewer*).  
- **Argumentos en contra (bloqueantes KYC y de transparencia):** **R-OWN-02, R-ID-01, R-ADDR-01, R-TAX-01, R-SOF-01, R-PEP-01 = FAIL** y screening **NO_CONCLUYENTE**; además falta reconciliación de deuda neta y cash flow para validar capacidad real de repago (fuente: *KYC Screener; Valuation Reviewer; Model Builder*).

*La decisión final corresponde al analista humano y queda condicionada al cierre satisfactorio de Cumplimiento y a la validación de la estructura de deuda y caja.*

---

## 8) Condiciones y próximos pasos (si aplica)

### 8.1 Condiciones KYC/Cumplimiento (previas a formalización o disposición)
- **Completar cadena UBO** de **Acme Europe Holding GmbH (35%)** hasta persona(s) física(s) final(es) o documentar exención aplicable (fuente: *KYC Screener R-OWN-02*).
- **Aportar IDs vigentes** de administradores y UBO PF (Roberto Acme Jiménez; y administradores relevantes) según política interna (fuente: *KYC Screener R-ID-01*).
- **Aportar prueba de domicilio** válida (registro/recibo ≤ 3 meses según política) (fuente: *KYC Screener R-ADDR-01*).
- **Aportar formularios fiscales** aplicables (CRS/FATCA u otros según clasificación) (fuente: *KYC Screener R-TAX-01*).
- **Declaración y soporte de Fuente de Fondos/Fuente de Riqueza** y **propósito de la relación** (fuente: *KYC Screener R-SOF-01*).
- **Ejecutar y documentar screening PEP/sanciones** para entidad, UBOs y administradores; registrar resultado (fuente: *KYC Screener R-PEP-01; screening_conclusion NO_CONCLUYENTE*).

### 8.2 Condiciones financieras / información adicional (para cierre de riesgo)
- **Conciliación de deuda** a 2024-12-31: deuda bruta por instrumento y entidad financiera, **caja y equivalentes**, y puente a **deuda neta €12,0m** (fuente: *Valuation Reviewer tensiones; preguntas_clave*).
- **Estado de flujos 2022–2024** y/o reporting interno para estimar **FCF/DSCR**, incluyendo **capex** y variación de circulante (fuente: *Valuation Reviewer; Model Builder data_quality.notes*).
- **Detalle confirming/factoring** (con/sin recurso) y tratamiento contable (fuente: *Valuation Reviewer preguntas_clave*).
- **Detalle de la cobertura de tipos** (notional 12,0m): vencimiento, strike, % cubierto y contabilidad de cobertura (fuente: *Valuation Reviewer preguntas_clave*).
- **Seguimiento del plan de Polonia**: hitos de ramp-up, presupuesto vs real, y métricas de calidad/entrega (PPM/OTIF) por el riesgo operativo asociado al arranque (fuente: *Market Researcher; Expansión 2025-05-15*).
- **Análisis de concentración de clientes**: top clientes, % ventas y términos contractuales clave hasta 2027 (fuente: *Market Researcher; El Economista 2025-12-01*).