from fastapi import FastAPI
from engines.forex import ForexEngine
from engines.architecture import ArchitectureEngine

app = FastAPI()

forex = ForexEngine()
arch = ArchitectureEngine()

@app.get("/fx/rates")
def rates():
    return forex.get_market()

@app.get("/fx/forecast")
def forecast():
    return forex.forecast()

@app.post("/arch/generate")
def generate(building_type: str):
    return arch.generate(building_type)
