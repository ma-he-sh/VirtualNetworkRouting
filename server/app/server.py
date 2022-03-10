import json
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import os
import sys
import requests

# database intialization
from modules.database import NetworkDB
db = NetworkDB()
db.create_tables()

from modules.graph import Graphs
from modules.handler import NodeHandler

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

    startNode = nodes[0]
    endNode   = nodes[len(nodes) - 1]

    graph = Graphs( nodes, nodeComb )
    path, nodeArr = graph.get_solution( startNode, endNode )

    # save the current data as a session
    NodeHandler.saveNodes( nodeArr )

    # create containers
    handler = NodeHandler( nodeArr, startNode )
    handler.generateContainers()
    
    return jsonify(
        error=False,
        start=startNode,
        end=endNode,
        path=path,
        code='path_generated'
    )

@app.route("/destroy_nodes", methods=["POST"])
def destroy_nodes():
    # check if data exists
    sessionExists = NodeHandler.sessionExists()
    if sessionExists:
        NodeHandler.saveNodes([])

@app.route("/send_packet", methods=["POST"])
def send_packet():
    if 'msg' not in request.json:
        return jsonify(
            error=True,
            code='invalid_request'
        )

    if request.json['msg'] == "":
        return jsonify(
            error=True,
            code='invalid_msg'
        )

    # check if session exists
    sessionExists = NodeHandler.sessionExists()
    if not sessionExists:
        return jsonify(
            error=True,
            code='session_not_exists'
        )

    message = request.json['msg']

    # get current session
    nodeArr = NodeHandler.getNodes()
    
    payoad_sent = False
    if len(nodeArr) > 1:
        # prepare payload
        payload = {
            'message': message,
            'routes' : {},
            'from'   : 'OBSERVER'
        }

        next_ip = nodeArr[0].getIP()
        next_host=nodeArr[0].getHost('/set_packet')

        for node in nodeArr:
            curr_node = node.getName()
            curr_ip   = node.getIP()
            next_node = node.getNext()
            next_route= node.getHost('/set_packet')

            payload['routes'][curr_node] = {
                'ip' : curr_ip,
                'recieved': False,
                'next' : next_node,
                'next_host' : next_route,
            }

        if next_ip is not None:
            try:
                resp = requests.post( next_host, data=payload )
                print(resp.json)
                payload_sent=True
            except Exception as ex:
                print(ex)
                print(payload)
                payload_sent=False,
            finally:
                pass


    return jsonify(
        error=False,
        code='packet_sent',
        sent=payoad_sent,
    )

@app.route("/set_status", methods=["POST"])
def set_status():
    pass

@app.route("/get_status", methods=["GET"])
def get_status():
    pass

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)