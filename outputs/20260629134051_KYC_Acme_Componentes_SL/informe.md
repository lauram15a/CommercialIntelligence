## 1) Resumen ejecutivo

Acme Componentes SL presenta un **perfil crediticio sólido** con **apalancamiento estable** (Debt/EBITDA ~**2,1x** en 2022–2024) y **capacidad de servicio de deuda holgada** (cobertura de intereses **>8,4x** y al alza), junto con **mejora de liquidez** (corriente **1,32x → 1,48x**). No obstante, el expediente KYC contiene **incidencias materiales**: **falta de cadena de titularidad del UBO corporativo**, **ausencia de IDs vigentes**, **sin auto-certificación fiscal (CRS/FATCA)**, **sin fuente de fondos/riqueza**, y **screening no concluyente con alertas** (PEP y adverse media) que requieren revisión. En señales externas, destaca una **expansión industrial en Polonia (9M€ CapEx)** y **contratos hasta 2027 (>15M€)**, que aportan visibilidad pero elevan el **riesgo de ejecución** y de **concentración sectorial (automoción alemana)**. Recomendación técnica: **APROBAR CON CONDICIONES / ESCALAR a Cumplimiento** para cierre KYC y validación de alertas antes de formalizar.

**Fuentes:** Valuation Reviewer (ratios e interpretación); Model Builder (magnitudes 2022–2024); KYC Screener (reglas KYC y screening); Market Researcher (noticias 2025).

---

## 2) Identificación de la empresa

- **Nombre legal:** Acme Componentes SL  
- **Forma jurídica:** **Sociedad de Responsabilidad Limitada**  
- **NIF/CIF:** **B50123987**  
- **Domicilio social:** **Polígono Malpica, Calle E nº 18, 50016 Zaragoza**  
- **Fecha de constitución:** **2003-07-10**  
- **Administración / cargos:**
  - **Roberto Acme Jiménez** — **Consejero Delegado**
  - **Klaus Meier** — **Consejero** (representante de Acme Europe)
- **Titulares reales (UBO) declarados:**
  - **Roberto Acme Jiménez** — **65,0%** (control por propiedad)
  - **Acme Europe Holding GmbH** — **35,0%** (control por propiedad)

**Fuente:** KYC Screener — evidencia en `escritura_constitucion.txt` (R-ENT-01, R-OWN-01, R-CTRL-01).

---

## 3) Hallazgos KYC (reglas y screening)

### 3.1 Resultado por regla KYC
- **R-ENT-01 Identificación completa entidad — PASS**  
  Evidencia: nombre, NIF, forma jurídica, domicilio y constitución en `escritura_constitucion.txt`.
- **R-OWN-01 UBOs declarados con % — PASS**  
  Evidencia: 65% PF + 35% UBO corporativo en `escritura_constitucion.txt`.
- **R-OWN-02 Cadena de titularidad UBO corporativo — FAIL (material)**  
  **Alerta:** falta cadena hasta **persona física final** para **Acme Europe Holding GmbH (35%)**.
- **R-CTRL-01 Administradores identificados — PASS**  
  Evidencia: Roberto Acme Jiménez y Klaus Meier en `escritura_constitucion.txt`.
- **R-ID-01 IDs vigentes admins/UBOs PF — FAIL (material)**  
  **Alerta:** no constan **DNI/pasaporte** ni vigencia de Roberto Acme Jiménez y Klaus Meier.
- **R-ADDR-01 Prueba de domicilio ≤ 3 meses — WARN**  
  Consta domicilio en escritura, pero falta soporte actualizado (nota registral/recibo reciente).
- **R-TAX-01 CRS/FATCA — FAIL (material)**  
  **Alerta:** no se aportan formularios de auto-certificación fiscal.
- **R-SOF-01 Fuente de fondos/riqueza — FAIL (material)**  
  **Alerta:** no hay documentación/explicación de origen de fondos y flujos.
- **R-FIN-01 Estados financieros recientes — PASS**  
  Evidencia: `balance_2022.txt`, `balance_2023.txt`, `balance_2024.txt` (según KYC Screener).
- **R-PEP-01 Declaración PEP y screening — FAIL (material)**  
  **Alerta:** no consta declaración formal ni resultado concluyente en fuentes operativas.

**Fuente:** KYC Screener — `kyc_results`.

### 3.2 Screening (sanciones/PEP/adverse media)
- **Acme Componentes SL:** sin hits en fuente local; **resultado no concluyente** (requiere repetición en fuente operativa actualizada).  
- **Roberto Acme Jiménez:** sin hits en fuente local; **resultado no concluyente**.  
- **Acme Europe Holding GmbH:** **hit adverse media** (confianza 0,71): investigación por prácticas fiscales (Alemania, 2021), **caso cerrado sin condena**. **Revisión requerida**.  
- **Klaus Meier:** **hit PEP** (confianza 0,78): exfuncionario Ministerio de Economía alemán (2014–2018), **sin sanciones activas**. **Revisión requerida**.

