# Documento de Diseño Técnico

## Introducción

Este documento especifica el diseño técnico del Agente de IA para el taller de ingeniería de la Corporación Universitaria Latinoamericana. El agente utilizará Amazon Bedrock como proveedor de modelos de lenguaje y el framework Strands SDK para implementar capacidades de razonamiento y ejecución de herramientas.

El sistema está diseñado para proporcionar tres herramientas especializadas: generación de números de tarjeta de prueba, generación de contraseñas seguras y cálculo de volemia según la fórmula de Nadler.

## Visión General

### Objetivo

Crear un agente de IA conversacional que funcione como Asistente Técnico de Ingeniería, capaz de:
- Procesar solicitudes en lenguaje natural
- Razonar sobre qué herramienta utilizar
- Ejecutar herramientas especializadas
- Proporcionar respuestas contextuales y precisas

### Alcance

El sistema incluye:
- Configuración de agente con Amazon Bedrock (Claude 3 Haiku o Amazon Titan)
- Interfaz de línea de comandos interactiva
- Tres herramientas especializadas con validación de entrada
- Manejo robusto de errores
- Documentación completa para el LLM

### Restricciones

- Debe usar el framework Strands SDK
- Debe integrarse con Amazon Bedrock
- Las credenciales AWS deben cargarse desde el entorno
- Todas las herramientas deben usar el decorador @tool
- Los docstrings deben ser suficientemente descriptivos para que el LLM comprenda el uso

## Arquitectura

### Arquitectura de Alto Nivel

El sistema sigue una arquitectura de tres capas:

```
┌─────────────────────────────────────────────────────────┐
│                    Usuario (Terminal)                    │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  Capa de Interacción                     │
│                     (agent.py)                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │  - Bucle de entrada/salida                       │   │
│  │  - Procesamiento de comandos                     │   │
│  │  - Formateo de respuestas                        │   │
│  └─────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  Capa de Razonamiento                    │
│                   (Strands Agent)                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │  - Interpretación de intención                   │   │
│  │  - Selección de herramienta                      │   │
│  │  - Orquestación de ejecución                     │   │
│  │  - Generación de respuesta                       │   │
│  └─────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  Capa de Herramientas                    │
│                     (tools.py)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Generador   │  │  Generador   │  │  Calculadora │ │
│  │  Tarjetas    │  │  Passwords   │  │   Volemia    │ │
│  │   Prueba     │  │   Seguros    │  │   Nadler     │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              Servicios Externos                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │         Amazon Bedrock (Claude/Titan)            │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Flujo de Datos

1. **Entrada del Usuario**: El usuario ingresa una solicitud en lenguaje natural
2. **Procesamiento Inicial**: agent.py captura la entrada y la envía al agente Strands
3. **Razonamiento**: El agente consulta a Bedrock para interpretar la intención
4. **Selección de Herramienta**: Basándose en los docstrings, el LLM decide qué herramienta invocar
5. **Ejecución**: La herramienta seleccionada se ejecuta con los parámetros extraídos
6. **Respuesta**: El resultado se formatea y se presenta al usuario

### Decisiones de Arquitectura

**DA-1: Uso de Strands SDK**
- Razón: Framework especializado para agentes con capacidades de razonamiento
- Alternativas consideradas: LangChain, implementación custom
- Ventajas: Integración nativa con Bedrock, manejo de herramientas simplificado

**DA-2: Separación de Herramientas en Módulo Independiente**
- Razón: Facilita mantenimiento, testing y extensibilidad
- Permite agregar nuevas herramientas sin modificar la lógica del agente

**DA-3: Interfaz de Terminal**
- Razón: Simplicidad para entorno de taller educativo
- Permite ejecución local sin infraestructura web

## Componentes e Interfaces

### Componente 1: Agent Manager (agent.py)

**Responsabilidad**: Orquestar la interacción entre el usuario y el agente de IA

**Interfaces**:
```python
def main() -> None:
    """Punto de entrada principal del agente"""
    
def initialize_agent() -> Agent:
    """Inicializa el agente con configuración de Bedrock y herramientas"""
    
def run_interactive_loop(agent: Agent) -> None:
    """Ejecuta el bucle interactivo de entrada/salida"""
```

**Dependencias**:
- strands_sdk: Para crear y configurar el agente
- boto3: Para credenciales AWS
- tools: Para importar las herramientas disponibles

**Configuración**:
```python
BEDROCK_CONFIG = {
    "model_id": "anthropic.claude-3-haiku-20240307-v1:0",  # o "amazon.titan-text-express-v1"
    "region": "us-east-1",
    "temperature": 0.7,
    "max_tokens": 2048
}

SYSTEM_PROMPT = """Eres un Asistente Técnico de Ingeniería para la Corporación 
Universitaria Latinoamericana. Tu objetivo es ayudar a estudiantes y profesionales 
con tareas técnicas específicas utilizando las herramientas disponibles."""
```

### Componente 2: Tool Collection (tools.py)

**Responsabilidad**: Proporcionar herramientas especializadas que el agente puede invocar

#### Herramienta 1: generar_tarjeta_prueba

**Firma**:
```python
@tool
def generar_tarjeta_prueba(tipo: str = "visa") -> str:
    """
    Genera un número de tarjeta de crédito ficticio válido para pruebas.
    
    Esta herramienta crea números de tarjeta que pasan la validación del 
    algoritmo de Luhn, útiles para probar sistemas de pago sin usar datos reales.
    
    Args:
        tipo: Tipo de tarjeta a generar. Opciones: "visa" o "mastercard"
        
    Returns:
        str: Número de tarjeta de 16 dígitos válido según algoritmo de Luhn
        
    Raises:
        ValueError: Si el tipo de tarjeta no es soportado
    """
