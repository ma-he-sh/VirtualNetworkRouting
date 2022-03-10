from modules.dockerize import Dockerize
ipStart = "172.20.0."

CONTAINER_DIR="./containers/"

class Node:
    def __init__(self, index, name, sendto):
        self.sendto = sendto
        self.name  = name
        self.index = index
        self.payload = None
        self.docker_container_name = "router_" + name

    def setPayload(self, payload=None):
        self.payload = payload

    def getName(self):
        return self.name

    def getIndex(self):
        return self.index

    def getStart(self):
        return self.name

    def getNext(self):
        return self.sendto

    def destroy(self):
        pass

    def create(self):
        getIP = self.getIP()
        getPort = self.getPort()

        router_name = "router_" + self.name.lower()

        entry = {
            "build": {
                "context": ".",
                "dockerfile": "Dockerfile",
            },
            "container_name": router_name,
            "environment": {
                "ROUTER_NAME": self.name,
                "ROUTER_IP": getIP,
            },
            "ports": [
                str(getPort) + ":8080"
            ],
            "networks": {
                "container_net": {
                    "ipv4_address": getIP
                }
            }
        }

        return entry, router_name

    def getIP(self):
        return ipStart + str(self.index)

    def getHost(self, path=""):
        ip = self.getIP()
        port = "8080"
        return "http://{ip}:{port}{path}".format(ip=ip, port=port, path=path)
    
    def getPort(self):
        return "80" + str(self.index)

    def getStatus(self):
        pass