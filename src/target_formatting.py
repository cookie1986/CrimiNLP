import pandas as pd
from typing import List
import logging
import os
from src.validators import check_type, data_integrity_check
from src.config import load_config

# Config logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
config = load_config()


def apply_value_mapping(values: pd.Series)-> pd.Series:
    """
    Replaces values in pd.Series with corresponding values from a CSV file mapping.

    Parameters:
    - values (pd.Series): The Series containing the values to be transformed.

    Returns:
    - pd.Series: A Series containing remapped values.

    Raises:
    - FileNotFoundError: If the CSV file cannot be found at the provided directory.
    """

    # Check the path to mapping file exists
    if not os.path.exists(config.label_remappings):
        error_message = f"The CSV file cannot be found at the provided directory: {config.label_remappings}"
        logging.error(error_message)
        raise FileNotFoundError(error_message)

    # Load remapping CSV file
    try:
        mapping_df = pd.read_csv(config.label_remappings, delimiter=',')
        mapping_df.columns = mapping_df.columns.str.strip()
    except Exception as e:
        logging.error(f"Error loading CSV file: {e}")
        raise
    
    # Replace values in target_name column with corresponding values in remapping file
    try:
        mapping_dict = mapping_df.set_index('value')['mapping'].to_dict() # Convert mapping CSV file (as DataFrame) to dict
        target_remapped = values.map(mapping_dict) # Perform the remapping
    except Exception as e:
        logging.error(f"Error during the mapping process: {e}")
        raise
    return target_remapped


def target_mapping(
        dataframe: pd.DataFrame,
        target_name: str,
        ignored_values: List = None,
        remap_target: bool = False
        ) -> pd.Series:
    """
    Extracts a target variable from available columns in a supplied DataFrame and optionally remaps its values.

    Parameters:
    - dataframe (pd.DataFrame): The DataFrame containing columns intended to act as the target in a supervised 
                                ML task.
    - target_name (str): The name of the target variable.
    - ignored_values (List, optional): A list of values to be ignored/removed within the target variable.
    - remap_target (bool, optional): If True, remaps values in the target column. Default is False.

    Returns:
    - pd.Series: A Series containing the processed target variable.

    Raises:
    - KeyError: If `target_name` is not found in the DataFrame's columns.
    - TypeError: If incorrect types are provided for the `dataframe`, `target_name`, or `remap_target` parameters.
    - ValueError: If `target_name` is invalid, if remapping directory is required but not provided, or if the target 
                column is empty after NaNs are removed.
    - DataIntegrityError: If the remapping process invalidates the dataset for supervised learning.
    """

    # TypeError checks
    check_type(dataframe, pd.DataFrame, 'dataframe')
    check_type(target_name, str, 'target_name')
    check_type(remap_target, bool, 'remap_target')
    
    # KeyError check
    if target_name not in dataframe.columns:
        error_message = f"{target_name} not found in DataFrame columns."
        logging.error(error_message)
        raise KeyError(error_message)
    
    # ValueError checks
    if remap_target and config.label_remappings is None:
        error_message = "remap_target set to True, but remap directory is blank."
        logging.error(error_message)
        raise ValueError(error_message)
    if target_name.strip() == "":
        error_message = "target_name cannot be empty or whitespace."
        logging.error(error_message)
        raise ValueError(error_message)

    # Filter DataFrame on target_name and drop NaNs
    target = dataframe[target_name].dropna()

    # Check if target is empty after removing NaNs.
    if target.empty:
        error_message = f'{target_name} is empty after removing NaNs.'
        logging.error(error_message)
        raise ValueError

    # Remap column values if remapping = True
    if remap_target == True:
        target = apply_value_mapping(values=target)
        
    # Remove whitespaces and convert to lower-case
    target = target.str.strip().str.lower()
    
    # Remove values appearing in the ignored_values list
    if isinstance(ignored_values, List):
        target = target[~target.isin([x.strip().lower() for x in ignored_values])]
    
    # Data integrity checks
    data_integrity_check(target)

    return target


