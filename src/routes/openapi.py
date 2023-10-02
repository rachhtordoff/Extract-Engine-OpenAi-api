from flask import Blueprint, jsonify, request
from src.models import MachineLearning
from flask_jwt_extended import create_access_token, jwt_required
from datetime import datetime, timedelta
from src import db
from src.utils.open_api import DataExtractor, TemplateFormatter, ChatResponder
import PyPDF2


openapi = Blueprint('openapi', __name__)

@openapi.route('/extract_data_bank_statement', methods=['POST'])
@jwt_required()
def extract_data_bank_statement():
    data = request.json
    # TEST -- REPLACE THIS
    path_to_pdf = 'src/routes/downloadfile.PDF'
    extracted_text = extract_text_from_pdf(path_to_pdf)
    generate_template = DataExtractor.call_bank_statement(extracted_text)
    return jsonify(generate_template) 

@openapi.route('/extract_data_from_webscraped_urls', methods=['POST'])
@jwt_required()
def extract_data_from_webscraped_urls():
    data = request.json
    output={}
    for key, value in data.get('scraped_websites').items():

        generate_template = DataExtractor.custom_template_data_extract(value, data.get('phrases_list'))
        output.update({key: generate_template})
    print(output)
    return jsonify(output) 


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        # Initialize a PDF reader
        reader = PyPDF2.PdfReader(file)
        
        # Initialize a string to store the extracted text
        text = ''
        
        # Loop through all the pages in the PDF
        for page_num in range(len(reader.pages)):
            # Extract text from the current page
            text += reader.pages[page_num].extract_text()
        
    return text


