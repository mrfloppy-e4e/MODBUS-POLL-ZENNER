# Modbus Poll - Zenner Tecnologías

## 🎯 Descripción
Aplicación para comunicación Modbus TCP diseñada especialmente para interactuar con todo tipo de esclavos modbus IP. Permite realizar operaciones de lectura y escritura con visualización completa de tramas y análisis detallado del protocolo.

<img width="1600" height="848" alt="image" src="https://github.com/user-attachments/assets/0cf1b153-1497-461f-87c5-96ee97ae0c2e" />


## ✨ Características Principales

### 🖥️ Interfaz Gráfica
- **Diseño dividido en dos paneles**: Configuración y visualización de resultados
- **Ventana maximizada automática** para mejor experiencia de usuario

### 📊 Funcionalidades Modbus
- **Soporte completo** para todas las funciones Modbus estándar:
  - FC01: Read Coils (Lectura de bobinas)
  - FC02: Read Discrete Inputs (Lectura de entradas discretas)
  - FC03: Read Holding Registers (Lectura de registros de retención)
  - FC04: Read Input Registers (Lectura de registros de entrada)
  - FC05: Write Single Coil (Escritura de bobina única)
  - FC06: Write Single Register (Escritura de registro único)
  - FC15: Write Multiple Coils (Escritura de bobinas múltiples)
  - FC16: Write Multiple Registers (Escritura de registros múltiples)

### 🔍 Visualización Avanzada de Tramas
- **Análisis completo TCP/IP**: Visualización del header Modbus TCP
  - Transaction ID, Protocol ID, Length, Unit ID
- **Desglose detallado del PDU**: Function Code, direcciones, datos
- **Formato hexadecimal y decimal** para todos los valores
- **Tramas de petición y respuesta** mostradas lado a lado
- **Timestamps** para todas las operaciones

### 🛠️ Sistema de Debug Inteligente
- **Detección automática de errores** comunes de configuración
- **Sugerencias específicas** para cada tipo de problema
- **Validación en tiempo real** de parámetros
- **Mensajes de éxito** con detalles de la operación

### 📈 Análisis de Datos
- **Tabla formateada** de registros con múltiples formatos:
  - Decimal, hexadecimal y binario
  - Direcciones mapeadas correctamente
- **Visualización de coils** en formato bit
- **Confirmación de escritura** para operaciones de modificación

## 🚀 Instalación Rápida

### Opción 1: Ejecutable (Windows)
Descargar ModbusPoll-Zenner-v2.exe y ejecutar.

### Opción 2: Desarrollo
```bash
# Clonar el repositorio
git clone https://github.com/mrfloppy-e4e/MODBUS-POLL-ZENNER.git

# Ir al directorio
cd "MODBUS POLL ZENNER"

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python modbus_gui.py
```

## 🎮 Uso de la Aplicación

### Panel de Configuración (Izquierda)
1. **Conexión TCP**:
   - IP del dispositivo
   - Puerto (por defecto: 502)
   - Unit ID del esclavo

2. **Operación Modbus**:
   - Seleccionar función deseada
   - Especificar dirección inicial
   - Configurar cantidad/valores según la operación

3. **Envío**:
   - Hacer clic en "📤 Enviar Trama"
   - Monitorear el estado de la conexión

### Panel de Resultados (Derecha)
- **Visualización de tramas**: Petición y respuesta completas
- **Datos procesados**: Tablas formateadas con valores
- **Debug inteligente**: Mensajes de error y sugerencias
- **Estado de conexión**: Indicadores visuales de éxito/error

### Área de Debug
- **Detección automática** de problemas comunes
- **Sugerencias específicas** para cada error
- **Botón "Acerca de"** con información del software

## 🔧 Tecnologías Utilizadas

- **Python 3.12**: Lenguaje base
- **tkinter**: Interfaz gráfica nativa
- **pymodbus 2.5.3**: Comunicación Modbus (versión compatible)
- **PIL/Pillow**: Procesamiento de imágenes
- **PyInstaller**: Generación de ejecutables
- **Threading**: Operaciones no bloqueantes

## 📂 Estructura del Proyecto

```
MODBUS POLL ZENNER/
├── modbus_gui.py              # Aplicación principal
├── modbus_zenner.py           # Versión CLI original
├── build_exe.py               # Script de construcción
├── requirements.txt           # Dependencias Python
├── img/                       # Recursos gráficos
│   ├── zenner-ico-sinfondo.ico
│   └── Zenner Tecnologia FONDOS CLAROS - chicos.png
├── dist/                      # Ejecutables generados
│   └── ModbusPoll-Zenner-v2.exe
├── docs/                      # Documentación completa
│   ├── README.md
│   ├── MANUAL_USUARIO.md
│   ├── DOCUMENTACION_TECNICA.md
│   └── CHANGELOG.md
└── venv/                      # Entorno virtual
```

## 🆕 Novedades en la Versión Actual

### ✅ Implementado
- ✅ **Visualización completa de tramas TCP y PDU**
- ✅ **Formato detallado de peticiones y respuestas**
- ✅ **Análisis hexadecimal de todos los campos**
- ✅ **Identificación de códigos de función**
- ✅ **Mapeo correcto de direcciones y datos**
- ✅ **Timestamps para todas las operaciones**
- ✅ **Debug inteligente con detección automática de errores**
- ✅ **Interfaz profesional con branding Zenner**
- ✅ **Ejecutable con todas las dependencias incluidas**

## 📊 Ejemplo de Uso

**Leer 5 registros holding desde dirección 40001:**
1. Conectar a dispositivo (IP: 192.168.1.100, Puerto: 502)
2. Seleccionar "3 - Read Holding Registers (FC03)"
3. Dirección: 40000 (40001-1, base 0)
4. Cantidad: 5
5. Enviar trama
6. Ver análisis completo de tramas TCP/PDU
7. Revisar tabla formateada con valores en decimal/hex/binario

## 🛡️ Compatibilidad

- **Sistemas Operativos**: Windows 10/11 (ejecutable), multiplataforma (código fuente)
- **Python**: 3.8 o superior
- **Modbus**: TCP/IP estándar
- **Dispositivos**: Compatible con cualquier dispositivo Modbus TCP

## 🤝 Soporte

Para soporte técnico o reportar problemas:
1. Revisar la documentación técnica completa
2. Verificar logs de debug en la aplicación
3. Consultar el manual de usuario
4. Contactar al equipo de desarrollo

## 📄 Licencia

Este proyecto está desarrollado para Zenner Technology como herramienta interna de diagnóstico y comunicación Modbus.

---
**Desarrollado con ❤️ para Zenner Technologias por Eric Azua Gargurevich (a.k.a. mrfloppy)**  
**https://eazua.com**  
**https://www.zenner.cl**  
*Versión: 2.0 con visualización completa de tramas Modbus TCP/PDU*
