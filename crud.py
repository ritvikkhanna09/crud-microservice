from flask import Flask, request, json, Response
from pymongo import MongoClient
import logging as log
from data import *

permission_dict = {'admin':['PUT','GET','POST','DELETE'], 'modifier':['PUT','GET','POST'],'watcher':['GET']}

class MongoAPI:
    def __init__(self, body, sender_id):
        # log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s:\n%(message)s\n')
        # self.client = MongoClient("mongodb://localhost:27017/")  # When only Mongo DB is running on Docker.
        self.client = MongoClient("mongodb://0.0.0.0:4004/")     # When both Mongo and This application is running on
                                                                    # Docker and we are using Docker Compose
        cursor = self.client['users']
        self.information = cursor['information']
        self.roles = cursor['roles']
        self.permissions = cursor['permissions']
        self.sequence = cursor['sequence']
        self.initialize_collections()
        self.body = body
        self.sender_id = sender_id

    def initialize_collections(self):
        sequence = self.sequence.count_documents({})
        if(sequence == 0):
            self.sequence.insert_one({'counter':'1000'})
        
        permissions = self.permissions.count_documents({})
        if(permissions == 0):
            self.permissions.insert_one({'role':'admin', 'actions':['PUT','GET','POST','DELETE']})
            self.permissions.insert_one({'role':'modifier', 'actions':['PUT','GET','POST']})
            self.permissions.insert_one({'role':'watcher', 'actions':['GET']})
        
        roles = self.roles.count_documents({})
        if(roles == 0):
            self.roles.insert_one({'id':'1000','role':'admin'})
        
    
    def get_permission_list(self,role):
        document = self.permissions.find_one({'role':role})
        return document['actions']

    
    def get_next_id(self):
        sequence_document = (self.sequence.find())[0]
        counter = sequence_document['counter']
        next_counter = str(int(counter)+1)
        response = self.sequence.update_one({}, { '$set': { 'counter' : next_counter} } )
        return next_counter

    def check_sender_permission(self, action):
        sender_document = self.roles.find_one({'id':self.sender_id})
        print(sender_document,self.sender_id)
        if sender_document is None:
            return False
        else:
            permission = sender_document['role']
            if action not in self.get_permission_list(permission):
                # permission error
                return False
        return True

    def read(self):
        # find the permission tuple form permission collection for this user and validate
        if self.check_sender_permission('GET') is False:
            return {'Status': 'sender permission error'}
        
        print(self.body.id)
        document = self.information.find_one({'id':self.body.id})
        output = {}
        if document is None:
            # return all the user list
            documents = self.information.find()
            if documents is not None:
                output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        else:
            output = {item: document[item] for item in document if item != '_id'}

        return output


    def write(self):
        if self.check_sender_permission('POST') is False:
            return {'Status': 'sender permission error'}

        # assign next available IDgoto
        unique_id = self.get_next_id()
        while(self.roles.find_one({'id':unique_id})):
            unique_id = self.get_next_id()
        
        self.body.id = unique_id
        
        response1 = self.information.insert_one(self.body.__dict__)
        response2 = self.roles.insert_one({'role':self.body.role ,'id': self.body.id})

        if not response1 or not response2:
            output = {'Status': 'Error in Write Operation'}
        else:
            output = {'Status': 'Successful Write Operation',
                        'name': str(self.body.name),
                        'id': str(self.body.id),
                        }
        return output

    def delete(self):
        # find the permission tuple form permission collection for this user and validate
        if self.check_sender_permission('DELETE') is False:
            return {'Status': 'sender permission error'}

        # first find to check if document available or not
        find_response_user = self.information.find_one({'id': self.body.id})
        if find_response_user is None:
            output = {'Status': 'Document(User) not found'}
            return output
        find_response_role = self.roles.find_one({'id': self.body.id})
        if find_response_role is None:
            output = {'Status': 'Document(Roles) not found'}
            return output
        
        # Now delete the document
        response1 = self.information.delete_one(self.body.__dict__)
        response2 = self.roles.delete_one(self.body.__dict__)

        if response1.deleted_count <= 0 or response2.deleted_count <= 0:
            output = {'Status': 'Error deleting document'}
        else:
            output = {'Status': 'Successful Delete Operation'}
        return output


    def update(self):
        # find the permission tuple form permission collection for this user and validate
        if self.check_sender_permission('PUT') is False:
            return {'Status': 'sender permission error'}
        
        filter = {'id':self.body.id}
        update = {"$set": self.body.to_json()}
        
         # first find to check if document available or not
        find_response_user = self.information.find_one({'id': self.body.id})
        if find_response_user is None:
            output = {'Status': 'Document(User) not found'}
            return output
        if self.body.role is not None:
            find_response_role = self.roles.find_one({'id': self.body.id})
            if find_response_role is None:
                output = {'Status': 'Document(Roles) not found'}
                return output



        response1 = self.information.update_one(filter, update)
        response2 = None

        if self.body.role is not None:
            response2 = self.roles.update_one(filter, {"$set": {'role':self.body.role }} )

        if response1.modified_count == 0:
            output = {'Status': 'Document to not found'} if response1.matched_count == 0 \
                else {'Status': 'Document already exists'}
        elif response2 is not None and response2.modified_count == 0:
            output = {'Status': 'Error updating document'} 
        else:
            output = {'Status': 'Successful Update Operation'}
        return output