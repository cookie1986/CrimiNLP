import pandas as pd
import logging
import warnings
from pandas.api.types import infer_dtype
from src.exceptions import DataIntegrityError

# Config logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def check_type(
        variable, 
        expected_type, 
        variable_name: str
        ):
    """
    Checks if the variable is of the expected type and raises a TypeError if not.

    Parameters:
    - variable: The variable to be checked.
    - expected_type: The type against which the variable is checked.
    - variable_name (str): The nae of the variable used in the error message.

    Raises:
    - TypeError if the variable is not of the expected type.
    """

    if not isinstance(variable, expected_type):
        error_message = f"{variable_name} must be {expected_type.__name__}."
        logging.error(error_message)
        raise TypeError(error_message)
    

def check_data_imbalance(data: pd.Series, threshold: float = 0.1):
    """
    Checks for imbalance in the target dataset and issues a warning if imbalance is detected.

    Parameters:
    - data (pd.Series): The target dataset as a pandas Series.
    - threshold (float): The threshold for determining imbalance. Default is 0.1, representing 10%.
                         If the proportion of the smallest class is less than this threshold,
                         a warning is issued.
    """
    # Calculate the proportion of each class
    class_proportions = data.value_counts(normalize=True)
    
    # Find the smallest class proportion
    smallest_class_proportion = class_proportions.min()
    
    # Check if the smallest class proportion is below the threshold
    if smallest_class_proportion < threshold:
        warning_message = (f"Warning: The dataset is highly imbalanced. "
                           f"The smallest class represents only {smallest_class_proportion:.2%} of the data. "
                           "Consider using techniques for handling imbalanced data.")
        warnings.warn(warning_message)


def data_integrity_check(data: pd.Series):
    """
    Performs data integrity checks on a pandas Series and raises a custom error if violated.

    Parameters:
    - data (pd.Series): The data to be checked.

    Raises:
    - DataIntegrityError: If data type other than 'string' is found in 'data'.
    """

    # Check data type equals string
    data_type = infer_dtype(data)
    if data_type != 'string':
        error_message = f'Data is of type {data_type}. Data type should be "string".'
        logging.error(error_message)
        raise DataIntegrityError
    
    # Check for single values
    if data.nunique() == 1:
        error_message = f'Values in dataset appear identical.'
        logging.error(error_message)
        raise DataIntegrityError
    
    # Check for potential data imbalance issues
    check_data_imbalance(data)