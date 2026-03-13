#!/usr/bin/env python3
"""
Agente de IA para Taller de Ingeniería
Corporación Universitaria Latinoamericana

Este agente funciona como Asistente Técnico de Ingeniería utilizando
Amazon Bedrock (cuando está disponible) o en modo local para desarrollo.
"""

import logging
import sys

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Importar herramientas
from tools import generar_tarjeta_prueba, generar_password_seguro, calcular_volemia_nadler

# Configuración de Bedrock
BEDROCK_CONFIG = {
    "model_id": "anthropic.claude-3-haiku-20240307-v1:0",
    "region": "us-east-1",
    "temperature": 0.7,
    "max_tokens": 2048
}

# System Prompt del agente
SYSTEM_PROMPT = """Eres un Asistente Técnico de Ingeniería para la Corporación 
Universitaria Latinoamericana. Tu objetivo es ayudar a estudiantes y profesionales 
con tareas técnicas específicas.

Tienes acceso a las siguientes herramientas:
- generar_tarjeta_prueba: Para crear números de tarjeta ficticios válidos para pruebas
- generar_password_seguro: Para crear contraseñas criptográficamente seguras
- calcular_volemia_nadler: Para calcular volumen sanguíneo según parámetros antropométricos

Usa estas herramientas cuando el usuario lo solicite. Siempre explica qué estás haciendo 
y proporciona contexto sobre los resultados."""


def initialize_agent():
    """
    Inicializa el agente con configuración de Bedrock y herramientas.
    
    Intenta usar Strands SDK si está disponible, de lo contrario
    retorna None para usar modo local.
    
    Returns:
        Agent: Instancia del agente configurado, o None si no está disponible
    """
    try:
        # Intentar importar Strands SDK
        from strands_sdk import Agent
        from strands_sdk.models import BedrockModel
        
        logger.info("Inicializando agente con Strands SDK y Amazon Bedrock...")
        
        # Configurar modelo de Bedrock
        model = BedrockModel(
            model_id=BEDROCK_CONFIG["model_id"],
            region=BEDROCK_CONFIG["region"],
            temperature=BEDROCK_CONFIG["temperature"],
            max_tokens=BEDROCK_CONFIG["max_tokens"]
        )
        
        # Crear agente
        agent = Agent(
            name="AsistenteTecnicoIngenieria",
            system_prompt=SYSTEM_PROMPT,
            model=model,
            tools=[generar_tarjeta_prueba, generar_password_seguro, calcular_volemia_nadler],
            reasoning_enabled=True
        )
        
        logger.info("Agente inicializado exitosamente con Bedrock")
        return agent
        
    except ImportError as e:
        logger.warning(f"Strands SDK no disponible: {e}")
        logger.info("Iniciando en modo local sin Bedrock")
        return None
        
    except Exception as e:
        logger.error(f"Error al inicializar agente con Bedrock: {e}")
        logger.info("Fallback a modo local")
        return None


