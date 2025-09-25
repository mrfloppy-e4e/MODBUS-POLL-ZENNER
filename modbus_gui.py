import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from pymodbus.client.sync import ModbusTcpClient
import threading
import datetime
import os
import sys
try:
    from PIL import Image, ImageTk
    IMAGES_AVAILABLE = True
except ImportError:
    IMAGES_AVAILABLE = False

def get_resource_path(relative_path):
    """Obtiene la ruta correcta de recursos tanto para desarrollo como para ejecutable"""
    try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # En desarrollo, usa la ruta actual
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def format_modbus_tcp_frame(transaction_id, protocol_id, length, unit_id, function_code, data_bytes=None):
    """Formatea una trama Modbus TCP para visualización"""
    frame_info = []
    frame_info.append("📡 TRAMA MODBUS TCP:")
    frame_info.append("-" * 40)
    frame_info.append(f"Transaction ID: 0x{transaction_id:04X} ({transaction_id})")
    frame_info.append(f"Protocol ID:    0x{protocol_id:04X} ({protocol_id})")
    frame_info.append(f"Length:         0x{length:04X} ({length} bytes)")
    frame_info.append(f"Unit ID:        0x{unit_id:02X} ({unit_id})")
    frame_info.append(f"Function Code:  0x{function_code:02X} ({function_code}) - {get_function_description(function_code)}")
    
    if data_bytes:
        frame_info.append(f"Data:           {' '.join([f'0x{b:02X}' for b in data_bytes])}")
        frame_info.append(f"Data (ASCII):   {data_bytes}")
    
    return "\n".join(frame_info)

def get_function_description(func_code):
    """Obtiene la descripción de un código de función Modbus"""
    descriptions = {
        1: "Read Coils",
        2: "Read Discrete Inputs",
        3: "Read Holding Registers", 
        4: "Read Input Registers",
        5: "Write Single Coil",
        6: "Write Single Register",
        15: "Write Multiple Coils",
        16: "Write Multiple Registers"
    }
    return descriptions.get(func_code, "Unknown Function")

def format_modbus_request(func_num, address, count_or_values, unit_id):
    """Formatea una petición Modbus para mostrar"""
    frame_lines = []
    frame_lines.append("📤 TRAMA ENVIADA (REQUEST):")
    frame_lines.append("=" * 50)
    
    # Simular MBAP Header (Modbus Application Protocol)
    transaction_id = 0x0001  # Simulado
    protocol_id = 0x0000     # Modbus TCP
    unit_id_byte = unit_id
    
    if func_num in [1, 2, 3, 4]:  # Lectura
        length = 6  # Unit ID (1) + Function (1) + Address (2) + Count (2)
        frame_lines.append(f"MBAP Header:")
        frame_lines.append(f"  Transaction ID: 0x{transaction_id:04X}")
        frame_lines.append(f"  Protocol ID:    0x{protocol_id:04X} (Modbus TCP)")
        frame_lines.append(f"  Length:         0x{length:04X} ({length} bytes)")
        frame_lines.append(f"  Unit ID:        0x{unit_id_byte:02X}")
        frame_lines.append(f"")
        frame_lines.append(f"PDU (Protocol Data Unit):")
        frame_lines.append(f"  Function Code:  0x{func_num:02X} ({get_function_description(func_num)})")
        frame_lines.append(f"  Start Address:  0x{address:04X} ({address})")
        frame_lines.append(f"  Quantity:       0x{count_or_values:04X} ({count_or_values})")
        
    elif func_num in [5, 6]:  # Escritura simple
        length = 6
        frame_lines.append(f"MBAP Header:")
        frame_lines.append(f"  Transaction ID: 0x{transaction_id:04X}")
        frame_lines.append(f"  Protocol ID:    0x{protocol_id:04X} (Modbus TCP)")
        frame_lines.append(f"  Length:         0x{length:04X} ({length} bytes)")
        frame_lines.append(f"  Unit ID:        0x{unit_id_byte:02X}")
        frame_lines.append(f"")
        frame_lines.append(f"PDU (Protocol Data Unit):")
        frame_lines.append(f"  Function Code:  0x{func_num:02X} ({get_function_description(func_num)})")
        frame_lines.append(f"  Address:        0x{address:04X} ({address})")
        if func_num == 5:  # Coil
            value_hex = 0xFF00 if count_or_values else 0x0000
            frame_lines.append(f"  Value:          0x{value_hex:04X} ({'ON' if count_or_values else 'OFF'})")
        else:  # Register
            frame_lines.append(f"  Value:          0x{count_or_values:04X} ({count_or_values})")
            
    elif func_num in [15, 16]:  # Escritura múltiple
        if isinstance(count_or_values, list):
            data_count = len(count_or_values)
            byte_count = data_count * 2 if func_num == 16 else (data_count + 7) // 8
            length = 7 + byte_count
            
            frame_lines.append(f"MBAP Header:")
            frame_lines.append(f"  Transaction ID: 0x{transaction_id:04X}")
            frame_lines.append(f"  Protocol ID:    0x{protocol_id:04X} (Modbus TCP)")
            frame_lines.append(f"  Length:         0x{length:04X} ({length} bytes)")
            frame_lines.append(f"  Unit ID:        0x{unit_id_byte:02X}")
            frame_lines.append(f"")
            frame_lines.append(f"PDU (Protocol Data Unit):")
            frame_lines.append(f"  Function Code:  0x{func_num:02X} ({get_function_description(func_num)})")
            frame_lines.append(f"  Start Address:  0x{address:04X} ({address})")
            frame_lines.append(f"  Quantity:       0x{data_count:04X} ({data_count})")
            frame_lines.append(f"  Byte Count:     0x{byte_count:02X} ({byte_count})")
            
            if func_num == 16:  # Registers
                frame_lines.append(f"  Values:         {[f'0x{v:04X}' for v in count_or_values[:5]]}")
                if len(count_or_values) > 5:
                    frame_lines.append(f"                  ... y {len(count_or_values)-5} valores más")
            else:  # Coils
                frame_lines.append(f"  Values:         {count_or_values[:10]}")
                if len(count_or_values) > 10:
                    frame_lines.append(f"                  ... y {len(count_or_values)-10} valores más")
    
    return "\n".join(frame_lines)

