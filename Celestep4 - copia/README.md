Celeste Súper Guía 🍓

 Es una plataforma web interactiva diseñada para llevar el registro completo (CRUD) de las fresas, cintas de casete y corazones de cristal ocultos en el videojuego Celeste.

Tecnologías Utilizadas
Backend: Python, FastAPI, SQLite3.
Frontend: HTML5, CSS3, JavaScript, Bootstrap 5.
Control de Versiones y Despliegue:GitHub y Vercel.

Estructura General del Sistema

├── Celestep4/
│   ├── frontend/          # Interfaz gráfica 
│   │   ├── index.html     # Estructura HTML de la aplicación
│   │   ├── css.css        # Estilos 
│   │   └── app.js         # Controlador JavaScript y consumo de la API
│   ├── database.py        # Configuración e inicialización de SQLite
│   ├── main.py            # Rutas, endpoints y servicio de archivos estáticos
│   ├── requirements.txt   # Dependencias de Python del servidor
│   ├──.gitignore          # Archivos excluidos del control de versiones
│   └──README.md           # Documentación técnica del proyecto

Instrucciones de Instalación y Ejecución

1. Clonar el repositorio
git clone <URL_DE_TU_REPOSITORIO_DE_GITHUB>
cd <Celestep4>

2. Configurar y ejecutar el Backend (FastAPI)
Navega a la carpeta del backend, instala las dependencias necesarias e inicia el servidor con Uvicorn:

cd backend
pip install -r requirements.txt
uvicorn main:app --reload

El servidor backend se ejecutará localmente en: http://127.0.0.1:8000

3. Acceder a la Aplicación
Gracias a la integración del sistema, puedes ver el Frontend directamente entrando a la raíz del servidor en tu navegador:
http://127.0.0.1:8000

Si deseas probar o inspeccionar los endpoints individuales de la API de forma interactiva, puedes ingresar a la documentación automática de FastAPI en:
http://127.0.0