```

**Algoritmo de Luhn**:
1. Generar 15 dígitos base según el tipo:
   - Visa: Comienza con "4"
   - Mastercard: Comienza con "5"
2. Aplicar algoritmo de Luhn para calcular dígito de control:
   - Duplicar cada segundo dígito de derecha a izquierda
   - Si el resultado es > 9, restar 9
   - Sumar todos los dígitos
   - El dígito de control es (10 - (suma % 10)) % 10

**Validaciones**:
- Verificar que el tipo sea "visa" o "mastercard"
- Asegurar que el número generado tenga exactamente 16 dígitos

#### Herramienta 2: generar_password_seguro

**Firma**:
```python
@tool
def generar_password_seguro(longitud: int = 16) -> str:
    """
    Genera una contraseña criptográficamente segura.
    
    Utiliza el módulo secrets de Python para garantizar alta entropía.
    La contraseña incluye letras mayúsculas, minúsculas, dígitos y símbolos.
    
    Args:
        longitud: Longitud de la contraseña (mínimo 8, recomendado 16+)
        
    Returns:
        str: Contraseña segura generada
        
    Raises:
        ValueError: Si la longitud es menor a 8 caracteres
    """
```

**Algoritmo**:
1. Validar que longitud >= 8
2. Definir conjunto de caracteres:
   - Letras: a-z, A-Z
   - Dígitos: 0-9
   - Símbolos: !@#$%^&*()_+-=[]{}|;:,.<>?
3. Usar secrets.choice() para seleccionar caracteres aleatorios
4. Asegurar al menos un carácter de cada categoría

**Validaciones**:
- Longitud mínima de 8 caracteres
- Verificar presencia de al menos: 1 mayúscula, 1 minúscula, 1 dígito, 1 símbolo

#### Herramienta 3: calcular_volemia_nadler

**Firma**:
```python
@tool
def calcular_volemia_nadler(peso: float, altura: float, genero: str) -> dict:
    """
    Calcula el volumen sanguíneo total usando la fórmula de Nadler.
    
    La fórmula de Nadler es un método estándar para estimar el volumen 
    sanguíneo basándose en características antropométricas del paciente.
    
    Fórmulas:
    - Hombres: 0.3669 × altura³ + 0.03219 × peso + 0.6041
    - Mujeres: 0.3561 × altura³ + 0.03308 × peso + 0.1833
    
    Args:
        peso: Peso del paciente en kilogramos (rango válido: 20-300 kg)
        altura: Altura del paciente en centímetros (rango válido: 100-250 cm)
        genero: Género del paciente ("masculino" o "femenino")
        
    Returns:
        dict: {
            "volumen_litros": float,
            "volumen_ml": float,
            "parametros": dict con los valores de entrada
        }
        
    Raises:
        ValueError: Si los parámetros están fuera de rango o género inválido
    """
```

**Algoritmo**:
1. Validar parámetros de entrada
2. Convertir altura de cm a metros (altura_m = altura / 100)
3. Aplicar fórmula según género:
   - Masculino: V = 0.3669 × altura_m³ + 0.03219 × peso + 0.6041
   - Femenino: V = 0.3561 × altura_m³ + 0.03308 × peso + 0.1833
4. Retornar resultado en litros y mililitros

**Validaciones**:
- Peso: 20 kg ≤ peso ≤ 300 kg
- Altura: 100 cm ≤ altura ≤ 250 cm
- Género: "masculino" o "femenino" (case-insensitive)

### Componente 3: Strands Agent

**Responsabilidad**: Proporcionar capacidades de razonamiento y orquestación

**Configuración**:
```python
agent = Agent(
    name="AsistenteTecnicoIngenieria",
    system_prompt=SYSTEM_PROMPT,
    model=BedrockModel(
        model_id=BEDROCK_CONFIG["model_id"],
        region=BEDROCK_CONFIG["region"]
    ),
    tools=[
        generar_tarjeta_prueba,
        generar_password_seguro,
        calcular_volemia_nadler
    ],
    reasoning_enabled=True
)
```

**Capacidades**:
- Interpretación de lenguaje natural
- Selección automática de herramientas basada en docstrings
- Extracción de parámetros desde la solicitud del usuario
- Manejo de conversaciones multi-turno
- Generación de respuestas contextuales

## Modelos de Datos

### Estructura de Configuración

```python
@dataclass
class BedrockConfig:
    """Configuración para Amazon Bedrock"""
    model_id: str
    region: str
    temperature: float = 0.7
    max_tokens: int = 2048
```

### Estructura de Respuesta de Herramientas

```python
# Respuesta de generar_tarjeta_prueba
CardResponse = str  # "4532015112830366"

# Respuesta de generar_password_seguro
PasswordResponse = str  # "aB3$xY9@mN2#pQ5!"

# Respuesta de calcular_volemia_nadler
@dataclass
class VolemiaResponse:
    volumen_litros: float
    volumen_ml: float
    parametros: dict[str, Any]
```

### Estructura de Errores

```python
@dataclass
class ToolError:
    """Error estandarizado de herramienta"""
    tool_name: str
    error_type: str  # "validation", "execution", "configuration"
    message: str
    details: dict[str, Any] = None
