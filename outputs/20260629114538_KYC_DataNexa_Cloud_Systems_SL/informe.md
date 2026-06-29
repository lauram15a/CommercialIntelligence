## 1) Resumen ejecutivo

DataNexa Cloud Systems SL presenta un perfil financiero **favorable** (crecimiento sostenido 2022–2024, mejora de margen EBITDA y **desapalancamiento relativo**), con comportamiento bancario **sin impagos** y operaciones **al corriente** (Valuation Reviewer; Model Builder). No obstante, el expediente KYC está **materialmente incompleto**: faltan verificaciones de administradores/UBOs, look-through del socio corporativo y el **screening externo** de sanciones/PEP/adverse media es **NO CONCLUYENTE** (KYC Screener). Existen además limitaciones de análisis por **estados financieros incompletos** (sin cash flow y balance no verificable) y un **riesgo de ejecución** asociado a M&A en evaluación (Market Researcher; Valuation Reviewer). Con la información disponible, el riesgo se considera **moderado (financiero)** pero con **bloqueos de Cumplimiento** que impiden cierre de recomendación sin condiciones.

## 2) Identificación de la empresa

- **Razón social**: DataNexa Cloud Systems SL (KYC Screener; Model Builder)
- **Forma jurídica**: **Sociedad de Responsabilidad Limitada (SL)** (Model Builder)
- **NIF/CIF**: **B87234561** (Model Builder)
- **Domicilio social**: **Calle Príncipe de Vergara 112, 28002 Madrid (España)** (Model Builder)
- **Fecha de constitución**: **2016-03-22** (Model Builder; doc. `escritura_constitucion.txt`)
- **Actividad (CNAE)**: **6201 – Actividades de programación informática** (Model Builder)
- **Descripción de negocio (interna)**: plataforma **SaaS B2B** de gestión de operaciones y reporting financiero para empresas medianas; ARR 11,2M€ en 2024; M&A en análisis (VerticalSync ERP SL) (Model Builder)
- **Empleados**: **128** (Model Builder)
- **Capital social**: **500.000 €** (Model Builder)

**Administración / control (declarado)** (Model Builder; `escritura_constitucion.txt`):
- **Marcos Delgado Vidal** — **Consejero Delegado**
- **Nuria Alonso Ferrer** — **Consejera y Directora de Producto**

**Titulares reales (UBO ≥25%)** (Model Builder; KYC Screener):
- **Marcos Delgado Vidal** — **45%** (persona física)
- **Nuria Alonso Ferrer** — **30%** (persona física)
- **Vertex Ventures Iberia SL** — **25%** (persona jurídica)

## 3) Hallazgos KYC (resultado por regla y alertas)

**Fuente principal**: salida KYC Screener + normalización Model Builder.

- **ENT-01 Identificación de entidad**: **PASS**  
  - Evidencia: `escritura_constitucion.txt` contiene nombre legal, NIF/CIF, domicilio, fecha de constitución y forma jurídica (KYC Screener).

- **ENT-02 Administradores / personas con control verificados**: **FAIL** (**ALERTA**)  
  - Evidencia: existen nombres/cargos en `escritura_constitucion.txt`, pero **no** se aportan documentos de identidad ni verificación de personas físicas (KYC Screener).

- **UBO-01 Identificación de UBOs (≥25%)**: **PASS**  
  - Evidencia: `escritura_constitucion.txt` lista 45%, 30%, 25% (KYC Screener).

- **UBO-02 UBOs personas físicas (DOB, nacionalidad, ID vigente)**: **FAIL** (**ALERTA**)  
  - Evidencia: nacionalidad indicada, pero **sin DOB ni documento ID** para Marcos Delgado Vidal y Nuria Alonso Ferrer (KYC Screener; Model Builder flags `missing_dob`, `missing_id_document`).

- **UBO-03 UBO corporativo (datos registrales + cadena de titularidad)**: **FAIL** (**ALERTA**)  
  - Evidencia: **Vertex Ventures Iberia SL (25%)** sin NIF, domicilio ni beneficiarios finales (KYC Screener; Model Builder flags `missing_tax_id`, `missing_registered_address`).

