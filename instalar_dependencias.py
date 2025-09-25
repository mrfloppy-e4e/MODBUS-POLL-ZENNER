#!/usr/bin/env python3
"""
Script de instalación de dependencias para MODBUS TCP ZENNER
"""

import subprocess
import sys

def install_package(package):
    """Instala un paquete usando pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Instala todas las dependencias necesarias"""
    print("🔧 INSTALADOR DE DEPENDENCIAS - MODBUS TCP ZENNER")
    print("=" * 50)
    
    packages = [
        "pymodbus==2.5.3",
        "requests",
        "Pillow"  # PIL
    ]
    
    print("📦 Instalando dependencias necesarias...\n")
    
    for package in packages:
        print(f"📥 Instalando {package}...")
        if install_package(package):
            print(f"   ✅ {package} instalado correctamente")
        else:
            print(f"   ❌ Error instalando {package}")
        print()
    
    print("🎯 RESUMEN DE FUNCIONALIDADES:")
    print("-" * 30)
    print("✅ pymodbus==2.5.3: Comunicación Modbus TCP")
    print("✅ requests: Descarga de favicon y logo desde internet")
    print("✅ Pillow (PIL): Procesamiento de imágenes")
    print()
    print("🚀 Una vez instaladas las dependencias, ejecute:")
    print("   python modbus_gui.py")
    print()
    print("💡 CARACTERÍSTICAS DE LA APLICACIÓN:")
    print("   • Área de DEBUG ampliada para mejor visualización")
    print("   • Botón 'Acerca de' con información de contacto")
    print("   • Favicon de Zenner en la ventana")
    print("   • Logo de Zenner en el header de la aplicación")
    print("   • Detección automática de errores de formato")
    print("   • Ayuda contextual según función Modbus seleccionada")

if __name__ == "__main__":
    main()