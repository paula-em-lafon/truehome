from flask import Blueprint
from flask import request
from flask import jsonify
import requests
import json
import ast
import os

actividades_bp = Blueprint('actividades', __name__,
                           url_prefix='/api/v1/actividades')


@actividades_bp.route('/', methods=['GET', 'POST'])
def create_get_meth():
    args = request.args.to_dict()
    args['api_token'] = os.environ.get('API_TOKEN')
    if request.method == 'POST':
        response = requests.post(os.environ.get('API_URL') + '/activities',
                                 params=args, data=request.form)
    if request.method == 'GET':
        response = requests.get(os.environ.get('API_URL') + '/activities',
                                params=args, data=request.form)
    res_dict = response.json()
    return (jsonify(res_dict), response.status_code)


@actividades_bp.route('/find', methods=['GET'])
def find_activity():
    args = request.args.to_dict()
    args['api_token'] = os.environ.get('API_TOKEN')
    response = requests.get(os.environ.get('API_URL') + '/activities/find',
                            params=args, data=request.form)
    res_dict = response.json()
    return (jsonify(res_dict), response.status_code)


@actividades_bp.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def delete_get_put_w_id(id):
    pid = str(id)
    args = request.args.to_dict()
    args['api_token'] = os.environ.get('API_TOKEN')
    if request.method == 'GET':
        response = requests.get(os.environ.get('API_URL') + '/activities/' +
                                pid, params=args)
    if request.method == 'PUT':
        response = requests.put(os.environ.get('API_URL') + '/activities/' +
                                pid, params=args, data=request.form)
    if request.method == 'DELETE':
        response = requests.delete(os.environ.get('API_URL') + '/activities/' +
                                   pid, params=args)
    res_dict = response.json()
    return (jsonify(res_dict), response.status_code)
