import yaml
import io

CONTAINER_DIR="./containers/"

class Dockerize:
    def __init__(self, name, ip):
        self.name = "router_"+name
        self.docker_file_name = CONTAINER_DIR + "docker-composer-" + name + ".yaml"
        self.ip   = ip

    def generate(self):
        entry = {
            "version": "3",
            "networks": {
                "container_net": {
                    "ipam": {
                        "config": {
                            "subnet": "172.20.0.0/24",
                        }
                    }
                }
            },
            "services": {
                "web": {
                    "build": {
                        "context": ".",
                        "dockerfile": "Dockerfile",
                    },
                    "container_name": self.name,
                    "networks": {
                        "container_net": {
                            "ipv4_address": self.ip
                        }
                    }
                }
            }
        }

        with io.open( self.docker_file_name, "w", encoding="utf8" ) as file:
            yaml.dump( entry, file, default_flow_style=False, allow_unicode=True )
