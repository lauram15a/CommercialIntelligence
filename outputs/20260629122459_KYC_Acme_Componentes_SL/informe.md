## 1) Resumen ejecutivo

Acme Componentes SL presenta un **perfil bancario históricamente favorable** (operaciones al corriente, **0 impagos** y **rating interno A-**), pero la **evaluación cuantitativa de solvencia, liquidez y capacidad de repago** queda **no validada** por ausencia de magnitudes financieras en el modelo consolidado (ratios no calculables). En KYC existen **alertas relevantes**: **screening PEP/sanciones NO CONCLUYENTE** por falta de ejecución/documentación, **falta de cadena de titularidad** del socio corporativo (35%) y **ausencia de IDs** de administradores/UBO persona física. A nivel de negocio, las señales externas apuntan a **crecimiento y mayor complejidad operativa** por apertura de planta en Polonia (inversión ~€9m) y **potencial concentración** por contratos con OEMs alemanes hasta 2027 (>€15m). Recomendación técnica: **ESCALAR** para cierre KYC/screening y completar información financiera antes de cualquier decisión de incremento de riesgo.

---

## 2) Identificación de la empresa

- **Nombre legal**: Acme Componentes SL  
  **Fuente**: KYC Screener, regla **R-ENT-01** (evidencia: *escritura_constitucion.txt*).
- **Forma jurídica**: **Sociedad de Responsabilidad Limitada**  
  **Fuente**: KYC Screener **R-ENT-01** (*escritura_constitucion.txt*).
- **NIF/CIF**: **B50123987**  
  **Fuente**: KYC Screener **R-ENT-01** (*escritura_constitucion.txt*).
- **Domicilio social**: **Polígono Malpica, Calle E nº 18, 50016 Zaragoza**  
  **Fuente**: KYC Screener **R-ENT-01** (*escritura_constitucion.txt*).
- **Fecha de constitución**: **2003-07-10**  
  **Fuente**: KYC Screener **R-ENT-01** (*escritura_constitucion.txt*).
- **Actividad**: Industrial (**CNAE 2562: tratamiento y revestimiento de metales**)  
  **Fuente**: KYC Screener **R-SOF-01** (actividad referida) + Model Builder (tendencias estructurales).
- **Administración / control**:
  - **Roberto Acme Jiménez** — **Consejero Delegado**  
  - **Klaus Meier** — **Consejero** (representante de Acme Europe)  
  **Fuente**: KYC Screener **R-CTRL-01** (*escritura_constitucion.txt*).
- **Titulares reales (UBO) declarados**:
  - **Roberto Acme Jiménez** — **65.0%** (base: participación)
  - **Acme Europe Holding GmbH (Alemania)** — **35.0%** (base: participación)  
  **Fuente**: KYC Screener **R-OWN-01** (*escritura_constitucion.txt*).

---

## 3) Hallazgos KYC (resultado por regla y alertas)

### 3.1 Resultado de reglas KYC
- **R-ENT-01 (Identificación entidad)**: **PASS**  
  Evidencia: *escritura_constitucion.txt* (nombre, CIF, forma jurídica, domicilio, constitución).
- **R-OWN-01 (UBOs declarados con % y base)**: **PASS**  
  Evidencia: *escritura_constitucion.txt* (65% PF + 35% holding).
- **R-OWN-02 (Cadena de titularidad UBO corporativo hasta PF final)**: **FAIL**  
  **Alerta**: **no se aporta cadena de titularidad/beneficiario final** de **Acme Europe Holding GmbH (35%)**.  
  Evidencia: KYC Screener **R-OWN-02** (*escritura_constitucion.txt*).
- **R-CTRL-01 (Administradores identificados)**: **PASS**  
  Evidencia: *escritura_constitucion.txt*.
