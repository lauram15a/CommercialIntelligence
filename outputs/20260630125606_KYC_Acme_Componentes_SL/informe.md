## 1) Resumen ejecutivo

Acme Componentes SL presenta un **perfil crediticio globalmente sólido** para segmento industrial, con **apalancamiento moderado y estable** (Debt/EBITDA ~**2,1x**) y **cobertura de intereses holgada** (>**8x**) en 2022–2024 (fuente: *Valuation Reviewer Agent* sobre datos financieros internos). No obstante, el expediente KYC contiene **incidencias materiales de cumplimiento**: **cadena de titularidad incompleta** del UBO corporativo (**FAIL R-OWN-02**), **ausencia de IDs vigentes** (**FAIL R-ID-01**), **falta de formularios fiscales** (**FAIL R-TAX-01**) y **screening PEP/sanciones no concluyente con alertas** (PEP para Klaus Meier y adverse media para Acme Europe Holding GmbH; **screening_conclusion: ALERTA**) (fuente: *KYC Screener Agent*). En señales externas, destaca una **expansión internacional con CAPEX relevante (~€9m) en Polonia** y **mayor dependencia de clientes alemanes del sector automoción** (fuente: *Market Researcher Agent*). Recomendación técnica: **ESCALAR** para cierre de KYC/screening y validación de estructura de deuda y plan de caja asociado al CAPEX; una vez mitigado, el caso sería **apto para APROBAR CON CONDICIONES** desde la óptica financiera (fuente: integración de *Valuation Reviewer* + *KYC Screener* + *Market Researcher*).

---

## 2) Identificación de la empresa (datos registrales, administración, titulares reales)

- **Nombre legal:** Acme Componentes SL (fuente: *KYC Screener*, R-ENT-01, escritura_constitucion.txt)  
- **Forma jurídica:** **Sociedad de Responsabilidad Limitada** (fuente: *KYC Screener*, R-ENT-01)  
- **NIF/CIF:** **B50123987** (fuente: *KYC Screener*, R-ENT-01)  
- **Domicilio social:** **Polígono Malpica, Calle E nº 18, 50016 Zaragoza** (fuente: *KYC Screener*, R-ENT-01)  
- **Fecha de constitución:** **2003-07-10** (fuente: *KYC Screener*, R-ENT-01)  
- **Actividad:** Industrial, **CNAE 2562 (tratamiento y revestimiento de metales)** (fuente: *KYC Screener*, R-SOF-01; *Model Builder*, tendencias_estructurales)  
- **Plantilla:** **310 empleados** (fuente: *Model Builder*, tendencias_estructurales)

**Administración / control**
- **Roberto Acme Jiménez** — **Consejero Delegado** (fuente: *KYC Screener*, R-CTRL-01)  
- **Klaus Meier** — **Consejero**, representante de Acme Europe (fuente: *KYC Screener*, R-CTRL-01)

**Titulares reales (UBO) declarados**
- **Roberto Acme Jiménez:** **65,0%** (control por propiedad) (fuente: *KYC Screener*, R-OWN-01)  
- **Acme Europe Holding GmbH:** **35,0%** (control por propiedad) (fuente: *KYC Screener*, R-OWN-01)  
- **Incidencia:** no consta **cadena de titularidad** del UBO corporativo hasta persona física final (fuente: *KYC Screener*, **FAIL R-OWN-02**).

---

## 3) Hallazgos KYC (resultado de cada regla, alertas de screening)

