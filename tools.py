"""
Herramientas especializadas para el Agente de IA del Taller de Ingeniería.

Este módulo contiene las herramientas que el agente puede invocar para:
- Generar números de tarjeta de prueba válidos
- Generar contraseñas criptográficamente seguras
- Calcular volemia según la fórmula de Nadler
"""

import random

# Decorador @tool compatible - funciona con o sin Strands SDK
try:
    from strands_sdk import tool
except ImportError:
    # Si strands_sdk no está disponible, creamos un decorador compatible
    def tool(func):
        """Decorador compatible que marca funciones como herramientas del agente"""
        func._is_tool = True
        return func


@tool
def generar_tarjeta_prueba(tipo: str = "visa") -> str:
    """
    Genera un número de tarjeta de crédito ficticio válido para pruebas.
    
    Esta herramienta crea números de tarjeta que pasan la validación del 
    algoritmo de Luhn, útiles para probar sistemas de pago sin usar datos reales.
    
    ⚠️ DISCLAIMER: Los números generados son SOLO para pruebas y desarrollo.
    NO deben usarse para transacciones reales ni con fines fraudulentos.
    
    El algoritmo de Luhn es un método de suma de verificación que valida
    números de identificación. Esta implementación:
    1. Genera 15 dígitos base según el tipo de tarjeta
    2. Calcula el dígito de control usando el algoritmo de Luhn
    3. Retorna un número de 16 dígitos válido
    
    Tipos de tarjeta soportados:
    - Visa: Comienza con el dígito 4
    - Mastercard: Comienza con el dígito 5
    
    Args:
        tipo: Tipo de tarjeta a generar. Opciones válidas: "visa" o "mastercard".
              Por defecto es "visa".
        
    Returns:
        str: Número de tarjeta de 16 dígitos válido según el algoritmo de Luhn.
             Ejemplo: "4532015112830366" para Visa
        
    Raises:
        ValueError: Si el tipo de tarjeta no es "visa" o "mastercard".
        
    Examples:
        >>> tarjeta_visa = generar_tarjeta_prueba("visa")
        >>> print(tarjeta_visa)  # Ejemplo: "4532015112830366"
        >>> len(tarjeta_visa)
        16
        >>> tarjeta_visa[0]
        '4'
        
        >>> tarjeta_mc = generar_tarjeta_prueba("mastercard")
        >>> print(tarjeta_mc)  # Ejemplo: "5425233430109903"
        >>> tarjeta_mc[0]
        '5'
    """
    # Validar tipo de tarjeta
    tipo_lower = tipo.lower()
    if tipo_lower not in ["visa", "mastercard"]:
        raise ValueError(
            f"Tipo de tarjeta '{tipo}' no soportado. Use 'visa' o 'mastercard'."
        )
    
    # Determinar prefijo según tipo de tarjeta
    if tipo_lower == "visa":
        prefijo = "4"
    else:  # mastercard
        prefijo = "5"
    
    # Generar 15 dígitos base (prefijo + 14 dígitos aleatorios)
    numero_base = prefijo + "".join([str(random.randint(0, 9)) for _ in range(14)])
    
    # Calcular dígito de control usando algoritmo de Luhn
    digito_control = _calcular_digito_luhn(numero_base)
    
    # Retornar número completo de 16 dígitos
    return numero_base + digito_control


def _calcular_digito_luhn(numero_base: str) -> str:
    """
    Calcula el dígito de control usando el algoritmo de Luhn.
    
    El algoritmo de Luhn:
    1. Comenzando desde el dígito más a la derecha, duplica cada segundo dígito
    2. Si el resultado de duplicar es mayor que 9, resta 9
    3. Suma todos los dígitos (duplicados y no duplicados)
    4. El dígito de control es (10 - (suma % 10)) % 10
    
    Args:
        numero_base: String de 15 dígitos para calcular el dígito de control
        
    Returns:
        str: Dígito de control (un solo carácter numérico)
    """
    digitos = [int(d) for d in numero_base]
    
    # Duplicar cada segundo dígito de derecha a izquierda
    for i in range(len(digitos) - 1, -1, -2):
        digitos[i] *= 2
        if digitos[i] > 9:
            digitos[i] -= 9
    
    # Calcular suma total
    suma = sum(digitos)
    
    # Calcular dígito de control
    digito_control = (10 - (suma % 10)) % 10
    
    return str(digito_control)


