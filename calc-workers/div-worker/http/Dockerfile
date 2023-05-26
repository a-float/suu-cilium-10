FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code

ENV PYTHONUNBUFFERED=1

ENV PYTHONIOENCODING=UTF-8

CMD ["python", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "5000", "--debug"]