### 3.1 Resultado por reglas KYC (según expediente)
- **R-ENT-01 Identificación entidad:** **PASS** (nombre, CIF, forma jurídica, domicilio, constitución) (fuente: *KYC Screener*, evidencia escritura_constitucion.txt).  
- **R-OWN-01 UBOs declarados con %:** **PASS** (65% PF + 35% holding) (fuente: *KYC Screener*).  
- **R-OWN-02 Cadena UBO corporativo hasta PF final:** **FAIL** (no aportada para Acme Europe Holding GmbH) (fuente: *KYC Screener*).  
- **R-CTRL-01 Administradores identificados:** **PASS** (Roberto Acme Jiménez; Klaus Meier) (fuente: *KYC Screener*).  
- **R-ID-01 IDs vigentes admins/UBOs PF:** **FAIL** (no se incluyen DNI/pasaporte vigentes) (fuente: *KYC Screener*).  
- **R-ADDR-01 Prueba de domicilio actualizada:** **WARN** (domicilio consta, falta soporte reciente ≤3 meses) (fuente: *KYC Screener*).  
- **R-TAX-01 CRS/FATCA u otros:** **FAIL** (no aportados) (fuente: *KYC Screener*).  
- **R-SOF-01 Fuente de fondos/riqueza:** **WARN** (coherencia operativa por balances, pero sin declaración/documentación explícita) (fuente: *KYC Screener*).  
- **R-FIN-01 Estados financieros recientes:** **PASS** (2022–2024 disponibles) (fuente: *KYC Screener*).  
- **R-PEP-01 Declaración PEP y screening PEP/sanciones:** **FAIL** (no consta declaración ni resultados concluyentes) (fuente: *KYC Screener*).

### 3.2 Screening (PEP/sanciones/adverse media) — estado y alertas
- **Conclusión de screening:** **ALERTA**; 2 coincidencias en 4 entidades revisadas (fuente: *KYC Screener*, screening_resumen/screening_conclusion).  
- **Acme Componentes SL:** sin hits en fuente local; **non_conclusive** (requiere repetición en fuentes operativas actualizadas) (fuente: *KYC Screener*, screening_results).  
- **Roberto Acme Jiménez:** sin hits en fuente local; **non_conclusive** (fuente: *KYC Screener*).  
- **Klaus Meier:** **hit PEP** (exfuncionario Ministerio de Economía alemán 2014–2018), sin sanciones activas; **review_required** (fuente: *KYC Screener*, screening_results).  
- **Acme Europe Holding GmbH:** **adverse media** (investigación prácticas fiscales 2021, caso cerrado sin condena); **review_required** (fuente: *KYC Screener*, screening_results).  
- **Nota operativa:** el propio screener indica que el resultado está basado en **fuente local** y debe repetirse en listas **UE/OFAC/ONU/HMT** o proveedor interno para cierre concluyente (fuente: *KYC Screener*, note por entidad).

---

## 4) Análisis financiero (evolución de ratios clave, tendencias)

### 4.1 Magnitudes operativas y de deuda (2022–2024)
Datos cargados desde base de datos interna (fuente: *Model Builder Agent*, periodos):
- **EBITDA:** 2022 **€3,8m** → 2023 **€4,9m** → 2024 **€5,8m**  
- **Deuda financiera:** 2022 **€8,0m** → 2023 **€10,5m** → 2024 **€12,0m**  
- **Activo corriente:** 2022 **€9,5m** → 2023 **€12,1m** → 2024 **€14,5m**  
- **Pasivo corriente:** 2022 **€7,2m** → 2023 **€8,9m** → 2024 **€9,8m**  
- **Gastos financieros:** 2022 **€0,45m** → 2023 **€0,52m** → 2024 **€0,61m**

### 4.2 Ratios de crédito (2022–2024) y lectura
Ratios calculados (fuente: *Valuation Reviewer Agent*, ratios_por_periodo):
- **Debt/EBITDA:** 2022 **2,11x** → 2023 **2,14x** → 2024 **2,07x** (**-1,7%** vs. 2022; ligera mejora)  
- **Liquidez corriente (AC/PC):** 2022 **1,32x** → 2023 **1,36x** → 2024 **1,48x** (tendencia positiva)  
- **Cobertura de intereses (EBITDA/Gastos fin.):** 2022 **8,44x** → 2023 **9,42x** → 2024 **9,51x** (holgada)

