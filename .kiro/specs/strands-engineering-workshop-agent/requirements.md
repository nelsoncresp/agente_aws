# Documento de Requisitos

## Introducción

Este documento especifica los requisitos para un Agente de IA diseñado para un taller de ingeniería en la Corporación Universitaria Latinoamericana. El agente funcionará como un Asistente Técnico de Ingeniería capaz de generar datos de prueba, crear contraseñas seguras y realizar cálculos médicos utilizando Amazon Bedrock y el framework Strands Agents.

## Glosario

- **Agente**: El sistema de IA que procesa solicitudes del usuario y ejecuta herramientas
- **Strands_SDK**: Framework para construir agentes de IA con capacidades de razonamiento
- **Bedrock**: Servicio de Amazon Web Services que proporciona acceso a modelos de lenguaje
- **Herramienta**: Función Python decorada que el Agente puede invocar
- **System_Prompt**: Instrucciones iniciales que definen el comportamiento del Agente
- **Algoritmo_de_Luhn**: Algoritmo de validación de dígitos de control para números de tarjeta
- **Entropía**: Medida de aleatoriedad en la generación de contraseñas
- **Fórmula_de_Nadler**: Ecuación médica para calcular el volumen sanguíneo total

## Requisitos

### Requisito 1: Configuración del Agente

**User Story:** Como desarrollador del taller, quiero configurar un agente de IA con Amazon Bedrock, para que pueda procesar solicitudes de los usuarios utilizando modelos de lenguaje avanzados.

#### Criterios de Aceptación

1. THE Agente SHALL utilizar Amazon Bedrock como proveedor de modelos de lenguaje
2. THE Agente SHALL soportar los modelos Claude 3 Haiku o Amazon Titan
3. THE Agente SHALL configurarse con un System_Prompt que lo identifique como "Asistente Técnico de Ingeniería para la Corporación Universitaria Latinoamericana"
4. THE Agente SHALL tener capacidad de razonamiento antes de ejecutar acciones
5. THE Agente SHALL cargar las credenciales de AWS desde el entorno o configuración local

### Requisito 2: Interfaz de Interacción

**User Story:** Como usuario del taller, quiero interactuar con el agente desde la terminal, para que pueda hacer preguntas y recibir respuestas en tiempo real.

#### Criterios de Aceptación

1. THE Agente SHALL proporcionar una interfaz de línea de comandos interactiva
2. WHEN el usuario inicia el Agente, THE Agente SHALL mostrar un mensaje de bienvenida
3. WHILE el Agente está en ejecución, THE Agente SHALL aceptar entradas del usuario continuamente
4. WHEN el usuario envía una solicitud, THE Agente SHALL procesar la solicitud y mostrar la respuesta
5. THE Agente SHALL permitir al usuario salir de la sesión mediante un comando o señal

### Requisito 3: Generación de Números de Tarjeta de Prueba

**User Story:** Como desarrollador, quiero generar números de tarjeta ficticios válidos, para que pueda probar sistemas de pago sin usar datos reales.

#### Criterios de Aceptación

1. THE Herramienta SHALL llamarse "generar_tarjeta_prueba"
2. THE Herramienta SHALL implementar el Algoritmo_de_Luhn para calcular el dígito de control
3. THE Herramienta SHALL soportar la generación de números Visa (comenzando con 4)
4. THE Herramienta SHALL soportar la generación de números Mastercard (comenzando con 5)
5. WHEN se solicita generar una tarjeta, THE Herramienta SHALL retornar un número de 16 dígitos válido según Luhn
6. THE Herramienta SHALL incluir un docstring detallado explicando su propósito y parámetros
7. THE Herramienta SHALL usar el decorador @tool del Strands_SDK

### Requisito 4: Generación de Contraseñas Seguras

**User Story:** Como usuario del taller, quiero generar contraseñas seguras, para que pueda crear credenciales robustas para mis sistemas.

#### Criterios de Aceptación

