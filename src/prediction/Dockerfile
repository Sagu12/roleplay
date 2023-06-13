FROM python:3.7-slim-buster

WORKDIR /code

COPY ./services /code/services
COPY ./models /code/models
COPY ./api /code/api
COPY ./main.py /code/main.py
COPY ./tmp_images /code/tmp_images

COPY ./requirements.txt /code/requirements.txt

COPY ./newrelic.ini /code/newrelic.ini

COPY ./env /code/env

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN apt-get update
RUN python -m spacy download en_core_web_sm

EXPOSE 80

CMD ["python","-m","uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
