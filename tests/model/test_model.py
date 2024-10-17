import unittest
import pandas as pd
from challenge.model import DelayModel

class TestModel(unittest.TestCase):
    def setUp(self):
        self.model = DelayModel()
        self.data = pd.DataFrame({
            "OPERA": ["Aerolineas Argentinas", "Grupo LATAM"],
            "TIPOVUELO": ["N", "I"],
            "MES": [3, 5],
            "DIA": [15, 22],
            "DIANOM": ["Lunes", "Jueves"],
            "SIGLAORI": ["SCL", "LIM"],
            "SIGLADES": ["EZE", "MIA"],
            "delay": [0, 1]
        })
        
    def test_model_preprocess(self):
        features, target = self.model.preprocess(data=self.data, target_column="delay")
        self.assertIn("DIANOM_Lunes", features.columns)
        self.assertIn("DIANOM_Jueves", features.columns)
        self.assertEqual(target.tolist(), [0, 1])

    def test_model_predict(self):
        # Preprocesar y entrenar el modelo antes de predecir
        features, target = self.model.preprocess(data=self.data, target_column="delay")
        self.model.train(features, target)
        predicted_targets = self.model.predict(features)
        self.assertEqual(predicted_targets, [0, 1])  # Comparar las predicciones con los valores esperados
