# Corporate & Deal Intelligence Pipeline

Este caso de uso cubre uno de los procesos más intensivos en tiempo dentro de cualquier banco con actividad comercial:

1. **Originación de oportunidades**: identificar empresas con potencial de financiación o asesoramiento.
2. **Preparación comercial**: construir el contexto, narrativa y materiales antes de una reunión con cliente.

La idea es que un conjunto de agentes de IA actúe como un **motor de inteligencia comercial y de mercado** que identifica oportunidades, analiza empresas y genera materiales listos para interacción con el cliente.

---

# Agentes, skills y arquitectura utilizada

Este caso de uso se basa en un enfoque **multiagente**, siguiendo la arquitectura definida por Anthropic, donde cada agente combina:

- **Skills**: instrucciones y conocimiento específico del dominio.
- **Connectors**: acceso gobernado a datos (internos y externos).
- **Subagents**: llamadas especializadas para subtareas concretas. 【1-95c741】  

---

## Agentes utilizados


| Fase | Agente |
|------|--------|
| Identificación oportunidades | Market Researcher |
| Análisis financiero | Earnings Reviewer |
| Modelización | Model Builder (opcional) |
| Preparación reunión | Meeting Preparer |
| Generación pitch | Pitch Builder |

### 1. Market Researcher
Responsable de:

- Identificar tendencias sectoriales  
- Detectar empresas relevantes  
- Sintetizar noticias y research  

**Rol en el flujo:** identificación de oportunidades

---

### 2. Earnings Reviewer
Responsable de:

- Analizar cuentas anuales y resultados  
- Detectar cambios relevantes  
- Identificar señales de riesgo o crecimiento  

**Rol en el flujo:** análisis financiero

---

### 3. Model Builder (opcional)

Responsable de:

- Construir modelos financieros base  
- Normalizar datos  
- Generar indicadores clave  

**Rol en el flujo:** estructuración financiera

---

### 4. Meeting Preparer

Responsable de:

- Preparar briefings de cliente  
- Sintetizar contexto  
- Proponer talking points  

**Rol en el flujo:** preparación de reuniones

---

### 5. Pitch Builder

Responsable de:

- Generar pitchbooks  
- Construir narrativa comercial  
- Crear comparables  

**Rol en el flujo:** generación de propuestas

---

## Skills relevantes

Las skills son paquetes estructurados de instrucciones y lógica de negocio que el agente activa dinámicamente. 【2-f266db】  

En este caso de uso incluyen, entre otras:

- **Sector analysis skills**  
  - Identificación de tendencias sectoriales  
  - Clasificación de empresas  

- **Financial analysis skills**  
  - Lectura de estados financieros  
  - Cálculo de métricas clave  

- **Comparables analysis skills**  
  - Selección de empresas comparables  
  - Generación de benchmarks  

- **Briefing generation skills**  
  - Síntesis estructurada de información  
  - Generación de resúmenes ejecutivos  

- **Pitch generation skills**  
  - Construcción de narrativa  
  - Estructuración de presentaciones  

---

## Connectors (fuentes de datos)

Los agentes se conectan a múltiples fuentes mediante acceso gobernado a datos. 【1-95c741】  

Ejemplos típicos en este flujo:

- Datos internos:
  - CRM
  - Historial de clientes
  - Operaciones previas

- Datos externos:
  - Noticias
  - Bases de datos financieras
  - Research sectorial

- Sistemas corporativos:
  - Excel (modelos)
  - PowerPoint (presentaciones)
  - Word (documentación)

---

## Subagents

Los subagentes ejecutan subtareas específicas dentro del flujo principal. 【3-f73d4c】  

Ejemplos en este caso:

- Selección de comparables  
- Validación de métricas financieras  
- Síntesis de noticias  
- Generación de narrativa  

Permiten dividir el problema en componentes más pequeños y especializados.

---

## Orquestación

El pipeline funciona como una cadena de agentes:

Market Researcher → Earnings Reviewer → Model Builder → Meeting Preparer → Pitch Builder

Cada agente:

- Consume el output del anterior  
- Añade contexto  
- Enriquce el análisis  

---

# ¿Qué problema resuelve?

En muchos bancos, la preparación de una reunión comercial o la búsqueda de oportunidades implica tareas manuales repetitivas:

