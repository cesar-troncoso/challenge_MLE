# Documentación del Proyecto: Software Engineer (ML & LLMs) Challenge

## Introducción
Este documento detalla el proceso de desarrollo y las decisiones tomadas durante la implementación del desafío "Software Engineer (ML & LLMs)". A continuación se describen las distintas partes del reto, las justificaciones para las elecciones realizadas y la funcionalidad del sistema desarrollado.

## Parte I: Transcripción del modelo
Se realizó la transcripción del contenido del cuaderno de Jupyter (`exploration.ipynb`) al archivo `model.py`. Se eligió el modelo **XGBoost** debido a su capacidad de manejar datos con gran dimensionalidad y su eficacia comprobada en problemas de clasificación, lo que lo convierte en una opción sólida para predecir retrasos en vuelos.

### Justificación
La elección de XGBoost se basó en las características del problema y la naturaleza de los datos, así como en la recomendación del equipo para utilizar este modelo como base para la predicción.

## Parte II: Implementación de la API
Se desarrolló una API utilizando **FastAPI**, tal como se especificaba en el README del reto. FastAPI se eligió por su facilidad de uso, alta velocidad y capacidades de validación automática de datos.

### Justificación
Se utilizó FastAPI porque era la tecnología recomendada en el README para implementar la API. Además, ofrece una excelente documentación y características que facilitan la creación de APIs RESTful eficientes y escalables.

## Parte III: Entrenamiento del Modelo
Para entrenar el modelo y asegurar que este pudiera predecir correctamente los retrasos de vuelos, se realizaron ajustes en la clase `DelayModel`. A continuación, se describen las modificaciones:

1. **Generación de la Columna `delay`**: En el método `preprocess`, se creó una nueva columna `delay` basada en la diferencia mínima de tiempo (`min_diff`). Se consideró un retraso si `min_diff` es mayor a 15 minutos, asignando así un valor de 1. En caso contrario, se asigna un valor de 0.
   ```python
   if target_column:
       data['delay'] = np.where(data['min_diff'] > 15, 1, 0)
   ```

2. **Balanceo de Clases**: En el método `fit`, se implementó un balanceo de clases utilizando `scale_pos_weight`. Este ajuste es crucial para abordar la desproporción entre las clases de retrasos y no retrasos en los datos, lo que ayuda a mejorar la precisión de las predicciones del modelo.
   ```python
   scale_pos_weight = n_y0 / n_y1 if n_y1 != 0 else 1
   ```

Estos cambios permitieron que el modelo se ajustara adecuadamente para distinguir entre los retrasos (1) y los vuelos a tiempo (0).

## Parte IV: Despliegue en GCP
La API se desplegó en **Google Cloud Platform (GCP)** utilizando **Cloud Run**. Este servicio se eligió por su capacidad de escalar automáticamente y manejar las solicitudes de manera eficiente, así como por su integración con otros servicios de GCP. La imagen del contenedor fue construida y luego subida a la nube utilizando Cloud Run, lo que facilitó el acceso a la API sin necesidad de preocuparse por la infraestructura subyacente.

### Justificación
GCP fue seleccionado porque el README del reto especificaba su uso para el despliegue de la API. Además, Cloud Run permite un manejo sencillo de contenedores y es ideal para aplicaciones que requieren escalabilidad dinámica.

## Parte V: Implementación de CI/CD
Se implementó un flujo de trabajo de **CI/CD** utilizando GitHub Actions. Esto permite que cada vez que se haga un push a la rama `main`, se construya y despliegue automáticamente la aplicación en GCP.

### Justificación
La implementación de CI/CD fue un requerimiento del README del reto. Al automatizar el proceso de construcción y despliegue, se mejora la eficiencia y se reduce la probabilidad de errores manuales durante estas etapas.

## Modificaciones en el Dockerfile
Se modificó el Dockerfile para asegurar que la aplicación se ejecute tanto localmente como en la nube. Se establecieron los puertos adecuados y se optimizó la instalación de dependencias.

## URL de la API
La API desplegada se puede acceder en la siguiente URL:
[https://challenge-mle-634329014145.us-central1.run.app](https://challenge-mle-634329014145.us-central1.run.app)

## Resultados de las Pruebas
Al ejecutar las pruebas, se genera un informe en formato HTML que muestra los resultados detallados de las pruebas y la cobertura del código. Este informe se almacena en la carpeta `reports`. 

### Cómo Acceder al Informe
1. **Ejecutar las Pruebas de Modelo**: Utiliza el siguiente comando para ejecutar las pruebas y generar el informe:
   ```bash
   make model-test
   ```

2. **Ejecutar las Pruebas de Estrés**: Para realizar pruebas de estrés en la API, utiliza el siguiente comando:
   ```bash
   make stress.test
   ```

3. **Ubicación del Informe**: El informe HTML se encontrará en la carpeta `reports/html/index.html`. 

4. **Abrir el Informe**: Puedes abrir el informe en tu navegador web. Por ejemplo, si estás en un entorno local, puedes usar:
   ```bash
   open reports/html/index.html
   ```

### Contenido del Informe
El informe incluirá detalles sobre:
- La cobertura de código de las pruebas.
- Los resultados de las pruebas individuales, incluyendo cualquier prueba fallida.
- Métricas de rendimiento si se han incluido.

Asegúrate de revisar este informe para entender el estado de la implementación y cualquier área que pueda requerir atención.

## Comandos de Docker para Levantar el Contenedor
Para levantar el contenedor de la aplicación, puedes usar los siguientes comandos:

1. **Construir la Imagen**:
   ```bash
   docker build -t challenge_mle .
   ```

2. **Ejecutar el Contenedor**:
   ```bash
   docker run -it -p 8080:8080 challenge_mle
   ```

Estos comandos te permitirán construir la imagen del contenedor y ejecutarla en tu entorno local, haciendo que la API esté disponible en `http://localhost:8080`.

## Ejemplo de Uso
A continuación se presenta un ejemplo de cómo realizar una solicitud a la API para predecir el retraso de un vuelo:

### Solicitud POST
```bash
curl -X POST "https://challenge-mle-634329014145.us-central1.run.app/predict" -H "Content-Type: application/json" -d '{
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
}'
```

### Respuesta Esperada
```json
{
  "prediction": [0]
}
```
Este ejemplo muestra cómo enviar una solicitud para predecir el retraso de un vuelo. La API responderá con la predicción correspondiente, que en este caso sería `0`, indicando que no hay retraso.
