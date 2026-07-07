import random

class ForexData:
    def get_rates(self):
        # Replace later with real API (Fixer / ECB / AlphaVantage)
        return {
            "USD": 1.0,
            "UGX": 3850 + random.uniform(-50, 50),
            "KES": 155 + random.uniform(-3, 3),
            "TZS": 2500 + random.uniform(-40, 40),
            "RWF": 1300 + random.uniform(-20, 20),
            "SSP": 1100 + random.uniform(-30, 30),
        }