1. THE Herramienta SHALL llamarse "generar_password_seguro"
2. THE Herramienta SHALL utilizar el módulo secrets de Python para alta Entropía
3. THE Herramienta SHALL generar contraseñas con longitud configurable
4. THE Herramienta SHALL incluir caracteres alfanuméricos y símbolos especiales
5. WHEN se solicita una contraseña, THE Herramienta SHALL retornar una cadena criptográficamente segura
6. THE Herramienta SHALL incluir un docstring detallado explicando su propósito y parámetros
7. THE Herramienta SHALL usar el decorador @tool del Strands_SDK

### Requisito 5: Cálculo de Volemia según Nadler

**User Story:** Como profesional médico o estudiante, quiero calcular el volumen sanguíneo total de un paciente, para que pueda estimar parámetros clínicos importantes.

#### Criterios de Aceptación

1. THE Herramienta SHALL llamarse "calcular_volemia_nadler"
2. THE Herramienta SHALL solicitar peso en kilogramos como parámetro
3. THE Herramienta SHALL solicitar altura en centímetros como parámetro
4. THE Herramienta SHALL solicitar género (masculino/femenino) como parámetro
5. THE Herramienta SHALL aplicar la Fórmula_de_Nadler específica para cada género
6. WHEN se proporcionan los parámetros válidos, THE Herramienta SHALL retornar el volumen sanguíneo en litros
7. IF los parámetros son inválidos o fuera de rango, THEN THE Herramienta SHALL retornar un mensaje de error descriptivo
8. THE Herramienta SHALL incluir un docstring detallado explicando la fórmula, propósito y parámetros
9. THE Herramienta SHALL usar el decorador @tool del Strands_SDK

### Requisito 6: Estructura Modular del Proyecto

**User Story:** Como desarrollador, quiero que el proyecto tenga una estructura modular clara, para que sea fácil de mantener y extender.

#### Criterios de Aceptación

1. THE proyecto SHALL contener un archivo agent.py con la lógica principal del Agente
2. THE proyecto SHALL contener un archivo tools.py con todas las definiciones de Herramientas
3. THE proyecto SHALL contener un archivo requirements.txt con las dependencias necesarias
4. THE requirements.txt SHALL incluir strands-sdk como dependencia
5. THE requirements.txt SHALL incluir boto3 como dependencia para AWS
6. THE agent.py SHALL importar las Herramientas desde tools.py
7. THE agent.py SHALL inicializar el Agente con las Herramientas importadas

### Requisito 7: Documentación de Herramientas

**User Story:** Como modelo de lenguaje, quiero entender cuándo y cómo usar cada herramienta, para que pueda seleccionar la herramienta correcta según la solicitud del usuario.

#### Criterios de Aceptación

1. THE Herramienta SHALL incluir un docstring en formato estándar de Python
2. THE docstring SHALL describir el propósito de la Herramienta
3. THE docstring SHALL especificar cada parámetro con su tipo y descripción
4. THE docstring SHALL especificar el tipo de retorno y su significado
5. THE docstring SHALL incluir ejemplos de uso cuando sea apropiado
6. THE docstring SHALL ser suficientemente descriptivo para que el modelo de Bedrock comprenda su uso

### Requisito 8: Manejo de Errores

**User Story:** Como usuario, quiero recibir mensajes de error claros cuando algo falla, para que pueda entender qué salió mal y cómo corregirlo.

#### Criterios de Aceptación

1. WHEN una Herramienta recibe parámetros inválidos, THEN THE Herramienta SHALL retornar un mensaje de error descriptivo
2. IF la conexión con Bedrock falla, THEN THE Agente SHALL informar al usuario del problema de conectividad
3. IF las credenciales de AWS son inválidas, THEN THE Agente SHALL informar al usuario sobre el problema de autenticación
4. WHEN ocurre un error durante la ejecución, THE Agente SHALL continuar en ejecución sin terminar abruptamente
5. THE Agente SHALL registrar errores de manera que faciliten la depuración

---

## Notas Adicionales

Este documento define los requisitos funcionales para el Agente de IA del taller de ingeniería. Los requisitos están diseñados para ser verificables y seguir los patrones EARS. La implementación técnica específica se definirá en el documento de diseño posterior.
