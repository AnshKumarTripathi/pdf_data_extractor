# PDF Data Extractor

## Overview

Welcome to the PDF Data Extractor! This tool allows you to effortlessly upload and analyze PDF documents. Extract critical information including names, dates, titles/positions, organizations, URLs, emails, phone numbers, and addresses. Additionally, generate a detailed document summary with key points highlighted for quick insights.

## Features

- **Upload PDFs**: Easily upload PDF documents for analysis.
- **Extract Information**: Extract names, dates, titles/positions, organizations, URLs, emails, phone numbers, and addresses from the PDF.
- **Document Summary**: Generate a detailed summary of the document with key points highlighted.
- **User-Friendly Interface**: A clean and intuitive interface for uploading files and viewing extracted data.

## File Structure

project-folder/ └── app/ ├── main.py├── extract.py├── preprocess.py├── ner.py├── templates/ │ ├── index.html│ ├── result.html└── static/ └── styles.css

### Code Explanation

#### `main.py`

The main script of the application that handles file uploads, text extraction, entity extraction, and rendering the results.

**Key Functions:**

- **upload_file()**: Handles file uploads and processes the PDF to extract information and generate a summary.

#### `extract.py`

Responsible for extracting text from PDF files.

**Key Function:**

- **extract_text_from_pdf(pdf_path)**: Extracts text from each page of the PDF and keeps track of page numbers.

#### `preprocess.py`

Handles text preprocessing tasks.

**Key Function:**

- **preprocess_text(text)**: Tokenizes the text and retains capitalization for better entity recognition.

#### `ner.py`

Performs Named Entity Recognition (NER) and extracts various entities from the text.

**Key Functions:**

- **extract_entities(text)**: Extracts named entities (persons, organizations).
- **extract_dates(text)**: Extracts dates from the text.
- **extract_titles_positions(text)**: Extracts titles and professional positions.
- **extract_organizations(text)**: Extracts organizations from the text.
- **extract_urls(text)**: Extracts URLs from the text.
- **extract_emails(text)**: Extracts email addresses from the text.
- **extract_phone_numbers(text)**: Extracts phone numbers from the text.
- **extract_addresses(text)**: Extracts addresses from the text.
- **extract_headings(text)**: Extracts headings from the text for use in summary generation.
- **summarize_document(text, key_points)**: Generates a summary based on key points and headings extracted from the text.

#### `index.html`

The main interface for uploading PDF files.

**Key Elements:**

- **Header**: Displays the title of the application.
- **Form**: Allows users to upload PDF files.

#### `result.html`

Displays the extracted data and document summary.

**Key Elements:**

- **Tables**: Displays extracted named entities, dates, titles/positions, organizations, URLs, emails, phone numbers, and addresses in a tabular format.
- **Summary**: Displays a detailed document summary with key points highlighted.

#### `styles.css`

A dedicated CSS file for styling the application.

**Key Styles:**

- **Body**: Sets the font, background color, and margin for the entire page.
- **Header**: Styles the header with a background color and padding.
- **Container**: Sets the width and margin for the main content.
- **Content**: Styles the content area with padding and a box shadow.
- **Tables**: Styles the tables with border, padding, and alternating row colors.

## How to Run

1. **Clone the repository**:

   ```
   git clone https://github.com/yourusername/pdf-data-extractor.git
   ```

2. **Navigate to the project folder**:

   ```
   cd pdf-data-extractor/app
   ```

3. **Install the required dependencies**:

   ```
   pip install -r requirements.txt
   ```

4. **Run the application**:

   ```
   python main.py
   ```

5. **Open a web browser and navigate to**:

   ```
   http://127.0.0.1:5000/
   ```

6. **Upload a PDF file and view the extracted data and summary.**

## Dependencies

- Flask
- PyPDF2
- SpaCy
- NLTK
- re (regular expressions)

## Contributing

Feel free to submit issues, fork the repository and send pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License.

---
