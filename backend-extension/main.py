import os
import requests
from typing import Optional, List
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from io import BytesIO
from pydantic import BaseModel, Field
from pdf_generator import generate_lab_pdf

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

# --- DATOS MOCK ---
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
        "fecha": "04/2026",
        "children": [
            {
                "id": 6.1,
                "name": "Cáncer colorrectal",
                "type": "flowchart",
                "fecha": "09/2025",
                "pdfDR": "/static/pdfs/6-A.pdf",
            },
            {
                "id": 6.2,
                "name": "Cáncer cervicouterino",
                "type": "flowchart",
                "fecha": "06/2025",
                "pdfDR": "/static/pdfs/6-B.pdf",
            },
            {
                "id": 6.3,
                "name": "Cáncer de mama",
                "type": "flowchart",
                "fecha": "04/2026",
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
     },
    {
        "id": 14,
        "name": "Salud sexual y reproductiva",
        "type": "flowchart",
        "category": "transversal",
        "fecha": "04/2026",
        "pdfDR": "/static/pdfs/SALUD_SEXUAL_REPRODUCTIVA.pdf",
    },
]

MOCK_LABORATORIOS = [
    {
        "id": "lab_101",
        "Nombre del Paciente": "Perez, Juan",
        "Numero de Documento": "41284061",
        "Nombre del Estudio": "Hemograma completo",
        "Problema Asociado": "Control de salud de rutina",
        "pdf_file": "hemograma_test.pdf",
        # Campos estructurados para generación de PDF
        "institucion": "Hospital Regional Enrique Vera Barros",
        "paciente_nombre": "Perez, Juan",
        "paciente_dni": "41284061",
        "origen": "AMBULATORIO",
        "solicitante": "Dra. Ana Maria Gomez",
        "validador": "Bioq. Carlos Lopez - MP 5678",
        "orden": "73327",
        "fecha": "25/10/2023",
        "hora": "09:30",
        "paciente_edad": "27",
        "estudio_nombre": "Hemograma completo",
        "resultados": [
            {"name": "Glóbulos Rojos", "value": "4.500.000", "unit": "/uL", "reference": "4.000.000 - 5.500.000", "status": "Normal"},
            {"name": "Hemoglobina", "value": "14.2", "unit": "g/dL", "reference": "12.0 - 16.0", "status": "Normal"},
            {"name": "Hematocrito", "value": "42", "unit": "%", "reference": "37 - 48", "status": "Normal"},
            {"name": "Glóbulos Blancos", "value": "7.000", "unit": "/uL", "reference": "4.000 - 11.000", "status": "Normal"},
            {"name": "Plaquetas", "value": "250.000", "unit": "/uL", "reference": "150.000 - 450.000", "status": "Normal"}
        ],
        "observaciones": "Valores dentro de los parámetros normales de referencia."
    },
    {
        "id": "lab_102",
        "Nombre del Paciente": "Lopez, Maxi",
        "Numero de Documento": "22333444",
        "Nombre del Estudio": "Glucemia",
        "Problema Asociado": "Sospecha de apendicitis aguda",
        "pdf_file": "glucemia_test.pdf",
        # Campos estructurados para generación de PDF
        "institucion": "Hospital de la Madre y el Niño",
        "paciente_nombre": "Lopez, Maxi",
        "paciente_dni": "22333444",
        "origen": "Guardia",
        "solicitante": "Dra. Meredith Grey",
        "validador": "Bioq. Carlos Lopez - MP 5678",
        "orden": "73328",
        "fecha": "15/01/2024",
        "hora": "12:08",
        "paciente_edad": "15",
        "estudio_nombre": "Glucemia",
        "resultados": [
            {"name": "Glucosa en sangre", "value": "95", "unit": "mg/dL", "reference": "70 - 110", "status": "Normal"}
        ],
        "tipo_solicitud": "Urgencia - Pre-quirúrgico",
        "observaciones": "Muestra levemente hemolizada. Resultados informados a cirugía."
    },
    {
        "id": "lab_103",
        "Nombre del Paciente": "Gomez, Laura",
        "Numero de Documento": "35123456",
        "Nombre del Estudio": "Perfil Tiroideo",
        "Problema Asociado": "Hipotiroidismo",
        "pdf_file": "tiroideo_test.pdf",
        # Campos estructurados para generación de PDF
        "institucion": "Centro Primario de Salud San Vicente",
        "paciente_nombre": "Gomez, Laura",
        "paciente_dni": "35123456",
        "origen": "AMBULATORIO",
        "solicitante": "Dra. Sofia Martinez",
        "validador": "Bioq. Sofia Martinez - MP 1212",
        "orden": "73329",
        "fecha": "20/02/2024",
        "hora": "08:15",
        "paciente_edad": "35",
        "estudio_nombre": "Perfil Tiroideo",
        "resultados": [
            {"name": "TSH", "value": "4.2", "unit": "mUI/L", "reference": "0.4 - 4.0", "status": "Alto"},
            {"name": "T4 Libre", "value": "0.9", "unit": "ng/dL", "reference": "0.8 - 1.9", "status": "Normal"}
        ],
        "observaciones": "Se observa TSH levemente elevada. Compatible con diagnóstico de Hipotiroidismo en seguimiento."
    }
]

