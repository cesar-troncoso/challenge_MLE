from locust import HttpUser, task

class StressUser(HttpUser):
    
    @task
    def predict_argentinas(self):
        self.client.post(
            "/predict", 
            json={
                "flights": [
                    {
                        "Fecha-I": "2017-01-02 23:30:00",
                        "Vlo-I": "226",
                        "Ori-I": "SCEL",
                        "Des-I": "KMIA",
                        "Emp-I": "AAL",
                        "Fecha-O": "2017-01-02 23:39:00",
                        "Vlo-O": "226",
                        "Ori-O": "SCEL",
                        "Des-O": "KMIA",
                        "Emp-O": "AAL",
                        "DIA": 2,
                        "MES": 1,
                        "AÑO": 2017,
                        "DIANOM": "Lunes",
                        "TIPOVUELO": "I",
                        "OPERA": "Aerolineas Argentinas",
                        "SIGLAORI": "Santiago",
                        "SIGLADES": "Miami",
                        "high_season": 1,
                        "min_diff": 9.0,
                        "period_day": "night",
                        "delay": 0
                    }
                ]
            }
        )

    @task
    def predict_latam(self):
        self.client.post(
            "/predict", 
            json={
                "flights": [
                    {
                        "Fecha-I": "2017-01-02 23:30:00",
                        "Vlo-I": "226",
                        "Ori-I": "SCEL",
                        "Des-I": "KMIA",
                        "Emp-I": "AAL",
                        "Fecha-O": "2017-01-02 23:39:00",
                        "Vlo-O": "226",
                        "Ori-O": "SCEL",
                        "Des-O": "KMIA",
                        "Emp-O": "AAL",
                        "DIA": 2,
                        "MES": 1,
                        "AÑO": 2017,
                        "DIANOM": "Lunes",
                        "TIPOVUELO": "I",
                        "OPERA": "Grupo LATAM",
                        "SIGLAORI": "Santiago",
                        "SIGLADES": "Miami",
                        "high_season": 1,
                        "min_diff": 9.0,
                        "period_day": "night",
                        "delay": 0
                    }
                ]
            }
        )