**Interpretación integrada**
- **Solvencia/apalancamiento:** nivel **moderado** y estable (~2,1x), compatible con perfil industrial corporativo (fuente: *Valuation Reviewer*).  
- **Liquidez:** mejora progresiva del ratio corriente, sugiriendo mayor colchón de circulante (fuente: *Valuation Reviewer*).  
- **Servicio de deuda:** cobertura de intereses >8x, consistente con capacidad de absorción de subidas de tipos o volatilidad moderada (fuente: *Valuation Reviewer*).  
- **Punto de atención:** incremento de deuda 2022→2024 (+€4,0m) en paralelo a crecimiento de EBITDA; requiere trazabilidad con **CAPEX/expansión** y calendario de vencimientos (fuente: *Model Builder* + *Valuation Reviewer* + *Market Researcher*).

---

## 5) Señales externas (noticias, litigios, cambios societarios relevantes)

### 5.1 Expansión internacional (Polonia) — riesgo de ejecución y caja
- **Hecho:** inauguración de **primera planta en Polonia (Wroclaw)**.  
- **Inversión estimada:** **~€9m**, capacidad **120 empleados**.  
- **Fuente/fecha:** *Expansión*, **2025-05-15** (fuente: *Market Researcher Agent*).  
- **Implicaciones de riesgo:** ramp-up productivo, cumplimiento regulatorio/laboral local, presión de liquidez por CAPEX, riesgos de supply chain y potencial **riesgo FX** PLN/EUR (fuente: *Market Researcher*).

### 5.2 Concentración de clientes y exposición a automoción alemana
- **Hecho:** renovación/ampliación de contratos con **dos fabricantes alemanes**; ingresos asegurados **>€15m hasta 2027**.  
- **Fuente/fecha:** *El Economista*, **2025-12-01** (fuente: *Market Researcher*).  
- **Implicaciones de riesgo:** concentración, presión de precios/penalizaciones por calidad, exposición al ciclo automoción (incl. transición EV), riesgo de volúmenes/cancelación (fuente: *Market Researcher*).  
- **Mitigante externo:** visibilidad de ingresos hasta 2027 y potencial mejora logística/coste por planta en Polonia (fuente: *Market Researcher*).

---

## 6) Evaluación de riesgo (riesgos identificados, mitigantes, comparativa con historial)

### 6.1 Riesgos principales identificados
**Riesgo de Cumplimiento/KYC (alto impacto, previo a decisión)**
- **UBO corporativo sin cadena hasta PF final** (**FAIL R-OWN-02**) (fuente: *KYC Screener*).  
- **IDs vigentes no aportados** (**FAIL R-ID-01**) (fuente: *KYC Screener*).  
- **Fiscales CRS/FATCA no aportados** (**FAIL R-TAX-01**) (fuente: *KYC Screener*).  
- **PEP/adverse media con screening no concluyente**: Klaus Meier **PEP** y Acme Europe Holding GmbH **adverse media**; necesidad de verificación en fuentes operativas (fuente: *KYC Screener*, screening_results + notes).

**Riesgo financiero (moderado, gestionable con condiciones)**
- **Apalancamiento** moderado (~2,1x) pero con **deuda creciente**; requiere confirmar si el CAPEX (Polonia) está ya reflejado y su financiación (fuente: *Model Builder* + *Market Researcher*).  
- **Riesgo de refinanciación/vencimientos** a partir de 2027 (mencionado como foco de seguimiento) (fuente: *Valuation Reviewer*, interpretacion/conclusions).  

**Riesgo operativo/estratégico (moderado)**
- **Ramp-up** de nueva planta y complejidad multi-planta (fuente: *Market Researcher*).  
- **Concentración de clientes** y exposición a automoción alemana (fuente: *Market Researcher*).

### 6.2 Mitigantes observados
- **Ratios de servicio de deuda sólidos** (cobertura intereses >8x) y **liquidez corriente en mejora** (fuente: *Valuation Reviewer*).  
- **Visibilidad comercial** por contratos hasta 2027 (>€15m) (fuente: *Market Researcher*).  
- **Historial bancario positivo:** **0 impagos**, operaciones al corriente, **rating interno A-** (fuente: *Valuation Reviewer*, interpretacion).

