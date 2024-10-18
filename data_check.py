import pandas as pd

# Leer el archivo CSV
data = pd.read_csv('data/data.csv')

# Mostrar información general del dataset
print(data.info())

# Mostrar las primeras filas del dataset para verificar la lectura
print(data.head())
