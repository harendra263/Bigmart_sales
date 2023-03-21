import sys
import os
from dataclasses import dataclass

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import (
    GradientBoostingRegressor, RandomForestRegressor, AdaBoostRegressor
)

from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_squared_error

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts', 'model.pkl')

class ModelTrainer:
    def __init__(self) -> None:
        self.model_trainer_config = ModelTrainerConfig()
    
    def initiate_model_trainer(self, train_array, val_array):
        try:
            logging.info("Split training and Validation dataset")
            X_train, y_train, X_val, y_val = (
                train_array[:, :-1],
                train_array[:, -1],
                val_array[:, :-1],
                val_array[:, -1]
            )
            models = {
                "Random Forest": RandomForestRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "XGBRegressor": XGBRegressor(),
                "LinearRegression": LinearRegression(),
                "Decision Tree": DecisionTreeRegressor(),
                "AdaBoost Regressor": AdaBoostRegressor()
            }
            params={
                "Random Forest":{
                    # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                 
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "XGBRegressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "LinearRegression": {},
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    # 'loss':['linear','square','exponential'],
                    'n_estimators': [8,16,32,64,128,256]
                }       
            }

            model_report: dict= evaluate_models(X_train=X_train, y_train= y_train, X_test=X_val, y_test=y_val, models=models, param=params)

            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No Best model found")
            logging.info(f"Best model {best_model} found on both training and validation dataset")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
            predicted = best_model.predict(X_val)
            rmse = np.sqrt(mean_squared_error(y_val, predicted))
            r_square = r2_score(y_val, predicted)
            logging.info(f'Model Training process completed with rmse: {rmse} and R_square: {r_square}')

            return rmse
        except Exception as e:
            raise CustomException(e, sys) from e