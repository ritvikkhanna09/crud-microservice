from api_calls import app
from flask import json
import unittest
import time

class API_Test(unittest.TestCase):

    """
    Unit Test 0: connection test
    """
    def test_connection(self):
        tester = app.test_client(self)
        response = tester.get('/')
        response_code = response.status_code
        response_mimetype = response.mimetype
        self.assertEqual(response_code , 200)
        self.assertEqual(response_mimetype , 'application/json')


    """
    Unit Test 1: User Creation / POST
        - creates a user successfully
        - creates the user again = 409 error
        - delete the user 
    """
    def test1(self):
        tester = app.test_client(self)
        response = tester.post('/user',
                    json={
                            "name" : "johnson",
                            "role" : "modifier",
                            "email" : "john@api.com"
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)
        user_id = str(response_json['data']['id'])

        response = tester.post('/user',
                    json={
                            "name" : "johnson",
                            "role" : "modifier",
                            "email" : "john@api.com"
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 409)

        response = tester.delete('/user',
                    json={
                            "id" : user_id
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 200)

        response = tester.post('/user',
            json={
                    "name" : "johnson",
                    "email" : "john@api.com"
                    },
                headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 400)
    

    """
    Unit Test 2: User Deletion / DELETE
        - creates a user successfully
        - delete the user 
        - delete the user = 404 error
    """
    def test2(self):
        tester = app.test_client(self)
        response = tester.post('/user',
                    json={
                            "name" : "ben",
                            "role" : "watcher",
                            "email" : "ben@api.com"
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)
        user_id = str(response_json['data']['id'])

        response = tester.delete('/user',
                    json={
                            "id" : user_id
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 200)
        

        response = tester.delete('/user',
                    json={
                            "id" : user_id
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 404)


    """
    Unit Test 3: Required Fields
        - name, email, role are required fields
    """
    def test3(self):
        tester = app.test_client(self)
        response = tester.post('/user',
            json={
                    "name" : "johnson",
                    "email" : "john@api.com"
                    },
                headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 400)


    """
    Unit Test 4: User Updation / PUT
        - create 1 users
        - update user:
            - by all fields
            - by specifing only few fields
        - update invalid id = 404 error
        - delete the user
    """

    def test4(self):
        tester = app.test_client(self)


        response = tester.post('/user',
                    json={
                            "name" : "Gini",
                            "role" : "modifier",
                            "email" : "gini@api.com"
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 200)
        response_json = json.loads(response.text)
        user_id = str(response_json['data']['id'])


        response = tester.put('/user',
                    json={
                            "id" : user_id,
                            "name" : "Adam",
                            "role" : "watcher",
                            "email" : "adam@api.com"
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 200)


        response = tester.put('/user',
                    json={
                            "id" : user_id,
                            "email" : "adam123@api.com"
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 200)

        response = tester.put('/user',
                    json={
                            "id" : user_id,
                            "role" : "modifier"
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 200)

        response = tester.put('/user',
                    json={
                            "id" : "0000",
                            "name" : "Adam",
                            "role" : "watcher",
                            "email" : "adam@api.com"
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 404)
        
        response = tester.delete('/user',
                    json={
                            "id" : user_id
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)


    """
    Unit Test 5: List Users / GET
        - create 2 users
        - list:
            - using valid id
            - invalid id = list all other users
        - delete 2 users
    """
    def test5(self):
        tester = app.test_client(self)


        response = tester.post('/user',
                    json={
                            "name" : "Sam",
                            "role" : "watcher",
                            "email" : "sam@api.com"
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 200)
        response_json = json.loads(response.text)
        user_id_1 = str(response_json['data']['id'])


        response = tester.post('/user',
                    json={
                            "name" : "olive",
                            "role" : "admin",
                            "email" : "olive@api.com"
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 200)
        response_json = json.loads(response.text)
        user_id_2 = str(response_json['data']['id'])

        
        response = tester.get('/user',
                    json={'id':user_id_1},
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)
        self.assertEqual(len(response_json['data']) == 1 , True)

        response = tester.get('/user',
                    json={'id':'0000'},
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)
        self.assertEqual(len(response_json['data']) >= 1 , True)

        response = tester.delete('/user',
                    json={
                            "id" : user_id_1
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)

        response = tester.delete('/user',
                    json={
                            "id" : user_id_2
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)

    """
    Unit Test 6: Users Permissions
        - create 3 users of each ole
        - perform actions per user and checks
            - watcher can only GET
            - modifier can only PUT GET POST
            - admin can only PUT GET POST DELETE
        - delete the 3 users
    """

    def test6(self):
        tester = app.test_client(self)

        response = tester.post('/user',
                    json={
                            "name" : "sam",
                            "role" : "admin",
                            "email" : "sam@api.com"
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 200)
        response_json = json.loads(response.text)
        admin_id = str(response_json['data']['id'])


        response = tester.post('/user',
                    json={
                            "name" : "olive",
                            "role" : "modifier",
                            "email" : "olive@api.com"
                            },
                    headers={'sender-id': admin_id})
        response_code = response.status_code
        self.assertEqual(response_code , 200)
        response_json = json.loads(response.text)
        modifier_id = str(response_json['data']['id'])

        response = tester.post('/user',
                    json={
                            "name" : "dave",
                            "role" : "watcher",
                            "email" : "dave@api.com"
                            },
                    headers={'sender-id': admin_id})
        response_code = response.status_code
        self.assertEqual(response_code , 200)
        response_json = json.loads(response.text)
        watcher_id = str(response_json['data']['id'])

        """
        watcher checks
        """
        response = tester.post('/user',
                    json={
                            "name" : "lilly",
                            "role" : "watcher",
                            "email" : "lilly@api.com"
                            },
                    headers={'sender-id': watcher_id})
        response_code = response.status_code
        self.assertEqual(response_code , 401)

        response = tester.put('/user',
                    json={
                            "id" : modifier_id,
                            "role" : "watcher",
                            },
                    headers={'sender-id': watcher_id})
        response_code = response.status_code
        self.assertEqual(response_code , 401)

        response = tester.delete('/user',
                    json={
                            "id" : watcher_id
                            },
                    headers={'sender-id': watcher_id})
        response_code = response.status_code
        self.assertEqual(response_code , 401)

        response = tester.get('/user',
                    json={'id':"0000"},
                    headers={'sender-id': watcher_id})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)
        self.assertEqual(len(response_json['data']) >= 1 , True)

        """
        modifier checks
        """

        response = tester.post('/user',
                    json={
                            "name" : "lilly",
                            "role" : "modifier",
                            "email" : "lilly@api.com"
                            },
                    headers={'sender-id': modifier_id})
        response_code = response.status_code
        self.assertEqual(response_code , 200)
        response_json = json.loads(response.text)
        user_1 = str(response_json['data']['id'])

        response = tester.put('/user',
                    json={
                            "id" : watcher_id,
                            "role" : "modifier",
                            },
                    headers={'sender-id': modifier_id})
        response_code = response.status_code
        self.assertEqual(response_code , 200)

        response = tester.delete('/user',
                    json={
                            "id" : user_1
                            },
                    headers={'sender-id': modifier_id})
        response_code = response.status_code
        self.assertEqual(response_code , 401)

        response = tester.get('/user',
                    json={'id':"0000"},
                    headers={'sender-id': modifier_id})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)
        self.assertEqual(len(response_json['data']) >= 1 , True)

        """
        admin checks
        """

        response = tester.post('/user',
                    json={
                            "name" : "lilly",
                            "role" : "modifier",
                            "email" : "lilly@api.com"
                            },
                    headers={'sender-id': admin_id})
        response_code = response.status_code
        self.assertEqual(response_code , 409)

        response = tester.put('/user',
                    json={
                            "id" : watcher_id,
                            "role" : "watcher",
                            },
                    headers={'sender-id': admin_id})
        response_code = response.status_code
        self.assertEqual(response_code , 200)

        response = tester.delete('/user',
                    json={
                            "id" : user_1
                            },
                    headers={'sender-id': admin_id})
        response_code = response.status_code
        self.assertEqual(response_code , 200)

        response = tester.get('/user',
                    json={'id':"0000"},
                    headers={'sender-id': admin_id})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)
        self.assertEqual(len(response_json['data']) >= 1 , True)

        """
        delete the created users
        """
        response = tester.delete('/user',
                    json={
                            "id" : modifier_id
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)

        response = tester.delete('/user',
                    json={
                            "id" : watcher_id
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)

        response = tester.delete('/user',
                    json={
                            "id" : admin_id
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)

if __name__ == '__main__':
    unittest.main()