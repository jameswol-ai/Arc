# =========================================================
# Arc — ARCHITECTURAL INTELLECT & EAST AFRICAN FOREX ENGINE
# streamlit_app.py – Ram AI, Multi‑FX, Modern UI, Results Tab
# =========================================================

import streamlit as st
import json
import random
import uuid
import hashlib
import requests
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# ═══════════════════════════════════════════════════════
# 0. ENGLISH ONLY – UNIT CONVERSION
# ═══════════════════════════════════════════════════════
M2_TO_FT2 = 10.7639
M_TO_FT = 3.28084

def to_display_length(m):
    if st.session_state.get("unit_system") == "imperial":
        return round(m * M_TO_FT, 1), "ft"
    return round(m, 1), "m"

def to_display_area(m2):
    if st.session_state.get("unit_system") == "imperial":
        return round(m2 * M2_TO_FT2, 1), "sq ft"
    return round(m2, 1), "m²"

# ═══════════════════════════════════════════════════════
# 1. AUTH & USER MANAGEMENT
# ═══════════════════════════════════════════════════════
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USER_FILE = DATA_DIR / "arc_users.json"
XP_PER_LEVEL = 100

def hash_password(password: str) -> str:
    return hashlib.sha256((password + "arc_salt_42").encode()).hexdigest()

def load_users() -> list:
    if USER_FILE.exists():
        try:
            with open(USER_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_users(users: list):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)

def get_user(username: str) -> dict | None:
    for u in load_users():
        if u["username"] == username:
            return u
    return None

def create_user(username: str, password: str, role: str = "user") -> dict:
    users = load_users()
    if get_user(username):
        raise ValueError("Username already exists.")
    user = {
        "username": username,
        "password_hash": hash_password(password),
        "role": role,
        "level": 1,
        "xp": 0,
        "badges": [],
        "created": datetime.now().isoformat()
    }
    users.append(user)
    save_users(users)
    return user

def authenticate(username: str, password: str) -> dict | None:
    user = get_user(username)
    if user and user["password_hash"] == hash_password(password):
        return user
    return None

def update_user_data(username: str, updates: dict):
    users = load_users()
    for u in users:
        if u["username"] == username:
            u.update(updates)
            break
    save_users(users)

def xp_for_level(level: int) -> int:
    return level * XP_PER_LEVEL

def add_xp(username: str, amount: int) -> bool:
    user = get_user(username)
    if not user:
        return False
    old_level = user["level"]
    user["xp"] += amount
    while user["xp"] >= xp_for_level(user["level"]):
        user["xp"] -= xp_for_level(user["level"])
        user["level"] += 1
        badge = f"level_{user['level']}"
        if user["level"] % 5 == 0 and badge not in user["badges"]:
            user["badges"].append(badge)
    update_user_data(username, {"level": user["level"], "xp": user["xp"], "badges": user["badges"]})
    return user["level"] > old_level

# ═══════════════════════════════════════════════════════
# 2. PER‑USER MEMORY
# ═══════════════════════════════════════════════════════
def get_memory_path(username: str) -> Path:
    return DATA_DIR / f"{username}_arc_memory.json"

DEFAULT_STATE = {"designs": [], "concepts": [], "logs": []}

def load_memory(username: str) -> dict:
    path = get_memory_path(username)
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for key in DEFAULT_STATE:
                if key not in data:
                    data[key] = DEFAULT_STATE[key]
            return data
        except:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory(username: str, memory: dict):
    with open(get_memory_path(username), "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

def log_event(username: str, memory: dict, msg: str):
    memory["logs"].append({"time": datetime.now().isoformat(), "msg": msg})
    save_memory(username, memory)

# ═══════════════════════════════════════════════════════
# 3. SAI ENGINE (soil‑aware, isolated random)
# ═══════════════════════════════════════════════════════
ARCH_DOMAINS = {
    "Residential": ["Luxury Villa", "Modern Apartment", "Townhouse Studio"],
    "Commercial": ["Corporate Hub Block", "Boutique Retail Space", "Medical Clinic Center"],
    "Industrial": ["Distribution Depot", "Heavy Machinery Plant Warehouse"],
}

SOIL_MULTIPLIERS = {
    "soft":   1.6,
    "medium": 1.0,
    "rock":   0.7,
}

def generate_spatial_model(domain, btype, plot_size, floors, target_bathrooms, target_country, soil_type, seed=0):
    rng = random.Random(seed if seed else int(time.time()))
    plot_size = max(200, plot_size + rng.randint(-300, 300))
    max_footprint = int(plot_size * rng.uniform(0.5, 0.75))
    floor_area = min(max_footprint, rng.randint(100, int(max_footprint * 1.3)))
    total_gfa = floor_area * floors

    span_length = 6.0 if domain == "Residential" else (7.5 if domain == "Commercial" else 12.0)
    span_length *= rng.uniform(0.85, 1.15)
    col_count = max(8, int((floor_area / (span_length * 5.0)) * rng.uniform(3, 5)))
    beam_count = int(col_count * rng.uniform(1.5, 2.2))

    rooms = [
        {"name": "Central Corridor Gallery", "type": "Corridor", "w": 2.5, "h": 14.0, "color": "#1e293b"},
        {"name": "Main Staircase Core", "type": "Stairs", "w": 4.5, "h": 4.0, "color": "#334155"},
    ]

    if domain == "Residential":
        rooms.append({"name": "Grand Living Room", "type": "Living Room", "w": rng.uniform(6, 8), "h": rng.uniform(5, 6), "color": "#0d2040"})
        rooms.append({"name": "Chef's Kitchen Deck", "type": "Kitchen", "w": rng.uniform(4, 5), "h": rng.uniform(3.5, 4.5), "color": "#053020"})
        bedroom_count = max(1, int(total_gfa / rng.randint(60, 90)))
        for i in range(bedroom_count):
            rooms.append({"name": f"Master Suite {i+1}", "type": "Bedroom", "w": rng.uniform(4, 5), "h": rng.uniform(3.5, 4.5), "color": "#2a0f4d"})
    elif domain == "Commercial":
        rooms.append({"name": "Co-Working Hub Suite", "type": "Office Space", "w": rng.uniform(10, 14), "h": rng.uniform(7, 9), "color": "#075e8a"})
        rooms.append({"name": "Executive Dialogue Hall", "type": "Conference", "w": rng.uniform(5, 7), "h": rng.uniform(4, 6), "color": "#1e1b4b"})
    else:
        rooms.append({"name": "Main Production Bay Floor", "type": "Manufacturing Floor", "w": rng.uniform(16, 20), "h": rng.uniform(10, 14), "color": "#3b0764"})
        rooms.append({"name": "Logistics Dispatch Terminal", "type": "Loading Bay", "w": rng.uniform(7, 9), "h": rng.uniform(7, 9), "color": "#451a03"})

    for b in range(target_bathrooms):
        rooms.append({"name": f"Sanitary Bathroom {b+1}", "type": "Bathroom", "w": rng.uniform(2.5, 3.5), "h": rng.uniform(2, 3), "color": "#4a2306"})

    doors = len(rooms) + floors * rng.randint(1, 3)
    windows = max(4, int(total_gfa / rng.randint(12, 20)))

    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "domain": domain,
        "type": btype,
        "plot_size": plot_size,
        "floors": floors,
        "floor_area": floor_area,
        "total_gfa": total_gfa,
        "rooms": rooms,
        "doors": doors,
        "windows": windows,
        "country": target_country,
        "soil_type": soil_type,
        "structural": {
            "columns": int(col_count * floors),
            "beams": int(beam_count * floors),
            "span": span_length,
        },
    }

