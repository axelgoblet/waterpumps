from pymongo import MongoClient
import pickle
import gridfs


class ModelRepository:
    def __init__(self):
        client = MongoClient(host='db', port=27017)
        db = client.water_pump_db
        self._fs = gridfs.GridFS(db)

    def read_model(self):
        cursor = self._fs.find(no_cursor_timeout=True).limit(1).sort([('$natural', -1)])
        for item in cursor:
            binary = item.read()
            model = pickle.loads(binary)

        print('model read succesfully.')

        return model
