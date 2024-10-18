from challenge.model import DelayModel
import pandas as pd

from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

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
print(features.head(5))  # Mostrar solo las primeras 5 filas
print("\nTarget:")
print(target.head(5))  # Mostrar solo las primeras 5 filas

# Predecir usando las mismas features para la prueba (solo como ejemplo)
predictions = model.predict(features)

# Imprimir las primeras predicciones
print("Predicciones:")
print(predictions[:20])  # Mostrar solo las primeras 5 predicciones

# Dividir los datos en entrenamiento y validación
x_train, x_val, y_train, y_val = train_test_split(features, target, test_size=0.2, random_state=42)
model.fit(x_train, y_train)

# Evaluar en el conjunto de validación
predictions = model.predict(x_val)
print("Reporte de Clasificación:")
print(classification_report(y_val, predictions))
