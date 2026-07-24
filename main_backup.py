from fastapi import FastAPI
from forex.engine import ForexEngine
from architecture.engine import ArchitectureEngine

app = FastAPI()

forex = ForexEngine()
arch = ArchitectureEngine()

# =========================
# 💹 FOREX ENDPOINTS
# =========================
@app.get("/fx/rates")
def get_rates():
    return forex.get_market()

@app.get("/fx/forecast")
def get_forecast():
    return forex.analyze()

# =========================
# 🏗️ ARCHITECTURE ENDPOINTS
# =========================
@app.post("/arch/generate")
def generate_plan(building_type: str = "residential"):
    return arch.generate(building_type)
