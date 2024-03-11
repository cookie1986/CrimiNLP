import json
import os
from dotenv import load_dotenv

# load environment variables from .env
load_dotenv('./config/.env')

def update_config(template_path):
    # load the template config
    with open(template_path, 'r') as file:
        config_template = json.load(file)

    # replace the variables in the template with the actual values in .env
    updated_config = {}
    for key, value in config_template.items():
        # strip ${} to get the actual VAR name
        env_var_name = value.strip('${}')
        # fetch the corresponding value from .env, using the original value as a fallback
        env_var_value = os.getenv(env_var_name, value)
        # write updated value to updated_config
        updated_config[key] = env_var_value
    
    # specify the path for the updated configuration
    updated_path_config = './config/config.json'

    # save the updated configuration
    with open(updated_path_config, 'w') as file:
        json.dump(updated_config, file, indent=4)
    
    print(f'Configuration updated and saved to {updated_path_config}')


def load_config(config_path='./config/config.json'):
    """load the configuration file"""
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config