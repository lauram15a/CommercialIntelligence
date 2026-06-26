## 1. Resumen ejecutivo

Acme Componentes SL presenta un **perfil crediticio financiero sólido y en mejora** en FY2022–FY2024 (crecimiento de ingresos, expansión de margen, liquidez al alza y **cobertura de intereses ~9–10x**), consistente con un **historial bancario sin impagos** y operaciones vigentes al corriente (fuente: *Valuation Reviewer*; *Model Builder*). No obstante, el expediente muestra **alertas relevantes de Cumplimiento/KYC**: **screening PEP/sanciones/adverse media no evidenciado**, **UBO corporativo (35%) sin transparencia hasta persona física final** y **origen de fondos/riqueza no documentado** (fuente: *KYC Screener*). En señales externas, destaca **expansión con CAPEX (planta en Polonia, ~€9m)** y **potencial concentración comercial** en clientes alemanes con visibilidad de ingresos hasta 2027 (fuente: *Market Researcher*). Nivel de riesgo consolidado: **medio**, principalmente por **gaps KYC/AML** y **riesgo de ejecución/capex**, con mitigación parcial por métricas financieras y comportamiento histórico.

---

## 2. Identificación de la empresa

- **Razón social:** Acme Componentes SL  
- **Forma jurídica:** **Sociedad de Responsabilidad Limitada**  
- **NIF/CIF:** **B50123987**  
- **Jurisdicción / país:** **España (ES)**  
- **Fecha de constitución:** **2003-07-10**  
- **Domicilio social:** Polígono Malpica, Calle E nº 18, 50016 Zaragoza (ES)  
- **Actividad (CNAE):** **2562 – Tratamiento y revestimiento de metales** (sector **Industrial**)  
- **Capital social:** **€800.000**  
- **Empleados:** **310**  
  - Fuente: *KYC Screener* (entidades extraídas) y *Model Builder* (perfil normalizado).

**Administración / control (declarado):**
- **Roberto Acme Jiménez** — **Consejero Delegado**  
- **Klaus Meier** — **Consejero (representante Acme Europe)**  
  - Fuente: *KYC Screener* / *Model Builder*.

**Titulares reales (UBO) declarados:**
- **Roberto Acme Jiménez** — **65%** (persona física; base de control: propiedad)  
- **Acme Europe Holding GmbH** — **35%** (persona jurídica; jurisdicción: Alemania)  
  - Fuente: *KYC Screener* / *Model Builder*.

---

## 3. Hallazgos KYC (resultado de reglas y screening)

### 3.1 Resultado del motor de reglas KYC (trazabilidad por regla)

- **ENT-01 (Identificación y verificación de la entidad): PASS**  
  - Evidencia: `escritura_constitucion.txt` con nombre legal, NIF/CIF, forma jurídica, domicilio y fecha de constitución.  
  - Fuente: *KYC Screener*.

- **OWN-01 (Identificar UBOs con % y base de control): PARTIAL**  
  - Evidencia: UBOs listados con % y nacionalidad; **faltan datos completos y verificación** del UBO individual (**sin DOB/ID**).  
  - Fuente: *KYC Screener*; corroborado por *Model Builder* (campos dob/id_document nulos).

- **OWN-02 (Cadena de titularidad UBO corporativo hasta PF final o exención): FAIL — ALERTA**  
  - Evidencia: **Acme Europe Holding GmbH (35%) sin UBO final**, sin número registral, domicilio ni estructura.  
  - Fuente: *KYC Screener*; corroborado por *Model Builder* (registration_number y registered_address nulos).

- **CTRL-01 (Identificar administradores/controladores): PASS**  
  - Evidencia: administradores listados en `escritura_constitucion.txt`.  
  - Fuente: *KYC Screener*.

- **SOF-01 (Origen de fondos / riqueza): FAIL — ALERTA**  
  - Evidencia: solo balances 2022–2024; **no consta declaración SOF/SOW** ni soporte específico.  
  - Fuente: *KYC Screener*.

- **DOC-01 (Inventario documental mínimo): FAIL — ALERTA**  
  - Evidencia: recibido escritura + balances; faltan registro mercantil actualizado, organigrama, IDs, prueba de domicilio, formularios fiscales.  
  - Fuente: *KYC Screener*.

