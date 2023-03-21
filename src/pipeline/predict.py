import sys
import pandas as pd
from src.exception import CustomException
from src.components.data_transformation import DataTransformation
from src.utils import load_object

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features: pd.DataFrame):
        try:
            model_path = 'artifacts/model.pkl'
            model = load_object(model_path)
            data_processed = DataTransformation().fit_transform(features)
            return model.predict(data_processed)
        except Exception as e:
            raise CustomException(e, sys) from e


class CustomData:
    def __init__(self, 
                 Item_Identifier: str,
                 Item_Weight: float,
                 Item_Fat_Content: str,
                Item_Visibility: float,            
                Item_Type: str,                
                Item_MRP: float,                 
                Outlet_Identifier: str,        
                Outlet_Size: str,              
                Outlet_Location_Type: str,   
                Outlet_Type: str) ->None:
        self.Item_Identifier = Item_Identifier
        self.Item_Weight = Item_Weight
        self.Item_Fat_Content = Item_Fat_Content
        self.Item_Visibility = Item_Visibility
        self.Item_Type = Item_Type
        self.Item_MRP = Item_MRP
        self.Outlet_Identifier = Outlet_Identifier
        self.Outlet_Size = Outlet_Size
        self.Outlet_Location_Type = Outlet_Location_Type
        self.Outlet_Type = Outlet_Type
    
    def get_data_as_dataframe(self) ->pd.DataFrame:
        try:
            custom_data_dict = {
                "Item_Identifier": [self.Item_Identifier],
                "Item_Weight": [self.Item_Weight],
                "Item_Fat_Content": [self.Item_Fat_Content],
                "Item_Visibility": [self.Item_Visibility],
                "Item_Type": [self.Item_Type],
                "Item_MRP": [self.Item_MRP],
                "Outlet_Identifier": [self.Outlet_Identifier],
                "Outlet_Size": [self.Outlet_Size],
                "Outlet_Location_Type": [self.Outlet_Location_Type],
                "Outlet_Type": [self.Outlet_Type]
            }
            return pd.DataFrame(custom_data_dict)
        except Exception as e:
            raise CustomException(e, sys) from e
