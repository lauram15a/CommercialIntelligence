# Informe de riesgo - Datalyx Iberia SL

## Resumen ejecutivo
Datalyx Iberia SL presenta un expediente societario consistente (nombre y NIF coherentes) y con titulares reales/administradores identificados según el **KYC Screener Agent** (escritura 2018-02-14, expediente actualizado en 2025). La principal brecha KYC es la **ausencia de documentos de identidad (DNI) de personas físicas** (regla KYC-001 en FAIL). En lo financiero (2022–2024), el negocio muestra crecimiento de ingresos y EBITDA, con apalancamiento moderado y métricas de liquidez y cobertura de intereses en mejora, según **Model Builder** y **Valuation Reviewer**. Existen **flags de consistencia** por saltos relevantes en patrimonio neto (2022–2023) y activo corriente (2023–2024) que requieren validación contra fuente. En señales externas, el **Market Researcher** no encontró información pública negativa en las fuentes consultadas (no concluyente).

## Validación KYC
- **KYC-001 – Documento de identidad presente: FAIL**  
  **Evidencia:** “no se encontró ningún documento tipo ‘dni’” (según KYC Screener Agent).  
  **Implicación:** brecha material para identificación/verificación de administradores y/o titulares reales personas físicas; requiere obtención de DNI/NIE/pasaporte vigente y verificación.
- **KYC-003 – Consistencia de nombre legal entre documentos: PASS**  
  **Evidencia:** nombres encontrados: “Datalyx Iberia SL” (KYC Screener Agent).
- **KYC-004 – Titular real identificado: PASS**  
  **Evidencia:** titulares reales presentes en escritura: **Sofía Datalyx Ferrer**, **Nordic Capital Iberia BV**, **Marc Ribera Vidal** (KYC Screener Agent).
- **KYC-005 – Información financiera presente: PASS**  
  **Evidencia:** balances con datos financieros 2022–2024 (KYC Screener Agent).

## Análisis financiero
- **Modelo financiero normalizado (periodos disponibles):** 2022, 2023 y 2024 con EBITDA, deuda financiera, activo/pasivo corriente, patrimonio neto, ingresos y gastos financieros completos (según **Model Builder Agent**).  
- **Audit_flags (a validar contra documentos fuente):**  
  - Salto relevante en **patrimonio neto** 2022 (2,2M) → 2023 (3,8M) (Model Builder).  
  - Salto relevante en **activo corriente** 2023 (4,1M) → 2024 (6,2M) (Model Builder).
- **Ratios clave y evolución (según Valuation Reviewer Agent):**
  - **Debt/EBITDA:** 1,36x (2022) → 1,27x (2023) → 1,25x (2024)  
  - **Liquidez corriente (Activo corriente/Pasivo corriente):** 2,33x → 2,56x → 2,95x  
  - **Cobertura de intereses (EBITDA/Gastos financieros):** 12,94x → 15,00x → 16,55x
- **Interpretación (Valuation Reviewer, con matiz):**  
  La compañía muestra **crecimiento** (ingresos 8,2M → 11,5M → 15,0M; EBITDA 1,1M → 1,65M → 2,4M) con **apalancamiento contenido** y mejora de liquidez y cobertura. No obstante, los **saltos señalados por Model Builder** sugieren revisar si hubo cambios de perímetro, reclasificaciones o efectos extraordinarios antes de extrapolar tendencias. El Valuation Reviewer indica además historial con el banco con **2 operaciones vigentes al corriente (impagos=0, incidencias=0)**.

## Screening (sanciones / PEP / adverse media)
Resultados por parte (según **KYC Screener Agent**):
- **Datalyx Iberia SL:** sin hits. **Nota:** “fichero de sanciones no encontrado” (screening en local_db).  
- **Sofía Datalyx Ferrer:** sin hits. **Nota:** “fichero de sanciones no encontrado”.  
- **Marc Ribera Vidal:** sin hits. **Nota:** “fichero de sanciones no encontrado”.  
- **Nordic Capital Iberia BV:** sin hits. **Nota:** “fichero de sanciones no encontrado”.  

**Implicación:** aunque no hay coincidencias, el screening **no es concluyente** por falta de acceso/actualización del fichero de sanciones; requiere **re-screening** en fuentes oficiales/proveedor corporativo antes de cierre KYC.

## Señales externas
Según el **Market Researcher Agent**, no se encontraron resultados públicos en las fuentes consultadas sobre Datalyx Iberia SL relativos a noticias negativas, concurso, litigios o eventos corporativos relevantes; tampoco sobre las partes relacionadas consultadas en conexión directa con la entidad. Se debe interpretar como **ausencia de hallazgos en las fuentes consultadas**, no como ausencia de riesgo.

## Recomendaciones
- **Cerrar brecha KYC (prioritario):** solicitar y verificar **DNI/NIE/pasaporte** vigente de **Sofía Datalyx Ferrer** y **Marc Ribera Vidal** (y de cualquier titular real PF aplicable), y evidenciar verificación (KYC-001 en FAIL).
- **Re-screening formal:** repetir screening de **sanciones/PEP/adverse media** en herramienta/proveedor actualizado (la ejecución actual indica “fichero de sanciones no encontrado”).
- **Validación de consistencia financiera:** contrastar contra balances fuente/depósito de cuentas los **saltos** en patrimonio neto (2022–2023) y activo corriente (2023–2024); documentar explicación (p.ej., ampliación de capital, reclasificaciones, cambio de perímetro).
- **Covenants/monitorización (si procede en la operación):** considerar covenants informativos (entrega anual de cuentas) y financieros básicos (p.ej., Debt/EBITDA máximo) alineados con el perfil observado, y seguimiento de liquidez.
- **Escalado a Cumplimiento:** elevar para sign-off por (i) **FAIL KYC-001** y (ii) necesidad de **screening concluyente** previo a cierre.  

Estas recomendaciones son propuestas; la decisión final corresponde al analista y al comité de riesgos.