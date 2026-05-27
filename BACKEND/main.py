# paquetes uvicorn y fast api
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import json
import os
from datetime import datetime

app = FastAPI()

@app.get("/")
def saludar():
    return "Hola API"

@app.get("/crear_agricultor", response_class=HTMLResponse)
def mostrar_formulario():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Registrar Agricultor</title>
        <meta charset="UTF-8">
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 50px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 500px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            h1 {
                text-align: center;
                color: #333;
            }
            input, textarea {
                width: 100%;
                padding: 10px;
                margin: 10px 0 20px 0;
                border: 1px solid #ddd;
                border-radius: 5px;
                box-sizing: border-box;
            }
            button {
                width: 100%;
                padding: 12px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background-color: #45a049;
            }
            .mensaje {
                margin-top: 20px;
                padding: 10px;
                border-radius: 5px;
                text-align: center;
            }
            .exito {
                background-color: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .error {
                background-color: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📋 Registrar Agricultor</h1>
            <form id="formulario">
                <label>ID (Identificador único):</label>
                <input type="number" id="id" required>
                
                <label>Cédula:</label>
                <input type="text" id="cedula" required>
                
                <label>Nombre Completo:</label>
                <input type="text" id="nombre" required>
                
                <label>Área de papa (hectáreas):</label>
                <input type="number" step="0.01" id="Area" required>
                
                <label>Variedad de papa:</label>
                <input type="text" id="Cultivo" required>
                
                <label>Inversión (USD):</label>
                <input type="number" step="0.01" id="inversion" required>
                
                <label>Fecha de siembra:</label>
                <input type="date" id="Fecha" required>
                
                <label>Ubicación (Polígono GeoJSON):</label>
                <textarea id="Ubicacion_cultivo" rows="4" placeholder='{"type":"Polygon","coordinates":[[[-75.574,6.244],[-75.573,6.244],[-75.573,6.245],[-75.574,6.245],[-75.574,6.244]]]}' required></textarea>
                
                <button type="submit">💾 Guardar Agricultor</button>
            </form>
            <div id="mensaje"></div>
        </div>

        <script>
            document.getElementById('formulario').onsubmit = async (e) => {
                e.preventDefault();
                
                // Validar que el polígono sea JSON válido
                let ubicacion;
                try {
                    ubicacion = JSON.parse(document.getElementById('Ubicacion_cultivo').value);
                } catch(e) {
                    document.getElementById('mensaje').innerHTML = '<div class="mensaje error">❌ Error: El polígono no es un JSON válido</div>';
                    return;
                }
                
                const datos = {
                    id: parseInt(document.getElementById('id').value),
                    cedula: document.getElementById('cedula').value,
                    nombre: document.getElementById('nombre').value,
                    Area: parseFloat(document.getElementById('Area').value),
                    Cultivo: document.getElementById('Cultivo').value,
                    inversion: parseFloat(document.getElementById('inversion').value),
                    Fecha: document.getElementById('Fecha').value,
                    Ubicacion_cultivo: ubicacion
                };
                
                const respuesta = await fetch('/guardar_agricultor', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(datos)
                });
                
                const resultado = await respuesta.json();
                
                if (respuesta.ok) {
                    document.getElementById('mensaje').innerHTML = `<div class="mensaje exito">✅ ${resultado.mensaje}<br>📁 Archivo: ${resultado.archivo}</div>`;
                    document.getElementById('formulario').reset();
                } else {
                    document.getElementById('mensaje').innerHTML = `<div class="mensaje error">❌ Error: ${resultado.detail}</div>`;
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/guardar_agricultor")
async def guardar_agricultor(datos: dict):
    try:
        # Ruta donde guardar el archivo
        ruta_carpeta = r"C:\Users\Estudiantes\Downloads\PapaApp\Backend"
        
        # Crear nombre del archivo
        nombre_archivo = f"agricultor_{datos['cedula']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
        
        # Agregar fecha de creación al diccionario
        datos['fecha_registro'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Guardar el archivo JSON
        with open(ruta_completa, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        
        return {
            "mensaje": "Datos guardados exitosamente",
            "archivo": nombre_archivo,
            "ruta": ruta_completa
        }
    except Exception as e:
        return {"error": str(e)}