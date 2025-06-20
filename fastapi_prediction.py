import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pymongo
import certifi
from dotenv import load_dotenv
from pymongo.server_api import ServerApi
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(f"Your MongoDB URL: {MONGO_DB_URL}")

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipelines.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

import pandas as pd
import numpy as np
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from starlette.responses import RedirectResponse


from networksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME

mongo_client = pymongo.MongoClient(MONGO_DB_URL,  server_api = ServerApi('1'), tls = True, tlsCAFile = certifi.where())
database = mongo_client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/", tags = ["authentication"])
async def index():
    return RedirectResponse(url = "/docs")

@app.get("/train")
async def train_route():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response("Training completed sucessfully.")
    except Exception as e:
        raise NetworkSecurityException(e, sys)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory = "./templates")

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df=pd.read_csv(file.file)
        #print(df)
        preprocesor = load_object("finalmodels/preprocessor.pkl")
        final_model = load_object("finalmodels/model.pkl")
        network_model = NetworkModel(preprocessor = preprocesor, model = final_model)
        print(df.iloc[0])

        y_pred = network_model.predict(df)
        print(y_pred)

        df['target'] = y_pred
        print(df['target']) 

        df.to_csv('testing_data/output.csv')
        table_html = df.to_html(classes = 'table table-striped')
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        
    except Exception as e:
            raise NetworkSecurityException(e,sys)

if __name__ == "__main__":
    app_run(app, hose = "localhost", port = 8000)