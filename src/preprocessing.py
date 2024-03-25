import pandas as pd
import logging
import datetime
from src.config import load_config

# Config logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
config = load_config()


def delete_outliers(
        data: pd.DataFrame,
        features_name: 'str'
        ) -> pd.DataFrame:
    """
    Remove outlying data-points based on the number of characters in the features string. Rows where
    the length of the feature string exceeds three standard deviations are removed.

    Parameters:
    - data (pd.DataFrame): A pandas DataFrame with strings as values.
    - features_name (str): The name of the column to check for outliers.

    Returns:
    - data (pd.DataFrame): A pandas DataFrame with outliers removed.
    """

    # Calculate upper/lower bounds
    mean_length = data[features_name].str.len().mean()
    std_dev_length = data[features_name].str.len().std()
    lower_bound = mean_length - 3 * std_dev_length
    upper_bound = mean_length + 3 * std_dev_length

    # Filter the data
    data_f = data[data[features_name].str.len().between(lower_bound, upper_bound)]
    
    # Store the outliers
    outliers = data[~data[features_name].str.len().between(lower_bound, upper_bound)]
    outliers.to_csv(f"{config.outliers}/{datetime.date.today()}_outliers.csv", index=False)

    logging.info(f"{len(outliers)} rows were removed due to length exceeding 3 standard deviations.")

    return data_f


def data_preprocessing(
        data: pd.DataFrame,
        features_name: str,
        save_duplicates: bool = True,
        remove_outliers: bool = True
        ) -> pd.DataFrame:
    """
    Performs basic filtering steps on the feature column including removing NaNs, handling duplicate
    rows, and potential outliers.

    Parameters:
    - data (pd.DataFrame): A pandas DataFrame with a nominated target and features column.
    - features_name (str): The name of the features variable (must be a column in 'data').
    - save_duplicates (bool): A boolean determining if duplicate records are kept for auditing.
    - remove_outliers (bool): A boolean that determines the treatment of outliers (default (True) is to remove).

    Returns:
    - data (pd.DataFrame): A filtered pandas DataFrame.

    Raises:
    - TypeError: If data is not of type pd.DataFrame, features_name is not of type str, and save_duplicates and 
                 remove_outliers are not of type bool.
    - ValueError: If DataFrame is empty after removing NaNs.
    - FileNotFoundError: If unable to save duplicates to specified directory.
    """

    # Type checks
    if not isinstance(data, pd.DataFrame):
        raise TypeError("data must be a pandas DataFrame.")
    if not isinstance(features_name, str):
        raise TypeError("features_name must be a string.")
    if not isinstance(save_duplicates, bool) or not isinstance(remove_outliers, bool):
        raise TypeError("save_duplicates and remove_outliers must be boolean values.")
    
    # Remove NaNs from features column
    data = data.dropna(subset=[features_name])

    if data.empty:
        error_message = "DataFrame is empty after removing NaNs. Check your data or processing steps."
        logging.error(error_message)
        raise ValueError(error_message)

    # Check for duplicate values in the features column -- first instances are kept.
    data_dupes_index = data.duplicated(subset=features_name, keep='first')
    
    # Gather info on the duplicates removed.
    data_dupes_sum = data_dupes_index.sum()
    logging.info(f'{data_dupes_sum} duplicate records have been removed.')

    # Filter the dataset
    data_f = data[~data_dupes_index]

    # If True, store the duplicate values (along with first occurence) for auditing.
    if save_duplicates:
        data_dupes_index_with_first = data.duplicated(subset=features_name, keep=False)
        duplicates = data[data_dupes_index_with_first]
        try:
            duplicates.to_csv(f"{config.duplicate_data}/{datetime.date.today()}_duplicates.csv", index=False)
        except Exception as e:
            logging.error(f"Failed to save duplicates. Error: {str(e)}")
            raise FileNotFoundError("Could not save duplicates to file. Check the directory exists and is writable.")
    
    # Check for potential outliers and remove.
    if remove_outliers:
        data_f = delete_outliers(data_f,features_name)

    return data_f