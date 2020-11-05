FROM python:3.7-slim-buster

WORKDIR /app

RUN : && \
    apt update -y && \
    apt upgrade -y && \
    pip install --upgrade pip && \
    :

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python" ]
CMD [ "bot.py" ]