```


## Correctness Properties

*Una propiedad es una característica o comportamiento que debe mantenerse verdadero en todas las ejecuciones válidas de un sistema - esencialmente, una declaración formal sobre lo que el sistema debe hacer. Las propiedades sirven como puente entre las especificaciones legibles por humanos y las garantías de corrección verificables por máquinas.*

### Property 1: Validación de Números de Tarjeta

*Para cualquier* número de tarjeta generado por la herramienta generar_tarjeta_prueba, el número debe tener exactamente 16 dígitos y pasar la validación del algoritmo de Luhn.

**Validates: Requirements 3.2, 3.5**

### Property 2: Prefijo Correcto por Tipo de Tarjeta

*Para cualquier* tipo de tarjeta solicitado (Visa o Mastercard), el número generado debe comenzar con el prefijo correcto: 4 para Visa, 5 para Mastercard.

**Validates: Requirements 3.3, 3.4**

### Property 3: Longitud Exacta de Contraseñas

*Para cualquier* longitud solicitada mayor o igual a 8 caracteres, la contraseña generada por generar_password_seguro debe tener exactamente esa longitud.

**Validates: Requirements 4.3**

### Property 4: Composición Completa de Contraseñas

*Para cualquier* contraseña generada por generar_password_seguro, debe contener al menos un carácter de cada categoría: letra mayúscula, letra minúscula, dígito y símbolo especial.

**Validates: Requirements 4.4**

### Property 5: Precisión del Cálculo de Volemia

*Para cualquier* conjunto de parámetros válidos (peso, altura, género) proporcionados a calcular_volemia_nadler, el resultado debe coincidir con la aplicación correcta de la fórmula de Nadler para el género especificado y retornar el volumen en litros con el formato correcto.

**Validates: Requirements 5.5, 5.6**

### Property 6: Validación de Entrada en Herramientas

*Para cualquier* herramienta y cualquier conjunto de parámetros inválidos o fuera de rango, la herramienta debe lanzar un ValueError con un mensaje descriptivo que explique el problema.

**Validates: Requirements 5.7, 8.1**

### Property 7: Resiliencia ante Errores

*Para cualquier* error que ocurra durante la ejecución de una herramienta, el agente debe capturar el error, informar al usuario de manera clara y continuar en ejecución sin terminar abruptamente.

**Validates: Requirements 8.4**


## Manejo de Errores

### Estrategia General

El sistema implementa un enfoque de manejo de errores en múltiples capas:

1. **Validación de Entrada**: Cada herramienta valida sus parámetros antes de ejecutar lógica
2. **Excepciones Tipadas**: Uso de ValueError para errores de validación, RuntimeError para errores de ejecución
3. **Mensajes Descriptivos**: Todos los errores incluyen contexto sobre qué falló y cómo corregirlo
4. **Recuperación Graceful**: El agente captura excepciones y continúa funcionando
5. **Logging**: Registro de errores para facilitar depuración

### Errores por Componente

#### Herramienta: generar_tarjeta_prueba

**Errores de Validación**:
- Tipo de tarjeta no soportado
  - Condición: `tipo not in ["visa", "mastercard"]`
  - Mensaje: "Tipo de tarjeta '{tipo}' no soportado. Use 'visa' o 'mastercard'."
  - Acción: Lanzar ValueError

**Errores de Ejecución**:
- Fallo en generación de número aleatorio
  - Condición: Error en random.randint()
  - Mensaje: "Error al generar número aleatorio para tarjeta"
  - Acción: Lanzar RuntimeError con detalles

#### Herramienta: generar_password_seguro

**Errores de Validación**:
- Longitud insuficiente
  - Condición: `longitud < 8`
  - Mensaje: "La longitud debe ser al menos 8 caracteres. Recibido: {longitud}"
  - Acción: Lanzar ValueError

- Longitud excesiva
  - Condición: `longitud > 128`
  - Mensaje: "La longitud máxima es 128 caracteres. Recibido: {longitud}"
  - Acción: Lanzar ValueError

**Errores de Ejecución**:
- Fallo en generación criptográfica
  - Condición: Error en secrets.choice()
  - Mensaje: "Error al generar contraseña segura"
  - Acción: Lanzar RuntimeError con detalles

#### Herramienta: calcular_volemia_nadler

**Errores de Validación**:
- Peso fuera de rango
  - Condición: `peso < 20 or peso > 300`
  - Mensaje: "Peso debe estar entre 20 y 300 kg. Recibido: {peso} kg"
  - Acción: Lanzar ValueError

- Altura fuera de rango
  - Condición: `altura < 100 or altura > 250`
  - Mensaje: "Altura debe estar entre 100 y 250 cm. Recibido: {altura} cm"
  - Acción: Lanzar ValueError

- Género inválido
  - Condición: `genero.lower() not in ["masculino", "femenino"]`
  - Mensaje: "Género debe ser 'masculino' o 'femenino'. Recibido: '{genero}'"
  - Acción: Lanzar ValueError

**Errores de Ejecución**:
- Error en cálculo matemático
  - Condición: Error en operaciones aritméticas
  - Mensaje: "Error al calcular volemia con los parámetros proporcionados"
  - Acción: Lanzar RuntimeError con detalles

#### Agente: Errores de Configuración

**Credenciales AWS**:
- Credenciales no encontradas
  - Condición: boto3 no puede cargar credenciales
  - Mensaje: "No se encontraron credenciales de AWS. Configure AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY"
  - Acción: Lanzar RuntimeError y terminar inicialización

- Credenciales inválidas
  - Condición: Bedrock rechaza credenciales
  - Mensaje: "Credenciales de AWS inválidas. Verifique sus credenciales"
  - Acción: Lanzar RuntimeError y terminar inicialización

**Conectividad Bedrock**:
- Timeout de conexión
  - Condición: Timeout al conectar con Bedrock
  - Mensaje: "Timeout al conectar con Amazon Bedrock. Verifique su conexión a internet"
  - Acción: Informar al usuario, permitir reintentos

- Modelo no disponible
  - Condición: Modelo especificado no existe o no está disponible
  - Mensaje: "Modelo '{model_id}' no disponible. Verifique el ID del modelo"
  - Acción: Lanzar RuntimeError y terminar inicialización

### Logging

**Configuración**:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)
```

**Niveles de Log**:
- INFO: Inicio de agente, ejecución de herramientas, respuestas exitosas
- WARNING: Parámetros en límite de rangos válidos, reintentos
- ERROR: Errores de validación, errores de ejecución de herramientas
- CRITICAL: Errores de configuración, fallos de conexión con Bedrock


## Estrategia de Testing

### Enfoque Dual de Testing

Este proyecto implementa un enfoque dual que combina pruebas unitarias tradicionales con pruebas basadas en propiedades (Property-Based Testing). Ambos tipos de pruebas son complementarios y necesarios para una cobertura completa:

- **Pruebas Unitarias**: Verifican ejemplos específicos, casos borde y condiciones de error
- **Pruebas de Propiedades**: Verifican propiedades universales a través de múltiples entradas generadas aleatoriamente

### Framework de Property-Based Testing

**Biblioteca Seleccionada**: Hypothesis (Python)

