from flask import Blueprint, jsonify, request
from src.models import MachineLearning
from flask_jwt_extended import create_access_token, jwt_required
from datetime import datetime, timedelta
from src import db
from src.utils import open_api
import PyPDF2


openapi = Blueprint('openapi', __name__)

@openapi.route('/chatgpt_call', methods=['POST'])
@jwt_required()
def chatgtp_call():
    data = request.json
    print(data)

    path_to_pdf = 'src/routes/downloadfile.PDF'
    print(path_to_pdf)
    extracted_text = extract_text_from_pdf(path_to_pdf)
    print(extracted_text)
    generate_template = open_api.call_bank_statement(extracted_text)
    print(generate_template)
    # generate_template_checkup = open_api.format_template_second(data)

    # open_api.get_chat_response(generate_template, generate_template_checkup, data)


    # product = Product(**data)
    # db.session.add(product)
    # db.session.commit()
    # return jsonify(product.to_dict())


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