**Conclusión de screening:** **ALERTA** (2 coincidencias de 4).  
**Fuente:** KYC Screener — `screening_results`, `screening_conclusion` (fuente `local_db`, marcada como no concluyente/review_required).

---

## 4) Análisis financiero (2022–2024)

### 4.1 Magnitudes base (según modelo)
- **EBITDA:** 3,8M€ (2022) → 4,9M€ (2023) → 5,8M€ (2024)  
- **Deuda financiera:** 8,0M€ (2022) → 10,5M€ (2023) → 12,0M€ (2024)  
- **Activo corriente:** 9,5M€ → 12,1M€ → 14,5M€  
- **Pasivo corriente:** 7,2M€ → 8,9M€ → 9,8M€  
- **Gastos financieros:** 0,45M€ → 0,52M€ → 0,61M€

**Fuente:** Model Builder — `periodos` (datos desde base de datos interna).

### 4.2 Ratios clave y evolución
- **Apalancamiento (Debt/EBITDA):** 2,11x (2022) → 2,14x (2023) → **2,07x (2024)**  
  - Variación 2022–2024: **-1,7%** (ligera mejora).
- **Liquidez corriente (Activo corriente / Pasivo corriente):** 1,32x → 1,36x → **1,48x** (mejora sostenida).
- **Cobertura de intereses (EBITDA / Gastos financieros):** 8,44x → 9,42x → **9,51x** (holgada y creciente).

**Lectura:** crecimiento de EBITDA acompaña el aumento de deuda, manteniendo el apalancamiento en torno a **~2,1x**; la liquidez mejora, y la carga financiera es absorbible con margen.  
**Fuente:** Valuation Reviewer — `ratios_por_periodo` e `interpretacion`; Model Builder — magnitudes.

### 4.3 Observaciones para comité (limitaciones y peticiones)
- Para validar sostenibilidad de la mejora y dimensionar necesidades de financiación, se requiere **P&L y cash flow** (ventas, margen, CapEx, variación de circulante, FCF) y **detalle de deuda** (instrumentos, vencimientos, tipo fijo/variable).  
**Fuente:** Valuation Reviewer — `data_requests_priority`.

---

## 5) Señales externas (mercado, noticias, litigios, cambios relevantes)

- **Expansión internacional (operativo / CapEx):** apertura de **primera planta en Polonia (Wroclaw)**, **120 empleados** y **9M€ de inversión**.  
  - Riesgos asociados: ramp-up, desviaciones de coste/plazo, cumplimiento local, complejidad logística y de proveedores.  
  **Fuente:** Market Researcher — *Expansión* (2025-05-15).

- **Contratos y concentración (comercial / sectorial):** renovación/ampliación con **dos OEM alemanes**, asegurando **>15M€ de ingresos hasta 2027**.  
  - Positivo: visibilidad de ingresos.  
  - Riesgos: **concentración de clientes**, exposición al ciclo de **automoción alemana**, exigencias de calidad/penalizaciones.  
  **Fuente:** Market Researcher — *El Economista* (2025-12-01).

- **Riesgo reputacional (grupo/accionista):** adverse media sobre **Acme Europe Holding GmbH** por investigación fiscal (cerrada sin condena).  
  **Fuente:** KYC Screener — screening adverse media (local_db, revisión requerida).

---

## 6) Evaluación de riesgo (riesgos, mitigantes, comparativa con historial)

### 6.1 Riesgos identificados
- **Riesgo de Cumplimiento/KYC (alto, condicionante):**
  - **UBO corporativo sin cadena** hasta PF final (R-OWN-02 FAIL).
  - **Sin IDs vigentes** de administradores/UBO PF (R-ID-01 FAIL).
  - **Sin CRS/FATCA** (R-TAX-01 FAIL) y **sin fuente de fondos/riqueza** (R-SOF-01 FAIL).
  - **Screening con alertas**: **PEP** (Klaus Meier) y **adverse media** (Acme Europe Holding GmbH), además de screening **no concluyente** por basarse en fuente local.
  **Fuente:** KYC Screener — reglas y screening.

- **Riesgo de ejecución por expansión (medio):**
  - CapEx relevante (9M€) y puesta en marcha en Polonia; potencial presión en circulante y costes.  
  **Fuente:** Market Researcher.

- **Riesgo sectorial/comercial (medio):**
  - Exposición a automoción alemana y posible **concentración** en pocos clientes (aunque con contratos hasta 2027).  
  **Fuente:** Market Researcher.

- **Riesgo financiero (moderado-bajo, a vigilar):**
  - Deuda crece (8,0M€ → 12,0M€) pero apalancamiento se mantiene ~2,1x por mejora de EBITDA; riesgo de que nuevas inversiones/circulante eleven deuda si el ramp-up no cumple.  
  **Fuente:** Model Builder + Valuation Reviewer.

