# main.py
from fastapi import FastAPI
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend (React) to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or set ["http://localhost:3000"] for your React port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to the NEW Returns API!"}

@app.get("/compay_returns")
def get_returns():
    df = pd.read_csv("investment_summary.csv")  # Make sure the path is correct
    return df.to_dict(orient="records")
