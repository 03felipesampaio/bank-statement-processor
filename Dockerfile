FROM python:3.12

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src
COPY ./main.py /app/main.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]