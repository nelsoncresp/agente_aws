# 🤖 Agente de IA para Taller de Ingeniería

**Corporación Universitaria Latinoamericana**

Agente de IA conversacional que funciona como Asistente Técnico de Ingeniería, utilizando Amazon Bedrock y el framework Strands Agents para proporcionar herramientas especializadas.

---

## 📋 Descripción del Proyecto

Este proyecto implementa un agente de IA con tres herramientas especializadas:

1. **Generador de Tarjetas de Prueba** - Crea números de tarjeta Visa/Mastercard válidos usando el algoritmo de Luhn
2. **Generador de Contraseñas Seguras** - Genera contraseñas criptográficamente seguras con alta entropía
3. **Calculadora de Volemia** - Calcula el volumen sanguíneo total usando la fórmula de Nadler

---

## 🎯 Características

- ✅ **Algoritmo de Luhn** implementado correctamente para validación de tarjetas
- ✅ **Generación criptográfica** usando el módulo `secrets` de Python
- ✅ **Fórmulas médicas** de Nadler para cálculo de volemia por género
- ✅ **Interfaz interactiva** de línea de comandos
- ✅ **Manejo robusto de errores** con validaciones completas
- ✅ **Logging completo** para debugging y auditoría
- ✅ **Modo local** funcional sin dependencias de Strands SDK
- ✅ **Compatible con Bedrock** cuando Strands SDK está instalado

---

## 🔧 Requisitos Previos

### Software Requerido
- **Python 3.9+**
- **pip** (gestor de paquetes de Python)

### Dependencias Opcionales
- **Strands SDK** (para integración con Amazon Bedrock)
- **Credenciales AWS** (para usar Amazon Bedrock)

---

## 📦 Instalación

### 1. Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd strands-engineering-workshop-agent
```

### 2. Crear Entorno Virtual (Recomendado)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar Dependencias Básicas
```bash
pip install -r requirements.txt
```

**Nota:** El proyecto funciona sin Strands SDK instalado. Las herramientas están completamente funcionales en modo local.

### 4. (Opcional) Configurar AWS Credentials

Si deseas usar Amazon Bedrock, configura tus credenciales:

**Opción 1: Variables de Entorno**
```bash
# Windows (PowerShell)
$env:AWS_ACCESS_KEY_ID="tu_access_key"
$env:AWS_SECRET_ACCESS_KEY="tu_secret_key"
$env:AWS_DEFAULT_REGION="us-east-1"

# Linux/Mac
export AWS_ACCESS_KEY_ID=tu_access_key
export AWS_SECRET_ACCESS_KEY=tu_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

**Opción 2: Archivo de Credenciales**
```bash
# Crear archivo ~/.aws/credentials
[default]
aws_access_key_id = tu_access_key
aws_secret_access_key = tu_secret_key
region = us-east-1
```

---

## 🚀 Uso

### Modo Interactivo

Ejecuta el agente en modo interactivo:

```bash
python agent.py
```

**Ejemplo de sesión:**
```
============================================================
🤖 ASISTENTE TÉCNICO DE INGENIERÍA - CUL
============================================================
⚠️  MODO LOCAL (Sin Strands SDK)
Herramientas disponibles: tarjeta, password, volemia
Escribe 'salir' para terminar

Usuario >>> genera una tarjeta visa
✅ Tarjeta Visa generada: 4532015112830366
⚠️  SOLO para pruebas - NO usar en producción

Usuario >>> necesito una contraseña de 16 caracteres
✅ Contraseña segura generada (16 caracteres):
   aB3$xY9@mN2#pQ5!
⚠️  Guárdala en un gestor de contraseñas seguro

Usuario >>> calcula volemia
📊 Calculadora de Volemia (Fórmula de Nadler)
Ingresa los datos del paciente:
  Peso (kg): 70
  Altura (cm): 175
  Género (masculino/femenino): masculino

✅ Volumen sanguíneo estimado:
   4.82 litros (4824.0 ml)
   Parámetros: {'peso_kg': 70.0, 'altura_cm': 175.0, 'genero': 'masculino'}
⚠️  Estimación - Consulte a un profesional médico

Usuario >>> salir
👋 Sesión terminada. ¡Hasta pronto!
```

### Demostración Automatizada

