# Plan de Implementación: Agente de IA para Taller de Ingeniería

## Descripción General

Este plan implementa un agente de IA conversacional usando Strands SDK y Amazon Bedrock que funciona como Asistente Técnico de Ingeniería. El agente proporciona tres herramientas especializadas: generación de números de tarjeta de prueba con algoritmo de Luhn, generación de contraseñas criptográficamente seguras, y cálculo de volemia según la fórmula de Nadler.

## Tareas

- [x] 1. Configurar estructura del proyecto y dependencias
  - Crear archivo requirements.txt con strands-sdk, boto3, pytest e hypothesis
  - Crear archivo .gitignore para proteger credenciales y logs
  - Crear estructura de directorios (tests/, archivos principales)
  - _Requisitos: 6.3, 6.4, 6.5_

- [ ] 2. Implementar herramienta de generación de tarjetas de prueba
  - [x] 2.1 Crear función generar_tarjeta_prueba en tools.py
    - Implementar algoritmo de Luhn para cálculo de dígito de control
    - Soportar generación de tarjetas Visa (prefijo 4) y Mastercard (prefijo 5)
    - Agregar decorador @tool de Strands SDK
    - Incluir docstring detallado con propósito, parámetros y ejemplos
    - Implementar validación de tipo de tarjeta
    - Agregar disclaimer de uso solo para pruebas
    - _Requisitos: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7_
  
  - [ ]* 2.2 Escribir pruebas unitarias para generar_tarjeta_prueba
    - Test de ejemplo: generar Visa y verificar prefijo 4
    - Test de ejemplo: generar Mastercard y verificar prefijo 5
    - Test de error: tipo inválido debe lanzar ValueError
    - Test de borde: verificar longitud exacta de 16 dígitos
    - _Requisitos: 3.2, 3.3, 3.4, 3.5_
  
  - [ ]* 2.3 Escribir property test para validación de Luhn
    - **Property 1: Validación de Números de Tarjeta**
    - **Valida: Requisitos 3.2, 3.5**
    - Para cualquier tipo de tarjeta generada, verificar que tiene 16 dígitos y pasa algoritmo de Luhn
    - _Requisitos: 3.2, 3.5_
  
  - [ ]* 2.4 Escribir property test para prefijos correctos
    - **Property 2: Prefijo Correcto por Tipo de Tarjeta**
    - **Valida: Requisitos 3.3, 3.4**
    - Para cualquier tipo solicitado, verificar que el prefijo es correcto (4 para Visa, 5 para Mastercard)
    - _Requisitos: 3.3, 3.4_

- [ ] 3. Implementar herramienta de generación de contraseñas seguras
  - [x] 3.1 Crear función generar_password_seguro en tools.py
    - Usar módulo secrets para alta entropía criptográfica
    - Implementar validación de longitud (mínimo 8, máximo 128)
    - Definir conjuntos de caracteres (mayúsculas, minúsculas, dígitos, símbolos)
    - Garantizar al menos un carácter de cada categoría
    - Mezclar caracteres para evitar patrones predecibles
    - Agregar decorador @tool de Strands SDK
    - Incluir docstring detallado con recomendaciones de seguridad
    - _Requisitos: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7_
  
  - [ ]* 3.2 Escribir pruebas unitarias para generar_password_seguro
    - Test de ejemplo: generar contraseña de 16 caracteres
    - Test de error: longitud menor a 8 debe lanzar ValueError
    - Test de error: longitud mayor a 128 debe lanzar ValueError
    - Test de borde: longitud exactamente 8 debe funcionar
    - Test de composición: verificar presencia de todos los tipos de caracteres
    - _Requisitos: 4.3, 4.4_
  
  - [ ]* 3.3 Escribir property test para longitud exacta
    - **Property 3: Longitud Exacta de Contraseñas**
    - **Valida: Requisitos 4.3**
    - Para cualquier longitud válida (8-128), verificar que la contraseña tiene exactamente esa longitud
    - _Requisitos: 4.3_
  
  - [ ]* 3.4 Escribir property test para composición completa
    - **Property 4: Composición Completa de Contraseñas**
    - **Valida: Requisitos 4.4**
    - Para cualquier contraseña generada, verificar que contiene al menos una mayúscula, minúscula, dígito y símbolo
    - _Requisitos: 4.4_

- [ ] 4. Implementar herramienta de cálculo de volemia
  - [x] 4.1 Crear función calcular_volemia_nadler en tools.py
    - Implementar validación de parámetros (peso: 20-300 kg, altura: 100-250 cm, género: masculino/femenino)
    - Convertir altura de centímetros a metros
    - Aplicar fórmula de Nadler para hombres: V = 0.3669 × H³ + 0.03219 × W + 0.6041
    - Aplicar fórmula de Nadler para mujeres: V = 0.3561 × H³ + 0.03308 × W + 0.1833
    - Retornar resultado en litros y mililitros con parámetros de entrada
    - Agregar decorador @tool de Strands SDK
    - Incluir docstring detallado con explicación de fórmulas y disclaimer médico
    - _Requisitos: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9_
  
  - [ ]* 4.2 Escribir pruebas unitarias para calcular_volemia_nadler
    - Test de ejemplo: calcular volemia para hombre de 70kg, 175cm
    - Test de ejemplo: calcular volemia para mujer de 60kg, 165cm
    - Test de error: peso fuera de rango debe lanzar ValueError
    - Test de error: altura fuera de rango debe lanzar ValueError
    - Test de error: género inválido debe lanzar ValueError
    - Test de borde: valores en límites de rangos (20kg, 300kg, 100cm, 250cm)
    - _Requisitos: 5.2, 5.3, 5.4, 5.5, 5.6, 5.7_
  
  - [ ]* 4.3 Escribir property test para precisión del cálculo
    - **Property 5: Precisión del Cálculo de Volemia**
    - **Valida: Requisitos 5.5, 5.6**
    - Para cualquier conjunto de parámetros válidos, verificar que el resultado coincide con la fórmula de Nadler
    - _Requisitos: 5.5, 5.6_
  
  - [ ]* 4.4 Escribir property test para validación de entrada
    - **Property 6: Validación de Entrada en Herramientas**
    - **Valida: Requisitos 5.7, 8.1**
    - Para cualquier parámetro inválido o fuera de rango, verificar que se lanza ValueError con mensaje descriptivo
    - _Requisitos: 5.7, 8.1_

