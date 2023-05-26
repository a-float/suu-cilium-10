from confluent_kafka import Consumer
import socket
import os
import requests as r

conf = {
    "bootstrap.servers": "kafka-service:9092",
    "client.id": socket.gethostname(),
    "group.id": "sub-worker-node",
    'session.timeout.ms': 30000,
}
consumer = Consumer(conf)
consumer.subscribe(["sub"])


def handle_job(msg):
    job_id, a, b = msg[0].value().decode("utf-8").split(":")
    return {"job_id": job_id, "a": a, "b": b, "op": "sub", "result": float(a) + float(b)}


while True:
    msg = consumer.consume()
    res = handle_job(msg)
    print("Returning", res)
    r.post(f"http://kafka-res-agg-service:5000/result", json=res)
