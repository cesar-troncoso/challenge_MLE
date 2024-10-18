from challenge.model import DelayModel
import pandas as pd

# Cargar los datos
data = pd.read_csv('data/data.csv')

# Crear una instancia de la clase
model = DelayModel()

# Preprocesar los datos
features, target = model.preprocess(data, target_column='delay')

# Entrenar el modelo
model.fit(features, target)

# Imprimir un mensaje de éxito
print("Entrenamiento del modelo completado exitosamente.")

# Imprimir las primeras filas de features y target para verificar
print("Features:")
print(features)
print("\nTarget:")
print(target)


# Predecir usando las mismas features para la prueba (solo como ejemplo)
predictions = model.predict(features)

# Imprimir las predicciones
print("Predicciones:")
print(predictions)