# Use an official Python runtime as a parent image
FROM python:3.9
LABEL authors="ouail laamiri"

WORKDIR /app

COPY requirements/prod.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r prod.txt

COPY . .


EXPOSE 5000
VOLUME [ "/data" ]

# Specify the CMD as an array
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]