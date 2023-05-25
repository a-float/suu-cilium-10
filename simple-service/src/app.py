from flask import Flask, request, jsonify, render_template
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
import socket

conf = {
    "bootstrap.servers": "kafka-service:9092",
    "client.id": socket.gethostname(),
    "session.timeout.ms": 30000,
}
admin = AdminClient(conf)
admin.create_topics([NewTopic(x) for x in ["add", "sub", "mult", "div"]])
producer = Producer(conf)
results = {}
ops = {"add": "+", "sub": "-", "mult": "*", "div": "/"}

app = Flask(__name__, template_folder=".")


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/update")
def update():
    print("in update haa")
    job_id = request.json.get("job_id")
    value = request.json.get("value")
    print(f"Received {job_id} {value}")
    results[job_id] = value
    return request.json, 200


@app.route("/res/<job_id>")
def data(job_id):
    print(job_id)
    if job_id not in results:
        return jsonify(code=400, message=f"Job with id {job_id} does not exist."), 404
    elif results.get(job_id, None) is None:
        return jsonify(code=404, status="Processing..."), 404
    else:
        return jsonify(code=200, status="Complete", result=results[job_id]), 200


@app.route("/calc")
def calc():
    op = request.args.get("op")
    a = request.args.get("a")
    b = request.args.get("b")
    # fmt: off
    if op is None or op not in ops:
        return jsonify(code=400,message=f"Invalid operation. op should be one of {', '.join(ops.keys())}."), 400
    try:
        a = int(a)
        b = int(b)
    except:
        return jsonify(code=400, message=f"Invalid operand. Both a and b should be numbers."), 400
    # fmt: on
    job_id = str(len(results))
    results[job_id] = None
    producer.produce(op, key=job_id, value=f"{job_id}:{a}:{op}:{b}")
    return jsonify(code=200, id=job_id, a=a, b=b, op=ops[op]), 200
