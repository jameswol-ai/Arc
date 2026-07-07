class Constraints:
    def validate_room_sizes(self, rooms):
        return all(10 <= r["size"] <= 50 for r in rooms)

    def enforce_zoning(self, plan):
        required = ["kitchen", "bathroom", "living"]
        return all(any(r["type"] == x for r in plan["rooms"]) for x in required)
