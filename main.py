from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "app": "FitFlow",
        "message": "FitFlow is running!"
    }