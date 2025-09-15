import spacy
import os
from pathlib import Path
from typing import List
from .logging import logger
from spacy.cli.download import download

# The path to the local SpaCy model
MODEL_PATH = Path(__file__).parent.parent.parent / "models" / \
    "en_core_web_sm" / "en_core_web_sm-3.8.0"

# Initialize the SpaCy NLP pipeline
nlp = None

try:
    # STEP 1: Try to load from local bundled model
    if MODEL_PATH.exists():
        logger.info(
            f"Loading SpaCy model from local bundled path: {MODEL_PATH}")
        nlp = spacy.load(str(MODEL_PATH))
        logger.info("Successfully loaded local SpaCy model")
    else:
        raise FileNotFoundError(
            "Local model not found, proceeding to download")

except Exception as e:
    logger.warning(f"Local SpaCy model failed to load: {e}")

    try:
        # STEP 2: Try to download and install the model
        logger.info("Attempting to download SpaCy model 'en_core_web_sm'...")
        download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
        logger.info("Successfully downloaded and loaded SpaCy model")

    except Exception as download_error:
        logger.warning(f"SpaCy model download failed: {download_error}")

        try:
            # STEP 3: Try to load from system-installed model (if already exists)
            logger.info("Trying to load from existing system installation...")
            nlp = spacy.load("en_core_web_sm")
            logger.info(
                "Successfully loaded SpaCy model from system installation")

        except Exception as system_error:
            # STEP 4: All SpaCy options failed - use simple fallback
            logger.error(
                f"All SpaCy loading attempts failed. System error: {system_error}")
            logger.warning(
                "SpaCy model unavailable - will use simple word extraction fallback")
            nlp = None


def extract_nouns(text: str) -> List[str]:
    # Extracts the top 3 most frequent nouns from the input text using SpaCy.

    if nlp is None:
        # Use simple word frequency analysis when SpaCy model loading fails
        logger.warning(
            "SpaCy not available, using simple word extraction fallback")

        # Split text into individual words and convert to lowercase for consistency
        words = text.lower().split()
        word_counts = {}

        # Process each word in the text
        for word in words:
            # Remove punctuation and keep only alphabetic characters
            clean_word = ''.join(c for c in word if c.isalpha())

            # Filter out very short words (likely articles, prepositions, etc.)
            if len(clean_word) > 3:
                word_counts[clean_word] = word_counts.get(clean_word, 0) + 1

        # Sort words by frequency, most frequent first and return top 3
        sorted_words = sorted(word_counts.items(),
                              key=lambda item: item[1], reverse=True)
        return [word for word, count in sorted_words[:3]]

    #  Process text via SpaCy's NLP pipeline
    doc = nlp(text)
    noun_counts = {}

    # Iterate through each token in the processed document
    for token in doc:
        # Check if the token is classified as a noun by SpaCy's part-of-speech tagger
        if token.pos_ == "NOUN":
            # Store noun in lowercase for case-insensitive counting
            noun_text = token.text.lower()
            noun_counts[noun_text] = noun_counts.get(noun_text, 0) + 1

    # Sort nouns by frequency in descending order to get most important ones first
    sorted_nouns = sorted(noun_counts.items(),
                          key=lambda item: item[1], reverse=True)

    # Return the top 3 most frequent nouns as our keywords for specificity and relevance
    return [noun for noun, count in sorted_nouns[:3]]
