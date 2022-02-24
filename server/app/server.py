from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import os
import sys

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/save_nodes", methods=["POST"])
def save_nodes():
    pass

@app.route("/deploy", methods=["POST"])
def deply():
    pass

@app.route("/destroy", methods=["POST"])
def destroy():
    pass

@app.route("/send_packet", methods=["POST"])
def send_packet():
    pass

@app.route("/set_status", methods=["POST"])
def set_status():
    pass

@app.route("/get_status", methods=["GET"])
def get_status():
    pass

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)