def run_eurocode_analysis(d, domain):
    span = d["structural"]["span"]
    gk = random.uniform(4.5, 6.5)
    qk = 2.0 if domain == "Residential" else (3.5 if domain == "Commercial" else 7.5)
    qk *= random.uniform(0.9, 1.1)
    f_ck = random.uniform(25, 35)
    b = random.uniform(250, 350)
    d_eff = random.uniform(400, 500)
    design_load_kpa = (1.35 * gk) + (1.50 * qk)
    w_ed = design_load_kpa * random.uniform(4.0, 5.0)
    m_ed = (w_ed * (span ** 2)) / 8
    m_rd = (0.167 * f_ck * b * (d_eff ** 2)) / 10**6
    return {
        "design_load": f"{design_load_kpa:.2f} kN/m²",
        "m_ed": f"{m_ed:.1f} kNm",
        "m_rd": f"{m_rd:.1f} kNm",
        "uls_status": "PASS ✅" if m_rd > m_ed else "FAIL ❌",
        "f_ck_used": round(f_ck, 1),
        "b_used": round(b),
        "d_eff_used": round(d_eff),
    }

def calculate_ai_scores(asset, ec_result, total_usd, prompt_keywords=None, weights=(0.25,0.25,0.25,0.25)):
    arch_score = 40 + min(30, asset['floors'] * 4) + min(20, len(asset['rooms']) * 2.5)
    arch_score = min(100, arch_score + random.randint(-10, 10))
    try:
        m_ed_val = float(ec_result['m_ed'].split(" ")[0])
        m_rd_val = float(ec_result['m_rd'].split(" ")[0])
        struct_score = 70 + min(30, (m_rd_val - m_ed_val) / m_ed_val * 20)
    except:
        struct_score = 50
    if ec_result['uls_status'] != "PASS ✅":
        struct_score -= random.randint(20, 40)
    struct_score = min(100, max(0, int(struct_score + random.randint(-5, 5))))
    sustain_score = 40 + min(40, int(asset['windows'] * 2.0))
    sustain_score += random.randint(0, 15)
    if prompt_keywords and 'sustain' in prompt_keywords.lower():
        sustain_score += 10
    sustain_score = min(100, sustain_score)
    cost_score = 50
    cost_per_m2 = total_usd / asset['total_gfa']
    if cost_per_m2 < 400:
        cost_score += 30
    elif cost_per_m2 < 600:
        cost_score += 20
    else:
        cost_score += 5
    cost_score = min(100, int(cost_score + random.randint(-5, 5)))
    w_arch, w_struct, w_sust, w_cost = weights
    composite = round(arch_score * w_arch + struct_score * w_struct + sustain_score * w_sust + cost_score * w_cost)
    return arch_score, struct_score, sustain_score, cost_score, composite

# ═══════════════════════════════════════════════════════
# 4. FOREX MODULE (cached)
# ═══════════════════════════════════════════════════════
STATIC_FX_RATES = {
    "Kenya":       129.49,
    "Uganda":      3665.20,
    "Tanzania":    2625.00,
    "South Sudan": 4626.40,
    "Rwanda":      1330.00,
    "Ethiopia":    125.00,
}

_BASE_FX_DATA = {
    "Kenya":       {"currency": "KES", "symbol": "KSh", "multiplier": 1.00, "region": "East Africa"},
    "Uganda":      {"currency": "UGX", "symbol": "USh", "multiplier": 0.95, "region": "East Africa"},
    "Tanzania":    {"currency": "TZS", "symbol": "TSh", "multiplier": 0.98, "region": "East Africa"},
    "South Sudan": {"currency": "SSP", "symbol": "SSP", "multiplier": 1.35, "region": "East Africa"},
    "Rwanda":      {"currency": "RWF", "symbol": "FRw", "multiplier": 0.85, "region": "Central Africa"},
    "Ethiopia":    {"currency": "ETB", "symbol": "Br",  "multiplier": 0.80, "region": "Horn of Africa"},
}

_CURRENT_RATES = {}
_BASELINE_RATES = {}
_CURRENCY_INFO = {}

def _fetch_live_rates():
    try:
        resp = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
        data = resp.json().get("rates", {})
        mapping = {
            "Kenya": "KES", "Uganda": "UGX", "Tanzania": "TZS",
            "South Sudan": "SSP", "Rwanda": "RWF", "Ethiopia": "ETB",
        }
        live = {}
        for country, code in mapping.items():
            if code in data:
                live[country] = data[code]
        return live or None
    except:
        return None

@st.cache_resource
def initialize_fx_rates():
    live = _fetch_live_rates()
    for country, info in _BASE_FX_DATA.items():
        rate = live.get(country, STATIC_FX_RATES.get(country, 1.0)) if live else STATIC_FX_RATES.get(country, 1.0)
        _CURRENT_RATES[country] = rate
        _BASELINE_RATES[country] = rate
        _CURRENCY_INFO[country] = {
            "currency": info["currency"],
            "symbol": info["symbol"],
            "multiplier": info["multiplier"],
            "region": info["region"],
        }
    return _CURRENT_RATES, _BASELINE_RATES, _CURRENCY_INFO

def get_fx_data(country):
    return _CURRENCY_INFO[country].copy() | {"rate": _CURRENT_RATES[country]}

def get_rate(country):
    return _CURRENT_RATES[country]

def get_all_countries():
    return list(_CURRENCY_INFO.keys())

def convert_currency(amount, from_curr, to_curr):
    if from_curr == to_curr:
        return amount
    if from_curr == "USD":
        usd = amount
    else:
        usd = amount / _CURRENT_RATES[from_curr]
    if to_curr == "USD":
        return usd
    else:
        return usd * _CURRENT_RATES[to_curr]

