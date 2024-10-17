from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel
from challenge.model import DelayModel

app = FastAPI()
model = DelayModel()

class FlightData(BaseModel):
    OPERA: str
    TIPOVUELO: str
    MES: int
    DIA: int
    DIANOM: str
    SIGLAORI: str
    SIGLADES: str

class FlightsRequest(BaseModel):
    flights: list[FlightData]

def train_model():
    # Cargar datos
    training_data = pd.read_csv('data/data.csv')  # Ajusta esto a tu ruta de archivo
    print("Iniciando el preprocesamiento de datos...")
    
    # Preprocesar los datos de entrenamiento
    features, target = model.preprocess(training_data, target_column="delay")
    
    # Entrenar el modelo
    model.train(features, target)
    
    # Verificar que el modelo ha sido entrenado
    print("Modelo entrenado:", model._model is not None)

# Llama a esta función al inicio de tu aplicación, por ejemplo:
train_model()

@app.post("/predict", status_code=200)
async def post_predict(flights: FlightsRequest) -> dict:
    flight_data = pd.DataFrame([flight.dict() for flight in flights.flights])
    
    print("Datos de vuelos recibidos para predicción:")
    print(flight_data)
    
    # Preprocesar los datos de entrada
    features, _ = model.preprocess(flight_data, target_column="delay")  # Asegúrate de pasar el target_column

    # Realizar la predicción
    predictions = model.predict(features)
    
    return {"predictions": predictions}
