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
    # Cargar los datos
    training_data = pd.read_csv('data/data.csv')  # Ajusta esto a tu ruta de archivo

    # Calcular el delay si no existe
    if 'delay' not in training_data.columns:
        training_data['Fecha-I'] = pd.to_datetime(training_data['Fecha-I'], errors='coerce')
        training_data['Fecha-O'] = pd.to_datetime(training_data['Fecha-O'], errors='coerce')

        # Calcular el delay en minutos
        training_data['delay'] = (training_data['Fecha-O'] - training_data['Fecha-I']).dt.total_seconds() / 60.0
    
    # Limpiar datos y forzar tipos
    training_data['DIA'] = training_data['DIA'].astype(int)
    training_data['MES'] = training_data['MES'].astype(int)
    training_data['DIANOM'] = training_data['DIANOM'].astype(str)
    training_data['TIPOVUELO'] = training_data['TIPOVUELO'].astype(str)
    training_data['OPERA'] = training_data['OPERA'].astype(str)
    training_data['SIGLAORI'] = training_data['SIGLAORI'].astype(str)
    training_data['SIGLADES'] = training_data['SIGLADES'].astype(str)

    # Eliminar filas con valores nulos (ajusta según tus necesidades)
    training_data.dropna(inplace=True)

    # Convertir todas las columnas de objetos a categorías si son categóricas
    for col in ['TIPOVUELO', 'OPERA', 'SIGLAORI', 'SIGLADES']:
        if training_data[col].dtype == 'object':
            training_data[col] = training_data[col].astype('category')

    # Imprimir tipos de datos después de la conversión
    print("Tipos de datos después de la conversión a categorías:")
    print(training_data.dtypes)

    # Seleccionar solo las columnas que queremos usar
    features = training_data.drop(columns=['delay', 'Fecha-I', 'Fecha-O'])
    
    # Usar pd.get_dummies para convertir columnas categóricas a variables dummy
    features = pd.get_dummies(features, drop_first=True)

    # Preprocesar los datos de entrenamiento
    target = training_data['delay']
    
    # Imprimir las primeras filas de las características y del objetivo
    print("Características para el entrenamiento:")
    print(features.head())
    print("Objetivo (delay):")
    print(target.head())

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
