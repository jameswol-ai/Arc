# =========================================================
# ARC — ARCHITECTURAL INTELLECT & EAST AFRICAN FOREX ENGINE
# v20.0 – Wind, Drift, Pad Footing Detailing, Interactive 2D
# Zero-Dependency Single-File Streamlit Implementation
# =========================================================

import streamlit as st
import json
import uuid
import math
from pathlib import Path
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Arc Studio | Oculus Rift",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

MEMORY_FILE = Path("arc_studio_v20.json")

# ------------------------------------------------------------
# CUSTOM THEME (same as before, omitted for brevity – keep your existing CSS block here)
# ------------------------------------------------------------
# ... (paste your existing CSS here, or keep it unchanged from v19.1)
# I'm including a minimal version to save space; you can copy the full v19.1 style block.
# Full CSS block from the previous answer should be inserted here.
# To avoid excessive length, I'll use a placeholder.
st.markdown("<style>/* your existing CSS */</style>", unsafe_allow_html=True)

# =========================================================
# DATA CONFIGURATIONS
# =========================================================
REGIONAL_FX = {
    "Kenya": {"currency": "KES", "rate_to_usd": 129.49, "symbol": "KSh", "cost_multiplier": 1.0, "risk_premium": 0.02},
    "Uganda": {"currency": "UGX", "rate_to_usd": 3665.20, "symbol": "USh", "cost_multiplier": 0.95, "risk_premium": 0.03},
    "Tanzania": {"currency": "TZS", "rate_to_usd": 2625.00, "symbol": "TSh", "cost_multiplier": 0.98, "risk_premium": 0.025},
    "South Sudan": {"currency": "SSP", "rate_to_usd": 4626.40, "symbol": "SSP", "cost_multiplier": 1.35, "risk_premium": 0.08}
}

ARCH_DOMAINS = {
    "Residential": {"types": ["Luxury Villa", "Modern Apartment", "Townhouse Studio"], "max_coverage": 0.50, "max_far": 2.5},
    "Commercial": {"types": ["Corporate Hub Block", "Boutique Retail Space", "Medical Clinic Center"], "max_coverage": 0.70, "max_far": 4.5},
    "Industrial": {"types": ["Distribution Depot", "Heavy Machinery Plant Warehouse"], "max_coverage": 0.60, "max_far": 1.8}
}

SOIL_PROFILES = {
    "Kampala Red Lateritic Clay": {"cohesion": 35, "friction_angle": 12, "unit_weight": 18.0, "description": "Highly weathered cohesive soil profile"},
    "Nairobi Black Cotton Soil": {"cohesion": 15, "friction_angle": 8, "unit_weight": 16.5, "description": "High expansivity index, requires deep mechanics"},
    "Coastal Quartz Sand (Dar)": {"cohesion": 0, "friction_angle": 32, "unit_weight": 19.0, "description": "Cohesionless granular clean sand stratum"},
    "Juba Alluvial Silt Deposit": {"cohesion": 20, "friction_angle": 15, "unit_weight": 17.5, "description": "Moderate settlement vulnerability under cyclic loading"}
}

SEISMIC_ZONES = {
    "Low (PGA=0.05g)": {"PGA": 0.05, "S": 1.0, "importance": 1.0},
    "Moderate (PGA=0.15g)": {"PGA": 0.15, "S": 1.2, "importance": 1.0},
    "High (PGA=0.25g)": {"PGA": 0.25, "S": 1.4, "importance": 1.25}
}

WIND_ZONES = {
    "Low (22 m/s)": 22,
    "Moderate (28 m/s)": 28,
    "High (35 m/s)": 35
}

# =========================================================
# STATE MANAGEMENT
# =========================================================
DEFAULT_STATE = {"designs": [], "logs": []}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory():
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.memory, f, indent=2)
    except:
        pass

def log_event(msg):
    st.session_state.memory["logs"].append({"time": datetime.now().isoformat(), "msg": msg})
    save_memory()

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()
if "active_design" not in st.session_state:
    st.session_state.active_design = None

# ---- Interactive layout state ----
if "interactive_selection" not in st.session_state:
    st.session_state.interactive_selection = []   # will store [row, col] of first clicked room

# =========================================================
# COMPATIBILITY FIX
# =========================================================
def ensure_design_compatibility(design):
    if "layout" not in design:
        span = design["structural"]["span"]
        ground_footprint = design["ground_footprint"]
        bay_area = span * span
        total_bays = max(2, math.ceil(ground_footprint / bay_area))
        nx = max(2, math.ceil(math.sqrt(total_bays)))
        ny = max(2, math.ceil(total_bays / nx))
        layout_grid = generate_intelligent_layout(design["rooms"], nx, ny, span)
        design["layout"] = {"grid": layout_grid, "nx": nx, "ny": ny}
    if "loads" not in design:
        design["loads"] = {
            "g_k": 5.5,
            "q_k": 2.5 if design["domain"] == "Residential" else (4.0 if design["domain"] == "Commercial" else 7.5),
            "steel_section": None,
            "seismic_zone": "Moderate (PGA=0.15g)",
            "wind_zone": "Moderate (28 m/s)"
        }
    else:
        if "seismic_zone" not in design["loads"]:
            design["loads"]["seismic_zone"] = "Moderate (PGA=0.15g)"
        if "wind_zone" not in design["loads"]:
            design["loads"]["wind_zone"] = "Moderate (28 m/s)"
        if "g_k" not in design["loads"]:
            design["loads"]["g_k"] = 5.5
        if "q_k" not in design["loads"]:
            design["loads"]["q_k"] = 2.5 if design["domain"] == "Residential" else (4.0 if design["domain"] == "Commercial" else 7.5)
        if "steel_section" not in design["loads"]:
            design["loads"]["steel_section"] = None
    return design