- **SCR-01 Screening sanciones/PEP/adverse media (entidad, UBOs, administradores)**: **FAIL** (**ALERTA CRÍTICA DE CUMPLIMIENTO**)  
  - Evidencia: el expediente solo indica “Sin alertas registradas” en BBDD interna; **no** hay evidencia de screening externo ni listas consultadas. Conclusión: **NO_CONCLUYENTE** (KYC Screener).

- **SOF-01 Fuente de fondos / actividad económica con soporte**: **FAIL**  
  - Evidencia: hay descripción de negocio y EEFF, pero no declaración/soporte explícito de **fuente de fondos** (contratos, extractos, rondas, etc.) (KYC Screener).

- **ADDR-01 Verificación de domicilio**: **FAIL**  
  - Evidencia: domicilio indicado, pero sin prueba documental reciente (KYC Screener).

- **TAX-01 Documentación fiscal (CRS/FATCA; W-8/W-9 si aplica)**: **FAIL**  
  - Evidencia: no se incluyen formularios fiscales (KYC Screener).

**Nota de trazabilidad**: el Market Researcher aporta señales de prensa, pero **no sustituye** el screening formal de sanciones/PEP/adverse media exigible por política (KYC Screener; Market Researcher).

## 4) Análisis financiero (evolución de ratios clave y tendencias)

**Fuente**: Model Builder (EEFF parciales 2022–2024) + Valuation Reviewer (comparativa con historial bancario).  
**Limitación explícita**: sin cash flow, sin CapEx/D&A y sin balance completo verificable; no se puede estimar FCF ni validar ecuación contable (Model Builder; Valuation Reviewer).

### 4.1 Cuenta de resultados (parcial) y rentabilidad
- **Ingresos**: 8,9M€ (2022) → 11,6M€ (2023) → 15,2M€ (2024) (Model Builder)  
  - Crecimiento YoY: **+30,3% (2023)**; **+31,0% (2024)** (Valuation Reviewer).
- **EBITDA**: 1,51M€ (2022) → 2,03M€ (2023) → 2,89M€ (2024) (Model Builder)  
  - Crecimiento YoY: **+34,4% (2023)**; **+42,4% (2024)** (Valuation Reviewer).
- **Margen EBITDA**: **17,0% (2022)** → **17,5% (2023)** → **19,0% (2024)** (Model Builder).  
  - Lectura: mejora de eficiencia / apalancamiento operativo (Valuation Reviewer).

### 4.2 Apalancamiento y cobertura
- **Deuda financiera neta**: 3,20M€ (2022) → 4,10M€ (2023) → 5,40M€ (2024) (Model Builder).
- **ND/EBITDA**: **2,12x (2022)** → **2,02x (2023)** → **1,87x (2024)** (Model Builder; Valuation Reviewer).  
  - Lectura: desapalancamiento relativo por crecimiento de EBITDA (Valuation Reviewer).
- **Gastos financieros**: 0,14M€ (2022) → 0,185M€ (2023) → 0,24M€ (2024) (Model Builder).
- **Cobertura de intereses (EBITDA/intereses)**: **10,79x** → **10,97x** → **12,04x** (2022–2024) (Model Builder; Valuation Reviewer).  
  - Lectura: holgada y mejorando; consistente con “operaciones al corriente” (Valuation Reviewer).

### 4.3 Liquidez (circulante)
- **Activos corrientes / Pasivos corrientes**:  
  - CA: 3,8M€ → 5,2M€ → 7,1M€ (2022–2024) (Model Builder)  
  - CL: 2,1M€ → 2,7M€ → 3,5M€ (2022–2024) (Model Builder)
- **Current ratio**: **1,81x** → **1,93x** → **2,03x** (Model Builder; Valuation Reviewer).  
  - Lectura: liquidez corriente sólida; requiere validación con detalle de caja y estacionalidad (Valuation Reviewer).

### 4.4 Relación bancaria y carga de deuda (historial)
- **Rating interno**: **BBB+**; **impagos: 0**; segmento Corporate Tecnología (Valuation Reviewer).
- **Préstamo corporativo**: 4,45M€, cuota mensual 72k€, 2024-03-01 a 2029-03-01, **al corriente** (Valuation Reviewer).
- **Línea de circulante**: límite 2,55M€, dispuesto 1,35M€ (utilización ~52,9%), 2025-01-10 a 2026-12-31, **al corriente** (Valuation Reviewer).
- **DSCR proxy (EBITDA / cuota anual préstamo)**: 2,89M€ / 0,864M€ = **~3,34x** (Valuation Reviewer).  
  - Nota: proxy parcial; no incluye impuestos, capex, variación de circulante ni servicio de la línea (Valuation Reviewer).

