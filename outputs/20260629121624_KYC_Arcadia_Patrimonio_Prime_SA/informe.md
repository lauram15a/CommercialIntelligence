## 1) Resumen ejecutivo

Arcadia Patrimonio Prime SA presenta un **riesgo de información/KYC elevado**: la documentación aportada (escritura) solo permite confirmar el **nombre legal**, pero **no** acredita **NIF/CIF, domicilio, fecha de constitución, administradores ni titulares reales (UBO)**, impidiendo completar el onboarding y el screening AML/PEP de forma concluyente (KYC Screener, *escritura_constitucion.txt*). En el plano crediticio, la relación bancaria histórica aporta señales de estabilidad operativa (**rating interno BBB+**, operaciones vigentes **al corriente**), pero **no existen estados financieros** para validar solvencia, apalancamiento, liquidez ni cobertura del servicio de deuda (Valuation Reviewer; Model Builder). No se identifican noticias/señales internas específicas en la base consultada; se recomienda un barrido externo una vez se disponga de identificadores para evitar homónimos (Market Researcher). **Recomendación técnica:** **ESCALAR** y/o **APROBAR CON CONDICIONES** estrictas de KYC y entrega financiera previa a cualquier incremento de exposición; la decisión final corresponde al analista humano.

---

## 2) Identificación de la empresa (datos registrales, administración, titulares reales)

- **Nombre legal:** Arcadia Patrimonio Prime SA  
  - **Fuente:** KYC Screener → *escritura_constitucion.txt* (R-ENT-01: consta nombre legal).
- **Forma jurídica:** inferida como **Sociedad Anónima (SA)** por denominación social “SA”.  
  - **Base de inferencia prudente:** denominación “Arcadia Patrimonio Prime SA”.  
  - **Fuente:** KYC Screener → *escritura_constitucion.txt* (no consigna forma jurídica como dato estructurado).
- **NIF/CIF:** no acreditado en expediente.  
  - **Fuente:** KYC Screener (R-ENT-01: “NIF/CIF… No consta”).
- **Domicilio social:** no acreditado en expediente.  
  - **Fuente:** KYC Screener (R-ADDR-01: “Domicilio social: No consta”).
- **Fecha de constitución:** no acreditada en expediente.  
  - **Fuente:** KYC Screener (R-ENT-01: “fecha de constitución… No consta”).
- **Administración / órgano de administración:** no identificado.  
  - **Fuente:** KYC Screener (R-CTRL-01: “ADMINISTRADORES: No consta”).
- **Titulares reales (UBO):** no declarados / no identificados.  
  - **Fuente:** KYC Screener (R-OWN-01: “TITULARES REALES (UBO): No consta”; R-OWN-02: no verificable cadena).

---

## 3) Hallazgos KYC (resultado de cada regla, alertas de screening)

**Documentación revisada:** únicamente *escritura_constitucion.txt* (KYC Screener).

### 3.1 Reglas KYC (por control)
- **R-ENT-01 Identificación completa entidad:** **FAIL**  
  - Evidencia: solo consta nombre legal; faltan NIF/CIF, forma jurídica (como campo), domicilio y fecha de constitución.  
  - **Fuente:** KYC Screener → *escritura_constitucion.txt*.
- **R-OWN-01 UBO declarados (% y control):** **FAIL**  
  - Evidencia: “TITULARES REALES (UBO): No consta”.  
  - **Fuente:** KYC Screener → *escritura_constitucion.txt*.
- **R-OWN-02 Cadena de titularidad hasta PF final:** **FAIL**  
  - Evidencia: no hay UBOs declarados; no se puede verificar cadena.  
  - **Fuente:** KYC Screener → *escritura_constitucion.txt*.
- **R-CTRL-01 Administradores/controladores identificados:** **FAIL**  
  - Evidencia: “ADMINISTRADORES: No consta”.  
  - **Fuente:** KYC Screener → *escritura_constitucion.txt*.
- **R-ID-01 IDs vigentes de admins/UBOs:** **FAIL**  
  - Evidencia: no hay admins/UBOs identificados y no se aportan documentos de identidad.  
  - **Fuente:** KYC Screener (expediente).
- **R-ADDR-01 Prueba de domicilio social:** **FAIL**  
  - Evidencia: domicilio no consta y no hay documento probatorio.  
  - **Fuente:** KYC Screener → *escritura_constitucion.txt*.
- **R-TAX-01 Formularios fiscales (CRS/FATCA, etc.):** **FAIL**  
  - Evidencia: no se aportan formularios fiscales.  
  - **Fuente:** KYC Screener (expediente).
- **R-SOF-01 Fuente de fondos/riqueza:** **FAIL**  
  - Evidencia: no hay declaración/documentación; solo observaciones internas sobre refinanciación/estructuración de deuda.  
  - **Fuente:** KYC Screener → *escritura_constitucion.txt*.