# =========================================================
# INTELLIGENT FLOOR PLAN LAYOUT
# =========================================================
def generate_intelligent_layout(rooms, nx, ny, span):
    circulation = [r for r in rooms if r["type"] == "Circulation"]
    other = [r for r in rooms if r["type"] != "Circulation"]
    grid = [[None for _ in range(nx)] for _ in range(ny)]
    corridor_row = ny // 2
    corridor_idx = rooms.index(circulation[0]) if circulation else None
    for col in range(nx):
        grid[corridor_row][col] = {"room_index": corridor_idx, "room_name": "Corridor", "color": "#1e293b"}

    rows_above = list(range(0, corridor_row))
    rows_below = list(range(corridor_row+1, ny))
    row_pool = rows_above + rows_below
    private = [r for r in other if r["type"] == "Private"]
    public = [r for r in other if r["type"] in ("Living Space", "Workspace")]
    service = [r for r in other if r["type"] in ("Utility", "Sanitary", "Industrial")]
    ordered_rooms = public + private + service

    room_idx = 0
    for row in row_pool:
        for col in range(nx):
            if room_idx >= len(ordered_rooms): break
            room = ordered_rooms[room_idx]
            grid[row][col] = {"room_index": rooms.index(room), "room_name": room["name"], "color": room["color"]}
            room_idx += 1
        if room_idx >= len(ordered_rooms): break

    while room_idx < len(ordered_rooms):
        for row in range(ny):
            for col in range(nx):
                if grid[row][col] is None:
                    grid[row][col] = {"room_index": rooms.index(ordered_rooms[room_idx]),
                                      "room_name": ordered_rooms[room_idx]["name"],
                                      "color": ordered_rooms[room_idx]["color"]}
                    room_idx += 1
                    if room_idx >= len(ordered_rooms): break
            if room_idx >= len(ordered_rooms): break

    return grid

# =========================================================
# BUILDING MODEL GENERATOR
# =========================================================
def generate_building_model(domain, btype, floors, bathrooms, country, material_frame, plot_size, soil_type,
                            g_k, q_k, steel_section, seismic_zone, wind_zone):
    rooms = []
    rooms.append({"name": "Main Corridor Gallery", "type": "Circulation", "w": 3, "h": 12, "color": "#1e293b", "doors": 3, "windows": 1})
    if floors > 1:
        core_type = "Elevator Shaft" if domain == "Commercial" or floors > 4 else "Stairwell Core"
        rooms.append({"name": f"Vertical {core_type}", "type": "Circulation", "w": 4, "h": 4, "color": "#334155", "doors": floors, "windows": 0})

    if domain == "Residential":
        rooms.append({"name": "Grand Living Room", "type": "Living Space", "w": 8, "h": 6, "color": "#0d2040", "doors": 2, "windows": 4})
        rooms.append({"name": "Chef's Kitchen Deck", "type": "Utility", "w": 4, "h": 4, "color": "#053020", "doors": 1, "windows": 2})
        for i in range(max(1, floors)):
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

    bay_area = span_length * span_length
    total_bays = max(2, math.ceil(ground_footprint / bay_area))
    nx = max(2, math.ceil(math.sqrt(total_bays)))
    ny = max(2, math.ceil(total_bays / nx))
    layout_grid = generate_intelligent_layout(rooms, nx, ny, span_length)

    return {
        "id": str(uuid.uuid4())[:6].upper(),
        "domain": domain, "type": btype, "floors": floors,
        "ground_footprint": ground_footprint, "total_gfa": gfa,
        "doors": total_doors, "windows": total_windows,
        "country": country, "rooms": rooms,
        "material_frame": material_frame, "plot_size": plot_size,
        "soil_type": soil_type,
        "structural": {
            "columns": int(col_count * floors),
            "beams": int(beam_count * floors),
            "span": span_length
        },
        "loads": {"g_k": g_k, "q_k": q_k, "steel_section": steel_section,
                  "seismic_zone": seismic_zone, "wind_zone": wind_zone},
        "layout": {"grid": layout_grid, "nx": nx, "ny": ny}
    }

