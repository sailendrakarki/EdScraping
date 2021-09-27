import database
import yaml
from yaml.error import YAMLError
with open('config.yml') as f:
    try:
        config = yaml.safe_load(f)
    except yaml.YAMLError as error:    
        print(error)


database.Database(config)