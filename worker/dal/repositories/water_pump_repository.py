from pymongo import MongoClient
import pandas as pd

from domain.constants import UNUSED_FEATURES


class WaterPumpRepository:
    def __init__(self):
        client = MongoClient(host='db', port=27017)
        db = client.water_pump_db
        self._water_pumps = db.water_pumps

    def read_water_pumps(self, only_broken=False, only_used=False):
        row_query = {'status_group': {'$nin': ['functional']}} if only_broken else None
        column_query = self._unused_features_to_query() if only_used else None

        water_pumps = self._water_pumps.find(row_query, column_query)
        df = pd.DataFrame(list(water_pumps))

        return df

    def _unused_features_to_query(self):
        query = {}
        for feature in UNUSED_FEATURES:
            query[feature] = 0

        return query

