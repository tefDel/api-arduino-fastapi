from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import time

app = FastAPI()

# Permitir acceso desde CodeSandbox
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar esto en producción si es necesario
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Memoria temporal para guardar los últimos valores
ULTIMOS_DATOS = []
MAX_PUNTOS = 100

# Esquema de datos recibidos
class DatoDistancia(BaseModel):
    timestamp: float
    distancia: float

@app.post("/upload")
def recibir_dato(dato: DatoDistancia):
    ULTIMOS_DATOS.append(dato.dict())
    if len(ULTIMOS_DATOS) > MAX_PUNTOS:
        ULTIMOS_DATOS.pop(0)
    return {"mensaje": "Dato recibido"}

@app.get("/distancias")
def get_distancias():
    return {
        "valores": [p["distancia"] for p in ULTIMOS_DATOS],
        "timestamps": [p["timestamp"] for p in ULTIMOS_DATOS],
    }

@app.get("/status")
def get_status():
    return {"estado": "conectado"}
