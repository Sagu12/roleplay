FROM python:3.9-slim-buster

WORKDIR /code

COPY src/prediction /code/src/prediction

RUN pip install --no-cache-dir --upgrade -r /code/src/prediction/requirements.txt

EXPOSE 80

CMD ["python","-m","uvicorn", "src.prediction.main:app", "--host", "0.0.0.0", "--port", "80"]
