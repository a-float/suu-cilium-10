FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--debug"]
