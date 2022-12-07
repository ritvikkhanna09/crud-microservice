
import json

class Document_To_Add:
    def __init__(self, data):
        self.id = None
        self.name = None if data.get('name') is None else data['name']
        self.role = None if data.get('role') is None else data['role']
        self.email = None if data.get('email') is None  else data['email']

class Document_By_ID:
    def __init__(self, data):
        self.id = None if data.get('id') is None else data['id']

class Document_To_Update:
    def __init__(self, data):
        self.id = None if data.get('id') is None else data['id']
        self.name = None if data.get('name') is None else data['name']
        self.role = None if data.get('role') is None else data['role']
        self.email = None if data.get('email') is None  else data['email']

    def to_json(self):
        json_object = json.loads(json.dumps(self, default=lambda o: o.__dict__, 
            allow_nan=False))
        for key, value in list(json_object.items()):
            if value is None:
                del json_object[key]
        return json_object