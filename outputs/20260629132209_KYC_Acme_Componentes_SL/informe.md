## 1) Resumen ejecutivo

Acme Componentes SL presenta un **perfil crediticio globalmente sólido** para un industrial corporate, con **apalancamiento moderado y estable** (Debt/EBITDA ~**2,1x** en 2022–2024) y **capacidad holgada de servicio de deuda** (cobertura de intereses **>8x**), junto con **mejora de liquidez** (corriente **1,32x → 1,48x**). En señales externas, destaca un **plan de expansión internacional** (planta en Polonia, **9M€** de inversión) que introduce **riesgo de ejecución/capex**, parcialmente mitigado por **visibilidad comercial** (contratos en Alemania con ingresos **>15M€ hasta 2027**). En KYC, existen **brechas relevantes**: **cadena UBO incompleta** para el socio corporativo extranjero (35%), **ausencia de IDs** de administradores/UBO PF, **screening PEP/sanciones no concluyente** (solo fuente local) y falta de **CRS/FATCA**. Recomendación orientativa: **APROBAR CON CONDICIONES** (cierre KYC + información de deuda/covenants), dejando la decisión final al analista/comité.

---

## 2) Identificación de la empresa

- **Nombre legal**: Acme Componentes SL  
  **Fuente**: KYC Screener, R-ENT-01 (escritura_constitucion.txt)
- **Forma jurídica**: **Sociedad de Responsabilidad Limitada**  
  **Fuente**: KYC Screener, R-ENT-01 (escritura_constitucion.txt)
- **NIF/CIF**: **B50123987**  
  **Fuente**: KYC Screener, R-ENT-01 (escritura_constitucion.txt)
- **Domicilio social**: **Polígono Malpica, Calle E nº 18, 50016 Zaragoza**  
  **Fuente**: KYC Screener, R-ENT-01 (escritura_constitucion.txt)
- **Fecha de constitución**: **2003-07-10**  
  **Fuente**: KYC Screener, R-ENT-01 (escritura_constitucion.txt)
- **Actividad**: industrial (CNAE **2562**: tratamiento y revestimiento de metales)  
  **Fuente**: KYC Screener, R-SOF-01 (escritura_constitucion.txt); Model Builder (tendencias_estructurales)
- **Plantilla**: **310 empleados** (dato operativo)  
  **Fuente**: Model Builder (tendencias_estructurales)

**Administración / control**
- **Roberto Acme Jiménez** — **Consejero Delegado**  
  **Fuente**: KYC Screener, R-CTRL-01 (escritura_constitucion.txt)
- **Klaus Meier** — **Consejero** (representante de Acme Europe)  
  **Fuente**: KYC Screener, R-CTRL-01 (escritura_constitucion.txt)

**Titulares reales (UBO) declarados**
- **Roberto Acme Jiménez** — **65,0%** (control por propiedad)  
  **Fuente**: KYC Screener, R-OWN-01 (escritura_constitucion.txt)
- **Acme Europe Holding GmbH** — **35,0%** (control por propiedad)  
  **Fuente**: KYC Screener, R-OWN-01 (escritura_constitucion.txt)

---

## 3) Hallazgos KYC (resultado por regla y alertas de screening)

### 3.1 Reglas KYC
- **R-ENT-01 (Identificación entidad)**: **PASS**  
  Evidencia: nombre, CIF, forma jurídica, domicilio y constitución.  
  **Fuente**: KYC Screener (escritura_constitucion.txt)
- **R-OWN-01 (UBOs declarados con %)**: **PASS**  
  **Fuente**: KYC Screener (escritura_constitucion.txt)
- **R-OWN-02 (Cadena UBO corporativo hasta PF final)**: **FAIL** — **ALERTA KYC**  
  Falta cadena de titularidad/beneficiario final PF de **Acme Europe Holding GmbH (35%)**.  
  **Fuente**: KYC Screener, R-OWN-02 (escritura_constitucion.txt)
