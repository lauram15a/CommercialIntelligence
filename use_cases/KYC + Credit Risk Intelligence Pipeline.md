# KYC + Credit Risk Intelligence Pipeline

Este caso de uso combina dos procesos que existen en prácticamente cualquier banco:

1. **KYC (Know Your Customer)**: verificar quién es el cliente y si cumple los requisitos regulatorios.  
2. **Análisis de riesgo de crédito**: determinar si es razonable conceder una financiación y en qué condiciones.  

La idea es que un conjunto de agentes de IA actúe como un **motor de inteligencia documental** que recopila, organiza y analiza toda la información disponible antes de que intervenga el analista humano.

---

# Por qué es el caso más prioritario

Este es probablemente el caso de uso con mayor impacto estructural:

* es obligatorio (regulación)
* es lento (cuellos de botella en onboarding)
* es caro (trabajo manual cualificado)
* es escalable horizontalmente (retail, pymes, corporate)

---

# Agentes, skills y arquitectura utilizada

Este caso de uso se basa en un enfoque **multiagente**, donde cada agente combina:

- **Skills**: lógica de negocio y reglas del proceso  
- **Connectors**: acceso a fuentes de datos (documentos, listas, históricos)  
- **Subagents**: ejecución de subtareas especializadas  

---

## Agentes utilizados

---


| Fase | Agente |
|------|--------|
| Validación KYC | KYC Screener |
| Señales externas | Market Researcher |
| Análisis financiero | Model Builder |
| Validación financiera | Valuation Reviewer |
| Generación informe | Credit Risk Report |

---

### 1. KYC Screener Agent
Valida identidad, documentación y cumplimiento regulatorio

---

### 2. Market Researcher Agent
Analiza contexto externo y señales reputacionales

---

### 3. Model Builder Agent (opcional)
Estructura información financiera

---

### 4. Valuation Reviewer Agent (opcional)
Evalúa coherencia financiera y métricas

---

### 5. Credit Risk Report Agent
Construye el informe final de riesgo y recomendaciones

---

## Skills utilizadas

### KYC Screener Agent

Objetivo: construir y validar el expediente KYC

Skills:

* `kyc_docs.get_documents`
* `kyc_docs.check_registry`
* `risk_data.get_risk_profile`
* `embeddings.embed`

---

### Market Researcher Agent

Objetivo: identificar señales externas de riesgo

Skills:

* `news.get_recent_news`
* `filings.get_filings`
* `risk_data.get_risk_profile`
* `embeddings.embed`

---

### Model Builder Agent

Objetivo: estructurar información financiera

Skills:

* `filings.get_filings`
* `financial_metrics.extract`
* `embeddings.embed`

---

### Valuation Reviewer Agent

Objetivo: validar coherencia financiera

Skills:

* `financial_metrics.extract`
* `filings.get_filings`
* `embeddings.embed`

---

### Credit Risk Report Agent

Objetivo: generar el informe final para comité

Skills:

* `report.generate_credit_report`
* `risk_metrics.aggregate`
* `explanations.generate`
* `embeddings.embed`

---

## Connectors (fuentes de datos)

El pipeline se conecta a:

- Documentación interna:
  - PDFs
  - Word
  - Excel
  - Emails
  - Formularios

- Sistemas internos:
  - CRM
  - historial del cliente
  - información transaccional

- Fuentes externas:
  - listas de sanciones
  - PEP
  - noticias
  - registros públicos

---

## Subagents

Ejemplos de subtareas:

- extracción de entidades de documentos  
- validación de identidad  
- cálculo de métricas financieras  
- detección de inconsistencias  
- generación de explicaciones  

Permiten ejecutar cada fase con mayor precisión.

# ¿Qué problema resuelve?

En muchos bancos, el proceso de estudio de una operación de crédito implica revisar decenas o cientos de documentos:

* DNI o documentación de identidad.
* Escrituras de constitución.
* Declaraciones fiscales.
* Estados financieros.
* Nóminas.
* Extractos bancarios.
* Informes de riesgos.
* Información del CRM.
* Historial del cliente.
* Documentación aportada durante el proceso.
* Noticias públicas sobre la empresa.
* Información de listas de sanciones o PEP.
* Informes de auditoría.

Un analista puede dedicar varias horas simplemente a **leer y recopilar información** antes de empezar a valorar el riesgo.

El agente automatiza esa fase.

---

# ¿Cómo funciona?

## 1. Ingesta documental

El sistema recopila automáticamente:

* PDFs
* Word
* Excel
* Emails
* Formularios
* Información del CRM
* Datos internos
* Información pública autorizada

Todo queda indexado.

---

## 2. Validación KYC

El agente comprueba:

* Identidad
* Caducidad de documentos
* Documentación incompleta
* Coincidencias entre fuentes
* Titularidad real
* PEP
* Sanciones
* Señales AML

Ejemplo:
--------------------
Cliente identificado correctamente.
Justificante de domicilio con antigüedad superior a 18 meses.
Sin coincidencias en listas de sanciones.
Posible relación indirecta con perfil PEP. Revisión recomendada.

--------------------

## 3. Extracción financiera

Se analiza automáticamente:

* Balance
* P&L
* Flujo de caja
* EBITDA
* Deuda
* Liquidez
* Patrimonio

---

## 4. Análisis de riesgo

Se calculan:

* Debt/EBITDA
* Liquidez
* Margen
* Evolución ingresos
* Cobertura intereses
* Endeudamiento

Ejemplo:

> Incremento de deuda del 35% frente a crecimiento de EBITDA del 8%.

---

## 5. Cruce histórico

El agente consulta:

* operaciones anteriores  
* incidencias  
* impagos  
* retrasos  
* productos  

---

## 6. Señales externas

Se incorporan:

* noticias  
* cambios societarios  
* litigios  
* eventos relevantes  

---

## 7. Generación del informe

Se genera un informe completo.

### Resumen ejecutivo

Empresa con crecimiento estable.  
Incremento de apalancamiento reciente.  
Sin incidencias KYC relevantes.  
Sin sanciones.  
Concentración en clientes.  
Liquidez adecuada.  

---

## 8. Recomendaciones

El sistema sugiere:

* solicitar documentación adicional  
* pedir garantías  
* ajustar importe  
* modificar plazo  
* escalar a comité  

---

# ¿Qué aporta al banco?

## 1. Reduce tiempos

De horas a minutos.

---

## 2. Mejora consistencia

Análisis homogéneo.

---

## 3. Reduce errores

Menos omisiones críticas.

---

## 4. Facilita auditorías

Trazabilidad completa.

---

## 5. Mejora productividad

Más foco en decisión, menos en recopilación.

---

# Valor diferencial

El valor no está en automatizar decisiones, sino en **construir un expediente inteligente completo y trazable** que permite al analista tomar mejores decisiones en menos tiempo.

Este tipo de pipeline suele ser el primero en escalar dentro de un banco, porque impacta directamente en riesgo, cumplimiento y eficiencia operativa.