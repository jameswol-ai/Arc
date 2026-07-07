import json

class Exporter:

    def to_json(self, data):
        return json.dumps(data, indent=2)
