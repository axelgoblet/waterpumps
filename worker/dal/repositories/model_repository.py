from pymongo import MongoClient
import pickle
import gridfs
import json


class ModelRepository:
    def __init__(self):
        client = MongoClient(host='db', port=27017)
        db = client.water_pump_db
        self._fs = gridfs.GridFS(db)

    def insert_model(self, model):
        binary = pickle.dumps(model)

        self._fs.put(binary)

        print('new model inserted.')

