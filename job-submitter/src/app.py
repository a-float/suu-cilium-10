from flask import Flask, request, jsonify, render_template
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
import socket
import requests

conf = {
    "bootstrap.servers": "kafka-service:9092",
    "client.id": socket.gethostname(),
    "session.timeout.ms": 30000,
}
admin = AdminClient(conf)
admin.create_topics([NewTopic(x) for x in ["add", "sub", "mul", "div"]])
producer = Producer(conf)
ops = ["add", "sub", "mul", "div"]
jobs = [0]

app = Flask(__name__, template_folder=".")


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/submit")
def submit():
    op = request.form["op"]
    a = request.form["a"]
    b = request.form["b"]
    protocol = request.form["protocol"]

    if protocol == "http":
        result = submit_http(op, a, b)
        return jsonify(result=result), 200
    elif protocol == "kafka":
        job_id = submit_kafka(op, a, b)
        return jsonify(code=200, value=protocol, message=f"Job submitted.", job_id=job_id), 200
    else:
        return jsonify(code=400, value=protocol, message=f"Invalid protocol. protocol should be one of http, kafka."), 400
    

def submit_http(op, a, b):
    response = requests.post(f"http://{op}-service:5000/calc", json={"a": a, "b": b})
    return response.json().get("result")


def submit_kafka(op, a, b):
    if op is None or op not in ops:
        return jsonify(code=400,message=f"Invalid operation. op should be one of {', '.join(ops.keys())}."), 400
    try:
        a = float(a)
        b = float(b)
    except:
        return jsonify(code=400, message=f"Invalid operand. Both a and b should be numbers."), 400
    

    job_id = str(jobs[0])
    jobs[0] += 1

    producer.produce(op, key=job_id, value=f"{job_id}:{a}:{b}")
    return job_id


@app.get("/result/<job_id>")
def get_result(job_id):
    response = requests.get(f"http://kafka-res-agg-service:5000/result/{job_id}")
    return jsonify(response.json()), response.status_code
