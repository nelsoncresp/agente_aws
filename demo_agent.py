#!/usr/bin/env python3
"""
Script de demostración del agente en modo no interactivo
Simula comandos del usuario para mostrar funcionalidad
"""

from tools import generar_tarjeta_prueba, generar_password_seguro, calcular_volemia_nadler

print("\n" + "="*60)
print("🤖 DEMOSTRACIÓN DEL ASISTENTE TÉCNICO DE INGENIERÍA")
print("Corporación Universitaria Latinoamericana")
print("="*60)

# Simulación 1: Usuario pide tarjeta Visa
print("\n👤 Usuario: Genera una tarjeta Visa de prueba")
print("🤖 Asistente: Generando tarjeta Visa...")
tarjeta = generar_tarjeta_prueba("visa")
print(f"   ✅ Tarjeta generada: {tarjeta}")
print("   ⚠️  IMPORTANTE: Este número es SOLO para pruebas.")
print("   No funcionará en sistemas de pago reales.")

# Simulación 2: Usuario pide contraseña
print("\n👤 Usuario: Necesito una contraseña segura de 20 caracteres")
print("🤖 Asistente: Generando contraseña criptográficamente segura...")
password = generar_password_seguro(20)
print(f"   ✅ Contraseña generada: {password}")
print("   📝 Características:")
print(f"      • Longitud: {len(password)} caracteres")
print(f"      • Mayúsculas: {'✓' if any(c.isupper() for c in password) else '✗'}")
print(f"      • Minúsculas: {'✓' if any(c.islower() for c in password) else '✗'}")
print(f"      • Dígitos: {'✓' if any(c.isdigit() for c in password) else '✗'}")
print(f"      • Símbolos: {'✓' if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password) else '✗'}")
print("   ⚠️  Guarda esta contraseña en un gestor seguro.")

# Simulación 3: Usuario pide cálculo de volemia
print("\n👤 Usuario: Calcula la volemia para un hombre de 75kg y 180cm")
print("🤖 Asistente: Calculando volumen sanguíneo con fórmula de Nadler...")
resultado = calcular_volemia_nadler(75, 180, "masculino")
print(f"   ✅ Resultado del cálculo:")
print(f"      • Volumen sanguíneo: {resultado['volumen_litros']} litros")
print(f"      • Equivalente: {resultado['volumen_ml']} mililitros")
print(f"      • Parámetros usados:")
print(f"        - Peso: {resultado['parametros']['peso_kg']} kg")
print(f"        - Altura: {resultado['parametros']['altura_cm']} cm")
print(f"        - Género: {resultado['parametros']['genero']}")
print("   ⚠️  AVISO MÉDICO: Esta es una estimación.")
print("   Consulte a un profesional de la salud para decisiones clínicas.")

# Simulación 4: Usuario pide tarjeta Mastercard
print("\n👤 Usuario: Ahora genera una Mastercard")
print("🤖 Asistente: Generando tarjeta Mastercard...")
tarjeta_mc = generar_tarjeta_prueba("mastercard")
print(f"   ✅ Tarjeta generada: {tarjeta_mc}")
print(f"   Verificación: Prefijo correcto ({'✓' if tarjeta_mc[0] == '5' else '✗'})")

# Simulación 5: Manejo de error
print("\n👤 Usuario: Genera una tarjeta American Express")
print("🤖 Asistente: Procesando solicitud...")
try:
    tarjeta_amex = generar_tarjeta_prueba("amex")
except ValueError as e:
    print(f"   ❌ Error: {e}")
    print("   💡 Sugerencia: Los tipos soportados son 'visa' y 'mastercard'")

print("\n" + "="*60)
print("✅ DEMOSTRACIÓN COMPLETADA")
print("="*60)
print("\n📚 Para usar el agente interactivamente, ejecuta:")
print("   python agent.py")
print("\n🧪 Para ejecutar las pruebas automatizadas:")
print("   python test_agent.py")
print()