def format_modbus_response(func_num, response, operation_desc):
    """Formatea una respuesta Modbus para mostrar"""
    frame_lines = []
    frame_lines.append("📥 TRAMA RECIBIDA (RESPONSE):")
    frame_lines.append("=" * 50)
    
    if response is None:
        frame_lines.append("❌ No se recibió respuesta")
        return "\n".join(frame_lines)
    
    if hasattr(response, 'isError') and response.isError():
        frame_lines.append("❌ RESPUESTA CON ERROR:")
        frame_lines.append(f"Error: {response}")
        return "\n".join(frame_lines)
    
    # Simular MBAP Header de respuesta
    transaction_id = 0x0001
    protocol_id = 0x0000
    unit_id = 1  # Simulado
    
    frame_lines.append(f"MBAP Header:")
    frame_lines.append(f"  Transaction ID: 0x{transaction_id:04X}")
    frame_lines.append(f"  Protocol ID:    0x{protocol_id:04X} (Modbus TCP)")
    frame_lines.append(f"  Unit ID:        0x{unit_id:02X}")
    frame_lines.append(f"")
    frame_lines.append(f"PDU (Protocol Data Unit):")
    frame_lines.append(f"  Function Code:  0x{func_num:02X} ({get_function_description(func_num)})")
    
    if func_num in [1, 2]:  # Coils/Discrete Inputs
        if hasattr(response, 'bits'):
            byte_count = (len(response.bits) + 7) // 8
            length = 3 + byte_count
            frame_lines.insert(4, f"  Length:         0x{length:04X} ({length} bytes)")
            frame_lines.append(f"  Byte Count:     0x{byte_count:02X} ({byte_count})")
            frame_lines.append(f"  Values:         {response.bits[:16]}")  # Mostrar primeros 16
            if len(response.bits) > 16:
                frame_lines.append(f"                  ... y {len(response.bits)-16} valores más")
                
    elif func_num in [3, 4]:  # Holding/Input Registers
        if hasattr(response, 'registers'):
            byte_count = len(response.registers) * 2
            length = 3 + byte_count
            frame_lines.insert(4, f"  Length:         0x{length:04X} ({length} bytes)")
            frame_lines.append(f"  Byte Count:     0x{byte_count:02X} ({byte_count})")
            frame_lines.append(f"  Registers (Dec): {response.registers}")
            frame_lines.append(f"  Registers (Hex): {[f'0x{r:04X}' for r in response.registers]}")
            
    elif func_num in [5, 6, 15, 16]:  # Escritura
        length = 6
        frame_lines.insert(4, f"  Length:         0x{length:04X} ({length} bytes)")
        frame_lines.append(f"  ✅ Escritura confirmada exitosamente")
    
    return "\n".join(frame_lines)

class ModbusGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MODBUS TCP POLL - ZENNER")
        self.root.geometry("1000x700")
        self.root.state('zoomed')  # Maximizar ventana al iniciar
        self.root.resizable(True, True)
        
        # Cliente Modbus
        self.client = None
        self.connected = False
        
        # Configurar favicon e imágenes
        self.setup_favicon()
        
        # Configurar el estilo
        self.setup_styles()
        
        # Crear la interfaz
        self.create_interface()
        
    def setup_favicon(self):
        """Configura el favicon de la aplicación"""
        try:
            # Ruta local del favicon
            favicon_path = get_resource_path(os.path.join("img", "zenner-ico-sinfondo.ico"))
            if os.path.exists(favicon_path):
                self.root.iconbitmap(favicon_path)
            else:
                self.root.iconbitmap(default=None)  # Usar favicon por defecto
        except:
            # Si falla, usar favicon por defecto
            try:
                self.root.iconbitmap(default=None)
            except:
                pass  # Ignorar errores de favicon
        
    def setup_styles(self):
        """Configura los estilos de la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores
        style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 10, 'bold'))
        style.configure('Connected.TLabel', foreground='green', font=('Arial', 9, 'bold'))
        style.configure('Disconnected.TLabel', foreground='red', font=('Arial', 9, 'bold'))
        
    def create_interface(self):
        """Crea la interfaz principal"""
        # Frame principal dividido en dos columnas
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights para redimensionamiento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header con logo y título
        self.create_header(main_frame)
        
        # PANEL IZQUIERDO - Configuración y Envío
        self.create_left_panel(main_frame)
        
        # PANEL DERECHO - Respuestas
        self.create_right_panel(main_frame)
        
    def create_header(self, parent):
        """Crea el header con título solamente"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        header_frame.columnconfigure(0, weight=1)
        
        # Solo título principal, sin logo
        title_label = ttk.Label(header_frame, text="🔧 MODBUS TCP POLL - ZENNER", style='Title.TLabel')
        title_label.grid(row=0, column=0)
        
    def create_left_panel(self, parent):
        """Crea el panel izquierdo para configuración y envío"""
        # Frame contenedor izquierdo
        left_frame = ttk.LabelFrame(parent, text="📤 CONFIGURACIÓN Y ENVÍO DE TRAMA", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        left_frame.columnconfigure(1, weight=1)
        left_frame.rowconfigure(5, weight=1)  # Permitir que el área de debug se expanda (row 5 es donde estará el debug)
        
        row = 0
        
        # === CONEXIÓN ===
        conn_frame = ttk.LabelFrame(left_frame, text="Conexión", padding="5")
        conn_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        conn_frame.columnconfigure(1, weight=1)
        
        # IP
        ttk.Label(conn_frame, text="IP:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.ip_var = tk.StringVar(value="192.168.1.100")
        self.ip_entry = ttk.Entry(conn_frame, textvariable=self.ip_var, width=15)
        self.ip_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        
        # Puerto
        ttk.Label(conn_frame, text="Puerto:").grid(row=0, column=2, sticky=tk.W, padx=(10, 5))
        self.port_var = tk.StringVar(value="502")
        self.port_entry = ttk.Entry(conn_frame, textvariable=self.port_var, width=8)
        self.port_entry.grid(row=0, column=3, sticky=tk.W, padx=(0, 10))
        
        # Unit ID
        ttk.Label(conn_frame, text="Unit ID:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.unit_var = tk.StringVar(value="1")
        self.unit_entry = ttk.Entry(conn_frame, textvariable=self.unit_var, width=8)
        self.unit_entry.grid(row=1, column=1, sticky=tk.W, pady=(5, 0))
        
        # Botón conectar y estado
        self.connect_btn = ttk.Button(conn_frame, text="Conectar", command=self.toggle_connection)
        self.connect_btn.grid(row=1, column=2, sticky=tk.W, padx=(10, 5), pady=(5, 0))
        
        self.status_label = ttk.Label(conn_frame, text="● Desconectado", style='Disconnected.TLabel')
        self.status_label.grid(row=1, column=3, sticky=tk.W, padx=(10, 0), pady=(5, 0))
        
        row += 1
        
        # === FUNCIÓN MODBUS ===
        func_frame = ttk.LabelFrame(left_frame, text="Función Modbus", padding="5")
        func_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        func_frame.columnconfigure(1, weight=1)
        
        ttk.Label(func_frame, text="Función:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.function_var = tk.StringVar(value="3")
        self.function_combo = ttk.Combobox(func_frame, textvariable=self.function_var, width=30, state="readonly")
        self.function_combo['values'] = (
            "1 - Leer Coils (FC01)",
            "2 - Leer Discrete Inputs (FC02)", 
            "3 - Leer Holding Registers (FC03)",
            "4 - Leer Input Registers (FC04)",
            "5 - Escribir Single Coil (FC05)",
            "6 - Escribir Single Register (FC06)",
            "15 - Escribir Multiple Coils (FC15)",
            "16 - Escribir Multiple Registers (FC16)"
        )
        self.function_combo.current(2)  # FC03 por defecto
        self.function_combo.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.function_combo.bind('<<ComboboxSelected>>', self.on_function_change)
        
        row += 1
        
        # === PARÁMETROS ===
        params_frame = ttk.LabelFrame(left_frame, text="Parámetros", padding="5")
        params_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        params_frame.columnconfigure(1, weight=1)
        
        # Dirección
        ttk.Label(params_frame, text="Dirección:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.address_var = tk.StringVar(value="0")
        self.address_entry = ttk.Entry(params_frame, textvariable=self.address_var, width=10)
        self.address_entry.grid(row=0, column=1, sticky=tk.W)
        
        # Cantidad (para lectura)
        self.count_label = ttk.Label(params_frame, text="Cantidad:")
        self.count_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.count_var = tk.StringVar(value="1")
        self.count_entry = ttk.Entry(params_frame, textvariable=self.count_var, width=10)
        self.count_entry.grid(row=1, column=1, sticky=tk.W, pady=(5, 0))
        
        # Valores (para escritura)
        self.values_label = ttk.Label(params_frame, text="Valores:")
        self.values_var = tk.StringVar()
        self.values_entry = ttk.Entry(params_frame, textvariable=self.values_var, width=30)
        
        row += 1
        
        # === TRAMA ACTUAL ===
        trama_frame = ttk.LabelFrame(left_frame, text="Trama a Enviar", padding="5")
        trama_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        trama_frame.columnconfigure(0, weight=1)
        
        self.trama_text = scrolledtext.ScrolledText(trama_frame, height=4, width=50, font=('Courier', 9))
        self.trama_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        row += 1
        
        # === BOTONES ===
        buttons_frame = ttk.Frame(left_frame)
        buttons_frame.grid(row=row, column=0, columnspan=2, pady=(10, 0))
        
        self.send_btn = ttk.Button(buttons_frame, text="📤 Enviar Trama", command=self.send_modbus_request, state="disabled")
        self.send_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.clear_btn = ttk.Button(buttons_frame, text="🗑️ Limpiar", command=self.clear_response)
        self.clear_btn.grid(row=0, column=1, padx=(0, 10))
        
        self.about_btn = ttk.Button(buttons_frame, text="ℹ️ Acerca de", command=self.show_about)
        self.about_btn.grid(row=0, column=2)
        
        row += 1
        
        # === ÁREA DE DEBUG Y AYUDA ===
        debug_frame = ttk.LabelFrame(left_frame, text="🔍 DEBUG - Ayuda y Correcciones", padding="5")
        debug_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        debug_frame.columnconfigure(0, weight=1)
        debug_frame.rowconfigure(0, weight=1)  # Permitir que el debug se expanda
        
        self.debug_text = scrolledtext.ScrolledText(debug_frame, height=15, width=50, font=('Courier', 8))
        self.debug_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar tags para colores en debug
        self.debug_text.tag_configure("debug_error", foreground="red", font=('Courier', 8, 'bold'))
        self.debug_text.tag_configure("debug_warning", foreground="orange", font=('Courier', 8, 'bold'))
        self.debug_text.tag_configure("debug_info", foreground="blue", font=('Courier', 8))
        self.debug_text.tag_configure("debug_success", foreground="green", font=('Courier', 8, 'bold'))
        
        # Mostrar ayuda inicial
        self.show_initial_debug_help()
        
        # Actualizar trama inicialmente
        self.update_frame_preview()
        
        # Bind para actualizar trama en tiempo real
        for var in [self.function_var, self.address_var, self.count_var, self.values_var]:
            var.trace('w', lambda *args: self.update_frame_preview())
        
    def create_right_panel(self, parent):
        """Crea el panel derecho para mostrar respuestas"""
        # Frame contenedor derecho
        right_frame = ttk.LabelFrame(parent, text="📥 RESPUESTA DEL ESCLAVO", padding="10")
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        
        # === INFO DE RESPUESTA ===
        info_frame = ttk.LabelFrame(right_frame, text="Información de Respuesta", padding="5")
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        info_frame.columnconfigure(1, weight=1)
        
        # Agregar logo de Zenner en el panel derecho (arriba a la derecha)
        self.logo_image_right = None
        if IMAGES_AVAILABLE:
            try:
                logo_path = get_resource_path(os.path.join("img", "Zenner Tecnologia FONDOS CLAROS - chicos.png"))
                
                if os.path.exists(logo_path):
                    # Cargar imagen desde archivo local para panel derecho
                    from PIL import Image, ImageTk
                    image_data = Image.open(logo_path)
                    # Redimensionar logo a tamaño apropiado para el panel derecho
                    image_data = image_data.resize((100, 35), Image.Resampling.LANCZOS)
                    self.logo_image_right = ImageTk.PhotoImage(image_data)
                    
                    # Crear label con logo en el panel derecho
                    logo_label_right = ttk.Label(info_frame, image=self.logo_image_right)
                    logo_label_right.grid(row=0, column=2, rowspan=2, padx=(10, 0))
                else:
                    self.logo_image_right = None
            except Exception as e:
                self.logo_image_right = None
        else:
            self.logo_image_right = None
        
        # Estado de la última operación
        ttk.Label(info_frame, text="Estado:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.response_status = ttk.Label(info_frame, text="Sin respuesta", foreground="gray")
        self.response_status.grid(row=0, column=1, sticky=tk.W)
        
        # Timestamp
        ttk.Label(info_frame, text="Timestamp:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.timestamp_label = ttk.Label(info_frame, text="-", foreground="gray")
        self.timestamp_label.grid(row=1, column=1, sticky=tk.W, pady=(5, 0))
        
        # === RESPUESTA DETALLADA ===
        response_frame = ttk.LabelFrame(right_frame, text="Datos Recibidos", padding="5")
        response_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        response_frame.columnconfigure(0, weight=1)
        response_frame.rowconfigure(0, weight=1)
        
        self.response_text = scrolledtext.ScrolledText(response_frame, font=('Courier', 10))
        self.response_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar tags para colores
        self.response_text.tag_configure("success", foreground="green", font=('Courier', 10, 'bold'))
        self.response_text.tag_configure("error", foreground="red", font=('Courier', 10, 'bold'))
        self.response_text.tag_configure("info", foreground="blue", font=('Courier', 10))
        self.response_text.tag_configure("header", foreground="purple", font=('Courier', 10, 'bold'))
        
    def show_initial_debug_help(self):
        """Muestra la ayuda inicial en el área de debug"""
        self.add_debug_log("🔍 ÁREA DE DEBUG Y AYUDA", "debug_info")
        self.add_debug_log("=" * 40, "debug_info")
        self.add_debug_log("ℹ️  Consejos para configurar tramas:", "debug_info")
        self.add_debug_log("", "debug_info")
        self.add_debug_log("📝 Escritura múltiple (FC15/FC16):", "debug_warning")
        self.add_debug_log("   - Separar valores con COMAS: 111,222,333", "debug_info")
        self.add_debug_log("   - NO usar espacios: ❌ '111 222 333'", "debug_error")
        self.add_debug_log("", "debug_info")
        self.add_debug_log("🔢 Valores numéricos:", "debug_warning")
        self.add_debug_log("   - Solo números enteros: 0-65535", "debug_info")
        self.add_debug_log("   - Sin caracteres especiales", "debug_info")
        self.add_debug_log("", "debug_info")
        self.add_debug_log("📍 Configuración detectada automáticamente", "debug_success")
        
    def add_debug_log(self, message, tag="debug_info"):
        """Añade un mensaje al área de debug"""
        self.debug_text.insert(tk.END, message + "\n", tag)
        self.debug_text.see(tk.END)
        
    def clear_debug_log(self):
        """Limpia el área de debug"""
        self.debug_text.delete(1.0, tk.END)
        
    def validate_and_debug_parameters(self, func_num):
        """Valida parámetros y muestra debug específico según la función"""
        self.clear_debug_log()
        self.add_debug_log("🔍 VALIDANDO CONFIGURACIÓN...", "debug_info")
        self.add_debug_log("=" * 40, "debug_info")
        
        # Debug de parámetros básicos
        try:
            address = int(self.address_var.get() or 0)
            unit_id = int(self.unit_var.get() or 1)
            self.add_debug_log(f"✅ Dirección: {address} (válida)", "debug_success")
            self.add_debug_log(f"✅ Unit ID: {unit_id} (válido)", "debug_success")
        except ValueError:
            self.add_debug_log("❌ Error: Dirección o Unit ID no son números válidos", "debug_error")
            return False
        
        # Debug específico por función
        if func_num in [1, 2, 3, 4]:  # Funciones de lectura
            try:
                count = int(self.count_var.get() or 1)
                if count < 1 or count > 2000:
                    self.add_debug_log("⚠️  Advertencia: Cantidad fuera del rango típico (1-2000)", "debug_warning")
                else:
                    self.add_debug_log(f"✅ Cantidad: {count} (válida)", "debug_success")
                
                self.add_debug_log("", "debug_info")
                self.add_debug_log("📖 FUNCIÓN DE LECTURA:", "debug_info")
                self.add_debug_log(f"   - Se leerán {count} valores desde dirección {address}", "debug_info")
                
            except ValueError:
                self.add_debug_log("❌ Error: La cantidad debe ser un número entero", "debug_error")
                return False
                
        elif func_num in [5, 6]:  # Escritura simple
            values_str = self.values_var.get().strip()
            if not values_str:
                self.add_debug_log("❌ Error: Debe especificar un valor para escribir", "debug_error")
                self.add_debug_log("💡 Ejemplo: 1234 (para registro) o 1 (para coil)", "debug_warning")
                return False
            
            try:
                value = int(values_str)
                if func_num == 5:  # Coil
                    if value not in [0, 1]:
                        self.add_debug_log("⚠️  Advertencia: Para coils use 0 (OFF) o 1 (ON)", "debug_warning")
                    self.add_debug_log(f"✅ Valor coil: {value} ({'ON' if value else 'OFF'})", "debug_success")
                else:  # Register
                    if value < 0 or value > 65535:
                        self.add_debug_log("⚠️  Advertencia: Valor fuera del rango (0-65535)", "debug_warning")
                    self.add_debug_log(f"✅ Valor registro: {value} (0x{value:04X})", "debug_success")
                
                self.add_debug_log("", "debug_info")
                self.add_debug_log("✏️  ESCRITURA SIMPLE:", "debug_info")
                self.add_debug_log(f"   - Se escribirá {value} en dirección {address}", "debug_info")
                
            except ValueError:
                self.add_debug_log("❌ Error: El valor debe ser un número entero", "debug_error")
                self.add_debug_log("💡 Ejemplo correcto: 1234", "debug_warning")
                return False
                
        elif func_num in [15, 16]:  # Escritura múltiple
            values_str = self.values_var.get().strip()
            if not values_str:
                self.add_debug_log("❌ Error: Debe especificar valores para escribir", "debug_error")
                self.add_debug_log("💡 Ejemplo: 111,222,333 (separados por comas)", "debug_warning")
                return False
            
            # Detectar si usa espacios en lugar de comas
            if ' ' in values_str and ',' not in values_str:
                self.add_debug_log("❌ ERROR DETECTADO: Está usando espacios en lugar de comas", "debug_error")
                self.add_debug_log("", "debug_info")
                self.add_debug_log("❌ Formato incorrecto:", "debug_error")
                self.add_debug_log(f"   '{values_str}'", "debug_error")
                self.add_debug_log("", "debug_info")
                self.add_debug_log("✅ Formato correcto:", "debug_success")
                corrected = values_str.replace(' ', ',')
                self.add_debug_log(f"   '{corrected}'", "debug_success")
                self.add_debug_log("", "debug_info")
                self.add_debug_log("💡 SOLUCIÓN: Cambie espacios por comas", "debug_warning")
                return False
            
            try:
                if ',' in values_str:
                    values = [int(v.strip()) for v in values_str.split(',')]
                else:
                    values = [int(values_str)]
                
                if len(values) > 123:  # Límite típico para múltiples registros
                    self.add_debug_log("⚠️  Advertencia: Muchos valores, puede fallar", "debug_warning")
                
                self.add_debug_log(f"✅ Valores detectados: {len(values)} elementos", "debug_success")
                self.add_debug_log(f"   Valores: {values[:5]}{'...' if len(values) > 5 else ''}", "debug_info")
                
                # Validar rango de valores
                invalid_values = [v for v in values if v < 0 or v > 65535]
                if invalid_values:
                    self.add_debug_log(f"⚠️  Valores fuera de rango: {invalid_values}", "debug_warning")
                
                self.add_debug_log("", "debug_info")
                self.add_debug_log("📝 ESCRITURA MÚLTIPLE:", "debug_info")
                self.add_debug_log(f"   - Se escribirán {len(values)} valores desde dirección {address}", "debug_info")
                self.add_debug_log(f"   - Direcciones: {address} a {address + len(values) - 1}", "debug_info")
                
            except ValueError as e:
                self.add_debug_log("❌ Error al procesar valores:", "debug_error")
                self.add_debug_log(f"   {str(e)}", "debug_error")
                self.add_debug_log("", "debug_info")
                self.add_debug_log("💡 Formatos válidos:", "debug_warning")
                self.add_debug_log("   - Un valor: 1234", "debug_info")
                self.add_debug_log("   - Múltiples: 111,222,333", "debug_info")
                self.add_debug_log("   - Con espacios: 111, 222, 333", "debug_info")
                return False
        
        self.add_debug_log("", "debug_info")
        self.add_debug_log("🎯 Configuración lista para enviar", "debug_success")
        return True
        
    def show_function_specific_help(self, func_num):
        """Muestra ayuda específica según la función seleccionada"""
        self.clear_debug_log()
        func_name = self.get_function_name(func_num)
        
        self.add_debug_log(f"📋 AYUDA - FUNCIÓN {func_num}: {func_name}", "debug_info")
        self.add_debug_log("=" * 45, "debug_info")
        
        if func_num in [1, 2, 3, 4]:  # Funciones de lectura
            self.add_debug_log("📖 FUNCIÓN DE LECTURA", "debug_warning")
            self.add_debug_log("", "debug_info")
            self.add_debug_log("🔧 Parámetros necesarios:", "debug_info")
            self.add_debug_log("   • Dirección: Dirección inicial (0-65535)", "debug_info")
            self.add_debug_log("   • Cantidad: Número de elementos a leer", "debug_info")
            self.add_debug_log("", "debug_info")
            self.add_debug_log("💡 Consejos:", "debug_warning")
            self.add_debug_log("   • Use cantidad pequeña para pruebas", "debug_info")
            self.add_debug_log("   • Direcciones típicas: 0, 1, 100, 203", "debug_info")
            
        elif func_num in [5, 6]:  # Escritura simple
            self.add_debug_log("✏️  ESCRITURA SIMPLE", "debug_warning")
            self.add_debug_log("", "debug_info")
            self.add_debug_log("🔧 Parámetros necesarios:", "debug_info")
            self.add_debug_log("   • Dirección: Donde escribir (0-65535)", "debug_info")
            if func_num == 5:
                self.add_debug_log("   • Valor: 0 (OFF) o 1 (ON) para coils", "debug_info")
            else:
                self.add_debug_log("   • Valor: Número entero (0-65535)", "debug_info")
            self.add_debug_log("", "debug_info")
            self.add_debug_log("💡 Ejemplos:", "debug_warning")
            if func_num == 5:
                self.add_debug_log("   • Activar coil: valor = 1", "debug_info")
                self.add_debug_log("   • Desactivar coil: valor = 0", "debug_info")
            else:
                self.add_debug_log("   • Escribir 1234: valor = 1234", "debug_info")
                self.add_debug_log("   • Hexadecimal: 1234 = 0x04D2", "debug_info")
                
        elif func_num in [15, 16]:  # Escritura múltiple
            self.add_debug_log("📝 ESCRITURA MÚLTIPLE", "debug_warning")
            self.add_debug_log("", "debug_info")
            self.add_debug_log("🔧 Parámetros necesarios:", "debug_info")
            self.add_debug_log("   • Dirección: Dirección inicial", "debug_info")
            self.add_debug_log("   • Valores: Lista separada por COMAS", "debug_info")
            self.add_debug_log("", "debug_info")
            self.add_debug_log("✅ FORMATOS CORRECTOS:", "debug_success")
            self.add_debug_log("   • Un valor: 1234", "debug_info")
            self.add_debug_log("   • Múltiples: 111,222,333", "debug_info")
            self.add_debug_log("   • Con espacios: 111, 222, 333", "debug_info")
            self.add_debug_log("", "debug_info")
            self.add_debug_log("❌ FORMATOS INCORRECTOS:", "debug_error")
            self.add_debug_log("   • Con espacios: 111 222 333", "debug_error")
            self.add_debug_log("   • Sin separador: 111222333", "debug_error")
            self.add_debug_log("", "debug_info")
            self.add_debug_log("🎯 ERROR COMÚN: Separar con comas, NO espacios", "debug_warning")
        
        self.add_debug_log("", "debug_info")
        self.add_debug_log("🚀 Configure los parámetros y haga clic en Enviar", "debug_success")
        
    def on_function_change(self, event=None):
        """Maneja el cambio de función Modbus"""
        func_num = int(self.function_var.get().split()[0])
        
        # Mostrar/ocultar campos según la función
        if func_num in [1, 2, 3, 4]:  # Funciones de lectura
            self.count_label.grid()
            self.count_entry.grid()
            self.values_label.grid_remove()
            self.values_entry.grid_remove()
        else:  # Funciones de escritura
            self.count_label.grid_remove()
            self.count_entry.grid_remove()
            self.values_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
            self.values_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(5, 0))
            
        self.update_frame_preview()
        
        # Actualizar debug con ayuda específica para la función seleccionada
        self.show_function_specific_help(func_num)
        
    def update_frame_preview(self):
        """Actualiza la vista previa de la trama"""
        try:
            func_num = int(self.function_var.get().split()[0])
            address = int(self.address_var.get() or 0)
            unit_id = int(self.unit_var.get() or 1)
            
            trama_info = f"Función: {func_num} ({self.get_function_name(func_num)})\n"
            trama_info += f"Unit ID: {unit_id}\n"
            trama_info += f"Dirección: {address}\n"
            
            if func_num in [1, 2, 3, 4]:  # Lectura
                count = int(self.count_var.get() or 1)
                trama_info += f"Cantidad: {count}\n"
            else:  # Escritura
                values = self.values_var.get()
                trama_info += f"Valores: {values}\n"
                
            trama_info += f"\nTrama TCP/IP será construida automáticamente por pymodbus"
            
            self.trama_text.delete(1.0, tk.END)
            self.trama_text.insert(1.0, trama_info)
            
        except ValueError:
            self.trama_text.delete(1.0, tk.END)
            self.trama_text.insert(1.0, "Error en parámetros - verificar valores numéricos")
            
    def get_function_name(self, func_num):
        """Obtiene el nombre de la función Modbus"""
        names = {
            1: "Read Coils",
            2: "Read Discrete Inputs", 
            3: "Read Holding Registers",
            4: "Read Input Registers",
            5: "Write Single Coil",
            6: "Write Single Register",
            15: "Write Multiple Coils",
            16: "Write Multiple Registers"
        }
        return names.get(func_num, "Desconocida")
        
    def toggle_connection(self):
        """Conecta o desconecta del dispositivo Modbus"""
        if not self.connected:
            self.connect_to_device()
        else:
            self.disconnect_from_device()
            
    def connect_to_device(self):
        """Conecta al dispositivo Modbus"""
        try:
            host = self.ip_var.get().strip()
            port = int(self.port_var.get())
            
            if not host:
                messagebox.showerror("Error", "Debe ingresar una dirección IP")
                return
                
            self.client = ModbusTcpClient(host, port=port)
            
            # Usar threading para no bloquear la UI
            def connect_thread():
                try:
                    if self.client.connect():
                        self.root.after(0, self.on_connection_success)
                    else:
                        self.root.after(0, lambda: self.on_connection_error("No se pudo establecer conexión"))
                except Exception as e:
                    error_msg = str(e)
                    self.root.after(0, lambda msg=error_msg: self.on_connection_error(msg))
                    
            self.connect_btn.config(text="Conectando...", state="disabled")
            thread = threading.Thread(target=connect_thread, daemon=True)
            thread.start()
            
        except ValueError:
            messagebox.showerror("Error", "Puerto debe ser un número válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error al conectar: {str(e)}")
            
    def on_connection_success(self):
        """Callback cuando la conexión es exitosa"""
        self.connected = True
        self.connect_btn.config(text="Desconectar", state="normal")
        self.send_btn.config(state="normal")
        self.status_label.config(text="● Conectado", style='Connected.TLabel')
        
        # Log en panel derecho
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.add_response_log(f"[{timestamp}] ✅ CONECTADO", "success")
        self.add_response_log(f"Dispositivo: {self.ip_var.get()}:{self.port_var.get()}", "info")
        self.timestamp_label.config(text=timestamp)
        self.response_status.config(text="Conectado", foreground="green")
        
    def on_connection_error(self, error_msg):
        """Callback cuando hay error en la conexión"""
        self.connect_btn.config(text="Conectar", state="normal")
        self.status_label.config(text="● Error", foreground="red")
        
        # Log en panel derecho
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.add_response_log(f"[{timestamp}] ❌ ERROR DE CONEXIÓN", "error")
        self.add_response_log(f"Error: {error_msg}", "error")
        self.timestamp_label.config(text=timestamp)
        self.response_status.config(text="Error de conexión", foreground="red")
        
    def disconnect_from_device(self):
        """Desconecta del dispositivo Modbus"""
        if self.client:
            self.client.close()
            
        self.connected = False
        self.connect_btn.config(text="Conectar")
        self.send_btn.config(state="disabled")
        self.status_label.config(text="● Desconectado", style='Disconnected.TLabel')
        
        # Log en panel derecho
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.add_response_log(f"[{timestamp}] 🔌 DESCONECTADO", "info")
        self.timestamp_label.config(text=timestamp)
        self.response_status.config(text="Desconectado", foreground="gray")
        
    def send_modbus_request(self):
        """Envía la petición Modbus"""
        if not self.connected:
            messagebox.showerror("Error", "Debe conectarse primero")
            return
            
        try:
            func_num = int(self.function_var.get().split()[0])
            
            # Validar parámetros y mostrar debug
            if not self.validate_and_debug_parameters(func_num):
                return
                
            address = int(self.address_var.get() or 0)
            unit_id = int(self.unit_var.get() or 1)
            
            # Usar threading para no bloquear la UI
            def send_thread():
                try:
                    response = None
                    operation_desc = ""
                    
                    if func_num == 1:  # Read Coils
                        count = int(self.count_var.get() or 1)
                        response = self.client.read_coils(address, count, unit=unit_id)
                        operation_desc = f"Leer {count} coils desde dirección {address}"
                        
                    elif func_num == 2:  # Read Discrete Inputs
                        count = int(self.count_var.get() or 1)
                        response = self.client.read_discrete_inputs(address, count, unit=unit_id)
                        operation_desc = f"Leer {count} discrete inputs desde dirección {address}"
                        
                    elif func_num == 3:  # Read Holding Registers
                        count = int(self.count_var.get() or 1)
                        response = self.client.read_holding_registers(address, count, unit=unit_id)
                        operation_desc = f"Leer {count} holding registers desde dirección {address}"
                        
                    elif func_num == 4:  # Read Input Registers
                        count = int(self.count_var.get() or 1)
                        response = self.client.read_input_registers(address, count, unit=unit_id)
                        operation_desc = f"Leer {count} input registers desde dirección {address}"
                        
                    elif func_num == 5:  # Write Single Coil
                        value = bool(int(self.values_var.get()))
                        response = self.client.write_coil(address, value, unit=unit_id)
                        operation_desc = f"Escribir coil en dirección {address} con valor {value}"
                        
                    elif func_num == 6:  # Write Single Register
                        value = int(self.values_var.get())
                        response = self.client.write_register(address, value, unit=unit_id)
                        operation_desc = f"Escribir registro en dirección {address} con valor {value}"
                        
                    elif func_num == 15:  # Write Multiple Coils
                        values = [bool(int(v.strip())) for v in self.values_var.get().split(',')]
                        response = self.client.write_coils(address, values, unit=unit_id)
                        operation_desc = f"Escribir {len(values)} coils desde dirección {address}"
                        
                    elif func_num == 16:  # Write Multiple Registers
                        values = [int(v.strip()) for v in self.values_var.get().split(',')]
                        response = self.client.write_registers(address, values, unit=unit_id)
                        operation_desc = f"Escribir {len(values)} registros desde dirección {address}"
                    
                    self.root.after(0, lambda r=response, desc=operation_desc, fn=func_num: self.on_response_received(r, desc, fn))
                    
                except Exception as e:
                    error_msg = str(e)
                    self.root.after(0, lambda msg=error_msg: self.on_request_error(msg))
                    
            self.send_btn.config(text="Enviando...", state="disabled")
            thread = threading.Thread(target=send_thread, daemon=True)
            thread.start()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error en parámetros: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al enviar: {str(e)}")
            
    def on_response_received(self, response, operation_desc, func_num):
        """Callback cuando se recibe respuesta"""
        self.send_btn.config(text="📤 Enviar Trama", state="normal")
        
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.timestamp_label.config(text=timestamp)
        
        # Limpiar log anterior
        self.response_text.delete(1.0, tk.END)
        
        # Mostrar información de la operación
        self.add_response_log(f"[{timestamp}] � OPERACIÓN MODBUS", "header")
        self.add_response_log(f"Descripción: {operation_desc}", "info")
        self.add_response_log("", "info")
        
        # Obtener parámetros para formatear la trama enviada
        try:
            address = int(self.address_var.get() or 0)
            unit_id = int(self.unit_var.get() or 1)
            
            if func_num in [1, 2, 3, 4]:  # Lectura
                count = int(self.count_var.get() or 1)
                request_frame = format_modbus_request(func_num, address, count, unit_id)
            elif func_num in [5, 6]:  # Escritura simple
                value = int(self.values_var.get())
                request_frame = format_modbus_request(func_num, address, value, unit_id)
            elif func_num in [15, 16]:  # Escritura múltiple
                values_str = self.values_var.get().strip()
                if ',' in values_str:
                    values = [int(v.strip()) for v in values_str.split(',')]
                else:
                    values = [int(values_str)]
                request_frame = format_modbus_request(func_num, address, values, unit_id)
            else:
                request_frame = "Trama de petición no disponible"
                
            # Mostrar trama enviada
            self.add_response_log(request_frame, "info")
            self.add_response_log("", "info")
            
        except Exception as e:
            self.add_response_log(f"Error al formatear trama de petición: {e}", "error")
            self.add_response_log("", "info")
        
        # Formatear y mostrar trama de respuesta
        response_frame = format_modbus_response(func_num, response, operation_desc)
        self.add_response_log(response_frame, "info")
        self.add_response_log("", "info")
        
        if response is None:
            self.add_response_log("❌ ERROR: No se recibió respuesta del dispositivo", "error")
            self.response_status.config(text="Sin respuesta", foreground="red")
            return
            
        # En pymodbus 2.5.3, verificamos errores de manera diferente
        if hasattr(response, 'isError') and response.isError():
            self.add_response_log(f"❌ ERROR EN RESPUESTA: {str(response)}", "error")
            self.response_status.config(text="Error en respuesta", foreground="red")
            return
            
        # Respuesta exitosa - mostrar datos procesados
        self.add_response_log("✅ DATOS PROCESADOS:", "success")
        self.add_response_log("-" * 30, "info")
        self.response_status.config(text="Éxito", foreground="green")
        
        # Mostrar datos según el tipo de función
        if func_num in [1, 2]:  # Coils/Discrete Inputs
            if hasattr(response, 'bits'):
                self.add_response_log(f"Valores (bits): {response.bits}", "info")
                
        elif func_num in [3, 4]:  # Holding/Input Registers
            if hasattr(response, 'registers'):
                self.add_response_log(f"Registros (decimal): {response.registers}", "info")
                hex_values = [f"0x{reg:04X}" for reg in response.registers]
                self.add_response_log(f"Registros (hex): {hex_values}", "info")
                
                # Tabla formateada
                self.add_response_log("\n📊 TABLA DE REGISTROS:", "header")
                self.add_response_log("-" * 40, "info")
                self.add_response_log(f"{'Addr':<8} {'Decimal':<10} {'Hex':<8} {'Binary':<16}", "info")
                self.add_response_log("-" * 40, "info")
                
                start_addr = int(self.address_var.get() or 0)
                for i, reg in enumerate(response.registers):
                    addr = start_addr + i
                    binary = f"{reg:016b}"
                    hex_value = f"0x{reg:04X}"
                    self.add_response_log(f"{addr:<8} {reg:<10} {hex_value:<8} {binary}", "info")
                    
        elif func_num in [5, 6, 15, 16]:  # Operaciones de escritura
            self.add_response_log("✅ Escritura completada exitosamente", "success")
            
        # Actualizar debug con mensaje de éxito
        self.show_success_debug(func_num, operation_desc)
            
    def on_request_error(self, error_msg):
        """Callback cuando hay error en la petición"""
        self.send_btn.config(text="📤 Enviar Trama", state="normal")
        
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.add_response_log(f"[{timestamp}] ❌ ERROR EN PETICIÓN", "error")
        self.add_response_log(f"Error: {error_msg}", "error")
        self.timestamp_label.config(text=timestamp)
        self.response_status.config(text="Error en petición", foreground="red")
        
        # Mostrar debug de error con sugerencias
        self.show_error_debug(error_msg)
        
    def show_success_debug(self, func_num, operation_desc):
        """Muestra debug de operación exitosa"""
        self.clear_debug_log()
        self.add_debug_log("🎉 OPERACIÓN EXITOSA!", "debug_success")
        self.add_debug_log("=" * 40, "debug_info")
        self.add_debug_log(f"✅ {operation_desc}", "debug_success")
        self.add_debug_log("", "debug_info")
        
        if func_num in [1, 2, 3, 4]:
            self.add_debug_log("📊 Los datos se muestran en el panel derecho", "debug_info")
            self.add_debug_log("💡 Revise la tabla con valores en decimal, hex y binario", "debug_warning")
        else:
            self.add_debug_log("✏️  Los valores se escribieron correctamente", "debug_info")
            self.add_debug_log("💡 Puede leer los registros para verificar", "debug_warning")
            
        self.add_debug_log("", "debug_info")
        self.add_debug_log("🔄 Puede realizar otra operación o cambiar función", "debug_info")
        
    def show_error_debug(self, error_msg):
        """Muestra debug de error con sugerencias"""
        self.clear_debug_log()
        self.add_debug_log("❌ ERROR DETECTADO", "debug_error")
        self.add_debug_log("=" * 40, "debug_info")
        self.add_debug_log(f"Error: {error_msg}", "debug_error")
        self.add_debug_log("", "debug_info")
        
        # Análisis específico del error
        if "invalid literal for int()" in error_msg.lower():
            self.add_debug_log("🔍 ANÁLISIS DEL ERROR:", "debug_warning")
            if "base 10" in error_msg:
                self.add_debug_log("❌ Problema: Formato de número incorrecto", "debug_error")
                self.add_debug_log("", "debug_info")
                
                # Detectar si es problema de espacios vs comas
                if "'" in error_msg:
                    error_value = error_msg.split("'")[1]
                    if " " in error_value and "," not in error_value:
                        self.add_debug_log("🎯 CAUSA DETECTADA: Usando espacios en lugar de comas", "debug_warning")
                        self.add_debug_log("", "debug_info")
                        self.add_debug_log("❌ Valor incorrecto:", "debug_error")
                        self.add_debug_log(f"   '{error_value}'", "debug_error")
                        self.add_debug_log("", "debug_info")
                        self.add_debug_log("✅ SOLUCIÓN:", "debug_success")
                        corrected = error_value.replace(" ", ",")
                        self.add_debug_log(f"   '{corrected}'", "debug_success")
                        self.add_debug_log("", "debug_info")
                        self.add_debug_log("💡 Para múltiples valores use COMAS, no espacios", "debug_warning")
                        
                self.add_debug_log("", "debug_info")
                self.add_debug_log("✅ FORMATOS VÁLIDOS:", "debug_success")
                self.add_debug_log("   • Un valor: 1234", "debug_info")
                self.add_debug_log("   • Múltiples: 111,222,333", "debug_info")
                self.add_debug_log("   • Con espacios: 111, 222, 333", "debug_info")
                
        elif "connection" in error_msg.lower():
            self.add_debug_log("🔍 PROBLEMA DE CONEXIÓN:", "debug_warning")
            self.add_debug_log("• Verificar IP y puerto del dispositivo", "debug_info")
            self.add_debug_log("• Comprobar que el dispositivo esté encendido", "debug_info")
            self.add_debug_log("• Revisar configuración de red", "debug_info")
            
        elif "timeout" in error_msg.lower():
            self.add_debug_log("🔍 PROBLEMA DE TIMEOUT:", "debug_warning")
            self.add_debug_log("• El dispositivo no responde a tiempo", "debug_info")
            self.add_debug_log("• Verificar Unit ID correcto", "debug_info")
            self.add_debug_log("• Comprobar direcciones válidas", "debug_info")
            
        else:
            self.add_debug_log("💡 SUGERENCIAS GENERALES:", "debug_warning")
            self.add_debug_log("• Verificar todos los parámetros", "debug_info")
            self.add_debug_log("• Comprobar conexión al dispositivo", "debug_info")
            self.add_debug_log("• Revisar formato de valores", "debug_info")
            
        self.add_debug_log("", "debug_info")
        self.add_debug_log("🔄 Corrija el error y vuelva a intentar", "debug_warning")
        
    def add_response_log(self, message, tag="info"):
        """Añade un mensaje al log de respuestas"""
        self.response_text.insert(tk.END, message + "\n", tag)
        self.response_text.see(tk.END)
        
    def clear_response(self):
        """Limpia el panel de respuestas"""
        self.response_text.delete(1.0, tk.END)
        self.response_status.config(text="Sin respuesta", foreground="gray")
        self.timestamp_label.config(text="-")
        # También limpiar el debug y mostrar ayuda inicial
        self.clear_debug_log()
        self.show_initial_debug_help()
        
    def show_about(self):
        """Muestra información sobre la aplicación"""
        about_text = """MODBUS TCP ZENNER

Desarrollado por: Eric Azúa (eric.azua@zenner.cl)
Linkedin: https://eazua.com
Tecnología: Python/Claude Sonnet 4

📧 Contáctenos:
• Web: www.zenner.cl
• Email: info@zenner.cl
• Teléfono: +56226346982

© 2024 Zenner Tecnologías Chile"""
        
        messagebox.showinfo("Acerca de MODBUS TCP ZENNER", about_text)

def main():
    root = tk.Tk()
    app = ModbusGUI(root)
    
    # Manejar cierre de ventana
    def on_closing():
        if app.connected:
            app.disconnect_from_device()
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()