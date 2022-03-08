from modules.dockerize import Dockerize
ipStart = "172.20.0."


class Node:
    def __init__(self, index, name, sendto):
        self.sendto = sendto
        self.name  = name
        self.index = index
        self.payload = None

    def setPayload(self, payload=None):
        self.payload = payload

    def getName(self):
        return self.name

    def getIndex(self):
        return self.index

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def destroy(self):
        pass

    def create(self):
        getIP = self.getIP()
        print(getIP)
        docker = Dockerize( self.name, getIP )
        docker.generate()

    def getIP(self):
        return ipStart + str(self.index)

    def getStatus(self):
        pass