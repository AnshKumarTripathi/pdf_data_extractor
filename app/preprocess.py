import nltk
import re

# Ensure required NLTK data is downloaded
nltk.download('punkt')

def preprocess_text(text):
    # Tokenize text
    tokens = nltk.word_tokenize(text)

    # Retain capitalization
    preprocessed_text = ' '.join(tokens)

    return preprocessed_text

if __name__ == "__main__":
    sample_text = """UDIT H. SHETH\n�The fears you don�t face becomes your limits�\n"""
    preprocessed_text = preprocess_text(sample_text)
    print(preprocessed_text)
