from flask import Blueprint, jsonify, request
from src.utils.Extractions import (
    DataBankStatementExtractor,
    WebScrapedDataExtractor
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
    extractor = WebScrapedDataExtractor(data.get('scraped_websites'),
                                        data.get('phrases_list'))
    return jsonify(extractor.extract_and_format_textblock())

@openapi.route('/extract_data_from_webscraped_pdf', methods=['POST'])
def extract_data_from_webscraped_pdf():
    data = request.json
    extractor = WebScrapedDataExtractor(data.get('document'),
                                        data.get('phrases_list'))
    return jsonify(extractor.extract_and_format_pdf())