def compute_forex_boq(d, target_country):
    gfa = d["total_gfa"]
    fx_data = get_fx_data(target_country)
    fx_rate = fx_data["rate"]
    regional_multiplier = fx_data["multiplier"]
    soil_mult = SOIL_MULTIPLIERS.get(d.get("soil_type", "medium"), 1.0)

    conc_qty = int(gfa * 0.35)
    steel_qty = int(conc_qty * 0.12)
    brick_qty = int(gfa * 38)
    finish_qty = int(gfa)

    base_usd_items = [
        ("Substructure Earth Excavations", int(gfa * 0.15), 150 * soil_mult),
        ("Structural C30 Concrete", conc_qty, 210),
        ("Tensile Steel Bars (B500B)", steel_qty, 1200),
        ("Blockwork Masonry", brick_qty, 2.5),
        ("Floor Screed & Tiling", finish_qty, 40),
        ("Timber Door Fittings", d["doors"], 300),
        ("Aluminum Window Assemblies", d["windows"], 450),
    ]
    grand_total_usd = 0
    for _, qty, unit_rate in base_usd_items:
        adjusted_rate = unit_rate * regional_multiplier
        grand_total_usd += qty * adjusted_rate
    grand_total_local = grand_total_usd * fx_rate
    return grand_total_usd, grand_total_local, fx_data

initialize_fx_rates()

# ═══════════════════════════════════════════════════════
# 5. MULTI‑CURRENCY FX HISTORY
# ═══════════════════════════════════════════════════════
@st.cache_data(ttl=3600)
def fetch_historical_fx_multi(start_date, end_date):
    currencies = ["KES","UGX","TZS","SSP","RWF","ETB"]
    try:
        url = f"https://api.exchangerate.host/timeseries?start_date={start_date}&end_date={end_date}&base=USD&symbols={','.join(currencies)}"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if "rates" in data:
            rates_dict = data["rates"]
            dates = []
            values = {cur: [] for cur in currencies}
            for date_str, cur_rates in sorted(rates_dict.items()):
                dates.append(date_str)
                for cur in currencies:
                    values[cur].append(cur_rates.get(cur, None))
            df = pd.DataFrame(values, index=pd.to_datetime(dates))
            df = df.ffill()  # forward fill missing
            return df
    except:
        pass
    return None