- **R-ID-01 (IDs vigentes admins/UBOs PF)**: **FAIL**  
  **Alerta**: faltan **DNI/pasaporte y vigencia** de **Roberto Acme Jiménez** y **Klaus Meier**.  
  Evidencia: KYC Screener **R-ID-01**.
- **R-ADDR-01 (Prueba de domicilio actual)**: **WARN**  
  Base: domicilio consta en escritura, pero falta **prueba reciente** (nota simple/recibo ≤3 meses).  
  Evidencia: KYC Screener **R-ADDR-01**.
- **R-TAX-01 (CRS/FATCA u otros)**: **FAIL**  
  **Alerta**: no constan formularios fiscales aplicables.  
  Evidencia: KYC Screener **R-TAX-01**.
- **R-SOF-01 (Fuente de fondos/riqueza)**: **WARN**  
  Base: actividad industrial y EEFF sugieren generación operativa, pero falta **declaración/documentación explícita** (contratos, detalle ingresos, origen aportaciones).  
  Evidencia: KYC Screener **R-SOF-01**.
- **R-FIN-01 (EEFF recientes)**: **PASS**  
  Evidencia: *balance_2022.txt, balance_2023.txt, balance_2024.txt* (disponibles en expediente; validados internamente).
- **R-PEP-01 (Declaración PEP + screening PEP/sanciones)**: **FAIL**  
  **Alerta crítica**: no consta **declaración** ni **resultados de screening** para entidad/UBOs/administradores.  
  Evidencia: KYC Screener **R-PEP-01**.

### 3.2 Screening (PEP/sanciones/adverse media)
- **Resultado**: **NO_CONCLUYENTE**  
- **Detalle**: “Screening sin entidades para revisar” (no se ejecutó/registró screening en el expediente).  
  **Fuente**: KYC Screener (*screening_conclusion* y *screening_resumen*).

---

## 4) Análisis financiero (evolución de ratios clave, tendencias)

### 4.1 Disponibilidad y limitaciones del modelo
- Existen estados financieros 2022–2024 en el expediente (**balance_2022.txt, balance_2023.txt, balance_2024.txt**), pero el **modelo consolidado recibido no incluye magnitudes** (ventas, EBITDA/resultado, deuda financiera, caja, circulante, gastos financieros), por lo que **no se han calculado ratios**.  
  **Fuente**: Model Builder (*interpretacion*: “no se han aportado aún cifras…”) + Valuation Reviewer (*interpretacion*: ratios no calculables).

### 4.2 Ratios no calculables (impacto en decisión)
No es posible validar, con trazabilidad cuantitativa:
- **Apalancamiento**: **Debt/EBITDA**  
- **Liquidez**: **ratio corriente**, prueba ácida, caja neta  
- **Servicio de deuda**: **cobertura de intereses** / DSCR  
- **Capital circulante**: rotación de existencias, DSO/DPO y necesidades de financiación  
**Fuente**: Valuation Reviewer (*interpretacion* y *conclusions.data_requests_priority*).

### 4.3 Señales internas de comportamiento bancario (cualitativas)
- **0 impagos**, operaciones vigentes **al corriente**, relación activa con productos de **circulante, CAPEX y confirming**; incidencias menores ya subsanadas.  
- **Rating interno A-**.  
**Fuente**: Valuation Reviewer (*interpretacion*).

> Inferencia prudente (para comité): el comportamiento bancario y rating sugieren **riesgo actual contenido**, pero **no sustituye** la validación de capacidad de repago ante potencial aumento de CAPEX/expansión (ver señales externas).

---

## 5) Señales externas (noticias, litigios, cambios societarios relevantes)

### 5.1 Expansión internacional (Polonia)
- **Inauguración de primera planta en Polonia (Wroclaw)**, capacidad **120 empleados**, inversión aproximada **€9m**.  
  **Fuente**: Market Researcher, *Expansión* (2025-05-15).
