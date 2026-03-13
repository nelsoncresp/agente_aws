"""
Configuración de pytest para las pruebas del agente
"""
import pytest
from hypothesis import settings, Verbosity

# Configurar Hypothesis para ejecutar mínimo 100 iteraciones por propiedad
settings.register_profile("default", max_examples=100)
settings.load_profile("default")
