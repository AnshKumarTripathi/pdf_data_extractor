import os
import logging
from flask import Flask, request, render_template, redirect, url_for, send_file
from app.extract import extract_text_from_pdf
from app.preprocess import preprocess_text
from app.ner import (
    extract_entities, extract_dates, extract_titles_positions, extract_organizations, extract_urls,
    extract_emails, extract_phone_numbers, extract_addresses, extract_headings, summarize_document
)
from collections import defaultdict
import tempfile
from flask_wtf.csrf import CSRFProtect
from io import BytesIO
from docx import Document
import json
import pdfkit


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_PERMANENT'] = False

csrf = CSRFProtect(app)
csrf.init_app(app)

UPLOAD_FOLDER = 'uploads'
DATA_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DATA_FOLDER'] = DATA_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

logging.basicConfig(filename='debug.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
@csrf.exempt  # CSRF protection for the upload route
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return redirect(request.url)
    
    if file:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            file.save(temp_file.name)
        
        logging.info(f"Uploaded file saved to: {temp_file.name}")
        all_text = extract_text_from_pdf(temp_file.name)
        
        entity_tracker = {}
        date_tracker = defaultdict(list)
        title_position_tracker = defaultdict(list)
        organization_tracker = defaultdict(list)
        url_tracker = defaultdict(list)
        email_tracker = {}
        phone_number_tracker = {}
        address_tracker = {}
        
        all_text_combined = " ".join(text for _, text in all_text)
        headings = extract_headings(all_text_combined)
        
        for page_num, text in all_text:
            preprocessed_text = preprocess_text(text)
            entities = extract_entities(preprocessed_text)
            dates = extract_dates(preprocessed_text)
            titles_positions = extract_titles_positions(preprocessed_text)
            organizations = extract_organizations(preprocessed_text)
            urls = extract_urls(preprocessed_text)
            emails = extract_emails(preprocessed_text)
            phone_numbers = extract_phone_numbers(preprocessed_text)
            addresses = extract_addresses(preprocessed_text)
            
            for entity in entities:
                if entity not in entity_tracker:
                    entity_tracker[entity] = {"frequency": 0, "pages": []}
                entity_tracker[entity]["frequency"] += 1
                entity_tracker[entity]["pages"].append(page_num)
            
            for date in dates:
                date_tracker[date].append(page_num)
            
            for title_position in titles_positions:
                title_position_tracker[title_position].append(page_num)
            
            for organization in organizations:
                organization_tracker[organization].append(page_num)
            
            for url in urls:
                url_tracker[url].append(page_num)
            
            for email in emails:
                if email not in email_tracker:
                    email_tracker[email] = {"frequency": 0, "pages": []}
                email_tracker[email]["frequency"] += 1
                email_tracker[email]["pages"].append(page_num)
            
            for phone_number in phone_numbers:
                if phone_number not in phone_number_tracker:
                    phone_number_tracker[phone_number] = {"frequency": 0, "pages": []}
                phone_number_tracker[phone_number]["frequency"] += 1
                phone_number_tracker[phone_number]["pages"].append(page_num)
            
            for address in addresses:
                if address not in address_tracker:
                    address_tracker[address] = {"frequency": 0, "pages": []}
                address_tracker[address]["frequency"] += 1
                address_tracker[address]["pages"].append(page_num)
        
        summary = summarize_document(all_text_combined, headings)
        
        # Clean up the temporary file
        temp_file.close()
        os.unlink(temp_file.name)
        
        # Store extracted data in a temporary file
        data = {
            'title': 'Document Title',  # Replace with actual title extraction
            'author': 'Document Author',  # Replace with actual author extraction
            'content': all_text_combined,
            'summary': summary,
            'entity_table': [
                {
                    "name": entity,
                    "frequency": details["frequency"],
                    "pages": ", ".join(map(str, details["pages"]))
                }
                for entity, details in entity_tracker.items()
            ],
            'date_table': [
                {
                    "date": date,
                    "pages": ", ".join(map(str, pages))
                }
                for date, pages in date_tracker.items()
            ],
            'title_position_table': [
                {
                    "title_position": title_position,
                    "pages": ", ".join(map(str, pages))
                }
                for title_position, pages in title_position_tracker.items()
            ],
            'organization_table': [
                {
                    "organization": organization,
                    "pages": ", ".join(map(str, pages))
                }
                for organization, pages in organization_tracker.items()
            ],
            'url_table': [
                {
                    "url": url,
                    "pages": ", ".join(map(str, pages))
                }
                for url, pages in url_tracker.items()
            ],
            'email_table': [
                {
                    "email": email,
                    "frequency": details["frequency"],
                    "pages": ", ".join(map(str, details["pages"]))
                }
                for email, details in email_tracker.items()
            ],
            'phone_number_table': [
                {
                    "phone_number": phone_number,
                    "frequency": details["frequency"],
                    "pages": ", ".join(map(str, details["pages"]))
                }
                for phone_number, details in phone_number_tracker.items()
            ],
            'address_table': [
                {
                    "address": address,
                    "frequency": details["frequency"],
                    "pages": ", ".join(map(str, details["pages"]))
                }
                for address, details in address_tracker.items()
            ]
        }
        
        data_file = os.path.join(app.config['DATA_FOLDER'], 'extracted_data.json')
        with open(data_file, 'w') as f:
            json.dump(data, f)
        
        return redirect(url_for('result', data_file=data_file))

@app.route('/result')
def result():
    data_file = request.args.get('data_file')
    if not data_file or not os.path.exists(data_file):
        return redirect(url_for('index'))
    
    with open(data_file, 'r') as f:
        extracted_data = json.load(f)
    
    return render_template('result.html', **extracted_data)

@app.errorhandler(500)
def internal_error(error):
    logging.error(f"Server error: {error}")
    return "An unexpected error occurred. Please try again later.", 500

@app.errorhandler(404)
def not_found_error(error):
    return "Page not found", 404



# if __name__ == "__main__":
#     app.run(debug=True)
