## 1. Resumen ejecutivo

AgroVal Export Partners SL presenta un **perfil de riesgo operativo y de mercado moderado** por su exposición creciente a **Reino Unido** (+18% volumen) y por la **materialidad del riesgo FX GBP/EUR**, junto con una **necesidad estacional de circulante** asociada a campañas (fuente: *El Economista*, 2026-02-10; Market Researcher). En el historial bancario figura **rating interno A**, **0 impagos** y facilidades vigentes al corriente, con **exposición dispuesta ~11,92M€** (fuente: Valuation Reviewer / banking_profile_summary). No obstante, el expediente presenta **alertas KYC relevantes**: **screening PEP/sanciones no concluyente por no ejecutado**, **falta de identificación (DNI) de administradores/UBO**, **cadena de titularidad incompleta del UBO corporativo (45%)** y **ausencia de formularios fiscales CRS/FATCA** (fuente: KYC Screener). Adicionalmente, el análisis cuantitativo de solvencia/capacidad de pago queda **bloqueado** porque los estados financieros referenciados 2022–2024 no contienen importes extraídos (fuente: Model Builder; Valuation Reviewer).

## 2. Identificación de la empresa

- **Nombre legal:** AgroVal Export Partners SL (fuente: KYC Screener, R-ENT-01; escritura_constitucion.txt)  
- **Forma jurídica:** **Sociedad de Responsabilidad Limitada** (fuente: KYC Screener, R-ENT-01; escritura_constitucion.txt)  
- **NIF/CIF:** **B46781234** (fuente: KYC Screener, R-ENT-01; escritura_constitucion.txt)  
- **Domicilio social:** Polígono Industrial Nazaret, Calle B nº 14, **46023 Valencia** (fuente: KYC Screener, R-ENT-01; escritura_constitucion.txt)  
- **Fecha de constitución:** **2008-09-14** (fuente: KYC Screener, R-ENT-01; escritura_constitucion.txt)  
- **Administración / cargos:**
  - **José Antonio Valero Gimeno** — Consejero Delegado (fuente: KYC Screener, R-CTRL-01; escritura_constitucion.txt)
  - **Amparo Roca Blanco** — Directora Financiera y Consejera (fuente: KYC Screener, R-CTRL-01; escritura_constitucion.txt)
- **Titulares reales (UBO) declarados:**
  - **José Antonio Valero Gimeno** — **55,0%** (base: participación) (fuente: KYC Screener, R-OWN-01; escritura_constitucion.txt)
  - **Cooperativa Hortofruticola Levante COOP** — **45,0%** (base: participación) (fuente: KYC Screener, R-OWN-01; escritura_constitucion.txt)
- **Métricas corporativas (normalizadas):**
  - **Capital social:** **950.000 €** (fuente: Model Builder, key_metrics.capital_social)
  - **Empleados:** **167** (fuente: Model Builder, key_metrics.employees)

## 3. Hallazgos KYC (resultado por regla y alertas)

### 3.1 Resultado de reglas KYC
- **R-ENT-01 (Identificación entidad): PASS** — nombre, CIF, forma jurídica, domicilio y constitución documentados (fuente: KYC Screener; escritura_constitucion.txt).
- **R-OWN-01 (UBOs con %): PASS** — UBOs declarados 55% PF y 45% corporativo (fuente: KYC Screener; escritura_constitucion.txt).
- **R-OWN-02 (Cadena UBO corporativo hasta PF final): FAIL** — falta cadena/beneficiario final de **Cooperativa Hortofruticola Levante COOP (45%)** (fuente: KYC Screener; escritura_constitucion.txt).
- **R-CTRL-01 (Administradores identificados): PASS** — cargos y nombres identificados (fuente: KYC Screener; escritura_constitucion.txt).
- **R-ID-01 (IDs vigentes admins/UBO PF): FAIL** — no constan **DNI/pasaporte** ni vigencias de José Antonio Valero Gimeno ni Amparo Roca Blanco (fuente: KYC Screener).
- **R-ADDR-01 (Prueba domicilio reciente): WARN** — domicilio en escritura, pero falta prueba reciente ≤3 meses / nota registral actual (fuente: KYC Screener).
- **R-TAX-01 (CRS/FATCA): FAIL** — no aportados formularios fiscales (fuente: KYC Screener).
- **R-SOF-01 (Fuente de fondos/riqueza): WARN** — actividad y operativa sugeridas por balances, pero sin documentación explícita de SoF/SoW (fuente: KYC Screener).
- **R-FIN-01 (Financieros recientes): PASS** — existen documentos 2022–2024 en inventario (fuente: KYC Screener), aunque sin importes extraídos (fuente: Model Builder).
- **R-PEP-01 (Declaración PEP + screening): FAIL** — no consta declaración ni resultados de screening para entidad/UBOs/admins (fuente: KYC Screener).