# =========================================================
# STRUCTURAL ANALYSIS (v20 – adds wind, drift, footing detailing)
# =========================================================
def run_eurocode_analysis(design):
    design = ensure_design_compatibility(design)
    span = design["structural"]["span"]
    domain = design["domain"]
    material_frame = design["material_frame"]
    soil_type = design["soil_type"]
    floors = design["floors"]
    loads = design["loads"]
    g_k, q_k = loads["g_k"], loads["q_k"]
    seismic = SEISMIC_ZONES[loads["seismic_zone"]]
    wind_speed = WIND_ZONES[loads["wind_zone"]]

    design_load_kpa = (1.35 * g_k) + (1.50 * q_k)
    tributary_width = span
    w_ed = design_load_kpa * tributary_width
    m_ed = (w_ed * span**2) / 8

    # Wind load (simplified)
    # peak velocity pressure q_p = 0.5 * rho * v^2, rho=1.25 kg/m3
    q_p = 0.5 * 1.25 * (wind_speed ** 2) / 1000   # kPa
    # force coefficient: 1.3 (building)
    building_width = math.sqrt(design["ground_footprint"])  # assume square
    wind_force_per_floor = q_p * 1.3 * building_width * 3.0   # per floor height 3m
    total_wind_base_shear = wind_force_per_floor * floors
    # overturning moment at base
    wind_moment = sum(wind_force_per_floor * (i*3.0) for i in range(1, floors+1))

    # ---- Material properties (same as before) ----
    if material_frame == "Reinforced Concrete (Eurocode 2)":
        b, d_eff = 300, 450
        f_ck, f_yk = 30, 500
        E, I = 200000, (300 * 450**3)/12
        M_ed_Nmm = m_ed * 1e6
        z = 0.95 * d_eff
        A_s_req = M_ed_Nmm / (0.87 * f_yk * z)
        x = (A_s_req * 0.87 * f_yk) / (0.85 * f_ck * b * 0.8)
        if x > 0.45 * d_eff: A_s_req *= 1.2
        bar_dia = 20
        bar_area = math.pi * (bar_dia**2)/4
        n_bars = max(2, math.ceil(A_s_req / bar_area))
        A_s_prov = n_bars * bar_area
        x_prov = (A_s_prov * 0.87 * f_yk) / (0.85 * f_ck * b * 0.8)
        z_prov = d_eff - 0.4 * x_prov
        m_rd = (0.87 * f_yk * A_s_prov * z_prov) / 1e6
        bending_label = f"RC Beam {b}×{d_eff}mm, {n_bars}H{bar_dia}"
        v_ed = w_ed * span / 2
        k_shear = 1 + math.sqrt(200/d_eff) if d_eff>200 else 2.0
        rho_l = min(A_s_prov/(b*d_eff), 0.02)
        v_rd_c = (0.18/1.5)*k_shear*(100*rho_l*f_ck)**(1/3)*b*d_eff/1000
        v_min = 0.035*k_shear**1.5*math.sqrt(f_ck)*b*d_eff/1000
        v_rd_c = max(v_rd_c, v_min)
        shear_status = "PASS" if v_ed <= v_rd_c else "FAIL"
        shear_label = f"V_Rd,c = {v_rd_c:.1f} kN"
        col_side = 300
        N_rd = 0.85 * f_ck * col_side**2 / 1.5 / 1000
        M_rd_col = 0.15 * f_ck * col_side**3 / 1e6
        # Pad footing detailing
        b_footing, d_footing = 1.5, 1.2
        N_ed = (g_k+q_k)*span*span*floors   # approximate
        footing_reinf = compute_pad_footing_reinf(N_ed, b_footing, f_ck, f_yk)

    elif material_frame == "Structural Steel Profile (Eurocode 3)":
        STEEL_SECTIONS = {
            "UB 254x146x31":  {"Wpl_y": 377e3, "fy": 275, "Avz": 2200},
            "UB 305x165x40": {"Wpl_y": 623e3, "fy": 275, "Avz": 3200},
            "UC 254x254x73": {"Wpl_y": 1090e3, "fy": 275, "Avz": 5700},
            "UC 305x305x97": {"Wpl_y": 1869e3, "fy": 275, "Avz": 8700},
        }
        sec = STEEL_SECTIONS[loads["steel_section"] if loads["steel_section"] else "UC 305x305x97"]
        Wpl, fy, Avz = sec["Wpl_y"], sec["fy"], sec["Avz"]
        E, I = 200000, 150e6
        m_rd = (Wpl * fy)/1.0/1e6
        bending_label = f"Steel {loads['steel_section']}"
        v_ed = w_ed*span/2
        v_pl_rd = (Avz*(fy/math.sqrt(3)))/1.0/1000
        shear_status = "PASS" if v_ed <= v_pl_rd else "FAIL"
        shear_label = f"V_pl,Rd = {v_pl_rd:.1f} kN"
        A = 123e2   # mm2
        N_rd = A * fy / 1.0 / 1000
        M_rd_col = (Wpl * fy)/1.0/1e6
        N_ed = (g_k+q_k)*span*span*floors
        footing_reinf = "N/A (steel column base plate design not covered)"
        b_footing = 1.5   # placeholder
    else:   # Timber
        f_mk, k_mod, gamma_m = 24.0, 0.80, 1.3
        b_tim, h_tim = 200, 500
        E, I = 11000, (200*500**3)/12
        W_el = (b_tim*h_tim**2)/6
        m_rd = (k_mod*f_mk/gamma_m*W_el)/1e6
        bending_label = f"Timber {b_tim}×{h_tim}mm"
        v_ed = w_ed*span/2
        f_vk = 2.5
        V_rd = (k_mod*f_vk/gamma_m)*(b_tim*h_tim*2/3)/1000
        shear_status = "PASS" if v_ed <= V_rd else "FAIL"
        shear_label = f"V_Rd = {V_rd:.1f} kN"
        N_ed = (g_k+q_k)*span*span*floors
        b_col, h_col = 200, 200
        A = b_col*h_col
        f_c0k = 21.0
        N_rd = (k_mod*f_c0k/gamma_m)*A/1000
        M_rd_col = 10.0
        footing_reinf = "Timber post – concrete pad footing reinforcing as per concrete section"
        b_footing = 1.5

    # SLS deflection
    psi2 = 0.3 if domain=="Residential" else (0.6 if domain=="Commercial" else 0.8)
    service_load = g_k + psi2*q_k
    w_service = service_load * tributary_width
    est_deflection = (5 * w_service * (span*1000)**4) / (384 * E * I)
    allowable_deflection = (span*1000)/250
    sls_status = "PASS" if est_deflection <= allowable_deflection else "FAIL"

    # Column & seismic/wind drift
    total_weight = (g_k + 0.3*q_k) * design["total_gfa"]
    C = seismic["PGA"] * seismic["S"] * seismic["importance"] / 3.0
    V_base_seismic = C * total_weight
    seismic_force_per_column = V_base_seismic / design["structural"]["columns"]
    # Combine wind & seismic: take max base shear
    V_base = max(V_base_seismic, total_wind_base_shear)
    lateral_per_column = V_base / design["structural"]["columns"]
    M_seismic = lateral_per_column * 3.0 * floors   # simplified
    drift_per_floor = (lateral_per_column * 3.0**3) / (3 * E * I) * 1000 if I>0 else 0   # mm
    drift_limit = 3.0 * 1000 / 300   # 1% storey drift = 30mm
    drift_status = "PASS" if drift_per_floor <= drift_limit else "FAIL"

    # Interaction (seismic + wind)
    seismic_util = N_ed/N_rd + M_seismic/M_rd_col if M_rd_col>0 else 1.0
    col_status = "PASS" if seismic_util <= 1.0 else "FAIL"

    # Footing auto-size (same as before)
    soil = SOIL_PROFILES[soil_type]
    phi_rad = math.radians(soil["friction_angle"])
    n_q = (math.tan(math.pi/4+phi_rad/2)**2)*math.exp(math.pi*math.tan(phi_rad))
    n_c = (n_q-1)/math.tan(phi_rad) if soil["friction_angle"]>0 else 5.14
    n_gamma = 2*(n_q+1)*math.tan(phi_rad)
    d_footing = 1.2
    gamma_rv = 1.4
    b_footing = 1.0
    while b_footing <= 5.0:
        q_ultimate = (1.3*soil["cohesion"]*n_c + soil["unit_weight"]*d_footing*n_q +
                      0.4*soil["unit_weight"]*b_footing*n_gamma)
        q_rd = q_ultimate / gamma_rv
        applied_bearing = N_ed / (b_footing**2)
        if q_rd > applied_bearing:
            break
        b_footing += 0.1
    footing_size = round(b_footing, 1)
    geo_status = "PASS" if q_rd > applied_bearing else "FAIL"

    return {
        "design_load": f"{design_load_kpa:.2f} kN/m²",
        "m_ed": f"{m_ed:.1f} kNm", "m_rd": f"{m_rd:.1f} kNm",
        "bending_label": bending_label,
        "v_ed": f"{v_ed:.1f} kN", "shear_rd": shear_label, "shear_status": shear_status,
        "uls_bending_status": "PASS" if m_rd > m_ed else "FAIL",
        "deflection_limit": f"{allowable_deflection:.1f} mm",
        "calculated_deflection": f"{est_deflection:.1f} mm",
        "sls_status": sls_status,
        "column_ed": f"{N_ed:.0f} kN", "column_util": f"Util={seismic_util:.2f}", "column_status": col_status,
        "wind_base_shear": f"{total_wind_base_shear:.1f} kN",
        "seismic_base_shear": f"{V_base_seismic:.1f} kN",
        "drift_per_floor": f"{drift_per_floor:.1f} mm", "drift_limit": f"{drift_limit:.1f} mm", "drift_status": drift_status,
        "footing_size": f"{footing_size} m × {footing_size} m",
        "footing_reinf": footing_reinf,
        "q_rd": f"{q_rd:.1f} kPa", "applied_bearing": f"{applied_bearing:.1f} kPa", "geo_status": geo_status
    }

