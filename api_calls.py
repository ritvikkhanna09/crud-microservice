from flask import Flask, request, json, Response
from crud import MongoAPI
from data import *

app = Flask(__name__)

@app.route('/')
def base():
    return Response(response=json.dumps({"Status": "Running"}),
                    status=200,
                    mimetype='application/json')


@app.route('/mongodb', methods=['GET'])
def mongo_read():
    sender_id = request.headers.get('sender_id')
    body = Document_By_ID(request.json)
    if body is None or body == {} or body.id is None or sender_id is None or sender_id == '':
        return Response(response=json.dumps({"Error": "Please provide correct API information"}),
                        status=400,
                        mimetype='application/json')

    object = MongoAPI(body,sender_id)
    response = object.read()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@app.route('/mongodb', methods=['POST'])
def mongo_write():
    sender_id = request.headers.get('sender_id') 
    body = Document_To_Add(request.json)
    if body is None or body == {} or body.email is None or body.name is None or body.role is None:
        return Response(response=json.dumps({"Error": "Please provide correct API information"}),
                        status=400,
                        mimetype='application/json')
    print('here')
    object = MongoAPI(body,sender_id)
    response = object.write()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

if __name__ == '__main__':
    # initialise sequence and permissions collections
    app.run(debug=True, port=4001, host='0.0.0.0')