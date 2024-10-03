import json
import os
import logging
import warnings
from dotenv import load_dotenv

# Config logging 
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a',
                    format='%(name)s - %(levelname)s - %(message)s')

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

    # check if an existing config.json file exists and remove if so before creating a new one.
    if os.path.exists(updated_path_config):
        try:
            os.remove(updated_path_config)
            logging.info("Existing config.json file deleted.")
        except OSError as e:
            warnings.warn(f"Failed to delete existing config.json file: {e.strerror}. Check environment vars are correct.")

    # save the updated configuration
    try:
        with open(updated_path_config, 'w') as file:
            json.dump(updated_config, file, indent=4)
        logging.info(f'Configuration updated and saved to {updated_path_config}')
    except Exception as e:
        error_message = f"Error saving to config.json: {e}"
        logging.error(error_message)
        raise


class ConfigObject:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                value = ConfigObject(value)
            self.__dict__[key] = value

_config_instance = None

def load_config(config_path='./config/config.json'):
    """load the configuration file"""
    global _config_instance
    if _config_instance is None:
        with open(config_path, 'r') as file:
            config_dict = json.load(file)
        _config_instance = ConfigObject(config_dict)
    return _config_instance