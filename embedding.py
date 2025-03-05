import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from sentence_transformers import SentenceTransformer
import sys
from exception import customexception
from logger import logging

def download_custom_embedding(model, document):
    """
    Downloads and initializes a custom embedding model for vector embeddings.
    """
    try:
        logging.info("Initializing Custom Embedding model")
        custom_embed_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

        # Ensure document is a list of sentences or strings
        if isinstance(document, str):
            document = [document]
        elif isinstance(document, list):
            document = [str(d) for d in document]
        else:
            raise ValueError("Unsupported document format")

        embeddings = custom_embed_model.encode(document, convert_to_tensor=True)

        # Placeholder logic for creating an index and query engine
        index = "VectorStoreIndex placeholder"

        logging.info("Persisting index")
        query_engine = "Query engine placeholder"
        return query_engine
    except Exception as e:
        raise customexception(e, sys)