Ejecuta el script de demostración para ver todas las funcionalidades:

```bash
python demo_agent.py
```

### Pruebas Automatizadas

Ejecuta la suite de pruebas completa:

```bash
python test_agent.py
```

---

## 🛠️ Herramientas Disponibles

### 1. Generador de Tarjetas de Prueba

**Función:** `generar_tarjeta_prueba(tipo: str = "visa") -> str`

**Descripción:** Genera números de tarjeta de crédito ficticios válidos usando el algoritmo de Luhn.

**Parámetros:**
- `tipo`: Tipo de tarjeta ("visa" o "mastercard")

**Ejemplo:**
```python
from tools import generar_tarjeta_prueba

# Generar tarjeta Visa
tarjeta_visa = generar_tarjeta_prueba("visa")
print(tarjeta_visa)  # Ejemplo: "4532015112830366"

# Generar tarjeta Mastercard
tarjeta_mc = generar_tarjeta_prueba("mastercard")
print(tarjeta_mc)  # Ejemplo: "5425233430109903"
```

**⚠️ IMPORTANTE:** Los números generados son SOLO para pruebas. NO usar en producción.

---

### 2. Generador de Contraseñas Seguras

**Función:** `generar_password_seguro(longitud: int = 16) -> str`

**Descripción:** Genera contraseñas criptográficamente seguras usando el módulo `secrets`.

**Parámetros:**
- `longitud`: Longitud de la contraseña (8-128 caracteres, recomendado 16+)

**Ejemplo:**
```python
from tools import generar_password_seguro

# Generar contraseña de 16 caracteres
password = generar_password_seguro(16)
print(password)  # Ejemplo: "aB3$xY9@mN2#pQ5!"

# Generar contraseña más larga
password_largo = generar_password_seguro(24)
print(password_largo)
```

**Características:**
- ✅ Alta entropía criptográfica
- ✅ Incluye mayúsculas, minúsculas, dígitos y símbolos
- ✅ Mezcla aleatoria para evitar patrones

---

### 3. Calculadora de Volemia (Fórmula de Nadler)

**Función:** `calcular_volemia_nadler(peso: float, altura: float, genero: str) -> dict`

**Descripción:** Calcula el volumen sanguíneo total usando la fórmula de Nadler.

**Parámetros:**
- `peso`: Peso en kilogramos (20-300 kg)
- `altura`: Altura en centímetros (100-250 cm)
- `genero`: "masculino" o "femenino" (case-insensitive)

**Ejemplo:**
```python
from tools import calcular_volemia_nadler

# Calcular para hombre
resultado = calcular_volemia_nadler(70, 175, "masculino")
print(resultado)
# {
#   'volumen_litros': 4.82,
#   'volumen_ml': 4824.0,
#   'parametros': {'peso_kg': 70, 'altura_cm': 175, 'genero': 'masculino'}
# }

# Calcular para mujer
resultado = calcular_volemia_nadler(60, 165, "femenino")
print(resultado['volumen_litros'])  # 3.77
```

**Fórmulas:**
- **Hombres:** V = 0.3669 × H³ + 0.03219 × W + 0.6041
- **Mujeres:** V = 0.3561 × H³ + 0.03308 × W + 0.1833

**⚠️ AVISO MÉDICO:** Esta es una estimación. Consulte a un profesional de la salud.

---

## 📁 Estructura del Proyecto

```
strands-engineering-workshop-agent/
├── agent.py                    # Punto de entrada del agente
├── tools.py                    # Definiciones de herramientas
├── requirements.txt            # Dependencias del proyecto
├── .gitignore                  # Archivos a ignorar en git
├── README.md                   # Este archivo
├── CORRECCIONES_SRE.md        # Documentación de correcciones
├── test_agent.py              # Suite de pruebas
├── demo_agent.py              # Script de demostración
├── tests/                     # Directorio de pruebas
│   ├── __init__.py
│   ├── conftest.py            # Configuración de pytest
│   ├── test_tools.py          # Pruebas de herramientas
│   └── test_agent.py          # Pruebas del agente
└── .kiro/                     # Especificaciones del proyecto
    └── specs/
        └── strands-engineering-workshop-agent/
            ├── .config.kiro
            ├── requirements.md
            ├── design.md
            └── tasks.md
```