def validar_sesion(token: str) -> bool:
    if not token: return False
    headers = {"Authorization": f"Bearer {token}", "accept": "*/*"}
    try:
        response = requests.get(f"{HSI_BASE_URL}/account/info", headers=headers, timeout=3)
        return response.status_code == 200
    except: return False

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, t: Optional[str] = Query(None)):
    sesion_activa = validar_sesion(t)
    objetivos_principales = [item for item in OBJETIVOS_DATA if item['id'] < 10]
    rutas_transversales = [item for item in OBJETIVOS_DATA if item['id'] >= 10]
    ahora = datetime.now()
    
    def es_reciente(fecha_str):
        if not fecha_str: return False
        try:
            fecha_item = datetime.strptime(fecha_str, "%m/%Y")
            return 0 <= (ahora - fecha_item).days <= 45
        except: return False

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "sesion_activa": sesion_activa,
        "objetivos": objetivos_principales,
        "transversales": rutas_transversales,
        "es_reciente": es_reciente  
    })

def call_hsi_api(endpoint: str, token: str, method: str = "GET", params: dict = None, stream: bool = False):
    url = f"{HSI_BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "*/*"
    }
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params, stream=stream, timeout=10)
        else:
            response = requests.post(url, headers=headers, json=params, stream=stream, timeout=10)
        return response
    except Exception as e:
        print(f"Error calling HSI API {url}: {e}")
        return None

@app.get("/api/laboratorios/{dni}")
async def api_laboratorios(
    dni: str, 
    authorization: Optional[str] = Header(None),
    x_institution_id: Optional[str] = Header(None)
):
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]

    # Si no se proporciona token de autorización, regresamos los datos mock locales como fallback
    if not token:
        resultados = [r for r in MOCK_LABORATORIOS if r["Numero de Documento"] == dni]
        return {
            "total_registros": len(resultados),
            "data": resultados
        }

    # 1. Obtener el institution_id
    institution_id = x_institution_id
    if not institution_id:
        # Intentar obtenerlo desde los permisos del usuario
        perm_res = call_hsi_api("/account/permissions", token)
        if perm_res and perm_res.status_code == 200:
            perm_data = perm_res.json()
            assignments = perm_data.get("roleAssignments", [])
            if assignments:
                institution_id = assignments[0].get("institutionId")
    
    if not institution_id:
        # Fallback si no hay institutionId disponible
        institution_id = "1"

    # 2. Consultar detalles de la institución para obtener el refsetCode (sisaCode)
    refset_code = str(institution_id) # default fallback
    inst_res = call_hsi_api(f"/public-api/institution/{institution_id}", token)
    if inst_res and inst_res.status_code == 200:
        inst_data = inst_res.json()
        refset_code = inst_data.get("sisaCode") or inst_data.get("refsetCode") or inst_data.get("code") or str(institution_id)

    # 3. Buscar el paciente para obtener su nombre completo
    patient_id = None
    patient_name = "Paciente"
    
    patient_id_res = call_hsi_api(f"/public-api/patient/identificationType/1/identificationNumber/{dni}", token)
    if patient_id_res and patient_id_res.status_code == 200:
        try:
            val = patient_id_res.json()
            if isinstance(val, dict):
                patient_id = val.get("id") or val.get("patientId")
            else:
                patient_id = val
        except:
            patient_id = patient_id_res.text.strip('"')

    if not patient_id:
        # Si no se encuentra el paciente en HSI, devolvemos 0 registros
        return {
            "total_registros": 0,
            "data": []
        }

    # Ahora obtenemos los detalles del paciente (nombre completo)
    patient_res = call_hsi_api(f"/public-api/patient/{patient_id}", token)
    if patient_res and patient_res.status_code == 200:
        patient_data = patient_res.json()
        first_name = patient_data.get("firstName", "")
        last_name = patient_data.get("lastName", "")
        if first_name or last_name:
            patient_name = f"{last_name}, {first_name}".strip(", ")

    # 4. Obtener las actividades del paciente
    activities_res = call_hsi_api(f"/public-api/institution/refset/{refset_code}/patient/{dni}/activities", token)
    if not activities_res or activities_res.status_code != 200:
        return {
            "total_registros": 0,
            "data": []
        }

    activities = activities_res.json()
    if not isinstance(activities, list):
        activities = [activities] if activities else []

    resultados = []
    
    # 5. Para cada actividad, buscar sus reportes de diagnóstico y documentos asociados
    for activity in activities:
        activity_id = activity.get("id") or activity.get("activityId")
        if not activity_id:
            continue

        # Obtener diagnóstico principal como "Problema Asociado"
        problema = "No especificado"
        diagnosticos = activity.get("diagnoses") or []
        if not isinstance(diagnosticos, list):
            diagnosticos = [diagnosticos]
            
        for diag in diagnosticos:
            snomed = diag.get("snomed", {}) if isinstance(diag, dict) else {}
            term = snomed.get("pt") or snomed.get("term") or diag.get("pt") or diag.get("term")
            if term:
                problema = term
                break

        # A. Intentar obtener reportes de diagnóstico mediante /diagnostic-report
        report_res = call_hsi_api(f"/public-api/institution/refset/{refset_code}/activity/{activity_id}/diagnostic-report", token)
        reports = []
        if report_res and report_res.status_code == 200:
            reports = report_res.json()
            if not isinstance(reports, list):
                reports = [reports] if reports else []

        for report in reports:
            report_id = report.get("id") or report.get("diagnosticReportFileId") or report.get("fileId")
            if not report_id:
                continue

            snomed_study = report.get("snomed", {})
            study_name = snomed_study.get("pt") or snomed_study.get("term") or report.get("pt") or report.get("term") or "Estudio de Laboratorio"

            resultados.append({
                "id": str(report_id),
                "Nombre del Paciente": patient_name,
                "Numero de Documento": dni,
                "Nombre del Estudio": study_name,
                "Problema Asociado": problema,
                "refsetCode": refset_code,
                "fileType": "diagnostic_report"
            })

        # B. También buscar documentos genéricos
        doc_res = call_hsi_api(f"/public-api/institution/refset/{refset_code}/activities/{activity_id}/documents-info", token)
        docs = []
        if doc_res and doc_res.status_code == 200:
            docs = doc_res.json()
            if not isinstance(docs, list):
                docs = [docs] if docs else []

        for doc in docs:
            doc_id = doc.get("id") or doc.get("documentId")
            if not doc_id:
                continue

            if any(str(r["id"]) == str(doc_id) for r in resultados):
                continue

            filename = doc.get("filename") or doc.get("name") or "Documento"
            study_name = os.path.splitext(filename)[0] if filename else "Documento de Laboratorio"

            resultados.append({
                "id": str(doc_id),
                "Nombre del Paciente": patient_name,
                "Numero de Documento": dni,
                "Nombre del Estudio": study_name,
                "Problema Asociado": problema,
                "refsetCode": refset_code,
                "fileType": "document"
            })

    return {
        "total_registros": len(resultados),
        "data": resultados
    }

@app.get("/descargar-estudio/{estudio_id}")
async def descargar_estudio(
    estudio_id: str, 
    t: Optional[str] = Query(None), 
    refset: Optional[str] = Query(None),
    type: Optional[str] = Query("diagnostic_report")
):
    if estudio_id.startswith("lab_") or not t or not refset:
        estudio = next((item for item in MOCK_LABORATORIOS if item["id"] == estudio_id), None)
        if not estudio:
            raise HTTPException(status_code=404, detail="Estudio no encontrado.")
        
        try:
            pdf_data = generate_lab_pdf(estudio)
            headers = {
                "Content-Disposition": f"inline; filename={estudio['Nombre del Estudio'].replace(' ', '_')}.pdf"
            }
            return StreamingResponse(BytesIO(pdf_data), media_type="application/pdf", headers=headers)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al generar el PDF: {str(e)}")

    if type == "document":
        url_path = f"/public-api/institution/refset/{refset}/document/{estudio_id}/download"
    else:
        url_path = f"/public-api/institution/refset/{refset}/diagnostic-report-file/{estudio_id}/download"

    res = call_hsi_api(url_path, t, stream=True)
    if not res or res.status_code != 200:
        status_code = res.status_code if res else 500
        raise HTTPException(status_code=status_code, detail="No se pudo descargar el estudio desde HSI.")

    content_type = res.headers.get("Content-Type", "application/pdf")
    
    return StreamingResponse(
        res.iter_content(chunk_size=4096),
        media_type=content_type,
        headers={
            "Content-Disposition": f"inline; filename={estudio_id}.pdf"
        }
    )

# Pydantic models for custom PDF generation
class AnalitoResult(BaseModel):
    name: str = Field(..., description="Nombre del analito (ej. TSH, Hemoglobina)")
    value: str = Field(..., description="Resultado obtenido (ej. 4.2)")
    unit: str = Field(..., description="Unidad de medida (ej. mUI/L, g/dL)")
    reference: Optional[str] = Field(None, description="Rango de referencia (ej. 0.4 - 4.0)")
    status: Optional[str] = Field(None, description="Estado (ej. Normal, Alto, Bajo)")

class LabPdfRequest(BaseModel):
    institucion: str
    paciente_nombre: str
    paciente_dni: str
    origen: str = "AMBULATORIO"
    solicitante: str
    validador: str
    orden: str
    fecha: str
    hora: str = "08:00"
    paciente_edad: str
    estudio_nombre: str
    resultados: List[AnalitoResult]
    observaciones: Optional[str] = None

@app.post("/api/laboratorios/generar-pdf")
async def api_generar_pdf(request_data: LabPdfRequest):
    try:
        # Compatibility with pydantic v2 model_dump and v1 dict
        data_dict = request_data.model_dump() if hasattr(request_data, "model_dump") else request_data.dict()
        pdf_bytes = generate_lab_pdf(data_dict)
        
        headers = {
            "Content-Disposition": f"inline; filename={request_data.estudio_nombre.replace(' ', '_')}.pdf"
        }
        return StreamingResponse(
            BytesIO(pdf_bytes), 
            media_type="application/pdf", 
            headers=headers
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar el PDF: {str(e)}")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    favicon_path = os.path.join(static_path, "icons", "DR-active-icon.png")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)
    raise HTTPException(status_code=404, detail="Favicon no encontrado.")

@app.get("/")
def health_check():
    return {"status": "online"}