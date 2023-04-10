from typing import Union
from fastapi import FastAPI
from sklearn.pipeline import Pipeline
import pickle
import imblearn

best_rf_model = pickle.load(open('best_rf_final_model.pickle', 'rb'))

app = FastAPI()

@app.post("/predict")
def predict(effective_rent: float, zip: int, USA_WIND: float, USA_GUST: float, USA_SSHS: float, prop_rent_growth: float, \
            sma_rent_growth: float, expose_status_code: int, occupancy: int, distance_from_coast: float, RISK_SCORE: float, \
                CFLD_RISKS: float, HRCN_RISKS: float, quarter_num:int):
    return {"prediction": 1}

@app.get("/heartbeat")
def heartbeat():
    return "Online"