FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

ENV FLAG="CSC{R0b0t_D3t3ct3d!}"

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
