FROM python:3.12

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src
COPY ./main.py /app/main.py
COPY ./log_config.json /app/log_config.json

CMD ["python", "main.py"]