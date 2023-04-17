import pandas as pd
import pickle
import imblearn
import random
import geocoder
import math
from typing import Union
from fastapi import FastAPI
from sklearn.pipeline import Pipeline
from joblib import dump, load

## Load lookups and model

estimator = load("best_rf_tuned.joblib")
lookup_risk_df = pd.read_csv('lookup_risk.csv')

## Serve application
app = FastAPI()

""" 
Model Parameter to User Input Mapping
'USA_WIND' --> wind
'USA_GUST' --> gust
'storm_category' --> hurricanecat
'effective_rent' --> rent
'zip' -- [come from address]
'occupancy' --> occupancy
'prop_rent_growth' [property rent growth - lookup from file - final_rent_data.csv]
** if you can't find prop rent growth, default to sma **
'sma_rent_growth' [SMA Stabilzed Market Rent: markets rent growth where property resides - lookup from file - macro_data.csv]
'distance_from_coast' [distance_from_coast]
'RISK_SCORE' [FEMA designated risk score - lookup from file - NRI_Table_Counties.csv]
'CFLD_RISKS', [Coastal flood risk - lookup from file - NRI_Table_Counties.csv]
'HRCN_RISKS' [Hurricane flood risk - lookup from file - NRI_Table_Counties.csv]
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
    risk_scores = get_risk_scores(address)
    
    input_data = {'USA_WIND': [wind], 
        'USA_GUST': [gust], 
        'storm_category': [hurricanecat], 
        'effective_rent': [rent], 
        'zip': ['32818'], 
        'occupancy': [occupancy], 
        'prop_rent_growth': [0.007035],
        'sma_rent_growth': [0.008267], 
        'distance_from_coast': [75.76417], 
        'RISK_SCORE': [risk_scores['risk_score']], 
        'CFLD_RISKS': [risk_scores['cfld_risks']],
        'HRCN_RISKS': [risk_scores['hrcn_risks']],
        'quarter_num': [quarter]}
    data_df = pd.DataFrame.from_dict(input_data, orient='columns')

    return data_df

def get_rent_growth(address):
    x = x

def get_risk_scores(address):
    risk_scores = {}
    zipcode = get_loc_info(address)
    risk_rec = lookup_risk_df[lookup_risk_df['ZIP'] == zipcode]
    print(risk_rec)
    risk_scores['risk_score'] = risk_rec['RISK_SCORE'].iloc[0] if not math.isnan(risk_rec['RISK_SCORE'].iloc[0]) else 0.0
    risk_scores['cfld_risks'] = risk_rec['CFLD_RISKS'].iloc[0] if not math.isnan(risk_rec['CFLD_RISKS'].iloc[0]) else 0.0
    risk_scores['hrcn_risks'] = risk_rec['HRCN_RISKS'].iloc[0] if not math.isnan(risk_rec['HRCN_RISKS'].iloc[0]) else 0.0
    return risk_scores

def get_loc_info(address, type="zip"):
    loc_val = None
    g = geocoder.osm(address, maxrows=1)
    if g:
        if type == "coord":
            loc_val = g.latlng
        if type == "zip":
            loc_val = int(g.postal)
    return loc_val