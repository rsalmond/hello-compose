from flask import Blueprint
from flask import current_app, jsonify, request
from hello.models import Greeting
from hello.errors import APIInvalidData, APIAlreadyExists

blueprint = Blueprint(__name__, __name__)

@blueprint.route('/health')
def index():
    return jsonify({'Status': 'OK'})

@blueprint.route('/hello/v1/greetings', methods=['GET', 'POST', 'OPTIONS'])
def greetings():
    if request.method == 'OPTIONS':
        return jsonify({'Methods': ['GET', 'POST']})

    elif request.method == 'POST':
        # create a new greeting
        if request.content_type != 'application/json':
            return jsonify({'Error': 'Updates must be JSON documents (content-type: application/json)'}), 415

        try:
            greeting = Greeting.create_from_api(request.json)

        except APIInvalidData as e:
            return jsonify({'Error': e.message}), 400

        except APIAlreadyExists as e:
            return jsonify({'Error': e.message, 'GreetingId': e.id}), 409

        return jsonify({'GreetingId': greeting.id}), 201

    elif request.method == 'GET':
        # fetch all greetings
        return Greeting.all_to_json()

@blueprint.route('/hello/v1/greetings/<int:greeting_id>', methods=['GET', 'PUT', 'OPTIONS', 'DELETE'])
def greeting(greeting_id):
    greeting = Greeting.by_id(greeting_id)
    if not greeting:
        return jsonify({'Error': 'Greeting with id {id} not found'.format(id=greeting_id)}), 404

    if request.method == 'OPTIONS':
        return jsonify({'Methods': ['GET', 'PUT']})

    elif request.method == 'GET':
        # fetch a single greeting
        return greeting.to_json()

    elif request.method == 'PUT':
        # update a single greeting
        if request.content_type != 'application/json':
            return jsonify({'Error': 'Updates must be JSON documents (content-type: application/json)'}), 415

        if greeting.update_from_api(request.json):
            status = 'updated'
        else:
            status = 'unmodified'

        return greeting.to_json(status=status)
        
    elif request.method == 'DELETE':
        # delete a single greeting
        greeting.delete()
        return greeting.to_json(status='deleted')
        
@blueprint.app_errorhandler(405)
def method_not_allowed(err):
    return jsonify({'Error': '{}'.format(err)}), 405
