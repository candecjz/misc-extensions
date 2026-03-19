import os
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
from typing import Optional
from datetime import datetime

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

templates.env.auto_reload = True
templates.env.cache = None

OBJETIVOS_DATA = [
    {
        "id": 1,
        "name": "Identificación y accesibilidad de la población a cargo",
        "type": "flowchart",
        "fecha": "06/2025",
        "pdfDR": "/static/pdfs/1.pdf",
    },
    {
        "id": 2,
        "name": "Reducción de la morbimortalidad materno infantil",
        "type": "objective",
        "fecha": "12/2025",
        "children": [
            {
                "id": 2.1,
                "name": "Persona gestante",
                "type": "flowchart",
                "fecha": "09/2025",
                "pdfDR": "/static/pdfs/2-A.pdf",
            },
            {
                "id": 2.2,
                "name": "Control de niños menores de 3 años",
                "type": "flowchart",
                "fecha": "12/2025",
                "pdfDR": "/static/pdfs/2-B.pdf",
            },
            {
                "id": 2.3,
                "name": "Chagas - Transmisión vertical materno infantil",
                "type": "flowchart",
                "fecha": "11/2025",
                "pdfDR": "/static/pdfs/2-C.pdf",
            },
        ],  
    },
    {
        "id": 3,
        "name": "Salud de la niñez y adolescencia",
        "type": "objective",
        "fecha": "12/2025",
        "children": [
            {
                "id": 3.1,
                "name": "Control escolar - Crecer sanos",
                "type": "flowchart",
                "fecha": "10/2025",
                "pdfDR": "/static/pdfs/3-A.pdf",
            },
            {
                "id": 3.2,
                "name": "Control de niños menores de 10 años",
                "type": "flowchart",
                "fecha": "12/2025",
                "pdfDR": "/static/pdfs/3-B.pdf",
            },
            {
                "id": 3.3,
                "name": "Prevención y asistencia en adolescentes",
                "type": "flowchart",
                "fecha": "12/2025",
                "pdfDR": "/static/pdfs/3-C.pdf",
            },
        ],
    },
    {
        "id": 4,
        "name": "Salud del adulto y adulto mayor",
        "type": "objective",
        "fecha": "06/2025",
        "children": [
            {
                "id": 4.1,
                "name": "Atención a la persona adulta",
                "type": "flowchart",
                "fecha": "06/2025",
                "pdfDR": "/static/pdfs/4-A.pdf",
            },
            {
                "id": 4.2,
                "name": "Atención a la persona mayor en PNA",
                "type": "flowchart",
                "fecha": "06/2025",
                "pdfDR": "/static/pdfs/4-B.pdf",
            },
        ],
    },
    {
        "id": 5,
        "name": "Prevención y atención de ECNT",
        "type": "objective",
        "fecha": "01/2026",
        "children": [
            {
                "id": 5.1,
                "name": "Atención de HTA en adultos",
                "type": "flowchart",
                "fecha": "09/2025",
                "pdfDR": "/static/pdfs/5-A.pdf",
            },
            {
                "id": 5.2,
                "name": "Pesquisa, atención y diabetes en el adulto",
                "type": "category",
                "fecha": "09/2025",
                "children": [
                     {
                        "id": 5.21,
                        "name": "Pesquisa, Diagnóstico y Tratamiento",
                        "type": "flowchart",
                        "fecha": "09/2025",
                        "pdfDR": "/static/pdfs/5-B-A.pdf",
                    },
                    {
                        "id": 5.22,
                        "name": "Seguimiento y Complicaciones",
                        "type": "flowchart",
                        "fecha": "09/2025",
                        "pdfDR": "/static/pdfs/5-B-B.pdf",
                    },
                ]
            },
            {
                "id": 5.3,
                "name": "Diagnóstico, tratamiento y seguimiento de EPOC",
                "type": "flowchart",
                "fecha": "01/2026",
                "pdfDR": "/static/pdfs/5-C.pdf",
            },
        ],
    },
    {
        "id": 6,
        "name": "Prevención oportuna del cáncer en adulto",
        "type": "objective",
        "fecha": "09/2025",
        "children": [
            {
                "id": 6.1,
                "name": "Cáncer colorrectal",
                "type": "flowchart",
                "fecha": "09/2025",
                "miniature1": "/static/images/6-a.png",
                "pdfDR": "/static/pdfs/6-A.pdf",
            },
            {
                "id": 6.2,
                "name": "Cáncer cervicouterino",
                "type": "flowchart",
                "fecha": "06/2025",
                "miniature1": "/static/images/6-b.png",
                "pdfDR": "/static/pdfs/6-B.pdf",
            },
            {
                "id": 6.3,
                "name": "Cáncer de mama",
                "type": "flowchart",
                "fecha": "06/2025",
                "miniature1": "/static/images/6-c.png",
                "pdfDR": "/static/pdfs/6-C.pdf",
            },
        ],
    },
    {
        "id": 7,
        "name": "Salud mental",
        "type": "objective",
        "fecha": "01/2026",
        "children": [
            {
                "id": 7.1,
                "name": "Primer nivel de atención",
                "type": "category",
                "fecha": "09/2025",
                "children": [
                    {
                        "id": 7.11,
                        "name": "Diagnóstico, tratamiento y seguimiento de intento de suicidio y consumo problemático",
                        "type": "flowchart",
                        "fecha": "09/2025",
                        "pdfDR": "/static/pdfs/7-A-A.pdf",
                    }
                ]
            },
            {
                "id": 7.2,
                "name": "Hospital Enrique Vera Barros",
                "type": "category",
                "fecha": "01/2026",
                "children": [
                    {
                        "id": 7.21,
                        "name": "Servicio de salud mental",
                        "type": "flowchart",
                        "fecha": "06/2025",
                        "pdfDR": "/static/pdfs/7-B-A.pdf",
                    },
                    {
                        "id": 7.22,
                        "name": "Servicio de adolescencia",
                        "type": "flowchart",
                        "fecha": "06/2025",
                        "pdfDR": "/static/pdfs/7-B-B.pdf",
                    },
                    {
                        "id": 7.23,
                        "name": "Servicio de psicología",
                        "type": "flowchart",
                        "fecha": "01/2026",
                        "pdfDR": "/static/pdfs/7-B-C.pdf", 
                    },
                ]
            },
            {
                "id": 7.3,
                "name": "Hospital de la madre y el niño",
                "type": "category",
                "fecha": "06/2025",
                "children": [
                    {
                        "id": 7.31,
                        "name": "Servicio de salud mental",
                        "type": "flowchart",
                        "fecha": "06/2025",
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
        "fecha": "09/2025",
        "children": [
            {
                "id": 8.1,
                "name": "HIV",
                "type": "flowchart",
                "fecha": "09/2025",
                "pdfDR": "/static/pdfs/8-A.pdf",
            },
            {
                "id": 8.2,
                "name": "Sífilis",
                "type": "flowchart",
                "fecha": "09/2025",
                "pdfDR": "/static/pdfs/8-B.pdf",
            },
            {
                "id": 8.3,
                "name": "Tuberculosis",
                "type": "flowchart",
                "fecha": "06/2025",
                "pdfDR": "/static/pdfs/8-C.pdf",
            }
        ],
    },
    {
        "id": 9,
        "name": "Garantía de Derechos de Accesibilidad en Salud",
        "type": "objective",
        "fecha": None,
        "children": [
            {
                "id": 9.1,
                "name": "Persona con Discapacidad",
                "type": "flowchart",
                "fecha": None,
                "pdfDR": None,
            },
            {
                "id": 9.2,
                "name": "Violencia de Género",
                "type": "flowchart",
                "fecha": None,
                "pdfDR": None,
            }
        ],
    },
            {
                "id": 10,
                "name": "Atención odontológica",
                "type": "flowchart",
                "category": "transversal",
                "fecha": "09/2025",
                "pdfDR": "/static/pdfs/ODON-TRANSVERSAL.pdf",
            },
            {
                "id": 11,
                "name": "Actividad física",
                "type": "flowchart",
                "category": "transversal",
                "fecha": "06/2025",
                "pdfDR": "/static/pdfs/ACT_FISICA_TRANSVERSAL.pdf",
            },
            {
                "id": 12,
                "name": "Atención nutricional",
                "type": "flowchart",
                "fecha": "06/2025",
                "category": "transversal",
                "children": [
                    {
                        "id": 12.1,
                        "name": "Sobrepeso y obesidad",
                        "type": "flowchart",
                        "fecha": "06/2025",
                        "pdfDR": "/static/pdfs/NUTRI-TRANSVERSAL-SOBREPESO.pdf",                    
                    },
                    {
                        "id": 12.2,
                        "name": "Celiaquía",
                        "type": "flowchart",
                        "pdfDR":None,
                    }
                ], 
            },
            {
                "id": 13,
                "name": "Enfermería",
                "type": "objective",
                "fecha": "11/2025",
                "category": "transversal",
                "children": [
                    {
                        "id": 13.1,
                        "name": "Primer y Segundo Nivel de Atención",
                        "type": "flowchart",
                        "fecha": "11/2025",
                        "pdfDR": "/static/pdfs/ENF_TRANSVERSAL_N1_N2.pdf",
                    },
                    {
                        "id": 13.2,
                        "name": "Tercer Nivel de Atención",
                        "type": "flowchart",
                        "fecha": "11/2025",
                        "pdfDR": "/static/pdfs/ENF_TRANSVERSAL_N3.pdf",
                    }

                ]
                
            }
]

def validar_sesion(token: str) -> bool:
    if not token:
        return False
    endpoint = f"{HSI_BASE_URL}/account/info"
    headers = {"Authorization": f"Bearer {token}", "accept": "*/*"}
    try:
        response = requests.get(endpoint, headers=headers, timeout=3)
        return response.status_code == 200
    except:
        return False

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, t: Optional[str] = Query(None, description="Token opcional")):
    
    sesion_activa = validar_sesion(t)
    objetivos_principales = [item for item in OBJETIVOS_DATA if item['id'] < 10]
    rutas_transversales = [item for item in OBJETIVOS_DATA if item['id'] >= 10]

    ahora = datetime.now()
    
    def es_reciente(fecha_str):
        if not fecha_str:
            return False
        try:
            fecha_item = datetime.strptime(fecha_str, "%m/%Y")
            diferencia = ahora - fecha_item
            return 0 <= diferencia.days <= 45
        except:
            return False

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "sesion_activa": sesion_activa,
        "objetivos": objetivos_principales,
        "transversales": rutas_transversales,
        "es_reciente": es_reciente  
    })

@app.get("/")
def health_check():
    return {"status": "online"}


MOCK_LABORATORIOS = [
    {
        "Institucion": "Hospital Regional Vera Barros (SISA: 102030 | CUIT: 30-12345678-9)",
        "Fecha": "2023-10-25T08:30:00",
        "Categoria": "Laboratorio",
        "Estado de la Orden": "Completado",
        "Profesional interviniente": "Gomez, Ana Maria",
        "Tipo de Solicitud": "Rutina",
        "Origen de la Solicitud": "Consultorio Externo",
        "Nombre del Paciente": "Perez, Juan",
        "Tipo de Documento": "DNI",
        "Numero de Documento": "41284061",
        "Obra Social": "APOS",
        "Numero de Afiliado": "123456789",
        "Profesional solicitante": "Dr. House, Gregory",
        "Tipo de Documento profesional": "DNI",
        "Numero de Documento profesional": "20123456",
        "profesion": "Médico Clínico",
        "Licencia": "MP 1234",
        "Nota": "Paciente en ayunas 8hs",
        "Fecha de Emision": "2023-10-25T11:45:00",
        "Nombre del Estudio": "Hemograma completo",
        "Resultados (Cantidad y Unidad)": "Glóbulos rojos 4.5 millones/uL | Glóbulos blancos 7000 /uL | Plaquetas 250000 /uL",
        "Notas adicionales": "Valores dentro de los parámetros normales",
        "Problema Asociado": "Control de salud de rutina [Estado: Activo, Verificación: Confirmado, Severidad: Leve, Tipo: Problema] Fecha: 2023-10-01"
    },
    {
        "Institucion": "Hospital de la Madre y el Niño (SISA: 405060 | CUIT: 30-98765432-1)",
        "Fecha": "2024-01-15T09:15:00",
        "Categoria": "Laboratorio",
        "Estado de la Orden": "Completado",
        "Profesional interviniente": "Lopez, Carlos",
        "Tipo de Solicitud": "Urgencia",
        "Origen de la Solicitud": "Guardia",
        "Nombre del Paciente": "Perez, Juan",
        "Tipo de Documento": "DNI",
        "Numero de Documento": "41284061",
        "Obra Social": "APOS",
        "Numero de Afiliado": "123456789",
        "Profesional solicitante": "Dra. Grey, Meredith",
        "Tipo de Documento profesional": "DNI",
        "Numero de Documento profesional": "25987654",
        "profesion": "Cirujano General",
        "Licencia": "MP 5678",
        "Nota": "Pre-quirúrgico de urgencia",
        "Fecha de Emision": "2024-01-15T10:30:00",
        "Nombre del Estudio": "Glucemia",
        "Resultados (Cantidad y Unidad)": "Glucosa 95 mg/dL",
        "Notas adicionales": "Muestra levemente hemolizada",
        "Problema Asociado": "Sospecha de apendicitis aguda [Estado: Activo, Verificación: Confirmado, Severidad: Moderada, Tipo: Problema] Fecha: 2024-01-15"
    },
    {
        "Institucion": "Centro Primario de Salud San Vicente",
        "Fecha": "2024-02-20T10:00:00",
        "Categoria": "Laboratorio",
        "Estado de la Orden": "Pendiente",
        "Profesional interviniente": "Martinez, Sofia",
        "Tipo de Solicitud": "Control",
        "Origen de la Solicitud": "Consultorio Externo",
        "Nombre del Paciente": "Gomez, Laura",
        "Tipo de Documento": "DNI",
        "Numero de Documento": "35123456",
        "Obra Social": "PAMI",
        "Numero de Afiliado": "987654321",
        "Profesional solicitante": "Dr. Fernandez, Luis",
        "Tipo de Documento profesional": "DNI",
        "Numero de Documento profesional": "18765432",
        "profesion": "Endocrinólogo",
        "Licencia": "MP 4321",
        "Nota": "",
        "Fecha de Emision": "2024-02-20T10:05:00",
        "Nombre del Estudio": "Perfil Tiroideo (TSH, T4L)",
        "Resultados (Cantidad y Unidad)": "Sin resultados",
        "Notas adicionales": "",
        "Problema Asociado": "Hipotiroidismo [Estado: Crónico, Verificación: Confirmado, Severidad: Moderada, Tipo: Diagnóstico] Fecha: 2020-05-10"
    }
]

@app.get("/api/laboratorios/{dni}")
async def api_laboratorios(dni: str):
    """
    Endpoint que recibe un DNI en la URL y devuelve los laboratorios del paciente.
    Filtra los datos hardcodeados para simular una consulta real.
    """
    resultados_paciente = [
        registro for registro in MOCK_LABORATORIOS 
        if registro["Numero de Documento"] == dni
    ]
    
    return {
        "status": "success",
        "paciente_dni": dni,
        "total_registros": len(resultados_paciente),
        "data": resultados_paciente
    }