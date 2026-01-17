# Lead Extractor: Gmail to Google Sheets

## El Problema 🚨

¿Recibis leads por email pero los procesas a mano?

- Copias datos a Excel/Sheets manualmente
- Pierdes **2-3 horas al día**
- Se te olvidan algunos leads
- Duplicados en la base de datos
- Es repetitivo y tedioso

## La Solución ✨

Este script automatiza **100% del proceso**:

✅ Lee emails nuevos de Gmail automáticamente
✅ Extrae datos clave (nombre, email, teléfono, empresa, presupuesto)
✅ Valida información (formato correcto, sin errores)
✅ Actualiza tu Google Sheets en tiempo real
✅ Marca emails como "procesados"
✅ Envia confirmación al cliente (opcional)

## Resultado Real

| Antes | Después |
|-------|----------|
| 3 horas/día procesando 50 leads | 2 minutos automático |
| Errores de tipeo | Datos validados |
| Sin registro de qué se procesó | Historial completo |

---

## Instalación

### Requisitos previos
- Python 3.8+
- Cuenta de Google (Gmail + Google Workspace)
- Git

### Paso 1: Clonar repositorio

```bash
git clone https://github.com/ocampoalbano-coder/lead-extractor-automation.git
cd lead-extractor-automation
```

### Paso 2: Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Google Cloud

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto
3. Activa estas APIs:
   - Gmail API
   - Google Sheets API
4. Crea credenciales (OAuth 2.0 - Cuenta de servicio)
5. Descarga el archivo JSON
6. Renombra a `credentials.json` y coloca en la raíz del proyecto

### Paso 5: Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` con:

```
# Gmail
GMAIL_USER=tu-email@gmail.com

# Google Sheets
SHEETS_ID=ID-de-tu-hoja
SHEET_NAME=Leads

# Configuración
SEARCH_QUERY=subject:Nueva consulta OR subject:Solicitud
MARK_AS_READ=True
SEND_CONFIRMATION=False
```

### Paso 6: Correr el script

```bash
# Una sola vez
python main.py

# Ejecutar cada hora (Windows)
python schedule_windows.py

# Ejecutar cada hora (Linux/macOS)
python schedule_unix.py
```

---

## Casos de Uso

### Agencia de Marketing
Lees leads de formulario en web → Sheets automáticamente → Tu equipo da seguimiento al día siguiente

### Consultoría
Clientes envían solicitudes por email → Se registran automáticamente → No se pierde ninguno

### Ecommerce
Órdenes/consultas por email → Se sincronizan con CRM → Respuestas automáticas

---

## Troubleshooting

### "Permission denied" en credenciales
- Verifica que `credentials.json` esté en la carpeta raíz
- Comprueba permisos: `ls -l credentials.json`

### "No module named 'google'"
```bash
pip install --upgrade google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Los emails no se leen
- Verifica el `SEARCH_QUERY` en `.env`
- Intenta: `python test_gmail.py`

---

## Estructura del Proyecto

```
├── main.py                    # Punto de entrada principal
├── config.py                  # Configuración (env vars)
├── modules/
│   ├── gmail_reader.py       # Lectura de Gmail
│   ├── data_extractor.py     # Extracción de datos
│   ├── sheets_writer.py      # Escritura en Sheets
│   └── logger.py             # Logs
├── requirements.txt          # Dependencias
├── .env.example              # Template de variables
├── credentials.json          # Credenciales de Google (NO VERSIONADO)
└── README.md                 # Este archivo
```

---

## Desarrollo

Si quieres contribuir o modificar:

```bash
# Crear rama
git checkout -b feature/tu-idea

# Hacer cambios
git add .
git commit -m "Descripción clara del cambio"
git push origin feature/tu-idea
```

---

## Pricing (Si lo vendes como servicio)

- **Setup inicial:** $150-300 USD
- **Mantenimiento/mes:** $30-50 USD
- **Setup + 3 meses:** $250 USD

---

## Licencia

MIT - Usa libremente

---

## Preguntas o Problemas?

Abre un [issue](https://github.com/ocampoalbano-coder/lead-extractor-automation/issues) o contactame en LinkedIn.

---

**Hecho por:** Albano Ocampo | [GitHub](https://github.com/ocampoalbano-coder) | Automatización & APIs