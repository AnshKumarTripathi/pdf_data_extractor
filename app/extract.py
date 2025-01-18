import PyPDF2
import logging
import os

# Configure logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def extract_text_from_pdf(pdf_path, text_path):
    try:
        logging.info(f"Opening PDF file: {pdf_path}")
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            logging.info(f"Number of pages: {len(reader.pages)}")
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() + "\n"
                logging.debug(f"Extracted text from page {page_num}")
            with open(text_path, 'w', encoding='utf-8') as text_file:
                text_file.write(text)
            return text
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        return None

if __name__ == "__main__":
    pdf_path = os.path.abspath("../data/sample.pdf")
    text_path = os.path.abspath("../data/extracted_text.txt")
    logging.info(f"Starting extraction for file: {pdf_path}")
    extracted_text = extract_text_from_pdf(pdf_path, text_path)
    if extracted_text:
        print(extracted_text)
    else:
        logging.error("Failed to extract text from PDF")
