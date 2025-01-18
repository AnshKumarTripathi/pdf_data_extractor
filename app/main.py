import os
import logging
from flask import Flask, request, render_template, redirect, url_for
from extract import extract_text_from_pdf
from preprocess import preprocess_text
from ner import extract_entities, extract_emails, extract_phone_numbers, extract_addresses

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configure logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        logging.info(f"Uploaded file saved to: {file_path}")
        all_text = extract_text_from_pdf(file_path)
        
        entity_tracker = {}
        email_tracker = {}
        phone_number_tracker = {}
        address_tracker = {}
        
        for page_num, text in all_text:
            preprocessed_text = preprocess_text(text)
            entities = extract_entities(preprocessed_text)
            emails = extract_emails(preprocessed_text)
            phone_numbers = extract_phone_numbers(preprocessed_text)
            addresses = extract_addresses(preprocessed_text)
            
            for entity in entities:
                if entity not in entity_tracker:
                    entity_tracker[entity] = {"frequency": 0, "pages": []}
                entity_tracker[entity]["frequency"] += 1
                entity_tracker[entity]["pages"].append(page_num)
            
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
        
        # Prepare data for display
        entity_table = [
            {
                "name": entity,
                "frequency": details["frequency"],
                "pages": ", ".join(map(str, details["pages"]))
            }
            for entity, details in entity_tracker.items()
        ]
        
        email_table = [
            {
                "email": email,
                "frequency": details["frequency"],
                "pages": ", ".join(map(str, details["pages"]))
            }
            for email, details in email_tracker.items()
        ]
        
        phone_number_table = [
            {
                "phone_number": phone_number,
                "frequency": details["frequency"],
                "pages": ", ".join(map(str, details["pages"]))
            }
            for phone_number, details in phone_number_tracker.items()
        ]
        
        address_table = [
            {
                "address": address,
                "frequency": details["frequency"],
                "pages": ", ".join(map(str, details["pages"]))
            }
            for address, details in address_tracker.items()
        ]
        
        return render_template('result.html', entity_table=entity_table, email_table=email_table, phone_number_table=phone_number_table, address_table=address_table)

if __name__ == "__main__":
    app.run(debug=True)
