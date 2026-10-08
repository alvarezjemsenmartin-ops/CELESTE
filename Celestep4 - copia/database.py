import sqlite3

DATABASE_NAME = "celeste.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS capitulos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            numero INTEGER NOT NULL UNIQUE,
            fresas_total INTEGER NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS secretos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            capitulo_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            tipo_coleccionable TEXT NOT NULL, -- Fresa, Casete, Corazon
            lado TEXT NOT NULL,              -- A, B, C
            ubicacion_detalles TEXT,
            FOREIGN KEY (capitulo_id) REFERENCES capitulos (id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM capitulos")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO capitulos (nombre, numero, fresas_total) VALUES ('Forsaken City', 1, 20)")
        cursor.execute("INSERT INTO capitulos (nombre, numero, fresas_total) VALUES ('Old Site', 2, 18)")
        
        cursor.execute("INSERT INTO secretos (capitulo_id, nombre, tipo_coleccionable, lado, ubicacion_detalles) VALUES (1, 'Fresa del inicio', 'Fresa', 'A', 'Al inicio del nivel, vuela hacia la izquierda.')")
        cursor.execute("INSERT INTO secretos (capitulo_id, nombre, tipo_coleccionable, lado, ubicacion_detalles) VALUES (1, 'Cassette del Capitulo 1', 'Casete', 'A', 'En la sala del bloque oculto cruzando la pantalla superior.')")
        
    conn.commit()
    conn.close()