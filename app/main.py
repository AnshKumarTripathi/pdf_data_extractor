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
        text_path = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted_text.txt')
        file.save(file_path)
        
        logging.info(f"Uploaded file saved to: {file_path}")
        text = extract_text_from_pdf(file_path, text_path)
        
        # Read from the text file
        with open(text_path, 'r', encoding='utf-8') as text_file:
            extracted_text = text_file.read()
        
        logging.info(f"Extracted Text: {extracted_text[:500]}")  # Log a snippet of the extracted text
        
        preprocessed_text = preprocess_text(extracted_text)
        logging.info(f"Preprocessed Text: {preprocessed_text[:500]}")  # Log a snippet of the preprocessed text
        
        entities = extract_entities(preprocessed_text)
        logging.info(f"Entities: {entities}")
        
        emails = extract_emails(preprocessed_text)
        logging.info(f"Emails: {emails}")
        
        phone_numbers = extract_phone_numbers(preprocessed_text)
        logging.info(f"Phone Numbers: {phone_numbers}")
        
        addresses = extract_addresses(preprocessed_text)
        logging.info(f"Addresses: {addresses}")
        
        extracted_data = {
            'entities': entities,
            'emails': emails,
            'phone_numbers': phone_numbers,
            'addresses': addresses
        }
        
        logging.info(f"Extracted data: {extracted_data}")
        return render_template('result.html', data=extracted_data)

if __name__ == "__main__":
    app.run(debug=True)
