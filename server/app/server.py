from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import os
import sys

from modules.node import Node

# database intialization
from modules.database import NetworkDB
db = NetworkDB()
db.create_tables()

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/save_nodes", methods=["POST"])
def save_nodes():
    pass

@app.route("/deploy_nodes", methods=["POST"])
def deploy_nodes():
    if 'nodes' not in request.json:
        return jsonify(
            error=True,
            code='invalid_request'
        )

    if len(request.json['nodes']) <= 0:
        return jsonify(
            error=True,
            code='empty_nodes'
        )

    nodes = request.json['nodes']

    # clear current sessions
    db.delete_session( '' )

    # create session
    db.create_session( '86ab42ee-8b2e-4b00-b306-e8483698ef2f', 'current_session' )

    nodeArr = []
    for i in nodes:
        nodeArr.append( Node( 'node_' + str(i), nodes[i]['name'], nodes[i]['cost'] ) )

    # save data on db


    pass

@app.route("/destroy_nodes", methods=["POST"])
def destroy_nodes():
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