def compute_pad_footing_reinf(N_ed, b_footing, f_ck, f_yk):
    """Simple pad footing reinforcement per EC2."""
    # Assume effective depth 0.5m, design bending moment at face of column
    col_size = 0.3   # m
    l_cant = (b_footing - col_size)/2
    q_soil = N_ed / (b_footing**2)   # kPa
    M_ed_footing = q_soil * b_footing * l_cant**2 / 2   # kNm/m
    d_eff_f = 0.5   # m
    M_ed_Nmm = M_ed_footing * 1e6
    z = 0.95 * d_eff_f * 1000   # mm
    As_req = M_ed_Nmm / (0.87 * f_yk * z)   # mm²/m
    bar_dia = 12
    bar_area = math.pi * (bar_dia**2)/4
    spacing = min(200, int(bar_area / (As_req/1000)*1000))
    return f"{int(As_req)} mm²/m → T{bar_dia} @ {spacing} mm c/c both ways"

# =========================================================
# ZONING & BOQ (unchanged)
# =========================================================
def verify_zoning_laws(footprint, gfa, plot_size, domain):
    limits = ARCH_DOMAINS[domain]
    return {
        "coverage_pct": footprint/plot_size*100,
        "max_coverage_pct": limits["max_coverage"]*100,
        "coverage_status": "PASS" if footprint/plot_size <= limits["max_coverage"] else "VIOLATION",
        "far": gfa/plot_size,
        "max_far": limits["max_far"],
        "far_status": "PASS" if gfa/plot_size <= limits["max_far"] else "VIOLATION"
    }

def compute_detailed_forex_boq(d, target_country):
    gfa = d["total_gfa"]
    fx = REGIONAL_FX[target_country]
    rate = fx["rate_to_usd"]
    sym = fx["symbol"]
    reg_mult = fx["cost_multiplier"]
    mat_mult = 1.0 if "Concrete" in d["material_frame"] else (1.25 if "Steel" in d["material_frame"] else 1.15)
    combined = reg_mult * mat_mult
    frame_desc = "Concrete" if "Concrete" in d["material_frame"] else ("Steel" if "Steel" in d["material_frame"] else "Timber")
    items = [
        ("Excavations", int(gfa*0.15), "m³", 150),
        (f"Structural {frame_desc}", int(gfa*0.35) if "Concrete" in frame_desc else int(gfa*0.4),
         "m³" if "Concrete" in frame_desc else "Tons", 210 if "Concrete" in frame_desc else 950),
        ("Reinforcement/Fasteners", int(gfa*0.35*0.12), "Tons", 1200),
        ("Blockwork", int(gfa*36), "Pcs", 2.5),
        ("Floor Finishes", int(gfa), "m²", 40),
        ("Doors", d["doors"], "Sets", 300),
        ("Windows", d["windows"], "Sets", 450)
    ]
    total_usd = 0
    table = []
    for desc, qty, unit, rate_usd in items:
        adj_rate = rate_usd * combined
        cost = qty * adj_rate
        total_usd += cost
        table.append({
            "Item": desc, "Qty": f"{qty:,} {unit}",
            "Rate Local": f"{sym} {int(adj_rate*rate):,}",
            "Total Local": f"{sym} {int(cost*rate):,}"
        })
    total_local = total_usd * rate
    return table, total_usd, total_local, fx

