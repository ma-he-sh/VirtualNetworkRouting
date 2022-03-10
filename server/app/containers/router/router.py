from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
import json
import os
import time

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
    if has_message:
        router_message = data['message']
        router_timestamp = data['timestamp']
        router_routes    = data['routes']

        next_ip = None
        if ROUTER_NAME in router_routes:
            router_routes[ROUTER_NAME]['recieved'] = True
            next_ip =  router_routes[ROUTER_NAME]['next']

        payload = {
            'message': router_message,
            'routes' : router_routes,
            'from'   : ROUTER_NAME
        }

        # send message to next router
        print( router_routes )
        print(next_ip)

        # TODO send message to next container >>

    return jsonify(
        status=True,
        has_message=has_message,
        router_message=router_message,
        router_timestamp=router_timestamp,
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

    data = {
        'message': payload,
        'routes' : routes,
        'timestamp': time.time()
    }
    recieved = Router.save(data)

    return jsonify(
        error=False,
        recieved=recieved
    )

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',  port=8080)