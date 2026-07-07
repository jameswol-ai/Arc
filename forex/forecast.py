import numpy as np

class ForexForecast:
    def predict_trend(self, series):
        # simple slope-based forecast (replace with ML later)
        x = np.arange(len(series))
        y = np.array(series)

        slope = np.polyfit(x, y, 1)[0]

        return {
            "trend_slope": float(slope),
            "direction": "UP" if slope > 0 else "DOWN"
        }
