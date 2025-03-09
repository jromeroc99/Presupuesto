FROM python:3.11-slim

COPY ..

WORKDIR APP

RUN pip install -r requirements.txt

CMD ["reflex run"]