### 3.2 Screening sanciones/PEP/adverse media
- **Resultado:** **NO_CONCLUYENTE** por ausencia de ejecución/entidades revisadas (“Screening sin entidades para revisar”) (fuente: KYC Screener, screening_conclusion y screening_resumen).  
- **Implicación para comité:** **alerta crítica de cumplimiento**: antes de cualquier decisión crediticia/renovación/ampliación debe completarse screening PEP/sanciones y adverse media para entidad, UBOs y administradores (trazabilidad: KYC Screener, R-PEP-01 FAIL).

## 4. Análisis financiero (ratios, evolución y tendencias)

### 4.1 Disponibilidad y calidad de información financiera
- Se referencian **balances 2022, 2023 y 2024**, pero el modelo normalizado no contiene **importes** (activos/pasivos/patrimonio/caja/deuda), por lo que **no es posible calcular** liquidez, apalancamiento, solvencia ni tendencias (fuente: Model Builder, data_gaps; Valuation Reviewer, key_gaps_blocking_comparison).
- No se aportan **Cuenta de Pérdidas y Ganancias** ni **Estado de Flujos**, impidiendo evaluar **rentabilidad** y **capacidad de servicio de deuda** (fuente: Model Builder, data_gaps; Valuation Reviewer).

### 4.2 Lectura prudente basada en señales internas disponibles (sin sustituir ratios)
- **Exposición bancaria actual (dispuesta): ~11,92M€** y **comprometida: ~14,20M€** (fuente: Valuation Reviewer, exposure_snapshot).
- **Deuda a plazo:** préstamo corporativo **8,95M€**, cuota mensual **108.000€**, vencimiento 2029-03-01 (fuente: Valuation Reviewer, active_facilities).
- **Circulante:** línea **5,25M€**, dispuesto **2,97M€**, vencimiento **2026-12-31** (fuente: Valuation Reviewer, active_facilities).
- **Comportamiento de pago:** **0 impagos** y facilidades al corriente (fuente: Valuation Reviewer, arrears_count y status_current).

> Nota metodológica (base de inferencia prudente): ante ausencia de PyG/CF, se toma el **historial de pago** como señal de comportamiento, pero **no** como evidencia suficiente de **capacidad futura** de repago, especialmente con vencimientos próximos de circulante y riesgos de mercado (fuente: Valuation Reviewer, reviewer_comment; Market Researcher).

## 5. Señales externas (noticias, litigios, cambios societarios)

- **Concentración geográfica/cliente (UK):** incremento de **+18%** de volumen hacia Reino Unido; riesgo de dependencia de destino y sensibilidad a shocks logísticos y regulación post‑Brexit (fuente: *El Economista*, 2026-02-10; Market Researcher).
- **Riesgo FX GBP/EUR:** la empresa estudia ampliar **coberturas FX**, señal de exposición material a GBP y potencial impacto en márgenes/caja (fuente: *El Economista*, 2026-02-10; Market Researcher).
- **Liquidez estacional / financiación de campaña 2027:** evaluación de financiación de campaña sugiere picos de circulante y dependencia de líneas (fuente: *El Economista*, 2026-02-10; Market Researcher).
- **Riesgo operativo por crecimiento:** récord de exportaciones puede tensionar capacidad, controles de calidad, trazabilidad y dependencia de terceros (fuente: *El Economista*, 2026-02-10; Market Researcher).
- **Partes vinculadas / litigios:** no se identifican señales externas específicas en la información aportada (fuente: Market Researcher, nota “Partes vinculadas”).

## 6. Evaluación de riesgo (riesgos, mitigantes, comparativa con historial)

### 6.1 Riesgos identificados
- **Cumplimiento/KYC (alto):**
  - **Screening PEP/sanciones no realizado → NO_CONCLUYENTE** (**alerta**) (fuente: KYC Screener, screening_conclusion; R-PEP-01 FAIL).
  - **Cadena UBO corporativo incompleta (45%)** (**alerta**) (fuente: KYC Screener, R-OWN-02 FAIL).
  - **Falta de DNI/pasaporte** de UBO PF y administradora (**alerta**) (fuente: KYC Screener, R-ID-01 FAIL).
  - **CRS/FATCA no aportado** (fuente: KYC Screener, R-TAX-01 FAIL).
- **Riesgo de información financiera / model risk (alto):**
  - Estados financieros sin importes extraídos; sin PyG/CF → **no se puede estimar DSCR/ICR, apalancamiento ni liquidez** (fuente: Model Builder, data_gaps; Valuation Reviewer, financials_missing high).
- **Riesgo de refinanciación/renovación de circulante (medio):**
  - Línea de circulante vence **2026-12-31**; sin financieros no se evalúa dependencia ni capacidad de renovación (fuente: Valuation Reviewer, short_maturity_working_capital_line).
- **Riesgo de mercado (medio):**
  - **Concentración UK** y **FX GBP/EUR** con potencial impacto en caja y márgenes (fuente: Market Researcher / *El Economista*, 2026-02-10).
- **Riesgo operativo (medio):**
  - Crecimiento rápido puede tensionar controles y cumplimiento fitosanitario/trazabilidad (fuente: Market Researcher / *El Economista*, 2026-02-10).
