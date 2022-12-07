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

    def read(self):
        # find the permission tuple form permission collection for this user and validate
        sender_document = self.roles.find_one({'id':self.sender_id})
        if sender_document is None:
            # error sender_id does not exists
            return 
        else:
            permission = sender_document['role']
            if 'GET' not in self.get_permission_list(permission):
                # permission error
                return 
        
        print(self.body.id)
        documents = self.information.find_one({'id':self.body.id})
        output = {}
        if documents is None:
            # return all the user list
            documents = self.information.find()
            if documents is not None:
                output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        else:
            output = [{item: data[item] for item in data if item != '_id'} for data in documents]

        return output



    def write(self):
        # find the permission tuple form permission collection for this user and validate
        sender_document = self.roles.find_one({'id':self.sender_id})
        print(sender_document)
        if sender_document is None:
            # error sender_id does not exists
            return 
        else:
            permission = sender_document['role']
            if 'POST' not in self.get_permission_list(permission):
                # permission error
                return 

        # assign next available ID
        self.body.id = self.get_next_id()

        self.information.insert_one(self.body.__dict__)
        self.roles.insert_one({'role':self.body.role ,'id': self.body.id})

        output = {'Status': 'Successful Write Operation',
                  'name': str(self.body.name),
                  'id': str(self.body.id)
                  }
        return output