---

## 🧪 Testing

### Ejecutar Todas las Pruebas
```bash
pytest
```

### Ejecutar con Cobertura
```bash
pytest --cov=. --cov-report=html --cov-report=term
```

### Ejecutar Pruebas Específicas
```bash
# Solo pruebas de herramientas
pytest tests/test_tools.py

# Solo pruebas del agente
pytest tests/test_agent.py
```

---

## 🔒 Consideraciones de Seguridad

### Generación de Tarjetas
- ⚠️ Los números son SOLO para pruebas
- ⚠️ NO usar en sistemas de producción
- ⚠️ NO usar para transacciones reales

### Generación de Contraseñas
- ✅ Usa `secrets` para aleatoriedad criptográfica
- ✅ Longitud mínima de 8 caracteres (recomendado 16+)
- ⚠️ Guarda las contraseñas en un gestor seguro
- ⚠️ No compartas por canales inseguros

### Cálculo de Volemia
- ⚠️ Solo para estimaciones educativas
- ⚠️ NO sustituye evaluación médica profesional
- ⚠️ Consulta a un profesional de la salud

### Credenciales AWS
- ⚠️ NUNCA commitear credenciales al repositorio
- ✅ Usar variables de entorno o archivos de configuración
- ✅ Agregar archivos sensibles a .gitignore

---

## 📊 Configuración de Bedrock

El agente está configurado para usar:

- **Modelo:** Claude 3 Haiku (`anthropic.claude-3-haiku-20240307-v1:0`)
- **Región:** us-east-1
- **Temperature:** 0.7
- **Max Tokens:** 2048

Puedes modificar estos valores en `agent.py`:

```python
BEDROCK_CONFIG = {
    "model_id": "anthropic.claude-3-haiku-20240307-v1:0",
    "region": "us-east-1",
    "temperature": 0.7,
    "max_tokens": 2048
}
```

---

## 🐛 Solución de Problemas

### Error: ModuleNotFoundError: No module named 'strands_sdk'

**Solución:** El proyecto funciona sin Strands SDK. El agente detecta automáticamente si la librería está disponible y usa modo local si no lo está.

Si deseas instalar Strands SDK:
```bash
pip install strands-sdk boto3
```

### Error: No AWS credentials found

**Solución:** Configura tus credenciales AWS usando variables de entorno o el archivo `~/.aws/credentials`.

### Error: ValueError en herramientas

**Solución:** Verifica que los parámetros estén dentro de los rangos válidos:
- Tarjetas: tipo debe ser "visa" o "mastercard"
- Contraseñas: longitud entre 8 y 128
- Volemia: peso 20-300 kg, altura 100-250 cm, género "masculino"/"femenino"

---

## 📝 Logging

El agente genera logs en:
- **Archivo:** `agent.log`
- **Consola:** Salida estándar

Niveles de log:
- **INFO:** Operaciones normales
- **WARNING:** Advertencias (ej: Strands SDK no disponible)
- **ERROR:** Errores recuperables
- **CRITICAL:** Errores críticos

---

## 🤝 Contribuciones

Este proyecto fue desarrollado como parte del taller de ingeniería de la Corporación Universitaria Latinoamericana.

---

## 📄 Licencia

Este proyecto es de uso educativo para la Corporación Universitaria Latinoamericana.

---

## 👨‍💻 Autor

**Taller de Ingeniería - CUL**  
Asistente Técnico de Ingeniería con IA

---

## 📚 Referencias

- [Algoritmo de Luhn](https://en.wikipedia.org/wiki/Luhn_algorithm)
- [Python secrets module](https://docs.python.org/3/library/secrets.html)
- [Fórmula de Nadler](https://pubmed.ncbi.nlm.nih.gov/14907713/)
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Strands SDK](https://github.com/strands-ai/strands-sdk)

---

## 🎓 Comandos Rápidos

```bash
# Ejecutar agente interactivo
python agent.py

# Ejecutar demostración
python demo_agent.py

# Ejecutar pruebas
python test_agent.py

# Ejecutar pruebas con pytest
pytest

# Ver cobertura de código
pytest --cov=. --cov-report=html

# Verificar imports
python -c "from tools import *; print('OK')"
```

---

**¡Listo para usar! 🚀**
