## 1. Resumen ejecutivo

Acme Componentes SL presenta un **perfil crediticio globalmente favorable** por **apalancamiento moderado y estable** (Debt/EBITDA ~2,1x), **liquidez corriente en mejora** (1,32x → 1,48x) y **cobertura de intereses sólida** (~8,4x → ~9,5x) en 2022–2024, junto con **historial bancario sin impagos** y **rating interno A-**. No obstante, el expediente muestra **alertas KYC relevantes**: **PEP potencial (Klaus Meier)** y **adverse media** sobre el socio corporativo **Acme Europe Holding GmbH**, además de **brechas documentales** (cadena UBO del socio corporativo, IDs vigentes, CRS/FATCA y declaración/resultado formal de screening). En señales externas, destaca la **expansión con planta en Polonia (capex ~€9m)** y **concentración comercial** en dos OEM alemanes con contratos hasta 2027, lo que introduce **riesgo de ejecución** y **dependencia sectorial (automoción)**. Recomendación: **APROBAR CON CONDICIONES** (condiciones KYC y de información financiera/deuda), dejando la decisión final al analista humano.

---

## 2. Identificación de la empresa

- **Nombre legal**: Acme Componentes SL  
  **Fuente**: KYC Screener, *escritura_constitucion.txt* (R-ENT-01)
- **Forma jurídica**: **Sociedad de Responsabilidad Limitada**  
  **Fuente**: KYC Screener, *escritura_constitucion.txt* (R-ENT-01)
- **NIF/CIF**: **B50123987**  
  **Fuente**: KYC Screener, *escritura_constitucion.txt* (R-ENT-01)
- **Domicilio social**: **Polígono Malpica, Calle E nº 18, 50016 Zaragoza**  
  **Fuente**: KYC Screener, *escritura_constitucion.txt* (R-ENT-01)
- **Fecha de constitución**: **2003-07-10**  
  **Fuente**: KYC Screener, *escritura_constitucion.txt* (R-ENT-01)
- **Actividad**: Industrial, **CNAE 2562 (tratamiento y revestimiento de metales)**  
  **Fuente**: KYC Screener (R-SOF-01) y Model Builder (*tendencias_estructurales*)
- **Plantilla (referencial)**: **310 empleados**  
  **Fuente**: Model Builder (*tendencias_estructurales*)

**Administración / control**
- **Roberto Acme Jiménez** — **Consejero Delegado**  
  **Fuente**: KYC Screener, *escritura_constitucion.txt* (R-CTRL-01)
- **Klaus Meier** — **Consejero** (representante de Acme Europe)  
  **Fuente**: KYC Screener, *escritura_constitucion.txt* (R-CTRL-01)

**Titulares reales (UBO) declarados**
- **Roberto Acme Jiménez** — **65,0%** (control por participación)  
  **Fuente**: KYC Screener, *escritura_constitucion.txt* (R-OWN-01)
- **Acme Europe Holding GmbH** — **35,0%** (UBO corporativo)  
  **Fuente**: KYC Screener, *escritura_constitucion.txt* (R-OWN-01)

---

## 3. Hallazgos KYC (resultado por regla y screening)

### 3.1 Reglas KYC (KYC Screener)
- **R-ENT-01 Identificación completa entidad**: **PASS**  
  Evidencia: nombre, CIF, forma jurídica, domicilio y constitución.  
  **Fuente**: *escritura_constitucion.txt* (R-ENT-01)
- **R-OWN-01 UBOs declarados con %**: **PASS**  
  **Fuente**: *escritura_constitucion.txt* (R-OWN-01)
- **R-OWN-02 Cadena de titularidad UBO corporativo hasta PF final**: **FAIL** (**brecha crítica**)  
  Falta identificar beneficiario final persona física de **Acme Europe Holding GmbH (35%)**.  
  **Fuente**: *escritura_constitucion.txt* (R-OWN-02)
- **R-CTRL-01 Administradores/controladores identificados**: **PASS**  
  **Fuente**: *escritura_constitucion.txt* (R-CTRL-01)
- **R-ID-01 IDs vigentes de administradores y UBO PF**: **FAIL**  
  No constan DNI/pasaporte vigentes de Roberto Acme Jiménez ni Klaus Meier.  
  **Fuente**: KYC Screener (R-ID-01)
