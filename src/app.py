import os
import re
import traceback
import logging
from waitress import serve
from flask import Flask, request, jsonify
from flask_compress import Compress
from flask_cors import CORS
from libs.text_utils import TextUtils
from libs.path_utils import PathUtils
from libs.converter import TextExtractor

UPLOAD_FOLDER = '/tmp/uploads'
MAX_CONTENT_LENGTH = 5 * 1024 * 1024
ALLOWED_TYPE = {'pdf', 'doc', 'docx', 'odt'}

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')


def getLogLevel() -> str:
    level = os.environ.get('LOG_LEVEL', 'info')

    if level not in ['error', 'warning', 'info', 'debug', 'notset']:
        level = 'info'

    return level.upper()


def getMaxFileSize() -> int:
    units = {'B': 1, 'KB': 10**3, 'MB': 10**6, 'GB': 10**9, 'TB': 10**12}
    size = os.environ.get('MAX_FILE_SIZE', '0B').upper()

    if not re.match(r' ', size):
        size = re.sub(r'([KMGT]?B)', r' \1', size)

    number, unit = [string.strip() for string in size.split()]
    value = int(float(number)*units[unit])

    return value if value > 0 else MAX_CONTENT_LENGTH


def createApp():
    app = Flask(__name__)
    app.logger.setLevel(getLogLevel())
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = getMaxFileSize()
    app.config['ALLOWED_FILE_TYPE'] = ALLOWED_TYPE

    app.logger.info('text extractor service')

    @app.route('/convert', methods=['POST'])
    def convertToText():
        try:
            app.logger.info('POST /convert')

            filepath = getFile('file')
            use_ocr_fallback = getBoolInput('ocr fallback')

            app.logger.debug(f'convert document: {filepath} (try use ocr: {use_ocr_fallback})')
            (content, ocr_fallback) = TextExtractor.getText(filepath, use_ocr_fallback)
            language = TextUtils.detectLanguage(content)

            app.logger.debug(f'language: {language}, ocr fallback: {ocr_fallback}')
            app.logger.debug(f'output text: {content}')
            return jsonify({
                'language': language,
                'content': content,
                'ocr': ocr_fallback
            })
        except Exception as e:
            app.logger.error(f'request failed with error: {str(e)}')
            app.logger.debug(f'error stack: {traceback.format_exc()}')
            return jsonify({
                'error': str(e)
            }), 500

    def getFile(key: str) -> str:
        if key not in request.files:
            raise Exception(f'request does not contains {key} field')

        file = request.files[key]

        if not file or TextUtils.isEmpty(file.filename):
            raise Exception('request does not contain a valid file')

        extension = PathUtils.getExtension(file.filename)

        if extension not in app.config['ALLOWED_FILE_TYPE']:
            raise Exception('file format not allowed')

        tempfile = PathUtils.getTempPath()
        path = os.path.join(app.config['UPLOAD_FOLDER'], tempfile + '.' + extension)
        file.save(path)

        return path

    def getInput(key: str, default: str = None) -> str:
        form_key = key.replace(' ', '_')
        header_key = 'x-' + key.replace(' ', '-')

        if form_key in request.form:
            return request.form[form_key]
        elif header_key in request.headers:
            return request.headers[header_key]
        else:
            return default

    def getBoolInput(key: str, default: str = 'false') -> bool:
        input = getInput(key, default)
        return input.lower() in ['true', 't', '1']

    CORS(app)
    Compress().init_app(app)

    return app


if __name__ == '__main__':
    app = createApp()
    serve(app, host='0.0.0.0', port=80)
