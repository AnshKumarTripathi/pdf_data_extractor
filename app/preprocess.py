import nltk
import re

# Ensure required NLTK data is downloaded
nltk.download('punkt')

def preprocess_text(text):
    # Tokenize text
    tokens = nltk.word_tokenize(text)

    # Convert to lowercase
    tokens = [token.lower() for token in tokens]

    # Join tokens back into a single string
    preprocessed_text = ' '.join(tokens)

    return preprocessed_text

if __name__ == "__main__":
    sample_text = """UDIT H. SHETH\n�The fears you don�t face becomes your limits�\n"""
    preprocessed_text = preprocess_text(sample_text)
    print(preprocessed_text)
