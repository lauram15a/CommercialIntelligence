## 1. Resumen ejecutivo

Acme Componentes SL presenta un **perfil crediticio globalmente sólido** para el segmento industrial, con **apalancamiento moderado y estable** (Debt/EBITDA ~**2,07x** en 2024) y **capacidad holgada de servicio de deuda** (cobertura de intereses ~**9,5x**), según estados 2022–2024 y ratios calculados internamente (Model Builder; Valuation Reviewer). No obstante, el expediente muestra **alertas KYC relevantes**: **cadena de titularidad incompleta** del socio corporativo (35%), **ausencia de IDs vigentes** de administradores/UBO PF, **sin PEP/sanciones** y **sin CRS/FATCA** ni **fuente de fondos/riqueza** documentada (KYC Screener). En señales externas, destaca una **expansión internacional** con **capex ~€9m** (planta en Polonia) y **mayor exposición a automoción alemana** con contratos >€15m hasta 2027, lo que introduce **riesgo de ejecución y concentración** (Market Researcher). Recomendación técnica: **APROBAR CON CONDICIONES** (condicionada a cierre KYC y a información de deuda/FCF), dejando la decisión final al analista/comité.

---

## 2. Identificación de la empresa

- **Nombre legal**: **Acme Componentes SL** (KYC Screener, R-ENT-01; evidencia: *escritura_constitucion.txt*).
- **Forma jurídica**: **Sociedad de Responsabilidad Limitada** (KYC Screener, R-ENT-01).
- **NIF/CIF**: **B50123987** (KYC Screener, R-ENT-01).
- **Domicilio social**: **Polígono Malpica, Calle E nº 18, 50016 Zaragoza** (KYC Screener, R-ENT-01).
- **Fecha de constitución**: **2003-07-10** (KYC Screener, R-ENT-01).
- **Actividad / sector**: Industrial, **CNAE 2562 (tratamiento y revestimiento de metales)** (Model Builder, tendencias_estructurales).
- **Tamaño operativo (referencia interna)**: **~310 empleados**; **capital social 800.000 EUR** (Model Builder, tendencias_estructurales).

**Administración / control**
- **Roberto Acme Jiménez** — **Consejero Delegado** (KYC Screener, R-CTRL-01; *escritura_constitucion.txt*).
- **Klaus Meier** — **Consejero** (representante de Acme Europe) (KYC Screener, R-CTRL-01; *escritura_constitucion.txt*).

**Titulares reales (UBO) declarados**
- **Roberto Acme Jiménez** — **65,0%** (control por participación) (KYC Screener, R-OWN-01).
- **Acme Europe Holding GmbH** — **35,0%** (control por participación) (KYC Screener, R-OWN-01).

---

## 3. Hallazgos KYC (resultado por regla y alertas)

### 3.1. Reglas KYC y evidencias

- **R-ENT-01 (Identificación entidad)**: **PASS**  
  - Evidencia: *escritura_constitucion.txt* (nombre, CIF, forma jurídica, domicilio, fecha constitución).

- **R-OWN-01 (UBOs declarados con % y base de control)**: **PASS**  
  - Evidencia: *escritura_constitucion.txt* (Roberto Acme Jiménez 65%; Acme Europe Holding GmbH 35%).

- **R-OWN-02 (Cadena de titularidad UBO corporativo hasta PF final)**: **FAIL — ALERTA**  
  - Evidencia: *escritura_constitucion.txt* identifica UBO corporativo **Acme Europe Holding GmbH (35%)** sin cadena hasta beneficiario final PF (KYC Screener).

- **R-CTRL-01 (Administradores/controladores identificados)**: **PASS**  
  - Evidencia: *escritura_constitucion.txt* (Roberto Acme Jiménez; Klaus Meier).

- **R-ID-01 (IDs vigentes de administradores y UBO PF)**: **FAIL — ALERTA**  
  - Evidencia: no constan DNI/pasaporte ni vigencia para **Roberto Acme Jiménez** ni **Klaus Meier** (KYC Screener).

- **R-ADDR-01 (Prueba de domicilio ≤ 3 meses)**: **WARN**  
  - Evidencia: domicilio consta en escritura, pero falta prueba actualizada (nota registral/recibo reciente) (KYC Screener).

- **R-TAX-01 (CRS/FATCA / formularios fiscales)**: **FAIL — ALERTA**  
  - Evidencia: no aportados (KYC Screener).

- **R-SOF-01 (Fuente de fondos/riqueza)**: **FAIL — ALERTA**  
  - Evidencia: no aportada declaración/documentación (KYC Screener).

- **R-FIN-01 (Información financiera reciente)**: **PASS**  
  - Evidencia: *balance_2022.txt, balance_2023.txt, balance_2024.txt* (KYC Screener).

- **R-PEP-01 (Declaración PEP + screening PEP/sanciones)**: **FAIL — ALERTA CRÍTICA DE CUMPLIMIENTO**  
  - Evidencia: no consta declaración ni resultados de screening para entidad/UBOs/administradores (KYC Screener).