- **SCR-01 (Screening sanciones/PEP/adverse media): FAIL — ALERTA**  
  - Evidencia: **no se aportan resultados de screening**; la nota “Sin alertas registradas” es interna y **no sustituye screening regulatorio**.  
  - Fuente: *KYC Screener*.

### 3.2 Screening (estado y alcance)

- **Estado:** **NO CONCLUYENTE / no realizado en el paquete**  
- **Partes a cribar:**  
  - Acme Componentes SL  
  - Roberto Acme Jiménez  
  - Acme Europe Holding GmbH  
  - Klaus Meier  
- Fuente: *KYC Screener* (screening.status = not_performed_in_this_packet; screening_conclusion = NO_CONCLUYENTE).

### 3.3 Disparadores de escalado (Cumplimiento)

- **UBO corporativo sin transparencia** (falta UBO final de Acme Europe Holding GmbH).  
- **Screening no evidenciado** (sanciones/PEP/adverse media).  
- **Origen de fondos/riqueza no documentado**.  
- Fuente: *KYC Screener* (escalation_triggers).

---

## 4. Análisis financiero (ratios clave y tendencias)

**Fuente financiera principal:** “Sistemas contables del banco (datos remitidos por la empresa y validados internamente)” para FY2022–FY2024 (fuente: *KYC Screener*; normalización y ratios: *Model Builder*). Lectura y consistencia con historial: *Valuation Reviewer*.

### 4.1 Evolución de resultados

- **Ingresos:** €32,0m (2022) → €38,0m (2023) → €42,0m (2024)  
  - Crecimiento YoY: **+18,8% (2023)**; **+10,5% (2024)** (desaceleración considerada normal).  
  - Fuente: *Model Builder* (yoy_changes) y *Valuation Reviewer*.

- **EBITDA:** €3,8m → €4,9m → €5,8m  
  - Crecimiento YoY: **+28,9% (2023)**; **+18,4% (2024)**.  
  - Fuente: *Model Builder*.

- **Margen EBITDA:** **11,9% (2022)** → **12,9% (2023)** → **13,8% (2024)** (**expansión de margen**).  
  - Fuente: *Model Builder*; lectura: *Valuation Reviewer*.

### 4.2 Liquidez y circulante

- **Current ratio:** **1,32x (2022)** → **1,36x (2023)** → **1,48x (2024)** (tendencia de mejora).  
- **Fondo de maniobra:** **€2,3m** → **€3,2m** → **€4,7m** (mayor colchón).  
  - Fuente: *Model Builder*; lectura: *Valuation Reviewer*.

### 4.3 Apalancamiento y servicio de deuda

- **Deuda financiera neta (NFD):** €8,0m → €10,5m → €12,0m (**+50% acumulado 2022–2024**).  
  - Fuente: *Model Builder*; flag: *Valuation Reviewer*.

- **NFD / EBITDA:** **2,11x (2022)** → **2,14x (2023)** → **2,07x (2024)**  
  - Lectura: **apalancamiento estable en rango moderado**.  
  - Fuente: *Model Builder*; lectura: *Valuation Reviewer*.

- **Cobertura de intereses (EBITDA / gastos financieros):** **8,44x** → **9,42x** → **9,51x**  
  - Lectura: **muy sólida**.  
  - Fuente: *Model Builder*; lectura: *Valuation Reviewer*.

### 4.4 Capitalización

- **Fondos propios:** €6,8m → €8,2m → €9,9m (refuerzo de equity).  
  - Fuente: *Model Builder*; lectura: *Valuation Reviewer*.

### 4.5 Coherencia con historial bancario y operaciones activas

- **Historial de impagos:** **0** (positivo).  
- **Incidencias:** 2 (documentales/operativas):  
  - Discrepancia puntual en poderes de firma (subsanada en 2023).  
  - Entrega tardía de cuentas auditadas 2022 (10 días).  
- **Operaciones activas (al corriente):**  
  - Préstamo corporativo **€5,2m**, vencimiento 2029-03-01.  
  - Línea de circulante **límite €2,5m**, dispuesto €1,3m, vencimiento 2026-12-31.  
- Fuente: *Valuation Reviewer*.

