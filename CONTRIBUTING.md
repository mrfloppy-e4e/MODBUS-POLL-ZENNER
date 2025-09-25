# 🤝 Contributing to Modbus Poll Zenner

¡Gracias por tu interés en contribuir al proyecto Modbus Poll Zenner! Este documento te guiará a través del proceso de contribución.

## 🎯 Cómo Contribuir

### 🐛 Reportar Bugs
1. Verifica que el bug no haya sido reportado previamente en [Issues](https://github.com/rockmanchile/MODBUS-POLL-ZENNER/issues)
2. Crea un nuevo issue usando la plantilla de Bug Report
3. Incluye toda la información solicitada en la plantilla

### ✨ Solicitar Funcionalidades
1. Verifica que la funcionalidad no haya sido solicitada previamente
2. Crea un nuevo issue usando la plantilla de Feature Request
3. Explica claramente el problema que resolvería y tu solución propuesta

### 🔧 Contribuir Código

#### Pre-requisitos
- Python 3.8 o superior
- Git configurado correctamente
- Conocimiento básico de protocolo Modbus TCP

#### Proceso de Desarrollo

1. **Fork el repositorio**
   ```bash
   git fork https://github.com/rockmanchile/MODBUS-POLL-ZENNER.git
   ```

2. **Clonar tu fork**
   ```bash
   git clone https://github.com/TU_USUARIO/MODBUS-POLL-ZENNER.git
   cd MODBUS-POLL-ZENNER
   ```

3. **Crear entorno virtual**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

5. **Crear rama para tu feature**
   ```bash
   git checkout -b feature/nombre-de-tu-feature
   ```

6. **Desarrollar y testear**
   - Escribe código limpio y bien documentado
   - Sigue las convenciones existentes del proyecto
   - Testea exhaustivamente tus cambios

7. **Commit tus cambios**
   ```bash
   git add .
   git commit -m "🚀 Descripción clara de tu cambio"
   ```

8. **Push a tu rama**
   ```bash
   git push origin feature/nombre-de-tu-feature
   ```

9. **Crear Pull Request**
   - Usa una descripción clara del cambio
   - Referencia issues relacionados
   - Incluye screenshots si es relevante

## 📋 Estándares de Código

### Python Style Guide
- Sigue PEP 8 para el estilo de código Python
- Usa nombres descriptivos para variables y funciones
- Incluye docstrings para funciones públicas
- Máximo 100 caracteres por línea

### Commits
- Usa prefijos descriptivos: 🚀 (feature), 🐛 (bug), 📚 (docs), 🔧 (config)
- Escribe mensajes en tiempo presente
- Mantén los commits atómicos y enfocados

### Documentación
- Actualiza la documentación para cambios en API
- Incluye ejemplos de uso para nuevas funcionalidades
- Mantén el README.md actualizado

## 🧪 Testing

### Pruebas Manuales
1. Ejecuta la aplicación GUI: `python modbus_gui.py`
2. Prueba todas las funciones Modbus (FC01-FC16)
3. Verifica la visualización de tramas
4. Testea con diferentes configuraciones de red

### Dispositivos de Prueba
- Simuladores Modbus TCP recomendados
- Dispositivos físicos si están disponibles
- Diferentes configuraciones de red

## 📁 Estructura del Proyecto

```
MODBUS POLL ZENNER/
├── modbus_gui.py              # Aplicación principal GUI
├── modbus_zenner.py           # Versión CLI
├── build_exe.py               # Script de construcción
├── requirements.txt           # Dependencias Python
├── img/                       # Recursos gráficos
│   ├── zenner-ico-sinfondo.ico
│   └── Zenner Tecnologia FONDOS CLAROS - chicos.png
├── docs/                      # Documentación
│   ├── README.md
│   ├── MANUAL_USUARIO.md
│   └── DOCUMENTACION_TECNICA.md
└── .github/                   # Templates de GitHub
    └── ISSUE_TEMPLATE/
```

## 🔍 Áreas de Contribución

### 🚀 Funcionalidades Prioritarias
- [ ] Soporte Modbus RTU (puerto serie)
- [ ] Perfiles de configuración guardados
- [ ] Exportación de datos a CSV/Excel
- [ ] Modo de monitoreo continuo
- [ ] Gráficos en tiempo real

### 🐛 Bugs Conocidos
- Consulta los [Issues abiertos](https://github.com/rockmanchile/MODBUS-POLL-ZENNER/issues)

### 📚 Documentación
- Traducción a otros idiomas
- Más ejemplos de uso
- Tutoriales en video
- Guías de troubleshooting

## 💬 Comunicación

- **Issues**: Para bugs y solicitudes de funcionalidades
- **Pull Requests**: Para contribuciones de código
- **Discusiones**: Para preguntas generales y discusiones

## 📜 Licencia

Al contribuir a este proyecto, aceptas que tus contribuciones serán licenciadas bajo la misma licencia del proyecto.

## 🙏 Reconocimiento

Todos los contribuyentes serán reconocidos en el archivo CONTRIBUTORS.md y en los releases del proyecto.

---

¡Gracias por hacer que Modbus Poll Zenner sea mejor para todos! 🚀