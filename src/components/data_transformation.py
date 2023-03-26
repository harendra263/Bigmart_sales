import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler, LabelEncoder

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"proprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            logging.info("Imputation process started")
            for i in df.columns:
                if i in df.select_dtypes(include=['float64', 'int64']):
                    df[i] = df[i].replace(np.nan, df[i].median())
                elif i in df.select_dtypes(include='object'):
                    df[i] = df[i].replace(np.nan, df[i].mode()[0])
                else:
                    raise CustomException("While imputing missing values, something went wring", sys)
            logging.info("Imputation process completed successfully")
            return df
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def _label_encoder(self, df: pd.DataFrame):
        try:
            logging.info("Encoding process started")
            for x in df.columns:
                if x in df.select_dtypes(include="object"):
                    df[x] = df[x].astype('category').cat.codes
            logging.info("Encoding process completed")
            return df
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def _scale_num_col(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            logging.info("Standardizing process started")
            num_df = df.select_dtypes(exclude="object")
            num_cols = num_df.columns
            scaled_df= pd.DataFrame(StandardScaler().fit_transform(num_df), columns=num_df.columns)
            new_df = df.drop(num_cols, axis=1)
            logging.info("Standardizing process completed")
            return pd.concat([new_df, scaled_df], axis=1)
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def fit_transform(self, df: pd.DataFrame):
        try:
            # df = self._handle_missing_values(df)
            df = self._label_encoder(df=df)
            df = self._scale_num_col(df=df)
            return df.to_numpy()
        except Exception as e:
            raise CustomException(e, sys) from e
    
        
    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("preprocessing process started")

            target_column_name="Item_Outlet_Sales"

            input_feature_train_df=train_df.drop(columns=[target_column_name, 'Outlet_Establishment_Year'],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name, 'Outlet_Establishment_Year'],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(
                "Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr=self.fit_transform(input_feature_train_df)
            input_feature_test_arr=self.fit_transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info("preprocessing process completed")

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys) from e