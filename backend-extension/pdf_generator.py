import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements(num_pages)
            super().showPage()
        super().save()

    def draw_page_elements(self, page_count):

        # 2. Pie de página
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        # Línea divisoria del pie de página
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(40, 45, 572, 45)
        
        # Textos de pie de página
        self.drawString(40, 30, "Historia de Salud Integrada (HSI)")
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(572, 30, page_text)
        self.restoreState()

def generate_lab_pdf(data: dict) -> bytes:
    """
    Genera un PDF en memoria (bytes) con los resultados de laboratorio
    utilizando ReportLab y siguiendo el diseño institucional de HSI.
    """
    buffer = BytesIO()
    
    # Configuración del documento Letter, márgenes de 40pt (532pt de ancho disponible)
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=60
    )
    
    styles = getSampleStyleSheet()
    
    # Paleta de colores institucionales
    primary_color = colors.HexColor("#2687C5")     # Azul HSI
    text_dark = colors.HexColor("#1e293b")         # Gris carbón
    text_muted = colors.HexColor("#64748b")        # Gris claro
    border_color = colors.HexColor("#cbd5e1")      # Gris borde
    bg_light = colors.HexColor("#f8fafc")          # Fondo gris suave
    alert_red = colors.HexColor("#b91c1c")         # Rojo para valores fuera de rango
    
    # Estilos personalizados de texto
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=text_dark,
        alignment=2 # Derecha
    )
    
    meta_label_style = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_dark
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=colors.white,
        alignment=1 # Centrado
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_dark
    )
    
    table_cell_bold_style = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName='Helvetica-Bold'
    )
    
    table_cell_center_style = ParagraphStyle(
        'TableCellCenter',
        parent=table_cell_style,
        alignment=1 # Centrado
    )

    table_cell_alert_style = ParagraphStyle(
        'TableCellAlert',
        parent=table_cell_style,
        fontName='Helvetica-Bold',
        textColor=alert_red,
        alignment=1 # Centrado
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=primary_color,
        spaceAfter=8
    )
    
    obs_title_style = ParagraphStyle(
        'ObsTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=text_dark,
        spaceAfter=4
    )
    
    obs_text_style = ParagraphStyle(
        'ObsText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=text_dark
    )
    
    signature_style = ParagraphStyle(
        'Signature',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=text_dark,
        alignment=1 # Centrado
    )

    story = []
    
    # 1. Cabecera (Logo a la izquierda, Título a la derecha)
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "logo-hsi.png")
    from reportlab.platypus import Image as RLImage
    
    if os.path.exists(logo_path):
        # Ajustamos el tamaño del logo en la cabecera preservando la relación de aspecto 5:1 (ancho=160pt, alto=32pt)
        logo_flowable = RLImage(logo_path, width=160, height=32)
    else:
        # Fallback de texto si el logo no está
        logo_flowable = Paragraph("<b>HISTORIA DE SALUD INTEGRADA</b>", ParagraphStyle('LogoFallback', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, textColor=primary_color))
        
    title_flowable = Paragraph("INFORME DE RESULTADOS DE LABORATORIO", title_style)
    
    header_table = Table([[logo_flowable, title_flowable]], colWidths=[180, 352])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 8))
    
    # Línea de acento azul institucional
    accent_line = Table([[""]], colWidths=[532], rowHeights=[2])
    accent_line.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), primary_color),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(accent_line)
    story.append(Spacer(1, 15))
    
    # 2. Bloque de Metadatos (Paciente / Institución) estructurado según lo solicitado
    # Columnas: 133 pt cada una (4 columnas)
    col_w = 133
    
    # Extraemos los campos del diccionario con valores por defecto seguros
    inst = data.get("institucion", "No especificada")
    paciente = data.get("paciente_nombre", "No especificado")
    dni = data.get("paciente_dni", "No especificado")
    origen = data.get("origen", "No especificado")
    solicitante = data.get("solicitante", "No especificado")
    validador = data.get("validador", "No especificado")
    orden = data.get("orden", "No especificado")
    fecha = data.get("fecha", "No especificada")
    hora = data.get("hora", "No especificada")
    edad = data.get("paciente_edad", "No especificada")
    
    # Creamos las celdas usando HTML-like tags soportados por Paragraph
    row1_p = Paragraph(f"<b>Institución:</b> {inst}", meta_label_style)
    row2_p = Paragraph(f"<b>Perteneciente a:</b> {paciente}", meta_label_style)
    
    row3_col1_p = Paragraph(f"<b>DNI.:</b> {dni}", meta_label_style)
    row3_col3_p = Paragraph(f"<b>Origen:</b> {origen}", meta_label_style)
    
    row4_p = Paragraph(f"<b>Solicitado por Dr./Dra.:</b> {solicitante}", meta_label_style)
    row5_p = Paragraph(f"<b>Validado por el Bioquimico/a:</b> {validador}", meta_label_style)
    
    row6_col1_p = Paragraph(f"<b>Orden:</b> {orden}", meta_label_style)
    row6_col2_p = Paragraph(f"<b>Fecha:</b> {fecha}", meta_label_style)
    row6_col3_p = Paragraph(f"<b>Hora:</b> {hora}", meta_label_style)
    row6_col4_p = Paragraph(f"<b>Edad:</b> {edad}", meta_label_style)
    
    metadata_data = [
        [row1_p, "", "", ""],                             # Fila 1: Institución (ocupa 4 cols)
        [row2_p, "", "", ""],                             # Fila 2: Perteneciente a (ocupa 4 cols)
        [row3_col1_p, "", row3_col3_p, ""],               # Fila 3: DNI (2 cols) | Origen (2 cols)
        [row4_p, "", "", ""],                             # Fila 4: Solicitado por (ocupa 4 cols)
        [row5_p, "", "", ""],                             # Fila 5: Validado por (ocupa 4 cols)
        [row6_col1_p, row6_col2_p, row6_col3_p, row6_col4_p] # Fila 6: Orden | Fecha | Hora | Edad
    ]
    
    metadata_table = Table(metadata_data, colWidths=[col_w]*4)
    metadata_table.setStyle(TableStyle([
        # Fusiones (Spans)
        ('SPAN', (0, 0), (3, 0)), # Fila 1: Institución abarca col 0 a 3
        ('SPAN', (0, 1), (3, 1)), # Fila 2: Perteneciente a abarca col 0 a 3
        ('SPAN', (0, 2), (1, 2)), # Fila 3: DNI abarca col 0 a 1
        ('SPAN', (2, 2), (3, 2)), # Fila 3: Origen abarca col 2 a 3
        ('SPAN', (0, 3), (3, 3)), # Fila 4: Solicitado por abarca col 0 a 3
        ('SPAN', (0, 4), (3, 4)), # Fila 5: Validado por abarca col 0 a 3
        
        # Ajustes de espaciado y fondo
        ('BACKGROUND', (0, 0), (-1, -1), bg_light),
        ('BOX', (0, 0), (-1, -1), 0.5, border_color),
        ('LINELEFT', (0, 0), (0, -1), 3.5, primary_color), # Borde lateral de acento azul
        
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(metadata_table)
    story.append(Spacer(1, 15))
    
    # 3. Observaciones (se muestra antes de los resultados)
    obs = data.get("observaciones", "")
    if obs:
        obs_elements = [
            Paragraph("Observaciones:", obs_title_style),
            Paragraph(obs, obs_text_style)
        ]
        
        # Ponemos las observaciones dentro de una caja destacada
        obs_table = Table([[obs_elements]], colWidths=[532])
        obs_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), bg_light),
            ('BOX', (0, 0), (0, 0), 0.5, border_color),
            ('LINELEFT', (0, 0), (0, 0), 3, colors.HexColor("#e2e8f0")),
            ('TOPPADDING', (0, 0), (0, 0), 8),
            ('BOTTOMPADDING', (0, 0), (0, 0), 8),
            ('LEFTPADDING', (0, 0), (0, 0), 12),
            ('RIGHTPADDING', (0, 0), (0, 0), 12),
        ]))
        story.append(obs_table)
        story.append(Spacer(1, 15))
        
    # 4. Sección de Resultados
    estudio_nombre = data.get("estudio_nombre", "Estudio de Laboratorio")
    story.append(Paragraph(estudio_nombre, section_title_style))
    
    # Definición de tabla de resultados
    # Columnas: Estudio/Analito (182 pt), Resultado (100 pt), Unidad (100 pt), Valores de Referencia (150 pt)
    results_headers = [
        Paragraph("Estudio / Analito", table_header_style),
        Paragraph("Resultado", table_header_style),
        Paragraph("Unidad", table_header_style),
        Paragraph("Valores de Referencia", table_header_style)
    ]
    
    results_rows = [results_headers]
    
    resultados_lista = data.get("resultados", [])
    for r in resultados_lista:
        name = r.get("name", "")
        val = r.get("value", "")
        unit = r.get("unit", "")
        ref = r.get("reference", "") or "-"
        status = r.get("status", "") or ""
        
        # Detección y formato si está fuera de rango
        is_outside = status.lower() in ["alto", "bajo", "high", "low", "out", "fuera de rango"]
        
        name_p = Paragraph(name, table_cell_bold_style)
        
        if is_outside:
            # Formato destacado en rojo
            val_p = Paragraph(f"<b>{val} *</b>", table_cell_alert_style)
        else:
            val_p = Paragraph(val, table_cell_center_style)
            
        unit_p = Paragraph(unit, table_cell_center_style)
        
        # Añadir la unidad al valor de referencia
        ref_val = f"{ref} {unit}".strip() if (ref and ref != "-") else ref
        ref_p = Paragraph(ref_val, table_cell_center_style)
        
        results_rows.append([name_p, val_p, unit_p, ref_p])
        
    results_table = Table(results_rows, colWidths=[182, 100, 100, 150])
    
    # Aplicar estilos a la tabla de resultados
    t_style = [
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
    ]
    
    # Fondos alternos para filas de datos
    for idx in range(1, len(results_rows)):
        bg = bg_light if idx % 2 == 0 else colors.white
        t_style.append(('BACKGROUND', (0, idx), (-1, idx), bg))
        
    results_table.setStyle(TableStyle(t_style))
    story.append(results_table)
    story.append(Spacer(1, 25))
        
    # 5. Firma y Acreditación Profesional (KeepTogether para evitar huérfanos)
    profesional = data.get("validador", "")
    # Extraer el nombre del bioquímico del texto de validador (e.g. "Bioq. Carlos Lopez - MP 5678" -> "Bioq. Carlos Lopez")
    nombre_firma = profesional.split(" - ")[0] if " - " in profesional else profesional
    licencia_firma = profesional.split(" - ")[1] if " - " in profesional else ""
    
    signature_elements = [
        Spacer(1, 35),
        # Línea de firma
        Table([[""]], colWidths=[200], rowHeights=[0.5], style=[('BACKGROUND', (0, 0), (0, 0), text_muted)]),
        Spacer(1, 4),
        Paragraph(f"<b>{nombre_firma}</b>", signature_style)
    ]
    if licencia_firma:
        signature_elements.append(Paragraph(licencia_firma, signature_style))
        
    # Tabla contenedora para alinear la firma a la derecha (ancho 220pt a la derecha, espacio libre de 312pt a la izquierda)
    signature_container = Table([["", signature_elements]], colWidths=[312, 220])
    signature_container.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    story.append(KeepTogether(signature_container))
    
    # Construcción final del PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data