def plot_multi_fx_history(df):
    if df.empty:
        return None
    fig = go.Figure()
    colors = {"KES":"#38bdf8", "UGX":"#facc15", "TZS":"#4ade80", "SSP":"#fb923c", "RWF":"#c084fc", "ETB":"#f43f5e"}
    for col in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='lines', name=col, line=dict(color=colors.get(col, '#94a3b8'))))
    fig.update_layout(
        title="East African FX Rates (USD base) – 60 days",
        xaxis_title="Date",
        yaxis_title="Rate",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# ═══════════════════════════════════════════════════════
# 6. RAM AI (Infinite Knowledge Engine)
# ═══════════════════════════════════════════════════════
RAM_WISDOM = {
    "soil": [
        "For soft clay soils, consider raft foundations or deep piles. In East Africa, black cotton soil expands when wet—always include a moisture barrier.",
        "Lateritic soils (common in Uganda/Rwanda) have good bearing capacity but require protection from erosion. Use strip footings with adequate cover.",
        "Rocky sites allow cost‑effective pad foundations. However, blasting may be needed and can increase costs by 15-20%.",
    ],
    "foundation": [
        "In seismic zones of the Rift Valley, design foundations with reinforcement continuity and avoid soft‑storey configurations.",
        "Coastal areas (Mombasa, Dar) need corrosion‑resistant steel and concrete with low water‑cement ratio to resist chloride attack.",
    ],
    "cost": [
        "Cement prices in landlocked countries (Uganda, Rwanda, South Sudan) can be 30% higher due to transport. Consider alternative binders.",
        "Steel reinforcement is often imported—monitor global prices and hedge with local pre‑order agreements.",
    ],
    "sustainability": [
        "Maximize natural ventilation by orienting long facades towards prevailing winds (e.g., Indian Ocean monsoon for coastal Kenya/Tanzania).",
        "Rainwater harvesting is essential in semi‑arid regions—design roof catchment with first‑flush diverters.",
    ],
    "default": [
        "Ram says: Begin with a thorough site analysis—soil, climate, and local materials dictate 70% of design success.",
        "In East Africa, labour is affordable but skilled labour is scarce; invest in training and simple, repeatable details.",
        "Always allow for future vertical expansion in rapidly urbanising areas like Nairobi or Addis Ababa.",
    ]
}

def ram_ai_response(prompt, country, domain):
    prompt_lower = prompt.lower()
    # Check keywords
    if "soil" in prompt_lower or "ground" in prompt_lower:
        pool = RAM_WISDOM["soil"]
    elif "foundation" in prompt_lower:
        pool = RAM_WISDOM["foundation"]
    elif "cost" in prompt_lower or "budget" in prompt_lower:
        pool = RAM_WISDOM["cost"]
    elif "sustain" in prompt_lower or "green" in prompt_lower or "eco" in prompt_lower:
        pool = RAM_WISDOM["sustainability"]
    else:
        pool = RAM_WISDOM["default"]
    # Add country-specific flavour
    country_tips = {
        "Kenya": "Nairobi's altitude reduces concrete curing time—adjust schedules.",
        "Uganda": "Kampala's laterite soils are excellent but watch for termite attacks on timber.",
        "Tanzania": "Dar es Salaam's coral limestone demands sulphate‑resistant cement.",
        "South Sudan": "Juba's black cotton soil requires rigorous compaction and possibly soil replacement.",
        "Rwanda": "Kigali's volcanic soil is stable; focus on energy‑efficient cooling strategies.",
        "Ethiopia": "Addis Ababa's seismic activity warrants ductile detailing per Eurocode 8.",
    }
    base_answer = random.choice(pool)
    extra = country_tips.get(country, "")
    return f"**Ram AI Insight:** {base_answer}\n\n📌 *{country} context:* {extra}"

# ═══════════════════════════════════════════════════════
# 7. RENDERERS (unchanged except style)
# ═══════════════════════════════════════════════════════
def render_floorplan_diagram(plan, span=6.0):
    corridor = None
    stairs = None
    other_rooms = []
    for room in plan:
        if room["type"] == "Corridor":
            corridor = room
        elif room["type"] == "Stairs":
            stairs = room
        else:
            other_rooms.append(room)
    if corridor is None:
        corridor = plan[0]
        other_rooms = plan[1:]

    corridor_len = corridor["h"]
    corridor_wid = corridor["w"]

    fig = go.Figure()
    unit_len = "ft" if st.session_state.get("unit_system") == "imperial" else "m"
    span_m = span

    def add_room(x0, y0, x1, y1, color, name, w_m, d_m):
        w_disp, _ = to_display_length(w_m)
        d_disp, _ = to_display_length(d_m)
        fig.add_shape(type="rect",
                      x0=x0, y0=y0, x1=x1, y1=y1,
                      fillcolor=color,
                      line=dict(color="white", width=2),
                      opacity=0.7)
        fig.add_annotation(x=(x0+x1)/2, y=(y0+y1)/2,
                           text=f"<b>{name}</b><br>{w_disp}×{d_disp} {unit_len}",
                           showarrow=False,
                           font=dict(size=10, color="white"),
                           bgcolor="rgba(0,0,0,0.5)")

    max_x = corridor_len + 5
    max_y = corridor_wid + sum([r["h"] for r in other_rooms]) + 5
    grid_spacing = span_m
    for x in np.arange(0, max_x + grid_spacing, grid_spacing):
        fig.add_shape(type="line", x0=x, y0=-max_y, x1=x, y1=max_y,
                      line=dict(color="rgba(56,189,248,0.15)", width=1), layer="below")
    for y in np.arange(-max_y, max_y, grid_spacing):
        fig.add_shape(type="line", x0=0, y0=y, x1=max_x, y1=y,
                      line=dict(color="rgba(56,189,248,0.15)", width=1), layer="below")

    add_room(0, -corridor_wid/2, corridor_len, corridor_wid/2,
             corridor["color"], corridor["name"], corridor["w"], corridor["h"])

    current_x = 1.5
    side = 1
    for room in other_rooms:
        rw = room["w"]
        rd = room["h"]
        if current_x + rw > corridor_len:
            current_x = 1.5
            side = -side
        if side == 1:
            y0 = corridor_wid/2 + 0.5
            y1 = y0 + rd
        else:
            y0 = -corridor_wid/2 - 0.5 - rd
            y1 = y0 + rd
        add_room(current_x, y0, current_x + rw, y1, room["color"], room["name"], rw, rd)

        door_x = current_x + rw/2
        if side == 1:
            door_y = corridor_wid/2
            fig.add_shape(type="path",
                          path=f"M {door_x-0.3},{door_y} Q {door_x-0.3},{door_y+0.6} {door_x+0.3},{door_y+0.6} Q {door_x+0.3},{door_y} {door_x-0.3},{door_y}",
                          line=dict(color="yellow", width=2),
                          fillcolor="rgba(255,255,0,0.2)")
        else:
            door_y = -corridor_wid/2
            fig.add_shape(type="path",
                          path=f"M {door_x-0.3},{door_y} Q {door_x-0.3},{door_y-0.6} {door_x+0.3},{door_y-0.6} Q {door_x+0.3},{door_y} {door_x-0.3},{door_y}",
                          line=dict(color="yellow", width=2),
                          fillcolor="rgba(255,255,0,0.2)")

        arrow_start = (door_x, door_y)
        arrow_end = (door_x, (y0+y1)/2 if side==1 else (y0+y1)/2)
        fig.add_annotation(
            x=arrow_end[0], y=arrow_end[1],
            ax=arrow_start[0], ay=arrow_start[1],
            xref="x", yref="y", axref="x", ayref="y",
            text="", showarrow=True,
            arrowhead=3, arrowsize=1.5, arrowwidth=2, arrowcolor="#facc15"
        )
        current_x += rw + 0.8
        side *= -1

    if stairs:
        stairs_x = corridor_len + 0.5
        stairs_y0 = -corridor_wid/2
        stairs_y1 = corridor_wid/2
        add_room(stairs_x, stairs_y0, stairs_x+stairs["w"], stairs_y1,
                 stairs["color"], stairs["name"], stairs["w"], stairs["h"])
        fig.add_annotation(
            x=stairs_x+stairs["w"]/2, y=0,
            ax=corridor_len-0.5, ay=0,
            xref="x", yref="y", axref="x", ayref="y",
            text="", showarrow=True,
            arrowhead=3, arrowsize=1.5, arrowwidth=2, arrowcolor="#facc15"
        )

    fig.add_annotation(
        x=0.5, y=0,
        ax=-1.0, ay=0,
        xref="x", yref="y", axref="x", ayref="y",
        text="<b>ENTRANCE</b>", showarrow=True,
        arrowhead=3, arrowsize=1.5, arrowwidth=3, arrowcolor="#22c55e",
        font=dict(color="#22c55e")
    )

    fig.update_layout(
        title="🗺️ 2D Floor Plan",
        xaxis=dict(visible=False, showgrid=False, zeroline=False),
        yaxis=dict(visible=False, showgrid=False, zeroline=False, scaleanchor="x", scaleratio=1),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False,
        width=800, height=500
    )
    fig.add_annotation(x=max_x-1, y=-max_y+1, text=f"Grid: {span_m} m × {span_m} m",
                       showarrow=False, font=dict(size=10, color="#38bdf8"), opacity=0.7)
    return fig

def render_plotly_3d_rooms(plan, floors=1, floor_height=3.0, span=6.0):
    traces = []
    min_x, max_x, min_y, max_y = float('inf'), -float('inf'), float('inf'), -float('inf')
    for i, room in enumerate(plan):
        col = i % 3
        row = i // 3
        xc = col * 12
        yc = row * 10
        min_x = min(min_x, xc - room["w"]/2)
        max_x = max(max_x, xc + room["w"]/2)
        min_y = min(min_y, yc - room["h"]/2)
        max_y = max(max_y, yc + room["h"]/2)

    grid_spacing = span * 2
    for x in range(int(min_x/grid_spacing)*int(grid_spacing), int(max_x/grid_spacing+1)*int(grid_spacing)+1, int(grid_spacing)):
        traces.append(go.Scatter3d(x=[x,x], y=[min_y, max_y], z=[0,0], mode='lines', line=dict(color='#1e293b', width=1), showlegend=False))
    for y in range(int(min_y/grid_spacing)*int(grid_spacing), int(max_y/grid_spacing+1)*int(grid_spacing)+1, int(grid_spacing)):
        traces.append(go.Scatter3d(x=[min_x, max_x], y=[y,y], z=[0,0], mode='lines', line=dict(color='#1e293b', width=1), showlegend=False))

    for i, room in enumerate(plan):
        col = i % 3
        row = i // 3
        xc = col * 12
        yc = row * 10
        w = room["w"]
        d = room["h"]
        color = room["color"]
        for f in range(floors):
            z_bottom = f * floor_height
            z_top = z_bottom + floor_height * 0.9
            x_b = [xc-w/2, xc+w/2, xc+w/2, xc-w/2, xc-w/2]
            y_b = [yc-d/2, yc-d/2, yc+d/2, yc+d/2, yc-d/2]
            z_b_arr = [z_bottom]*5
            traces.append(go.Scatter3d(x=x_b, y=y_b, z=z_b_arr, mode='lines', line=dict(color=color, width=2), showlegend=False))
            x_t = [xc-w/2, xc+w/2, xc+w/2, xc-w/2, xc-w/2]
            y_t = [yc-d/2, yc-d/2, yc+d/2, yc+d/2, yc-d/2]
            z_t_arr = [z_top]*5
            traces.append(go.Scatter3d(x=x_t, y=y_t, z=z_t_arr, mode='lines', line=dict(color=color, width=2), showlegend=False))
            for cx, cy in [(xc-w/2, yc-d/2), (xc+w/2, yc-d/2), (xc+w/2, yc+d/2), (xc-w/2, yc+d/2)]:
                traces.append(go.Scatter3d(x=[cx, cx], y=[cy, cy], z=[z_bottom, z_top], mode='lines', line=dict(color=color, width=2), showlegend=False))

    for gx in range(int(min_x/grid_spacing)*int(grid_spacing), int(max_x/grid_spacing+1)*int(grid_spacing)+1, int(grid_spacing)):
        for gy in range(int(min_y/grid_spacing)*int(grid_spacing), int(max_y/grid_spacing+1)*int(grid_spacing)+1, int(grid_spacing)):
            traces.append(go.Scatter3d(x=[gx,gx], y=[gy,gy], z=[0, floors*floor_height],
                                       mode='lines', line=dict(color='#c084fc', width=2, dash='dot'),
                                       showlegend=False))

    fig = go.Figure(data=traces)
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False, showgrid=False),
            yaxis=dict(visible=False, showgrid=False),
            zaxis=dict(visible=False, showgrid=False),
            bgcolor='#040711'
        ),
        paper_bgcolor='#040711',
        margin=dict(l=0, r=0, b=0, t=20),
        showlegend=False,
        title="3D Massing with Column Grid",
        title_font=dict(color='#94a3b8', size=14)
    )
    return fig