Hypothesis es la biblioteca estándar para property-based testing en Python, proporcionando:
- Generación inteligente de datos de prueba
- Shrinking automático de casos de fallo
- Integración con pytest
- Estrategias personalizables para tipos complejos

**Instalación**:
```
pip install hypothesis pytest
```

### Configuración de Pruebas de Propiedades

**Configuración Mínima**:
- Cada prueba de propiedad debe ejecutar mínimo 100 iteraciones
- Configuración en pytest.ini o conftest.py:

```python
from hypothesis import settings, Verbosity

settings.register_profile("default", max_examples=100)
settings.load_profile("default")
```

**Formato de Tags**:
Cada prueba de propiedad debe incluir un comentario que referencie la propiedad del documento de diseño:

```python
# Feature: strands-engineering-workshop-agent, Property 1: Validación de Números de Tarjeta
@given(tipo=st.sampled_from(["visa", "mastercard"]))
def test_tarjeta_valida_luhn(tipo):
    ...
```

### Plan de Pruebas por Componente

#### Pruebas para generar_tarjeta_prueba

**Pruebas Unitarias**:
1. Test de ejemplo: Generar tarjeta Visa y verificar que comienza con 4
2. Test de ejemplo: Generar tarjeta Mastercard y verificar que comienza con 5
3. Test de error: Tipo de tarjeta inválido debe lanzar ValueError
4. Test de configuración: Verificar que la función tiene decorador @tool

**Pruebas de Propiedades**:
1. **Property 1**: Para cualquier tarjeta generada, debe tener 16 dígitos y pasar Luhn
   ```python
   # Feature: strands-engineering-workshop-agent, Property 1: Validación de Números de Tarjeta
   @given(tipo=st.sampled_from(["visa", "mastercard"]))
   def test_property_tarjeta_valida(tipo):
       numero = generar_tarjeta_prueba(tipo)
       assert len(numero) == 16
       assert validar_luhn(numero) == True
   ```

2. **Property 2**: Para cualquier tipo, el prefijo debe ser correcto
   ```python
   # Feature: strands-engineering-workshop-agent, Property 2: Prefijo Correcto por Tipo de Tarjeta
   @given(tipo=st.sampled_from(["visa", "mastercard"]))
   def test_property_prefijo_correcto(tipo):
       numero = generar_tarjeta_prueba(tipo)
       if tipo == "visa":
           assert numero.startswith("4")
       else:
           assert numero.startswith("5")
   ```

#### Pruebas para generar_password_seguro

**Pruebas Unitarias**:
1. Test de ejemplo: Generar contraseña de 16 caracteres
2. Test de error: Longitud menor a 8 debe lanzar ValueError
3. Test de error: Longitud mayor a 128 debe lanzar ValueError
4. Test de borde: Longitud exactamente 8 debe funcionar

**Pruebas de Propiedades**:
1. **Property 3**: Para cualquier longitud válida, la contraseña debe tener esa longitud
   ```python
   # Feature: strands-engineering-workshop-agent, Property 3: Longitud Exacta de Contraseñas
   @given(longitud=st.integers(min_value=8, max_value=128))
   def test_property_longitud_password(longitud):
       password = generar_password_seguro(longitud)
       assert len(password) == longitud
   ```

2. **Property 4**: Para cualquier contraseña, debe contener todas las categorías
   ```python
   # Feature: strands-engineering-workshop-agent, Property 4: Composición Completa de Contraseñas
   @given(longitud=st.integers(min_value=8, max_value=128))
   def test_property_composicion_password(longitud):
       password = generar_password_seguro(longitud)
       assert any(c.isupper() for c in password)
       assert any(c.islower() for c in password)
       assert any(c.isdigit() for c in password)
       assert any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
   ```

#### Pruebas para calcular_volemia_nadler

**Pruebas Unitarias**:
1. Test de ejemplo: Calcular volemia para hombre de 70kg, 175cm
2. Test de ejemplo: Calcular volemia para mujer de 60kg, 165cm
3. Test de error: Peso fuera de rango debe lanzar ValueError
4. Test de error: Altura fuera de rango debe lanzar ValueError
5. Test de error: Género inválido debe lanzar ValueError
6. Test de borde: Valores en límites de rangos (20kg, 300kg, 100cm, 250cm)

**Pruebas de Propiedades**:
1. **Property 5**: Para cualquier entrada válida, el resultado debe coincidir con la fórmula
   ```python
   # Feature: strands-engineering-workshop-agent, Property 5: Precisión del Cálculo de Volemia
   @given(
       peso=st.floats(min_value=20, max_value=300),
       altura=st.floats(min_value=100, max_value=250),
       genero=st.sampled_from(["masculino", "femenino"])
   )
   def test_property_calculo_volemia(peso, altura, genero):
       resultado = calcular_volemia_nadler(peso, altura, genero)
       altura_m = altura / 100
       if genero.lower() == "masculino":
           esperado = 0.3669 * (altura_m ** 3) + 0.03219 * peso + 0.6041
       else:
           esperado = 0.3561 * (altura_m ** 3) + 0.03308 * peso + 0.1833
       assert abs(resultado["volumen_litros"] - esperado) < 0.001
   ```

2. **Property 6**: Para cualquier entrada inválida, debe lanzar error
   ```python
   # Feature: strands-engineering-workshop-agent, Property 6: Validación de Entrada en Herramientas
   @given(
       peso=st.one_of(
           st.floats(max_value=19.9),
           st.floats(min_value=300.1)
       )
   )
   def test_property_validacion_peso(peso):
       with pytest.raises(ValueError):
           calcular_volemia_nadler(peso, 170, "masculino")
   ```

#### Pruebas de Integración del Agente

**Pruebas Unitarias**:
1. Test de configuración: Verificar que el agente se inicializa con Bedrock
2. Test de configuración: Verificar que el system prompt es correcto
3. Test de configuración: Verificar que las tres herramientas están registradas
4. Test de error: Credenciales AWS inválidas deben informar error
5. Test de error: Modelo no disponible debe informar error