### 6.2 Mitigantes
- **Capacidad de servicio de deuda holgada:** cobertura de intereses ~9,5x (2024).  
- **Liquidez corriente en mejora:** 1,48x (2024).  
- **Visibilidad comercial:** contratos >15M€ hasta 2027 (si se confirman condiciones y concentración).  
**Fuentes:** Valuation Reviewer (ratios); Market Researcher (contratos).

### 6.3 Comparativa con historial bancario
- Se reporta **0 impagos**, operaciones al corriente y **rating interno A-**; se mencionan incidencias documentales menores ya subsanadas.  
**Fuente:** Valuation Reviewer — `interpretacion` (nota: no se adjunta extracto de histórico; se toma como referencia del agente de valoración).

---

## 7) Recomendación (para decisión del analista)

**Recomendación técnica:** **APROBAR CON CONDICIONES** y **ESCALAR a Cumplimiento** para cierre KYC/screening antes de formalización o desembolso.

**Racional:**
- **A favor (crédito):** ratios consistentes con **riesgo moderado-bajo** (Debt/EBITDA ~2,1x; cobertura >9x; liquidez en mejora) y buen comportamiento histórico reportado.  
  **Fuente:** Valuation Reviewer + Model Builder.
- **En contra (cumplimiento):** **incidencias KYC materiales** y **alertas de screening** (PEP/adverse media) con screening no concluyente; esto impide un cierre KYC robusto sin validación adicional.  
  **Fuente:** KYC Screener.

> La decisión final corresponde al analista humano y a Cumplimiento, una vez completadas las verificaciones.

---

## 8) Condiciones y próximos pasos (para cierre y mitigación)

### 8.1 Condiciones KYC/Cumplimiento (previas a formalización/desembolso)
- **Completar cadena de titularidad** de **Acme Europe Holding GmbH (35%)** hasta **beneficiario(s) final(es) persona física**, con documentación soporte.  
  **Fuente:** KYC Screener — R-OWN-02 FAIL.
- **Aportar IDs vigentes** (DNI/pasaporte) de **Roberto Acme Jiménez** y **Klaus Meier** (y de UBOs PF finales de la cadena).  
  **Fuente:** KYC Screener — R-ID-01 FAIL.
- **Auto-certificación fiscal CRS/FATCA** firmada y validada.  
  **Fuente:** KYC Screener — R-TAX-01 FAIL.
- **Declaración y evidencia de Fuente de Fondos/Fuente de Riqueza** coherente con actividad y flujos (contratos principales, explicación de cobros/pagos, estructura de ingresos).  
  **Fuente:** KYC Screener — R-SOF-01 FAIL.
- **Re-screening en fuentes operativas actualizadas** (UE/OFAC/ONU/HMT y/o proveedor interno) para entidad, UBOs y administradores; **revisión reforzada PEP** para Klaus Meier y análisis de adverse media para Acme Europe Holding GmbH.  
  **Fuente:** KYC Screener — screening `local_db` no concluyente + hits.

### 8.2 Condiciones financieras / información para seguimiento
- **Detalle de deuda 2024–2025** por instrumento, vencimientos, covenants y tipo (fijo/variable), para evaluar sensibilidad a tipos y cualquier mención de refinanciación 2027.  
  **Fuente:** Valuation Reviewer — `data_requests_priority`.
- **P&L y cash flow 2022–2024 (y YTD 2025 si existe):** ventas, margen EBITDA, CapEx, variación de circulante y FCF; foco en impacto de expansión en Polonia.  
  **Fuente:** Valuation Reviewer — `data_requests_priority`; Market Researcher — CapEx 9M€.
- **Seguimiento de concentración de clientes:** solicitar desglose de ventas por cliente y condiciones contractuales (penalizaciones, SLAs, duración), alineado con contratos hasta 2027.  
  **Fuente:** Market Researcher — contratos con OEM alemanes.

--- 

**Anexos / trazabilidad de inputs utilizados**
- KYC Screener: `escritura_constitucion.txt`, `balance_2022.txt`, `balance_2023.txt`, `balance_2024.txt`; reglas R-ENT-01, R-OWN-01/02, R-CTRL-01, R-ID-01, R-ADDR-01, R-TAX-01, R-SOF-01, R-FIN-01, R-PEP-01; screening `local_db`.  
- Model Builder: magnitudes 2022–2024 (EBITDA, deuda, activo/pasivo corriente, gastos financieros).  
- Valuation Reviewer: ratios (Debt/EBITDA, liquidez corriente, cobertura intereses), lectura de historial (A-, 0 impagos) y data requests.  
- Market Researcher: noticias *Expansión* (2025-05-15) y *El Economista* (2025-12-01).