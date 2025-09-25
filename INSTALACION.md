# 🚀 GUÍA DE INSTALACIÓN Y DISTRIBUCIÓN

## 📦 Opciones de Instalación

### Opción 1: Ejecutable Windows (Recomendado para usuarios finales)

**Ventajas:**
- ✅ No requiere Python instalado
- ✅ Funciona en cualquier Windows
- ✅ Un solo archivo ejecutable
- ✅ Instalación inmediata

**Pasos:**
1. Descargar `ModbusPoll-Zenner.exe` de la carpeta `dist/`
2. Ejecutar directamente haciendo doble clic
3. ¡Listo para usar!

### Opción 2: Desde Código Fuente (Para desarrolladores)

**Requisitos:**
- Python 3.8 o superior
- pip (gestor de paquetes Python)

**Pasos:**
```bash
# 1. Descargar el proyecto
git clone [URL_DEL_REPOSITORIO]
cd "MODBUS POLL ZENNER"

# 2. Crear entorno virtual (recomendado)
python -m venv venv
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar aplicación
python modbus_gui.py
```

## 🔧 Construcción del Ejecutable

### Para desarrolladores que quieran crear su propio .exe:

**Requisitos adicionales:**
```bash
pip install pyinstaller
```

**Método 1: Script automatizado**
```bash
python build_exe.py
```

**Método 2: Manual**
```bash
pyinstaller --onefile --windowed --name "ModbusPoll-Zenner" modbus_gui.py
```

**Parámetros explicados:**
- `--onefile`: Crea un solo archivo ejecutable
- `--windowed`: No muestra consola de comandos
- `--name`: Nombre del archivo ejecutable
- `--icon`: Archivo de icono (opcional)

## 📁 Estructura de Distribución

```
ModbusPoll-Zenner-v2.1.0/
├── 📱 EJECUTABLE/
│   └── ModbusPoll-Zenner.exe     # Aplicación lista para usar
├── 📝 DOCUMENTACION/
│   ├── README.md                 # Descripción general
│   ├── MANUAL_USUARIO.md         # Manual de uso
│   ├── DOCUMENTACION_TECNICA.md  # Detalles técnicos
│   └── CHANGELOG.md              # Historial de versiones
├── 💾 CODIGO_FUENTE/
│   ├── modbus_gui.py            # Aplicación GUI principal
│   ├── modbus_zenner.py         # Versión CLI
│   ├── build_exe.py             # Script de construcción
│   └── requirements.txt         # Dependencias
└── 📋 INSTALACION.md            # Este archivo
```

## 🔄 Actualización

### Desde Ejecutable
1. Descargar nueva versión del ejecutable
2. Reemplazar archivo anterior
3. Ejecutar nueva versión

### Desde Código Fuente
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## 🔧 Configuración del Sistema

### Firewall Windows
Si hay problemas de conexión, configurar firewall:

1. **Windows Defender Firewall:**
   - Permitir aplicación a través del firewall
   - Agregar `ModbusPoll-Zenner.exe` a excepciones

2. **Puertos necesarios:**
   - **Saliente:** Puerto 502 (TCP) - Modbus TCP estándar
   - **Entrada:** No se requieren puertos de entrada

### Antivirus
Algunos antivirus pueden detectar falsos positivos:

1. **Solución:**
   - Agregar `ModbusPoll-Zenner.exe` a exclusiones
   - O descargar desde fuente confiable

2. **Verificación:**
   - Ejecutable es creado con PyInstaller (herramienta legítima)
   - Código fuente disponible para inspección

## 🌐 Requisitos de Red

### Conectividad
- **Protocolo:** TCP/IP
- **Puerto:** 502 (configurable)
- **Latencia:** < 1000ms recomendado
- **Ancho de banda:** Mínimo (< 1 KB/s)

### Pruebas de Conectividad
```bash
# Verificar conectividad básica
ping 192.168.1.100

# Verificar puerto específico (requiere telnet)
telnet 192.168.1.100 502

# Con PowerShell (Windows 10/11)
Test-NetConnection -ComputerName 192.168.1.100 -Port 502
```

## 🐛 Solución de Problemas Comunes

### Problema: "No se puede ejecutar el archivo .exe"
**Soluciones:**
1. Ejecutar como administrador
2. Verificar arquitectura (32-bit vs 64-bit)
3. Instalar Microsoft Visual C++ Redistributable
4. Verificar que Windows no esté bloqueando el archivo

### Problema: "Error al importar pymodbus"
**Causa:** Instalación desde código fuente sin dependencias
**Solución:**
```bash
**Desde Código Fuente**
```bash
pip install pymodbus==2.5.3
```

### Problema: "Conexión rechazada"
**Verificaciones:**
1. IP correcta del dispositivo
2. Puerto 502 abierto
3. Dispositivo encendido y accesible
4. Firewall no bloqueando conexión

## 📊 Compatibilidad

### Sistemas Operativos Soportados
- ✅ **Windows 10** (32-bit y 64-bit)
- ✅ **Windows 11** (64-bit)
- ✅ **Windows Server 2016+**
- ⚠️ **Windows 7/8:** Puede funcionar pero no probado oficialmente

### Versiones Python (para código fuente)
- ✅ **Python 3.8**
- ✅ **Python 3.9**
- ✅ **Python 3.10**
- ✅ **Python 3.11**
- ✅ **Python 3.12**

### Dispositivos Modbus Compatibles
- ✅ **Medidores Zenner** (objetivo principal)
- ✅ **Cualquier dispositivo Modbus TCP estándar**
- ✅ **Simuladores Modbus**
- ✅ **PLCs con soporte Modbus TCP**

## 🔐 Consideraciones de Seguridad

### Red
- Usar VPN para conexiones remotas
- Segmentar red industrial
- Monitorear tráfico Modbus

### Aplicación
- No almacena credenciales
- Conexiones directas TCP (sin autenticación Modbus)
- Logs locales únicamente

## 📞 Soporte Técnico

### Información para Reportar Problemas
1. **Versión de la aplicación**
2. **Sistema operativo**
3. **Descripción del problema**
4. **Pasos para reproducir**
5. **Logs de error (si los hay)**

### Logs y Diagnósticos
Los logs se muestran en la interfaz pero también se pueden capturar:
- Pantalla de respuestas en la aplicación
- Screenshots de errores
- Configuración de red utilizada

---
*Guía de Instalación v2.1.0 - MODBUS TCP POLL ZENNER*