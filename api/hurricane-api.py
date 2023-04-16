from typing import Union
from fastapi import FastAPI
from sklearn.pipeline import Pipeline
import pickle
import imblearn
import random

best_rf_model = pickle.load(open('best_rf_final_model.pickle', 'rb'))

app = FastAPI()

# From webpage:
# User is adding:
# effective_rent
# property address (zip, expose_status_code, distance_from_coast, RISK_SCORE, CFLD_RISKS, HRCN_RISKS, prop_rent_growth, sma_rent_growth)
# quarter_num
# OPTIONAL:
# occupancy -> (90%)
# 'USA_WIND' (max hurricane wind speed) ->
# 'USA_GUST',
# 'USA_SSHS' -> category (1-5)
# address, rent, quarter, occupancy, gust, wind, hurricanecat


@app.get("/predict")
def predict(address: str, rent: float, quarter: int, occupancy: int, gust: float, wind: float, hurricanecat: int):
    # random for now
    random_predict = random.randrange(3)
    prediction = random_predict
    return {"prediction": prediction}

@app.get("/heartbeat")
def heartbeat():
    return "Online"