* Búsqueda de empresas en sectores relevantes.
* Lectura de cuentas anuales y resultados.
* Revisión de noticias.
* Análisis de evolución financiera.
* Identificación de necesidades potenciales.
* Comparación con otras empresas del sector.
* Preparación de presentaciones comerciales.

Un banker puede dedicar entre varias horas y un día completo para preparar correctamente una interacción con un cliente.

El agente automatiza esa fase.

---

# ¿Cómo funciona?

## 1. Identificación de oportunidades

El agente analiza automáticamente:

* Sectores estratégicos.
* Empresas con crecimiento relevante.
* Cambios recientes en el mercado.
* Movimientos de financiación o expansión.
* Señales de necesidad de capital.

Genera una lista priorizada.

Por ejemplo:

--------------------------
Sector: Industrial
Empresas detectadas:

Empresa A: crecimiento sostenido sin financiación reciente
Empresa B: expansión internacional significativa
Empresa C: incremento de deuda en el último ejercicio
--------------------------

---

## 2. Análisis de resultados financieros

El agente revisa automáticamente:

* Cuentas anuales.
* Resultados trimestrales.
* Presentaciones corporativas.

Identifica tendencias clave.

Por ejemplo:

Empresa B:
Incremento de ingresos del 18% interanual.
Reducción del margen operativo.
Aumento del CAPEX asociado a expansión.

---

## 3. Construcción de visión financiera

A partir de los datos extraídos:

* Normaliza información financiera.
* Calcula indicadores clave.
* Identifica tendencias estructurales.
* Genera una visión básica del negocio.

Ejemplo de interpretación:

> La compañía presenta un crecimiento sólido, pero con presión en márgenes derivada de su expansión, lo que puede implicar necesidades de financiación adicionales.

---

## 4. Preparación de briefing

Antes de cualquier interacción, el agente genera un resumen estructurado:

* Perfil de la empresa.
* Situación actual.
* Posibles necesidades.
* Riesgos relevantes.
* Temas de conversación.

Por ejemplo:

----------------------
Cliente: Empresa B
Situación:

Fase de crecimiento activo
Expansión internacional en curso

Posibles necesidades:

Financiación de CAPEX
Optimización de estructura de deuda

Riesgos:

Compresión de márgenes
Incremento de exposición internacional

---

## 5. Generación de propuesta comercial

El agente crea automáticamente:

* Presentación en PowerPoint.
* Narrativa comercial.
* Comparables sectoriales.
* Argumentos de valor.

Ejemplo:

---

### Oportunidad detectada

Empresa en fase de expansión con necesidad potencial de financiación estructurada.

Posible encaje con productos de financiación corporativa.

---

## 6. Validación y ajuste humano

El equipo comercial:

* Revisa el análisis.
* Ajusta el mensaje.
* Personaliza la aproximación.
* Define estrategia de entrada.

El agente no sustituye al banker, sino que acelera su preparación.

---

# Resultado

Se genera un paquete completo listo para acción:

* Lista priorizada de oportunidades.
* Análisis financiero básico por empresa.
* Briefing estructurado.
* Presentación comercial generada.
* Puntos clave para la reunión.

---

# ¿Qué aporta al banco?

## 1. Reduce tiempos de preparación

Una tarea que puede requerir varias horas pasa a resolverse en menos de una hora, permitiendo mayor foco en la interacción con el cliente.

---

## 2. Incrementa la proactividad comercial

El banco deja de depender únicamente de solicitudes entrantes y puede identificar oportunidades de forma sistemática.

---

## 3. Mejora la calidad de las reuniones

Cada interacción se apoya en:

* Contexto completo.
* Datos actualizados.
* Narrativa estructurada.

---

## 4. Estandariza el enfoque comercial

Todos los equipos trabajan con:

* Misma estructura de análisis.
* Mismos indicadores.
* Misma calidad de preparación.

---

## 5. Aumenta la productividad

Los equipos comerciales reducen trabajo manual y pueden centrarse en:

* Relación con el cliente.
* Negociación.
* Generación de negocio.

---

# Valor diferencial

El valor de este caso de uso no está en automatizar la venta, sino en **preparar mejor cada interacción comercial**.

El agente construye un contexto completo sobre cada empresa, identifica oportunidades potenciales y genera materiales estructurados, permitiendo que el equipo humano llegue a cada reunión con mayor conocimiento, mejor narrativa y mayor capacidad de generar valor desde el primer contacto.