def render_isometric_html(plan, span=6.0):
    canvas_w, canvas_h = 800, 380
    unit_len = "ft" if st.session_state.get("unit_system") == "imperial" else "m"
    shapes_js = f"""
    ctx.strokeStyle = 'rgba(56,189,248,0.1)';
    ctx.lineWidth = 1;
    const step = {span*2};
    for(let x=0; x<canvas_w; x+=step) {{
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas_h);
        ctx.stroke();
    }}
    for(let y=0; y<canvas_h; y+=step) {{
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas_w, y);
        ctx.stroke();
    }}
    """
    for idx, r in enumerate(plan):
        offset_x = (idx % 3) * 170 + 100
        offset_y = (idx // 3) * 110 + 130
        rw = min(115, int(r["w"] * 14))
        rh = min(95, int(r["h"] * 14))
        color = r["color"]
        w_disp, _ = to_display_length(r["w"])
        h_disp, _ = to_display_length(r["h"])
        shapes_js += f"""
        ctx.fillStyle = "{color}";
        ctx.beginPath();
        ctx.moveTo({offset_x}, {offset_y});
        ctx.lineTo({offset_x} + {rw}, {offset_y} - {rh}/2);
        ctx.lineTo({offset_x} + {rw} + {rw}, {offset_y});
        ctx.lineTo({offset_x} + {rw}, {offset_y} + {rh}/2);
        ctx.closePath();
        ctx.fill(); ctx.strokeStyle = "rgba(255,255,255,0.3)"; ctx.stroke();
        ctx.fillStyle = "rgba(255,255,255,0.06)";
        ctx.beginPath();
        ctx.moveTo({offset_x}, {offset_y});
        ctx.lineTo({offset_x}, {offset_y} - 40);
        ctx.lineTo({offset_x} + {rw}, {offset_y} + {rh}/2 - 40);
        ctx.lineTo({offset_x} + {rw}, {offset_y} + {rh}/2);
        ctx.closePath(); ctx.fill(); ctx.stroke();
        ctx.fillStyle = "#ffffff"; ctx.font = "bold 11px Space Grotesk";
        ctx.fillText("{r['name']} ({w_disp}×{h_disp} {unit_len})", {offset_x} + 15, {offset_y} - 2);
        """
    grid_label = f"Grid: {span} m × {span} m"
    return f"""
    <div class="canvas-container">
        <canvas id="arc3dCanvas" width="{canvas_w}" height="{canvas_h}" style="max-width:100%; background:#050814;"></canvas>
        <script>
            const canvas = document.getElementById('arc3dCanvas'); const ctx = canvas.getContext('2d');
            {shapes_js}
        </script>
        <div style="text-align:center; color:#38bdf8; font-size:10px; opacity:0.5;">{grid_label}</div>
    </div>
    """

def get_boq_table(asset):
    gfa = asset["total_gfa"]
    fx = asset["fx"]
    multiplier = fx["multiplier"]
    soil_mult = SOIL_MULTIPLIERS.get(asset.get("soil_type", "medium"), 1.0)
    items = [
        ("Substructure Excavations", int(gfa*0.15), 150 * soil_mult),
        ("C30 Concrete (m³)", int(gfa*0.35), 210),
        ("Steel Rebar (kg)", int(gfa*0.35*0.12), 1200),
        ("Blockwork (units)", int(gfa*38), 2.5),
        ("Floor Finishes (m²)", int(gfa), 40),
        ("Doors", asset["doors"], 300),
        ("Windows", asset["windows"], 450)
    ]
    rows = []
    for desc, qty, unit_usd in items:
        adj_rate = unit_usd * multiplier
        usd_total = qty * adj_rate
        local_total = usd_total * fx["rate"]
        rows.append({
            "Item": desc,
            "Qty": qty,
            "Unit (USD)": f"${adj_rate:,.2f}",
            "Total USD": f"${usd_total:,.0f}",
            f"Total {fx['currency']}": f"{fx['symbol']} {local_total:,.0f}"
        })
    return pd.DataFrame(rows)

def describe_concept(asset):
    gfa_m = asset['total_gfa']
    gfa_ft = round(gfa_m * M2_TO_FT2, 1)
    return f"{asset['type']}, {asset['floors']}-storey, {len(asset['plan'])} rooms, in {asset['country']}. GFA: {gfa_m} m² ({gfa_ft} sq ft)"

def generate_gantt_chart(asset):
    gfa = asset["total_gfa"]
    floors = asset["floors"]
    start_date = datetime.today()
    tasks = [("Mobilization", 5), ("Substructure", int(gfa*0.15)), *[(f"Floor {f+1}", 20) for f in range(floors)],
             ("Roofing", 12), ("Finishes", int(gfa*0.02)), ("Commissioning", 14), ("Handover", 3)]
    df = pd.DataFrame(tasks, columns=["Task", "Duration"])
    end_dates = []
    current_end = start_date
    for dur in df["Duration"]:
        current_end += timedelta(days=dur)
        end_dates.append(current_end)
    df["Start"] = [start_date] + end_dates[:-1]
    df["Finish"] = end_dates
    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", title="📅 Construction Gantt Chart")
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        xaxis_title="Date",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        margin=dict(l=0, r=0, t=40, b=20)
    )
    return fig

