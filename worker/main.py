import time
import redis
import json

from engines.forex import ForexEngine
from engines.architecture import ArchitectureEngine

r = redis.Redis(host="redis", port=6379, decode_responses=True)

forex = ForexEngine()
arch = ArchitectureEngine()

while True:

    fx = forex.get_market()
    fx_forecast = forex.forecast()

    arch_plan = arch.generate("residential")

    r.publish("fx_stream", json.dumps(fx))
    r.publish("fx_forecast", json.dumps(fx_forecast))
    r.publish("arch_stream", json.dumps(arch_plan))

    time.sleep(3)
