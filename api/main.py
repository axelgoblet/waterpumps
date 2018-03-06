from flask import Flask, request
import pandas as pd
import json

from dal.repositories.model_repository import ModelRepository
from domain.services.preprocessing_service import PreprocessingService
from domain.services.prediction_service import PredictionService
from domain.services.queueing_service import QueueingService


preprocessing_service = PreprocessingService()
prediction_service = PredictionService()
queueing_service = QueueingService()
model_repository = ModelRepository()

app = Flask(__name__)


@app.route('/train', methods=['GET'])
def train():
    queueing_service.enqueue()

    return 'Succesfully queued training request. The new model will be ready soon.'


@app.route('/predict', methods=['POST'])
def predict():
    json_data = request.get_json()
    df = pd.DataFrame(json_data)

    print('Dataset containing', len(df), 'rows loaded.')

    model = model_repository.read_model()
    X, _ = preprocessing_service.create_X(df)
    predictions = prediction_service.predict(model, X)

    return json.dumps(list(predictions.astype(str)))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)

