import PyPDF2
import logging

# Configure logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def extract_text_from_pdf(pdf_path):
    try:
        logging.info(f"Opening PDF file: {pdf_path}")
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            all_text = []
            logging.info(f"Number of pages: {len(reader.pages)}")
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text() + "\n"
                all_text.append((page_num + 1, text))  # Store text with page number
                logging.debug(f"Extracted text from page {page_num}")
            return all_text
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        return None
