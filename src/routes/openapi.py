from flask import Blueprint, jsonify, request
from src.utils.Extractions import (
    DataBankStatementExtractor,
    DataExtractor
)

openapi = Blueprint('openapi', __name__)


@openapi.route('/extract_data_bank_statement', methods=['POST'])
def extract_data_bank_statement():
    data = request.json
    pdf_path = data.path
    extractor = DataBankStatementExtractor(pdf_path)
    return jsonify(extractor.extract_and_format())


@openapi.route('/extract_data_from_webscraped_urls', methods=['POST'])
def extract_data_from_webscraped_urls():
    data = request.json
    output = DataExtractor().get_query_from_url(data.get('website_urls'),
                                                data.get('phrases_list'))
    return jsonify(output)


@openapi.route('/extract_data_from_pdfs', methods=['POST'])
def extract_data_from_pdfs():
    data = request.json
    output = DataExtractor().get_query_from_pdfs(data.get('files'),
                                                 data.get('phrases_list'))
    return jsonify(output)
