import joblib
import os
import numpy as np
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from models import ModelParams



# initiate API
app = FastAPI(
    title="Health Management Planning API",
    description="API for predicting how long patients will stay at a hospital",
    version="1.0"
)

data = []


def get_prediction(
        Hospital_code,
        Hospital_type_code,
        City_Code_Hospital,
        Hospital_region_code,
        Available_Extra_Rooms,
        Department,
        Ward_Type,
        Ward_Facility_Code,
        Bed_Grade,
        City_Code_Patient,
        Type_of_Admission,
        Severity_of_Illness,
        Visitors_with_Patient,
        Age,
        Admission_Deposit):

    data = [Hospital_code, Hospital_type_code, City_Code_Hospital,
            Hospital_region_code, Available_Extra_Rooms,
            Department, Ward_Type, Ward_Facility_Code, Bed_Grade,
            City_Code_Patient, Type_of_Admission, Severity_of_Illness,
            Visitors_with_Patient, Age, Admission_Deposit]

    columns = ['Hospital_code', 'Hospital_type_code', 'City_Code_Hospital',
               'Hospital_region_code', 'Available Extra Rooms in Hospital',
               'Department', 'Ward_Type', 'Ward_Facility_Code', 'Bed Grade',
               'City_Code_Patient', 'Type of Admission', 'Severity of Illness',
               'Visitors with Patient', 'Age', 'Admission_Deposit']


    X = pd.DataFrame(np.array(data).reshape(-1, len(data)), columns=columns)

    PATH = os.path.join(os.getcwd(), "model.joblib")
    clf = joblib.load(PATH)

    prediction = clf.predict(X)[0]

    return {'prediction': prediction}





@app.get("/")
def home():
    html = """
    <html>
    <head>
    <style>
    h2 {
        text-align: center;
        font-family: sans-serif;
    }
    </style>
    <title>Health Management API</title>
    </head>
    <body>
    <h2>Patient's Admission Prediction</h2>
    </body>
    </html>
    
    """
    return HTMLResponse(html)


@app.post("/predict", tags=["predictions"])
async def predict(params: ModelParams):
    
    pred = get_prediction(
        params.Hospital_code,
        params.Hospital_type_code,
        params.City_Code_Hospital,
        params.Hospital_region_code,
        params.Available_Extra_Rooms,
        params.Department,
        params.Ward_Type,
        params.Ward_Facility_Code,
        params.Bed_Grade,
        params.City_Code_Patient,
        params.Type_of_Admission,
        params.Severity_of_Illness,
        params.Visitors_with_Patient,
        params.Age,
        params.Admission_Deposit
    )
    return pred
