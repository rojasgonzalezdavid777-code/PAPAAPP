from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def saludar():
    return "HOLA API"

@app.get("/crear_agricultor")
def create_agricultor():
    return "Cambiar esto por la funcionalidad"