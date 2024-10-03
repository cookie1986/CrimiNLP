import argparse
from src.config import update_config, load_config
from src.read_data import load_data
from src.preprocessing import data_preprocessing
from src.target_formatting import target_mapping
from src.text_preprocessing import text_cleaning
from src.train_evaluate import training_and_eval_setup, train_and_evaluate


def main(update=False):
    if update:
        update_config(
            './config/config.template.json'
            )
    # Load config variables as dot notation
    config = load_config()
    
    # Read data from CSV file
    input_data_path = config.input_data
    if not input_data_path:
        print("Input data path not configured.")
    data = load_data(input_data_path)

    # Preprocessing
    data = data_preprocessing(
        data=data,
        features_name=config.features_name,
        save_duplicates = True,
        remove_outliers = True
        )

    # Map target values
    target = target_mapping(
        dataframe=data, 
        target_name = config.target_name,
        remap_target=True,
        ignored_values = ['Other']
        )
    
    # Clean text features
    text = text_cleaning(
        data = data[config.features_name],
        id_values = target.index
        )
    
    # Setup training environment
    training_setup = training_and_eval_setup()

    # Training and evaluation loop
    train_and_evaluate(X = text,
                       y = target)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the application")
    parser.add_argument(
        "--update-config", 
        action="store_true", 
        help="Update the configuration file before running."
        )
    args=parser.parse_args()
    
    main(update=args.update_config)