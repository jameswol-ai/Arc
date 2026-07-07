import random

class ForexEngine:

    def get_market(self):
        return {
            "USD": 1.0,
            "UGX": 3850 + random.uniform(-10, 10),
            "KES": 155 + random.uniform(-0.5, 0.5),
            "TZS": 2500 + random.uniform(-5, 5),
            "RWF": 1300 + random.uniform(-3, 3),
            "SSP": 1100 + random.uniform(-8, 8),
        }

    def forecast(self):
        import random
        return {
            "trend": random.choice(["UP", "DOWN", "STABLE"]),
            "volatility": round(random.uniform(0.1, 2.0), 2)
        }
