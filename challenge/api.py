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

    # Obtener la primera fila del DataFrame como un diccionario sin lista
    csv_head = data.head(1).to_dict(orient="index")  # Convierte a diccionario

    # Extraer el primer registro del diccionario
    csv_head = csv_head[list(csv_head.keys())[0]]  # Acceder al primer registro

    # Retornar el body recibido y los datos del CSV
    return {"body": input_data, "csv": csv_head}
