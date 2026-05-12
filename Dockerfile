FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .
RUN grep -v "openai-whisper" requirements.txt > requirements_clean.txt
RUN pip install --no-cache-dir -r requirements_clean.txt
RUN pip install git+https://github.com/openai/whisper.git

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]