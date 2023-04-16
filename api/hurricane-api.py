import pandas as pd
import pickle
import imblearn
import random
from typing import Union
from fastapi import FastAPI
from sklearn.pipeline import Pipeline
from joblib import dump, load

estimator = load("best_rf_final.joblib")

app = FastAPI()

""" 
Model Parameter to User Input Mapping
'USA_WIND' --> wind
'USA_GUST' --> gust
'USA_SSHS' --> hurricanecat
'effective_rent' --> rent
'expose_status_code'
'zip' 
'occupancy' --> occupancy
'prop_rent_growth',
'sma_rent_growth' ?
'distance_from_coast' ?
'RISK_SCORE' ?
'CFLD_RISKS', ?
'HRCN_RISKS' ?
'quarter_num' --> quarter """


@app.get("/predict")
def predict(address: str, rent: float, quarter: int, occupancy: int, gust: float, wind: float, hurricanecat: int):
    # random for now
    predict_rec = input_to_df(address, rent, quarter, occupancy, gust, wind, hurricanecat)
    print(predict_rec)
    prediction = estimator.predict(predict_rec)
    api_predict = int(prediction[0])
    return {"prediction": api_predict}

@app.get("/heartbeat")
def heartbeat():
    return "Online"

def input_to_df(address, rent, quarter, occupancy, gust, wind, hurricanecat):
    input_data = {'USA_WIND': [wind], 
        'USA_GUST': [gust], 
        'USA_SSHS': [hurricanecat], 
        'effective_rent': [rent], 
        'expose_status_code': [1], 
        'zip': ['32818'], 
        'occupancy': [occupancy], 
        'prop_rent_growth': [0.007035],
        'sma_rent_growth': [0.008267], 
        'distance_from_coast': [75.76417], 
        'RISK_SCORE': [33.495147], 
        'CFLD_RISKS': [1.988109],
        'HRCN_RISKS': [18.73492],
        'quarter_num': [quarter]}
    data_df = pd.DataFrame.from_dict(input_data, orient='columns')

    return data_df