### 3.2. Screening sanciones/PEP/adverse media

- **Resultado operativo del screening**: **NO_CONCLUYENTE**  
  - Evidencia: “Screening sin entidades para revisar” y ausencia de resultados en *screening_results* (KYC Screener).  
- Implicación: requiere **validación manual por Cumplimiento** antes de formalizar/elevar límites (KYC Screener, nota de evidencias).

---

## 4. Análisis financiero (ratios clave y tendencias)

> Fuente de datos: estados financieros 2022–2024 cargados desde **base de datos interna** (Model Builder, “resumen”). Ratios calculados por Valuation Reviewer.

### 4.1. Magnitudes operativas (base interna)

- **EBITDA**: 2022 **€3,8m** → 2023 **€4,9m** → 2024 **€5,8m** (Model Builder, periodos).
- **Deuda financiera**: 2022 **€8,0m** → 2023 **€10,5m** → 2024 **€12,0m** (Model Builder, periodos).
- **Activo corriente / Pasivo corriente**:  
  - 2022: **€9,5m / €7,2m**  
  - 2023: **€12,1m / €8,9m**  
  - 2024: **€14,5m / €9,8m** (Model Builder, periodos).
- **Gastos financieros**: 2022 **€0,45m** → 2023 **€0,52m** → 2024 **€0,61m** (Model Builder, periodos).

### 4.2. Ratios de crédito (2022–2024)

- **Debt/EBITDA**:  
  - 2022: **2,11x**  
  - 2023: **2,14x**  
  - 2024: **2,07x** (Valuation Reviewer, ratios_por_periodo).  
  - Variación 2022→2024: **-1,7%** (Valuation Reviewer, variacion).

- **Liquidez corriente (Activo corriente / Pasivo corriente)**:  
  - 2022: **1,32x**  
  - 2023: **1,36x**  
  - 2024: **1,48x** (Valuation Reviewer, ratios_por_periodo).

- **Cobertura de intereses (EBITDA / gastos financieros)**:  
  - 2022: **8,44x**  
  - 2023: **9,42x**  
  - 2024: **9,51x** (Valuation Reviewer, ratios_por_periodo).

### 4.3. Lectura técnica

- **Apalancamiento**: estable y en ligera mejora en 2024 (Debt/EBITDA ~2,07x), pese al aumento nominal de deuda, apoyado por crecimiento de EBITDA (Model Builder; Valuation Reviewer).
- **Liquidez**: mejora progresiva (1,32x → 1,48x), consistente con mayor holgura de circulante en balance (Model Builder; Valuation Reviewer).
- **Servicio de deuda**: cobertura de intereses holgada (~9,5x), mitigando riesgo de tensión financiera por coste de financiación (Model Builder; Valuation Reviewer).

**Nota de trazabilidad/limitación**: aunque existen magnitudes clave y ratios, el Valuation Reviewer solicita para completar la visión de repago: **calendario de vencimientos 2025–2029 (foco 2027)** y **generación de caja/FCF** (CFO, CapEx, variación de circulante) (Valuation Reviewer, data_requests_priority).

---

## 5. Señales externas (noticias, litigios, cambios societarios)

> Fuentes: *Expansión* (2025-05-15) y *El Economista* (2025-12-01), según base interna (Market Researcher).

- **Expansión internacional / capex**: apertura de **primera planta en Polonia (Wroclaw)** con **inversión ~€9m** y capacidad ~120 empleados (Market Researcher).  
  - Riesgos asociados: **ramp-up**, desviaciones de coste/plazo/calidad, riesgos laborales, logística transfronteriza y cumplimiento regulatorio local; potencial **presión de caja** por capex (Market Researcher).

- **Concentración comercial y ciclo sectorial**: renovación/ampliación de contratos con **dos fabricantes alemanes** con ingresos asegurados **>€15m hasta 2027** (Market Researcher).  
  - Riesgos asociados: **concentración de clientes**, presión de márgenes por poder de negociación OEM/tier1, riesgo de penalizaciones por desempeño, exposición al **ciclo de automoción alemana** y shocks macro/geopolíticos europeos (Market Researcher).

---

## 6. Evaluación de riesgo (riesgos, mitigantes, comparativa con historial)

### 6.1. Riesgos identificados

- **Riesgo de Cumplimiento/KYC (alto, condicionante)**  
  - **Cadena UBO incompleta** para el socio corporativo (35%) (KYC Screener, R-OWN-02 FAIL).  
  - **Sin IDs vigentes** de UBO PF/administradores (KYC Screener, R-ID-01 FAIL).  
  - **Sin PEP/sanciones** (screening **NO_CONCLUYENTE**) (KYC Screener, R-PEP-01 FAIL; screening_conclusion).  
  - **Sin CRS/FATCA** y **sin fuente de fondos/riqueza** (KYC Screener, R-TAX-01 FAIL; R-SOF-01 FAIL).  
  - Implicación: no debería avanzarse a formalización sin **cierre documental y screening** conforme a política interna.

