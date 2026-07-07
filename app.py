# =========================================================
# ARC — ARCHITECTURAL INTELLECT & EAST AFRICAN FOREX ENGINE
# Multi-Story Floor Plan, Eurocode Selector & Zoning Engine
# Zero-Dependency Single-File Streamlit Implementation (v17 — Dynamic Structural & Intelligent Layout)
# =========================================================

import streamlit as st
import json
import uuid
import random
import math
from pathlib import Path
from datetime import datetime, timedelta

# =========================================================
# SYSTEM CONFIG & UI STYLING
# =========================================================

st.set_page_config(
    page_title="Arc Studio | Oculus Rift",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

MEMORY_FILE = Path("arc_studio_v15.json")

# =========================================================
# STUNNING CUSTOM THEME — DEEP SPACE / NEON CYBERPUNK
# =========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;700&display=swap');
    
    /* ---------- GLOBAL RESETS ---------- */
    html, body, [data-testid="stAppViewContainer"], .main {
        background: radial-gradient(ellipse at 20% 50%, #0a0f1c 0%, #03050b 70%);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #e0e7ff;
        scrollbar-width: thin;
        scrollbar-color: #1e293b #0b0f19;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0b0f19;
    }
    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #4b5563;
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #e0e7ff, #a5b4fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.8rem;
    }
    
    p, li, span, div {
        color: #cbd5e1;
    }

    /* ---------- SIDEBAR ---------- */
    [data-testid="stSidebar"] {
        background: linear-gradient(145deg, #060b17 0%, #030712 100%);
        border-right: 1px solid rgba(56, 189, 248, 0.15);
        box-shadow: 4px 0 30px rgba(0, 229, 255, 0.05);
    }
    [data-testid="stSidebar"] * {
        color: #cbd5e1 !important;
    }
    [data-testid="stSidebar"] .stSelectbox label, 
    [data-testid="stSidebar"] .stSlider label {
        font-weight: 600;
        color: #94a3b8 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .sidebar .st-emotion-cache-1wrcr7h, .sidebar .st-emotion-cache-1xarl3l {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid #2d3a5a;
        border-radius: 10px;
        padding: 10px;
    }

    /* ---------- METRIC CARDS ---------- */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.4));
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 18px;
        padding: 18px 22px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4), 0 0 0 1px rgba(56, 189, 248, 0.1) inset;
        transition: all 0.3s ease;
        backdrop-filter: blur(4px);
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: #38bdf8;
        box-shadow: 0 12px 40px rgba(0, 229, 255, 0.15);
    }
    div[data-testid="stMetric"] label {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.85rem;
        color: #94a3b8 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #f8fafc;
        text-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
    }

    /* ---------- BUTTONS ---------- */
    .stButton > button {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #38bdf8;
        color: #e0e7ff;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 700;
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: 0.02em;
        transition: all 0.3s ease;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.2);
        text-transform: uppercase;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #0f172a, #020617);
        border-color: #f59e0b;
        color: #f59e0b;
        box-shadow: 0 0 25px #f59e0b80;
        transform: translateY(-2px);
    }

    /* ---------- TABS (GLOWING PILLS) ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(15, 23, 42, 0.7);
        border-radius: 30px;
        padding: 10px 24px;
        font-weight: 600;
        border: 1px solid #2d3a5a;
        color: #cbd5e1;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(30, 41, 59, 0.8);
        border-color: #38bdf8;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1e3a5f, #0f172a) !important;
        border-color: #38bdf8 !important;
        color: #38bdf8 !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.3);
        font-weight: 700;
    }

    /* ---------- CUSTOM CARDS (Room Cards) ---------- */
    .blueprint-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
        gap: 18px;
        background: transparent;
        padding: 0;
        margin: 20px 0;
    }
    .room-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.3));
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5);
        backdrop-filter: blur(4px);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .room-card:hover {
        transform: translateY(-6px) scale(1.02);
        border-color: #f59e0b;
        box-shadow: 0 0 35px rgba(245, 158, 11, 0.3);
    }
    .room-name {
        font-size: 1.2rem;
        font-weight: 700;
        font-family: 'Space Grotesk', sans-serif;
        margin-bottom: 8px;
        background: linear-gradient(to right, #e0e7ff, #a5b4fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .room-specs {
        font-family: 'Space Grotesk', monospace;
        font-size: 0.85rem;
        letter-spacing: 0.02em;
        opacity: 0.7;
    }

    /* ---------- SLIDERS / SELECTS / INPUTS ---------- */
    .stSlider, .stSelectbox, .stNumberInput {
        background: transparent !important;
    }
    .stSlider > div > div > div > div {
        background: #1e293b;
        border-radius: 5px;
    }
    
    /* ---------- GLOWING DIVIDERS ---------- */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #38bdf8, transparent);
        margin: 30px 0;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# DATA CONFIGURATIONS (unchanged)
# =========================================================

REGIONAL_FX = {
    "Kenya": {"currency": "KES", "rate_to_usd": 129.49, "symbol": "KSh", "cost_multiplier": 1.0, "risk_premium": 0.02},
    "Uganda": {"currency": "UGX", "rate_to_usd": 3665.20, "symbol": "USh", "cost_multiplier": 0.95, "risk_premium": 0.03},
    "Tanzania": {"currency": "TZS", "rate_to_usd": 2625.00, "symbol": "TSh", "cost_multiplier": 0.98, "risk_premium": 0.025},
    "South Sudan": {"currency": "SSP", "rate_to_usd": 4626.40, "symbol": "SSP", "cost_multiplier": 1.35, "risk_premium": 0.08}
}

ARCH_DOMAINS = {
    "Residential": {
        "types": ["Luxury Villa", "Modern Apartment", "Townhouse Studio"],
        "max_coverage": 0.50,
        "max_far": 2.5
    },
    "Commercial": {
        "types": ["Corporate Hub Block", "Boutique Retail Space", "Medical Clinic Center"],
        "max_coverage": 0.70,
        "max_far": 4.5
    },
    "Industrial": {
        "types": ["Distribution Depot", "Heavy Machinery Plant Warehouse"],
        "max_coverage": 0.60,
        "max_far": 1.8
    }
}

SOIL_PROFILES = {
    "Kampala Red Lateritic Clay": {"cohesion": 35, "friction_angle": 12, "unit_weight": 18.0, "description": "Highly weathered cohesive soil profile"},
    "Nairobi Black Cotton Soil": {"cohesion": 15, "friction_angle": 8, "unit_weight": 16.5, "description": "High expansivity index, requires deep mechanics"},
    "Coastal Quartz Sand (Dar)": {"cohesion": 0, "friction_angle": 32, "unit_weight": 19.0, "description": "Cohesionless granular clean sand stratum"},
    "Juba Alluvial Silt Deposit": {"cohesion": 20, "friction_angle": 15, "unit_weight": 17.5, "description": "Moderate settlement vulnerability under cyclic loading"}
}

# =========================================================
# STATE MANAGEMENT (unchanged)
# =========================================================

DEFAULT_STATE = {
    "designs": [],
    "logs": []
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory():
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.memory, f, indent=2)
    except Exception:
        pass

def log_event(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "active_design" not in st.session_state:
    st.session_state.active_design = None

# =========================================================
# INTELLIGENT FLOOR PLAN LAYOUT ENGINE
# =========================================================

def generate_intelligent_layout(rooms, nx, ny, span):
    """
    Returns a 2D list (ny rows × nx cols) where each cell is a dict:
      {'room_index': int, 'room_name': str, 'color': str}
    Places a central corridor row and distributes other rooms into wings.
    """
    # Separate circulation from other rooms
    circulation = [r for r in rooms if r["type"] == "Circulation"]
    other = [r for r in rooms if r["type"] != "Circulation"]

    grid = [[None for _ in range(nx)] for _ in range(ny)]

    # Corridor row: middle row (index floor(ny/2))
    corridor_row = ny // 2
    corridor_name = "Main Corridor Gallery"
    corridor_color = "#1e293b"
    # Use the first circulation room if available, else placeholder
    if circulation:
        corridor_idx = rooms.index(circulation[0])
    else:
        corridor_idx = None

    for col in range(nx):
        grid[corridor_row][col] = {
            "room_index": corridor_idx,
            "room_name": corridor_name,
            "color": corridor_color
        }

    # Distribute remaining rooms into rows above and below corridor
    rows_above = list(range(0, corridor_row))
    rows_below = list(range(corridor_row+1, ny))
    row_pool = rows_above + rows_below   # simple concatenation

    # Group by type to keep similar rooms together
    private = [r for r in other if r["type"] == "Private"]
    public = [r for r in other if r["type"] in ("Living Space", "Workspace")]
    service = [r for r in other if r["type"] in ("Utility", "Sanitary", "Industrial")]
    ordered_rooms = public + private + service   # public first

    room_idx = 0
    for row in row_pool:
        for col in range(nx):
            if room_idx >= len(ordered_rooms):
                break
            room = ordered_rooms[room_idx]
            grid[row][col] = {
                "room_index": rooms.index(room),
                "room_name": room["name"],
                "color": room["color"]
            }
            room_idx += 1
        if room_idx >= len(ordered_rooms):
            break

    # If any rooms left (more rooms than cells), fill remaining cells
    while room_idx < len(ordered_rooms):
        for row in range(ny):
            for col in range(nx):
                if grid[row][col] is None:
                    grid[row][col] = {
                        "room_index": rooms.index(ordered_rooms[room_idx]),
                        "room_name": ordered_rooms[room_idx]["name"],
                        "color": ordered_rooms[room_idx]["color"]
                    }
                    room_idx += 1
                    if room_idx >= len(ordered_rooms):
                        break
            if room_idx >= len(ordered_rooms):
                break

    return grid

# =========================================================
# SPATIAL SYNTHESIS ENGINE (SAI) — upgraded with loads & layout
# =========================================================

def generate_building_model(domain, btype, floors, bathrooms, country, material_frame, plot_size, soil_type,
                            g_k, q_k, steel_section):
    rooms = []
    rooms.append({"name": "Main Corridor Gallery", "type": "Circulation", "w": 3, "h": 12, "color": "#1e293b", "doors": 3, "windows": 1})

    if floors > 1:
        core_type = "Elevator Shaft" if domain == "Commercial" or floors > 4 else "Stairwell Core"
        rooms.append({"name": f"Vertical {core_type}", "type": "Circulation", "w": 4, "h": 4, "color": "#334155", "doors": floors, "windows": 0})

    if domain == "Residential":
        rooms.append({"name": "Grand Living Room", "type": "Living Space", "w": 8, "h": 6, "color": "#0d2040", "doors": 2, "windows": 4})
        rooms.append({"name": "Chef's Kitchen Deck", "type": "Utility", "w": 4, "h": 4, "color": "#053020", "doors": 1, "windows": 2})
        bedroom_count = max(1, floors)
        for i in range(bedroom_count):
            rooms.append({"name": f"Master Suite Room {i+1}", "type": "Private", "w": 5, "h": 4, "color": "#2a0f4d", "doors": 1, "windows": 2})
    elif domain == "Commercial":
        rooms.append({"name": "Co-Working Hub Suite", "type": "Workspace", "w": 12, "h": 8, "color": "#075e8a", "doors": 3, "windows": 6})
        rooms.append({"name": "Executive Dialogue Hall", "type": "Workspace", "w": 6, "h": 5, "color": "#1e1b4b", "doors": 1, "windows": 2})
    else:
        rooms.append({"name": "Main Production Floor", "type": "Industrial", "w": 20, "h": 12, "color": "#3b0764", "doors": 2, "windows": 8})
        rooms.append({"name": "Logistics Dispatch Terminal", "type": "Industrial", "w": 8, "h": 8, "color": "#451a03", "doors": 2, "windows": 1})

    for b in range(bathrooms):
        rooms.append({"name": f"Sanitary Bathroom {b+1}", "type": "Sanitary", "w": 3, "h": 3, "color": "#4a2306", "doors": 1, "windows": 1})

    total_doors = sum(r["doors"] for r in rooms)
    total_windows = sum(r["windows"] for r in rooms)

    ground_footprint = sum(r["w"] * r["h"] for r in rooms)
    gfa = ground_footprint * floors

    span_length = 6.0 if domain == "Residential" else (7.5 if domain == "Commercial" else 12.0)
    col_count = max(12, int((ground_footprint / (span_length * 4.0)) * 4))
    beam_count = int(col_count * 1.8)

    # Compute grid dimensions for intelligent layout
    bay_area = span_length * span_length
    total_bays = max(2, math.ceil(ground_footprint / bay_area))
    nx = max(2, math.ceil(math.sqrt(total_bays)))
    ny = max(2, math.ceil(total_bays / nx))
    layout_grid = generate_intelligent_layout(rooms, nx, ny, span_length)

    return {
        "id": str(uuid.uuid4())[:6].upper(),
        "domain": domain,
        "type": btype,
        "floors": floors,
        "ground_footprint": ground_footprint,
        "total_gfa": gfa,
        "doors": total_doors,
        "windows": total_windows,
        "country": country,
        "rooms": rooms,
        "material_frame": material_frame,
        "plot_size": plot_size,
        "soil_type": soil_type,
        "structural": {
            "columns": int(col_count * floors),
            "beams": int(beam_count * floors),
            "span": span_length
        },
        "loads": {
            "g_k": g_k,
            "q_k": q_k,
            "steel_section": steel_section
        },
        "layout": {
            "grid": layout_grid,
            "nx": nx,
            "ny": ny
        }
    }

# =========================================================
# ENGINEERING & COMPLIANCE — Dynamic Structural Analysis
# =========================================================

def run_eurocode_analysis(design):
    span = design["structural"]["span"]
    domain = design["domain"]
    material_frame = design["material_frame"]
    soil_type = design["soil_type"]
    floors = design["floors"]
    loads = design["loads"]
    g_k = loads["g_k"]
    q_k = loads["q_k"]

    # ----- ULS bending with actual tributary width -----
    design_load_kpa = (1.35 * g_k) + (1.50 * q_k)
    tributary_width = span          # regular grid
    w_ed = design_load_kpa * tributary_width   # kN/m
    m_ed = (w_ed * (span ** 2)) / 8             # kNm (simply supported)

    # ----- Material resistance -----
    if material_frame == "Reinforced Concrete (Eurocode 2)":
        b = 300            # mm
        d_eff = 450        # mm (cover assumed)
        f_ck = 30          # MPa
        f_yk = 500         # MPa

        M_ed_Nmm = m_ed * 1e6
        z = 0.95 * d_eff
        A_s_req = M_ed_Nmm / (0.87 * f_yk * z)   # mm²

        # Simplified iterative improvement
        x = (A_s_req * 0.87 * f_yk) / (0.85 * f_ck * b * 0.8)
        if x > 0.45 * d_eff:
            A_s_req *= 1.2
        bar_dia = 20
        bar_area = 3.14159 * (bar_dia**2) / 4
        n_bars = max(2, math.ceil(A_s_req / bar_area))
        A_s_prov = n_bars * bar_area

        x_prov = (A_s_prov * 0.87 * f_yk) / (0.85 * f_ck * b * 0.8)
        z_prov = d_eff - 0.4 * x_prov
        m_rd = (0.87 * f_yk * A_s_prov * z_prov) / 1e6
        standard_label = f"RC Beam {b}×{d_eff}mm, {n_bars}H{bar_dia} ({A_s_prov:.0f} mm²)"
        code_ref = "EC2 – Rectangular Stress Block"
        formula_latex = r"M_{Rd} = 0.87 \cdot f_{yk} \cdot A_s \cdot z"

    elif material_frame == "Structural Steel Profile (Eurocode 3)":
        STEEL_SECTIONS = {
            "UB 254x146x31":  {"Wpl_y": 377e3, "fy": 275},
            "UB 305x165x40": {"Wpl_y": 623e3, "fy": 275},
            "UC 254x254x73": {"Wpl_y": 1090e3, "fy": 275},
            "UC 305x305x97": {"Wpl_y": 1869e3, "fy": 275},
        }
        sec_name = loads["steel_section"]
        sec = STEEL_SECTIONS[sec_name]
        Wpl = sec["Wpl_y"]
        fy = sec["fy"]
        gamma_m0 = 1.0
        m_rd = (Wpl * fy) / gamma_m0 / 1e6
        standard_label = f"Steel {sec_name} (Wpl={Wpl/1e3:.0f} cm³)"
        code_ref = "EC3 – Plastic Section Resistance"
        formula_latex = r"M_{pl,Rd} = \frac{W_{pl} \cdot f_y}{\gamma_{M0}}"

    else:   # Timber Eurocode 5
        f_mk = 24.0
        k_mod = 0.80
        gamma_m = 1.3
        b_timber = 200
        h_timber = 500
        W_el = (b_timber * (h_timber ** 2)) / 6
        m_rd = (k_mod * f_mk / gamma_m * W_el) / 1e6
        standard_label = f"Timber {b_timber}×{h_timber}mm (GL24h)"
        code_ref = "EC5 – Solid Timber Bending"
        formula_latex = r"M_{Rd} = \frac{k_{mod} \cdot f_{m,k}}{\gamma_M} \cdot W"

    # ----- SLS deflection (quasi‑permanent combination) -----
    psi2 = 0.3 if domain == "Residential" else (0.6 if domain == "Commercial" else 0.8)
    service_load = g_k + psi2 * q_k
    w_service = service_load * tributary_width
    if "Concrete" in material_frame:
        E = 200000   # N/mm²
        I = (300 * 450**3) / 12
    elif "Steel" in material_frame:
        E = 200000
        I = 150e6   # approximate for UC section
    else:
        E = 11000   # timber
        I = (200 * 500**3) / 12
    est_deflection = (5 * w_service * (span * 1000)**4) / (384 * E * I)
    allowable_deflection = (span * 1000) / 250
    sls_status = "PASS (Deflection OK)" if est_deflection <= allowable_deflection else "FAIL (Excessive Deflection)"

    # ----- EC7 Foundation (based on actual column load) -----
    soil = SOIL_PROFILES[soil_type]
    phi_rad = math.radians(soil["friction_angle"])
    n_q = (math.tan(math.pi/4 + phi_rad/2)**2) * math.exp(math.pi * math.tan(phi_rad))
    n_c = (n_q - 1) / math.tan(phi_rad) if soil["friction_angle"] > 0 else 5.14
    n_gamma = 2 * (n_q + 1) * math.tan(phi_rad)

    b_footing = 1.5  # m (could be sized later)
    d_footing = 1.2
    q_ultimate = (1.3 * soil["cohesion"] * n_c +
                  soil["unit_weight"] * d_footing * n_q +
                  0.4 * soil["unit_weight"] * b_footing * n_gamma)
    gamma_rv = 1.4
    q_rd = q_ultimate / gamma_rv

    tributary_area_per_column = span * span
    column_load_per_floor = tributary_area_per_column * design_load_kpa
    total_column_load = column_load_per_floor * floors
    applied_bearing_pressure = total_column_load / (b_footing ** 2)
    geo_status = "PASS (Bearing OK)" if q_rd > applied_bearing_pressure else "FAIL (Soil Failure)"

    return {
        "design_load": f"{design_load_kpa:.2f} kN/m²",
        "m_ed": f"{m_ed:.1f} kNm",
        "m_rd": f"{m_rd:.1f} kNm",
        "label": standard_label,
        "code_ref": code_ref,
        "formula_latex": formula_latex,
        "uls_status": "PASS (Structural OK)" if m_rd > m_ed else "FAIL (Increase Section)",
        "deflection_limit": f"{allowable_deflection:.1f} mm",
        "calculated_deflection": f"{est_deflection:.1f} mm",
        "sls_status": sls_status,
        "q_rd": f"{q_rd:.1f} kPa",
        "applied_bearing": f"{applied_bearing_pressure:.1f} kPa",
        "geo_status": geo_status
    }

# =========================================================
# ZONING & BOQ (unchanged)
# =========================================================

def verify_zoning_laws(footprint, gfa, plot_size, domain):
    limits = ARCH_DOMAINS[domain]
    actual_coverage = footprint / plot_size
    actual_far = gfa / plot_size
    coverage_pass = actual_coverage <= limits["max_coverage"]
    far_pass = actual_far <= limits["max_far"]
    return {
        "coverage_pct": actual_coverage * 100,
        "max_coverage_pct": limits["max_coverage"] * 100,
        "coverage_status": "PASS" if coverage_pass else "VIOLATION (Footprint Too Large)",
        "far": actual_far,
        "max_far": limits["max_far"],
        "far_status": "PASS" if far_pass else "VIOLATION (Exceeds Density Cap)"
    }

def compute_detailed_forex_boq(d, target_country):
    gfa = d["total_gfa"]
    fx_meta = REGIONAL_FX[target_country]
    fx_rate = fx_meta["rate_to_usd"]
    currency_symbol = fx_meta["symbol"]
    regional_multiplier = fx_meta["cost_multiplier"]

    if d["material_frame"] == "Reinforced Concrete (Eurocode 2)":
        material_multiplier = 1.0
        frame_desc = "Structural Framing Concrete Matrix (C30)"
    elif d["material_frame"] == "Structural Steel Profile (Eurocode 3)":
        material_multiplier = 1.25
        frame_desc = "Structural Steel Framework Members"
    else:
        material_multiplier = 1.15
        frame_desc = "Premium Structural Engineered Timber Joists"

    combined_multiplier = regional_multiplier * material_multiplier

    conc_qty = int(gfa * 0.35)
    steel_qty = int(conc_qty * 0.12)
    brick_qty = int(gfa * 36)
    finish_qty = int(gfa)

    base_items = [
        {"Item Description": "Substructure Ground Earth Excavations", "Qty": int(gfa * 0.15), "Unit": "m³", "Rate_USD": 150},
        {"Item Description": frame_desc, "Qty": conc_qty if "Concrete" in frame_desc else int(conc_qty * 0.4), "Unit": "m³" if "Concrete" in frame_desc else "Tons", "Rate_USD": 210 if "Concrete" in frame_desc else 950},
        {"Item Description": "Tensile Structural Reinforcement & Fasteners", "Qty": steel_qty, "Unit": "Tons", "Rate_USD": 1200},
        {"Item Description": "External Perimeter Blockwork Masonry", "Qty": brick_qty, "Unit": "Pcs", "Rate_USD": 2.5},
        {"Item Description": "Internal Floor Level Finish Screed & Tiling", "Qty": finish_qty, "Unit": "m²", "Rate_USD": 40},
        {"Item Description": "Timber Internal Opening Door Fitting Units", "Qty": d["doors"], "Unit": "Sets", "Rate_USD": 300},
        {"Item Description": "Anodized Aluminum Glazed Window Assemblies", "Qty": d["windows"], "Unit": "Sets", "Rate_USD": 450}
    ]

    grand_total_usd = 0
    calculated_items = []
    for item in base_items:
        adjusted_rate_usd = item["Rate_USD"] * combined_multiplier
        cost_usd = item["Qty"] * adjusted_rate_usd
        grand_total_usd += cost_usd
        cost_local = cost_usd * fx_rate
        calculated_items.append({
            "Material Asset Item": item["Item Description"],
            "Quantity Matrix": f"{item['Qty']:,} {item['Unit']}",
            "Rate (Local Currency)": f"{currency_symbol} {int(adjusted_rate_usd * fx_rate):,}",
            "Total Local Cost": f"{currency_symbol} {int(cost_local):,}"
        })

    grand_total_local = grand_total_usd * fx_rate
    return calculated_items, grand_total_usd, grand_total_local, fx_meta

# =========================================================
# ENHANCED 2D BLUEPRINT — now uses intelligent layout
# =========================================================

def draw_2d_blueprint(design):
    layout = design["layout"]
    nx = layout["nx"]
    ny = layout["ny"]
    span = design["structural"]["span"]
    grid = layout["grid"]

    canvas_w, canvas_h = 800, 500
    padding = 60
    scale_x = (canvas_w - (padding * 2)) / (nx * span)
    scale_y = (canvas_h - (padding * 2)) / (ny * span)
    scale = min(scale_x, scale_y)

    rooms_js = ""
    for row in range(ny):
        for col in range(nx):
            cell = grid[row][col]
            if cell is None:
                continue
            room = design["rooms"][cell["room_index"]]
            rx = padding + (col * span * scale)
            ry = padding + (row * span * scale)
            rw = span * scale * 0.95
            rh = span * scale * 0.95
            color = cell["color"]
            rooms_js += f"""
            ctx.fillStyle = "{color}d0";
            ctx.fillRect({rx}, {ry}, {rw}, {rh});
            ctx.strokeStyle = "rgba(0, 229, 255, 0.3)";
            ctx.lineWidth = 1.5;
            ctx.strokeRect({rx}, {ry}, {rw}, {rh});
            ctx.fillStyle = "#ffffff";
            ctx.font = "600 11px 'Space Grotesk', sans-serif";
            ctx.fillText("{room['name']}", {rx} + 8, {ry} + 20);
            ctx.fillStyle = "rgba(255,255,255,0.6)";
            ctx.font = "10px monospace";
            ctx.fillText("{room['w']}m x {room['h']}m", {rx} + 8, {ry} + 34);
            """

    html_content = f"""
    <div style="background: radial-gradient(circle at 50% 50%, #0a1120, #02040d); padding:24px; border-radius:24px; border:1px solid rgba(0,229,255,0.15); box-shadow: 0 0 40px rgba(56,189,248,0.2);">
        <canvas id="canvas2d" width="{canvas_w}" height="{canvas_h}" style="max-width:100%; background:#040714; border-radius:12px; box-shadow: inset 0 0 30px rgba(0,0,0,0.8);"></canvas>
        <script>
            const canvas = document.getElementById('canvas2d');
            const ctx = canvas.getContext('2d');
            const nx = {nx}, ny = {ny}, span = {span}, scale = {scale}, padding = {padding};
            // Grid lines and column dots
            ctx.lineWidth = 1;
            for(let i = 0; i <= nx; i++) {{
                let x = padding + (i * span * scale);
                ctx.strokeStyle = "rgba(0, 229, 255, 0.2)";
                ctx.setLineDash([5, 10]);
                ctx.beginPath(); ctx.moveTo(x, padding-15); ctx.lineTo(x, padding + (ny*span*scale)+15); ctx.stroke();
                ctx.fillStyle = "#38bdf8"; ctx.setLineDash([]);
                ctx.fillText(String.fromCharCode(65+i), x-4, padding-25);
            }}
            for(let j = 0; j <= ny; j++) {{
                let y = padding + (j * span * scale);
                ctx.strokeStyle = "rgba(0, 229, 255, 0.2)";
                ctx.setLineDash([5, 10]);
                ctx.beginPath(); ctx.moveTo(padding-15, y); ctx.lineTo(padding + (nx*span*scale)+15, y); ctx.stroke();
                ctx.fillStyle = "#38bdf8"; ctx.setLineDash([]);
                ctx.fillText(j+1, padding-35, y+4);
            }}
            {rooms_js}
            // Column markers
            ctx.fillStyle = "#ff6b35";
            const colSize = 10;
            for(let i=0; i<=nx; i++) {{
                for(let j=0; j<=ny; j++) {{
                    let cx = padding + (i*span*scale), cy = padding + (j*span*scale);
                    ctx.fillRect(cx-colSize/2, cy-colSize/2, colSize, colSize);
                    ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 1.5;
                    ctx.strokeRect(cx-colSize/2, cy-colSize/2, colSize, colSize);
                }}
            }}
        </script>
    </div>
    """
    st.components.v1.html(html_content, height=560)

# =========================================================
# 3D ISOMETRIC VIEW — uses layout grid dimensions
# =========================================================

def draw_3d_isometric_view(design):
    nx = design["layout"]["nx"]
    ny = design["layout"]["ny"]
    span = design["structural"]["span"]
    floors = design["floors"]
    canvas_w, canvas_h = 800, 500

    html_content = f"""
    <div style="background: radial-gradient(circle at 50% 50%, #0a1120, #02040d); padding:24px; border-radius:24px; border:1px solid rgba(0,229,255,0.15); box-shadow: 0 0 40px rgba(56,189,248,0.2);">
        <canvas id="canvas3d" width="{canvas_w}" height="{canvas_h}" style="max-width:100%; background:#040714; border-radius:12px; box-shadow: inset 0 0 30px rgba(0,0,0,0.8);"></canvas>
        <script>
            const canvas = document.getElementById('canvas3d');
            const ctx = canvas.getContext('2d');
            const nx = {nx}, ny = {ny}, span = {span}, totalFloors = {floors};
            const originX = canvas.width/2, originY = canvas.height - 80;
            const isoScale = Math.min(180 / (nx*span), 180 / (ny*span));
            const floorHeightPixels = 32;
            function project(gX, gY, floorIndex) {{
                const isoX = originX + (gX - gY) * Math.cos(Math.PI/6) * isoScale;
                const isoY = originY - (gX + gY) * Math.sin(Math.PI/6) * isoScale - (floorIndex * floorHeightPixels);
                return {{x: isoX, y: isoY}};
            }}
            // Background grid
            ctx.strokeStyle = 'rgba(0, 229, 255, 0.05)';
            for(let i=0; i<canvas.width; i+=40) {{ ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i,canvas.height); ctx.stroke(); }}
            for(let j=0; j<canvas.height; j+=40) {{ ctx.beginPath(); ctx.moveTo(0,j); ctx.lineTo(canvas.width,j); ctx.stroke(); }}
            // Ground grid
            ctx.strokeStyle = "rgba(148, 163, 184, 0.2)"; ctx.lineWidth = 1; ctx.setLineDash([4,4]);
            for(let i=0; i<=nx; i++) {{ let pStart=project(i*span,0,0), pEnd=project(i*span, ny*span,0); ctx.beginPath(); ctx.moveTo(pStart.x,pStart.y); ctx.lineTo(pEnd.x,pEnd.y); ctx.stroke(); }}
            for(let j=0; j<=ny; j++) {{ let pStart=project(0,j*span,0), pEnd=project(nx*span, j*span,0); ctx.beginPath(); ctx.moveTo(pStart.x,pStart.y); ctx.lineTo(pEnd.x,pEnd.y); ctx.stroke(); }}
            ctx.setLineDash([]);
            // Floor slabs & beams
            for (let f = 1; f <= totalFloors; f++) {{
                ctx.strokeStyle = "rgba(0, 229, 255, 0.8)"; ctx.lineWidth = 2.2;
                for(let j=0; j<=ny; j++) {{ for(let i=0; i<nx; i++) {{ let p1=project(i*span, j*span, f), p2=project((i+1)*span, j*span, f); ctx.beginPath(); ctx.moveTo(p1.x,p1.y); ctx.lineTo(p2.x,p2.y); ctx.stroke(); }} }}
                for(let i=0; i<=nx; i++) {{ for(let j=0; j<ny; j++) {{ let p1=project(i*span, j*span, f), p2=project(i*span, (j+1)*span, f); ctx.beginPath(); ctx.moveTo(p1.x,p1.y); ctx.lineTo(p2.x,p2.y); ctx.stroke(); }} }}
                // Columns (orange)
                ctx.strokeStyle = "rgba(255, 107, 53, 0.9)"; ctx.lineWidth = 3.5;
                for(let i=0; i<=nx; i++) {{ for(let j=0; j<=ny; j++) {{ let basePt=project(i*span, j*span, f-1), topPt=project(i*span, j*span, f); ctx.beginPath(); ctx.moveTo(basePt.x,basePt.y); ctx.lineTo(topPt.x,topPt.y); ctx.stroke(); }} }}
                // Node dots
                ctx.fillStyle = "#ffffff";
                for(let i=0; i<=nx; i++) {{ for(let j=0; j<=ny; j++) {{ let nodePt=project(i*span, j*span, f); ctx.beginPath(); ctx.arc(nodePt.x, nodePt.y, 2, 0, 2*Math.PI); ctx.fill(); }} }}
                // Floor label
                let textPt = project(0, ny*span, f);
                ctx.fillStyle = "rgba(148, 163, 184, 0.8)"; ctx.font = "9px monospace";
                ctx.fillText("L" + f, textPt.x - 95, textPt.y + 4);
            }}
            // Legend
            ctx.fillStyle = "rgba(2, 4, 13, 0.85)"; ctx.fillRect(20,20,220,95);
            ctx.strokeStyle = "#38bdf8"; ctx.lineWidth = 1.5; ctx.strokeRect(20,20,220,95);
            ctx.font = "600 11px 'Space Grotesk', sans-serif"; ctx.fillStyle = "#e0e7ff";
            ctx.fillText("STRUCTURAL MODEL", 32, 40);
            ctx.font = "10px monospace";
            ctx.fillStyle = "#ff6b35"; ctx.fillText("■ Columns", 32, 58);
            ctx.fillStyle = "#00e5ff"; ctx.fillText("▬ Beams", 32, 74);
            ctx.fillStyle = "#94a3b8"; ctx.fillText("--- " + nx + "x" + ny + " Bays @" + span + "m", 32, 90);
        </script>
    </div>
    """
    st.components.v1.html(html_content, height=560)

# =========================================================
# SIDEBAR — GLASSMORPHIC WORKSPACE (with new load controls)
# =========================================================

st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <h1 style="color: #38bdf8; font-size: 2.2rem; margin:0;">ARC STUDIO</h1>
    <p style="color: #94a3b8; font-family: 'Space Grotesk', sans-serif; letter-spacing: 2px;">OCULUS RIFT v17.0</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

nav_workspace = st.sidebar.pills("🌐 Workspace", ["Control Hub Overview", "Generative Synthesis Lab"], default="Control Hub Overview")
st.sidebar.markdown("---")

with st.sidebar.expander("⚙️ Configuration Matrix", expanded=True):
    select_country = st.selectbox("Target Region", list(REGIONAL_FX.keys()))
    select_domain = st.selectbox("Building Category", list(ARCH_DOMAINS.keys()))
    select_type = st.selectbox("Typology", ARCH_DOMAINS[select_domain]["types"])

    st.markdown("### Structural Parameters")
    input_plot = st.slider("Plot Size (m²)", 200, 5000, 800, step=50)
    input_floors = st.slider("Storeys", 1, 12, 3)
    input_baths = st.slider("Bathrooms", 1, 10, 2)

    select_soil = st.selectbox("Soil Stratum", list(SOIL_PROFILES.keys()))

    select_material = st.pills(
        "Framing Matrix",
        ["Reinforced Concrete (Eurocode 2)", "Structural Steel Profile (Eurocode 3)", "Timber Profile (Eurocode 5)"],
        default="Reinforced Concrete (Eurocode 2)"
    )

    st.markdown("### Load Parameters")
    g_k_input = st.slider("Permanent Load (kN/m²)", 3.0, 8.0, 5.5, step=0.5,
                          help="Self‑weight + finishes + services.")
    default_q = 2.5 if select_domain == "Residential" else (4.0 if select_domain == "Commercial" else 7.5)
    q_k_input = st.slider("Imposed Load (kN/m²)", 1.5, 10.0, default_q, step=0.5,
                          help="Live load according to occupancy category.")

    if select_material == "Structural Steel Profile (Eurocode 3)":
        steel_section = st.selectbox(
            "Steel Section",
            ["UB 254x146x31", "UB 305x165x40", "UC 254x254x73", "UC 305x305x97"],
            index=3
        )
    else:
        steel_section = None

st.sidebar.markdown("---")
trigger_btn = st.sidebar.button("⚡ Execute Generative Sequence", type="primary", use_container_width=True)

# =========================================================
# CONTROL HUB OVERVIEW — GLOWING FOREX TILES
# =========================================================

if nav_workspace == "Control Hub Overview":
    st.title("🌍 Regional Structural Telemetry Dashboard")
    st.markdown("Cross-border East African indices synchronized with active design queues.")
    st.markdown("---")

    fx_1, fx_2, fx_3, fx_4 = st.columns(4)
    fx_1.metric("Forex Base USD / KES", f"KSh {REGIONAL_FX['Kenya']['rate_to_usd']:.2f}")
    fx_2.metric("Forex Base USD / UGX", f"USh {REGIONAL_FX['Uganda']['rate_to_usd']:.2f}")
    fx_3.metric("Forex Base USD / TZS", f"TSh {REGIONAL_FX['Tanzania']['rate_to_usd']:.2f}")
    fx_4.metric("Forex Base USD / SSP", f"SSP {REGIONAL_FX['South Sudan']['rate_to_usd']:.2f}")

    st.markdown("---")

    stat_c1, stat_c2 = st.columns(2)
    with stat_c1:
        st.subheader("📊 Synthesis Pipeline Memory Status")
        st.metric("Total Cached Archetypes", f"{len(st.session_state.memory['designs'])} Units")
    with stat_c2:
        st.subheader("📜 Recent Pipeline Engine Events")
        if st.session_state.memory["logs"]:
            for event in reversed(st.session_state.memory["logs"][-4:]):
                st.caption(f"⏱️ `{event['time'][-11:-3]}` — {event['msg']}")
        else:
            st.info("System logs clear. Ready for structural generation sequences.")

# =========================================================
# GENERATIVE SYNTHESIS LAB — IMMERSIVE EXPERIENCE
# =========================================================

elif nav_workspace == "Generative Synthesis Lab":
    st.title("📐 Architecture Generation & Material Synthesis Engine")
    st.markdown("Dynamic layout vectors with Eurocode compliance and regional forex integration.")
    st.markdown("---")

    if trigger_btn:
        with st.spinner("Processing architectural synthesis..."):
            model_data = generate_building_model(
                select_domain, select_type, input_floors, input_baths, select_country,
                select_material, input_plot, select_soil,
                g_k_input, q_k_input, steel_section
            )
            st.session_state.active_design = model_data
            st.session_state.memory["designs"].append(model_data)
            log_event(f"Generated regional structural array instance #{model_data['id']}")

    if st.session_state.active_design:
        design = st.session_state.active_design

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Region", design["country"])
        m2.metric("GFA", f"{design['total_gfa']:,} m²")
        m3.metric("Storeys", f"{design['floors']}")
        m4.metric("Doors / Windows", f"🚪 {design['doors']} | 🪟 {design['windows']}")

        st.markdown("<br>", unsafe_allow_html=True)

        tab_spatial_2d, tab_spatial_3d, tab_eurocode, tab_zoning, tab_financials, tab_timeline = st.tabs([
            "🗺️ 2D Blueprint", "📦 3D Isometric", "📐 Eurocode Controls",
            "🏢 Zoning Compliance", "💰 Forex BoQ", "⏳ Schedule"
        ])

        with tab_spatial_2d:
            draw_2d_blueprint(design)

        with tab_spatial_3d:
            draw_3d_isometric_view(design)

        with tab_eurocode:
            st.markdown("### 📐 Structural Capacity & Deflection Verification")
            analysis = run_eurocode_analysis(design)
            st.caption(f"Standard: **{analysis['code_ref']}**")
            st.latex(analysis["formula_latex"])

            ec_c1, ec_c2, ec_c3 = st.columns(3)
            with ec_c1:
                st.markdown("#### ULS Bending")
                st.metric("Load ($w_{Ed}$)", analysis["design_load"])
                st.metric("Moment ($M_{Ed}$)", analysis["m_ed"])
                st.metric("Resistance ($M_{Rd}$)", analysis["m_rd"])
                if "PASS" in analysis["uls_status"]:
                    st.success(analysis["uls_status"])
                else:
                    st.error(analysis["uls_status"])

            with ec_c2:
                st.markdown("#### SLS Deflection")
                st.metric("Limit ($L/250$)", analysis["deflection_limit"])
                st.metric("Deflection", analysis["calculated_deflection"])
                if "PASS" in analysis["sls_status"]:
                    st.success(analysis["sls_status"])
                else:
                    st.error(analysis["sls_status"])

            with ec_c3:
                st.markdown("#### EC7 Foundation")
                st.caption(f"Soil: `{design['soil_type']}`")
                st.metric("Bearing ($q_{Rd}$)", analysis["q_rd"])
                st.metric("Pressure ($q_{Ed}$)", analysis["applied_bearing"])
                if "PASS" in analysis["geo_status"]:
                    st.success(analysis["geo_status"])
                else:
                    st.error(analysis["geo_status"])

        with tab_zoning:
            st.markdown("### 🏢 Municipal Physical Planning Compliance")
            zoning = verify_zoning_laws(design["ground_footprint"], design["total_gfa"], design["plot_size"], design["domain"])
            zc1, zc2 = st.columns(2)
            with zc1:
                st.metric("Coverage", f"{zoning['coverage_pct']:.1f}%", f"Max {zoning['max_coverage_pct']:.1f}%")
                if "PASS" in zoning["coverage_status"]:
                    st.success(zoning["coverage_status"])
                else:
                    st.error(zoning["coverage_status"])
            with zc2:
                st.metric("FAR", f"{zoning['far']:.2f}", f"Max {zoning['max_far']:.2f}")
                if "PASS" in zoning["far_status"]:
                    st.success(zoning["far_status"])
                else:
                    st.error(zoning["far_status"])

        with tab_financials:
            st.markdown("### 📊 Multi-Currency Dynamic Bill of Quantities")
            boq_table, total_usd, total_local, current_fx = compute_detailed_forex_boq(design, design["country"])
            st.table(boq_table)
            b_usd, b_local = st.columns(2)
            b_usd.metric("Total (USD)", f"$ {int(total_usd):,}")
            b_local.metric(f"Total ({current_fx['currency']})", f"{current_fx['symbol']} {int(total_local):,}")
            st.caption(f"Rate: 1 USD = {current_fx['rate_to_usd']} {current_fx['currency']}")

            st.markdown("---")
            st.subheader("⚡ Forward Rate Hedging Sandbox")
            lock_period = st.select_slider("Lockup Period", options=["3 Months", "6 Months", "12 Months"])
            months_map = {"3 Months": 3, "6 Months": 6, "12 Months": 12}
            t_periods = months_map[lock_period]
            usd_base_yield = 0.045
            local_yield = usd_base_yield + current_fx["risk_premium"] * 2
            forward_rate_est = current_fx["rate_to_usd"] * ((1 + local_yield * (t_periods/12)) / (1 + usd_base_yield * (t_periods/12)))
            hedged_cost_local = total_usd * forward_rate_est
            variance = hedged_cost_local - total_local
            fc1, fc2, fc3 = st.columns(3)
            fc1.metric("Forward Rate", f"{forward_rate_est:.2f} {current_fx['currency']}")
            fc2.metric("Hedged Liability", f"{current_fx['symbol']} {int(hedged_cost_local):,}")
            fc3.metric("Premium vs Spot", f"{current_fx['symbol']} {int(variance):+,}", delta_color="inverse")
            st.caption(f"Risk premium: {current_fx['risk_premium']*100}%")

        with tab_timeline:
            st.markdown("### ⏳ Chronological Project Lifecycle")
            t_config_1, t_config_2 = st.columns(2)
            with t_config_1:
                base_start = st.date_input("Start Date", value=datetime(2026, 7, 6))
            with t_config_2:
                tempo_factor = st.slider("Efficiency Factor", 0.8, 1.5, 1.0, step=0.1)

            floor_scale = design["floors"]
            substructure_days = int(12 * tempo_factor)
            framing_days = int((8 * floor_scale) * tempo_factor)
            enclosure_days = int((10 * floor_scale) * tempo_factor)
            finishing_days = int(15 * tempo_factor)

            schedule_data = [
                {"Task": "Substructure & Grading", "Start": 0, "Duration": substructure_days, "Color": "#4b5563"},
                {"Task": "Core Framing Erection", "Start": substructure_days, "Duration": framing_days, "Color": "#f59e0b"},
                {"Task": "Envelope & Roofing", "Start": substructure_days + framing_days, "Duration": enclosure_days, "Color": "#10b981"},
                {"Task": "Interior Finishes", "Start": substructure_days + framing_days + enclosure_days, "Duration": finishing_days, "Color": "#3b82f6"}
            ]

            total_days = sum(item["Duration"] for item in schedule_data)
            project_start_str = base_start.strftime("%b %d, %Y")
            project_finish_str = (base_start + timedelta(days=total_days)).strftime("%b %d, %Y")

            rows_html = ""
            for item in schedule_data:
                start_dt = (base_start + timedelta(days=item["Start"])).strftime("%b %d")
                end_dt = (base_start + timedelta(days=item["Start"] + item["Duration"])).strftime("%b %d")
                start_pct = (item["Start"] / total_days) * 100 if total_days > 0 else 0
                width_pct = (item["Duration"] / total_days) * 100 if total_days > 0 else 0
                rows_html += f"""
                <div style="margin-bottom: 14px;">
                    <div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:5px;">
                        <span style="font-weight:600; color:#f8fafc;">{item['Task']}</span>
                        <span style="color:#94a3b8; font-family:'Space Grotesk',monospace; font-size:12px;">{start_dt} → {end_dt} ({item['Duration']}d)</span>
                    </div>
                    <div style="background:#0f172a; border-radius:6px; height:14px; width:100%; position:relative; border:1px solid #1e293b; overflow:hidden;">
                        <div style="position:absolute; left:{start_pct}%; width:{width_pct}%; background:{item['Color']}; height:100%; border-radius:4px; box-shadow: 0 0 10px {item['Color']}80;"></div>
                    </div>
                </div>
                """

            timeline_html = f"""
            <div style="background:rgba(2,4,13,0.9); padding:24px; border-radius:24px; border:1px solid rgba(0,229,255,0.2); backdrop-filter:blur(10px);">
                <div style="display:flex; justify-content:space-between; margin-bottom:24px; font-size:12px; color:#94a3b8; border-bottom:1px dashed #334155; padding-bottom:12px; font-family:'Space Grotesk',sans-serif;">
                    <div>📅 <strong>INITIATION:</strong> {project_start_str}</div>
                    <div>⏱️ <strong>TOTAL LIFECYCLE:</strong> {total_days} Days</div>
                    <div>🏁 <strong>COMPLETION:</strong> {project_finish_str}</div>
                </div>
                {rows_html}
            </div>
            """
            st.components.v1.html(timeline_html, height=300)

    else:
        st.info("💡 Adjust structural properties in the sidebar and execute the synthesis run.")
