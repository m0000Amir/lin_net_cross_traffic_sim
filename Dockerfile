FROM python:3.7-slim

WORKDIR /usr

COPY requirements.txt .
COPY ./queue_model ./queue_model
COPY ./sim ./sim
COPY cross_traffic.py .
COPY data.json .
COPY input.json .
COPY prepare_inputs.py .
COPY calculation.py .


RUN pip install -r requirements.txt --no-cache-dir

CMD [ "python", "./calculation.py" ]