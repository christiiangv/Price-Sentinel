# 🛡️ PriceSentinel — Rastreador Inteligente de Precios y Ofertas

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Pytest](https://img.shields.io/badge/Tests-Passing-10b981?style=for-the-badge&logo=pytest&logoColor=white)
![Licencia](https://img.shields.io/badge/Licencia-MIT-6366f1?style=for-the-badge)

**PriceSentinel** es una herramienta CLI modular desarrollada en Python para monitorizar precios de tiendas online, almacenar su evolución histórica en SQLite, detectar mínimos históricos reales y enviar alertas instantáneas a Telegram cuando un producto alcanza tu precio objetivo.

---

## ✨ Características Principales

* **🕷️ Scraping Inteligente:** Extracción mediante selectores CSS con limpieza automática de divisas europeas (`1.299,95 €`) y anglosajonas (`$1,299.95`).
* **🗄️ Histórico en SQLite:** Base de datos relacional local (`prices.db`) para registrar cada consulta y evitar falsas ofertas.
* **📈 Motor de Análisis:** Calcula mínimos históricos, precios máximos, media y porcentaje real de descuento.
* **📲 Alertas por Telegram:** Notificaciones automáticas al móvil cuando se alcanza el precio deseado o un mínimo histórico.
* **🎨 Interfaz CLI con Rich:** Tablas formateadas, colores e indicadores de estado en tiempo real.
* **⚙️ Integración Continua (CI):** Workflow de GitHub Actions incluido para ejecutar automáticamente la suite de tests (`pytest`) en cada `push`.

---

## 📁 Estructura del Proyecto

```text
price-sentinel/
├── .github/
│   └── workflows/
│       └── ci_and_check.yml # Pipeline de CI con pytest
├── src/
│   ├── __init__.py
│   ├── database.py          # Persistencia y consultas SQLite
│   ├── scraper.py           # Extracción web y normalización de precios
│   ├── analyzer.py          # Lógica de análisis de ofertas
│   └── notifier.py          # Integración con API de Telegram
├── tests/
│   └── test_analyzer.py     # Pruebas unitarias
├── .env.example             # Plantilla de variables de entorno
├── .gitignore               # Archivos excluidos de Git
├── main.py                  # Punto de entrada e interfaz CLI
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Documentación
```

---

## 🚀 Instalación y Uso

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/christiian.gv/price-sentinel.git
   cd price-sentinel
   ```

2. **Crea un entorno virtual e instala las dependencias:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. *(Opcional)* **Configura las alertas de Telegram:**
   Copia `.env.example` como `.env` o exporta las variables de entorno:
   ```bash
   export TELEGRAM_BOT_TOKEN="tu_token_aqui"
   export TELEGRAM_CHAT_ID="tu_chat_id_aqui"
   ```

4. **Ejecuta la aplicación:**
   ```bash
   python main.py
   ```
   Para ejecutar una comprobación directa sin menú interactivo (ideal para `cron` o tareas programadas):
   ```bash
   python main.py --check
   ```

---

## 🧪 Ejecutar Pruebas

```bash
pytest -v
```

---

## 📄 Licencia

Distribuido bajo la **Licencia MIT**.
