import unittest
import requests
import json 
import random
import string


api_url = "http://0.0.0.0:4001/"

"""
run by command `python integration_tests.py -v`
"""


class API_Test(unittest.TestCase):

    """
    Integration Test 0: connection test
    """
    def test0_connection(self):
        response = requests.get(api_url)
        response_code = response.status_code
        self.assertEqual(response_code , 200)


    """
    Integration Test 1: User Creation / POST
        - creates a user successfully
        - creates the user again = 409 error
        - delete the user 
    """
    def test1(self):
        name = get_random_string()
        email = get_random_string()
        response = requests.post( api_url+'user',
                    json={
                            "name" : name,
                            "role" : "modifier",
                            "email" : email
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)
        user_id = str(response_json['data']['id'])

        response = requests.post( api_url+'user',
                    json={
                            "name" : name,
                            "role" : "modifier",
                            "email" : email
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 409)

        response = requests.delete( api_url+'user',
                    json={
                            "id" : user_id
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 200)

    """
    Integration Test 2: User Deletion / DELETE
        - creates a user successfully
        - delete the user 
        - delete the user = 404 error
    """
    def test2(self):

        response = requests.post( api_url+'user',
                    json={
                            "name" : get_random_string(),
                            "role" : "watcher",
                            "email" : get_random_string()
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)
        user_id = str(response_json['data']['id'])

        response = requests.delete( api_url+'user',
                    json={
                            "id" : user_id
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 200)
        

        response = requests.delete( api_url+'user',
                    json={
                            "id" : user_id
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 404)


    """
    Integration Test 3: Required Fields
        - name, email, role are required fields
    """
    def test3(self):
        response = requests.post( api_url+'user',
            json={
                    "name" : get_random_string(),
                    "email" : get_random_string()
                    },
                headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 400)


    """
    Integration Test 4: User Updation / PUT
        - create 1 users
        - update user:
            - by all fields
            - by specifing only few fields
        - update invalid id = 404 error
        - delete the user
    """

    def test4(self):
        response = requests.post( api_url+'user',
                    json={
                            "name" : get_random_string(),
                            "role" : "modifier",
                            "email" : get_random_string()
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 200)
        response_json = json.loads(response.text)
        user_id = str(response_json['data']['id'])


        response = requests.put( api_url+'user',
                    json={
                            "id" : user_id,
                            "name" : get_random_string(),
                            "role" : "watcher",
                            "email" : get_random_string()
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 200)


        response = requests.put( api_url+'user',
                    json={
                            "id" : user_id,
                            "email" : get_random_string()
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 200)

        response = requests.put( api_url+'user',
                    json={
                            "id" : user_id,
                            "role" : "modifier"
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 200)

        response = requests.put( api_url+'user',
                    json={
                            "id" : "0000",
                            "name" : get_random_string(),
                            "role" : "watcher",
                            "email" : get_random_string()
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 404)
        
        response = requests.delete( api_url+'user',
                    json={
                            "id" : user_id
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)


    """
    Integration Test 5: List Users / GET
        - create 2 users
        - list:
            - using valid id
            - invalid id = list all other users
        - delete 2 users
    """
    def test5(self):
        response = requests.post( api_url+'user',
                    json={
                            "name" : get_random_string(),
                            "role" : "watcher",
                            "email" : get_random_string()
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 200)
        response_json = json.loads(response.text)
        user_id_1 = str(response_json['data']['id'])


        response = requests.post( api_url+'user',
                    json={
                            "name" : get_random_string(),
                            "role" : "admin",
                            "email" : get_random_string()
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 200)
        response_json = json.loads(response.text)
        user_id_2 = str(response_json['data']['id'])

        
        response = requests.get( api_url+'user',
                    json={'id':user_id_1},
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)
        self.assertEqual(len(response_json['data']) == 1 , True)

        response = requests.get( api_url+'user',
                    json={'id':'0000'},
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)
        self.assertEqual(len(response_json['data']) >= 1 , True)

        response = requests.delete( api_url+'user',
                    json={
                            "id" : user_id_1
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)

        response = requests.delete( api_url+'user',
                    json={
                            "id" : user_id_2
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)

    """
    Integration Test 6: Users Permissions
        - create 3 users of each ole
        - perform actions per user and checks
            - watcher can only GET
            - modifier can only PUT GET POST
            - admin can only PUT GET POST DELETE
        - delete the 3 users
    """

    def test6(self):
        

        response = requests.post( api_url+'user',
                    json={
                            "name" : get_random_string(),
                            "role" : "admin",
                            "email" : get_random_string()
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        self.assertEqual(response_code , 200)
        response_json = json.loads(response.text)
        admin_id = str(response_json['data']['id'])


        response = requests.post( api_url+'user',
                    json={
                            "name" : get_random_string(),
                            "role" : "modifier",
                            "email" : get_random_string()
                            },
                    headers={'sender-id': admin_id})
        response_code = response.status_code
        self.assertEqual(response_code , 200)
        response_json = json.loads(response.text)
        modifier_id = str(response_json['data']['id'])

        response = requests.post( api_url+'user',
                    json={
                            "name" : get_random_string(),
                            "role" : "watcher",
                            "email" : get_random_string()
                            },
                    headers={'sender-id': admin_id})
        response_code = response.status_code
        self.assertEqual(response_code , 200)
        response_json = json.loads(response.text)
        watcher_id = str(response_json['data']['id'])

        """
        watcher checks
        """
        response = requests.post( api_url+'user',
                    json={
                            "name" : get_random_string(),
                            "role" : "watcher",
                            "email" : get_random_string()
                            },
                    headers={'sender-id': watcher_id})
        response_code = response.status_code
        self.assertEqual(response_code , 403)

        response = requests.put( api_url+'user',
                    json={
                            "id" : modifier_id,
                            "role" : "watcher",
                            },
                    headers={'sender-id': watcher_id})
        response_code = response.status_code
        self.assertEqual(response_code , 403)

        response = requests.delete( api_url+'user',
                    json={
                            "id" : watcher_id
                            },
                    headers={'sender-id': watcher_id})
        response_code = response.status_code
        self.assertEqual(response_code , 403)

        response = requests.get( api_url+'user',
                    json={'id':"0000"},
                    headers={'sender-id': watcher_id})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)
        self.assertEqual(len(response_json['data']) >= 1 , True)

        """
        modifier checks
        """

        response = requests.post( api_url+'user',
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

        response = requests.put( api_url+'user',
                    json={
                            "id" : watcher_id,
                            "role" : "modifier",
                            },
                    headers={'sender-id': modifier_id})
        response_code = response.status_code
        self.assertEqual(response_code , 200)

        response = requests.delete( api_url+'user',
                    json={
                            "id" : user_1
                            },
                    headers={'sender-id': modifier_id})
        response_code = response.status_code
        self.assertEqual(response_code , 403)

        response = requests.get( api_url+'user',
                    json={'id':"0000"},
                    headers={'sender-id': modifier_id})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)
        self.assertEqual(len(response_json['data']) >= 1 , True)

        """
        admin checks
        """

        response = requests.post( api_url+'user',
                    json={
                            "name" : get_random_string(),
                            "role" : "modifier",
                            "email" : get_random_string()
                            },
                    headers={'sender-id': admin_id})
        response_code = response.status_code
        self.assertEqual(response_code , 200)

        response = requests.put( api_url+'user',
                    json={
                            "id" : watcher_id,
                            "role" : "watcher",
                            },
                    headers={'sender-id': admin_id})
        response_code = response.status_code
        self.assertEqual(response_code , 200)

        response = requests.delete( api_url+'user',
                    json={
                            "id" : user_1
                            },
                    headers={'sender-id': admin_id})
        response_code = response.status_code
        self.assertEqual(response_code , 200)

        response = requests.get( api_url+'user',
                    json={'id':"0000"},
                    headers={'sender-id': admin_id})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)
        self.assertEqual(len(response_json['data']) >= 1 , True)

        """
        delete the created users
        """
        response = requests.delete( api_url+'user',
                    json={
                            "id" : modifier_id
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)

        response = requests.delete( api_url+'user',
                    json={
                            "id" : watcher_id
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)

        response = requests.delete( api_url+'user',
                    json={
                            "id" : admin_id
                            },
                    headers={'sender-id': '1000'})
        response_code = response.status_code
        response_json = json.loads(response.text)
        self.assertEqual(response_code , 200)

def get_random_string():
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))

if __name__ == '__main__':
    unittest.main()