from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Returns API!"}


# Allow frontend to connect (especially for React running on localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:3000"]
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/returns")
def get_returns():
    try:
        df = pd.read_csv("all_company_returns.csv")
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}
