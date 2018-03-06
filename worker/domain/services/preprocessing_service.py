import pandas as pd

from domain.constants import UNUSED_FEATURES


class PreprocessingService:
    def __init__(self):
        pass

    def create_y(self, df):
        y = pd.to_numeric(pd.to_datetime(df.date_recorded)).values

        return y

    def create_X(self, df):
        df = self._delete_unused_features(df)

        df.permit = pd.to_numeric(df.permit)
        df.public_meeting = pd.to_numeric(df.public_meeting)

        df.district_code = df.district_code.astype(str)
        df.region_code = df.region_code.astype(str)

        label_column = 'date_recorded'
        if label_column in df.columns:
            del df[label_column]

        X = df.values
        categorical_features = self._create_categorical_feature_vector(df)

        return X, categorical_features

    def _create_categorical_feature_vector(self, df):
        return (df.dtypes == 'object').values

    def _delete_unused_features(self, df):
        for feature in UNUSED_FEATURES:
            if feature in df.columns:
                del(df[feature])

        return df