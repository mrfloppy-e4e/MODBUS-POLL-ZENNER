# 📖 MANUAL DE USUARIO - MODBUS TCP POLL ZENNER

## 🎯 Introducción

Esta aplicación permite comunicarse con dispositivos Modbus TCP (como medidores Zenner) para leer y escribir datos de forma sencilla e intuitiva. La nueva versión incluye **visualización completa de tramas** con análisis detallado del protocolo TCP y PDU.

## ✨ Características Principales

### � Visualización Completa de Tramas
- **Header Modbus TCP**: Transaction ID, Protocol ID, Length, Unit ID
- **PDU (Protocol Data Unit)**: Function Code, direcciones, datos
- **Formato hexadecimal**: Para análisis técnico detallado
- **Tramas de petición y respuesta**: Mostradas lado a lado
- **Timestamps**: Para seguimiento temporal de operaciones

### 🛠️ Debug Inteligente
- **Detección automática de errores** comunes
- **Sugerencias específicas** para cada problema
- **Área expandida** para mejor visibilidad
- **Validación en tiempo real** de parámetros

## �🖥️ Interfaz de Usuario

### Panel Izquierdo: Configuración y Envío
```
┌─────────────────────────────────────┐
│  📤 CONFIGURACIÓN Y ENVÍO DE TRAMA  │
├─────────────────────────────────────┤
│  Conexión                           │
│  IP: [192.168.1.100] Puerto: [502] │
│  Unit ID: [1]    [Conectar]        │
│  ● Desconectado                     │
├─────────────────────────────────────┤
│  Función Modbus                     │
│  [3 - Leer Holding Registers▼]     │
├─────────────────────────────────────┤
│  Parámetros                         │
│  Dirección: [0]                     │
│  Cantidad: [1]                      │
├─────────────────────────────────────┤
│  Trama a Enviar                     │
│  Función: 3 (Read Holding Regs)    │
│  Unit ID: 1                         │
│  Dirección: 0                       │
│  Cantidad: 1                        │
├─────────────────────────────────────┤
│  [📤 Enviar Trama] [🗑️ Limpiar]    │
└─────────────────────────────────────┘
```

### Panel Derecho: Respuestas y Análisis de Tramas
```
┌─────────────────────────────────────┐
│  📥 DATOS RECIBIDOS                 │
├─────────────────────────────────────┤
│  [14:30:25] 🔄 OPERACIÓN MODBUS     │
│  Descripción: Read Holding Regs...  │
│                                     │
│  📤 TRAMA ENVIADA (REQUEST):        │
│  ────────────────────────────────   │
│  🌐 MODBUS TCP HEADER:              │
│  Transaction ID: 0001 (1)           │
│  Protocol ID: 0000 (0)              │
│  Length: 0006 (6)                   │
│  Unit ID: 01 (1)                    │
│                                     │
│  📦 MODBUS PDU:                     │
│  Function Code: 03 (3) - Read Hold. │
│  Data: 00 00 00 01                  │
│    - Dirección inicial: 0 (0x0000)  │
│    - Cantidad: 1                    │
│                                     │
│  📥 TRAMA RECIBIDA (RESPONSE):      │
│  ────────────────────────────────   │
│  🌐 MODBUS TCP HEADER:              │
│  Transaction ID: 0001 (1)           │
│  Protocol ID: 0000 (0)              │
│  Length: 0005 (5)                   │
│  Unit ID: 01 (1)                    │
│                                     │
│  📦 MODBUS PDU:                     │
│  Function Code: 03 (3) - Read Hold. │
│  Data: 02 04 D2                     │
│    - Bytes de datos: 2              │
│    - Registros: [1234]              │
│                                     │
│  ✅ DATOS PROCESADOS:               │
│  ──────────────────────────────     │
│  Registros (decimal): [1234]        │
│  Registros (hex): [0x04D2]          │
│                                     │
│  📊 TABLA DE REGISTROS:             │
│  ────────────────────────────────   │
│  Addr     Decimal   Hex      Binary │
│  ────────────────────────────────   │
│  0        1234      0x04D2   0001... │
└─────────────────────────────────────┘
```