**Pruebas de Propiedades**:
1. **Property 7**: Para cualquier error en herramienta, el agente debe continuar
   ```python
   # Feature: strands-engineering-workshop-agent, Property 7: Resiliencia ante Errores
   @given(entrada_invalida=st.text())
   def test_property_resiliencia_agente(entrada_invalida):
       # Simular error en herramienta
       # Verificar que el agente no termina y puede procesar siguiente solicitud
       assert agente.is_running() == True
   ```

### Cobertura de Testing

**Objetivo de Cobertura**:
- Cobertura de líneas: Mínimo 80%
- Cobertura de ramas: Mínimo 70%
- Todas las propiedades de corrección deben tener prueba correspondiente

**Herramientas**:
- pytest para ejecución de pruebas
- pytest-cov para medición de cobertura
- hypothesis para property-based testing

**Comando de Ejecución**:
```bash
pytest --cov=. --cov-report=html --cov-report=term
```

### Estrategia de Testing Continuo

1. **Pre-commit**: Ejecutar pruebas unitarias rápidas
2. **CI/CD**: Ejecutar suite completa incluyendo property tests
3. **Nightly**: Ejecutar property tests con 1000+ iteraciones para mayor confianza


## Detalles de Implementación

### Algoritmo de Luhn (Detallado)

El algoritmo de Luhn es un método de suma de verificación usado para validar números de identificación:

**Pasos para Generar Dígito de Control**:
1. Generar 15 dígitos base según tipo de tarjeta
2. Comenzando desde el dígito más a la derecha (excluyendo el dígito de control):
   - Duplicar cada segundo dígito
   - Si el resultado es mayor que 9, restar 9
3. Sumar todos los dígitos (incluyendo los no duplicados)
4. El dígito de control es: `(10 - (suma % 10)) % 10`

**Ejemplo para Visa**:
```
Número base: 4532 0151 1283 036_
Posiciones:  1234 5678 9012 345

Duplicar posiciones pares (de derecha a izquierda):
Original: 4 5 3 2 0 1 5 1 1 2 8 3 0 3 6
Duplicar: 4 10 3 4 0 2 5 2 1 4 8 6 0 6 6
Ajustar:  4 1 3 4 0 2 5 2 1 4 8 6 0 6 6

Suma: 4+1+3+4+0+2+5+2+1+4+8+6+0+6+6 = 52
Dígito de control: (10 - (52 % 10)) % 10 = (10 - 2) % 10 = 8

Número completo: 4532 0151 1283 0368
```

**Implementación en Python**:
```python
def calcular_digito_luhn(numero_base: str) -> str:
    """Calcula el dígito de control usando algoritmo de Luhn"""
    digitos = [int(d) for d in numero_base]
    
    # Duplicar cada segundo dígito de derecha a izquierda
    for i in range(len(digitos) - 1, -1, -2):
        digitos[i] *= 2
        if digitos[i] > 9:
            digitos[i] -= 9
    
    suma = sum(digitos)
    digito_control = (10 - (suma % 10)) % 10
    
    return str(digito_control)
```

### Generación de Contraseñas Seguras (Detallado)

**Requisitos de Seguridad**:
- Usar `secrets` en lugar de `random` para garantizar aleatoriedad criptográfica
- Asegurar distribución uniforme de caracteres
- Garantizar presencia de todos los tipos de caracteres

**Algoritmo**:
```python
import secrets
import string

def generar_password_seguro(longitud: int = 16) -> str:
    if longitud < 8:
        raise ValueError(f"La longitud debe ser al menos 8 caracteres. Recibido: {longitud}")
    if longitud > 128:
        raise ValueError(f"La longitud máxima es 128 caracteres. Recibido: {longitud}")
    
    # Definir conjuntos de caracteres
    mayusculas = string.ascii_uppercase
    minusculas = string.ascii_lowercase
    digitos = string.digits
    simbolos = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    todos_caracteres = mayusculas + minusculas + digitos + simbolos
    
    # Asegurar al menos un carácter de cada tipo
    password = [
        secrets.choice(mayusculas),
        secrets.choice(minusculas),
        secrets.choice(digitos),
        secrets.choice(simbolos)
    ]
    
    # Completar con caracteres aleatorios
    password += [secrets.choice(todos_caracteres) for _ in range(longitud - 4)]
    
    # Mezclar para evitar patrón predecible
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)
```

### Fórmula de Nadler (Detallado)

La fórmula de Nadler estima el volumen sanguíneo total basándose en características antropométricas:

**Fórmulas Específicas por Género**:

**Hombres**:
```
V = 0.3669 × H³ + 0.03219 × W + 0.6041
```

**Mujeres**:
```
V = 0.3561 × H³ + 0.03308 × W + 0.1833
```

Donde:
- V = Volumen sanguíneo en litros
- H = Altura en metros
- W = Peso en kilogramos

**Implementación**:
```python
def calcular_volemia_nadler(peso: float, altura: float, genero: str) -> dict:
    # Validaciones
    if peso < 20 or peso > 300:
        raise ValueError(f"Peso debe estar entre 20 y 300 kg. Recibido: {peso} kg")
    if altura < 100 or altura > 250:
        raise ValueError(f"Altura debe estar entre 100 y 250 cm. Recibido: {altura} cm")
    
    genero_lower = genero.lower()
    if genero_lower not in ["masculino", "femenino"]:
        raise ValueError(f"Género debe ser 'masculino' o 'femenino'. Recibido: '{genero}'")
    
    # Convertir altura a metros
    altura_m = altura / 100
    
    # Aplicar fórmula según género
    if genero_lower == "masculino":
        volumen_litros = 0.3669 * (altura_m ** 3) + 0.03219 * peso + 0.6041
    else:
        volumen_litros = 0.3561 * (altura_m ** 3) + 0.03308 * peso + 0.1833
    
    return {
        "volumen_litros": round(volumen_litros, 2),
        "volumen_ml": round(volumen_litros * 1000, 0),
        "parametros": {
            "peso_kg": peso,
            "altura_cm": altura,
            "genero": genero
        }
    }
```


## Integración con Strands SDK y AWS Bedrock

### Configuración de Strands Agent

