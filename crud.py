# Python Copyright Information                                                                                  
# Copyright (c) 2022 Ritvik Khanna                                                         
# All Rights Reserved.                                                                                          
                       
from flask import Flask, request, json, Response
from pymongo import MongoClient
from classes import *

class MongoAPI:
    def __init__(self, body, sender_id):
        # self.client = MongoClient("mongodb://0.0.0.0:27017/")
        self.client = MongoClient("mongodb://mongodb_service:27017/")


        # get database/collection cursors
        cursor = self.client['users']
        self.information = cursor['information']
        self.roles = cursor['roles']
        self.permissions = cursor['permissions']
        self.sequence = cursor['sequence']
        self.initialize_collections()

        # store request data 
        self.body = body
        self.sender_id = sender_id

    """
    Function to initialise permissions and sequence collection if does
    not exists or is empty
    """
    def initialize_collections(self):
        sequence = self.sequence.count_documents({})
        information = self.information.count_documents({})
        if sequence == 0:
            self.sequence.insert_one({'counter':'1000'})
        elif information == 0:
            self.sequence.update_one({}, { '$set': { 'counter' : '1000'} } )
        
        permissions = self.permissions.count_documents({})
        if permissions == 0:
            self.permissions.insert_one({'role':'admin', 'actions':['PUT','GET','POST','DELETE']})
            self.permissions.insert_one({'role':'modifier', 'actions':['PUT','GET','POST']})
            self.permissions.insert_one({'role':'watcher', 'actions':['GET']})
        
        # we add a super admin with id:1000. To be used initially to create
        # first admin/users
        roles = self.roles.count_documents({})
        if roles == 0:
            self.roles.insert_one({'id':'1000','role':'admin'})
        
    
    def get_permission_list(self,role):
        document = self.permissions.find_one({'role':role})
        return document['actions']

    """
    Function to check if sender has permission to perfrom action
    """
    def check_sender_permission(self, action):
        sender_document = self.roles.find_one({'id':self.sender_id})
        if sender_document is None:
            return False
        else:
            permission = sender_document['role']
            if action not in self.get_permission_list(permission):
                return False
        return True

    """
    Function to assign next available unique id to user
    """
    def get_next_id(self):
        sequence_document = (self.sequence.find())[0]
        counter = sequence_document['counter']
        next_counter = str(int(counter)+1)
        self.sequence.update_one({}, { '$set': { 'counter' : next_counter} } )
        return next_counter
    
    """
    Function to perform READ
    """
    def read(self):
        # sender action permission check
        if self.check_sender_permission('GET') is False:
            output = {'error': 'sender permission error', 'status': '403'}
            return output
           
        document = self.information.find_one({'id':self.body.id})
        
        if document is None:
            # return all users
            documents = self.information.find()
            if documents is not None:
                output = {'warning': 'document does not exist', 
                            'data' : 
                                [{item: data[item] for item in data if item != '_id'} \
                                    for data in documents],
                                    'status': '200'}
        else:
            # return found users
            output = {item: document[item] for item in document if item != '_id'}
            output = {'message': 'read operation success', 
                            'data' : 
                                [{item: document[item] for item in document if item != '_id'}],
                            'status': '200'}

        return output

    """
    Function to perform WRITE
    """
    def write(self):
        # sender action permission check
        if self.check_sender_permission('POST') is False:
            output = {'error': 'sender permission error', 'status': '403'}
            return output

        # first, find to check if document already exists
        document_exists = self.information.find_one(self.body.to_json())
        if document_exists is not None:
            output = {'error': 'document already exists', 'status': '409'}
            return output

        # assign next available unique id
        unique_id = self.get_next_id()
        while(self.roles.find_one({'id':unique_id})):
            unique_id = self.get_next_id()
        self.body.id = unique_id
        
        # insert to both information and role collection
        response1 = self.information.insert_one(self.body.__dict__)
        response2 = self.roles.insert_one({'role':self.body.role ,'id': self.body.id})

        if not response1 or not response2:
            output = {'error': 'write operation failed', 'status': '400'}
        else:
            output = {'message': 'write operation success',
                     'data':{
                        'name': str(self.body.name),
                        'id': str(self.body.id),
                        },
                        'status': '200'
                    }

        return output

    def delete(self):
        # sender action permission check
        if self.check_sender_permission('DELETE') is False:
            output = {'error': 'sender permission error', 'status': '403'}
            return output

        # first, find to check if document exists
        find_response_user = self.information.find_one({'id': self.body.id})
        if find_response_user is None:
            output = {'error': 'document(in users) does not exists', 'status': '404'}
            return output
        find_response_role = self.roles.find_one({'id': self.body.id})
        if find_response_role is None:
            output = {'error': 'document(in roles) does not exists', 'status': '404'}
            return output
        
        # Now delete the document
        response1 = self.information.delete_one(self.body.__dict__)
        response2 = self.roles.delete_one(self.body.__dict__)

        if response1.deleted_count <= 0 or response2.deleted_count <= 0:
            output = {'error': 'delete operation failed', 'status': '400'}
        else:
            output = {'message': 'delete operation success', 'status': '200'}

        return output


    def update(self):
        # sender action permission check
        if self.check_sender_permission('PUT') is False:
            output = {'error': 'sender permission error', 'status': '403'}
            return output
        
        filter = {'id':self.body.id}
        update = {"$set": self.body.to_json()}
        
        # first, find to check if document exists
        find_response_user = self.information.find_one({'id': self.body.id})
        if find_response_user is None:
            output = {'error': 'document(in users) does not exists', 'status': '404'}
            return output
        if self.body.role is not None:
            find_response_role = self.roles.find_one({'id': self.body.id})
            if find_response_role is None:
                output = {'error': 'document(in roles) does not exists', 'status': '404'}
                return output

        # Now update the document
        response1 = self.information.update_one(filter, update)
        response2 = None

        if self.body.role is not None:
            response2 = self.roles.update_one(filter, {"$set": {'role':self.body.role }} )
        if response1.modified_count == 0:
            output = {'error': 'document does not exists', 'status': '404'} \
                if response1.matched_count == 0 \
                else {'error': 'document already exists', 'status': '409'}
        elif response2 is not None and response2.modified_count == 0:
            output = {'error': 'update operation failed', 'status': '400'}
        else:
            output = {'message': 'update operation success', 'status': '200'}

        return output