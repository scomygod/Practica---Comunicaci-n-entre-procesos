from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Inicializamos la aplicación
app = FastAPI(title="API de Tareas")

# Simulación de base de datos en memoria (Diccionario)
db_tareas = {}
contador_id = 1

# Modelo de datos que esperamos recibir en el POST (cuerpo JSON)
class TareaCreate(BaseModel):
    titulo: str
    descripcion: str

# 1. GET /tareas -> Retorna lista de todas las tareas
@app.get("/tareas")
def listar_tareas():
    # Retornamos los valores del diccionario como una lista
    return list(db_tareas.values())

# 2. GET /tareas/{id} -> Retorna una tarea por ID o 404
@app.get("/tareas/{id_tarea}")
def obtener_tarea(id_tarea: int):
    if id_tarea not in db_tareas:
        raise HTTPException(status_code=404, detail="Error: Tarea no encontrada")
    return db_tareas[id_tarea]

# 3. POST /tareas -> Crea nueva tarea
@app.post("/tareas", status_code=201)
def crear_tarea(tarea: TareaCreate):
    global contador_id
    if not tarea.titulo:
        raise HTTPException(status_code=400, detail="El título es obligatorio")

    nueva_tarea = {
        "id": contador_id,
        "titulo": tarea.titulo,
        "descripcion": tarea.descripcion,
        "estado": "pendiente"
    }
    db_tareas[contador_id] = nueva_tarea
    contador_id += 1
    return nueva_tarea

# 4. PUT /tareas/{id} -> Actualiza el estado a "completada"
@app.put("/tareas/{id_tarea}")
def completar_tarea(id_tarea: int):
    if id_tarea not in db_tareas:
        raise HTTPException(status_code=404, detail="Error: No se puede completar, tarea inexistente")

    db_tareas[id_tarea]["estado"] = "completada"
    return db_tareas[id_tarea]

# 5. DELETE /tareas/{id} -> Elimina una tarea por ID
@app.delete("/tareas/{id_tarea}")
def eliminar_tarea(id_tarea: int):
    if id_tarea not in db_tareas:
        raise HTTPException(status_code=404, detail="Error: No se puede eliminar, tarea inexistente")

    del db_tareas[id_tarea]
    return {"mensaje": f"Tarea {id_tarea} eliminada correctamente"}