**Estructura Básica**:
```python
from strands_sdk import Agent, tool
from strands_sdk.models import BedrockModel

# Configurar modelo de Bedrock
model = BedrockModel(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    region="us-east-1",
    temperature=0.7,
    max_tokens=2048
)

# Definir system prompt
SYSTEM_PROMPT = """Eres un Asistente Técnico de Ingeniería para la Corporación 
Universitaria Latinoamericana. Tu objetivo es ayudar a estudiantes y profesionales 
con tareas técnicas específicas.

Tienes acceso a las siguientes herramientas:
- generar_tarjeta_prueba: Para crear números de tarjeta ficticios válidos
- generar_password_seguro: Para crear contraseñas criptográficamente seguras
- calcular_volemia_nadler: Para calcular volumen sanguíneo según parámetros antropométricos

Usa estas herramientas cuando el usuario lo solicite. Siempre explica qué estás haciendo 
y proporciona contexto sobre los resultados."""

# Crear agente
agent = Agent(
    name="AsistenteTecnicoIngenieria",
    system_prompt=SYSTEM_PROMPT,
    model=model,
    tools=[generar_tarjeta_prueba, generar_password_seguro, calcular_volemia_nadler],
    reasoning_enabled=True
)
```

### Decorador @tool

El decorador `@tool` del Strands SDK convierte funciones Python en herramientas que el agente puede invocar:

**Características**:
- Extrae automáticamente el docstring para que el LLM entienda la herramienta
- Maneja la serialización de parámetros y resultados
- Proporciona manejo de errores integrado

**Ejemplo de Uso**:
```python
from strands_sdk import tool

@tool
def generar_tarjeta_prueba(tipo: str = "visa") -> str:
    """
    Genera un número de tarjeta de crédito ficticio válido para pruebas.
    
    Esta herramienta crea números de tarjeta que pasan la validación del 
    algoritmo de Luhn, útiles para probar sistemas de pago sin usar datos reales.
    
    Args:
        tipo: Tipo de tarjeta a generar. Opciones: "visa" o "mastercard"
        
    Returns:
        str: Número de tarjeta de 16 dígitos válido según algoritmo de Luhn
    """
    # Implementación...
```

### Configuración de AWS Bedrock

**Credenciales**:
Las credenciales se cargan automáticamente desde:
1. Variables de entorno: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
2. Archivo de credenciales: `~/.aws/credentials`
3. Rol de IAM (si se ejecuta en EC2/ECS)

**Permisos IAM Requeridos**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-haiku-20240307-v1:0",
        "arn:aws:bedrock:*::foundation-model/amazon.titan-text-express-v1"
      ]
    }
  ]
}
```

**Modelos Soportados**:
- **Claude 3 Haiku**: `anthropic.claude-3-haiku-20240307-v1:0`
  - Rápido y económico
  - Excelente para tareas de razonamiento
  - Recomendado para este proyecto

- **Amazon Titan**: `amazon.titan-text-express-v1`
  - Alternativa de AWS
  - Buena relación costo-beneficio

### Flujo de Ejecución de Herramientas

1. **Usuario envía solicitud**: "Genera una tarjeta Visa de prueba"
2. **Agente procesa con LLM**: Bedrock interpreta la intención
3. **Selección de herramienta**: El LLM decide usar `generar_tarjeta_prueba`
4. **Extracción de parámetros**: El LLM extrae `tipo="visa"`
5. **Ejecución**: Strands SDK invoca la función Python
6. **Resultado**: La función retorna el número de tarjeta
7. **Respuesta**: El LLM formatea la respuesta para el usuario

**Diagrama de Secuencia**:
```
Usuario -> Agent: "Genera una tarjeta Visa"
Agent -> Bedrock: Procesar solicitud + herramientas disponibles
Bedrock -> Agent: Usar generar_tarjeta_prueba(tipo="visa")
Agent -> Tool: Ejecutar generar_tarjeta_prueba("visa")
Tool -> Agent: "4532015112830366"
Agent -> Bedrock: Formatear respuesta con resultado
Bedrock -> Agent: "He generado una tarjeta Visa de prueba: 4532015112830366"
Agent -> Usuario: Mostrar respuesta
```


## Consideraciones de Seguridad

### Generación de Números de Tarjeta

**Advertencias Importantes**:
- Los números generados son SOLO para pruebas
- NO usar en producción con sistemas de pago reales
- Incluir disclaimer en la salida de la herramienta

**Mitigaciones**:
- Documentar claramente el propósito de prueba
- No almacenar números generados en logs
- Agregar marca de agua en la respuesta: "⚠️ SOLO PARA PRUEBAS"

### Generación de Contraseñas

**Buenas Prácticas Implementadas**:
- Uso de `secrets` para aleatoriedad criptográfica
- No usar `random` que es predecible
- Longitud mínima de 8 caracteres (recomendado 16+)
- Inclusión obligatoria de todos los tipos de caracteres

**Advertencias al Usuario**:
- Las contraseñas generadas deben almacenarse de forma segura
- Usar un gestor de contraseñas
- No compartir contraseñas por canales inseguros

### Cálculo de Volemia

**Limitaciones Médicas**:
- La fórmula de Nadler es una estimación
- No sustituye evaluación médica profesional
- Resultados pueden variar según condiciones individuales

**Disclaimer Requerido**:
```
⚠️ AVISO MÉDICO: Este cálculo es una estimación basada en la fórmula de Nadler.
No debe usarse como única base para decisiones médicas. Consulte a un profesional
de la salud para evaluaciones clínicas precisas.
```

### Protección de Credenciales AWS

**Nunca Incluir en Código**:
- No hardcodear credenciales en el código fuente
- No commitear archivos de credenciales al repositorio
- Usar variables de entorno o servicios de secretos

**Archivo .gitignore**:
```
# Credenciales AWS
.aws/
*.pem
*.key

# Variables de entorno
.env
.env.local

