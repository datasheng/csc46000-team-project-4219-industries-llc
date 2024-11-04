FROM python:3.9.10-slim

WORKDIR /app

COPY req.txt .

RUN pip install --no-cache-dir -r req.txt

COPY . .

# output is unbuffered
ENV PYTHONUNBUFFERED=1 

CMD ["python", "Sentiment.py"]
