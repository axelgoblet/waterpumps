import pandas as pd


class PredictionService:
    def __init__(self):
        pass

    def predict(self, model, X):
        y_pred = model.predict(X)
        datetime_pred = pd.to_datetime(y_pred)

        return datetime_pred