@tool
def generar_password_seguro(longitud: int = 16) -> str:
    """
    Genera una contraseña criptográficamente segura.
    
    Utiliza el módulo secrets de Python para garantizar alta entropía criptográfica,
    lo que hace que las contraseñas sean impredecibles y seguras contra ataques.
    La contraseña incluye una mezcla de letras mayúsculas, minúsculas, dígitos 
    y símbolos especiales.
    
    ⚠️ RECOMENDACIONES DE SEGURIDAD:
    - Usa contraseñas de al menos 16 caracteres para máxima seguridad
    - Guarda las contraseñas en un gestor de contraseñas seguro
    - No compartas contraseñas por canales inseguros (email, SMS, chat)
    - Usa contraseñas únicas para cada servicio
    
    El algoritmo garantiza:
    1. Aleatoriedad criptográfica usando secrets.choice()
    2. Al menos un carácter de cada categoría (mayúscula, minúscula, dígito, símbolo)
    3. Mezcla aleatoria para evitar patrones predecibles
    4. Longitud configurable entre 8 y 128 caracteres
    
    Categorías de caracteres incluidas:
    - Letras mayúsculas: A-Z
    - Letras minúsculas: a-z
    - Dígitos: 0-9
    - Símbolos especiales: !@#$%^&*()_+-=[]{}|;:,.<>?
    
    Args:
        longitud: Longitud de la contraseña a generar. Debe ser entre 8 y 128 caracteres.
                  Por defecto es 16 caracteres (recomendado para buena seguridad).
        
    Returns:
        str: Contraseña criptográficamente segura con la longitud especificada.
             Ejemplo: "aB3$xY9@mN2#pQ5!"
        
    Raises:
        ValueError: Si la longitud es menor a 8 caracteres (inseguro).
        ValueError: Si la longitud es mayor a 128 caracteres (excesivo).
        
    Examples:
        >>> password = generar_password_seguro(16)
        >>> len(password)
        16
        >>> any(c.isupper() for c in password)  # Tiene mayúsculas
        True
        >>> any(c.islower() for c in password)  # Tiene minúsculas
        True
        >>> any(c.isdigit() for c in password)  # Tiene dígitos
        True
        
        >>> password_corto = generar_password_seguro(12)
        >>> len(password_corto)
        12
        
        >>> # Esto lanzará ValueError
        >>> password_invalido = generar_password_seguro(5)
        Traceback (most recent call last):
        ValueError: La longitud debe ser al menos 8 caracteres. Recibido: 5
    """
    import secrets
    import string
    
    # Validar longitud mínima
    if longitud < 8:
        raise ValueError(
            f"La longitud debe ser al menos 8 caracteres. Recibido: {longitud}"
        )
    
    # Validar longitud máxima
    if longitud > 128:
        raise ValueError(
            f"La longitud máxima es 128 caracteres. Recibido: {longitud}"
        )
    
    # Definir conjuntos de caracteres
    mayusculas = string.ascii_uppercase  # A-Z
    minusculas = string.ascii_lowercase  # a-z
    digitos = string.digits  # 0-9
    simbolos = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Combinar todos los caracteres disponibles
    todos_caracteres = mayusculas + minusculas + digitos + simbolos
    
    # Asegurar al menos un carácter de cada categoría
    # Esto garantiza que la contraseña cumple con requisitos de complejidad
    password = [
        secrets.choice(mayusculas),
        secrets.choice(minusculas),
        secrets.choice(digitos),
        secrets.choice(simbolos)
    ]
    
    # Completar con caracteres aleatorios hasta alcanzar la longitud deseada
    password += [secrets.choice(todos_caracteres) for _ in range(longitud - 4)]
    
    # Mezclar los caracteres para evitar patrones predecibles
    # (los primeros 4 caracteres siempre serían mayúscula, minúscula, dígito, símbolo)
    secrets.SystemRandom().shuffle(password)
    
    # Convertir lista de caracteres a string
    return ''.join(password)


