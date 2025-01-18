# import nltk
# import re

# # Ensure required NLTK data is downloaded
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
# nltk.download('averaged_perceptron_tagger')

# # Load common names from file
# def load_common_names(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         names = [line.strip().lower() for line in file]
#     return set(names)

# common_names = load_common_names('D:/Fact-byte Porject/pdf_data_extractor/common_names.txt')

# def extract_entities(text):
#     # Tokenize text into words
#     words = nltk.word_tokenize(text)

#     # Part-of-Speech tagging
#     pos_tags = nltk.pos_tag(words)

#     # Named Entity Recognition
#     named_entities = nltk.ne_chunk(pos_tags, binary=True)

#     # Extract named entities
#     entities = []
#     for subtree in named_entities:
#         if hasattr(subtree, 'label'):
#             entity = " ".join([leaf[0] for leaf in subtree.leaves()])
#             entities.append(entity.lower())

#     # Check against common names
#     filtered_entities = [entity for entity in entities if entity in common_names]

#     return filtered_entities

# def extract_emails(text):
#     # Use regex to find email addresses
#     email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#     emails = re.findall(email_pattern, text)
#     return emails

# def extract_phone_numbers(text):
#     # Use regex to find phone numbers
#     phone_pattern = r'\b\d{10}\b'  # Assuming 10-digit phone numbers
#     phone_numbers = re.findall(phone_pattern, text)
#     return phone_numbers

# def extract_addresses(text):
#     # For simplicity, use regex to find addresses (e.g., street addresses)
#     address_pattern = r'\d+\s+[\w\s]+(?:st|street|rd|road|ave|avenue|blvd|boulevard)\s*'
#     addresses = re.findall(address_pattern, text, re.IGNORECASE)
#     return addresses

# # if __name__ == "__main__":

# #     sample_text = """UDIT H. SHETH\nudit@example.com\n123 Main Street\nContact: 9876543210\n"""
# #     entities = extract_entities(sample_text)
# #     emails = extract_emails(sample_text)
# #     phone_numbers = extract_phone_numbers(sample_text)
# #     addresses = extract_addresses(sample_text)

# #     print("Entities:", entities)
# #     print("Emails:", emails)
# #     print("Phone Numbers:", phone_numbers)
# #     print("Addresses:", addresses)

import spacy
import re

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Load common names from file
def load_common_names(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        names = [line.strip().lower() for line in file]
    return set(names)

common_names = load_common_names('common_names.txt')

def extract_entities(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG"]:
            entities.append(ent.text.lower())

    # Check against common names
    filtered_entities = [entity for entity in entities if any(name in entity.split() for name in common_names)]

    return filtered_entities

def extract_emails(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails

def extract_phone_numbers(text):
    phone_pattern = r'\b\d{10}\b'  # Assuming 10-digit phone numbers
    phone_numbers = re.findall(phone_pattern, text)
    return phone_numbers

def extract_addresses(text):
    address_pattern = r'\d+\s+[\w\s]+(?:st|street|rd|road|ave|avenue|blvd|boulevard)\s*'
    addresses = re.findall(address_pattern, text, re.IGNORECASE)
    return addresses

if __name__ == "__main__":
    sample_text = """UDIT H. SHETH\nudit@example.com\n123 Main Street\nContact: 9876543210\n"""
    entities = extract_entities(sample_text)
    emails = extract_emails(sample_text)
    phone_numbers = extract_phone_numbers(sample_text)
    addresses = extract_addresses(sample_text)

    print("Entities:", entities)
    print("Emails:", emails)
    print("Phone Numbers:", phone_numbers)
    print("Addresses:", addresses)
