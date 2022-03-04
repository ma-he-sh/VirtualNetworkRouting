import yaml

class Dockerize:
    COMPOSITION = {'services': {}, 'version': '3'}

    def __init__(self, name, ip):
        self.name = name
        self.ip   = ip

    def generate(self):
        entry = {""}
    