**Nota de prudencia (base de inferencia):** dado el **crecimiento de NFD** y la señal externa de **CAPEX €9m** (planta Polonia), se infiere una **fase de inversión/expansión** que puede tensionar caja si el ramp-up se retrasa; esta inferencia se apoya en la noticia y en la trayectoria de deuda neta, sin disponer de plan de negocio ni cash flow detallado (fuentes: *Market Researcher*; *Model Builder*; limitaciones: *Valuation Reviewer*).

---

## 5. Señales externas (noticias, litigios, cambios societarios)

**Fuentes:** *Expansión* (2025-05-15) y *El Economista* (2025-12-01), recopiladas por *Market Researcher*.

- **Expansión internacional / CAPEX:** inauguración de **planta en Polonia (Wroclaw)**, **capacidad 120 empleados**, **inversión ~€9m**.  
  - Riesgo: **ejecución (ramp-up), sobrecostes, presión de caja**, reconfiguración de supply chain intra-UE.  
  - Fuente: *Market Researcher*.

- **Concentración comercial:** renovación/ampliación con **dos fabricantes alemanes de primer nivel**, con **ingresos >€15m hasta 2027**.  
  - Riesgo: **concentración de clientes**, presión de precios/penalizaciones, exposición al ciclo automotriz alemán.  
  - Mitigante: **visibilidad de ingresos hasta 2027** (reduce riesgo de corto plazo).  
  - Fuente: *Market Researcher*.

- **Riesgo regulatorio/laboral (implícito por operación en Polonia):** requisitos de calidad automoción, EHS/medioambiente, mercado laboral local.  
  - Fuente: *Market Researcher*.

**Alcance:** no se aportan señales de litigios ni sanciones en estas noticias; no sustituyen el **screening regulatorio** (fuente: *Market Researcher*; *KYC Screener*).

---

## 6. Evaluación de riesgo (riesgos, mitigantes, comparativa con historial)

### 6.1 Riesgos identificados

**Cumplimiento / KYC (materiales para onboarding/renovación):**
- **Screening no evidenciado** para entidad, UBOs y administradores (**SCR-01 fail**).  
- **UBO corporativo (35%) sin cadena de titularidad hasta PF final** (**OWN-02 fail**).  
- **Origen de fondos/riqueza no documentado** (**SOF-01 fail**).  
- **Inventario documental incompleto** (registro mercantil actualizado, organigrama, IDs, prueba domicilio, CRS/FATCA) (**DOC-01 fail**).  
- Fuente: *KYC Screener*; flags KYC: *Valuation Reviewer*.

**Financieros / estructura:**
- **Deuda neta en aumento** (2022–2024) aunque **ND/EBITDA estable ~2,1x**; riesgo de que nuevas inversiones eleven apalancamiento por encima de política interna/sector.  
- Fuente: *Model Builder*; lectura: *Valuation Reviewer*.

**Riesgo de mercado/derivados:**
- **Cobertura de tipos** por nominal **€12,0m** sin detalle de **MTM, vencimientos, contrapartida ni CSA/colateral**; posible impacto en liquidez/colateral y riesgo de valoración.  
- Fuente: *Valuation Reviewer*.

**Operativo / negocio (externo):**
- **Riesgo de ejecución** por nueva planta en Polonia (ramp-up, costes, calidad).  
- **Riesgo de concentración** en clientes automoción alemanes (pricing/penalizaciones/ciclo).  
- Fuente: *Market Researcher*.

### 6.2 Mitigantes

- **Métricas operativas en mejora** (margen EBITDA al alza) y **cobertura de intereses muy holgada** (~9–10x).  
- **Liquidez mejorando** (current ratio 1,48x en 2024; fondo de maniobra creciente).  
- **Refuerzo de fondos propios** (equity 2024: €9,9m).  
- **Historial bancario positivo:** **0 impagos** y operaciones al corriente; incidencias previas menores y subsanadas.  
- **Visibilidad parcial de ingresos** hasta 2027 por contratos (>€15m).  
- Fuentes: *Model Builder*; *Valuation Reviewer*; *Market Researcher*.

### 6.3 Comparativa con historial bancario

