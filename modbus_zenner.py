from pymodbus.client.sync import ModbusTcpClient

def obtener_configuracion_conexion():
    """Obtiene la configuración de conexión del usuario"""
    print("=== CONFIGURACIÓN DE CONEXIÓN MODBUS TCP ===")
    
    host = input("Ingrese la dirección IP del dispositivo [192.168.1.100]: ").strip()
    if not host:
        host = "192.168.1.100"
    
    puerto_str = input("Ingrese el puerto [502]: ").strip()
    if not puerto_str:
        puerto = 502
    else:
        try:
            puerto = int(puerto_str)
        except ValueError:
            print("Puerto inválido, usando 502 por defecto")
            puerto = 502
    
    unit_str = input("Ingrese el Unit ID del dispositivo [1]: ").strip()
    if not unit_str:
        unit_id = 1
    else:
        try:
            unit_id = int(unit_str)
        except ValueError:
            print("Unit ID inválido, usando 1 por defecto")
            unit_id = 1
    
    return host, puerto, unit_id

def mostrar_menu_funciones():
    """Muestra el menú de funciones Modbus disponibles"""
    print("\n=== FUNCIONES MODBUS DISPONIBLES ===")
    print("1. Leer Coils (FC01)")
    print("2. Leer Discrete Inputs (FC02)")
    print("3. Leer Holding Registers (FC03)")
    print("4. Leer Input Registers (FC04)")
    print("5. Escribir Single Coil (FC05)")
    print("6. Escribir Single Register (FC06)")
    print("7. Escribir Multiple Coils (FC15)")
    print("8. Escribir Multiple Registers (FC16)")

def obtener_parametros_lectura():
    """Obtiene los parámetros para operaciones de lectura"""
    address_str = input("Ingrese la dirección inicial [0]: ").strip()
    if not address_str:
        address = 0
    else:
        try:
            address = int(address_str)
        except ValueError:
            print("Dirección inválida, usando 0 por defecto")
            address = 0
    
    count_str = input("Ingrese la cantidad de registros/coils a leer [1]: ").strip()
    if not count_str:
        count = 1
    else:
        try:
            count = int(count_str)
        except ValueError:
            print("Cantidad inválida, usando 1 por defecto")
            count = 1
    
    return address, count

def obtener_parametros_escritura_simple():
    """Obtiene los parámetros para escritura simple"""
    address_str = input("Ingrese la dirección del registro/coil [0]: ").strip()
    if not address_str:
        address = 0
    else:
        try:
            address = int(address_str)
        except ValueError:
            print("Dirección inválida, usando 0 por defecto")
            address = 0
    
    value_str = input("Ingrese el valor a escribir: ").strip()
    try:
        value = int(value_str)
    except ValueError:
        print("Valor inválido")
        return None, None
    
    return address, value

def obtener_parametros_escritura_multiple():
    """Obtiene los parámetros para escritura múltiple"""
    address_str = input("Ingrese la dirección inicial [0]: ").strip()
    if not address_str:
        address = 0
    else:
        try:
            address = int(address_str)
        except ValueError:
            print("Dirección inválida, usando 0 por defecto")
            address = 0
    
    values_str = input("Ingrese los valores separados por comas (ej: 1,2,3): ").strip()
    try:
        values = [int(v.strip()) for v in values_str.split(',')]
    except ValueError:
        print("Valores inválidos")
        return None, None
    
    return address, values

