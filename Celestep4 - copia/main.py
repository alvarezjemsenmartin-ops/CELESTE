from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # Requerido para servir el frontend
from pydantic import BaseModel
from typing import List, Optional
import database

# Inicializar la base de datos SQLite y cargar datos semilla al arrancar
database.init_db()

app = FastAPI(title="Celeste Tracker API")

# Habilitar CORS para permitir la comunicación bidireccional libre
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- MODELOS PYDANTIC (VALIDACIÓN) -----------------

class SecretoBase(BaseModel):
    capitulo_id: int
    nombre: str
    tipo_coleccionable: str
    lado: str
    ubicacion_detalles: Optional[str] = None

class SecretoCreate(BaseModel):
    capitulo_id: int
    nombre: str
    tipo_coleccionable: str
    lado: str
    ubicacion_detalles: str


# ----------------- ENDPOINTS CRUD PARA SECRETOS -----------------

# CREATE: Registrar un nuevo secreto en el juego
@app.post("/secretos", status_code=status.HTTP_201_CREATED)
def crear_secreto(secreto: SecretoCreate):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO secretos (capitulo_id, nombre, tipo_coleccionable, lado, ubicacion_detalles) VALUES (?, ?, ?, ?, ?)",
            (secreto.capitulo_id, secreto.nombre, secreto.tipo_coleccionable, secreto.lado, secreto.ubicacion_detalles)
        )
        conn.commit()
        nuevo_id = cursor.lastrowid
        return {"id": nuevo_id, "mensaje": "Secreto registrado con éxito"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

# READ: Obtener todos los secretos guardados (incluye el nombre del capítulo asociado)
@app.get("/secretos")
def obtener_secretos():
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT secretos.*, capitulos.nombre AS capitulo_nombre 
        FROM secretos 
        JOIN capitulos ON secretos.capitulo_id = capitulos.id
    ''')
    filas = cursor.fetchall()
    conn.close()
    return [dict(fila) for fila in filas]

# READ: Obtener un solo secreto por su ID
@app.get("/secretos/{secreto_id}")
def obtener_secreto(secreto_id: int):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM secretos WHERE id = ?", (secreto_id,))
    fila = cursor.fetchone()
    conn.close()
    if fila is None:
        raise HTTPException(status_code=404, detail="Secreto no encontrado")
    return dict(fila)

# UPDATE: Modificar los datos de un secreto existente
@app.put("/secretos/{secreto_id}")
def actualizar_secreto(secreto_id: int, secreto: SecretoCreate):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM secretos WHERE id = ?", (secreto_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Secreto no existente")
    
    cursor.execute('''
        UPDATE secretos 
        SET capitulo_id = ?, nombre = ?, tipo_coleccionable = ?, lado = ?, ubicacion_detalles = ?
        WHERE id = ?
    ''', (secreto.capitulo_id, secreto.nombre, secreto.tipo_coleccionable, secreto.lado, secreto.ubicacion_detalles, secreto_id))
    conn.commit()
    conn.close()
    return {"mensaje": "Secreto actualizado correctamente"}

# DELETE: Eliminar un registro de la base de datos de forma definitiva
@app.delete("/secretos/{secreto_id}")
def eliminar_secreto(secreto_id: int):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM secretos WHERE id = ?", (secreto_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Secreto no encontrado")
    
    cursor.execute("DELETE FROM secretos WHERE id = ?", (secreto_id,))
    conn.commit()
    conn.close()
    return {"mensaje": f"Secreto con ID {secreto_id} eliminado de manera definitiva"}


# ----------------- ENDPOINTS AUXILIARES -----------------

# Obtener listado de capítulos para rellenar los selectores dinámicos del formulario
@app.get("/capitulos")
def obtener_capitulos():
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM capitulos")
    filas = cursor.fetchall()
    conn.close()
    return [dict(fila) for fila in filas]


# ----------------- SERVIR INTERFAZ GRÁFICA (FRONTEND) -----------------

# Monta la carpeta "frontend" en la raíz del servidor.
# Al entrar a http://127.0.0 cargará automáticamente tu 'index.html'.
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")