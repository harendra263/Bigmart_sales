import os
import sys
from src.logger import logging
from src.exception import CustomException
from src.components.data_transformation import DataTransformation, DataTransformationConfig
from src.components.model_trainer import ModelTrainer, ModelTrainerConfig

from dataclasses import dataclass
from sklearn.model_selection import train_test_split
import pandas as pd


@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    val_data_path: str = os.path.join('artifacts', 'val.csv')
    raw_data_path: str = os.path.join('artifacts', 'data.csv')


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    

    def initiate_data_ingestion(self) ->tuple[str, str]:
        logging.info("Enter the data ingestion method or components")
        try:
            df = pd.read_csv('notebook/data/data.csv')
            logging.info("Reading the raw data as dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            

            logging.info("Train-Test Split initiated")
            train_set, val_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            val_set.to_csv(self.ingestion_config.val_data_path, index=False, header=True)

            logging.info("Data Ingestion is completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.val_data_path
            )

        except Exception as e:
            raise CustomException(e, sys) from e

if __name__ == "__main__":
    obj = DataIngestion()
    train_data, val_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_arr, val_arr, _ = data_transformation.initiate_data_transformation(train_data, val_data)

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,val_arr))
