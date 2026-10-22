
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --no-cache-dir --retries 10 --timeout 120 -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
