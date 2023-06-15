from confluent_kafka import Consumer
import socket
import os
import requests as r
import sys

configs = {
    "ADD": [lambda a, b: a + b, "Addition"],
    "SUB": [lambda a, b: a - b, "Subtraction"],
    "MUL": [lambda a, b: a * b, "Multiplication"],
    "DIV": [lambda a, b: a / b, "Division"]
}

op = os.environ["OP"]
if op not in configs:
    print(f"Invalid env OP={op}")
    sys.exit()
fn, name = configs[op]

conf = {
    "bootstrap.servers": "kafka-service:9092",
    "client.id": socket.gethostname(),
    "group.id": f"{op.lower()}-worker-node",
    'session.timeout.ms': 10000,
}
consumer = Consumer(conf)
consumer.subscribe([op.lower()])


def handle_job(msg):
    job_id, a, b = msg[0].value().decode("utf-8").split(":")
    return {"job_id": job_id, "a": a, "b": b, "op": op, "result": fn(float(a), float(b))}


while True:
    msg = consumer.consume()
    res = handle_job(msg)
    print("Returning", res)
    r.post(f"http://kafka-res-agg-service:5000/result", json=res)
