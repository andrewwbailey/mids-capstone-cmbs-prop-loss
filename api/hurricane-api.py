from typing import Union
from fastapi import FastAPI
from sklearn.pipeline import Pipeline
import pickle
import imblearn

best_rf_model = pickle.load(open('best_rf_final_model.pickle', 'rb'))

app = FastAPI()

@app.post("/predict")
def read_root(lat: int, lon: int):
    return {"prediction": 1}

@app.get("/heartbeat")
def heartbeat():
    return "Online"