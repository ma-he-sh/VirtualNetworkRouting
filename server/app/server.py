import json
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import os
import sys

# database intialization
from modules.database import NetworkDB
db = NetworkDB()
db.create_tables()

from modules.graph import Graphs

app = Flask(__name__)

defaultSession = "86ab42ee-8b2e-4b00-b306-e8483698ef2f"

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
    
    if 'cost' not in request.json:
        return jsonify(
            error=True,
            code='invalid_request'
        )

    nodes = request.json['nodes']
    nodeComb  = request.json['cost']

    print( nodeComb )

    graph = Graphs( nodes, nodeComb )
    graph.get_solution( nodes[len(nodes) - 1] )

    path = graph.getSolution()
    print(path)

    # # clear current sessions
    # db.delete_session( defaultSession )

    # # create session
    # db.create_session( defaultSession, 'current_session' )

    # nodeArr = []
    # index = 0
    # for key in nodes:
    #     nodeObj = Node( index, key['name'], key['cost'] )
    #     nodeArr.append( nodeObj )
    #     print(nodeObj.getIP())
    #     index+=1
    
    return jsonify(
        error=False,
        code='nodes_saved'
    )

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