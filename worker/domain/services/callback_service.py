from dal.repositories.water_pump_repository import WaterPumpRepository
from dal.repositories.model_repository import ModelRepository
from domain.services.preprocessing_service import PreprocessingService
from domain.services.model_train_service import ModelTrainService


class CallbackService:
    def __init__(self):
        self._water_pump_repository = WaterPumpRepository()
        self._preprocessing_service = PreprocessingService()
        self._model_train_service = ModelTrainService()
        self._model_repository = ModelRepository()

    def callback(self, ch, method, properties, body):
        df = self._water_pump_repository.read_water_pumps(only_broken=True, only_used=True)

        y = self._preprocessing_service.create_y(df)
        X, categorical_features = self._preprocessing_service.create_X(df)

        model, performance_mean, performance_var = self._model_train_service.train(X, y, categorical_features)

        self._model_repository.insert_model(model)

        print('New model stored. Performance = ' + str(performance_mean) + ' (' + str(performance_var) + ')')