## 5) Señales externas (noticias, litigios, cambios societarios relevantes)

**Fuente**: Market Researcher (prensa: *Expansión* 2026-02-15; *CincoDías* 2026-04-20). Alcance limitado a 2 señales; no se aportan registros de litigios/sanciones/cambios mercantiles (Market Researcher).

- **Crecimiento acelerado + posible M&A**: crecimiento “35% en ARR” y estudio de adquisición vertical en Iberia (VerticalSync ERP SL) (Market Researcher; consistente con Model Builder mna_activity=active).  
  - Riesgo: integración, consumo de caja/apalancamiento, distracción del management, cláusulas de cambio de control en contratos enterprise (Market Researcher).

- **Concentración en clientes enterprise del sector financiero**: cierre de 3 contratos enterprise con corporaciones financieras; ARR previsto >18M€ a 2026 (Market Researcher).  
  - Riesgo: concentración de ingresos, ciclos de venta/cobro largos, exigencias de compliance (seguridad, continuidad, auditorías, protección de datos) y riesgo reputacional ante incidentes (Market Researcher).

## 6) Evaluación de riesgo (riesgos, mitigantes, comparativa con historial)

### 6.1 Riesgos principales identificados (con trazabilidad)
- **Riesgo de Cumplimiento/KYC (material)**: expediente **incompleto** en verificación de administradores/UBOs, look-through de UBO corporativo y **screening externo NO CONCLUYENTE** (**KYC Screener**; flags en **Valuation Reviewer**).  
  - Impacto: imposibilidad de cierre KYC y de elevar propuesta sin condiciones de remediación (implicación operativa de política interna).

- **Riesgo de información financiera / calidad de datos**: EEFF **parciales** (sin cash flow, sin balance completo verificable, sin desglose de deuda/caja) (Model Builder; Valuation Reviewer).  
  - Impacto: limita evaluación de generación de caja real, covenants y capacidad de repago bajo estrés.

- **Riesgo de apalancamiento y conciliación de deuda**: diferencia entre **deuda neta 5,40M€** y **dispuesto bancario total 5,80M€** (préstamo + circulante) (Model Builder vs Valuation Reviewer).  
  - Impacto: requiere conciliación de caja y composición de deuda; posible deuda adicional o clasificación distinta.

- **Riesgo de ejecución por M&A**: proceso activo de adquisición (VerticalSync ERP SL) sin impacto cuantificado proforma (Market Researcher; Model Builder; Valuation Reviewer).  
  - Impacto: potencial aumento de apalancamiento, consumo de caja y riesgo operativo de integración.

- **Riesgo de concentración/compliance por base de clientes**: expansión en enterprise financiero puede elevar exigencias de seguridad y continuidad; concentración potencial en pocos clientes (Market Researcher).  
  - Impacto: sensibilidad a churn/renovaciones y a incidentes de ciber/servicio.

- **Riesgo operativo de datos internos**: fecha “cliente_desde” inválida (20112-06-15) en historial (Valuation Reviewer).  
  - Impacto: medio (calidad de dato); afecta lectura de antigüedad/vinculación.

### 6.2 Mitigantes observados
- **Crecimiento y rentabilidad en mejora**: ingresos y EBITDA creciendo con margen EBITDA al alza (Model Builder; Valuation Reviewer).
- **Desapalancamiento relativo**: ND/EBITDA mejora a ~1,87x en 2024 (Model Builder; Valuation Reviewer).
- **Cobertura de intereses holgada**: ~12x en 2024 (Model Builder; Valuation Reviewer).
- **Historial bancario positivo**: **0 impagos** y operaciones al corriente (Valuation Reviewer).
- **Liquidez corriente sólida (indicativa)**: current ratio ~2,03x en 2024 (Model Builder), si bien requiere validación con caja y circulante (Valuation Reviewer).

