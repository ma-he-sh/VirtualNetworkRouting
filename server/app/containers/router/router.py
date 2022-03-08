from flask import Flask, jsonify
from dotenv import load_dotenv

app = Flask(__name__)

def set_status():
    """
    send status
    :return:
    """
    pass

@app.route("/")
def index():
    return "ROUTER"

@app.route("/set_packet")
def set_packet():
    pass

@app.route("/send_packet")
def send_packet():
    pass

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',  port=8181)