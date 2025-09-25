# 📋 CHANGELOG - MODBUS TCP POLL ZENNER

Registro de todas las versiones y cambios del proyecto.

## [2.2.0] - 2025-09-25 🚀 NUEVA VERSIÓN MAYOR

### ✅ Agregado - VISUALIZACIÓN COMPLETA DE TRAMAS
- **🔍 Análisis detallado de tramas Modbus TCP**
  - Visualización completa del header TCP (Transaction ID, Protocol ID, Length, Unit ID)
  - Desglose detallado del PDU (Protocol Data Unit)
  - Formato hexadecimal para todos los campos de la trama
  - Identificación automática de códigos de función con nombres descriptivos
  
- **📊 Formateo avanzado de datos**
  - Tramas de petición (REQUEST) mostradas con sintaxis completa
  - Tramas de respuesta (RESPONSE) con análisis detallado
  - Mapeo correcto de direcciones y datos en formato hex/decimal
  - Timestamps para todas las operaciones de comunicación

- **🎨 Mejoras visuales en la interfaz**
  - Panel de resultados reorganizado con secciones claras
  - Separadores visuales entre trama enviada y recibida
  - Códigos de color mejorados para diferentes tipos de información
  - Limpieza automática del log anterior en cada operación

- **🔧 Funciones técnicas nuevas**
  - `format_modbus_tcp_frame()`: Formatea headers TCP completos
  - `format_modbus_pdu()`: Analiza Protocol Data Units
  - `format_modbus_request()`: Construye tramas de petición
  - `format_modbus_response()`: Procesa tramas de respuesta
  - `get_function_name()`: Traduce códigos de función a nombres

### 🔧 Mejorado
- **📈 Análisis de datos más robusto**
  - Detección inteligente del tipo de operación para formateo correcto
  - Manejo mejorado de valores múltiples en escrituras
  - Validación de datos de entrada más estricta
  - Mejor manejo de errores en la construcción de tramas

- **🖥️ Experiencia de usuario mejorada**
  - Información más clara y estructurada en el panel de resultados
  - Mejor separación visual entre datos de configuración y resultados
  - Indicadores de estado más precisos y descriptivos

### 🐛 Corregido
- Compatibilidad mejorada con diferentes tipos de respuestas Modbus
- Manejo correcto de tramas de error con códigos de excepción
- Validación mejorada de parámetros de entrada
- Estabilidad aumentada en operaciones de escritura múltiple

## [2.1.1] - 2025-09-25

### 🔧 Cambiado
- **Downgrade de pymodbus a versión 2.5.3**
  - Actualizado import: `from pymodbus.client.sync import ModbusTcpClient`
  - Mejorada verificación de errores para compatibilidad
  - Actualizada documentación técnica
  - Compatible con sistemas más antiguos

### ✅ Agregado
- **Sistema de debug inteligente expandido**
  - Área de debug más grande y visible
  - Detección automática de errores comunes
  - Sugerencias específicas para cada tipo de problema
  - Botón "Acerca de" con información del software

- **🎨 Branding Zenner completo**
  - Logo Zenner Technology integrado en la interfaz
  - Favicon personalizado (zenner-ico-sinfondo.ico)
  - Ventana maximizada al inicio para mejor visualización
  - Posicionamiento perfecto del logo en esquina superior derecha

- **📦 Mejoras en el ejecutable**
  - Script build_exe.py actualizado para incluir imágenes
  - Empaquetado correcto de recursos gráficos
  - Ejecutable ModbusPoll-Zenner-v2.exe con todos los assets

- **Script de verificación de compatibilidad**
  - verificar_compatibilidad.py para probar la instalación
  - Verificación automática de métodos y versión
  - Guía de diferencias entre versiones

### 🐛 Corregido
- Compatibilidad con entornos que requieren pymodbus 2.5.3
- Importaciones corregidas para mayor estabilidad
- Verificación de errores más robusta
- Carga correcta de imágenes en el ejecutable

## [2.1.0] - 2025-09-23

### ✅ Agregado
- **Documentación completa del proyecto**
  - README.md con descripción general y guía de instalación
  - MANUAL_USUARIO.md con instrucciones detalladas de uso
  - DOCUMENTACION_TECNICA.md con arquitectura y detalles técnicos
  - CHANGELOG.md con historial de versiones

### 🔧 Mejorado
- Organización de archivos del proyecto
- Estructura de carpetas más clara
- Comentarios en código fuente

## [2.0.0] - 2025-09-23

### ✅ Agregado
- **Interfaz gráfica completa (GUI)**
  - Panel izquierdo para configuración de tramas
  - Panel derecho para visualización de respuestas
  - Interfaz dividida en dos columnas como se solicitó
  
- **Funcionalidades GUI avanzadas**
  - Vista previa de trama en tiempo real
  - Respuestas formateadas en múltiples formatos (decimal, hex, binario)
  - Logs con timestamps y códigos de color
  - Tabla detallada de registros leídos
  