- **R-CTRL-01 (Administradores identificados)**: **PASS**  
  **Fuente**: KYC Screener, R-CTRL-01 (escritura_constitucion.txt)
- **R-ID-01 (IDs vigentes admins/UBO PF)**: **FAIL** — **ALERTA KYC**  
  No constan DNI/pasaporte de **Roberto Acme Jiménez** ni **Klaus Meier**.  
  **Fuente**: KYC Screener, R-ID-01
- **R-ADDR-01 (Prueba de domicilio ≤3 meses)**: **WARN**  
  Consta domicilio en escritura, falta prueba actual (nota registral/recibo reciente).  
  **Fuente**: KYC Screener, R-ADDR-01
- **R-TAX-01 (CRS/FATCA / formularios fiscales)**: **FAIL** — **ALERTA KYC**  
  No se aportan formularios fiscales aplicables.  
  **Fuente**: KYC Screener, R-TAX-01
- **R-SOF-01 (Fuente de fondos/riqueza)**: **WARN**  
  Actividad y estados financieros coherentes, pero falta declaración/documentación explícita de SoF/SoW.  
  **Fuente**: KYC Screener, R-SOF-01
- **R-FIN-01 (Información financiera reciente)**: **PASS**  
  Estados 2022–2024 disponibles (validación interna).  
  **Fuente**: KYC Screener, R-FIN-01; Model Builder (resumen)
- **R-PEP-01 (Declaración PEP y screening PEP/sanciones)**: **FAIL** — **ALERTA KYC/COMPLIANCE**  
  No consta declaración ni resultados concluyentes de screening.  
  **Fuente**: KYC Screener, R-PEP-01

### 3.2 Screening sanciones/PEP/adverse media (según inputs)
- Entidades/personas revisadas: **Acme Componentes SL**, **Acme Europe Holding GmbH**, **Klaus Meier**, **Roberto Acme Jiménez**
- Resultado: sin hits en **fuente local**, pero **no concluyente**; requiere repetición en fuentes operativas actualizadas (UE/OFAC/ONU/HMT y/o proveedor interno).  
  **Fuente**: KYC Screener (screening_results; confidence: non_conclusive)

---

## 4) Análisis financiero (evolución de ratios clave, tendencias)

> Nota de trazabilidad: cifras y ratios provienen de **base de datos interna** (Model Builder) y cálculo de ratios (Valuation Reviewer).

### 4.1 Magnitudes operativas (proxy de capacidad)
- **EBITDA**: 3,8M€ (2022) → 4,9M€ (2023) → 5,8M€ (2024)  
  **Fuente**: Model Builder (periodos)
- **Deuda financiera**: 8,0M€ (2022) → 10,5M€ (2023) → 12,0M€ (2024)  
  **Fuente**: Model Builder (periodos)
- **Gastos financieros**: 0,45M€ (2022) → 0,52M€ (2023) → 0,61M€ (2024)  
  **Fuente**: Model Builder (periodos)

### 4.2 Ratios de apalancamiento, liquidez y cobertura
- **Debt/EBITDA**: **2,11x** (2022) → **2,14x** (2023) → **2,07x** (2024)  
  Variación 2022–2024: **-1,73%** (ligera mejora).  
  **Fuente**: Valuation Reviewer (ratios; variacion)
- **Liquidez corriente (Activo corriente/Pasivo corriente)**: **1,32x** (2022) → **1,36x** (2023) → **1,48x** (2024)  
  **Fuente**: Valuation Reviewer (ratios_por_periodo)
- **Cobertura de intereses (EBITDA/Gastos financieros)**: **8,44x** (2022) → **9,42x** (2023) → **9,51x** (2024)  
  **Fuente**: Valuation Reviewer (ratios_por_periodo)

### 4.3 Lectura de tendencia (para comité)
- **Apalancamiento**: estable en torno a **~2,1x**, compatible con perfil industrial con inversión; la deuda crece, pero el EBITDA crece en paralelo.  
  **Fuente**: Model Builder (periodos) + Valuation Reviewer (interpretacion)