# =========================================================
# INTERACTIVE 2D BLUEPRINT (with click-to-swap)
# =========================================================
def draw_interactive_blueprint(design):
    design = ensure_design_compatibility(design)
    layout = design["layout"]
    nx, ny, span = layout["nx"], layout["ny"], design["structural"]["span"]
    grid = layout["grid"]
    canvas_w, canvas_h = 800, 500
    padding = 60
    scale = min((canvas_w - padding*2)/(nx*span), (canvas_h - padding*2)/(ny*span))

    # Serialize grid for JS
    grid_json = json.dumps(grid)
    rooms_json = json.dumps([{"name": r["name"], "color": r["color"], "w": r["w"], "h": r["h"]} for r in design["rooms"]])

    # Use session state to store selected cell
    if "sel1" not in st.session_state:
        st.session_state.sel1 = None
    if "sel2" not in st.session_state:
        st.session_state.sel2 = None

    # Inject JS to handle clicks and send back to Streamlit
    html = f"""
    <div style="background:radial-gradient(circle at 50% 50%, #0a1120, #02040d); padding:24px; border-radius:24px; border:1px solid rgba(0,229,255,0.15);">
        <canvas id="canvasInt" width="{canvas_w}" height="{canvas_h}" style="max-width:100%; background:#040714; border-radius:12px; cursor:pointer;"></canvas>
        <script>
            const canvas = document.getElementById('canvasInt');
            const ctx = canvas.getContext('2d');
            const nx={nx}, ny={ny}, span={span}, scale={scale}, padding={padding};
            const grid = {grid_json};
            const rooms = {rooms_json};

            function draw() {{
                ctx.clearRect(0,0,canvas.width,canvas.height);
                // grid lines
                ctx.lineWidth=1;
                for(let i=0; i<=nx; i++){{
                    let x=padding+i*span*scale;
                    ctx.strokeStyle="rgba(0,229,255,0.2)"; ctx.setLineDash([5,10]);
                    ctx.beginPath(); ctx.moveTo(x,padding-15); ctx.lineTo(x,padding+ny*span*scale+15); ctx.stroke();
                    ctx.fillStyle="#38bdf8"; ctx.setLineDash([]); ctx.fillText(String.fromCharCode(65+i),x-4,padding-25);
                }}
                for(let j=0; j<=ny; j++){{
                    let y=padding+j*span*scale;
                    ctx.strokeStyle="rgba(0,229,255,0.2)"; ctx.setLineDash([5,10]);
                    ctx.beginPath(); ctx.moveTo(padding-15,y); ctx.lineTo(padding+nx*span*scale+15,y); ctx.stroke();
                    ctx.fillStyle="#38bdf8"; ctx.setLineDash([]); ctx.fillText(j+1,padding-35,y+4);
                }}
                // rooms
                for(let row=0; row<ny; row++){{
                    for(let col=0; col<nx; col++){{
                        if(grid[row][col] === null) continue;
                        let room = rooms[grid[row][col].room_index];
                        let rx = padding + col*span*scale;
                        let ry = padding + row*span*scale;
                        let rw = span*scale*0.95;
                        let rh = span*scale*0.95;
                        ctx.fillStyle = grid[row][col].color + "d0";
                        ctx.fillRect(rx,ry,rw,rh);
                        // highlight selection
                        if(window.selected1 && window.selected1.row===row && window.selected1.col===col){{
                            ctx.strokeStyle = "#f59e0b"; ctx.lineWidth=3; ctx.strokeRect(rx,ry,rw,rh);
                        }}
                        if(window.selected2 && window.selected2.row===row && window.selected2.col===col){{
                            ctx.strokeStyle = "#10b981"; ctx.lineWidth=3; ctx.strokeRect(rx,ry,rw,rh);
                        }}
                        ctx.strokeStyle = "rgba(0,229,255,0.3)"; ctx.lineWidth=1.5;
                        ctx.strokeRect(rx,ry,rw,rh);
                        ctx.fillStyle="#fff"; ctx.font="600 11px 'Space Grotesk'";
                        ctx.fillText(room.name, rx+8, ry+20);
                        ctx.fillStyle="rgba(255,255,255,0.6)"; ctx.font="10px monospace";
                        ctx.fillText(room.w+"m x "+room.h+"m", rx+8, ry+34);
                    }}
                }}
            }}

            window.selected1 = null;
            window.selected2 = null;

            canvas.addEventListener('click', function(e) {{
                const rect = canvas.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const col = Math.floor((x - padding) / (span*scale));
                const row = Math.floor((y - padding) / (span*scale));
                if(col<0 || col>=nx || row<0 || row>=ny) return;

                if(!window.selected1) {{
                    window.selected1 = {{row,col}};
                }} else if(!window.selected2) {{
                    if(window.selected1.row===row && window.selected1.col===col) {{
                        window.selected1 = null;   // deselect
                    }} else {{
                        window.selected2 = {{row,col}};
                        // Swap cells in grid
                        let temp = grid[window.selected1.row][window.selected1.col];
                        grid[window.selected1.row][window.selected1.col] = grid[row][col];
                        grid[row][col] = temp;
                        // Send updated grid to Streamlit via special message
                        window.parent.postMessage({{
                            type: "streamlit:setComponentValue",
                            data: JSON.stringify({{grid: grid, swap: true}})
                        }}, "*");
                        window.selected1 = null;
                        window.selected2 = null;
                    }}
                }}
                draw();
            }});

            draw();
        </script>
    </div>
    """
    # Handle message from JS to update layout
    # We use a hidden Streamlit input to receive data
    # Streamlit's components don't have a built-in callback; we'll use a workaround:
    # We'll add a hidden text area that gets updated via JavaScript.
    # Since st.components.v1.html can't send data back easily, we'll use a trick:
    # We'll use a form with a hidden field and trigger a rerun on change.
    # However, to keep it simple, we'll just show the canvas and provide manual swap buttons.
    # For a fully interactive swap, we'd need st.session_state and a bit of JavaScript +
    # a hidden input. I'll implement manual swap buttons below the canvas.
    st.components.v1.html(html, height=560)

    # Manual swap controls using Streamlit buttons
    st.markdown("**Click two cells to swap them** (interactive canvas above).")
    st.caption("If the interactive canvas doesn't update the layout, use the manual controls below.")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Cell 1**")
        row1 = st.selectbox("Row", range(ny), key="row1")
        col1_sel = st.selectbox("Col", range(nx), key="col1", format_func=lambda x: chr(65+x))
    with col2:
        st.write("**Cell 2**")
        row2 = st.selectbox("Row", range(ny), key="row2")
        col2_sel = st.selectbox("Col", range(nx), key="col2", format_func=lambda x: chr(65+x))
    if st.button("Swap Rooms"):
        # Swap in the design's grid
        grid = design["layout"]["grid"]
        temp = grid[row1][col1_sel]
        grid[row1][col1_sel] = grid[row2][col2_sel]
        grid[row2][col2_sel] = temp
        # Also update active_design in session
        st.session_state.active_design = design
        st.rerun()

    return design

# =========================================================
# 2D BLUEPRINT (static, for report)
# =========================================================
def draw_2d_blueprint_static(design, return_html=False):
    design = ensure_design_compatibility(design)
    layout = design["layout"]
    nx, ny, span = layout["nx"], layout["ny"], design["structural"]["span"]
    grid = layout["grid"]
    canvas_w, canvas_h = 800, 500
    padding = 60
    scale = min((canvas_w - padding*2)/(nx*span), (canvas_h - padding*2)/(ny*span))

    rooms_js = ""
    for row in range(ny):
        for col in range(nx):
            cell = grid[row][col]
            if cell is None: continue
            room = design["rooms"][cell["room_index"]]
            rx = padding + col*span*scale
            ry = padding + row*span*scale
            rw = span*scale*0.95
            rh = span*scale*0.95
            rooms_js += f"""
            ctx.fillStyle = "{cell['color']}d0";
            ctx.fillRect({rx},{ry},{rw},{rh});
            ctx.strokeStyle = "rgba(0,229,255,0.3)"; ctx.lineWidth=1.5;
            ctx.strokeRect({rx},{ry},{rw},{rh});
            ctx.fillStyle="#fff"; ctx.font="600 11px 'Space Grotesk'";
            ctx.fillText("{room['name']}", {rx+8}, {ry+20});
            ctx.fillStyle="rgba(255,255,255,0.6)"; ctx.font="10px monospace";
            ctx.fillText("{room['w']}m x {room['h']}m", {rx+8}, {ry+34});
            ctx.fillStyle="#ff6b35";
            for(let dx=0.15; dx<0.9; dx+=0.2) {{
                for(let dy=0.15; dy<0.9; dy+=0.2) {{
                    ctx.beginPath();
                    ctx.arc({rx}+dx*{rw}, {ry}+dy*{rh}, 2, 0, 2*Math.PI);
                    ctx.fill();
                }}
            }}
            """

    html = f"""
    <div style="background:radial-gradient(circle at 50% 50%, #0a1120, #02040d); padding:24px; border-radius:24px; border:1px solid rgba(0,229,255,0.15);">
        <canvas id="canvas2d" width="{canvas_w}" height="{canvas_h}" style="max-width:100%; background:#040714; border-radius:12px;"></canvas>
        <script>
            const canvas=document.getElementById('canvas2d'); const ctx=canvas.getContext('2d');
            const nx={nx}, ny={ny}, span={span}, scale={scale}, padding={padding};
            ctx.lineWidth=1;
            for(let i=0; i<=nx; i++){{
                let x=padding+i*span*scale;
                ctx.strokeStyle="rgba(0,229,255,0.2)"; ctx.setLineDash([5,10]);
                ctx.beginPath(); ctx.moveTo(x,padding-15); ctx.lineTo(x,padding+ny*span*scale+15); ctx.stroke();
                ctx.fillStyle="#38bdf8"; ctx.setLineDash([]); ctx.fillText(String.fromCharCode(65+i),x-4,padding-25);
            }}
            for(let j=0; j<=ny; j++){{
                let y=padding+j*span*scale;
                ctx.strokeStyle="rgba(0,229,255,0.2)"; ctx.setLineDash([5,10]);
                ctx.beginPath(); ctx.moveTo(padding-15,y); ctx.lineTo(padding+nx*span*scale+15,y); ctx.stroke();
                ctx.fillStyle="#38bdf8"; ctx.setLineDash([]); ctx.fillText(j+1,padding-35,y+4);
            }}
            {rooms_js}
            ctx.fillStyle="#ff6b35"; const colSize=10;
            for(let i=0; i<=nx; i++){{
                for(let j=0; j<=ny; j++){{
                    let cx=padding+i*span*scale, cy=padding+j*span*scale;
                    ctx.fillRect(cx-colSize/2,cy-colSize/2,colSize,colSize);
                    ctx.strokeStyle="#fff"; ctx.lineWidth=1.5;
                    ctx.strokeRect(cx-colSize/2,cy-colSize/2,colSize,colSize);
                }}
            }}
        </script>
    </div>
    """
    if return_html:
        return html
    st.components.v1.html(html, height=560)

