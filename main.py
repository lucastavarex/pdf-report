import json
from fpdf import FPDF
from datetime import datetime

# Function to generate report ID
def generate_report_id():
    now = datetime.now()
    code = f"{now.year}{str(now.month).zfill(2)}{str(now.day).zfill(2)}.{str(now.hour).zfill(2)}{str(now.minute).zfill(2)}{str(now.second).zfill(2)}{str(now.microsecond // 1000).zfill(3)}"
    return code

# Load data from JSON files
with open("mock/data.json", "r", encoding="utf-8") as file:
    report_data = json.load(file)

with open("mock/params.json", "r", encoding="utf-8") as file:
    params = json.load(file)

with open("mock/ranking.json", "r", encoding="utf-8") as file:
    ranking = json.load(file)

# Add generated report ID to params
params['report_id'] = generate_report_id()

# Custom PDF class to add header
class CustomPDF(FPDF):
    def header(self):
        # Set position
        self.set_y(10)

        # First row: Two cells (images + title)
        self.set_font("Times", size=14)
        
        # First cell: Add two images
        first_cell_width = 60  # Increased width of the first cell
        first_line_height = 15  # Increased height of the first line to accommodate larger images
        image_height = 18  # Increased height of the images
        y_offset = (first_line_height - image_height) / 2  # Vertical offset to center the images

        # Draw the placeholder cell
        self.cell(first_cell_width, first_line_height, '', border=1)

        # Add the first image (vertically centered)
        self.image("assets/logoPrefeitura.png", x=12, y=13 + y_offset, w=22)  # Adjust x, y, and width
        # Add the second image (vertically centered)
        self.image("assets/logoCivitas.png", x=38, y=14 + y_offset, w=30)

        # Second cell: Title
        remaining_width = self.w - first_cell_width - 2 * self.l_margin  # Total width - first cell width - margins
        self.set_xy(self.l_margin + first_cell_width, 10)  # Set position for the title
        self.multi_cell(remaining_width, 15, "RELATÓRIO DE DETECÇÃO DE PLACAS CONJUNTAS", border=1, align="C")

        # Second row: One cell (ID)
        self.set_xy(self.l_margin, 10 + first_line_height)  # Set position for the ID
        self.cell(0, 7, f"ID: {params.get('report_id', 'N/A')}", border=1, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

# PDF setup
pdf = CustomPDF()
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

# Disclaimer Section
pdf.set_font("Times", size=18)
pdf.cell(0, 4, text="Informações gerais sobre o relatório", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.ln(3)

pdf.set_font("Times", style="B", size=12)
pdf.cell(0, 5, text="Estrutura do relatório", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Times", size=10)
pdf.multi_cell(0, 5, text="O relatório identifica placas de veículos que passaram junto a uma placa principal monitorada (Placas conjuntas). A identificação é feita dentro de um intervalo de tempo determinado pela investigação a partir dos parâmetros de busca no sistema. O relatório também aponta a frequência com que as placas conjuntas foram detectadas junto à placa principal monitorada. A apresentação do resultado se dá por ordem decrescente de passagens conjuntas. Este documento é gerado automaticamente pelo sistema, sem interferência humana. Todo esse documento é auditável.")
pdf.ln(2)

pdf.set_font("Times", style="B", size=12)
pdf.cell(0, 5, text="Parâmetros de busca", new_x="LMARGIN", new_y="NEXT")
pdf.ln(1)

pdf.set_font("Times", style="B", size=10)
pdf.cell(0, 5, text="Intervalo de tempo", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Times", size=10)
pdf.multi_cell(0, 5, text="As buscas por placas conjuntas podem ser feitas até cinco minutos antes e cinco minutos depois da passagem da placa principal monitorada. A escolha dos parâmetros é feita pelo solicitante da informação. Quando não há informação sobre o período de busca na solicitação, o operador da Civitas utiliza o intervalo padrão definido nas diretrizes operacionais internas (três minutos antes e três minutos depois e de até 50 placas).")
pdf.ln(1)

pdf.set_font("Times", style="B", size=10)
pdf.cell(0, 5, text="Quantidade de placas conjuntas por buscas", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Times", size=10)
pdf.multi_cell(0, 5, text="São identificadas no máximo 50 placas antes e 50 placas depois da placa principal monitorada.")
pdf.ln(2)

pdf.set_font("Times", style="B", size=12)
pdf.cell(0, 5, text="Radares e localização", new_x="LMARGIN", new_y="NEXT")
pdf.ln(1)

pdf.set_font("Times", size=10)
bullet_points = [
    "Cada radar possui um número identificador próprio. Todas as detecções feitas pelo sistema apontam o número identificador do equipamento que fez a leitura.",
    "Cada radar possui também informações de localização que incluem coordenadas geográficas e endereços completos. Essas informações também estão disponíveis junto a cada registro.",
    "O sentido de circulação da via é fornecido, salvo quando há indisponibilidade da informação no banco de dados."
]

for point in bullet_points:
    pdf.multi_cell(0, 5, text=f"{chr(149)} {point}")
    pdf.ln(1)
pdf.ln(2)

pdf.set_font("Times", style="B", size=12)
pdf.cell(0, 5, text="Como ler o relatório", new_x="LMARGIN", new_y="NEXT")
pdf.ln(1)

pdf.set_font("Times", size=10)
bullet_points = [
    "O relatório é disposto em duas partes. Na primeira parte, consta um ranking com a frequência com que cada placa conjunta aparece junto à placa monitorada durante o tempo determinado nas buscas. Nesta parte, as placas são classificadas de forma decrescente a partir da quantidade de vezes que passavam junto à placa monitorada.",
    "A segunda parte é composta por tabelas que apresentam em ordem cronológica todas as placas detectadas que passaram antes e depois da placa principal monitorada por grupo de radar.",
    "O relatório apresenta tabelas com linhas e colunas. A linha grifada em amarelo representa a placa principal monitorada na qual pretende-se buscar as placas conjuntas.",
    "Ao lado da listagem com cada placa, na coluna à direita, é apresentado a quantidade de vezes (ocorrências) que cada placa foi registrada em conjunto com a placa monitorada."
]

for point in bullet_points:
    pdf.multi_cell(0, 5, text=f"{chr(149)} {point}")
    pdf.ln(1)

pdf.ln(2)

pdf.set_font("Times", style="B", size=12)
pdf.cell(0, 5, text="Limitações do relatório", new_x="LMARGIN", new_y="NEXT")
pdf.ln(1)

pdf.set_font("Times", style="B", size=10)
pdf.cell(0, 5, text="Período disponível", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Times", size=10)
pdf.multi_cell(0, 5, text="A base de dados dos Sistema conta com um histórico de detecções a partir da data de 01/06/2024. Não é possível realizar buscas a períodos anteriores.")
pdf.ln(1)

pdf.set_font("Times", style="B", size=10)
pdf.cell(0, 5, text="Ausência de detecção", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Times", size=10)
pdf.multi_cell(0, 5, text=f"{chr(149)} A falta de registro de uma placa não significa, necessariamente, que o veículo não passou pelo local. A leitura de OCR pode ser inviabilizada em algumas circunstâncias, tais como: mau estado de conservação das placas, objetos obstruindo as câmeras de leitura, condições climáticas, período de inatividade do equipamento entre outros.")
pdf.ln(1)
pdf.multi_cell(0, 5, text=f"{chr(149)} O relatório não é exaustivo e a falta de registro de uma determinada placa não é determinante para comprovar que não houve a passagem naquela localidade.")

pdf.ln(1)

pdf.set_font("Times", style="B", size=10)
pdf.cell(0, 5, text="Distância entre radares", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Times", size=10)
pdf.multi_cell(0, 5, text="O relatório não indica trajetos percorridos entre as detecções.")

pdf.ln(10)

pdf.set_font("Times", size=18)
pdf.cell(0, 10, text="Parâmetros Gerais", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.ln(5)

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
    pdf.cell(0, 5, text=f"{param['label']} {param['value']}", new_x="LMARGIN", new_y="NEXT")

pdf.ln(10)

# Ranking section
pdf.set_font("Times", size=18 )
pdf.cell(0, 5, text="Placas com mais de uma ocorrência", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.ln(10)

if ranking:
    # Calculate the horizontal offset to center the table
    table_width = 90  # 45 (Placa) + 45 (Nº de ocorrências)
    page_width = pdf.w  # Get the page width
    horizontal_offset = (page_width - table_width) / 2

    # Move to the calculated horizontal offset
    pdf.set_x(horizontal_offset)

    # Table headers
    pdf.set_font("Times", style="B", size=10)
    pdf.cell(40, 7, text="Placa", border=1, align="C")
    pdf.cell(45, 7, text="Nº de ocorrências", border=1, align="C", new_x="LMARGIN", new_y="NEXT")

    # Table rows
    pdf.set_font("Times")
    for row in ranking:
        pdf.set_x(horizontal_offset)  # Move to the calculated horizontal offset for each row
        if row["plate"] == params["plate"]:
            pdf.set_fill_color(255, 255, 0)  # Yellow background
            pdf.set_font('', 'B') 
            fill = True
        else:
            fill = False
            pdf.set_font('', '') 
        pdf.cell(40, 7, text=row["plate"], border=1, align="C", fill=fill)
        pdf.cell(45, 7, text=str(row["count"]), border=1, align="C", new_x="LMARGIN", new_y="NEXT", fill=fill)
else:
    pdf.cell(0, 10, text="Nenhuma placa foi detectada mais de uma vez nesse relatório além da própria placa monitorada.", new_x="LMARGIN", new_y="NEXT")

pdf.ln(10)

# Detection groups
for i, group in enumerate(report_data):
    pdf.set_font("Times", size=18)
    if len(report_data) > 1:
        pdf.cell(0, 10, text=f"Detecção {i + 1} da placa monitorada", new_x="LMARGIN", new_y="NEXT", align="C")
    else:
        pdf.cell(0, 10, text="Detecção única da placa monitorada", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)

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
        pdf.multi_cell(0, 5, text=f"{param['label']} {param['value']}", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(10)

    # Detections table
    if group["detections"]:
        # Table headers
        pdf.set_font("Times", style="B", size=10)
        pdf.cell(45, 7, text="Data e Hora", border=1, align="C")
        pdf.cell(25, 7, text="Placa", border=1, align="C")
        pdf.cell(25, 7, text="Radar", border=1, align="C")
        pdf.cell(15, 7, text="Faixa", border=1, align="C")
        pdf.cell(40, 7, text="Velocidade [Km/h]", border=1, align="C")
        pdf.cell(40, 7, text="Nº de ocorrências", border=1, align="C", new_x="LMARGIN", new_y="NEXT")

        # Table rows
        pdf.set_font("Times")
        for detection in group["detections"]:
            if detection["plate"] == params["plate"]:
                pdf.set_fill_color(255, 255, 0)  # Yellow background
                pdf.set_font('', 'B') 
                fill = True
            else:
                fill = False
                pdf.set_font('', '') 
            pdf.cell(45, 7, text=format_date(detection["timestamp"]), border=1, align="C", fill=fill)
            pdf.cell(25, 7, text=detection["plate"], border=1, align="C", fill=fill)
            pdf.cell(25, 7, text=detection["camera_numero"], border=1, align="C", fill=fill)
            pdf.cell(15, 7, text=detection["lane"], border=1, align="C", fill=fill)
            pdf.cell(40, 7, text=str(detection["speed"]), border=1, align="C", fill=fill)
            pdf.cell(40, 7, text=str(detection["count"]), border=1, align="C", new_x="LMARGIN", new_y="NEXT", fill=fill)
    else:
        pdf.cell(0, 10, text="Nenhuma detecção encontrada para este grupo.", new_x="LMARGIN", new_y="NEXT")

    # pdf.ln(10)
    pdf.set_font("Times", size=10)
    pdf.cell(0, 10, text=f"Tabela {i + 1}: Detecções conjuntas àquela de número {i + 1} da placa monitorada", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(4)

# Save PDF
pdf.output("output.pdf")
print("PDF generated successfully: output.pdf")