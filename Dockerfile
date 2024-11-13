FROM python:3.10-slim

WORKDIR /app

RUN apt-get install python3-bs4

COPY req.txt .
RUN pip3 install --no-cache-dir -r req.txt

COPY . .

# output is unbuffered
ENV PYTHONUNBUFFERED=1 

CMD ["python", "Sentiment.py"]
