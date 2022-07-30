# syntax=docker/dockerfile:1.2.0
FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./bitcoin_rate_api /code/bitcoin_rate_api
CMD ["uvicorn", "bitcoint_rate_api.main:app", "--host","0.0.0.0", "--port", "80"]