- **R-ADDR-01 Prueba de domicilio reciente (≤3 meses)**: **WARN**  
  Consta domicilio, pero no prueba reciente/fecha de emisión.  
  **Fuente**: KYC Screener (R-ADDR-01)
- **R-TAX-01 Formularios fiscales (CRS/FATCA, etc.)**: **FAIL**  
  **Fuente**: KYC Screener (R-TAX-01)
- **R-SOF-01 Fuente de fondos/riqueza documentada**: **WARN**  
  Actividad y operativa coherentes con balances, pero sin declaración/documentación explícita de SoF/SoW.  
  **Fuente**: KYC Screener (R-SOF-01)
- **R-FIN-01 Información financiera reciente**: **PASS** (balances 2022–2024)  
  **Fuente**: *balance_2022.txt, balance_2023.txt, balance_2024.txt* (R-FIN-01)
- **R-PEP-01 Declaración PEP y screening PEP/sanciones**: **FAIL** (no consta declaración ni resultado formal)  
  **Fuente**: KYC Screener (R-PEP-01)

### 3.2 Screening (base local; requiere cierre en fuente operativa)
- **Acme Componentes SL**: sin hits en base local (**non_conclusive**)  
  **Fuente**: KYC Screener, *screening_results* (local_db)
- **Roberto Acme Jiménez**: sin hits en base local (**non_conclusive**)  
  **Fuente**: KYC Screener, *screening_results* (local_db)
- **Acme Europe Holding GmbH**: **hit adverse media** (conf. 0,71): investigación prácticas fiscales 2021 (Alemania), **caso cerrado sin condena** (**review_required**)  
  **Fuente**: KYC Screener, *screening_results* (local_db)
- **Klaus Meier**: **hit PEP** (conf. 0,78): exfuncionario Ministerio de Economía alemán (2014–2018), sin sanciones activas (**review_required**)  
  **Fuente**: KYC Screener, *screening_results* (local_db)

**Conclusión de screening del expediente**: **ALERTA** (2 coincidencias/4) y necesidad de **re-screening en listas operativas actualizadas (UE/OFAC/ONU/HMT y/o proveedor interno)**.  
**Fuente**: KYC Screener, *screening_resumen* y *screening_conclusion*

---

## 4. Análisis financiero (ratios, evolución y tendencias)

> Base: métricas 2022–2024 cargadas desde **base de datos interna** (Model Builder) y ratios calculados (Valuation Reviewer).

### 4.1 Magnitudes operativas y de deuda (selección)
- **EBITDA**: €3,8m (2022) → €4,9m (2023) → €5,8m (2024)  
  **Fuente**: Model Builder, *periodos*
- **Deuda financiera**: €8,0m (2022) → €10,5m (2023) → €12,0m (2024)  
  **Fuente**: Model Builder, *periodos*
- **Activo corriente / Pasivo corriente**:  
  - 2022: €9,5m / €7,2m  
  - 2023: €12,1m / €8,9m  
  - 2024: €14,5m / €9,8m  
  **Fuente**: Model Builder, *periodos*
- **Gastos financieros**: €0,45m (2022) → €0,52m (2023) → €0,61m (2024)  
  **Fuente**: Model Builder, *periodos*

### 4.2 Ratios clave (2022–2024)
- **Debt/EBITDA**: 2,11x (2022) → 2,14x (2023) → 2,07x (2024)  
  Variación 2022–2024: **-1,7%** (ligera mejora)  
  **Fuente**: Valuation Reviewer, *ratios_por_periodo* y *variacion*
- **Liquidez corriente**: 1,32x → 1,36x → 1,48x (mejora sostenida)  
  **Fuente**: Valuation Reviewer, *ratios_por_periodo*
- **Cobertura de intereses (EBITDA/Gastos financieros)**: 8,44x → 9,42x → 9,51x (sólida y creciente)  
  **Fuente**: Valuation Reviewer, *ratios_por_periodo*

### 4.3 Lectura crediticia de la evolución
- **Apalancamiento**: moderado y estable (~2,1x), compatible con perfil industrial; mejora ligera en 2024 pese a mayor deuda absoluta.  
  **Fuente**: Valuation Reviewer, *interpretacion*
- **Liquidez**: mejora del colchón de circulante (current ratio 1,32x → 1,48x).  
  **Fuente**: Valuation Reviewer, *interpretacion*
