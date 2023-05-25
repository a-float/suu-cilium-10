from confluent_kafka import Consumer
import socket
import os
import operator
import requests as r

print(f"Will respond to http://{os.getenv('SCHEDULER_SERVICE_CONNECT')}/update")

conf = {
    "bootstrap.servers": "kafka-service:9092",
    "client.id": socket.gethostname(),
    "group.id": "worker-node",
    'session.timeout.ms': 30000,
}
consumer = Consumer(conf)
ops = {
    "add": operator.add,
    "sub": operator.sub,
    "mult": operator.mul,
    "div": lambda a, b: a / b,
}
consumer.subscribe(list(ops.keys()))


def handle_job(msg):
    job_id, a, op, b = msg[0].value().decode("utf-8").split(":")
    return {"job_id": job_id, "value": ops[op](float(a), float(b))}


while True:
    msg = consumer.consume()
    res = handle_job(msg)
    print("Returning", res)
    r.post(f"http://{os.getenv('SCHEDULER_SERVICE_CONNECT')}/update", json=res)