### 6.3 Comparativa con historial
- El comportamiento histórico descrito (sin impagos, rating A-) es **coherente** con los ratios 2022–2024 (apalancamiento contenido y cobertura holgada). El principal diferencial respecto al histórico es el **incremento de complejidad y CAPEX** por expansión internacional, que puede tensionar caja si el ramp-up se retrasa (fuente: *Valuation Reviewer* + *Market Researcher*).

---

## 7) Recomendación (APROBAR / APROBAR CON CONDICIONES / DENEGAR / ESCALAR)

**Recomendación: ESCALAR** (a Cumplimiento/KYC y Riesgos) **antes de formalizar** por incidencias KYC materiales y screening no concluyente con alertas:
- **FAIL R-OWN-02** (cadena UBO corporativo), **FAIL R-ID-01**, **FAIL R-TAX-01**, **FAIL R-PEP-01** y **ALERTA** en screening (fuente: *KYC Screener*).

**Vista financiera (condicionada a cierre KYC):** una vez resueltas las incidencias, el perfil financiero soportaría una **APROBACIÓN CON CONDICIONES** orientadas a control de vencimientos, caja y ejecución del CAPEX (fuente: *Valuation Reviewer* + *Model Builder* + *Market Researcher*).  
> La decisión final corresponde al analista humano y al circuito de aprobación del banco.

---

## 8) Condiciones y próximos pasos (si aplica)

### 8.1 Cierre KYC / Cumplimiento (prioridad alta)
- Aportar **cadena de titularidad completa** de **Acme Europe Holding GmbH** hasta **persona(s) física(s) final(es)**, con % y base de control (fuente: *KYC Screener*, FAIL R-OWN-02).  
- Aportar **documentos de identidad vigentes** de **Roberto Acme Jiménez** y **Klaus Meier** (y UBO PF final de la holding, cuando se identifique) (fuente: *KYC Screener*, FAIL R-ID-01).  
- Aportar **CRS/FATCA** y formularios fiscales aplicables según política interna (fuente: *KYC Screener*, FAIL R-TAX-01).  
- Ejecutar **screening en fuentes operativas actualizadas** (UE/OFAC/ONU/HMT y/o proveedor interno) para: entidad, UBOs y administradores; documentar conclusión sobre **PEP (Klaus Meier)** y **adverse media (Acme Europe Holding GmbH)** (fuente: *KYC Screener*, screening_results + notes).  
- Completar **declaración y evidencias de fuente de fondos/riqueza** (p.ej., principales clientes/contratos, desglose de ingresos, origen de aportaciones) (fuente: *KYC Screener*, WARN R-SOF-01).  
- Aportar **prueba de domicilio** actualizada (nota simple/registro mercantil reciente o recibo ≤3 meses) (fuente: *KYC Screener*, WARN R-ADDR-01).

### 8.2 Información financiera / estructuración (prioridad media-alta)
Solicitudes alineadas con el revisor de valoración:
- **Detalle de deuda por instrumento**, tipo (fijo/variable), **calendario de amortización 2026–2029** y **covenants** (fuente: *Valuation Reviewer*, data_requests_priority).  
- Evidencia de **generación de caja**: **CFO, CapEx, variación de circulante** 2022–2024 y YTD 2025; uso/disponibilidad de líneas de circulante/confirming (fuente: *Valuation Reviewer*, data_requests_priority).  
- Vincular el **CAPEX ~€9m** (planta Polonia) a: presupuesto, hitos, contingencias, y plan de financiación; incluir análisis de sensibilidad de ramp-up (fuente: *Market Researcher*).

### 8.3 Condiciones típicas sugeridas (si se aprueba tras cierre KYC)
- **Covenant de apalancamiento** (p.ej., Debt/EBITDA máximo) y/o **cobertura de intereses mínima**, coherentes con niveles históricos observados (fuente: *Valuation Reviewer*, ratios).  
- **Reporting trimestral** de desempeño de la planta en Polonia (capex ejecutado vs presupuesto, OEE/scrap, plantilla, cumplimiento) durante fase de ramp-up (fuente: *Market Researcher*).  
- Revisión anual de **concentración de clientes** y condiciones contractuales clave (volúmenes, penalizaciones, revisiones de precio) (fuente: *Market Researcher*).