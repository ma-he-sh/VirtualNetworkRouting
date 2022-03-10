from sys import stderr, stdout
import sys
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

    def exec(self, rebuild=False):
        pidstdout = 0
        if path.exists( self.docker_file_name ):
            if rebuild:
                process = subprocess.Popen(['docker-compose', '-f', self.docker_file_name, 'up', '-d', '--no-deps', '--build'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                process = subprocess.Popen(['docker-compose', '-f', self.docker_file_name, 'up', '-d'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pidstdout, stderr = process.communicate()
            if len(pidstdout.splitlines()) > 0:
                sys.exit(0)
        return pidstdout

    @staticmethod
    def shutdown(sess_name):
        docker_file_name = CONTAINER_DIR + "docker-composer-" + sess_name + ".yaml"

        if path.exists( docker_file_name ):
            process = subprocess.Popen(['docker-compose', '-f', docker_file_name, 'down'])
            pidstdout, stderr = process.communicate()
            if len(pidstdout.splitlines()) > 0:
                sys.exit(0)
        return True