from flask import Flask, jsonify
from flask_cors import CORS

from header import getHeader
from proc import getProcs

app = Flask(__name__)
CORS(app)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/getHeader")
def getH():
    return jsonify(getHeader())


@app.route("/getProcs")
def getP():
    return jsonify(getProcs())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)