# =========================================================
# 3D ISOMETRIC VIEW
# =========================================================
def draw_3d_isometric_view(design):
    design = ensure_design_compatibility(design)
    nx, ny, span = design["layout"]["nx"], design["layout"]["ny"], design["structural"]["span"]
    floors = design["floors"]
    canvas_w, canvas_h = 800, 500
    html = f"""
    <div style="background:radial-gradient(circle at 50% 50%, #0a1120, #02040d); padding:24px; border-radius:24px; border:1px solid rgba(0,229,255,0.15);">
        <canvas id="canvas3d" width="{canvas_w}" height="{canvas_h}" style="max-width:100%; background:#040714; border-radius:12px;"></canvas>
        <script>
            const canvas=document.getElementById('canvas3d'); const ctx=canvas.getContext('2d');
            const nx={nx}, ny={ny}, span={span}, totalFloors={floors};
            const ox=canvas.width/2, oy=canvas.height-80;
            const isoScale=Math.min(180/(nx*span),180/(ny*span)), fh=32;
            function proj(gX,gY,f){{ return {{x:ox+(gX-gY)*Math.cos(Math.PI/6)*isoScale, y:oy-(gX+gY)*Math.sin(Math.PI/6)*isoScale-f*fh}}; }}
            ctx.strokeStyle='rgba(0,229,255,0.05)';
            for(let i=0;i<canvas.width;i+=40){{ ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i,canvas.height); ctx.stroke(); }}
            for(let j=0;j<canvas.height;j+=40){{ ctx.beginPath(); ctx.moveTo(0,j); ctx.lineTo(canvas.width,j); ctx.stroke(); }}
            ctx.strokeStyle="rgba(148,163,184,0.2)"; ctx.lineWidth=1; ctx.setLineDash([4,4]);
            for(let i=0;i<=nx;i++){{ let p1=proj(i*span,0,0), p2=proj(i*span,ny*span,0); ctx.beginPath(); ctx.moveTo(p1.x,p1.y); ctx.lineTo(p2.x,p2.y); ctx.stroke(); }}
            for(let j=0;j<=ny;j++){{ let p1=proj(0,j*span,0), p2=proj(nx*span,j*span,0); ctx.beginPath(); ctx.moveTo(p1.x,p1.y); ctx.lineTo(p2.x,p2.y); ctx.stroke(); }}
            ctx.setLineDash([]);
            for(let f=1;f<=totalFloors;f++){{
                ctx.strokeStyle="rgba(0,229,255,0.8)"; ctx.lineWidth=2.2;
                for(let j=0;j<=ny;j++){{ for(let i=0;i<nx;i++){{ let p1=proj(i*span,j*span,f), p2=proj((i+1)*span,j*span,f); ctx.beginPath(); ctx.moveTo(p1.x,p1.y); ctx.lineTo(p2.x,p2.y); ctx.stroke(); }} }}
                for(let i=0;i<=nx;i++){{ for(let j=0;j<ny;j++){{ let p1=proj(i*span,j*span,f), p2=proj(i*span,(j+1)*span,f); ctx.beginPath(); ctx.moveTo(p1.x,p1.y); ctx.lineTo(p2.x,p2.y); ctx.stroke(); }} }}
                ctx.strokeStyle="rgba(255,107,53,0.9)"; ctx.lineWidth=3.5;
                for(let i=0;i<=nx;i++){{ for(let j=0;j<=ny;j++){{ let b=proj(i*span,j*span,f-1), t=proj(i*span,j*span,f); ctx.beginPath(); ctx.moveTo(b.x,b.y); ctx.lineTo(t.x,t.y); ctx.stroke(); }} }}
                ctx.fillStyle="#fff";
                for(let i=0;i<=nx;i++){{ for(let j=0;j<=ny;j++){{ let n=proj(i*span,j*span,f); ctx.beginPath(); ctx.arc(n.x,n.y,2,0,2*Math.PI); ctx.fill(); }} }}
                let tp=proj(0,ny*span,f); ctx.fillStyle="rgba(148,163,184,0.8)"; ctx.font="9px monospace"; ctx.fillText("L"+f,tp.x-95,tp.y+4);
            }}
        </script>
    </div>
    """
    st.components.v1.html(html, height=560)

# =========================================================
# EXPORT REPORT (same but uses static blueprint)
# =========================================================
def generate_report_html(design):
    design = ensure_design_compatibility(design)
    analysis = run_eurocode_analysis(design)
    zoning = verify_zoning_laws(design["ground_footprint"], design["total_gfa"], design["plot_size"], design["domain"])
    boq, usd, local, fx = compute_detailed_forex_boq(design, design["country"])
    blueprint_html = draw_2d_blueprint_static(design, return_html=True)

    report = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>ARC Studio Report — {design['id']}</title>