- **Liquidez**: mejora progresiva del ratio corriente, sugiriendo mayor holgura de circulante a cierre de 2024.  
  **Fuente**: Valuation Reviewer (ratios_por_periodo)
- **Coste financiero**: aumento de gastos financieros, sin deterioro de cobertura (se mantiene holgada).  
  **Fuente**: Model Builder (gastos_financieros) + Valuation Reviewer (cobertura_intereses)
- **Comportamiento bancario**: historial reportado como **0 impagos** y operaciones al corriente; incidencias menores de documentación/auditoría subsanadas.  
  **Fuente**: Valuation Reviewer (interpretacion)

---

## 5) Señales externas (noticias, litigios, cambios societarios relevantes)

- **Expansión internacional (Polonia, Wroclaw)**: apertura de primera planta, **120 empleados** de capacidad, **9M€** de inversión.  
  Implicación: **riesgo de ejecución/ramp-up** y presión de caja si hay retrasos o baja utilización; también riesgo regulatorio/laboral en nueva jurisdicción.  
  **Fuente**: Market Researcher (Expansión, 2025-05-15)
- **Contratos Alemania (automoción)**: renovación/ampliación con dos fabricantes alemanes; **ingresos >15M€ hasta 2027**.  
  Implicación: **mitigante de visibilidad** de ingresos, pero eleva **riesgo de concentración** y exposición al ciclo de automoción (volúmenes, pricing, KPIs de calidad/entrega).  
  **Fuente**: Market Researcher (El Economista, 2025-12-01)

---

## 6) Evaluación de riesgo (riesgos identificados, mitigantes, comparativa con historial)

### 6.1 Riesgos principales
- **Riesgo KYC/Compliance (material)**:
  - **Cadena UBO incompleta** para socio corporativo extranjero (**35%**) (**R-OWN-02 FAIL**).  
  - **IDs no aportados** de administradores/UBO PF (**R-ID-01 FAIL**).  
  - **PEP/sanciones no concluyente** y sin declaración formal (**R-PEP-01 FAIL**; screening solo local_db).  
  - **CRS/FATCA no aportado** (**R-TAX-01 FAIL**).  
  **Fuente**: KYC Screener (kyc_results; screening_results)
- **Riesgo de inversión y ejecución (capex)** por nueva planta en Polonia (ramp-up, calidad, productividad, permisos, costes).  
  **Fuente**: Market Researcher (Expansión, 2025-05-15)
- **Riesgo de concentración/ciclo (automoción)**: dependencia de pocos contratos y exposición a OEMs alemanes (renegociación, presión de márgenes, penalizaciones por KPIs).  
  **Fuente**: Market Researcher (El Economista, 2025-12-01)
- **Riesgo de endeudamiento incremental**: deuda financiera sube 2022→2024; aunque ratios se mantienen, conviene validar **estructura, vencimientos, covenants y tipo fijo/variable**.  
  **Fuente**: Model Builder (deuda_financiera) + Valuation Reviewer (data_requests_priority)

### 6.2 Mitigantes observados
- **Capacidad de repago**: cobertura de intereses **>8x** y apalancamiento **~2,1x** con ligera mejora.  
  **Fuente**: Valuation Reviewer (ratios; interpretacion)
- **Liquidez en mejora** (ratio corriente hasta **1,48x** en 2024).  
  **Fuente**: Valuation Reviewer (ratios_por_periodo)
- **Visibilidad comercial** hasta 2027 por contratos reportados (**>15M€**).  
  **Fuente**: Market Researcher (El Economista, 2025-12-01)
- **Historial bancario** sin impagos y operaciones al corriente (según revisión).  
  **Fuente**: Valuation Reviewer (interpretacion)

### 6.3 Comparativa con historial (según inputs internos)
- Se reporta **consistencia** con perfil previo: sin señales de estrés (0 impagos), incidencias menores ya subsanadas; se menciona contratación de **cobertura de tipos** por nominal elevado (indicativo de gestión de riesgo de tipos y/o exposición a deuda variable).  
  **Fuente**: Valuation Reviewer (interpretacion)

