# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

WORKDIR /code/app
#
ENV FLAG="CSC{d0g0_1s_s4fe!}"

# 
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
