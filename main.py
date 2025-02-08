import json
from fpdf import FPDF
from datetime import datetime

# Load data from JSON files
with open("data.json", "r", encoding="utf-8") as file:
    report_data = json.load(file)

with open("params.json", "r", encoding="utf-8") as file:
    params = json.load(file)

with open("ranking.json", "r", encoding="utf-8") as file:
    ranking = json.load(file)

# PDF setup
pdf = FPDF()
pdf.add_page()
pdf.set_font("Times", size=11)

# Styles
styles = {
    "page": {
        "padding_horizontal": 30,
        "padding_vertical": 40,
    },
    "group_title": {
        "font_size": 18,
        "font_style": "B",
        "align": "C",
        "padding_top": 20,
    },
    "table_header": {
        "font_style": "B",
        "align": "C",
        "border": 1,
        "padding_top": 2,
    },
    "table_data": {
        "align": "C",
        "border": 1,
        "padding_top": 2,
    },
    "params_container": {
        "margin_top": 12,
        "margin_bottom": 18,
    },
    "params_row": {
        "gap": 4,
    },
    "params_label": {
        "font_style": "B",
    },
}

# Helper function to format date
def format_date(date_str):
    try:
        # Try parsing with milliseconds and 'Z' suffix
        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        try:
            # Try parsing without milliseconds and 'Z' suffix
            date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            # If both fail, return the original string
            return date_str
    return date.strftime("%d/%m/%Y %H:%M:%S")

# Cover page
pdf.set_font("Times", size=18, style="B")
pdf.cell(0, 10, text="RELATÓRIO DE DETECÇÃO DE PLACAS CONJUNTAS", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.ln(10)

pdf.set_font("Times", size=11)
cover_params = [
    {"label": "Placa monitorada:", "value": params["plate"]},
    {
        "label": "Período analisado:",
        "value": f"De {format_date(params['startTime'])} até {format_date(params['endTime'])}",
    },
    {"label": "Limite de placas antes e depois:", "value": params["nPlates"]},
    {"label": "Total de detecções da placa monitorada:", "value": len(report_data)},
    {
        "label": "Total de detecções de todos os radares e placas:",
        "value": sum(group["total_detections"] for group in report_data),
    },
]

for param in cover_params:
    pdf.cell(0, 10, text=f"{param['label']} {param['value']}", new_x="LMARGIN", new_y="NEXT")

pdf.ln(10)

# Ranking section
pdf.set_font("Times", size=18, style="B")
pdf.cell(0, 10, text="Placas com mais de uma ocorrência", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.ln(10)

if ranking:
    # Table headers
    pdf.set_font("Times", style="B")
    pdf.cell(45, 10, text="Placa", border=1, align="C")
    pdf.cell(45, 10, text="Nº de ocorrências", border=1, align="C", new_x="LMARGIN", new_y="NEXT")

    # Table rows
    pdf.set_font("Times")
    for row in ranking:
        pdf.cell(45, 10, text=row["plate"], border=1, align="C")
        pdf.cell(45, 10, text=str(row["count"]), border=1, align="C", new_x="LMARGIN", new_y="NEXT")
else:
    pdf.cell(0, 10, text="Nenhuma placa foi detectada mais de uma vez nesse relatório além da própria placa monitorada.", new_x="LMARGIN", new_y="NEXT")

pdf.ln(20)

# Detection groups
for i, group in enumerate(report_data):
    pdf.set_font("Times", size=18, style="B")
    if len(report_data) > 1:
        pdf.cell(0, 10, text=f"Detecção {i + 1} da placa monitorada", new_x="LMARGIN", new_y="NEXT", align="C")
    else:
        pdf.cell(0, 10, text="Detecção única da placa monitorada", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(10)

    # Group parameters
    pdf.set_font("Times", size=11)
    detection_params = [
        {
            "label": "Data e hora da detecção da placa monitorada:",
            "value": format_date(group["detection_time"]),
        },
        {
            "label": "Período analisado:",
            "value": f"De {format_date(group['start_time'])} até {format_date(group['end_time'])}",
        },
        {"label": "Radares:", "value": ", ".join(group["radars"])},
        {
            "label": "Coordenadas:",
            "value": f"Latitude: {group['latitude']}, Longitude: {group['longitude']}",
        },
        {"label": "Endereço:", "value": group["location"]},
        {"label": "Total de detecções:", "value": str(group["total_detections"])},
    ]

    for param in detection_params:
        pdf.cell(0, 10, text=f"{param['label']} {param['value']}", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(10)

    # Detections table
    if group["detections"]:
        # Table headers
        pdf.set_font("Times", style="B")
        pdf.cell(45, 10, text="Data e Hora", border=1, align="C")
        pdf.cell(30, 10, text="Placa", border=1, align="C")
        pdf.cell(30, 10, text="Radar", border=1, align="C")
        pdf.cell(20, 10, text="Faixa", border=1, align="C")
        pdf.cell(40, 10, text="Velocidade [Km/h]", border=1, align="C")
        pdf.cell(40, 10, text="Nº de ocorrências", border=1, align="C", new_x="LMARGIN", new_y="NEXT")

        # Table rows
        pdf.set_font("Times")
        for detection in group["detections"]:
            pdf.cell(45, 10, text=format_date(detection["timestamp"]), border=1, align="C")
            pdf.cell(30, 10, text=detection["plate"], border=1, align="C")
            pdf.cell(30, 10, text=detection["camera_numero"], border=1, align="C")
            pdf.cell(20, 10, text=detection["lane"], border=1, align="C")
            pdf.cell(40, 10, text=str(detection["speed"]), border=1, align="C")
            pdf.cell(40, 10, text=str(detection["count"]), border=1, align="C", new_x="LMARGIN", new_y="NEXT")
    else:
        pdf.cell(0, 10, text="Nenhuma detecção encontrada para este grupo.", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(20)

# Save PDF
pdf.output("output.pdf")
print("PDF generated successfully: output.pdf")