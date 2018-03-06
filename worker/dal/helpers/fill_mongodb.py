import pandas as pd
from pymongo import MongoClient


def load_data():
    X = pd.read_csv('data/water_pump_labels.csv',
                    index_col=0)
    y = pd.read_csv('data/water_pump_set.csv',
                    index_col=0)
    dataset = pd.concat([X,y], axis=1)

    return dataset


def init_mongo():
    client = MongoClient('localhost', 27017)
    db = client.water_pump_db
    collection = db.water_pumps

    return collection


def insert_data(dataset, collection):
    records = dataset.to_dict('records')
    collection.insert_many(records)


dataset = load_data()
collection = init_mongo()
insert_data(dataset, collection)
found_records = collection.find()
