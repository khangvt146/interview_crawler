import yaml

CONFIG_PATH = '../config.yml'
with open(CONFIG_PATH, "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

databases_config = config["databases"]
mongo_config = databases_config["mongo"]
MONGO_HOST: str = mongo_config["host"]
MONGO_PORT: int = mongo_config["port"]
MONGO_USERNAME: str = mongo_config["username"]
MONGO_PASSWORD: str = mongo_config["password"]