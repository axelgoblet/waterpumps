from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import OneHotEncoder, Imputer, MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.decomposition import TruncatedSVD
from sklearn.svm import SVR
from sklearn.utils import shuffle
import numpy as np

from domain.pipeline_components.feature_encoder import FeatureEncoder
from domain.pipeline_components.item_selector import ItemSelector


class ModelTrainService:
    def __init__(self):
        pass

    def train(self, X, y, categorical_features):
        X, y = shuffle(X, y, random_state=847)

        pipeline = self._build_pipeline(categorical_features)

        fit_params = {'feature_encoder__feature_types': categorical_features}

        performances = cross_val_score(pipeline,
                                       X,
                                       y,
                                       scoring='r2',
                                       cv=10,
                                       n_jobs=-1,
                                       verbose=100,
                                       fit_params=fit_params)
        performance_mean = np.mean(performances)
        performance_var = np.var(performances)

        pipeline.fit(X, y, **fit_params)

        return pipeline, performance_mean, performance_var

    def _build_pipeline(self, categorical_features):
        feature_encoder = FeatureEncoder()

        numerical_selector = ItemSelector(key=np.where(categorical_features == 0)[0])
        mean_imputer = Imputer(missing_values=0,
                               strategy='mean')
        scaler = MinMaxScaler()
        numerical_pipeline = Pipeline(steps=[('numerical_selector', numerical_selector),
                                             ('mean_imputer', mean_imputer),
                                             ('scaler', scaler)])

        categorical_selector = ItemSelector(key=np.where(categorical_features == 1)[0])
        mode_imputer = Imputer(missing_values='NaN',
                               strategy='most_frequent')
        onehot = OneHotEncoder()
        categorical_steps = [('categorical_selector', categorical_selector),
                             ('mode_imputer', mode_imputer),
                             ('onehot', onehot)]
        categorical_pipeline = Pipeline(steps=categorical_steps)

        type_union = FeatureUnion(transformer_list=[('numerical_pipeline', numerical_pipeline),
                                                    ('categorical_pipeline', categorical_pipeline)],
                                  n_jobs=1)

        rf = RandomForestRegressor(random_state=123,
                                   n_estimators=100,
                                   n_jobs=1,
                                   max_features='auto',
                                   min_samples_leaf=10)

        pipeline_steps = [('feature_encoder', feature_encoder),
                          ('type_union', type_union),
                          ('rf', rf)]
        pipeline = Pipeline(steps=pipeline_steps)

        return pipeline