- La evolución 2022–2024 es **consistente** con el comportamiento observado por el banco (sin impagos; uso de circulante/confirming coherente con crecimiento).  
- Las incidencias históricas son **operativas/documentales** y no contradicen el desempeño financiero, pero refuerzan la necesidad de **disciplina de reporting** y cierre de **gaps KYC**.  
- Fuente: *Valuation Reviewer*.

---

## 7. Recomendación (para decisión del analista)

**Recomendación propuesta:** **APROBAR CON CONDICIONES** (condicionada a cierre de Cumplimiento y a información financiera adicional), con **posible ESCALADO a Cumplimiento** si no se completa la transparencia de UBO corporativo y el screening.

**Racional (trazable):**
- A favor: desempeño financiero robusto (margen, liquidez, coberturas), apalancamiento moderado y estable, historial bancario sin impagos (fuentes: *Model Builder*; *Valuation Reviewer*).  
- En contra / condicionantes: **fallos KYC críticos** (OWN-02, SOF-01, DOC-01, SCR-01) y **derivado sin transparencia** (fuentes: *KYC Screener*; *Valuation Reviewer*).  
- Riesgo adicional a monitorizar: ejecución de CAPEX y concentración comercial (fuente: *Market Researcher*).

> La decisión final corresponde al analista humano y debe alinearse con la política interna AML/KYC y de derivados.

---

## 8. Condiciones y próximos pasos (si aplica)

### 8.1 Condiciones KYC/AML (previas a formalización o como condición suspensiva según política)
- **Completar screening** sanciones/PEP/adverse media para: Acme Componentes SL, Roberto Acme Jiménez, Acme Europe Holding GmbH y Klaus Meier, con evidencia archivada.  
  - Fuente: *KYC Screener* (SCR-01 fail; parties_to_screen).

- **Transparencia UBO corporativo (Acme Europe Holding GmbH, 35%)**: aportar **extracto registral alemán (Handelsregister)**, domicilio, número registral y **cadena de titularidad hasta PF final** (o justificación de exención conforme a política).  
  - Fuente: *KYC Screener* (OWN-02 fail) y *Valuation Reviewer* (flag data_gap_kyc).

- **Identificación UBO/controladores:** aportar **DOB + documento vigente** de Roberto Acme Jiménez y de Klaus Meier (y verificación según estándar interno).  
  - Fuente: *KYC Screener* (OWN-01 partial; missing docs).

- **Origen de fondos / riqueza y propósito de la relación:** declaración firmada y soporte razonable (p.ej., explicación de generación de caja, contratos relevantes, estados auditados), y **actividad esperada**.  
  - Fuente: *KYC Screener* (SOF-01 fail; missing items).

- **Paquete documental mínimo:** nota simple/registro mercantil actualizado, organigrama firmado, prueba de domicilio (si aplica), formularios fiscales (CRS/FATCA).  
  - Fuente: *KYC Screener* (DOC-01 fail; missing docs).

### 8.2 Condiciones financieras / información adicional
- **Detalle de deuda financiera total** (bruta vs caja) con vencimientos y tipo fijo/variable para reconciliar con NFD FY2024 (€12,0m).  
  - Fuente: *Valuation Reviewer* (recomendación; limitaciones).

- **Derivado de cobertura de tipos (nominal €12,0m):** ficha completa con **MTM**, calendario, contrapartida, CSA/colateral y tratamiento contable.  
  - Fuente: *Valuation Reviewer* (flag derivados).

- **Covenants / reporting (propuesta):**
  - Entrega de EEFF auditados en plazo (calendario pactado) dada la incidencia histórica de retraso (10 días en 2022).  
  - Seguimiento trimestral de **ND/EBITDA** e **Interest Coverage** (métricas ya calculadas en el modelo).  
  - Fuente: *Valuation Reviewer* (incidencias y recomendaciones) y *Model Builder* (métricas).

### 8.3 Monitorización de negocio (post-aprobación)
- Solicitar **plan de inversión y ramp-up** de la planta en Polonia (capex, hitos, sensibilidad de caja) y **detalle de concentración por cliente** (top clientes, cláusulas de penalización, duración).  
  - Base: señal externa de CAPEX y concentración; se solicita para cuantificar riesgos identificados.  
  - Fuente: *Market Researcher*.

---