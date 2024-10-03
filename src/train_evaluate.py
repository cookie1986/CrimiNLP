import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import KFold, GridSearchCV
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.ensemble import RandomForestClassifier

def training_and_eval_setup():
    """
    Setup training and evaluation strategy.
    
    Returns:
    - param_grid (dict): A dictionary containing CV grid parameters
    """

    # Set seed value
    seed = 42
    
    # Init training and evaluation components
    tfidf_vectorizer = TfidfVectorizer()
    rf = RandomForestClassifier(random_state=seed)
    inner_cv = KFold(
        n_splits=3, 
        shuffle=True, 
        random_state=seed
        )
    outer_cv = KFold(
        n_splits=10, 
        shuffle=True, 
        random_state=seed
        )

    # Define the paramater grid for CV
    param_grid = {
        'n_estimators': [20, 50, 80, 100],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 4],
        'min_samples_leaf': [1, 2],
    }

    return param_grid


def train_and_evaluate(X: pd.Series,
                       y = pd.Series):
    """
    
    """

    
    return None