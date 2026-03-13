#!/usr/bin/env python3
"""
Script de prueba para verificar que el agente funciona correctamente
"""

from tools import generar_tarjeta_prueba, generar_password_seguro, calcular_volemia_nadler

print("="*60)
print("🧪 PRUEBA DE HERRAMIENTAS DEL AGENTE")
print("="*60)

# Prueba 1: Generar tarjeta Visa
print("\n1️⃣ Generando tarjeta Visa...")
try:
    tarjeta_visa = generar_tarjeta_prueba("visa")
    print(f"   ✅ Tarjeta Visa: {tarjeta_visa}")
    print(f"   Longitud: {len(tarjeta_visa)} dígitos")
    print(f"   Prefijo correcto: {'✅' if tarjeta_visa[0] == '4' else '❌'}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Prueba 2: Generar tarjeta Mastercard
print("\n2️⃣ Generando tarjeta Mastercard...")
try:
    tarjeta_mc = generar_tarjeta_prueba("mastercard")
    print(f"   ✅ Tarjeta Mastercard: {tarjeta_mc}")
    print(f"   Longitud: {len(tarjeta_mc)} dígitos")
    print(f"   Prefijo correcto: {'✅' if tarjeta_mc[0] == '5' else '❌'}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Prueba 3: Generar contraseña segura
print("\n3️⃣ Generando contraseña segura de 16 caracteres...")
try:
    password = generar_password_seguro(16)
    print(f"   ✅ Contraseña: {password}")
    print(f"   Longitud: {len(password)} caracteres")
    print(f"   Tiene mayúsculas: {'✅' if any(c.isupper() for c in password) else '❌'}")
    print(f"   Tiene minúsculas: {'✅' if any(c.islower() for c in password) else '❌'}")
    print(f"   Tiene dígitos: {'✅' if any(c.isdigit() for c in password) else '❌'}")
    print(f"   Tiene símbolos: {'✅' if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password) else '❌'}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Prueba 4: Calcular volemia para hombre
print("\n4️⃣ Calculando volemia para hombre (70kg, 175cm)...")
try:
    resultado = calcular_volemia_nadler(70, 175, "masculino")
    print(f"   ✅ Volumen: {resultado['volumen_litros']} litros")
    print(f"   En mililitros: {resultado['volumen_ml']} ml")
    print(f"   Parámetros: {resultado['parametros']}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Prueba 5: Calcular volemia para mujer
print("\n5️⃣ Calculando volemia para mujer (60kg, 165cm)...")
try:
    resultado = calcular_volemia_nadler(60, 165, "femenino")
    print(f"   ✅ Volumen: {resultado['volumen_litros']} litros")
    print(f"   En mililitros: {resultado['volumen_ml']} ml")
    print(f"   Parámetros: {resultado['parametros']}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Prueba 6: Validación de errores
print("\n6️⃣ Probando validación de errores...")
try:
    generar_tarjeta_prueba("amex")
    print("   ❌ No detectó tipo inválido")
except ValueError as e:
    print(f"   ✅ Error detectado correctamente: {e}")

try:
    generar_password_seguro(5)
    print("   ❌ No detectó longitud inválida")
except ValueError as e:
    print(f"   ✅ Error detectado correctamente: {e}")

try:
    calcular_volemia_nadler(10, 175, "masculino")
    print("   ❌ No detectó peso inválido")
except ValueError as e:
    print(f"   ✅ Error detectado correctamente: {e}")

print("\n" + "="*60)
print("✅ TODAS LAS PRUEBAS COMPLETADAS")
print("="*60)