### 6.3 Comparativa con historial bancario (coherencias/incoherencias)
- **Coherente**: capacidad de servicio de intereses y buen comportamiento de pago (Model Builder ratios; Valuation Reviewer).  
- **Parcialmente consistente**: deuda neta vs dispuesto bancario (Model Builder vs Valuation Reviewer) — plausible por caja/ajustes, pero requiere evidencia.  
- **Inconsistente**: antigüedad de relación (Model Builder “desde 2022” vs historial con fecha inválida) (Valuation Reviewer).

## 7) Recomendación (para decisión del analista)

**Recomendación propuesta**: **APROBAR CON CONDICIONES** (condicionada a cierre KYC y ampliación de información financiera), o **ESCALAR** a Cumplimiento si la política interna exige screening concluido previo a cualquier aprobación.

**Racional** (trazable):
- A favor: métricas 2022–2024 muestran **crecimiento**, **margen en mejora**, **ND/EBITDA <2x** y **cobertura de intereses >10x**, con **historial sin impagos** (Model Builder; Valuation Reviewer).
- En contra / condicionantes: **SCR-01 FAIL (NO CONCLUYENTE)** y fallos en verificación de UBO/administradores y look-through corporativo (KYC Screener), además de **EEFF incompletos** y riesgos de M&A sin cuantificar (Model Builder; Valuation Reviewer; Market Researcher).

> La decisión final corresponde al analista humano y debe alinearse con la política de KYC/AML del banco, especialmente por el **screening externo no concluido**.

## 8) Condiciones y próximos pasos (si aplica)

### 8.1 Condiciones de Cumplimiento (previas a cierre / desembolso)
- Completar **screening externo** de **sanciones/PEP/adverse media** para: entidad, administradores y UBOs, con evidencia de listas consultadas y fecha (KYC Screener: SCR-01 FAIL).
- Aportar y verificar **documentos de identidad vigentes** + **fecha de nacimiento** de UBOs personas físicas (Marcos Delgado Vidal; Nuria Alonso Ferrer) (KYC Screener: UBO-02 FAIL; Model Builder flags).
- Para **Vertex Ventures Iberia SL (25%)**: NIF, domicilio registral y **cadena de titularidad (look-through)** hasta beneficiario final (KYC Screener: UBO-03 FAIL).
- **Verificación de domicilio** (documento válido según política) y **formularios fiscales** aplicables (ADDR-01 FAIL; TAX-01 FAIL) (KYC Screener).
- **Fuente de fondos**: soporte documental (p.ej., contratos relevantes, extractos, detalle de cobros recurrentes, rondas de inversión si aplica) (SOF-01 FAIL) (KYC Screener).

### 8.2 Condiciones de Riesgo/Finanzas (para cerrar análisis y covenants)
- Entregar **estados financieros completos 2022–2024** (balance completo, PyG completa) y **estado de flujos de efectivo**; alternativamente, CapEx, D&A y variación de circulante (Model Builder; Valuation Reviewer).
- **Conciliación de deuda neta** 2024: caja y equivalentes a 2024-12-31 + desglose de deuda (por entidad, tipo, tipo de interés, calendario) e identificación de deuda fuera de balance (leasing/factoring con recurso) (Valuation Reviewer).
- Confirmar condiciones de la **línea de circulante** (precio, comisiones, covenants) y justificación de uso (estacional vs estructural) (Valuation Reviewer).
- Si avanza el **M&A**: entregar plan proforma (precio, estructura cash/deuda/equity, sinergias, calendario, impacto en ND/EBITDA y liquidez) y principales conclusiones de due diligence (Market Researcher; Valuation Reviewer).

### 8.3 Correcciones operativas internas
- Reconciliar en sistemas la fecha **cliente_desde** (posible 2012/2021/2022) para consistencia de expediente (Valuation Reviewer).

--- 

**Anexos de trazabilidad (inputs utilizados)**  
- KYC: `escritura_constitucion.txt` + reglas KYC Screener (ENT-01..TAX-01)  
- Financieros: `balance_2022.txt`, `balance_2023.txt`, `balance_2024.txt` (Model Builder; datos “validados internamente”)  
- Historial bancario y exposición: Valuation Reviewer (préstamo, línea, rating, impagos)  
- Señales externas: Market Researcher (*Expansión* 2026-02-15; *CincoDías* 2026-04-20)