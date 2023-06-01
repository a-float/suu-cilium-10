from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder=".")

@app.route("/")
def index():
    return render_template("index.html")


@app.post("/calc")
def calculate():
    print("Calculate (ADD):")
    a = float(request.json.get("a"))
    b = float(request.json.get("b"))
    result = a + b
    print(f"Received {a} {b}, result={result}")
    return jsonify(result=result), 200
