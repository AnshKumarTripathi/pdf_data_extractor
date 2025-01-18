import nltk
import re

nltk.download('punkt')

def preprocess_text(text):
    tokens = nltk.word_tokenize(text)

    preprocessed_text = ' '.join(tokens)

    return preprocessed_text

if __name__ == "__main__":
    sample_text = """UDIT H. SHETH\n�The fears you don�t face becomes your limits�\n"""
    preprocessed_text = preprocess_text(sample_text)
    print(preprocessed_text)