def ejecutar_operacion_modbus(client, funcion, unit_id):
    """Ejecuta la operación Modbus seleccionada"""
    response = None
    
    if funcion == 1:  # Leer Coils
        address, count = obtener_parametros_lectura()
        print(f"\nEjecutando: Leer {count} coils desde dirección {address}")
        response = client.read_coils(address, count, unit=unit_id)
        
    elif funcion == 2:  # Leer Discrete Inputs
        address, count = obtener_parametros_lectura()
        print(f"\nEjecutando: Leer {count} discrete inputs desde dirección {address}")
        response = client.read_discrete_inputs(address, count, unit=unit_id)
        
    elif funcion == 3:  # Leer Holding Registers
        address, count = obtener_parametros_lectura()
        print(f"\nEjecutando: Leer {count} holding registers desde dirección {address}")
        response = client.read_holding_registers(address, count, unit=unit_id)
        
    elif funcion == 4:  # Leer Input Registers
        address, count = obtener_parametros_lectura()
        print(f"\nEjecutando: Leer {count} input registers desde dirección {address}")
        response = client.read_input_registers(address, count, unit=unit_id)
        
    elif funcion == 5:  # Escribir Single Coil
        address, value = obtener_parametros_escritura_simple()
        if address is not None and value is not None:
            print(f"\nEjecutando: Escribir coil en dirección {address} con valor {value}")
            response = client.write_coil(address, value, unit=unit_id)
        
    elif funcion == 6:  # Escribir Single Register
        address, value = obtener_parametros_escritura_simple()
        if address is not None and value is not None:
            print(f"\nEjecutando: Escribir registro en dirección {address} con valor {value}")
            response = client.write_register(address, value, unit=unit_id)
        
    elif funcion == 7:  # Escribir Multiple Coils
        address, values = obtener_parametros_escritura_multiple()
        if address is not None and values is not None:
            print(f"\nEjecutando: Escribir {len(values)} coils desde dirección {address}")
            response = client.write_coils(address, values, unit=unit_id)
        
    elif funcion == 8:  # Escribir Multiple Registers
        address, values = obtener_parametros_escritura_multiple()
        if address is not None and values is not None:
            print(f"\nEjecutando: Escribir {len(values)} registros desde dirección {address}")
            response = client.write_registers(address, values, unit=unit_id)
    
    return response

def mostrar_respuesta(response, funcion):
    """Muestra la respuesta de la operación Modbus"""
    if response is None:
        print("❌ No se pudo ejecutar la operación")
        return
    
    # En pymodbus 2.5.3, verificamos errores de manera diferente
    if hasattr(response, 'isError') and response.isError():
        print(f"❌ Error en la respuesta: {response}")
        return
    
    print("✅ Operación exitosa!")
    
    # Mostrar datos según el tipo de operación
    if funcion in [1, 2]:  # Coils o Discrete Inputs
        if hasattr(response, 'bits'):
            print(f"📊 Valores: {response.bits}")
    elif funcion in [3, 4]:  # Holding o Input Registers
        if hasattr(response, 'registers'):
            print(f"📊 Registros: {response.registers}")
            # Mostrar también en hexadecimal para mejor análisis
            hex_values = [f"0x{reg:04X}" for reg in response.registers]
            print(f"📊 Registros (hex): {hex_values}")
    elif funcion in [5, 6, 7, 8]:  # Operaciones de escritura
        print("✅ Escritura completada exitosamente")

def main():
    """Función principal del programa"""
    print("🔧 CLIENTE MODBUS TCP - ZENNER")
    print("=" * 40)
    
    # Obtener configuración de conexión
    host, puerto, unit_id = obtener_configuracion_conexion()
    
    # Crear cliente Modbus
    client = ModbusTcpClient(host, port=puerto)
    
    # Intentar conectar
    print(f"\n🔗 Conectando a {host}:{puerto}...")
    if not client.connect():
        print(f"❌ No se pudo conectar al dispositivo en {host}:{puerto}")
        return
    
    print(f"✅ Conectado exitosamente a {host}:{puerto}")
    
    try:
        while True:
            # Mostrar menú de funciones
            mostrar_menu_funciones()
            
            # Obtener selección del usuario
            opcion_str = input("\nSeleccione una función (1-8) o 'q' para salir: ").strip().lower()
            
            if opcion_str == 'q':
                break
            
            try:
                funcion = int(opcion_str)
                if funcion < 1 or funcion > 8:
                    print("❌ Opción inválida. Seleccione entre 1-8.")
                    continue
            except ValueError:
                print("❌ Opción inválida. Seleccione entre 1-8.")
                continue
            
            # Ejecutar operación
            response = ejecutar_operacion_modbus(client, funcion, unit_id)
            
            # Mostrar respuesta
            mostrar_respuesta(response, funcion)
            
            # Preguntar si desea continuar
            continuar = input("\n¿Desea realizar otra operación? (s/n) [s]: ").strip().lower()
            if continuar == 'n':
                break
            
            print("\n" + "="*50)
    
    except KeyboardInterrupt:
        print("\n🛑 Programa interrumpido por el usuario")
    
    finally:
        # Cerrar conexión
        client.close()
        print("🔌 Conexión cerrada")

if __name__ == "__main__":
    main()