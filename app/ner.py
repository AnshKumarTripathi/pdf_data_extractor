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
            cleaned_entity = re.sub(r'\d+', '', ent.text).strip().lower()
            entities.append(cleaned_entity)

    # Check against common names
    filtered_entities = [entity for entity in entities if any(name in entity.split() for name in common_names)]

    return filtered_entities

def extract_emails(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails

def extract_phone_numbers(text):
    phone_pattern = r'\b(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}\b'
    phone_numbers = re.findall(phone_pattern, text)
    return phone_numbers

def extract_addresses(text):
    address_pattern = r'\d+\s+\w+\s(?:st|street|rd|road|ave|avenue|blvd|boulevard)\s*'
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