# ═══════════════════════════════════════════════════════
# 8. MODERN GLASS‑MORPHIC CSS
# ═══════════════════════════════════════════════════════
MODERN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, .stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #141432 100%);
    font-family: 'Inter', sans-serif;
    color: #e2e8f0;
}
.glass-panel {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    transition: all 0.3s ease;
}
.glass-panel:hover {
    border-color: rgba(99, 102, 241, 0.5);
    box-shadow: 0 8px 32px rgba(99, 102, 241, 0.2);
}
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 10px 24px;
    transition: all 0.2s;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(139, 92, 246, 0.6);
}
[data-testid="stSidebar"] {
    background: rgba(10, 10, 30, 0.9);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}
.stTextInput > div > div > input, .stNumberInput input, .stSelectbox > div > div, .stTextArea textarea {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px;
    color: #e2e8f0 !important;
}
.stSlider > div > div > div { background: #6366f1 !important; }
.metric-bar-bg { background: rgba(30,41,59,0.8); border-radius: 6px; height: 6px; }
.metric-bar-fg { border-radius: 6px; background: linear-gradient(90deg, #6366f1, #38bdf8); }
</style>
"""
st.set_page_config(page_title="Arc – Ram AI", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")
st.markdown(MODERN_CSS, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 9. SESSION INITIALISATION
# ═══════════════════════════════════════════════════════
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_data = None
    st.session_state.memory = DEFAULT_STATE.copy()
    st.session_state.generated_concepts = []
    st.session_state.active_design = None
    st.session_state.unit_system = "metric"
    st.session_state.ram_history = []  # for Ram AI chat

if not load_users():
    create_user("admin", "admin123", role="admin")

# ═══════════════════════════════════════════════════════
# 10. LOGIN PAGE
# ═══════════════════════════════════════════════════════
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align:center; color:#6366f1;'>🧠 Arc Station</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#a5b4fc;'>Ram AI – Infinite Architectural Intelligence</p>", unsafe_allow_html=True)
        with st.form("auth_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            col_login, col_reg = st.columns(2)
            with col_login:
                login_btn = st.form_submit_button("🚀 Launch")
            with col_reg:
                register_btn = st.form_submit_button("✨ Register")
            if login_btn:
                user = authenticate(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_data = user
                    st.session_state.memory = load_memory(username)
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
            if register_btn:
                if not username or not password:
                    st.error("Please fill all fields.")
                else:
                    try:
                        create_user(username, password)
                        st.success("Account created! You can now log in.")
                    except ValueError as e:
                        st.error(str(e))
    st.stop()

# ═══════════════════════════════════════════════════════
# 11. LOGGED IN – SIDEBAR CONTROLS
# ═══════════════════════════════════════════════════════
username = st.session_state.username
user_data = st.session_state.user_data
mem = st.session_state.memory

with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:20px;">
        <div style="font-size:1.5rem; font-weight:700; color:#6366f1;">🧠 Arc</div>
        <div style="font-size:0.8rem; color:#a5b4fc;">{username} | Lvl {user_data['level']}</div>
    </div>
    """, unsafe_allow_html=True)
    # Level progress bar
    lvl = user_data["level"]
    xp = user_data["xp"]
    needed = xp_for_level(lvl)
    progress = xp / needed if needed > 0 else 1.0
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
        <span style="font-size:12px; color:#a78bfa;">LVL {lvl}</span>
        <div style="flex:1; height:6px; background:#1e293b; border-radius:3px;">
            <div style="width:{progress*100}%; height:100%; background:linear-gradient(90deg,#6366f1,#38bdf8); border-radius:3px;"></div>
        </div>
        <span style="font-size:10px; color:#94a3b8;">{xp}/{needed} XP</span>
    </div>
    """, unsafe_allow_html=True)

    unit_option = st.selectbox("📏 Unit System", ["Metric (m, m²)", "Imperial (ft, sq ft)"])
    st.session_state.unit_system = "metric" if "Metric" in unit_option else "imperial"

    # Navigation tabs
    nav_page = st.radio("Navigate", ["Dashboard", "Results", "Ram AI"])

    st.markdown("---")

    # Arc Configuration (now includes generate button)
    with st.expander("📐 Arc Configuration", expanded=True):
        select_country = st.selectbox("Target Region", get_all_countries())
        select_domain = st.selectbox("Domain", list(ARCH_DOMAINS.keys()))
        select_type = st.selectbox("Typology", ARCH_DOMAINS[select_domain])
        input_plot = st.slider("Plot Area (m²)", 200, 5000, 800, step=50)
        if st.session_state.unit_system == "imperial":
            area_ft = round(input_plot * M2_TO_FT2, 0)
            st.caption(f"= {area_ft} sq ft")
        input_floors = st.slider("Floors", 1, 12, 3)
        input_baths = st.slider("Bathrooms", 1, 10, 2)
        # Soil type
        soil_labels = {"soft": "Soft Clay/Silt", "medium": "Medium Sand/Gravel", "rock": "Rock/Laterite"}
        selected_soil_label = st.selectbox("🌱 Soil Condition", list(soil_labels.values()))
        selected_soil = [k for k, v in soil_labels.items() if v == selected_soil_label][0]

    with st.expander("⚖️ AI Weights", expanded=False):
        w_arch = st.slider("Architecture", 0.0, 1.0, 0.25, 0.05)
        w_struct = st.slider("Structural", 0.0, 1.0, 0.25, 0.05)
        w_sust = st.slider("Sustainability", 0.0, 1.0, 0.25, 0.05)
        w_cost = st.slider("Cost", 0.0, 1.0, 0.25, 0.05)
        total_w = w_arch + w_struct + w_sust + w_cost
        if total_w > 0:
            w_arch /= total_w; w_struct /= total_w; w_sust /= total_w; w_cost /= total_w
        weights = (w_arch, w_struct, w_sust, w_cost)
        st.caption(f"Norm: arch {w_arch:.2f} struct {w_struct:.2f} sust {w_sust:.2f} cost {w_cost:.2f}")

    # Ram AI Prompt + Generate button
    st.markdown("---")
    st.markdown("### 🧠 Ram AI Prompt")
    prompt_text = st.text_area("Describe your dream project...", placeholder="e.g. A sustainable beach house with open spaces...", height=80)
    if st.button("✨ Generate Concepts", use_container_width=True):
        with st.spinner("Ram AI synthesizing 5 architectural variations..."):
            concepts = []
            for i in range(5):
                mut_plot = input_plot + random.randint(-400, 400)
                mut_floors = max(1, input_floors + random.randint(-2, 2))
                mut_rooms = max(1, input_baths + random.randint(-2, 2))
                d = generate_spatial_model(select_domain, select_type, mut_plot, mut_floors, mut_rooms,
                                           select_country, selected_soil, seed=i)
                d["plan"] = d["rooms"]
                ec = run_eurocode_analysis(d, d["domain"])
                d["eurocode"] = ec
                total_usd, total_local, fx = compute_forex_boq(d, d["country"])
                arch, struct, sust, cost, comp = calculate_ai_scores(d, ec, total_usd, prompt_text, weights)
                d["scores"] = {"arch": arch, "struct": struct, "sust": sust, "cost": cost, "composite": comp}
                d["total_usd"] = total_usd
                d["total_local"] = total_local
                d["fx"] = fx
                concepts.append(d)
            concepts.sort(key=lambda x: x["scores"]["composite"], reverse=True)
            st.session_state.generated_concepts = concepts
            st.session_state.active_design = concepts[0]
            log_event(username, mem, f"Generated 5 concepts. Alpha: {concepts[0]['id']}")
            leveled_up = add_xp(username, 20)
            st.session_state.user_data = get_user(username)
            if leveled_up:
                st.balloons()
            # Switch to Results tab
            nav_page = "Results"
            st.rerun()

    # Forex converter
    with st.expander("💱 Forex Converter"):
        if st.button("🔄 Refresh Rates"):
            initialize_fx_rates.clear()
            initialize_fx_rates()
            st.rerun()
        currencies = ["USD"] + get_all_countries()
        from_cur = st.selectbox("From", currencies, key="conv_from")
        to_cur = st.selectbox("To", currencies, key="conv_to")
        amt = st.number_input("Amount", min_value=0.0, value=1000.0, step=100.0)
        result = convert_currency(amt, from_cur, to_cur)
        sym_from = "$" if from_cur == "USD" else get_fx_data(from_cur)["symbol"]
        sym_to = "$" if to_cur == "USD" else get_fx_data(to_cur)["symbol"]
        st.metric(label=f"{sym_from} {amt:,.2f}", value=f"{sym_to} {result:,.2f}")

    st.markdown("---")
    st.markdown("📂 Project Memory")
    if mem["designs"]:
        for d in mem["designs"][-5:]:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.05); border-radius:8px; padding:8px; margin:4px 0; font-size:0.8rem;">
                🏗️ #{d['id']} - {d['type']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("No designs yet")

    if st.button("🚪 Logout", use_container_width=True):
        save_memory(username, mem)
        st.session_state.logged_in = False
        st.rerun()

# ═══════════════════════════════════════════════════════
# 12. MAIN AREA – TABS (Dashboard / Results / Ram AI)
# ═══════════════════════════════════════════════════════
if nav_page == "Dashboard":
    st.markdown(f"""
    <div class="glass-panel" style="text-align:center; margin-bottom:32px;">
        <h1 style="color:#6366f1; margin:0;">Welcome back, Architect 👋</h1>
        <p style="color:#a5b4fc;">Create. Evolve. Perfect.</p>
    </div>
    """, unsafe_allow_html=True)

    # Live FX rates
    st.markdown("### 💹 Live FX Rates")
    fx_cols = st.columns(6)
    for i, country in enumerate(get_all_countries()):
        data = get_fx_data(country)
        with fx_cols[i]:
            st.markdown(f"""
            <div class="glass-panel" style="padding:12px; text-align:center;">
                <div style="font-size:0.8rem; color:#94a3b8;">{country}</div>
                <div style="font-size:1.4rem; font-weight:700;">{data['symbol']} {data['rate']:.2f}</div>
                <div style="font-size:0.7rem; color:#22c55e;">{data['region']}</div>
            </div>
            """, unsafe_allow_html=True)

    # Multi‑currency FX history
    st.markdown("---")
    with st.expander("📈 East African FX History (60 days)", expanded=True):
        end_date = datetime.today()
        start_date = end_date - timedelta(days=60)
        df_multi = fetch_historical_fx_multi(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        if df_multi is not None and not df_multi.empty:
            fig_multi = plot_multi_fx_history(df_multi)
            if fig_multi:
                st.plotly_chart(fig_multi, use_container_width=True)
            else:
                st.warning("Could not plot multi‑currency chart.")
        else:
            st.info("Live multi‑currency data unavailable – showing simulated trends.")
            # Simulate
            base_rates = {c: get_rate(c) for c in get_all_countries()}
            sim_data = {}
            dates = [start_date + timedelta(days=i) for i in range(61)]
            for country, rate in base_rates.items():
                rng = np.random.default_rng(42)
                steps = rng.normal(0, 0.005, len(dates))
                values = [rate]
                for s in steps:
                    values.append(values[-1] * (1 + s))
                sim_data[country] = values[1:]
            df_sim = pd.DataFrame(sim_data, index=dates[1:])
            fig_sim = plot_multi_fx_history(df_sim)
            if fig_sim:
                st.plotly_chart(fig_sim, use_container_width=True)

    # Ram Suggestions (dynamic)
    st.markdown("---")
    st.markdown("### 🧠 Ram AI Suggestions")
    if st.button("🔄 Refresh Suggestions"):
        st.rerun()
    suggestions = [
        "**Kenya:** Nairobi's red coffee soil needs deep foundations—consider raft or pile.",
        "**Uganda:** Lateritic soils are stable but require erosion control; use terracing on slopes.",
        "**Tanzania:** Coastal corrosion is real—use high‑grade concrete and galvanized rebar.",
        "**South Sudan:** Black cotton soil expands—always include a moisture barrier and flexible joints.",
        "**Rwanda:** Volcanic soil has excellent bearing capacity; go for lightweight steel framing.",
        "**Ethiopia:** Addis Ababa is seismically active—follow Eurocode 8 detailing for ductility.",
    ]
    cols = st.columns(3)
    for i, sug in enumerate(suggestions):
        with cols[i % 3]:
            st.markdown(f'<div class="glass-panel" style="padding:12px; font-size:0.85rem;">{sug}</div>', unsafe_allow_html=True)

    # Stats
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="glass-panel" style="text-align:center;">', unsafe_allow_html=True)
        st.metric("Total Blueprints", len(mem["designs"]), delta="+1")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="glass-panel" style="text-align:center;">', unsafe_allow_html=True)
        st.metric("Arch Concepts", len(mem["designs"]) * 5, delta="Evolving")
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="glass-panel" style="text-align:center;">', unsafe_allow_html=True)
        st.metric("Pipeline Logs", len(mem["logs"]))
        st.markdown('</div>', unsafe_allow_html=True)

elif nav_page == "Results":
    if st.session_state.generated_concepts:
        concepts = st.session_state.generated_concepts
        st.markdown("## 🔬 Evolution Engine Results")
        st.markdown("*5 unique design concepts evaluated by Sai AI Agents*")
        concept_names = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
        colors = ["#4ade80", "#eab308", "#3b82f6", "#8b5cf6", "#ec4899"]
        tabs = st.tabs(concept_names[:len(concepts)])
        for idx, (tab, c) in enumerate(zip(tabs, concepts)):
            with tab:
                sc = c["scores"]
                ec = c["eurocode"]
                st.markdown(f"**Design brief:** {describe_concept(c)}")
                col1, col2 = st.columns([3, 2])
                with col1:
                    st.markdown("### 🗺️ 2D Floor Plan")
                    fig_fp = render_floorplan_diagram(c["plan"], span=c["structural"]["span"])
                    st.plotly_chart(fig_fp, use_container_width=True, key=f"fp_{idx}")
                    st.caption(f"Floor Area: {c['floor_area']} m² | {c['floors']} floors | {c['country']}")
                    with st.expander("🧱 Material Breakdown"):
                        st.dataframe(get_boq_table(c), use_container_width=True)
                with col2:
                    for label_key, key, bar_color in [
                        ('🏛️ Architect AI', 'arch', '#4ade80'),
                        ('⚙️ Structural AI', 'struct', '#00d2ff'),
                        ('🌱 Sustainability AI', 'sust', '#38bdf8'),
                        ('💰 Cost AI', 'cost', '#facc15')
                    ]:
                        st.markdown(f"""
                        <div style="margin-bottom:6px;">
                            <div style="display:flex; align-items:center; font-size:12px; color:#94a3b8;">{label_key} {sc[key]}%</div>
                            <div class="metric-bar-bg"><div class="metric-bar-fg" style="width:{sc[key]}%; background:{bar_color};"></div></div>
                        </div>
                        """, unsafe_allow_html=True)
                    st.metric("USD Total", f"${c['total_usd']:,.0f}")
                    st.metric(f"Local ({c['fx']['currency']})", f"{c['fx']['symbol']} {c['total_local']:,.0f}")
                    st.markdown("### 📦 3D Massing")
                    view_mode = st.radio("View", ["Isometric", "Interactive"], horizontal=True, key=f"3d_{idx}")
                    if view_mode == "Isometric":
                        st.components.v1.html(render_isometric_html(c["plan"], span=c["structural"]["span"]), height=400)
                    else:
                        fig3d = render_plotly_3d_rooms(c["plan"], floors=c["floors"], span=c["structural"]["span"])
                        st.plotly_chart(fig3d, use_container_width=True, key=f"3d_{idx}")

        # Radar comparison
        with st.expander("📊 AI Score Radar", expanded=False):
            radar_data = []
            for i, c in enumerate(concepts):
                sc = c["scores"]
                radar_data.append({"Concept": f"{concept_names[i]} ({c['type']})",
                                   "Architecture": sc["arch"], "Structural": sc["struct"],
                                   "Sustainability": sc["sust"], "Cost Efficiency": sc["cost"]})
            df_radar = pd.DataFrame(radar_data)
            categories = list(df_radar.columns[1:])
            fig_radar = go.Figure()
            for i, row in df_radar.iterrows():
                fig_radar.add_trace(go.Scatterpolar(r=row[categories].values, theta=categories,
                                                     fill='toself', name=row["Concept"], line_color=colors[i]))
            fig_radar.update_layout(polar=dict(radialaxis=dict(range=[0,100], showticklabels=False)),
                                    showlegend=True, paper_bgcolor='rgba(0,0,0,0)', font_color='#94a3b8')
            st.plotly_chart(fig_radar, use_container_width=True)

        # Top recommendation & save/export
        asset = concepts[0]
        st.markdown("---")
        st.markdown("### 🏆 Top Recommendation: CONCEPT ALPHA")
        col_save, col_export = st.columns(2)
        with col_save:
            if st.button("💾 Save to Library"):
                mem["designs"].append({
                    "id": asset["id"], "type": asset["type"], "country": asset["country"],
                    "total_gfa": asset["total_gfa"], "scores": asset["scores"],
                    "plan": asset["plan"], "timestamp": datetime.now().isoformat()
                })
                save_memory(username, mem)
                st.success("Saved!")
        with col_export:
            export_df = pd.DataFrame([{
                "ID": c["id"], "Type": c["type"], "Country": c["country"], "Soil": c.get("soil_type","medium"),
                "GFA": c["total_gfa"], "Floors": c["floors"], "Rooms": len(c["plan"]),
                "Cost USD": c["total_usd"], "Cost Local": c["total_local"],
                "Arch%": c["scores"]["arch"], "Struct%": c["scores"]["struct"],
                "Sust%": c["scores"]["sust"], "CostEff%": c["scores"]["cost"], "Composite": c["scores"]["composite"]
            } for c in concepts])
            csv = export_df.to_csv(index=False).encode()
            st.download_button("📥 Export CSV", csv, file_name="arc_concepts.csv", mime="text/csv")

        st.markdown("---")
        with st.expander("📅 Construction Gantt"):
            fig_gantt = generate_gantt_chart(asset)
            st.plotly_chart(fig_gantt, use_container_width=True)
    else:
        st.info("No designs generated yet. Go to sidebar, enter your prompt and click **Generate Concepts**.")

elif nav_page == "Ram AI":
    st.markdown("## 🧠 Ram AI – Infinite Architectural Knowledge")
    st.markdown("Ask Ram anything about construction, soil, costs, or design in East Africa.")
    with st.form("ram_form"):
        user_question = st.text_input("Your question:", placeholder="e.g., What foundation for black cotton soil in Juba?")
        submitted = st.form_submit_button("Ask Ram AI")
    if submitted and user_question:
        with st.spinner("Ram is thinking..."):
            response = ram_ai_response(user_question, select_country, select_domain)
            st.session_state.ram_history.append(("You", user_question))
            st.session_state.ram_history.append(("Ram", response))
    # Display chat history
    for speaker, msg in st.session_state.ram_history:
        if speaker == "You":
            st.markdown(f"**👤 {speaker}:** {msg}")
        else:
            st.markdown(f'**🧠 {speaker}:** {msg}')