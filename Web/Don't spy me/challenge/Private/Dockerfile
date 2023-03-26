FROM python:3.9

WORKDIR /code

ENV FLAG="CSC{Y0u_4r3_4_m4573r_5py}"

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
