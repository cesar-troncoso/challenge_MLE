import unittest
from fastapi.testclient import TestClient
from challenge import app

class TestBatchPipeline(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_should_get_predict(self):
        data = {
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas",
                    "TIPOVUELO": "N",
                    "MES": 3,
                    "DIA": 15,
                    "DIANOM": "Lunes",
                    "SIGLAORI": "SCL",
                    "SIGLADES": "EZE"
                }
            ]
        }
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("predict", response.json())

    def test_should_fail_unknown_column(self):
        data = {
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas",
                    "TIPOVUELO": "O",
                    "MES": 13,  # Esto está fuera de rango, deberías definir qué es válido
                    "DIA": 32,  # Debería ser un número válido para los días
                    "DIANOM": "Domingo",
                    "SIGLAORI": "SCL",
                    "SIGLADES": "EZE"
                }
            ]
        }
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 422)  # Verifica que falle por valores incorrectos
