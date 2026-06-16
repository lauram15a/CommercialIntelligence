# Informe de riesgo - Nexuria Tech Solutions SL

## Resumen ejecutivo
Nexuria Tech Solutions SL (NIF B66123409) presenta documentación societaria y estados financieros 2022–2024 legibles y consistentes en nombre legal (según KYC Screener Agent). En KYC, el principal gap es la ausencia de documentos de identidad (DNI) en el paquete, pese a que se identifican titulares reales y administradores. Financiera y operativamente, muestra fuerte crecimiento de ingresos (2,1M → 5,6M) y EBITDA (280k → 950k), con liquidez holgada y buena cobertura de intereses (según Model Builder y Valuation Reviewer). El apalancamiento se mantiene en rango moderado (~2,1x Debt/EBITDA) con repunte en 2024 por mayor deuda. No se detectan señales externas negativas en las fuentes consultadas (Market Researcher), pero el screening interno no pudo validar sanciones por falta de fichero/feeds (KYC Screener).

## Validación KYC
- **KYC-001 – Documento de identidad presente: FAIL**. Evidencia: “no se encontró ningún documento tipo ‘dni’” (KYC Screener Agent).  
  - **Implicación:** no se puede completar la verificación de identidad de personas físicas (administradores/titulares reales) con el estándar requerido; requiere subsanación antes de cierre de onboarding/refresh.
- **KYC-003 – Consistencia de nombre legal entre documentos: PASS**. Evidencia: nombres encontrados: “Nexuria Tech Solutions SL” (KYC Screener Agent).
- **KYC-004 – Titular real identificado: PASS**. Evidencia: “titulares reales presentes” (KYC Screener Agent). Titulares reales listados: Adrián Nexuria Pujol, Laura Morales Sanz y Vertex Ventures Spain SL (según escritura 2019-11-05).
- **KYC-005 – Información financiera presente: PASS**. Evidencia: “balance/PyG encontrado” (KYC Screener Agent), con balances 2022–2024.

## Análisis financiero
- **Modelo financiero normalizado:** 3 periodos (2022, 2023, 2024) con EBITDA, deuda financiera, activo/pasivo corriente, patrimonio neto, ingresos y gastos financieros completos (Model Builder Agent).  
- **Audit flags (Model Builder):**
  - Salto >100% en **EBITDA** 2022→2023 (~121%): revisar posible cambio de criterio o error de extracción.
  - Salto ~100% en **deuda financiera** 2022→2023: revisar posible error de extracción/escala.
- **Ratios clave y evolución (Valuation Reviewer Agent):**
  - **Debt/EBITDA:** 2,14x (2022) → 1,94x (2023) → 2,11x (2024). Interpretación: mejora en 2023 por crecimiento de EBITDA; repunte en 2024 por crecimiento de deuda más rápido que EBITDA, manteniéndose en rango moderado.
  - **Liquidez corriente (Activo corriente/Pasivo corriente):** 2,18x → 2,57x → 3,26x. Interpretación: holgura creciente para obligaciones de corto plazo.
  - **Cobertura de intereses (EBITDA/Gastos financieros):** 6,22x → 8,61x → 8,64x. Interpretación: capacidad sólida de servicio de deuda.
- **Crecimiento (base estados aportados):** ingresos 2,1M → 3,8M → 5,6M; EBITDA 280k → 620k → 950k; deuda 0,6M → 1,2M → 2,0M (KYC Screener/Model Builder).  
- **Ajuste/nota:** la interpretación del Valuation Reviewer es consistente con los ratios; no obstante, los “saltos” 2022→2023 marcados por Model Builder aconsejan **validación documental** (p.ej., memoria/EEFF auditadas o detalle de deuda) antes de basar límites en la tendencia.

## Screening (sanciones / PEP / adverse media)
Partes screeneadas (KYC Screener Agent, fuente: local_db):
- **Adrián Nexuria Pujol:** sin hits. Nota: “fichero de sanciones no encontrado”. **Requiere re-screening** con listas actualizadas (limitación de fuente).
- **Laura Morales Sanz:** sin hits. Nota: “fichero de sanciones no encontrado”. **Requiere re-screening**.
- **Nexuria Tech Solutions SL:** sin hits. Nota: “fichero de sanciones no encontrado”. **Requiere re-screening**.
- **Vertex Ventures Spain SL:** sin hits. Nota: “fichero de sanciones no encontrado”. **Requiere re-screening**.  
**Conclusión screening:** ausencia de coincidencias en la consulta realizada, pero **no concluyente** por fallo/ausencia del fichero de sanciones (no se reporta nivel de confianza; procede revisión manual/segunda fuente).

## Señales externas
Según Market Researcher Agent: no se encontraron resultados públicos relevantes/negativos sobre Nexuria Tech Solutions SL (incl. concurso/preconcurso), ni litigios asociados a Adrián Nexuria Pujol, ni sanciones regulatorias/litigios para Vertex Ventures Spain SL en las fuentes consultadas. Se indica explícitamente que es **ausencia de información recuperada**, no prueba de ausencia de riesgo.

## Recomendaciones
- Solicitar y archivar **DNI/NIE/pasaporte** vigente de **Adrián Nexuria Pujol** y **Laura Morales Sanz** (y cualquier otro UBO/administrador aplicable), para cerrar el **FAIL KYC-001** (según KYC Screener Agent).
- Ejecutar **re-screening** de entidad y partes relacionadas (UBOs/administradores y Vertex Ventures Spain SL) en proveedor/listas de sanciones/PEP/adverse media **actualizadas**, documentando evidencia y fecha (por limitación “fichero de sanciones no encontrado”, KYC Screener Agent).
- Pedir **detalle de deuda financiera** (vencimientos, tipo, covenants, acreedores) y, si existe, **EEFF auditadas/memoria** para validar los saltos 2022→2023 en EBITDA y deuda (audit_flags del Model Builder Agent).
- En estructuración crediticia: considerar **covenants de apalancamiento** (p.ej., Debt/EBITDA) y **seguimiento trimestral** de deuda/EBITDA dada la subida de deuda en 2024 (Valuation Reviewer Agent).
- Confirmar **estructura accionarial** y % de participación de Vertex Ventures Spain SL y personas físicas (la escritura identifica titulares reales, pero conviene % y control efectivo para expediente completo; KYC Screener Agent).
- Escalar a Compliance para **sign-off** condicionado a subsanación de identidad y re-screening, dejando trazabilidad de las limitaciones actuales del screening (KYC Screener Agent).

Estas recomendaciones son propuestas; la decisión final corresponde al analista y al comité de riesgos.