- Implicaciones de riesgo:
  - **Riesgo de ejecución/ramp-up** industrial (calidad, OEE, homologaciones).
  - **Riesgo de desviaciones de CAPEX/OPEX** y presión de costes (energía/logística).
  - **Riesgo regulatorio/laboral** local y continuidad operativa.  
  **Fuente**: Market Researcher (análisis asociado a la señal).

### 5.2 Contratos y concentración (automoción Alemania)
- Renovación/ampliación de contratos con **dos fabricantes alemanes**, asegurando **>€15m de ingresos hasta 2027**.  
  **Fuente**: Market Researcher, *El Economista* (2025-12-01).
- Implicaciones de riesgo:
  - **Concentración de clientes** y exposición a recortes/renegociaciones.
  - Riesgo sectorial por **ciclo automoción europea** y presión de precios.  
  **Fuente**: Market Researcher.

### 5.3 Riesgo regional / continuidad / FX (derivado)
- Mayor exposición a Europa Central (energía, logística, regulación); posible **riesgo FX PLN/EUR** si existiera descalce (no confirmado).  
  **Fuente**: Market Researcher (señal derivada).

---

## 6) Evaluación de riesgo (riesgos, mitigantes, comparativa con historial)

### 6.1 Riesgos identificados
- **Riesgo de Cumplimiento (KYC/AML) — Alto (procedimental)**  
  - **Screening PEP/sanciones NO CONCLUYENTE** y **sin declaración PEP** (**R-PEP-01 FAIL**).  
  - **Cadena de titularidad incompleta** del UBO corporativo extranjero (**R-OWN-02 FAIL**).  
  - **Falta de IDs vigentes** de administradores/UBO PF (**R-ID-01 FAIL**).  
  - **Falta de formularios fiscales** (**R-TAX-01 FAIL**) y **prueba de domicilio actual** (**R-ADDR-01 WARN**).  
  **Fuente**: KYC Screener (reglas citadas).
- **Riesgo financiero — Medio/No validable**  
  - No se puede confirmar apalancamiento, liquidez ni cobertura por **ausencia de cifras** en el modelo consolidado.  
  **Fuente**: Model Builder + Valuation Reviewer.
- **Riesgo operativo/ejecución — Medio**  
  - Ramp-up de nueva planta en Polonia con inversión relevante (posible presión de caja y costes fijos).  
  **Fuente**: Market Researcher (*Expansión* 2025-05-15).
- **Riesgo de concentración/sectorial — Medio**  
  - Dependencia de dos clientes alemanes y sensibilidad al ciclo de automoción.  
  **Fuente**: Market Researcher (*El Economista* 2025-12-01).

### 6.2 Mitigantes observados
- **Historial bancario positivo**: **0 impagos**, operaciones al corriente; incidencias menores subsanadas.  
  **Fuente**: Valuation Reviewer.
- **Rating interno A-** (indicador de riesgo contenido en histórico interno).  
  **Fuente**: Valuation Reviewer.
- **Contratos con visibilidad hasta 2027** (>€15m) pueden aportar estabilidad de ingresos, sujeto a condiciones contractuales (indexación/penalizaciones).  
  **Fuente**: Market Researcher.

### 6.3 Comparativa con historial (visión de continuidad)
- Frente a un histórico interno favorable (rating A-, sin impagos), el **perfil de riesgo incremental** viene por:
  - **Mayor complejidad operativa** (nueva planta internacional).
  - **Necesidad de validar** que la estructura financiera soporta CAPEX y circulante asociado.
  - **Brechas KYC** que impiden cierre de cumplimiento.  
  **Fuente**: Valuation Reviewer + Market Researcher + KYC Screener.

---

## 7) Recomendación (para decisión del analista)

**Recomendación: ESCALAR** (a Cumplimiento/AML y a Riesgos de Crédito) **antes de aprobar** nueva exposición o modificaciones relevantes.