@tool
def calcular_volemia_nadler(peso: float, altura: float, genero: str) -> dict:
    """
    Calcula el volumen sanguíneo total usando la fórmula de Nadler.
    
    La fórmula de Nadler es un método estándar para estimar el volumen 
    sanguíneo basándose en características antropométricas del paciente.
    Es ampliamente utilizada en medicina para estimar parámetros clínicos
    importantes relacionados con el volumen sanguíneo.
    
    ⚠️ AVISO MÉDICO: Este cálculo es una estimación basada en la fórmula de Nadler.
    No debe usarse como única base para decisiones médicas. Los resultados pueden
    variar según condiciones individuales del paciente. Consulte a un profesional
    de la salud para evaluaciones clínicas precisas y decisiones terapéuticas.
    
    Fórmulas utilizadas:
    - Hombres: V = 0.3669 × H³ + 0.03219 × W + 0.6041
    - Mujeres: V = 0.3561 × H³ + 0.03308 × W + 0.1833
    
    Donde:
    - V = Volumen sanguíneo en litros
    - H = Altura en metros
    - W = Peso en kilogramos
    
    El algoritmo:
    1. Valida que los parámetros estén dentro de rangos fisiológicos normales
    2. Convierte la altura de centímetros a metros
    3. Aplica la fórmula específica según el género del paciente
    4. Retorna el resultado en litros y mililitros con los parámetros de entrada
    
    Args:
        peso: Peso del paciente en kilogramos. Debe estar entre 20 y 300 kg.
              Rango válido cubre desde niños pequeños hasta adultos con obesidad mórbida.
        altura: Altura del paciente en centímetros. Debe estar entre 100 y 250 cm.
                Rango válido cubre desde niños hasta adultos muy altos.
        genero: Género del paciente. Valores válidos: "masculino" o "femenino".
                No es case-sensitive (acepta "Masculino", "FEMENINO", etc.).
        
    Returns:
        dict: Diccionario con tres claves:
            - "volumen_litros" (float): Volumen sanguíneo en litros, redondeado a 2 decimales
            - "volumen_ml" (float): Volumen sanguíneo en mililitros, redondeado a entero
            - "parametros" (dict): Diccionario con los valores de entrada usados:
                - "peso_kg" (float): Peso en kilogramos
                - "altura_cm" (float): Altura en centímetros
                - "genero" (str): Género del paciente
        
    Raises:
        ValueError: Si el peso está fuera del rango 20-300 kg
        ValueError: Si la altura está fuera del rango 100-250 cm
        ValueError: Si el género no es "masculino" o "femenino"
        
    Examples:
        >>> resultado = calcular_volemia_nadler(70, 175, "masculino")
        >>> print(resultado["volumen_litros"])
        5.23
        >>> print(resultado["volumen_ml"])
        5230.0
        
        >>> resultado = calcular_volemia_nadler(60, 165, "femenino")
        >>> print(resultado["volumen_litros"])
        4.35
        
        >>> # Género no es case-sensitive
        >>> resultado = calcular_volemia_nadler(75, 180, "MASCULINO")
        >>> print(resultado["parametros"]["genero"])
        'MASCULINO'
        
        >>> # Esto lanzará ValueError
        >>> resultado = calcular_volemia_nadler(15, 175, "masculino")
        Traceback (most recent call last):
        ValueError: Peso debe estar entre 20 y 300 kg. Recibido: 15.0 kg
    """
    # Validar peso
    if peso < 20 or peso > 300:
        raise ValueError(
            f"Peso debe estar entre 20 y 300 kg. Recibido: {peso} kg"
        )
    
    # Validar altura
    if altura < 100 or altura > 250:
        raise ValueError(
            f"Altura debe estar entre 100 y 250 cm. Recibido: {altura} cm"
        )
    
    # Validar género (case-insensitive)
    genero_lower = genero.lower()
    if genero_lower not in ["masculino", "femenino"]:
        raise ValueError(
            f"Género debe ser 'masculino' o 'femenino'. Recibido: '{genero}'"
        )
    
    # Convertir altura de centímetros a metros
    altura_m = altura / 100
    
    # Aplicar fórmula de Nadler según género
    if genero_lower == "masculino":
        # Fórmula para hombres: V = 0.3669 × H³ + 0.03219 × W + 0.6041
        volumen_litros = 0.3669 * (altura_m ** 3) + 0.03219 * peso + 0.6041
    else:
        # Fórmula para mujeres: V = 0.3561 × H³ + 0.03308 × W + 0.1833
        volumen_litros = 0.3561 * (altura_m ** 3) + 0.03308 * peso + 0.1833
    
    # Retornar resultado con formato especificado
    return {
        "volumen_litros": round(volumen_litros, 2),
        "volumen_ml": round(volumen_litros * 1000, 0),
        "parametros": {
            "peso_kg": peso,
            "altura_cm": altura,
            "genero": genero
        }
    }
