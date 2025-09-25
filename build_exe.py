# Script para crear ejecutable (.exe) de la aplicación Modbus GUI
# Requiere PyInstaller: pip install pyinstaller

# Comando para crear el .exe:
# pyinstaller --onefile --windowed --name "ModbusPoll-Zenner" --icon=icon.ico modbus_gui.py

# Comando alternativo (sin icono):
# pyinstaller --onefile --windowed --name "ModbusPoll-Zenner" modbus_gui.py

# Opciones explicadas:
# --onefile: Crea un solo archivo ejecutable
# --windowed: No muestra consola (solo ventana GUI)
# --name: Nombre del ejecutable
# --icon: Archivo de icono (opcional)

# Para ejecutar este script:
# python build_exe.py

import subprocess
import sys
import os

def build_exe():
    """Construye el archivo ejecutable"""
    
    print("🔨 Construyendo ejecutable de Modbus Poll - Zenner...")
    print("📦 Usando pymodbus v2.5.3 para mayor compatibilidad...")
    
    # Verificar que PyInstaller esté instalado
    try:
        import PyInstaller
    except ImportError:
        print("❌ PyInstaller no está instalado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller instalado correctamente")
    
    # Comando para crear el ejecutable
    cmd = [
        "pyinstaller",
        "--onefile",           # Un solo archivo
        "--windowed",          # Sin consola
        "--name", "ModbusPoll-Zenner-v2",  # Nombre del exe
        "--add-data", "img;img",  # Incluir carpeta de imágenes
        "modbus_gui.py"        # Archivo principal
    ]
    
    # Verificar que las imágenes existan
    img_files = [
        "img/zenner-ico-sinfondo.ico",
        "img/Zenner Tecnologia FONDOS CLAROS - chicos.png"
    ]
    
    images_ok = True
    for img_file in img_files:
        if os.path.exists(img_file):
            print(f"✅ Imagen encontrada: {img_file}")
        else:
            print(f"❌ Imagen no encontrada: {img_file}")
            images_ok = False
    
    if not images_ok:
        print("⚠️ ADVERTENCIA: Algunas imágenes no se encontraron. El .exe funcionará pero sin logos.")
    
    # Si existe el favicon como icono del ejecutable, agregarlo
    favicon_path = "img/zenner-ico-sinfondo.ico"
    if os.path.exists(favicon_path):
        cmd.extend(["--icon", favicon_path])
        print(f"🎨 Usando favicon como icono del ejecutable: {favicon_path}")
    elif os.path.exists("icon.ico"):
        cmd.extend(["--icon", "icon.ico"])
        print("🎨 Icono alternativo encontrado, será incluido en el ejecutable")
    
    try:
        print("⚙️ Ejecutando PyInstaller...")
        print(" ".join(cmd))
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Ejecutable creado exitosamente!")
            print("📁 Ubicación: dist/ModbusPoll-Zenner-v2.exe")
            print("💡 El archivo .exe está listo para distribuir")
        else:
            print("❌ Error al crear el ejecutable:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    build_exe()