from flask import Flask, request, json, Response
from crud import MongoAPI
from classes import *

app = Flask(__name__)

@app.route('/')
def base():
    return Response(response=json.dumps({"Status": "Running"}),
                    status=200,
                    mimetype='application/json')


@app.route('/user', methods=['GET'])
def user_read():
    
    # retrieve header and body 
    sender_id = request.headers.get('sender_id')
    body = Document_By_ID(request.json)

    # api request format checks
    if body is None or body == {} or body.id is None or sender_id is None or sender_id == '':
        return Response(response=json.dumps({"Error": "Please provide correct API information"}),
                        status=400,
                        mimetype='application/json')

    # create MongoAPI object
    object = MongoAPI(body,sender_id)
    response = object.read()

    # return response
    return Response(response=json.dumps(response),
                    status=response['status'],
                    mimetype='application/json')


@app.route('/user', methods=['POST'])
def user_write():

    # retrieve header and body 
    sender_id = request.headers.get('sender_id') 
    body = Document_To_Add(request.json)

    # api request format checks
    if body is None or body == {} or body.email is None or body.name is None \
        or body.role is None or body.role not in ['admin','modifier','watcher']:
        return Response(response=json.dumps({"Error": "Please provide correct API information"}),
                        status=400,
                        mimetype='application/json')

    # create MongoAPI object
    object = MongoAPI(body,sender_id)
    response = object.write()

    # return response
    return Response(response=json.dumps(response),
                    status=response['status'],
                    mimetype='application/json')

@app.route('/user', methods=['DELETE'])
def user_delete():

    # retrieve header and body 
    sender_id = request.headers.get('sender_id')
    body = Document_By_ID(request.json)

    # api request format checks
    if body is None or body == {} or body.id is None or sender_id is None or sender_id == '':
        return Response(response=json.dumps({"Error": "Please provide correct API information"}),
                        status=400,
                        mimetype='application/json')

    # create MongoAPI object
    object = MongoAPI(body,sender_id)
    response = object.delete()

    # return response
    return Response(response=json.dumps(response),
                    status=response['status'],
                    mimetype='application/json')

@app.route('/user', methods=['PUT'])
def user_update():

    # retrieve header and body 
    sender_id = request.headers.get('sender_id')
    body = Document_To_Update(request.json)

    # api request format checks
    if body is None or body == {} or body.id is None or sender_id is None or sender_id == '':
        return Response(response=json.dumps({"Error": "Please provide correct API information"}),
                        status=400,
                        mimetype='application/json')

    # create MongoAPI object
    object = MongoAPI(body, sender_id)
    response = object.update()

    # return response
    return Response(response=json.dumps(response),
                    status=response['status'],
                    mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=False, port=4001, host='0.0.0.0')