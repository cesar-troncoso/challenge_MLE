import fastapi
import pandas as pd
from challenge.model import DelayModel
from pydantic import BaseModel, constr, conint, condecimal, Field
from typing import List

app = fastapi.FastAPI()

# Inicializar el modelo
model = DelayModel()

# Cargar los datos y entrenar el modelo solo una vez
data = pd.read_csv('data/data.csv')

# Preprocesar los datos
features, target = model.preprocess(data, target_column='delay')

# Entrenar el modelo
model.fit(features, target)

class FlightDetails(BaseModel):
    Fecha_I: str = Field(..., alias="Fecha-I")  # Formato: YYYY-MM-DD HH:MM:SS
    Vlo_I: constr(min_length=1) = Field(..., alias="Vlo-I")
    Ori_I: constr(min_length=1) = Field(..., alias="Ori-I")
    Des_I: constr(min_length=1) = Field(..., alias="Des-I")
    Emp_I: constr(min_length=1) = Field(..., alias="Emp-I")
    Fecha_O: str = Field(..., alias="Fecha-O")
    Vlo_O: constr(min_length=1) = Field(..., alias="Vlo-O")
    Ori_O: constr(min_length=1) = Field(..., alias="Ori-O")
    Des_O: constr(min_length=1) = Field(..., alias="Des-O")
    Emp_O: constr(min_length=1) = Field(..., alias="Emp-O")
    DIA: conint(ge=1, le=31) = Field(..., alias="DIA")
    MES: conint(ge=1, le=12) = Field(..., alias="MES")
    AÑO: conint(ge=1900) = Field(..., alias="AÑO")
    DIANOM: constr(min_length=1) = Field(..., alias="DIANOM")
    TIPOVUELO: constr(regex=r'^[IN]$') = Field(..., alias="TIPOVUELO")
    OPERA: constr(min_length=1) = Field(..., alias="OPERA")
    SIGLAORI: constr(min_length=1) = Field(..., alias="SIGLAORI")
    SIGLADES: constr(min_length=1) = Field(..., alias="SIGLADES")
    high_season: conint(ge=0, le=1) = Field(..., alias="high_season")
    min_diff: condecimal(ge=0) = Field(..., alias="min_diff")
    period_day: constr(min_length=1) = Field(..., alias="period_day")
    delay: conint(ge=0) = Field(..., alias="delay")

class FlightRequest(BaseModel):
    flights: List[FlightDetails]

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {"status": "OK"}

@app.post("/predict", status_code=200)
async def post_predict(input_data: FlightRequest) -> dict:
    # Imprimir el cuerpo del input para diagnóstico
    print("Datos del body:", input_data.dict())

    predictions = []
    
    for flight in input_data.flights:
        # Convertir el vuelo a un DataFrame usando el método dict()
        flight_df = pd.DataFrame([flight.dict(by_alias=True)])  # Crear DataFrame usando alias

        # Preprocesar el DataFrame
        input_features = model.preprocess(flight_df)

        # Obtener las características esperadas del modelo
        expected_features = model._model.get_booster().feature_names

        # Crear un diccionario para las características esperadas y sus valores
        expected_feature_values = {feature: 0.0 for feature in expected_features}  # Inicializar en 0

        # Llenar los valores esperados con los de input_features
        for feature in expected_features:
            if feature in input_features.columns:
                expected_feature_values[feature] = input_features[feature].iloc[0].item()  # Convertir a valor escalar

        # Crear un DataFrame para la predicción usando expected_feature_values
        prediction_input = pd.DataFrame([expected_feature_values])  # Crear DataFrame a partir de expected_feature_values

        # Realizar la predicción utilizando las características del input
        prediction = model.predict(prediction_input)

        # Añadir la predicción a la lista (sin tolist) y asumir que prediction es un número
        predictions.append(prediction[0])  # Asegúrate de que estás tomando el valor correcto

    # Retornar las predicciones para cada vuelo como una lista simple
    return {
        "prediction": predictions,  # Cambiar a "prediction"
    }
