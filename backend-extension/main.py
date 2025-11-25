import os
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI(title="Punto de Extensión HSI")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
templates_path = os.path.join(BASE_DIR, "templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(directory=templates_path)

HSI_BASE_URL = "https://hsi-dev.nubecenter.com.ar/api"


# --- DATOS HARDCODEADOS (MIGRACIÓN DE ANGULAR) ---
OBJETIVOS_DATA = [
    {
        "id": 1,
        "name": "Identificación y accesibilidad de la población a cargo",
        "type": "flowchart",
        "miniature1": "/static/images/1.png",
        "pdfDR": "/static/pdfs/1.pdf",
    },
    {
        "id": 2,
        "name": "Reducción de la morbimortalidad materno infantil",
        "type": "objective",
        "children": [
            {
                "id": 2.1,
                "name": "Persona gestante",
                "type": "flowchart",
                "miniature1": "/static/images/2-a.png",
                "pdfDR": "/static/pdfs/2-A.pdf",
            },
            {
                "id": 2.2,
                "name": "Control de niños menores de 3 años",
                "type": "flowchart",
                "miniature1": None,
                "pdfDR": None,
            },
        ],
    },
    {
        "id": 3,
        "name": "Salud de la niñez y adolescencia",
        "type": "objective",
        "children": [
            {
                "id": 3.1,
                "name": "Control escolar - Crecer sanos",
                "type": "flowchart",
                "miniature1": "/static/images/3-a.png",
                "pdfDR": "/static/pdfs/3-A.pdf",
            },
            {
                "id": 3.2,
                "name": "Prevención y asistencia en adolescentes",
                "type": "flowchart",
                "miniature1": "/static/images/3-b.png",
                "pdfDR": "/static/pdfs/3-B.pdf",
            },
        ]
    },
    {
        "id": 4,
        "name": "Salud del adulto y adulto mayor",
        "type": "objective",
        "children": [
            {
                "id": 4.1,
                "name": "Atención a la persona adulta",
                "type": "flowchart",
                "miniature1": "/static/images/4-a.png",
                "pdfDR": "/static/pdfs/4-A.pdf",
            },
            {
                "id": 4.2,
                "name": "Atención a la persona mayor en PNA",
                "type": "flowchart",
                "miniature1": "/static/images/4-b.png",
                "pdfDR": "/static/pdfs/4-B.pdf",
            },
        ],
    },
    {
        "id": 5,
        "name": "Prevención y atención de ECNT",
        "type": "objective",
        "children": [
            {
                "id": 5.1,
                "name": "Atención de HTA en adultos",
                "type": "flowchart",
                "miniature1": "/static/images/5-a.png",
                "pdfDR": "/static/pdfs/5-A.pdf",
            },
            {
                "id": 5.2,
                "name": "Pesquisa, atención y diabetes en el adulto",
                "type": "category",
                "children": [
                     {
                        "id": 5.21,
                        "name": "Pesquisa, Diagnóstico y Tratamiento",
                        "type": "flowchart",
                        "miniature1": "/static/images/5-b-a.png",
                        "pdfDR": "/static/pdfs/5-B-A.pdf",
                    },
                    {
                        "id": 5.22,
                        "name": "Seguimiento y Complicaciones",
                        "type": "flowchart",
                        "miniature1": "/static/images/5-b-b.png",
                        "pdfDR": "/static/pdfs/5-B-B.pdf",
                    },
                ]
            },
            {
                "id": 5.3,
                "name": "Diagnóstico, tratamiento y seguimiento de EPOC",
                "type": "flowchart",
                "miniature1": "/static/images/5-c.png",
                "pdfDR": "/static/pdfs/5-C.pdf",
            },
        ],
    },
    {
        "id": 6,
        "name": "Prevención oportuna del cáncer en adulto",
        "type": "objective",
        "children": [
            {
                "id": 6.11,
                "name": "Cáncer colorrectal",
                "type": "flowchart",
                "miniature1": "/static/images/6-a.png",
                "pdfDR": "/static/pdfs/6-A.pdf",
            },
            {
                "id": 6.2,
                "name": "Cáncer cervicouterino",
                "type": "flowchart",
                "miniature1": "/static/images/6-b.png",
                "pdfDR": "/static/pdfs/6-B.pdf",
            },
            {
                "id": 6.3,
                "name": "Cáncer de mama",
                "type": "flowchart",
                "miniature1": "/static/images/6-c.png",
                "pdfDR": "/static/pdfs/6-C.pdf",
            },
        ],
    },
    {
        "id": 7,
        "name": "Salud mental",
        "type": "objective",
        "children": [
            {
                "id": 7.1,
                "name": "Primer nivel de atención",
                "type": "category",
                "children": [
                    {
                        "id": 7.11,
                        "name": "Diagnóstico, tratamiento y seguimiento de intento de suicidio",
                        "type": "flowchart",
                        "miniature1": "/static/images/7-a-a.png",
                        "pdfDR": "/static/pdfs/7-A-A.pdf",
                    }
                ]
            },
            {
                "id": 7.2,
                "name": "Hospital Enrique Vera Barros",
                "type": "category",
                "children": [
                    {
                        "id": 7.21,
                        "name": "Servicio de salud mental",
                        "type": "flowchart",
                        "miniature1": "/static/images/7-b-a.png",
                        "pdfDR": "/static/pdfs/7-B-A.pdf",
                    },
                    {
                        "id": 7.22,
                        "name": "Servicio de adolescencia",
                        "type": "flowchart",
                        "miniature1": "/static/images/7-b-b.png",
                        "pdfDR": "/static/pdfs/7-B-B.pdf",
                    },
                    {
                        "id": 7.23,
                        "name": "Servicio de psicología",
                        "type": "flowchart",
                        "miniature1": None,
                        "pdfDR": None,
                    },
                ]
            },
            {
                "id": 7.3,
                "name": "Hospital de la madre y el niño",
                "type": "category",
                "children": [
                    {
                        "id": 7.31,
                        "name": "Servicio de salud mental",
                        "type": "flowchart",
                        "miniature1": "/static/images/7-c-a.png",
                        "pdfDR": "/static/pdfs/7-C-A.pdf",
                    },
                ]
            },
        ],
    },
    {
        "id": 8,
        "name": "Prevención y atención de enfermedades transmisibles",
        "type": "objective",
        "children": [
            {
                "id": 8.1,
                "name": "HIV",
                "type": "flowchart",
                "miniature1": "/static/images/8-a.png",
                "pdfDR": "/static/pdfs/8-A.pdf",
            },
            {
                "id": 8.21,
                "name": "Sífilis",
                "type": "flowchart",
                "miniature1": "/static/images/8-b.png",
                "pdfDR": "/static/pdfs/8-B.pdf",
            },
            {
                "id": 8.31,
                "name": "Tuberculosis",
                "type": "flowchart",
                "miniature1": "/static/images/8-c.png",
                "pdfDR": "/static/pdfs/8-C.pdf",
            },
            {
                "id": 8.41,
                "name": "Chagas",
                "type": "flowchart",
                "miniature1": "/static/images/8-d.png",
                "pdfDR": "/static/pdfs/8-D.pdf",
            },
        ],
    },
    {
        "id": 9,
        "name": "Atención odontológica",
        "type": "flowchart",
        "category": "transversal",
        "miniature1": "/static/images/ODON-TRANSVERSAL.png",
        "pdfDR": "/static/pdfs/ODON-TRANSVERSAL.pdf",
    },
    {
        "id": 10,
        "name": "Actividad física",
        "type": "flowchart",
        "category": "transversal",
        "miniature1": "/static/images/ACT_FISICA_TRANSVERSAL..png",
        "pdfDR": "/static/pdfs/ACT_FISICA_TRANSVERSAL.pdf",
    },
    {
        "id": 11,
        "name": "Atención nutricional",
        "type": "flowchart",
        "category": "transversal",
        "miniature1": "/static/images/NUTRI-TRANSVERSAL-SOBREPESO.png",
        "pdfDR": "/static/pdfs/NUTRI-TRANSVERSAL-SOBREPESO.pdf",
    },
]


# --- LÓGICA DE VALIDACIÓN Y OBTENCIÓN DE USUARIO ---
def obtener_usuario_hsi(token: str):
    endpoint = f"{HSI_BASE_URL}/account/info"
    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "*/*"
    }
    
    print(f"📡 [DEBUG] Intentando conectar a: {endpoint}") 
    
    try:
        response = requests.get(endpoint, headers=headers, timeout=5)
        print(f"📡 [DEBUG] Respuesta HSI: {response.status_code}") 
        if response.status_code == 200:
            data = response.json()
            print(f"📡 [DEBUG] Datos recibidos: {data}") 
            return data
        else:
            print(f"⛔ [ERROR] Token rechazado: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"⛔ [ERROR] Excepción conectando: {e}")
        return None

# --- ENDPOINT DEL DASHBOARD ---
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, t: str = Query(..., description="Token de autenticación")):
    
    # 1. VALIDAR TOKEN Y OBTENER USUARIO REAL
    datos_usuario = obtener_usuario_hsi(t)
    
    if not datos_usuario:
        return """
        <html>
            <body style="background-color: #ffebee; font-family: sans-serif; text-align: center; padding: 50px;">
                <h1 style="color: #c62828;">⛔ Acceso Denegado</h1>
                <p>No se pudo validar su sesión con el HSI.</p>
                <p><small>Verifique que su sesión en HSI esté activa.</small></p>
            </body>
        </html>
        """

    nombre_completo = "Usuario HSI"
    user_id = datos_usuario.get("id", "Unknown")
    
    if "personDto" in datos_usuario:
        nombre = datos_usuario["personDto"].get("firstName", "")
        apellido = datos_usuario["personDto"].get("lastName", "")
        nombre_completo = f"{nombre} {apellido}".strip()

    objetivos_principales = [item for item in OBJETIVOS_DATA if item['id'] < 9]
    rutas_transversales = [item for item in OBJETIVOS_DATA if item['id'] >= 9]

  
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "token": t,
        "usuario": {
            "id": user_id,
            "nombre": nombre_completo,
            "raw": datos_usuario
        },
        "objetivos": objetivos_principales,
        "transversales": rutas_transversales
    })

# Ruta de salud para Docker
@app.get("/")
def health_check():
    return {"status": "online", "service": "Extension HSI Python", "version": "2.1.0"}