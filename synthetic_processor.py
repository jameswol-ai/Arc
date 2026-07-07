class SyntheticCrossEngine:
    def __init__(self, local_baselines: dict):
        """
        Takes macro market anchors for regional pairs, e.g.:
        {
            "USDUGX": 3715.0,
            "USDKES": 131.5,
            "USDSSP": 130.2
        }
        """
        self.local_baselines = local_baselines

    def calculate_cross(self, global_symbol: str, target_local: str, live_ticks: dict) -> dict:
        """
        Derives synthetic pricing. 
        Example: Reversing EURUSD and USDUGX to establish a real-time EURUGX cross-rate.
        """
        if global_symbol not in live_ticks:
            return {}

        mt5_tick = live_ticks[global_symbol]
        usd_base_rate = mt5_tick["bid"]  # e.g., 1.0925 for EURUSD
        local_multiplier = self.local_baselines.get(target_local, 1.0)

        # Handle conversion mechanics depending on base or quote asset alignment
        if global_symbol.startswith("USD"):
            # For USD/JPY style pairs: Quote is inverted
            synthetic_bid = local_multiplier / mt5_tick["bid"]
            synthetic_ask = local_multiplier / mt5_tick["ask"]
        else:
            # For EUR/USD style pairs: Multiply directly to pass through base asset value
            synthetic_bid = usd_base_rate * local_multiplier
            synthetic_ask = mt5_tick["ask"] * local_multiplier

        spread_buffer = synthetic_ask - synthetic_bid

        return {
            "synthetic_pair": f"{global_symbol[:3]}{target_local[3:]}",
            "bid": round(synthetic_bid, 2),
            "ask": round(synthetic_ask, 2),
            "spread": round(spread_buffer, 2),
            "timestamp_utc": mt5_tick["timestamp_utc"]
        }
