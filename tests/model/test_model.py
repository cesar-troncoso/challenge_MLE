import unittest
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from challenge.model import DelayModel

class TestModel(unittest.TestCase):

    # Definir las características y el objetivo
    FEATURES_COLS = [
        'OPERA_Aerolineas Argentinas', 
        'OPERA_Aeromexico', 
        'OPERA_Air Canada', 
        'OPERA_Air France', 
        'OPERA_Alitalia', 
        'OPERA_American Airlines', 
        'OPERA_Austral', 
        'OPERA_Avianca', 
        'OPERA_British Airways', 
        'OPERA_Copa Air', 
        'OPERA_Delta Air', 
        'OPERA_Gol Trans', 
        'OPERA_Grupo LATAM', 
        'OPERA_Iberia', 
        'OPERA_JetSmart SPA', 
        'OPERA_K.L.M.', 
        'OPERA_Lacsa', 
        'OPERA_Latin American Wings', 
        'OPERA_Oceanair Linhas Aereas', 
        'OPERA_Plus Ultra Lineas Aereas', 
        'OPERA_Qantas Airways', 
        'OPERA_Sky Airline', 
        'OPERA_United Airlines', 
        'TIPOVUELO_I', 
        'TIPOVUELO_N', 
        'MES_1', 
        'MES_2', 
        'MES_3', 
        'MES_4', 
        'MES_5', 
        'MES_6', 
        'MES_7', 
        'MES_8', 
        'MES_9', 
        'MES_10', 
        'MES_11', 
        'MES_12', 
        'high_season', 
        'min_diff'
    ]

    TARGET_COL = ["delay"]

    def setUp(self) -> None:
        super().setUp()
        self.model = DelayModel()
        self.data = pd.read_csv('data/data.csv')
        self.features, self.target = self.model.preprocess(data=self.data, target_column="delay")
        self.model.fit(self.features, self.target)

    def test_model_preprocess_for_training(self):
        assert isinstance(self.features, pd.DataFrame)
        assert self.features.shape[1] == len(self.FEATURES_COLS)
        assert set(self.features.columns) == set(self.FEATURES_COLS)

        assert isinstance(self.target, pd.DataFrame)
        assert self.target.shape[1] == len(self.TARGET_COL)
        assert set(self.target.columns) == set(self.TARGET_COL)

    def test_model_fit(self):
        _, features_validation, _, target_validation = train_test_split(self.features, self.target, test_size=0.33, random_state=42)
        
        predicted_target = self.model._model.predict(features_validation)
        
        # Imprimir predicciones y objetivos reales
        print("Predicciones:", predicted_target)
        print("Objetivos reales:", target_validation.values.flatten())
        
        # Compara las predicciones con los objetivos reales
        assert len(predicted_target) == len(target_validation)
        assert all(pt == tv for pt, tv in zip(predicted_target, target_validation.values.flatten()))

    def test_model_predict(self):
        predicted_targets = self.model.predict(features=self.features)

        assert isinstance(predicted_targets, list)
        assert len(predicted_targets) == self.features.shape[0]
        assert all(isinstance(predicted_target, int) for predicted_target in predicted_targets)

if __name__ == '__main__':
    unittest.main()
