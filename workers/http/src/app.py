from flask import Flask, request, jsonify, render_template
import os
import sys

app = Flask(__name__)
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

@app.route("/")
def index():
    return f"<h1>{name} worker</h1>"


@app.post("/calc")
def calculate():
    print(f"Calculate ({op}):")
    a = float(request.json.get("a"))
    b = float(request.json.get("b"))
    result = fn(a,b)
    print(f"Received {a} {b}, result={result}")
    return jsonify(result=result), 200