def run_interactive_loop(agent=None):
    """
    Ejecuta el bucle interactivo de entrada/salida.
    
    Si el agente está disponible, usa agent.repl().
    Si no, implementa un bucle local simple para demostración.
    
    Args:
        agent: Instancia del agente de Strands SDK, o None para modo local
    """
    if agent is not None:
        # Modo con Strands SDK
        logger.info("Iniciando interfaz interactiva con Strands Agent")
        print("\n" + "="*60)
        print("🤖 ASISTENTE TÉCNICO DE INGENIERÍA - CUL")
        print("="*60)
        print("Powered by Amazon Bedrock & Strands SDK")
        print("Escribe 'salir' o presiona Ctrl+C para terminar\n")
        
        try:
            agent.repl()
        except KeyboardInterrupt:
            print("\n\n👋 Sesión terminada. ¡Hasta pronto!")
            logger.info("Sesión terminada por el usuario")
        except Exception as e:
            logger.error(f"Error durante la ejecución del agente: {e}")
            print(f"\n❌ Error: {e}")
    else:
        # Modo local sin Strands SDK
        logger.info("Iniciando interfaz interactiva en modo local")
        print("\n" + "="*60)
        print("🤖 ASISTENTE TÉCNICO DE INGENIERÍA - CUL")
        print("="*60)
        print("⚠️  MODO LOCAL (Sin Strands SDK)")
        print("Herramientas disponibles: tarjeta, password, volemia")
        print("Escribe 'salir' para terminar\n")
        
        try:
            while True:
                user_input = input("Usuario >>> ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ["salir", "exit", "quit"]:
                    print("\n👋 Sesión terminada. ¡Hasta pronto!")
                    break
                
                # Procesamiento simple basado en palabras clave
                user_lower = user_input.lower()
                
                try:
                    if "tarjeta" in user_lower or "visa" in user_lower or "mastercard" in user_lower:
                        tipo = "mastercard" if "mastercard" in user_lower else "visa"
                        resultado = generar_tarjeta_prueba(tipo)
                        print(f"\n✅ Tarjeta {tipo.capitalize()} generada: {resultado}")
                        print("⚠️  SOLO para pruebas - NO usar en producción\n")
                        
                    elif "password" in user_lower or "contraseña" in user_lower or "clave" in user_lower:
                        # Extraer longitud si se menciona
                        longitud = 16
                        for word in user_input.split():
                            if word.isdigit():
                                longitud = int(word)
                                break
                        resultado = generar_password_seguro(longitud)
                        print(f"\n✅ Contraseña segura generada ({longitud} caracteres):")
                        print(f"   {resultado}")
                        print("⚠️  Guárdala en un gestor de contraseñas seguro\n")
                        
                    elif "volemia" in user_lower or "sangre" in user_lower or "nadler" in user_lower:
                        print("\n📊 Calculadora de Volemia (Fórmula de Nadler)")
                        print("Ingresa los datos del paciente:")
                        
                        peso = float(input("  Peso (kg): "))
                        altura = float(input("  Altura (cm): "))
                        genero = input("  Género (masculino/femenino): ").strip()
                        
                        resultado = calcular_volemia_nadler(peso, altura, genero)
                        print(f"\n✅ Volumen sanguíneo estimado:")
                        print(f"   {resultado['volumen_litros']} litros ({resultado['volumen_ml']} ml)")
                        print(f"   Parámetros: {resultado['parametros']}")
                        print("⚠️  Estimación - Consulte a un profesional médico\n")
                        
                    elif "ayuda" in user_lower or "help" in user_lower:
                        print("\n📚 Herramientas disponibles:")
                        print("  • 'tarjeta' - Generar número de tarjeta de prueba")
                        print("  • 'password' - Generar contraseña segura")
                        print("  • 'volemia' - Calcular volumen sanguíneo (Nadler)")
                        print("  • 'salir' - Terminar sesión\n")
                        
                    else:
                        print("\n🤔 No entendí tu solicitud. Escribe 'ayuda' para ver las opciones.\n")
                        
                except ValueError as e:
                    print(f"\n❌ Error de validación: {e}\n")
                except Exception as e:
                    logger.error(f"Error procesando solicitud: {e}")
                    print(f"\n❌ Error: {e}\n")
                    
        except KeyboardInterrupt:
            print("\n\n👋 Sesión terminada. ¡Hasta pronto!")
            logger.info("Sesión terminada por el usuario")
        except Exception as e:
            logger.error(f"Error crítico en bucle interactivo: {e}")
            print(f"\n❌ Error crítico: {e}")


def main():
    """
    Punto de entrada principal del agente.
    
    Inicializa el agente y ejecuta el bucle interactivo.
    Maneja errores de nivel superior con mensajes claros.
    """
    try:
        logger.info("Iniciando Asistente Técnico de Ingeniería")
        
        # Inicializar agente (con Bedrock si está disponible)
        agent = initialize_agent()
        
        # Ejecutar bucle interactivo
        run_interactive_loop(agent)
        
    except KeyboardInterrupt:
        print("\n\n👋 Sesión terminada por el usuario")
        logger.info("Aplicación terminada por el usuario")
        sys.exit(0)
        
    except Exception as e:
        logger.critical(f"Error crítico en main: {e}", exc_info=True)
        print(f"\n❌ Error crítico: {e}")
        print("Revisa el archivo agent.log para más detalles")
        sys.exit(1)


if __name__ == "__main__":
    main()