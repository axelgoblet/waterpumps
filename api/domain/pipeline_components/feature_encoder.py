from sklearn.preprocessing import LabelEncoder
from sklearn.base import TransformerMixin, BaseEstimator
import numpy
import pandas as pd

from domain.constants import FEATURETYPE


class FeatureEncoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.encoders = []

    def fit(self, X, y=None, feature_types=None):
        if feature_types is None:
            feature_types = [FEATURETYPE.CATEGORICAL] * X.shape[1]
        
        self.encoders = []

        for feature_index, feature_type in enumerate(feature_types):
            if feature_type == FEATURETYPE.CATEGORICAL:
                missing_features = pd.isnull(X[:, feature_index])
                X[missing_features, feature_index] = 'missing_value'

                fitted_encoder = LabelEncoder()
                fitted_encoder.fit(X[:, feature_index])

                X[missing_features, feature_index] = numpy.nan
            else:
                fitted_encoder = None
            
            self.encoders.append(fitted_encoder)
        
        return self
    
    def transform(self, X):
        transformed_X = X.copy()

        for feature_index, encoder in enumerate(self.encoders):
            if encoder is not None:
                feature = X[:, feature_index]
                new_label_rows = self.__is_new_label(feature, encoder)
                substituted_feature = self.__substitute_new_labels(feature, encoder, new_label_rows)
                substituted_feature = encoder.transform(substituted_feature).astype(float)
                substituted_feature = self.__remove_new_labels(substituted_feature, new_label_rows)
                transformed_X[:, feature_index] = substituted_feature

        return transformed_X.astype(float)

    def __is_new_label(self, feature, encoder):
        return numpy.in1d(feature,encoder.classes_, invert=True)

    def __substitute_new_labels(self, feature, encoder, new_label_rows):
        substituted_feature = feature.copy()
        substituted_feature[new_label_rows] = encoder.classes_[0]
        return substituted_feature

    def __remove_new_labels(self, feature, new_label_rows):
        substituted_feature = feature.copy()
        substituted_feature[new_label_rows] = numpy.nan
        return substituted_feature
