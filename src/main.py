from fastapi import FastAPI, HTTPException, Header
import configcatclient

app = FastAPI()

# Inicializamos ConfigCat 
configcat_client = configcatclient.get('configcat-sdk-1/gSHfCDv24UyHMtp50P-3xg/y4b-lUQex0iEVs3sK9x6Lw')

# Base de datos en memoria para las etiquetas y tareas
tags_db = []
tasks_db = []

@app.get("/")
def read_root():
    return {"status": "API Gestor de Tareas OK"}

# --- TICKET 1: Modelo Tag + CRUD ---
@app.post("/tags/")
def create_tag(name: str, color: str):
    # Validamos si el feature toggle está encendido
    is_tags_enabled = configcat_client.get_value("tags_enabled", False)
    if not is_tags_enabled:
        raise HTTPException(status_code=403, detail="Feature tags_enabled está apagado")
    
    new_tag = {"id": len(tags_db) + 1, "name": name, "color": color}
    tags_db.append(new_tag)
    return new_tag

@app.get("/tags/")
def get_tags():
    is_tags_enabled = configcat_client.get_value("tags_enabled", False)
    if not is_tags_enabled:
        raise HTTPException(status_code=403, detail="Feature tags_enabled está apagado")
    
    return tags_db

# --- TICKET 2: Permitir asignar una etiqueta a una tarea (flag al 10%) ---
@app.post("/tasks/")
def create_task(title: str, tag_id: int = None, user_id: str = Header(default="anonymous")):
    new_task = {"id": len(tasks_db) + 1, "title": title, "tag_id": None}
    
    if tag_id is not None:
        # Para que el "10%" funcione, necesitamos identificar al usuario
        from configcatclient.user import User
        user = User(user_id)
        is_assign_enabled = configcat_client.get_value("assign_tags_enabled", False, user)
        
        if not is_assign_enabled:
            raise HTTPException(status_code=403, detail="Feature assign_tags_enabled está apagado para tu usuario")
            
        # Verificamos si el tag existe
        if not any(t["id"] == tag_id for t in tags_db):
            raise HTTPException(status_code=404, detail="La etiqueta no existe")
            
        new_task["tag_id"] = tag_id
        
    tasks_db.append(new_task)
    return new_task

@app.get("/tasks/")
def get_tasks(tag_id: int = None):
    if tag_id is not None:
        return [task for task in tasks_db if task["tag_id"] == tag_id]
    return tasks_db

# Mantengo tu calculadora original para que no se rompa nada previo
class calculator:
    def sum(self, a: int, b: int) -> int:    
        return a + b
    
    def resta(self, a: int, b: int) -> int:
        return a - b