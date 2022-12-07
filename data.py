class Document_To_Add:
    def __init__(self, data):
        self.id = None
        self.name = None if data['name'] == {} else data['name']
        self.role = None if data['role'] == {} else data['role']
        self.email = None if data['email'] == {} else data['email']

class Document_By_ID:
    def __init__(self, data):
        self.id = None if not data or data['id'] == {}  else data['id']

class Document_To_Update:
    def __init__(self, data):
        self.id = None if data['id'] == {} else data['id']
        self.name = None if data['name'] == {} else data['name']
        self.role = None if data['role'] == {} else data['role']
        self.email = None if data['email'] == {} else data['email']
