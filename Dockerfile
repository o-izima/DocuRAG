FROM python:3.11-slim

# Optional: install tesseract for true OCR
RUN apt-get update && apt-get install -y --no-install-recommends     tesseract-ocr     && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
ENV PYTHONUNBUFFERED=1

EXPOSE 7860
CMD ["python", "-m", "docurag.ui.gradio_app"]
