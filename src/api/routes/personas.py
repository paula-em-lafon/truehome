from flask import Blueprint
from flask import request
import requests
import os
import gzip

personas_bp = Blueprint('personas', __name__, url_prefix='/api/v1/personas')


@personas_bp.route('/', methods=['GET', 'POST'])
def create_get_meth():
    args = request.args.to_dict()
    args['api_token'] = os.environ.get('API_TOKEN')
    if request.method == 'POST':
        response = requests.post(os.environ.get('API_URL') + '/persons',
                                 params=args, data=request.form)
    if request.method == 'GET':
        response = requests.get(os.environ.get('API_URL') + '/persons',
                                params=args, data=request.form)
    res_gzip = gzip.compress(response.content)
    return (res_gzip, response.status_code, response.headers.items())


@personas_bp.route('/find', methods=['GET'])
def find_person():
    args = request.args.to_dict()
    args['api_token'] = os.environ.get('API_TOKEN')
    response = requests.get(os.environ.get('API_URL') + '/persons/find',
                            params=args, data=request.form)
    res_gzip = gzip.compress(response.content)
    return (res_gzip, response.status_code, response.headers.items())


@personas_bp.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def delete_get_put_w_id(id):
    pid = str(id)
    args = request.args.to_dict()
    args['api_token'] = os.environ.get('API_TOKEN')
    if request.method == 'GET':
        response = requests.get(os.environ.get('API_URL') + '/persons/' + pid,
                                params=args)
    if request.method == 'PUT':
        response = requests.put(os.environ.get('API_URL') + '/persons/' + pid,
                                params=args, data=request.form)
    if request.method == 'DELETE':
        response = requests.delete(os.environ.get('API_URL') + '/persons/' +
                                   pid, params=args)
    res_gzip = gzip.compress(response.content)
    return (res_gzip, response.status_code, response.headers.items())


@personas_bp.route('/<id>/actividades', methods=['GET'])
def get_activities_by_user(id):
    pid = str(id)
    args = request.args.to_dict()
    args['api_token'] = os.environ.get('API_TOKEN')
    response = requests.get(os.environ.get('API_URL') + '/persons/' +
                            pid + '/activities', params=args)
    res_gzip = gzip.compress(response.content)
    return (res_gzip, response.status_code, response.headers.items())


@personas_bp.route('/<id>/deals', methods=['GET'])
def get_deals_by_user(id):
    pid = str(id)
    args = request.args.to_dict()
    args['api_token'] = os.environ.get('API_TOKEN')
    response = requests.get(os.environ.get('API_URL') + '/persons/' +
                            pid + '/deals', params=args)
    res_gzip = gzip.compress(response.content)
    return (res_gzip, response.status_code, response.headers.items())
