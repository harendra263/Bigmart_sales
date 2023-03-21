import sys
import os
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

from sklearn.metrics import r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer

from dataclasses import dataclass
import pandas as pd
import numpy as np

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    
    def get_data_transformation_object(self) -> ColumnTransformer:
        """This function will return preprocessing objects"""
        try:
            num_cols = ['Item_Weight', 'Item_Visibility', 'Item_MRP']
            categorical_cols = ['Item_Identifier', 'Item_Fat_Content', 'Item_Type', 'Outlet_Identifier',
                                'Outlet_Size', 'Outlet_Location_Type', 'Outlet_Type']
            
            num_pipeline = Pipeline(
                steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("label_encoding", LabelEncoder()),
                ("scaler", StandardScaler())
                ]
            )

            logging.info(f"Categorical Columns: {categorical_cols}")
            logging.info(f"Numerical Columns: {num_cols}")

            return ColumnTransformer(
                [
                ("num_pipeline", num_pipeline, num_cols),
                ("cat_pipelines", cat_pipeline, categorical_cols)
                ]
            )
            
        except Exception as e:
            raise CustomException(e, sys) from e
    
    def initiate_data_transformation(self, train_path, val_path):
        try:
            train_df = pd.read_csv(train_path)
            val_df = pd.read_csv(val_path)

            logging.info("Train and val data has been read successfully")
            logging.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformation_object()

            logging.info("Preprocessing obj obtained successfully")

            target_column = "Item_Outlet_Sales"
            input_feature_train= train_df.drop(columns=["Outlet_Establishment_Year", "Item_Outlet_Sales"], axis=1)
            target_feature_train_df = train_df[target_column]

            input_feature_val= val_df.drop(columns=["Outlet_Establishment_Year", "Item_Outlet_Sales"], axis=1)
            target_feature_val_df = val_df[target_column]

            logging.info("Applying preprocessing object on training and Validation Dataframes")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train)
            input_feature_val_arr = preprocessing_obj.fit_transform(input_feature_val)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]

            val_arr = np.c_[
                input_feature_val_arr, np.array(target_feature_val_df)
            ]
            logging.info("Saving preprocessing object")
            save_object(
                file_path= self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (
                train_arr,
                val_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys) from e