# Logs que pueden contener información sensible
*.log
agent.log
```

### Validación de Entrada

**Principio de Defensa en Profundidad**:
1. **Validación en Herramientas**: Cada herramienta valida sus propios parámetros
2. **Sanitización**: Limpiar entradas antes de procesamiento
3. **Límites Estrictos**: Rangos definidos para todos los parámetros numéricos
4. **Mensajes de Error Seguros**: No revelar detalles de implementación interna

### Logging Seguro

**Qué NO Loggear**:
- Credenciales AWS
- Tokens de sesión
- Información personal identificable (PII)
- Contraseñas generadas (solo loggear que se generó, no el valor)

**Qué SÍ Loggear**:
- Eventos de inicio/cierre del agente
- Invocaciones de herramientas (sin parámetros sensibles)
- Errores y excepciones (sanitizados)
- Métricas de uso


## Estructura del Proyecto

### Organización de Archivos

```
strands-engineering-workshop-agent/
├── agent.py                 # Punto de entrada y lógica del agente
├── tools.py                 # Definiciones de herramientas
├── requirements.txt         # Dependencias del proyecto
├── .gitignore              # Archivos a ignorar en git
├── README.md               # Documentación del proyecto
├── tests/                  # Suite de pruebas
│   ├── __init__.py
│   ├── test_tools.py       # Pruebas de herramientas
│   ├── test_agent.py       # Pruebas del agente
│   └── conftest.py         # Configuración de pytest
└── .kiro/                  # Especificaciones del proyecto
    └── specs/
        └── strands-engineering-workshop-agent/
            ├── .config.kiro
            ├── requirements.md
            └── design.md
```

### Contenido de requirements.txt

```
# Framework de agentes
strands-sdk>=1.0.0

# AWS Bedrock
boto3>=1.28.0
botocore>=1.31.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
hypothesis>=6.82.0

# Utilidades
python-dotenv>=1.0.0
```

### Ejemplo de agent.py (Estructura)

```python
#!/usr/bin/env python3
"""
Agente de IA para Taller de Ingeniería
Corporación Universitaria Latinoamericana
"""

import logging
from strands_sdk import Agent
from strands_sdk.models import BedrockModel
from tools import generar_tarjeta_prueba, generar_password_seguro, calcular_volemia_nadler

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """..."""

def initialize_agent() -> Agent:
    """Inicializa el agente con configuración de Bedrock y herramientas"""
    # Implementación...

def run_interactive_loop(agent: Agent) -> None:
    """Ejecuta el bucle interactivo de entrada/salida"""
    # Implementación...

def main():
    """Punto de entrada principal"""
    # Implementación...

if __name__ == "__main__":
    main()
```

### Ejemplo de tools.py (Estructura)

```python
"""
Herramientas especializadas para el Agente de Ingeniería
"""

from strands_sdk import tool
import secrets
import string
import random

@tool
def generar_tarjeta_prueba(tipo: str = "visa") -> str:
    """Docstring detallado..."""
    # Implementación...

@tool
def generar_password_seguro(longitud: int = 16) -> str:
    """Docstring detallado..."""
    # Implementación...

@tool
def calcular_volemia_nadler(peso: float, altura: float, genero: str) -> dict:
    """Docstring detallado..."""
    # Implementación...
```

## Dependencias y Versiones

### Dependencias Principales

| Paquete | Versión Mínima | Propósito |
|---------|---------------|-----------|
| strands-sdk | 1.0.0 | Framework de agentes con capacidades de razonamiento |
| boto3 | 1.28.0 | SDK de AWS para acceso a Bedrock |
| botocore | 1.31.0 | Núcleo de boto3 |
| pytest | 7.4.0 | Framework de testing |
| hypothesis | 6.82.0 | Property-based testing |

### Compatibilidad

- **Python**: 3.9+
- **Sistema Operativo**: Linux, macOS, Windows
- **AWS Bedrock**: Regiones con soporte de Claude 3 Haiku o Titan

## Métricas y Monitoreo

### Métricas Clave

1. **Latencia de Respuesta**:
   - Tiempo desde solicitud del usuario hasta respuesta completa
   - Objetivo: < 3 segundos para operaciones simples

2. **Tasa de Éxito de Herramientas**:
   - Porcentaje de ejecuciones exitosas vs. errores
   - Objetivo: > 95%

3. **Uso de Tokens Bedrock**:
   - Tokens consumidos por solicitud
   - Importante para control de costos

4. **Selección Correcta de Herramientas**:
   - Porcentaje de veces que el LLM selecciona la herramienta correcta
   - Objetivo: > 90%

### Logging de Métricas

```python
import time

def log_tool_execution(tool_name: str, duration: float, success: bool):
    """Registra métricas de ejecución de herramientas"""
    logger.info(
        f"Tool: {tool_name}, Duration: {duration:.2f}s, Success: {success}"
    )
```

## Extensibilidad

### Agregar Nueva Herramienta

Para agregar una nueva herramienta al agente:

1. **Definir la función en tools.py**:
```python
@tool
def nueva_herramienta(parametro: tipo) -> tipo_retorno:
    """
    Docstring detallado que explica:
    - Propósito de la herramienta
    - Cuándo usarla
    - Parámetros y sus tipos
    - Qué retorna
    """
    # Validar entrada
    # Implementar lógica
    # Retornar resultado
```

2. **Importar en agent.py**:
```python
from tools import generar_tarjeta_prueba, generar_password_seguro, 
                  calcular_volemia_nadler, nueva_herramienta
