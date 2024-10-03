import pandas as pd
import re
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import logging
from src.text_utils import ensure_nltk_resources


# Config logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Check stopwords are available
ensure_nltk_resources()
stop_words = set(stopwords.words('english'))

# Init stemmer
stemmer = PorterStemmer()


def basic_cleaning(
        data: pd.Series
        ) -> pd.Series:
    """
    Performs basic cleaning steps (convert text to lower-case and remove punctuation).

    Parameters:
    - data (pd.Series): A pandas Series containing text-values.

    Returns:
    - cleaned_data: A pandas Series with converted text.
    """
    
    # Convert text to lower-case.
    cleaned_data = data.str.lower()

    # Remove punctuation.
    cleaned_data = cleaned_data.apply(lambda x: re.sub(r'[^\w\s]|(\d+)', '', x))

    return cleaned_data


def text_cleaning(
        data: pd.Series,
        id_values = None
        ) -> pd.Series:
    """
    Cleans text in a pandas Series. Removes stopwords and stems the remaining tokens.

    Parameters:
    - data (pd.Series): A pandas Series containing text values.
    - id_values: Index values corresponding to the rows to be processed (non-indexed values are removed).

    Returns:
    - data (pd.Series): A pandas Series containing cleaned text values
    """
    
    # Filter data with the indices present in id_values.
    # Note: this ensures target/feaures match downstream.
    data = data.loc[id_values]
    
    # Basic cleaning steps
    data = basic_cleaning(data=data)

    # Remove stopwords
    data = data.apply(lambda x: ' '.join(word for word in x.split() if word not in stop_words))

    # Stem remaining tokens
    data = data.apply(lambda x: ' '.join(stemmer.stem(word) for word in x.split()))

    return data