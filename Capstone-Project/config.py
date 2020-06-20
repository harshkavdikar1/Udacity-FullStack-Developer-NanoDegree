from configparser import ConfigParser

config = ConfigParser()

config.read('capstone.conf')

bearer_tokens = {
    "assistant": config["TOKENS"]["assistant"],
    "director": config["TOKENS"]["director"],
    "producer": config["TOKENS"]["producer"]
}
