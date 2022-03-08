from sys import stderr, stdout
import yaml
import io
from os import path
import subprocess

CONTAINER_DIR="./containers/"

class Dockerize:
    def __init__(self, sess_name, routers=[] ):
        self.name = "session_"+sess_name
        self.docker_file_name = CONTAINER_DIR + "docker-composer-" + sess_name + ".yaml"
        self.routers = routers

    def generate(self):
        entry = {
            "version": "3",
            "networks": {
                "container_net": {
                    "ipam": {
                        "config": [
                            {"subnet": "172.20.0.0/24"},
                        ]
                    }
                }
            },
            "services": {}
        }

        if len(self.routers) > 0:
            entry["services"] = self.routers 

        with io.open( self.docker_file_name, "w", encoding="utf8" ) as file:
            yaml.dump( entry, file, default_flow_style=False, allow_unicode=True )

    def exec(self):
        if path.exists( self.docker_file_name ):
            process = subprocess.Popen(['docker-compose', '-f', self.docker_file_name, 'up'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            print(stdout, stderr)
            print("STARTED")
