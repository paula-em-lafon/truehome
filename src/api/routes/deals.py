from flask import Blueprint
from flask import request
import requests
import os
import gzip

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