- **Soporte completo de funciones Modbus**
  - FC01: Read Coils
  - FC02: Read Discrete Inputs  
  - FC03: Read Holding Registers
  - FC04: Read Input Registers
  - FC05: Write Single Coil
  - FC06: Write Single Register
  - FC15: Write Multiple Coils
  - FC16: Write Multiple Registers

- **Características técnicas**
  - Threading para operaciones no bloqueantes
  - Manejo robusto de errores
  - Validación de entradas del usuario
  - Conexión/desconexión dinámica

- **Ejecutable Windows (.exe)**
  - Script automatizado para crear ejecutable
  - Aplicación standalone sin dependencias
  - Listo para distribución

### 🔧 Mejorado
- Arquitectura modular y extensible
- Interfaz de usuario intuitiva
- Mensajes de error descriptivos
- Performance y estabilidad

## [1.0.0] - 2025-09-23 (Versión inicial)

### ✅ Agregado
- **Versión CLI (línea de comandos)**
  - Script interactivo básico
  - Configuración manual de parámetros
  - Soporte para funciones Modbus principales
  - Menú de selección de funciones

- **Funcionalidades básicas**
  - Conexión Modbus TCP
  - Lectura de holding registers
  - Configuración de IP, puerto y Unit ID
  - Manejo básico de errores

### 📁 Archivos incluidos
- `modbus_zenner.py` - Script CLI principal
- `requirements.txt` - Dependencias del proyecto
  - Tabla detallada de registros leídos
  
- **Soporte completo de funciones Modbus**
  - FC01: Read Coils
  - FC02: Read Discrete Inputs  
  - FC03: Read Holding Registers
  - FC04: Read Input Registers
  - FC05: Write Single Coil
  - FC06: Write Single Register
  - FC15: Write Multiple Coils
  - FC16: Write Multiple Registers

- **Características técnicas**
  - Threading para operaciones no bloqueantes
  - Manejo robusto de errores
  - Validación de entradas del usuario
  - Conexión/desconexión dinámica

- **Ejecutable Windows (.exe)**
  - Script automatizado para crear ejecutable
  - Aplicación standalone sin dependencias
  - Listo para distribución

### 🔧 Mejorado
- Arquitectura modular y extensible
- Interfaz de usuario intuitiva
- Mensajes de error descriptivos
- Performance y estabilidad

## [1.0.0] - 2025-09-23 (Versión inicial)

### ✅ Agregado
- **Versión CLI (línea de comandos)**
  - Script interactivo básico
  - Configuración manual de parámetros
  - Soporte para funciones Modbus principales
  - Menú de selección de funciones

- **Funcionalidades básicas**
  - Conexión Modbus TCP
  - Lectura de holding registers
  - Configuración de IP, puerto y Unit ID
  - Manejo básico de errores

### 📁 Archivos incluidos
- `modbus_zenner.py` - Script CLI principal
- `requirements.txt` - Dependencias del proyecto

---

## 🔮 Roadmap Futuro

### [3.0.0] - Planificado
- **Nuevas funcionalidades**
  - Soporte Modbus RTU (puerto serie)
  - Perfiles de configuración guardados
  - Modo de monitoreo continuo
  - Exportación de datos a CSV/Excel
  - Gráficos en tiempo real

- **Mejoras técnicas**
  - Base de datos para historial
  - API REST para integración
  - Scripting automatizado
  - Soporte multi-idioma

### [2.2.0] - Próxima versión menor
- **Mejoras de usabilidad**
  - Configuraciones favoritas
  - Atajos de teclado
  - Modo oscuro/claro
  - Ayuda contextual

- **Optimizaciones**
  - Mejor manejo de timeouts
  - Cache de conexiones
  - Logs más detallados
  - Diagnósticos de red

---

## 📊 Estadísticas de Desarrollo

### Líneas de Código
- **v1.0.0:** ~150 líneas (CLI básico)
- **v2.0.0:** ~450 líneas (GUI completa)
- **v2.1.0:** ~500 líneas (con documentación)

### Archivos del Proyecto
- **v1.0.0:** 2 archivos
- **v2.0.0:** 5 archivos + ejecutable
- **v2.1.0:** 8 archivos + documentación completa

### Funcionalidades
- **v1.0.0:** 4 funciones Modbus básicas
- **v2.0.0:** 8 funciones Modbus completas + GUI
- **v2.1.0:** Mismas funciones + documentación

---

## 🏷️ Convenciones de Versionado

Este proyecto sigue [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (X.Y.Z)
- **MAJOR:** Cambios incompatibles en la API
- **MINOR:** Nuevas funcionalidades compatibles hacia atrás
- **PATCH:** Correcciones de bugs compatibles

### Tipos de Cambios
- ✅ **Agregado:** Nuevas funcionalidades
- 🔧 **Mejorado:** Mejoras en funcionalidades existentes
- 🐛 **Corregido:** Corrección de bugs
- ⚠️ **Deprecated:** Funcionalidades que serán removidas
- ❌ **Removido:** Funcionalidades eliminadas
- 🔒 **Seguridad:** Vulnerabilidades corregidas

---
*Changelog mantenido según [Keep a Changelog](https://keepachangelog.com/)*