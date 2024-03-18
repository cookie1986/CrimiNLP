import argparse
from src.config import update_config, load_config
from src.read_data import load_data
from src.preprocessing import target_mapping
# from src.feature_engineering import create_feature_vector
# from src.train_evaluate import train_and_evaluate


def main(update=False):
    if update:
        update_config(
            './config/config.template.json'
            )
    # load config variables
    config = load_config()
    
    # Read data
    input_data_path = config.get('input_data','')
    if not input_data_path:
        print("Input data path not configured.")
    data = load_data(input_data_path)

    # Map target values
    target_remappings_path = config.get('label_remappings')
    target_name = input("Name of target label: ")
    target = target_mapping(
        dataframe=data, 
        target_name = target_name,
        remap_target=True,
        remap_file_dir=target_remappings_path
        )
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the application")
    parser.add_argument(
        "--update-config", 
        action="store_true", 
        help="Update the configuration file before running."
        )
    args=parser.parse_args()
    
    main(update=args.update_config)