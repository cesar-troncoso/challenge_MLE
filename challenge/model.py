import pandas as pd
import numpy as np
from typing import Tuple, Union, List
import xgboost as xgb

class DelayModel:
    
    def __init__(self):
        self._model = None  # El modelo de Machine Learning se guardará aquí.

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepara los datos crudos para entrenamiento o predicción.

        Args:
            data (pd.DataFrame): Datos crudos.
            target_column (str, opcional): si se especifica, se devuelve el objetivo.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features y target.
            o
            pd.DataFrame: solo features.
        """
        # Generación de características adicionales
        data['high_season'] = data['Fecha-I'].apply(self.is_high_season)
        data['min_diff'] = data.apply(self.get_min_diff, axis=1)
        data['period_day'] = data['Fecha-I'].apply(self.get_period_day)
        
        # Si se especifica la columna objetivo, crear la columna 'delay'
        if target_column:
            data['delay'] = np.where(data['min_diff'] > 15, 1, 0)
        
        # Aplicar One-Hot Encoding a las variables categóricas
        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix='OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO'),
            pd.get_dummies(data['MES'], prefix='MES'),
            data[['high_season', 'min_diff']]
        ], axis=1)

        # Si se especifica target_column, devolver features y target
        if target_column:
            target = data[[target_column]]
            return features, target
        return features

    @staticmethod
    def get_period_day(date: str) -> str:
        from datetime import datetime
        date_time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').time()
        morning_min = datetime.strptime("05:00", '%H:%M').time()
        morning_max = datetime.strptime("11:59", '%H:%M').time()
        afternoon_min = datetime.strptime("12:00", '%H:%M').time()
        afternoon_max = datetime.strptime("18:59", '%H:%M').time()

        if morning_min <= date_time <= morning_max:
            return 'morning'
        elif afternoon_min <= date_time <= afternoon_max:
            return 'afternoon'
        else:
            return 'night'
    
    @staticmethod
    def is_high_season(date: str) -> int:
        from datetime import datetime
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        year = date.year
        high_season_ranges = [
            (datetime(year, 12, 15), datetime(year, 12, 31)),
            (datetime(year, 1, 1), datetime(year, 3, 3)),
            (datetime(year, 7, 15), datetime(year, 7, 31)),
            (datetime(year, 9, 11), datetime(year, 9, 30))
        ]
        for start, end in high_season_ranges:
            if start <= date <= end:
                return 1
        return 0
    
    @staticmethod
    def get_min_diff(row: pd.Series) -> float:
        from datetime import datetime
        fecha_o = datetime.strptime(row['Fecha-O'], '%Y-%m-%d %H:%M:%S')
        fecha_i = datetime.strptime(row['Fecha-I'], '%Y-%m-%d %H:%M:%S')
        min_diff = (fecha_o - fecha_i).total_seconds() / 60
        return min_diff

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Ajusta el modelo con los datos preprocesados.

        Args:
            features (pd.DataFrame): Datos preprocesados.
            target (pd.DataFrame): Objetivo.
        """
        # Balanceo de clases usando scale_pos_weight
        n_y0 = len(target[target == 0])
        n_y1 = len(target[target == 1])
        scale_pos_weight = n_y0 / n_y1 if n_y1 != 0 else 1

        # Entrenamiento de XGBoost con las clases balanceadas
        self._model = xgb.XGBClassifier(
            random_state=1,
            learning_rate=0.01,
            scale_pos_weight=scale_pos_weight
        )
        self._model.fit(features, target)

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Realiza predicciones sobre nuevos datos.

        Args:
            features (pd.DataFrame): Datos preprocesados para predecir.
        
        Returns:
            List[int]: Predicciones de retraso (1 = retrasado, 0 = no retrasado).
        """
        if self._model is None:
            raise ValueError("El modelo no ha sido entrenado. Llame al método 'fit' antes de predecir.")

        predictions = self._model.predict(features)
        return predictions.tolist()