**Argumentos trazables**:
- **KYC crítico pendiente**: **R-PEP-01 FAIL** (screening no concluido), **R-OWN-02 FAIL** (UBO corporativo sin cadena), **R-ID-01 FAIL** (IDs), **R-TAX-01 FAIL**.  
  **Fuente**: KYC Screener.
- **Riesgo financiero no cuantificado**: ratios clave no calculables por falta de magnitudes en el modelo consolidado.  
  **Fuente**: Model Builder + Valuation Reviewer.
- **Riesgo de ejecución** por expansión en Polonia (CAPEX ~€9m) que puede tensionar liquidez si el ramp-up se retrasa.  
  **Fuente**: Market Researcher (*Expansión* 2025-05-15).

> La decisión final corresponde al analista humano una vez completados los puntos de Cumplimiento y la validación financiera.

---

## 8) Condiciones y próximos pasos (si aplica)

### 8.1 Cierre KYC/AML (condiciones previas)
- Ejecutar y documentar **screening PEP/sanciones/adverse media** para:
  - **Acme Componentes SL**
  - **Roberto Acme Jiménez**
  - **Klaus Meier**
  - **Acme Europe Holding GmbH**  
  **Base**: **R-PEP-01 FAIL** y screening **NO_CONCLUYENTE** (KYC Screener).
- Aportar **cadena de titularidad completa** de **Acme Europe Holding GmbH** hasta **persona(s) física(s) beneficiaria(s) final(es)** (con % y control).  
  **Base**: **R-OWN-02 FAIL** (KYC Screener).
- Aportar **documentos de identidad vigentes** (y verificación de vigencia) de **Roberto Acme Jiménez** y **Klaus Meier**.  
  **Base**: **R-ID-01 FAIL** (KYC Screener).
- Aportar **formularios fiscales** aplicables (**CRS/FATCA** u otros según criterio de Cumplimiento).  
  **Base**: **R-TAX-01 FAIL** (KYC Screener).
- Aportar **prueba de domicilio actual** (nota simple/registro reciente o recibo ≤3 meses).  
  **Base**: **R-ADDR-01 WARN** (KYC Screener).
- Formalizar **declaración y soporte de fuente de fondos/riqueza** (p.ej., explicación de origen de aportaciones, principales contratos/ingresos).  
  **Base**: **R-SOF-01 WARN** (KYC Screener).

### 8.2 Información financiera (para decisión de crédito)
- Remitir estados financieros 2022–2024 **con cifras** (balance + PyG) y, preferiblemente, memoria/nota de deuda.  
- Desglose de **deuda financiera** (corto/largo), **caja**, **gastos financieros** y **calendario de vencimientos** (incl. confirming y líneas).  
- Detalle de **activo/pasivo corriente** (clientes, existencias, proveedores) para evaluar **capital circulante**.  
  **Base**: solicitudes prioritarias del Valuation Reviewer (*conclusions.data_requests_priority*) y limitaciones del Model Builder.

### 8.3 Foco de seguimiento por señales externas
- Evidencias de **ramp-up** en Polonia (hitos, calidad, OTIF, certificaciones) y control de desviaciones CAPEX/OPEX.  
- Revisión de **contratos** con OEMs alemanes: indexación, pass-through, penalizaciones, duración efectiva y concentración.  
  **Base**: Market Researcher (observaciones para el analista).

--- 

**Anexos / Trazabilidad de fuentes (inputs del pipeline)**  
- KYC Screener: *escritura_constitucion.txt*, *balance_2022.txt*, *balance_2023.txt*, *balance_2024.txt*; reglas R-ENT-01, R-OWN-01/02, R-CTRL-01, R-ID-01, R-ADDR-01, R-TAX-01, R-SOF-01, R-FIN-01, R-PEP-01.  
- Valuation Reviewer: interpretación de comportamiento bancario, rating A-, y lista de data requests.  
- Market Researcher: *Expansión* (2025-05-15) y *El Economista* (2025-12-01) con implicaciones de riesgo.