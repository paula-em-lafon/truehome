from flask import Blueprint
from flask import request
import requests
import os
import gzip

actividades_bp = Blueprint('actividades', __name__,
                           url_prefix='/api/v1/actividades')


@actividades_bp.route('/', methods=['GET', 'POST'])
def create_get_meth():
    """
    create and retrieve list of activities
    ---
      post:
        summary: Creates an activity.   
        requestBody:
          description: activityID
          required: true
          description: The ID of the user to return.
          content:
            application/json:
              schema:
                subject: 
                  type: integer
                  format: int64
                  minimum: 1
      responses:
        responses:
          '200':    # status code
            description: A JSON array of user names
            content:
              application/json:
                schema:
                  type: array
                  items:
                    type: string
    """
    args = request.args.to_dict()
    args['api_token'] = os.environ.get('API_TOKEN')
    if request.method == 'POST':
        response = requests.post(os.environ.get('API_URL') + '/activities',
                                 params=args, data=request.form)
    if request.method == 'GET':
        response = requests.get(os.environ.get('API_URL') + '/activities',
                                params=args, data=request.form)
    res_gzip = gzip.compress(response.content)
    return (res_gzip, response.status_code, response.headers.items())


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
    res_gzip = gzip.compress(response.content)
    return (res_gzip, response.status_code, response.headers.items())