```

3. **Agregar al agente**:
```python
agent = Agent(
    tools=[..., nueva_herramienta]
)
```

4. **Crear pruebas**:
   - Pruebas unitarias en `tests/test_tools.py`
   - Pruebas de propiedades si aplica

### Cambiar Modelo de Bedrock

Para usar un modelo diferente:

```python
# Cambiar de Claude 3 Haiku a Claude 3 Sonnet
model = BedrockModel(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    region="us-east-1"
)
```

Modelos disponibles:
- Claude 3 Haiku: Rápido y económico
- Claude 3 Sonnet: Balance entre velocidad y capacidad
- Claude 3 Opus: Máxima capacidad
- Amazon Titan: Alternativa de AWS


## Guía de Implementación

### Orden de Implementación Recomendado

1. **Fase 1: Configuración Básica**
   - Crear estructura de archivos
   - Configurar requirements.txt
   - Configurar .gitignore
   - Verificar credenciales AWS

2. **Fase 2: Implementar Herramientas**
   - Implementar generar_tarjeta_prueba con algoritmo de Luhn
   - Implementar generar_password_seguro con secrets
   - Implementar calcular_volemia_nadler con fórmulas
   - Agregar validaciones y manejo de errores

3. **Fase 3: Testing de Herramientas**
   - Escribir pruebas unitarias para cada herramienta
   - Escribir pruebas de propiedades
   - Verificar cobertura de código
   - Validar manejo de errores

4. **Fase 4: Integración del Agente**
   - Configurar Strands Agent con Bedrock
   - Registrar herramientas en el agente
   - Implementar bucle interactivo
   - Agregar logging

5. **Fase 5: Testing de Integración**
   - Probar flujo completo end-to-end
   - Verificar selección correcta de herramientas
   - Validar manejo de errores del agente
   - Probar resiliencia

6. **Fase 6: Documentación y Refinamiento**
   - Completar README.md
   - Agregar ejemplos de uso
   - Refinar mensajes de error
   - Optimizar system prompt

### Comandos de Desarrollo

**Instalar dependencias**:
```bash
pip install -r requirements.txt
```

**Ejecutar agente**:
```bash
python agent.py
```

**Ejecutar pruebas**:
```bash
# Todas las pruebas
pytest

# Con cobertura
pytest --cov=. --cov-report=html

# Solo pruebas de herramientas
pytest tests/test_tools.py

# Solo pruebas de propiedades
pytest -m property
```

**Verificar estilo de código**:
```bash
# Formatear código
black agent.py tools.py

# Verificar tipos
mypy agent.py tools.py

# Linting
pylint agent.py tools.py
```

### Configuración de Variables de Entorno

Crear archivo `.env` (no commitear):
```bash
# Credenciales AWS
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1

# Configuración del agente
BEDROCK_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
AGENT_TEMPERATURE=0.7
AGENT_MAX_TOKENS=2048

# Logging
LOG_LEVEL=INFO
```

Cargar en agent.py:
```python
from dotenv import load_dotenv
import os

load_dotenv()

model_id = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")
```

## Casos de Uso y Ejemplos

### Caso de Uso 1: Generar Tarjeta de Prueba

**Solicitud del Usuario**:
```
Usuario: Necesito un número de tarjeta Visa para probar mi sistema de pagos
```

**Respuesta Esperada**:
```
Agente: He generado un número de tarjeta Visa de prueba para ti:

4532 0151 1283 0366

⚠️ IMPORTANTE: Este número es SOLO para pruebas y desarrollo. 
No funcionará en sistemas de pago reales. El número es válido 
según el algoritmo de Luhn, lo que permite probar validaciones 
de formato.
```

### Caso de Uso 2: Generar Contraseña Segura

**Solicitud del Usuario**:
```
Usuario: Genera una contraseña segura de 20 caracteres
```

**Respuesta Esperada**:
```
Agente: He generado una contraseña criptográficamente segura de 20 caracteres:

aB3$xY9@mN2#pQ5!vL8&

Esta contraseña incluye:
- Letras mayúsculas y minúsculas
- Dígitos
- Símbolos especiales

⚠️ RECOMENDACIÓN: Guarda esta contraseña en un gestor de contraseñas 
seguro. No la compartas por canales inseguros.
```

### Caso de Uso 3: Calcular Volemia

**Solicitud del Usuario**:
```
Usuario: Calcula la volemia para un hombre de 75 kg y 180 cm
```

**Respuesta Esperada**:
```
Agente: He calculado el volumen sanguíneo usando la fórmula de Nadler:

Parámetros:
- Peso: 75 kg
- Altura: 180 cm
- Género: Masculino

Resultado:
- Volumen sanguíneo: 5.47 litros (5470 ml)

⚠️ AVISO MÉDICO: Este cálculo es una estimación basada en la fórmula 
de Nadler. No debe usarse como única base para decisiones médicas. 
Consulte a un profesional de la salud para evaluaciones clínicas precisas.
```

### Caso de Uso 4: Manejo de Errores

**Solicitud del Usuario**:
```
Usuario: Genera una contraseña de 5 caracteres
```

**Respuesta Esperada**:
```
Agente: No puedo generar una contraseña de 5 caracteres porque no cumple 
con los requisitos mínimos de seguridad.

Error: La longitud debe ser al menos 8 caracteres para garantizar 
seguridad adecuada.

¿Te gustaría que genere una contraseña de 8 caracteres o más?
```

## Consideraciones de Rendimiento

### Optimizaciones

1. **Caché de Configuración**:
   - Inicializar el agente una sola vez
   - Reutilizar conexión con Bedrock

2. **Validación Temprana**:
   - Validar parámetros antes de llamar a Bedrock
   - Reducir llamadas innecesarias al LLM

3. **Timeouts Apropiados**:
   - Configurar timeouts para llamadas a Bedrock
   - Implementar reintentos con backoff exponencial

### Límites y Cuotas

**AWS Bedrock**:
- Límite de tokens por minuto: Varía según región y modelo
- Límite de solicitudes concurrentes: Típicamente 10-50
- Costo por token: Consultar pricing de AWS

**Recomendaciones**:
- Monitorear uso de tokens
- Implementar rate limiting si es necesario
- Considerar caché de respuestas para consultas comunes

## Conclusión

Este diseño técnico proporciona una base sólida para implementar el Agente de IA del taller de ingeniería. Los componentes están diseñados para ser:

- **Modulares**: Fácil agregar nuevas herramientas
- **Testables**: Cobertura completa con unit tests y property tests
- **Seguros**: Validaciones robustas y manejo de errores
- **Mantenibles**: Código limpio y bien documentado
- **Extensibles**: Arquitectura que permite crecimiento

La implementación debe seguir las propiedades de corrección definidas y asegurar que todas las pruebas pasen antes de considerar el proyecto completo.

