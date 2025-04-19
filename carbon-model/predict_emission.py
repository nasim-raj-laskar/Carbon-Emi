import joblib
import numpy as np
import json
from typing import Tuple
from xgboost import XGBRegressor  
import pandas as pd


class CarbonPredictor:
    def __init__(self, 
                 model_path: str = '/mnt/x/nasim_xhqpjmy/Code/Hacathon/carbon-footprint/carbon-model/model/xmodel.json', 
                 scaler_path: str = '/mnt/x/nasim_xhqpjmy/Code/Hacathon/carbon-footprint/carbon-model/model/xscaler.pkl'):
        try:    
            self.model = XGBRegressor()
            self.model.load_model(model_path)         
            self.scaler = joblib.load(scaler_path) 
            self.required_features = 3  
            self.feature_order = [
                "energy_kwh",
                "transport_km",
                "waste_kg",
                "energy_transport_interaction",
                "energy_waste_interaction"
            ]
            
        except Exception as e:
            raise RuntimeError(f"Model initialization failed: {str(e)}")

    def _validate_inputs(self, *inputs: float) -> Tuple[float, float, float]:
        if len(inputs) != self.required_features:
            raise ValueError(
                f"Expected {self.required_features} inputs "
                f"(energy_kwh, transport_km, waste_kg), got {len(inputs)}"
            )
        
        try:
            energy, transport, waste = map(float, inputs)
        except (TypeError, ValueError) as e:
            raise ValueError("All inputs must be numeric") from e
        
        if any(val < 0 for val in [energy, transport, waste]):
            raise ValueError("Inputs must be non-negative")
            
        return energy, transport, waste
    


    def _prepare_features(self, 
                      energy: float, 
                      transport: float, 
                      waste: float) -> pd.DataFrame:
        data = {
            "energy_kwh": [energy],
            "transport_km": [transport],
            "waste_kg": [waste],
            "energy_transport_interaction": [energy * transport],
            "energy_waste_interaction": [energy * waste]
        }
        return pd.DataFrame(data, columns=self.feature_order)

    
    def predict(self, 
               energy_kwh: float, 
               transport_km: float, 
               waste_kg: float) -> float:

        try:
           
            energy, transport, waste = self._validate_inputs(
                energy_kwh, transport_km, waste_kg
            )
            
            features = self._prepare_features(energy, transport, waste)
            
            scaled_features = self.scaler.transform(features)
           
            return float(self.model.predict(scaled_features)[0])
            
        except ValueError as ve:
            raise ve  
        except Exception as e:
            raise RuntimeError(f"Prediction failed: {str(e)}") from e

try:
    predictor = CarbonPredictor()
except Exception as e:
    print(f"⚠️ Failed to initialize predictor: {e}")
    predictor = None