from flask import Flask, request, jsonify

app = Flask(__name__, template_folder=".")


results = {}


@app.post("/result")
def submit():
    a = float(request.json.get("a"))
    b = float(request.json.get("b"))
    op = request.json.get("op")
    result = float(request.json.get("result"))
    job_id = request.json.get("job_id")

    results[job_id] = {"a": a, "b": b, "op": op, "result": result}

    return jsonify({"status": "ok"}), 200

@app.get("/result/<job_id>")
def get_result(job_id):
    if job_id not in results:
        return jsonify({"error": "job not found"}), 404
    return jsonify({"data": results[job_id], "job_id": job_id}), 200