- [ ] 5. Checkpoint - Verificar que todas las herramientas funcionan correctamente
  - Asegurarse de que todas las pruebas pasan, preguntar al usuario si surgen dudas.

- [ ] 6. Implementar configuración y lógica del agente
  - [ ] 6.1 Crear archivo agent.py con estructura básica
    - Configurar logging con formato apropiado y archivo de log
    - Definir constantes de configuración de Bedrock (model_id, region, temperature, max_tokens)
    - Definir system prompt como "Asistente Técnico de Ingeniería para la Corporación Universitaria Latinoamericana"
    - Importar herramientas desde tools.py
    - _Requisitos: 1.3, 6.1, 6.6, 8.5_
  
  - [ ] 6.2 Implementar función initialize_agent
    - Crear instancia de BedrockModel con configuración
    - Crear instancia de Agent con nombre, system prompt, modelo y herramientas
    - Habilitar capacidad de razonamiento (reasoning_enabled=True)
    - Implementar manejo de errores para credenciales AWS inválidas
    - Implementar manejo de errores para modelo no disponible
    - _Requisitos: 1.1, 1.2, 1.4, 1.5, 6.7, 8.2, 8.3_
  
  - [ ] 6.3 Implementar función run_interactive_loop
    - Mostrar mensaje de bienvenida al iniciar
    - Crear bucle que acepta entradas del usuario continuamente
    - Procesar cada solicitud con el agente
    - Mostrar respuestas formateadas al usuario
    - Permitir salir con comando o señal (Ctrl+C)
    - Capturar y manejar errores sin terminar el agente abruptamente
    - _Requisitos: 2.1, 2.2, 2.3, 2.4, 2.5, 8.4_
  
  - [ ] 6.4 Implementar función main como punto de entrada
    - Llamar a initialize_agent para configurar el agente
    - Llamar a run_interactive_loop para iniciar interacción
    - Manejar excepciones de nivel superior con mensajes claros
    - _Requisitos: 6.1, 8.4_

- [ ] 7. Implementar pruebas de integración del agente
  - [ ]* 7.1 Escribir pruebas unitarias de configuración del agente
    - Test: verificar que el agente se inicializa con Bedrock
    - Test: verificar que el system prompt es correcto
    - Test: verificar que las tres herramientas están registradas
    - Test de error: credenciales AWS inválidas deben informar error claro
    - Test de error: modelo no disponible debe informar error claro
    - _Requisitos: 1.1, 1.2, 1.3, 6.7, 8.2, 8.3_
  
  - [ ]* 7.2 Escribir property test para resiliencia ante errores
    - **Property 7: Resiliencia ante Errores**
    - **Valida: Requisitos 8.4**
    - Para cualquier error en herramienta, verificar que el agente captura el error, informa al usuario y continúa en ejecución
    - _Requisitos: 8.4_

- [ ] 8. Checkpoint final - Integración completa
  - Asegurarse de que todas las pruebas pasan, verificar cobertura de código, preguntar al usuario si surgen dudas.

- [ ] 9. Crear documentación del proyecto
  - [ ] 9.1 Crear archivo README.md
    - Incluir descripción del proyecto y objetivos
    - Documentar requisitos previos (Python 3.9+, credenciales AWS)
    - Incluir instrucciones de instalación (pip install -r requirements.txt)
    - Documentar configuración de credenciales AWS
    - Incluir ejemplos de uso para cada herramienta
    - Documentar comandos para ejecutar el agente y las pruebas
    - Agregar sección de consideraciones de seguridad
    - _Requisitos: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_
  
  - [ ] 9.2 Agregar comentarios y docstrings finales
    - Revisar que todas las funciones tienen docstrings completos
    - Agregar comentarios explicativos en lógica compleja
    - Verificar que los docstrings son suficientemente descriptivos para el LLM
    - _Requisitos: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_

## Notas

- Las tareas marcadas con `*` son opcionales y pueden omitirse para un MVP más rápido
- Cada tarea referencia los requisitos específicos que implementa para trazabilidad
- Los checkpoints aseguran validación incremental del progreso
- Las pruebas de propiedades validan las propiedades de corrección universales del diseño
- Las pruebas unitarias validan ejemplos específicos y casos borde
- La implementación sigue el orden lógico: herramientas → pruebas → agente → integración → documentación
