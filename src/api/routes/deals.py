from flask import Blueprint
from flask import request
from flask import abort
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
import requests
import os
import gzip

ALLOWED_EXTENSIONS = set(['pdf'])

deals_bp = Blueprint('deals', __name__, url_prefix='/api/v1/deals')


@deals_bp.route('/', methods=['GET', 'POST'])
def create_get_meth():
    args = request.args.to_dict()
    args['api_token'] = os.environ.get('API_TOKEN')
    if request.method == 'POST':
        response = requests.post(os.environ.get('API_URL') + '/deals',
                                 params=args, data=request.form)
    if request.method == 'GET':
        response = requests.get(os.environ.get('API_URL') + '/deals',
                                params=args, data=request.form)
    res_gzip = gzip.compress(response.content)
    return (res_gzip, response.status_code, response.headers.items())


@deals_bp.route('/find', methods=['GET'])
def find_person():
    args = request.args.to_dict()
    args['api_token'] = os.environ.get('API_TOKEN')
    response = requests.get(os.environ.get('API_URL') + '/deals/find',
                            params=args, data=request.form)
    res_gzip = gzip.compress(response.content)
    return (res_gzip, response.status_code, response.headers.items())


@deals_bp.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def delete_get_put_w_id(id):
    pid = str(id)
    args = request.args.to_dict()
    args['api_token'] = os.environ.get('API_TOKEN')
    if request.method == 'GET':
        response = requests.get(os.environ.get('API_URL') + '/deals/' + pid,
                                params=args)
    if request.method == 'PUT':
        response = requests.put(os.environ.get('API_URL') + '/deals/' + pid,
                                params=args, data=request.form)
    if request.method == 'DELETE':
        response = requests.delete(os.environ.get('API_URL') + '/deals/' +
                                   pid, params=args)
    res_gzip = gzip.compress(response.content)
    return (res_gzip, response.status_code, response.headers.items())


@deals_bp.route('/<id>/files', methods=['GET', 'PUT', 'DELETE'])
def list_deal_files(id):
    pid = str(id)
    args = request.args.to_dict()
    args['api_token'] = os.environ.get('API_TOKEN')
    if request.method == 'GET':
        response = requests.get(os.environ.get('API_URL') + '/deals/' + pid +
                                '/files/', params=args)
    res_gzip = gzip.compress(response.content)
    return (res_gzip, response.status_code, response.headers.items())


@deals_bp.route('/file', methods=['POST'])
def upload_deal_file():
    args = request.args.to_dict()
    args['api_token'] = os.environ.get('API_TOKEN')
    if request.method == 'POST':
        data_err_str = ''
        data = request.form.to_dict()
        if not data['deal_id']:
            data_err_str = 'deal_id not included'
        elif not set(data.keys()).issubset(['deal_id']):
            data_err_str = 'no data other than deal_id must be included'
        if 'file' not in request.files:
            return abort(400, description="Please select a pdf file " +
                         data_err_str)
        file = request.files['file']
        if file.filename == '':
            return abort(400, description="Please select a pdf file " +
                         data_err_str)
        if file and allowed_file(file.filename):
            if data_err_str != '':
                return abort(400, description=data_err_str)
            m = MultipartEncoder(fields={'deal_id': data['deal_id'],
                                 'file': (file.filename, file.read(),
                                          'text/plain')})
            response = requests.post(os.environ.get('API_URL') + '/files',
                                     params=args, data=m,
                                     headers={'Content-Type': m.content_type})
            res_gzip = gzip.compress(response.content)
            return (res_gzip, response.status_code, response.headers.items())
        else:
            return abort(400, description="File is not pdf" + data_err_str)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
