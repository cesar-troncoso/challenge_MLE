import pandas as pd
from sklearn.linear_model import LogisticRegression

class DelayModel:
    def __init__(self):
        self._model = None

    def preprocess(self, data: pd.DataFrame, target_column: str):
        print("Iniciando el preprocesamiento de datos...")
        features = data.drop(columns=[target_column])
        target = data[target_column]
        print("Preprocesamiento completado.")
        return features, target

    def train(self, features: pd.DataFrame, target: pd.Series):
        print("Entrenando el modelo...")
        self._model = LogisticRegression().fit(features, target)

    def predict(self, features: pd.DataFrame):
        if self._model is None:
            raise ValueError("Model is not trained yet. Please train the model before predicting.")
        return self._model.predict(features)