---

## 7) Recomendación (no vinculante)

**Recomendación orientativa: APROBAR CON CONDICIONES**.

**Racional** (para decisión del analista/comité):
- **A favor**: métricas de crédito **sólidas** (Debt/EBITDA ~2,1x; cobertura >8x; liquidez al alza) y **buen comportamiento bancario** reportado.  
  **Fuente**: Valuation Reviewer (ratios, interpretacion); Model Builder (periodos)
- **A vigilar**: **capex y ramp-up** en Polonia y **concentración** en automoción; potencial presión de caja si la ejecución se retrasa.  
  **Fuente**: Market Researcher (ambas noticias)
- **Condicionante**: **brechas KYC/Compliance materiales** (UBO corporativo sin cadena PF final, IDs, PEP/sanciones concluyente, CRS/FATCA).  
  **Fuente**: KYC Screener (R-OWN-02, R-ID-01, R-PEP-01, R-TAX-01; screening non_conclusive)

---

## 8) Condiciones y próximos pasos (si aplica)

### 8.1 Condiciones KYC/Compliance (previas a disposición o dentro de plazo corto, según política interna)
- Completar **cadena de titularidad** de **Acme Europe Holding GmbH** hasta **persona física final** (documentación societaria y declaración UBO).  
  **Fuente**: KYC Screener, R-OWN-02 (FAIL)
- Aportar **documentos de identidad vigentes** de **Roberto Acme Jiménez** y **Klaus Meier** (y UBO PF final del socio corporativo cuando se identifique).  
  **Fuente**: KYC Screener, R-ID-01 (FAIL)
- Ejecutar y archivar **screening PEP/sanciones** en **fuentes operativas actualizadas** (UE/OFAC/ONU/HMT y/o proveedor interno) para entidad, UBOs y administradores, junto con **declaración PEP**.  
  **Fuente**: KYC Screener (R-PEP-01 FAIL; screening_results non_conclusive)
- Aportar **CRS/FATCA** (y formularios fiscales aplicables).  
  **Fuente**: KYC Screener, R-TAX-01 (FAIL)
- Aportar **prueba de domicilio** actual (≤3 meses) o nota registral actualizada.  
  **Fuente**: KYC Screener, R-ADDR-01 (WARN)
- Formalizar **fuente de fondos/riqueza** (declaración y soporte: contratos principales, detalle de ingresos, origen de aportaciones/capex).  
  **Fuente**: KYC Screener, R-SOF-01 (WARN)

### 8.2 Condiciones financieras / información para cierre de análisis (prioridad alta)
- Entregar **desglose de deuda** (corto/largo, fijo/variable), **calendario de vencimientos**, **covenants**, **garantías** y conciliación con operaciones activas.  
  **Fuente**: Valuation Reviewer (data_requests_priority)
- Remitir **estados financieros completos 2022–2024** (PyG, balance y cash flow) y **detalle de capital circulante** (clientes/inventario/proveedores) para validar generación de caja y estacionalidad.  
  **Fuente**: Valuation Reviewer (data_requests_priority)

### 8.3 Seguimiento de riesgos de negocio (post-disposición / covenant de información)
- Reporting trimestral del **avance de la planta en Polonia** (capex ejecutado vs plan, ramp-up, KPIs de calidad/entrega, utilización).  
  **Fuente**: Market Researcher (Expansión, 2025-05-15)
- Información de **concentración de clientes** y desempeño de contratos (top clientes, % ventas, KPIs, cláusulas de revisión de precio).  
  **Fuente**: Market Researcher (El Economista, 2025-12-01)

--- 

**Nota para el analista**: el perfil financiero soporta una visión favorable, pero la **regularización KYC/Compliance** (especialmente **UBO corporativo** y **screening concluyente**) debe considerarse condición necesaria para una decisión operativa conforme a política interna.