- **Servicio de deuda**: cobertura de intereses alta (~9x), sugiere resiliencia ante subida de coste financiero en el periodo observado.  
  **Fuente**: Valuation Reviewer, *interpretacion*

**Limitación de alcance (para trazabilidad)**: aunque hay balances 2022–2024, el propio Model Builder indica que para una lectura completa se recomienda disponer de **PyG y flujos de caja**, además de detalle de circulante y deuda.  
**Fuente**: Model Builder, *interpretacion*; Valuation Reviewer, *data_requests_priority*

---

## 5. Señales externas (noticias, litigios, cambios societarios)

### 5.1 Expansión internacional (operativo/capex)
- **Inauguración de primera planta en Polonia (Wroclaw)**, capacidad 120 empleados, **inversión ~€9m**.  
  Implicaciones: riesgo de ramp-up, presión de caja por capex, cumplimiento regulatorio local y complejidad de supply chain.  
  **Fuente**: Market Researcher, *Expansión* (2025-05-15)

### 5.2 Concentración comercial y exposición a automoción
- Renovación/ampliación de contratos con **dos fabricantes alemanes**, asegurando **ingresos >€15m hasta 2027**.  
  Implicaciones: mitigante por visibilidad de ingresos; riesgo por concentración, presión de precios y exigencias de calidad/entrega típicas de OEM.  
  **Fuente**: Market Researcher, *El Economista* (2025-12-01)

### 5.3 Señales reputacionales (screening)
- **Adverse media** sobre **Acme Europe Holding GmbH** (investigación fiscal 2021; caso cerrado sin condena).  
  **Fuente**: KYC Screener, *screening_results* (local_db)
- **PEP** potencial: **Klaus Meier** (exfuncionario 2014–2018).  
  **Fuente**: KYC Screener, *screening_results* (local_db)

---

## 6. Evaluación de riesgo (riesgos, mitigantes, comparativa con historial)

### 6.1 Riesgos identificados
- **Riesgo de Cumplimiento/KYC (alto impacto operativo)**:
  - **Falta cadena UBO** del socio corporativo (35%) (**R-OWN-02 FAIL**).  
  - **Falta identificación vigente** de administradores/UBO PF (**R-ID-01 FAIL**).  
  - **Falta CRS/FATCA** (**R-TAX-01 FAIL**).  
  - **PEP hit** y **adverse media** en screening local (requiere verificación en fuentes operativas).  
  **Fuentes**: KYC Screener (R-OWN-02, R-ID-01, R-TAX-01, R-PEP-01) y *screening_results*
- **Riesgo de ejecución (operativo/capex)** por puesta en marcha de planta en Polonia (ramp-up, costes, calidad, licencias).  
  **Fuente**: Market Researcher, *Expansión* (2025-05-15)
- **Riesgo sectorial y de concentración**: dependencia de automoción alemana/europea y de dos OEM (potencial presión de márgenes y riesgo de cancelación/renegociación).  
  **Fuente**: Market Researcher, *El Economista* (2025-12-01)
- **Riesgo de refinanciación/coste financiero**: aumento de deuda absoluta 2022–2024 y necesidad de vigilar vencimientos; nota de seguimiento hacia 2027.  
  **Fuente**: Valuation Reviewer, *interpretacion* y *conclusions*

### 6.2 Mitigantes
- **Ratios de crédito robustos** (apalancamiento ~2,1x; cobertura intereses ~9x; liquidez en mejora).  
  **Fuente**: Valuation Reviewer, *ratios_por_periodo* e *interpretacion*
- **Historial bancario positivo**: **0 impagos**, operaciones al corriente, **rating interno A-**; incidencias menores ya subsanadas.  
  **Fuente**: Valuation Reviewer, *interpretacion*
- **Visibilidad comercial** hasta 2027 por contratos >€15m (mitigante de demanda, sujeto a cumplimiento de calidad/servicio).  
  **Fuente**: Market Researcher, *El Economista* (2025-12-01)

### 6.3 Comparativa con historial
- La lectura actual es **consistente con un perfil favorable** (A-) y comportamiento sin impagos; el principal cambio a vigilar es el **incremento de deuda** y el **riesgo de ejecución** asociado a la expansión internacional.  
  **Fuente**: Valuation Reviewer, *interpretacion*; Market Researcher, *Expansión* (2025-05-15)

---

## 7. Recomendación (para decisión del analista)

**Recomendación propuesta: APROBAR CON CONDICIONES**.