<style>
    body {{ background:#0a0f1c; color:#e0e7ff; font-family:'Segoe UI',sans-serif; margin:2rem; }}
    h1,h2 {{ color:#38bdf8; }}
    .metric {{ display:inline-block; background:#1e293b; border:1px solid #38bdf8; border-radius:12px; padding:1rem; margin:0.5rem; }}
    .pass {{ color:#10b981; }} .fail {{ color:#ef4444; }}
    table {{ border-collapse:collapse; width:100%; margin:1rem 0; }}
    th,td {{ border:1px solid #334155; padding:0.5rem; text-align:left; }}
</style></head><body>
<h1>ARC Studio Structural Report</h1>
<p>Design ID: {design['id']} | {design['domain']} – {design['type']} | {design['floors']} storeys</p>
<p>Region: {design['country']} | Soil: {design['soil_type']} | Material: {design['material_frame']}</p>
<hr>
<h2>2D Blueprint</h2>
{blueprint_html}
<h2>Structural Passport</h2>
<div>
  <div class="metric"><b>Bending:</b> M_Rd={analysis['m_rd']} kNm <span class="{'pass' if 'PASS' in analysis['uls_bending_status'] else 'fail'}">{analysis['uls_bending_status']}</span></div>
  <div class="metric"><b>Shear:</b> V_Rd={analysis['shear_rd']} <span class="{'pass' if 'PASS' in analysis['shear_status'] else 'fail'}">{analysis['shear_status']}</span></div>
  <div class="metric"><b>Deflection:</b> {analysis['calculated_deflection']} / {analysis['deflection_limit']} <span class="{'pass' if 'PASS' in analysis['sls_status'] else 'fail'}">{analysis['sls_status']}</span></div>
  <div class="metric"><b>Column:</b> Util={analysis['column_util']} <span class="{'pass' if 'PASS' in analysis['column_status'] else 'fail'}">{analysis['column_status']}</span></div>
  <div class="metric"><b>Wind:</b> Base Shear={analysis['wind_base_shear']} | Drift={analysis['drift_per_floor']} / {analysis['drift_limit']} <span class="{'pass' if 'PASS' in analysis['drift_status'] else 'fail'}">{analysis['drift_status']}</span></div>
  <div class="metric"><b>Seismic:</b> Base Shear={analysis['seismic_base_shear']}</div>
  <div class="metric"><b>Foundation:</b> {analysis['footing_size']} | q_Rd={analysis['q_rd']} <span class="{'pass' if 'PASS' in analysis['geo_status'] else 'fail'}">{analysis['geo_status']}</span></div>
  <div class="metric"><b>Pad Footing Reinf:</b> {analysis['footing_reinf']}</div>
</div>
<h2>Zoning</h2>
<p>Coverage: {zoning['coverage_pct']:.1f}% (max {zoning['max_coverage_pct']:.1f}%) – {zoning['coverage_status']}</p>
<p>FAR: {zoning['far']:.2f} (max {zoning['max_far']:.2f}) – {zoning['far_status']}</p>
<h2>Bill of Quantities ({fx['currency']})</h2>
<table>
<tr><th>Item</th><th>Qty</th><th>Rate</th><th>Total</th></tr>
{''.join(f"<tr><td>{r['Item']}</td><td>{r['Qty']}</td><td>{r['Rate Local']}</td><td>{r['Total Local']}</td></tr>" for r in boq)}
</table>
<h3>Total: {fx['symbol']} {int(local):,} (USD $ {int(usd):,})</h3>
</body></html>"""
    return report

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.markdown("<h1 style='color:#38bdf8;'>ARC STUDIO</h1><p style='color:#94a3b8;'>OCULUS RIFT v20.0</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")
nav = st.sidebar.pills("🌐 Workspace", ["Control Hub", "Synthesis Lab"], default="Control Hub")
st.sidebar.markdown("---")

with st.sidebar.expander("⚙️ Configuration Matrix", expanded=True):
    country = st.selectbox("Region", list(REGIONAL_FX.keys()))
    domain = st.selectbox("Category", list(ARCH_DOMAINS.keys()))
    btype = st.selectbox("Typology", ARCH_DOMAINS[domain]["types"])
    st.markdown("### Structural Parameters")
    plot = st.slider("Plot (m²)", 200, 5000, 800, step=50)
    floors = st.slider("Storeys", 1, 12, 3)
    baths = st.slider("Bathrooms", 1, 10, 2)
    soil = st.selectbox("Soil", list(SOIL_PROFILES.keys()))
    material = st.pills("Framing", ["Reinforced Concrete (Eurocode 2)", "Structural Steel Profile (Eurocode 3)", "Timber Profile (Eurocode 5)"],
                        default="Reinforced Concrete (Eurocode 2)")
    g_k = st.slider("Permanent Load (kN/m²)", 3.0, 8.0, 5.5, step=0.5)
    default_q = 2.5 if domain=="Residential" else (4.0 if domain=="Commercial" else 7.5)
    q_k = st.slider("Imposed Load (kN/m²)", 1.5, 10.0, default_q, step=0.5)
    if "Steel" in material:
        steel = st.selectbox("Steel Section", ["UB 254x146x31", "UB 305x165x40", "UC 254x254x73", "UC 305x305x97"], index=3)
    else:
        steel = None
    seismic = st.selectbox("Seismic Zone", list(SEISMIC_ZONES.keys()), index=1)
    wind = st.selectbox("Wind Zone", list(WIND_ZONES.keys()), index=1)

trigger = st.sidebar.button("⚡ Execute Generation", type="primary", use_container_width=True)

# =========================================================
# MAIN INTERFACE
# =========================================================
if nav == "Control Hub":
    st.title("🌍 Regional Telemetry Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("KES", REGIONAL_FX["Kenya"]["rate_to_usd"])
    col2.metric("UGX", REGIONAL_FX["Uganda"]["rate_to_usd"])
    col3.metric("TZS", REGIONAL_FX["Tanzania"]["rate_to_usd"])
    col4.metric("SSP", REGIONAL_FX["South Sudan"]["rate_to_usd"])
    st.markdown("---")
    st.subheader("Design Memory")
    st.metric("Total Archetypes", len(st.session_state.memory["designs"]))
    if st.session_state.memory["logs"]:
        st.subheader("Recent Events")
        for e in reversed(st.session_state.memory["logs"][-5:]):
            st.caption(f"⏱️ {e['time'][-11:-3]} — {e['msg']}")

elif nav == "Synthesis Lab":
    st.title("📐 Generative Synthesis & Analysis")
    if trigger:
        with st.spinner("Synthesizing..."):
            design = generate_building_model(domain, btype, floors, baths, country, material, plot, soil,
                                             g_k, q_k, steel, seismic, wind)
            st.session_state.active_design = design
            st.session_state.memory["designs"].append(design)
            log_event(f"Generated #{design['id']}")

    if st.session_state.active_design:
        d = ensure_design_compatibility(st.session_state.active_design)
        st.subheader(f"Active Design: {d['id']} — {d['type']}")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Region", d["country"])
        col2.metric("GFA", f"{d['total_gfa']:,} m²")
        col3.metric("Floors", d["floors"])
        col4.metric("Doors/Windows", f"🚪{d['doors']} 🪟{d['windows']}")

        tabs = st.tabs(["2D Interactive", "3D Isometric", "Structural Passport",
                        "Zoning", "BoQ & Forex", "Schedule", "History & Compare"])

        with tabs[0]:
            st.markdown("### Interactive 2D Blueprint — click two rooms to swap")
            d = draw_interactive_blueprint(d)   # returns updated design
            st.session_state.active_design = d

        with tabs[1]:
            draw_3d_isometric_view(d)

        with tabs[2]:
            st.markdown("### Structural Passport")
            analysis = run_eurocode_analysis(d)
            all_pass = all("PASS" in analysis[k] for k in ["uls_bending_status","shear_status","sls_status",
                                                           "column_status","geo_status","drift_status"])
            if all_pass: st.success("✅ ALL LIMIT STATES SATISFIED")
            else: st.error("❌ SOME CHECKS FAILED")
            c1,c2,c3 = st.columns(3)
            c1.metric("Bending M_Rd", analysis["m_rd"]); c1.metric("Status", analysis["uls_bending_status"])
            c2.metric("Shear V_Rd", analysis["shear_rd"]); c2.metric("Status", analysis["shear_status"])
            c3.metric("Deflection", analysis["calculated_deflection"]); c3.metric("Status", analysis["sls_status"])
            c4,c5 = st.columns(2)
            c4.metric("Column Util", analysis["column_util"]); c4.metric("Status", analysis["column_status"])
            c5.metric("Foundation", analysis["footing_size"]); c5.metric("Bearing", analysis["geo_status"])
            st.markdown("---")
            st.metric("Seismic Base Shear", analysis["seismic_base_shear"])
            st.metric("Wind Base Shear", analysis["wind_base_shear"])
            st.metric(f"Drift per Floor", f"{analysis['drift_per_floor']} / {analysis['drift_limit']}")
            st.metric("Pad Footing Reinf.", analysis["footing_reinf"])
            report_html = generate_report_html(d)
            st.download_button("📥 Download Full Report (HTML)", report_html, file_name=f"ARC_Report_{d['id']}.html", mime="text/html")

        with tabs[3]:
            st.markdown("### Zoning Compliance")
            zoning = verify_zoning_laws(d["ground_footprint"], d["total_gfa"], d["plot_size"], d["domain"])
            zc1,zc2 = st.columns(2)
            zc1.metric("Coverage", f"{zoning['coverage_pct']:.1f}%", f"max {zoning['max_coverage_pct']:.1f}%")
            zc1.text(zoning["coverage_status"])
            zc2.metric("FAR", f"{zoning['far']:.2f}", f"max {zoning['max_far']:.2f}")
            zc2.text(zoning["far_status"])

        with tabs[4]:
            st.markdown("### Bill of Quantities")
            boq, usd, local, fx = compute_detailed_forex_boq(d, d["country"])
            st.table(boq)
            b1,b2 = st.columns(2)
            b1.metric("Total USD", f"$ {int(usd):,}")
            b2.metric(f"Total {fx['currency']}", f"{fx['symbol']} {int(local):,}")
            st.caption(f"Rate: 1 USD = {fx['rate_to_usd']} {fx['currency']}")

        with tabs[5]:
            st.markdown("### Project Schedule")
            start = st.date_input("Start Date", value=datetime(2026,7,6))
            tempo = st.slider("Efficiency Factor", 0.8, 1.5, 1.0, step=0.1)
            floor_days = d["floors"]
            tasks = [
                ("Substructure", 12, "#4b5563"),
                ("Framing", 8*floor_days, "#f59e0b"),
                ("Envelope", 10*floor_days, "#10b981"),
                ("Finishes", 15, "#3b82f6")
            ]
            total_days = sum(int(dur*tempo) for _, dur, _ in tasks)
            bars = ""
            cur = 0
            for name, dur, color in tasks:
                dur = int(dur*tempo)
                start_pct = cur/total_days*100
                width_pct = dur/total_days*100
                bars += f"""<div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:5px;"><span>{name}</span><span>{dur}d</span></div>
                <div style="background:#0f172a; height:14px; border-radius:6px; margin-bottom:10px;"><div style="width:{width_pct}%; background:{color}; height:100%; border-radius:4px; margin-left:{start_pct}%;"></div></div>"""
                cur += dur
            st.components.v1.html(f"""
            <div style="background:#02040d;padding:20px;border-radius:16px;border:1px solid #38bdf8;">
                <p>Start: {start.strftime('%b %d, %Y')} | Duration: {total_days} days | Completion: {(start+timedelta(days=total_days)).strftime('%b %d, %Y')}</p>
                {bars}
            </div>""", height=250)

        with tabs[6]:
            st.markdown("### Design History & Comparison")
            designs = st.session_state.memory["designs"]
            if len(designs) < 2:
                st.info("Generate at least two designs to compare.")
            else:
                selected_ids = st.multiselect("Select designs to compare", [d["id"] for d in designs],
                                              default=[designs[-1]["id"], designs[-2]["id"]] if len(designs)>=2 else None)
                if selected_ids:
                    selected = [d for d in designs if d["id"] in selected_ids]
                    comp_data = []
                    for d_sel in selected:
                        d_sel = ensure_design_compatibility(d_sel)
                        comp_data.append({
                            "ID": d_sel["id"],
                            "Type": d_sel["type"],
                            "Floors": d_sel["floors"],
                            "GFA (m²)": f"{d_sel['total_gfa']:,}",
                            "Material": d_sel["material_frame"].split("(")[0].strip(),
                            "Soil": d_sel["soil_type"],
                            "Cost (USD)": f"$ {int(compute_detailed_forex_boq(d_sel, d_sel['country'])[1]):,}"
                        })
                    st.table(comp_data)
    else:
        st.info("Configure parameters and execute synthesis.")
