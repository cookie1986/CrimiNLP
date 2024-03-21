import nltk
import os
import logging

# Config logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def ensure_nltk_resources():
    """Ensures necessary NLTK resources, such as stopwords, are downloaded"""

    if not any(os.path.isdir(os.path.join(path, 'corpora', 'stopwords')) for path in nltk.data.path):
        nltk.download('stopwords')
        logging.info("NLTK stopwords have been downloaded.")
    else:
        logging.info("Using existing NLTK stopwords download")