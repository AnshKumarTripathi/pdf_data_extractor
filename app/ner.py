import spacy
import re
from collections import defaultdict

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

def extract_dates(text):
    date_pattern = r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2}|\w+\s\d{1,2},\s\d{4})\b'
    dates = re.findall(date_pattern, text)
    return dates

def extract_titles_positions(text):
    title_pattern = r'\b(?:Dr|Mr|Ms|Mrs|Prof|Sir)\.?\s\w+\b'
    titles = re.findall(title_pattern, text)
    return titles

def extract_organizations(text):
    doc = nlp(text)
    organizations = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    return organizations

def extract_urls(text):
    url_pattern = r'https?://\S+|www\.\S+'
    urls = re.findall(url_pattern, text)
    return urls

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

def extract_headings(text):
    heading_pattern = r'^\s*(?:[A-Z][A-Za-z0-9\s,.-]*[A-Z][A-Za-z0-9\s,.-]*)\s*$'
    headings = re.findall(heading_pattern, text, re.MULTILINE)
    return headings

def summarize_document(text, key_points):
    doc = nlp(text)
    summary = []
    
    for sent in doc.sents:
        for point in key_points:
            if point.lower() in sent.text.lower():
                summary.append((point, sent.text))
                break
    
    bullets = "\n".join([f"<li><strong>{point}</strong>: {desc}</li>" for point, desc in summary])
    return bullets

if __name__ == "__main__":
    sample_text = """UDIT H. SHETH\nudit@example.com\n123 Main Street\nContact: 9876543210\nDr. John Doe, CEO of Acme Corp., www.example.com\n"""
    entities = extract_entities(sample_text)
    dates = extract_dates(sample_text)
    titles_positions = extract_titles_positions(sample_text)
    organizations = extract_organizations(sample_text)
    urls = extract_urls(sample_text)
    emails = extract_emails(sample_text)
    phone_numbers = extract_phone_numbers(sample_text)
    addresses = extract_addresses(sample_text)
    headings = extract_headings(sample_text)
    summary = summarize_document(sample_text, headings)

    print("Entities:", entities)
    print("Dates:", dates)
    print("Titles/Positions:", titles_positions)
    print("Organizations:", organizations)
    print("URLs:", urls)
    print("Emails:", emails)
    print("Phone Numbers:", phone_numbers)
    print("Addresses:", addresses)
    print("Headings:", headings)
    print("Summary:", summary)