- **Riesgo operativo/ejecución (medio)**  
  - Nueva planta en Polonia con capex relevante (~€9m): riesgo de ramp-up y desviaciones (Market Researcher).

- **Riesgo comercial/sectorial (medio)**  
  - Dependencia de automoción alemana y potencial **concentración** en dos clientes (Market Researcher).

- **Riesgo de refinanciación/estructura de deuda (medio, a monitorizar)**  
  - Necesidad de visibilidad sobre **vencimientos y covenants**, con foco en “optimización de estructura de deuda” hacia **2027** (Valuation Reviewer, interpretacion y data_requests_priority).

### 6.2. Mitigantes y fortalezas

- **Métricas financieras consistentes**: apalancamiento moderado (~2,1x), **liquidez en mejora** y **cobertura de intereses holgada** (Model Builder; Valuation Reviewer).
- **Historial bancario positivo**: **0 impagos**, operaciones al corriente y **rating interno A-**; incidencias menores ya subsanadas (Valuation Reviewer, interpretacion).  
- **Visibilidad comercial** hasta 2027 por contratos >€15m (aunque con riesgo de concentración) (Market Researcher).

### 6.3. Comparativa con historial

- La lectura actual es coherente con un perfil históricamente sólido (rating interno **A-**, sin impagos), pero el **paquete KYC actual no alcanza estándar** por faltantes críticos (Valuation Reviewer; KYC Screener).  
- La expansión internacional introduce un vector de riesgo adicional respecto a un escenario “base” doméstico (Market Researcher).

---

## 7. Recomendación (para decisión del analista)

**Recomendación técnica: APROBAR CON CONDICIONES** (sujeto a cierre de Cumplimiento y a información financiera adicional clave).

**Racional**:
- A favor: ratios 2022–2024 muestran **capacidad de repago cómoda** (Debt/EBITDA ~2,07x; cobertura intereses ~9,5x; liquidez ~1,48x) y **buen comportamiento bancario** (Model Builder; Valuation Reviewer).
- En contra/condicionantes: **alertas KYC críticas** (UBO corporativo sin cadena, ausencia de IDs, PEP/sanciones no realizado, CRS/FATCA y SoF/SoW no aportados) que impiden concluir elegibilidad de cumplimiento (KYC Screener). Además, expansión con capex y concentración sectorial requieren **monitorización** (Market Researcher).

> La decisión final corresponde al analista humano/comité, una vez verificado el cierre de condiciones.

---

## 8. Condiciones y próximos pasos (si aplica)

### 8.1. Condiciones de Cumplimiento (previas a formalización / desembolso)
- **Completar cadena de titularidad** de **Acme Europe Holding GmbH (35%)** hasta **beneficiario final persona física**, con documentación soporte (KYC Screener, R-OWN-02 FAIL).
- Aportar **documentos de identidad vigentes** (DNI/pasaporte) de **Roberto Acme Jiménez** y **Klaus Meier** (KYC Screener, R-ID-01 FAIL).
- Ejecutar y documentar **screening PEP/sanciones** para entidad, UBOs y administradores + **declaración PEP** (KYC Screener, R-PEP-01 FAIL; screening_conclusion NO_CONCLUYENTE).
- Aportar **CRS/FATCA** (y otros formularios fiscales aplicables) (KYC Screener, R-TAX-01 FAIL).
- Aportar **Fuente de fondos/riqueza** (declaración y evidencias: contratos principales, explicación de operativa, origen de aportaciones si aplica) (KYC Screener, R-SOF-01 FAIL).
- Aportar **prueba de domicilio** actualizada (≤ 3 meses) (KYC Screener, R-ADDR-01 WARN).

### 8.2. Información financiera adicional (para completar análisis de repago)
- **Detalle de deuda** por instrumento (CP/LP), **calendario de amortización 2025–2029**, tipos (fijo/variable), coberturas y **covenants**, con foco en **2027** (Valuation Reviewer, data_requests_priority).
- **Generación de caja y FCF 2022–2024**: CFO, CapEx, variación de circulante; desglose de **clientes/inventario/proveedores** para validar necesidad de circulante (Valuation Reviewer, data_requests_priority).

### 8.3. Monitorización recomendada (post-aprobación)
- Seguimiento trimestral del **ramp-up de la planta en Polonia** (costes, productividad, calidad, hitos regulatorios) (Market Researcher).
- Seguimiento de **concentración de clientes** y evolución del sector automoción alemán (Market Researcher).
- Revisión anual de **apalancamiento y liquidez** con objetivo de mantener Debt/EBITDA en rango prudente (~2–2,5x) y cobertura de intereses holgada, en línea con el histórico observado (Valuation Reviewer; Model Builder).