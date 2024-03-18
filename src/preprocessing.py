import pandas as pd
from typing import List

def apply_value_mapping(
        values: pd.Series,
        mapping_dir: str
        ):
    """
    Replaces values in pd.Series with corresponding values from a CSV file mapping.

    Parameters:
    - values (pd.Series): The Series containing the values to be transformed.
    - mapping_dir (str): The file path to the CSV file containing the mapping. The CSV should have two columns:
                         one for original values and one for the remapped values.

    Returns:
    - pd.Series: A Series containing remapped values.

    Raises:
    - FileNotFoundError: If the CSV file cannot be found at the provided mapping_dir directory.
    """
    # Load remapping CSV file
    mapping_df = pd.read_csv(mapping_dir, delimiter=',')
    mapping_df.columns = mapping_df.columns.str.strip()
    
    # Replace values in target_name column with corresponding values in remapping file
    mapping_dict = mapping_df.set_index('value')['mapping'].to_dict() # Convert mapping CSV file (as DataFrame) to dict
    target_remapped = values.map(mapping_dict) # Perform the remapping

    return target_remapped

def target_mapping(
        dataframe: pd.DataFrame,
        target_name: str,
        ignored_values: List = None,
        remap_target: bool = False,
        remap_file_dir: str = None,
        ) -> pd.Series:
    """
    Extracts a target variable from available columns in a supplied DataFrame and optionally remaps its values.

    Parameters:
    - dataframe (pd.DataFrame): The DataFrame containing columns intended to act as the target in a supervised ML task.
    - target_name (str): The name of the target variable.
    - ignored_values (List, optional): A list of values to be ignored/removed within the target variable.
    - remap_target (bool, optional): If True, remaps values in the target column based on `remap_file_dir`. Default is False.
    - remap_file_dir (str): Directory to the file containing remappings. Required if `remap_target` is True.

    Returns:
    - pd.Series: A Series containing the processed target variable.

    Raises:
    - FileNotFoundError: If no DataFrame exists or if `remap_target` is True and `remap_file_dir` does not point to a valid file.
    - KeyError: If `target_name` is not found in the DataFrame's columns.
    - TypeError: If incorrect types are provided for the `dataframe`, `target_name`, or `remap_target` parameters.
    - ValueError: If `target_name` is invalid, if `remap_file_dir` is required but not provided, or if the target column is empty after NaNs are removed.
    - CustomDataIntegrityError: If the remapping process compromises data integrity in a way that invalidates the dataset for supervised learning.
    """

    # Filter DataFrame on target_name and drop NaNs
    target = dataframe[target_name].dropna()

    # Remap column values if remapping = True
    if remap_target == True:
        target = apply_value_mapping(
            values=target,
            mapping_dir=remap_file_dir
            )
        
        
    return target
