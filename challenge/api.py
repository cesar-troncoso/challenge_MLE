import fastapi
import pandas as pd
from challenge.model import DelayModel
from pydantic import BaseModel

app = fastapi.FastAPI()

# Inicializar el modelo
model = DelayModel()

# Cargar los datos y entrenar el modelo solo una vez
data = pd.read_csv('data/data.csv')

# Preprocesar los datos
features, target = model.preprocess(data, target_column='delay')

# Entrenar el modelo
model.fit(features, target)

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {"status": "OK"}

@app.post("/predict", status_code=200)
async def post_predict(input_data: dict) -> dict:
    # Imprimir el cuerpo del input para diagnóstico
    print("Datos del body:", input_data)

    # Convertir el input a un DataFrame
    input_df = pd.DataFrame([input_data])  # Crear DataFrame directamente del body

    # Preprocesar el DataFrame
    input_features = model.preprocess(input_df)

    # Obtener las características esperadas del modelo
    expected_features = model._model.get_booster().feature_names

    # Crear un diccionario para las características esperadas y sus valores
    expected_feature_values = {feature: 0.0 for feature in expected_features}  # Inicializar en 0

    # Llenar los valores esperados con los de input_features
    for feature in expected_features:
        if feature in input_features.columns:
            expected_feature_values[feature] = input_features[feature].iloc[0].item()  # Convertir a valor escalar

    # Combinar el input original con los valores esperados
    combined_output = {**input_data, **expected_feature_values}

    # Transformar combined_output a un formato similar a expected_features
    combined_output_transformed = [
        {"feature": key, "value": value}
        for key, value in combined_output.items()
    ]

    # Crear un DataFrame para la predicción usando combined_output
    prediction_input = pd.DataFrame([expected_feature_values])  # Crear DataFrame a partir de expected_feature_values

    # Realizar la predicción utilizando las características del input
    prediction = model.predict(prediction_input)

    # Crear una lista de características esperadas con sus valores
    expected_features_with_values = [
        {"feature": feature, "value": expected_feature_values[feature]}
        for feature in expected_features
    ]

    # Retornar el JSON combinado
    return {
        "prediction": prediction  # Añadir la predicción al retorno
    }
