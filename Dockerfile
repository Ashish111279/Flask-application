FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip && python -m pip install -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["python", "app.py"]
