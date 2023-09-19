from flask import Blueprint, jsonify, request
from src.models import MachineLearning
from flask_jwt_extended import create_access_token, jwt_required
from datetime import datetime, timedelta
from src import db, config
from src.utils import openapi

openapi = Blueprint('openapi', __name__)

@openapi.route('/chatgpt-call', methods=['POST'])
@jwt_required()
def chatgtp_call():
    data = request.get_json()

    OPENAPI_KEY = config.OPENAPI_KEY

    generate_template = openapi.format_template(data)
    generate_template_checkup = openapi.format_template_second(data)

    openapi.get_first_response(generate_template, generate_template_checkup, data)


    # product = Product(**data)
    # db.session.add(product)
    # db.session.commit()
    # return jsonify(product.to_dict())