- **Riesgo de calidad de datos maestros (bajo-medio):**
  - Campo “cliente_desde” con formato inválido (probable 2012-08-15) (fuente: Valuation Reviewer, bank_history_anomalies).

### 6.2 Mitigantes observados
- **Historial bancario positivo:** **0 impagos** y operaciones al corriente (fuente: Valuation Reviewer).
- **Rating interno A** en segmento Corporate Agroindustria (fuente: Valuation Reviewer).
- **Señal de gestión de riesgo FX:** intención de ampliar coberturas (mitigante potencial, sujeto a política formal y evidencias) (fuente: Market Researcher / *El Economista*, 2026-02-10).

### 6.3 Comparativa con historial
- La comparativa cuantitativa con el historial (apalancamiento, liquidez, cobertura de deuda) **no es posible** por ausencia de importes financieros 2022–2024 (fuente: Valuation Reviewer, what_cannot_be_compared_due_to_missing_financials).  
- A nivel cualitativo, el historial refleja **comportamiento de pago adecuado**, pero el comité debería tratarlo como **condición necesaria, no suficiente**, dada la exposición dispuesta (~11,92M€) y la proximidad del vencimiento de circulante (fuente: Valuation Reviewer; Market Researcher).

## 7. Recomendación (para decisión del analista)

**RECOMENDACIÓN: ESCALAR** (a Cumplimiento/KYC y a Riesgos de Crédito) **antes de aprobar nuevas disposiciones, renovaciones o ampliaciones**, por concurrir simultáneamente:
- **Alertas KYC críticas** (screening no concluyente; UBO corporativo sin cadena; IDs no aportados; CRS/FATCA ausente) (fuente: KYC Screener).
- **Imposibilidad de análisis financiero cuantitativo** por falta de importes y ausencia de PyG/CF (fuente: Model Builder; Valuation Reviewer).

> El analista humano podrá convertir la recomendación en **APROBAR CON CONDICIONES** únicamente si se completan los puntos de Cumplimiento y se reconstruye el modelo financiero con ratios y capacidad de servicio, manteniendo coherencia con la exposición y el perfil de campaña/exportación.

## 8. Condiciones y próximos pasos (si aplica)

### 8.1 Condiciones KYC/Cumplimiento (prioridad alta)
- Ejecutar y documentar **screening PEP/sanciones/adverse media** para:
  - AgroVal Export Partners SL,
  - José Antonio Valero Gimeno,
  - Amparo Roca Blanco,
  - Cooperativa Hortofruticola Levante COOP (fuente: KYC Screener, R-PEP-01 FAIL; screening_conclusion NO_CONCLUYENTE).
- Aportar **DNI/pasaporte vigente** de José Antonio Valero Gimeno y Amparo Roca Blanco (fuente: KYC Screener, R-ID-01 FAIL).
- Completar **cadena de titularidad/beneficiario final** de la cooperativa (45%) hasta persona(s) física(s) final(es) o justificar estructura conforme a política interna (fuente: KYC Screener, R-OWN-02 FAIL).
- Aportar **CRS/FATCA** y formularios fiscales aplicables (fuente: KYC Screener, R-TAX-01 FAIL).
- Aportar **prueba de domicilio reciente** (≤3 meses) o nota registral actual (fuente: KYC Screener, R-ADDR-01 WARN).
- Documentar **Fuente de Fondos/Fuente de Riqueza** (contratos, extractos, explicación de aportaciones y ciclo de cobros/pagos de exportación) (fuente: KYC Screener, R-SOF-01 WARN).

### 8.2 Condiciones financieras / información para riesgo (prioridad alta)
- Reprocesar/aportar estados con importes:
  - **Balances 2022–2024** con detalle (activo/pasivo/patrimonio, caja, deuda CP/LP, clientes, existencias, proveedores) (fuente: Valuation Reviewer, priority_1; Model Builder, data_gaps).
  - **PyG 2022–2024** (ventas, margen, EBITDA, EBIT, resultado neto) (fuente: Valuation Reviewer, priority_1).
  - **Flujos 2022–2024** o conciliación de caja + detalle de deuda (fuente: Valuation Reviewer, priority_1).
- Con la información anterior, recalcular y presentar a comité:
  - **Net Debt**, **Net Debt/EBITDA**, **Current ratio**, **CFO/FCF**, **DSCR** vs cuota **108k/mes** y sensibilidad por campaña (fuente: Valuation Reviewer, next_steps).

### 8.3 Acciones operativas / datos maestros
- Corregir en sistemas el campo **cliente_desde** (confirmar si **2012-08-15**) para consistencia de reporting (fuente: Valuation Reviewer, bank_history_anomalies).

### 8.4 Puntos de atención para estructura de la operación (si se evalúa campaña 2027)
- Solicitar evidencia de **política de coberturas FX** (límites, contrapartes, instrumentos, calendario de cobros) y su alineación con exposición GBP (fuente: Market Researcher).
- Revisar dependencia de **UK** (top clientes/destinos, concentración, términos de cobro, Incoterms) y mitigación logística/regulatoria post‑Brexit (fuente: Market Researcher).