- **R-FIN-01 Información financiera reciente:** **FAIL**  
  - Evidencia: no se aportan estados financieros/cuentas anuales.  
  - **Fuente:** KYC Screener (expediente).
- **R-PEP-01 Declaración PEP y screening PEP/sanciones:** **WARN**  
  - Evidencia: no consta declaración; no hay UBOs/admins para screening; “sin alertas internas registradas en BBDD del banco”.  
  - **Fuente:** KYC Screener (R-PEP-01).

### 3.2 Screening sanciones/PEP
- **Resultado:** **NO_CONCLUYENTE** (no hay entidades/personas identificadas para revisar).  
  - **Fuente:** KYC Screener → “screening_resumen: Screening sin entidades para revisar”; “screening_conclusion: NO_CONCLUYENTE”.
- **Alertas:** no se reportan coincidencias, pero **no puede descartarse riesgo AML/PEP** por falta de UBOs/admins.  
  - **Fuente:** KYC Screener (R-PEP-01).

---

## 4) Análisis financiero (evolución de ratios clave, tendencias)

### 4.1 Disponibilidad de información y ratios
- **Ratios financieros:** no calculables (sin periodos ni estados financieros).  
  - **Fuente:** Valuation Reviewer (“No es posible calcular ratios…”); Model Builder (sin indicadores/periodos).
- **Estados financieros:** no aportados (Balance, PyG, Cash Flow).  
  - **Fuente:** KYC Screener (R-FIN-01 FAIL); Model Builder (interpretación).

### 4.2 Perfil de negocio (cualitativo) y sensibilidad
- Actividad descrita como **gestora de activos inmobiliarios terciarios en reposicionamiento**, con sensibilidad a **ciclo inmobiliario**, **ocupación** y **tipos de interés**, y potencial necesidad de financiación por proyecto (capex/circulante/deuda puente).  
  - **Fuente:** Model Builder → “tendencias_estructurales” e “interpretación”.
- **Plantilla declarada: 63 empleados**, consistente con plataforma operativa de tamaño medio.  
  - **Fuente:** Model Builder → “tendencias_estructurales”.

### 4.3 Relación bancaria y comportamiento (proxy de desempeño)
- Relación desde **2011**, **rating interno BBB+**.  
- Exposición vigente: **préstamo corporativo 5,45m€** y **línea de circulante límite 3,15m€ (dispuesto 1,71m€)**, **ambas al corriente**.  
- **1 impago histórico** (sin detalle temporal/causal en inputs).  
  - **Fuente:** Valuation Reviewer → “interpretación”.

---

## 5) Señales externas (noticias, litigios, cambios societarios relevantes)

- **Cobertura interna de noticias/señales:** *sin resultados específicos* para la entidad en la base consultada.  
  - **Fuente:** Market Researcher → “Cobertura… Sin resultados específicos”.
- Dado que faltan **identificadores (país, NIF/registro, administradores/UBO)**, el análisis externo queda limitado y se recomienda un barrido dirigido en:
  - **Registro mercantil:** cambios de administradores, domicilio, capital, estatutos, reestructuraciones, cierres registrales.  
  - **Depósito de cuentas y auditoría:** retrasos, salvedades, *going concern*.  
  - **Insolvencia/concursal:** preconcurso, concurso, refinanciaciones homologadas.  
  - **Litigios/embargos/ejecuciones**.  
  - **Sanciones/PEP/regulatorio**.  
  - **Fuente:** Market Researcher (secciones A–G y red flags).

---

## 6) Evaluación de riesgo (riesgos identificados, mitigantes, comparativa con historial)

### 6.1 Riesgos principales identificados
- **Riesgo AML/KYC crítico (alto):** imposibilidad de identificar y verificar **UBOs**, **administradores**, **domicilio** e **identificador fiscal**, dejando el screening en estado **NO_CONCLUYENTE**.  
  - **Fuente:** KYC Screener (R-ENT-01, R-OWN-01/02, R-CTRL-01, R-ADDR-01, R-PEP-01).
- **Riesgo de información financiera (alto):** ausencia total de estados financieros impide evaluar **solvencia**, **apalancamiento**, **liquidez**, **cobertura de intereses** y **calendario de vencimientos**.  
  - **Fuente:** Model Builder (interpretación); Valuation Reviewer (interpretación; data requests).
- **Riesgo sectorial (medio-alto, cualitativo):** exposición al ciclo inmobiliario terciario y a ejecución de reposicionamientos (ocupación, capex, tipos).  
  - **Fuente:** Model Builder (tendencias/interpretación); Valuation Reviewer (sensibilidad a ocupación y tipos).
- **Riesgo de comportamiento (medio):** existe **1 impago histórico** (sin detalle), aunque actualmente las operaciones están al corriente.  
  - **Fuente:** Valuation Reviewer.

