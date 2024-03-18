import pandas as pd
import logging
import glob

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(directory_path: str) -> pd.DataFrame:
    """
    Loads data from a CSV file into a Pandas DataFrame.

    Parameters:
    - directory_path (str): The path to the directory containing CSV files to be loaded.

    Returns:
    - pd.DataFrame: The DataFrame containing the data from the CSV file.

    Raises:
    - FileNotFoundError: If no file exists.
    - pd.errors.EmptyDataError: If the file is empty.
    - pd.errors.ParserError: If there is an issue with the file.
    """

    files = glob.glob(f"{directory_path}/*.csv")

    if files:
        try:
            first_csv = files[0]
            data = pd.read_csv(first_csv)
            logging.info(f"Data successfully loaded from {first_csv}")
            return data
        except pd.errors.EmptyDataError:
            logging.error(f"File {first_csv} found at {directory_path} is empty")
            raise
        except pd.errors.ParserError:
            logging.error(f"Parser error for file {first_csv} at {directory_path}")
            raise
    else:
        file_not_found_error_msg = (f"File not found at: {directory_path}")
        logging.error(file_not_found_error_msg)
        raise FileNotFoundError(file_not_found_error_msg)