### Área de Debug (Parte Inferior)
```
┌─────────────────────────────────────┐
│  🔍 DEBUG Y DIAGNÓSTICOS            │
├─────────────────────────────────────┤
│  ✅ Conexión establecida            │
│  ✅ Parámetros validados            │
│  ✅ Respuesta recibida exitosamente │
│  ℹ️ Trama procesada correctamente    │
├─────────────────────────────────────┤
│  [ℹ️ Acerca de]                     │
└─────────────────────────────────────┘
```
│  Addr    Decimal   Hex     Binary   │
│  ---------------------------------- │
│  0       1234      0x04D2  xxxxxxxx │
│  1       5678      0x162E  xxxxxxxx │
└─────────────────────────────────────┘
```

## 🔧 Guía Paso a Paso

### 1. Conexión Inicial

1. **Configurar IP del dispositivo:**
   - Ingresar la dirección IP del medidor Zenner
   - Ejemplo: `192.168.1.100`

2. **Configurar Puerto:**
   - Puerto estándar Modbus TCP: `502`
   - Cambiar solo si el dispositivo usa puerto diferente

3. **Configurar Unit ID:**
   - Identificador del dispositivo esclavo
   - Generalmente: `1`
   - Consultar manual del dispositivo si es diferente

4. **Hacer clic en "Conectar":**
   - El estado cambiará a "● Conectado" en verde
   - Si hay error, se mostrará en rojo

### 2. Selección de Función Modbus

**Funciones de Lectura (más comunes):**
- **FC01 - Leer Coils:** Estados binarios (ON/OFF)
- **FC02 - Leer Discrete Inputs:** Entradas digitales
- **FC03 - Leer Holding Registers:** Datos principales (valores de medición)
- **FC04 - Leer Input Registers:** Datos de solo lectura

**Funciones de Escritura:**
- **FC05 - Escribir Single Coil:** Cambiar un estado binario
- **FC06 - Escribir Single Register:** Cambiar un valor
- **FC15 - Escribir Multiple Coils:** Cambiar varios estados
- **FC16 - Escribir Multiple Registers:** Cambiar varios valores

### 3. Configuración de Parámetros

**Para Funciones de Lectura:**
- **Dirección:** Registro inicial a leer
- **Cantidad:** Número de registros/coils consecutivos

**Para Funciones de Escritura:**
- **Dirección:** Registro/coil a modificar
- **Valores:** Datos a escribir (separados por comas para múltiples)

### 4. Envío y Interpretación

1. **Verificar trama:** El panel muestra la configuración actual
2. **Hacer clic "Enviar Trama"**
3. **Interpretar respuesta en panel derecho:**
   - ✅ Verde: Operación exitosa
   - ❌ Rojo: Error en la operación
   - 📊 Datos formateados en múltiples formatos

## 📋 Casos de Uso Comunes

### Caso 1: Leer Consumo de Agua (Típico Zenner)
```
Función: 3 - Leer Holding Registers
Dirección: 0 (o según manual del medidor)
Cantidad: 2 (lectura de 32 bits = 2 registros)
```

### Caso 2: Leer Estado de Alarmas
```
Función: 1 - Leer Coils
Dirección: 0
Cantidad: 8 (8 alarmas diferentes)
```

### Caso 3: Configurar Parámetro del Medidor
```
Función: 6 - Escribir Single Register
Dirección: 100 (ejemplo)
Valores: 1500 (valor a configurar)
```

### Caso 4: Leer Múltiples Parámetros
```
Función: 3 - Leer Holding Registers
Dirección: 0
Cantidad: 10 (leer 10 registros consecutivos)
```

## 🔍 Interpretación de Respuestas

### Registros (16 bits cada uno)
- **Decimal:** Valor directo (ej: 1234)
- **Hexadecimal:** Representación hex (ej: 0x04D2)
- **Binario:** Para análisis bit a bit

### Valores de 32 bits
Los medidores a menudo usan 2 registros para un valor:
```
Registro 0: 0x1234 (parte alta)
Registro 1: 0x5678 (parte baja)
Valor completo: 0x12345678
```

### Estados Binarios (Coils)
- `True/1`: Estado activo/ON
- `False/0`: Estado inactivo/OFF

## ⚠️ Solución de Problemas

### Error de Conexión
**Síntoma:** "❌ No se pudo conectar"
**Soluciones:**
1. Verificar que el dispositivo esté encendido
2. Comprobar conectividad de red (`ping IP_dispositivo`)
3. Verificar que el puerto 502 esté abierto
4. Confirmar la dirección IP correcta

### Error en Respuesta
**Síntoma:** "❌ Error en respuesta"
**Soluciones:**
1. Verificar que la dirección de registro existe
2. Confirmar el Unit ID correcto
3. Algunos registros pueden ser de solo lectura

### Sin Respuesta
**Síntoma:** "❌ Sin respuesta"
**Soluciones:**
1. Verificar timeout de red
2. El dispositivo puede estar ocupado
3. Reintentar la operación

### Valores Inesperados
**Soluciones:**
1. Consultar manual del medidor para mapeo de registros
2. Verificar factor de escala (algunos valores requieren división)
3. Confirmar orden de bytes (big-endian vs little-endian)

## 📊 Consejos de Uso

### Optimización
- **Leer múltiples registros:** Más eficiente que lecturas individuales
- **Usar FC03 para datos principales:** Más rápido que FC04
- **Limitar cantidad de registros:** Evitar timeouts con lecturas muy grandes

### Monitoreo Continuo
- **Intervalo recomendado:** No menos de 1 segundo entre lecturas
- **Uso de scripts:** Para automatización, usar la versión CLI

### Documentación
- **Guardar configuraciones exitosas:** Anotar direcciones útiles
- **Mapeo de registros:** Crear tabla con significado de cada dirección

## 🔄 Mantenimiento

### Logs de Actividad
La aplicación muestra logs detallados con:
- Timestamp de cada operación
- Estado de conexión
- Respuestas recibidas
- Errores específicos

### Backup de Configuraciones
Anotar configuraciones exitosas:
```
Dispositivo: Zenner XYZ
IP: 192.168.1.100
Puerto: 502
Unit ID: 1
Registros útiles:
- 0-1: Consumo total (32 bits)
- 10: Estado de batería
- 20-25: Datos de flujo
```

---
*Manual de Usuario v2.0 - MODBUS TCP POLL ZENNER*