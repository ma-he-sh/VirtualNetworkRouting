from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
import json
import os
import time
import requests

app = Flask(__name__)

ROUTER_NAME = os.getenv('ROUTER_NAME')
ROUTER_IP   = os.getenv('ROUTER_IP')

class Router:
    router_file = 'router_data.json'

    @staticmethod
    def save(payload={}):
        with open(Router.router_file, 'w') as file:
            json.dump(payload, file)
        return True

    @staticmethod
    def read():
        if os.path.exists( Router.router_file ):
            with open(Router.router_file, 'r') as file:
                return json.loads(file.read())
        return {}

    @staticmethod
    def clear():
        if os.path.exists( Router.router_file ):
            with open(Router.router_file, 'w') as file:
                json.dump({}, file)

@app.route("/")
def index():
    Router.clear()
    return render_template('index.html', 
        router_name=ROUTER_NAME, 
        router_ip=ROUTER_IP,
    )

@app.route("/status", methods=["GET"])
def status():
    data = Router.read()
    has_message = 'message' in data

    router_message = ""
    router_timestamp= ""
    router_from = ""
    if has_message:
        router_message = data['message']
        router_timestamp = data['timestamp']
        router_routes    = data['routes']
        router_from      = "RECIEVED FROM: " + data['from']

        next_node = None
        next_host = None
        next_ip   = None
        if ROUTER_NAME in router_routes:
            router_routes[ROUTER_NAME]['recieved'] = True
            next_ip =  router_routes[ROUTER_NAME]['ip']
            next_node =  router_routes[ROUTER_NAME]['next']
        
        if next_node in router_routes:
            next_host = router_routes[next_node]['node_route']

        payload = {
            'message': router_message,
            'routes' : router_routes,
            'from'   : ROUTER_NAME
        }

        # send message to next router
        if next_node != "OBSERVER" and next_node is not None:
            # send message to next container
            try:
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                resp = requests.post( next_host, data=json.dumps(payload), headers=headers )
                data = resp.json()
                payload_sent=bool(data['recieved'])
            except Exception as ex:
                print(ex)
                pass
            finally:
                Router.clear() # clear current data

    return jsonify(
        status=True,
        has_message=has_message,
        router_message=router_message,
        router_timestamp=router_timestamp,
        router_from=router_from
    )

@app.route("/info")
def ping():
    return jsonify(
        ping="pong",
        router=ROUTER_NAME,
        router_ip=ROUTER_IP
    )

@app.route("/set_packet", methods=['POST'])
def set_packet():
    if 'message' not in request.json:
        return jsonify(
            error=True,
            code='payload_error'
        )
    
    payload = request.json['message']
    routes  = request.json['routes']
    fromNode= request.json['from']

    data = {
        'message': payload,
        'routes' : routes,
        'timestamp': time.time(),
        'from'   : fromNode,
    }
    recieved = Router.save(data)

    return jsonify(
        error=False,
        recieved=recieved
    )

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',  port=8080)