### 6.2 Mitigantes observados
- **Track record bancario:** relación desde 2011 y **operaciones al corriente** (préstamo y circulante), lo que sugiere capacidad operativa de pago en el corto plazo.  
  - **Fuente:** Valuation Reviewer.
- **Rating interno BBB+** (indicador interno favorable, sujeto a actualización con información financiera).  
  - **Fuente:** Valuation Reviewer.

### 6.3 Comparativa con historial / consistencia
- La estabilidad actual (al corriente) es **consistente** con un perfil de riesgo moderado en comportamiento; sin embargo, la **brecha documental KYC y financiera** es incompatible con estándares de originación/renovación sin condiciones.  
  - **Fuente:** Valuation Reviewer (estabilidad + impago histórico); KYC Screener (fails generalizados).

---

## 7) Recomendación (APROBAR / APROBAR CON CONDICIONES / DENEGAR / ESCALAR)

**Recomendación técnica para comité:** **ESCALAR** (a Cumplimiento AML/KYC y Riesgos) y, en caso de continuidad operativa necesaria, **APROBAR CON CONDICIONES** **previas** (condiciones suspensivas) sin incremento de exposición hasta cierre documental.

**Racional trazable:**
- **KYC/AML no concluible** por falta de UBOs/admins/identificación completa (KYC Screener: múltiples FAIL; PEP WARN; screening NO_CONCLUYENTE).
- **Riesgo crediticio no validable** por ausencia de estados financieros y ratios (Model Builder; Valuation Reviewer).
- **Mitigante parcial**: comportamiento actual al corriente y rating BBB+ (Valuation Reviewer), insuficiente para compensar el riesgo de información.

> La decisión final corresponde al analista humano, considerando apetito de riesgo, materialidad de la exposición y urgencia operativa.

---

## 8) Condiciones y próximos pasos (si aplica)

### 8.1 Condiciones KYC/AML (cierre obligatorio antes de formalizar/renovar o ampliar)
- **Identificación registral completa**: NIF/CIF, domicilio social, fecha de constitución y jurisdicción/registro mercantil.  
  - **Fuente de necesidad:** KYC Screener (R-ENT-01, R-ADDR-01).
- **Administradores/apoderados**: identificación, cargos y vigencia; **IDs** vigentes.  
  - **Fuente:** KYC Screener (R-CTRL-01, R-ID-01).
- **UBO**: declaración de titulares reales con % y base de control; si hay UBO corporativo, **cadena completa** hasta persona física.  
  - **Fuente:** KYC Screener (R-OWN-01, R-OWN-02).
- **Declaración y screening PEP/sanciones** para entidad, UBOs y administradores, con resolución de homónimos.  
  - **Fuente:** KYC Screener (R-PEP-01; screening NO_CONCLUYENTE).
- **Fuente de fondos/riqueza (SoF/SoW)** documentada y coherente con actividad y operaciones.  
  - **Fuente:** KYC Screener (R-SOF-01).

### 8.2 Condiciones financieras (mínimo para análisis de solvencia)
- **Estados financieros completos** (Balance, PyG, Cash Flow) de **2–3 ejercicios** y último cierre disponible, con detalle de EBITDA y gastos financieros.  
  - **Fuente:** Valuation Reviewer (data_requests_priority #1); Model Builder (interpretación).
- **Detalle de deuda**: saldos, tipos, covenants, garantías, calendario de vencimientos y conciliación con operaciones bancarias activas.  
  - **Fuente:** Valuation Reviewer (data_requests_priority #2).

### 8.3 Señales externas (cierre reputacional/legal)
- Una vez se disponga de **NIF/registro y jurisdicción**, ejecutar barrido externo dirigido (registro mercantil, depósito de cuentas, concursal, litigios, sanciones/PEP) para confirmar **hallazgos vs. no hallazgos** con fechas.  
  - **Fuente:** Market Researcher (limitaciones y próximos pasos).

--- 

**Anexos / trazabilidad de inputs utilizados**
- KYC Screener Agent → *escritura_constitucion.txt* + reglas R-ENT-01, R-OWN-01/02, R-CTRL-01, R-ID-01, R-ADDR-01, R-TAX-01, R-SOF-01, R-FIN-01, R-PEP-01; screening_conclusion NO_CONCLUYENTE.  
- Model Builder Agent → tendencias_estructurales (actividad inmobiliaria terciaria en reposicionamiento; 63 empleados) e interpretación (sin estados financieros).  
- Valuation Reviewer Agent → relación desde 2011, rating BBB+, operaciones (5,45m€ préstamo; 3,15m€ línea/1,71m€ dispuesto) al corriente; 1 impago histórico; data requests.  
- Market Researcher Agent → sin señales internas específicas; checklist de barrido externo y red flags.