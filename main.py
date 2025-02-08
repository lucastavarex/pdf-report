from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fpdf import FPDF
import io

app = FastAPI()

@app.post("/generate-pdf")
async def generate_pdf(data: dict):
    try:
        # Extract data from JSON payload
        title = data.get("title", "Default Title")
        content = data.get("content", "This is a default content.")

        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=title, ln=True, align="C")
        pdf.multi_cell(0, 10, txt=content)

        # Save PDF to a bytes buffer
        buffer = io.BytesIO()
        pdf.output(buffer)
        buffer.seek(0)

        # Return PDF as a downloadable file
        return StreamingResponse(buffer, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=generated.pdf"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))