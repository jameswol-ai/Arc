import numpy as np
import random

class ArchitectureEngine:
    def __init__(self):
        self.grid_size = 10

    # -----------------------------
    # 🧱 FLOOR GRID GENERATOR
    # -----------------------------
    def generate_grid(self, size=10):
        grid = np.zeros((size, size))
        return grid

    # -----------------------------
    # 🏠 ROOM ZONING SYSTEM
    # -----------------------------
    def generate_floor_plan(self, size=10, rooms=4):
        grid = self.generate_grid(size)

        zones = ["Living", "Kitchen", "Bedroom", "Bathroom", "Office"]
        layout = []

        for i in range(rooms):
            w, h = random.randint(2, 4), random.randint(2, 4)
            x = random.randint(0, size - w - 1)
            y = random.randint(0, size - h - 1)

            label = random.choice(zones)

            grid[x:x+w, y:y+h] = i + 1

            layout.append({
                "room": label,
                "x": x,
                "y": y,
                "w": w,
                "h": h
            })

        return grid, layout

    # -----------------------------
    # 🪜 STAIR PLACEMENT LOGIC
    # -----------------------------
    def place_stairs(self, grid):
        size = grid.shape[0]
        x, y = random.randint(1, size-2), random.randint(1, size-2)
        grid[x][y] = 9  # stair marker
        return grid, (x, y)

    # -----------------------------
    # 📐 "EUROCODE-LITE" CHECKS
    # -----------------------------
    def structural_check(self, layout):
        warnings = []

        total_rooms = len(layout)

        if total_rooms < 2:
            warnings.append("❌ Too few rooms for structural viability")

        max_size = max([r["w"] * r["h"] for r in layout])

        if max_size > 12:
            warnings.append("⚠️ Large unsupported span detected (beam reinforcement needed)")

        if not warnings:
            warnings.append("✅ Structure passes basic heuristic checks")

        return warnings