**Racional**:
- **A favor**: métricas de apalancamiento, liquidez y cobertura de intereses **compatibles con concesión** y **historial bancario sólido** (0 impagos, A-).  
  **Fuente**: Valuation Reviewer, *ratios* e *interpretacion*
- **Condicionantes**: existen **brechas KYC** (UBO corporativo sin cadena, IDs, CRS/FATCA, PEP/screening formal) y **alertas de screening** (PEP y adverse media) que requieren **cierre de Cumplimiento** antes de formalizar/activar.  
  **Fuente**: KYC Screener, *kyc_results* y *screening_results*
- **Seguimiento**: expansión en Polonia y concentración en OEM alemanes justifican **covenants/monitorización** y revisión de plan de financiación/capex.  
  **Fuente**: Market Researcher (noticias) y Valuation Reviewer (foco en vencimientos)

> La decisión final corresponde al analista humano y a Cumplimiento, una vez completadas las verificaciones y documentación pendiente.

---

## 8. Condiciones y próximos pasos (si aplica)

### 8.1 Condiciones KYC/Cumplimiento (previas a formalización o desembolso)
- **Completar cadena de titularidad** de **Acme Europe Holding GmbH** hasta **beneficiario(s) final(es) persona física** y documentación soporte.  
  **Fuente**: KYC Screener (R-OWN-02 FAIL)
- Aportar **documentos de identidad vigentes** de **Roberto Acme Jiménez** y **Klaus Meier**.  
  **Fuente**: KYC Screener (R-ID-01 FAIL)
- Aportar **CRS/FATCA** (y formularios fiscales aplicables según operativa).  
  **Fuente**: KYC Screener (R-TAX-01 FAIL)
- Ejecutar **screening en fuentes operativas actualizadas** (UE/OFAC/ONU/HMT y/o proveedor interno) para entidad, UBOs y administradores, con **dictamen de Cumplimiento** sobre:
  - **PEP** (Klaus Meier) y medidas EDD si procede.
  - **Adverse media** (Acme Europe Holding GmbH) y conclusión documentada.  
  **Fuente**: KYC Screener (*screening_results*, *screening_conclusion*; R-PEP-01 FAIL)

### 8.2 Condiciones de información financiera / riesgo (para cierre de análisis y seguimiento)
- Entregar **detalle de deuda financiera** (instrumento, importes, tipo fijo/variable, spreads, **calendario de amortización/vencimientos**, garantías y covenants) y conciliación con operaciones bancarias.  
  **Fuente**: Valuation Reviewer, *data_requests_priority*
- Entregar **EEFF completos 2022–2024** (PyG y flujos de caja) y **desglose de capital circulante** (clientes, inventario, proveedores) para validar generación de caja y estacionalidad.  
  **Fuente**: Valuation Reviewer, *data_requests_priority*; Model Builder, *interpretacion*
- Para la expansión en Polonia: solicitar **plan de negocio del proyecto** (capex ejecutado vs. pendiente, calendario, ramp-up, contratos asociados, sensibilidad de costes) y **fuentes de financiación**.  
  **Fuente**: Market Researcher, *Expansión* (2025-05-15); KYC Screener (R-SOF-01 WARN)

### 8.3 Seguimiento sugerido (post-aprobación)
- Monitorizar trimestralmente: **Debt/EBITDA**, **cobertura de intereses**, evolución de **deuda absoluta** y **liquidez**, y cumplimiento de hitos de la planta en Polonia.  
  **Fuente**: Valuation Reviewer, *ratios*; Market Researcher (expansión)

--- 

**Anexos de trazabilidad (inputs utilizados)**  
- KYC Screener: *escritura_constitucion.txt*, *balance_2022.txt*, *balance_2023.txt*, *balance_2024.txt*; reglas R-ENT-01, R-OWN-01/02, R-CTRL-01, R-ID-01, R-ADDR-01, R-TAX-01, R-SOF-01, R-FIN-01, R-PEP-01; *screening_results* (local_db).  
- Model Builder: métricas 2022–2024 (EBITDA, deuda, activo/pasivo corriente, gastos financieros) desde base interna.  
- Valuation Reviewer: ratios (Debt/EBITDA, liquidez corriente, cobertura intereses), interpretación, historial (0 impagos, A-), y data requests.  
- Market Researcher: noticias *Expansión* (2025-05-15) y *El Economista* (2025-12-01).