import argparse
from src.read_data import load_data
from src.preprocessing import preprocess_data
from src.feature_engineering import create_feature_vector
from src.train_evaluate import train_and_evaluate
from src.config import update_config, load_config

def main(update=False):
    if update:
        update_config(
            './config/config.template.json'
            )
    else:
        load_config()

        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the application")
    parser.add_argument(
        "--update-config", 
        action="store_true", 
        help="Update the configuration file before running."
        )
    args=parser.parse_args()
    
    main(update=args.update_config)