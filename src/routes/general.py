from flask import Blueprint, jsonify, current_app

general_blueprint = Blueprint('general', __name__)


@general_blueprint.route('/health', methods=['GET'])
def health():
    # test all log levels
    current_app.logger.debug('debug message')
    current_app.logger.info('info message')
    current_app.logger.warning('warning message')
    current_app.logger.error('error message')
    current_app.logger.critical('critical message')

    return jsonify({
        "status": "OK",
        "message": "Service is up and running"
    })
