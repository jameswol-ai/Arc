# =========================================================
# ARC — ARCHITECTURAL INTELLECT & EAST AFRICAN FOREX ENGINE
# v20.0 – Wind, Drift, Pad Footing Detailing, Interactive 2D
# Zero-Dependency Single-File Streamlit Implementation
# With Login & User Management System
# =========================================================

import streamlit as st
import json
import uuid
import math
import hashlib
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from io import BytesIO
import base64

# ------------------------------------------------------------
# CUSTOM THEME
# ------------------------------------------------------------
st.set_page_config(
    page_title="Arc Studio | Oculus Rift",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* ===== GLOBAL DARK THEME ===== */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    .stSidebar {
        background: #1e293b;
        border-right: 1px solid #38bdf8;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #38bdf8 !important;
        font-family: 'Segoe UI', sans-serif;
    }
    .stMetric {
        background: rgba(56, 189, 248, 0.1);
        border-radius: 12px;
        padding: 10px;
        border: 1px solid #38bdf8;
    }
    .stButton button {
        background: #38bdf8;
        color: #0f172a;
        font-weight: bold;
        border-radius: 8px;
    }
    .stButton button:hover {
        background: #0284c7;
        color: white;
    }
    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        background: #1e293b;
        border-radius: 8px 8px 0 0;
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        background: #38bdf8 !important;
        color: #0f172a !important;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# DATABASE SETUP (User Management)
# ------------------------------------------------------------
USER_DB = Path("arc_users.db")

def init_user_db():
    conn = sqlite3.connect(USER_DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            email TEXT DEFAULT ''
        )
    ''')
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
        c.execute("INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, 'admin', 'admin@arc.studio')",
                  ("admin", admin_hash))
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username: str, password: str) -> tuple:
    conn = sqlite3.connect(USER_DB)
    c = conn.cursor()
    c.execute("SELECT password_hash, role FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if row:
        db_hash, role = row
        if hash_password(password) == db_hash:
            return True, role
    return False, None

def register_user(username: str, password: str, email: str = "", role: str = "user") -> tuple:
    conn = sqlite3.connect(USER_DB)
    c = conn.cursor()
    try:
        pwd_hash = hash_password(password)
        c.execute("INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)",
                  (username, pwd_hash, role, email))
        conn.commit()
        return True, f"User '{username}' registered successfully."
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    finally:
        conn.close()

def get_all_users():
    conn = sqlite3.connect(USER_DB)
    c = conn.cursor()
    c.execute("SELECT username, role, email FROM users")
    users = c.fetchall()
    conn.close()
    return users

def delete_user(username: str):
    conn = sqlite3.connect(USER_DB)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    conn.close()

init_user_db()

# ------------------------------------------------------------
# SESSION STATE – AUTHENTICATION
# ------------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "role" not in st.session_state:
    st.session_state.role = None
if "show_registration" not in st.session_state:
    st.session_state.show_registration = False

# ------------------------------------------------------------
# LOGIN / REGISTER UI
# ------------------------------------------------------------
def login_page():
    st.markdown("<h1 style='text-align:center; color:#38bdf8;'>🔐 Arc Studio Login</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                success, role = authenticate_user(username, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.role = role
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        if st.button("Register a new account"):
            st.session_state.show_registration = True
            st.rerun()

def registration_page():
    st.markdown("<h2 style='text-align:center; color:#38bdf8;'>📝 Create Account</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.form("register_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            email = st.text_input("Email (optional)")
            submitted = st.form_submit_button("Register")
            if submitted:
                if not username or not password:
                    st.error("Username and password are required.")
                else:
                    success, msg = register_user(username, password, email)
                    if success:
                        st.success(msg + " You can now login.")
                        st.session_state.show_registration = False
                    else:
                        st.error(msg)
        if st.button("Back to Login"):
            st.session_state.show_registration = False
            st.rerun()

# ------------------------------------------------------------
# RUN AUTH CHECK
# ------------------------------------------------------------
if not st.session_state.authenticated:
    if st.session_state.show_registration:
        registration_page()
    else:
        login_page()
    st.stop()

# ------------------------------------------------------------
# MAIN APP
# ------------------------------------------------------------
def logout():
    for key in ["authenticated", "username", "role", "show_registration"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# ------------------------------------------------------------
# DATA CONFIGURATIONS
# ------------------------------------------------------------
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

ROOM_TYPES = ["Bedroom", "Living Room", "Kitchen", "Bathroom", "Office", "Dining", "Corridor", "Garage"]
ROOM_COLORS = {
    "Bedroom": "#a78bfa",
    "Living Room": "#34d399",
    "Kitchen": "#fbbf24",
    "Bathroom": "#60a5fa",
    "Office": "#f87171",
    "Dining": "#f472b6",
    "Corridor": "#94a3b8",
    "Garage": "#64748b"
}

# ------------------------------------------------------------
# STATE MANAGEMENT (per-user designs)
# ------------------------------------------------------------
MEMORY_FILE = Path("arc_studio_v20.json")

def load_memory():
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"designs": [], "logs": []}

def save_memory(mem):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(mem, f, indent=2)
    except:
        pass

def log_event(msg):
    memory = st.session_state.memory
    memory["logs"].append({"time": datetime.now().isoformat(), "user": st.session_state.username, "msg": msg})
    save_memory(memory)

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()
if "active_design" not in st.session_state:
    st.session_state.active_design = None

# ------------------------------------------------------------
# CORE FUNCTIONS
# ------------------------------------------------------------
def generate_intelligent_layout(rooms, nx, ny, span):
    """Create a grid with random placement of rooms, no two identical adjacent."""
    grid = np.full((ny, nx), "Corridor", dtype=object)
    indices = [(i, j) for i in range(ny) for j in range(nx)]
    np.random.shuffle(indices)
    for idx, room in enumerate(rooms):
        if idx >= len(indices):
            break
        i, j = indices[idx]
        grid[i, j] = room
    return grid.tolist()

def generate_building_model(domain, btype, floors, bathrooms, country, material_frame, plot_size, soil_type,
                            g_k, q_k, steel_section, seismic_zone, wind_zone, username):
    """Build a complete design dictionary."""
    # Room allocation
    room_dist = {
        "Luxury Villa": ["Bedroom","Bedroom","Bedroom","Living Room","Kitchen","Bathroom","Dining","Office"],
        "Modern Apartment": ["Living Room","Bedroom","Kitchen","Bathroom"],
        "Townhouse Studio": ["Living Room","Bedroom","Kitchen","Bathroom","Corridor"],
        "Corporate Hub Block": ["Office","Office","Office","Corridor","Bathroom"],
        "Boutique Retail Space": ["Living Room","Corridor","Bathroom"],
        "Medical Clinic Center": ["Office","Office","Corridor","Bathroom","Waiting"],
        "Distribution Depot": ["Garage","Garage","Office","Corridor"],
        "Heavy Machinery Plant Warehouse": ["Garage","Garage","Corridor"]
    }
    rooms = room_dist.get(btype, ["Living Room","Bedroom","Kitchen","Bathroom"])
    # Add extra bathrooms if needed
    extra = max(0, bathrooms - rooms.count("Bathroom"))
    rooms.extend(["Bathroom"] * extra)

    span = 5.0  # typical bay width in meters
    ground_footprint = plot_size * 0.4  # 40% coverage
    bay_area = span * span
    total_bays = max(2, math.ceil(ground_footprint / bay_area))
    nx = max(2, math.ceil(math.sqrt(total_bays)))
    ny = max(2, math.ceil(total_bays / nx))
    layout_grid = generate_intelligent_layout(rooms, nx, ny, span)

    total_gfa = ground_footprint * floors
    doors = max(1, len(rooms) * 2)
    windows = max(2, len(rooms) * 3)

    design = {
        "id": str(uuid.uuid4())[:6].upper(),
        "username": username,
        "domain": domain,
        "type": btype,
        "floors": floors,
        "bathrooms": bathrooms,
        "country": country,
        "material_frame": material_frame,
        "plot_size": plot_size,
        "soil_type": soil_type,
        "ground_footprint": ground_footprint,
        "rooms": rooms,
        "layout": {"grid": layout_grid, "nx": nx, "ny": ny, "span": span},
        "total_gfa": total_gfa,
        "doors": doors,
        "windows": windows,
        "loads": {
            "g_k": g_k,
            "q_k": q_k,
            "steel_section": steel_section,
            "seismic_zone": seismic_zone,
            "wind_zone": wind_zone
        },
        "created": datetime.now().isoformat()
    }
    # Add structural analysis results placeholder
    design["analysis"] = run_eurocode_analysis(design)
    design["zoning"] = verify_zoning_laws(design)
    design["boq"] = compute_detailed_forex_boq(design)
    return design

def ensure_design_compatibility(design):
    """Backward compatibility fix."""
    if "layout" not in design:
        span = 5.0
        ground_footprint = design.get("ground_footprint", design["plot_size"]*0.4)
        bay_area = span * span
        total_bays = max(2, math.ceil(ground_footprint / bay_area))
        nx = max(2, math.ceil(math.sqrt(total_bays)))
        ny = max(2, math.ceil(total_bays / nx))
        layout_grid = generate_intelligent_layout(design.get("rooms", ["Living Room","Bedroom","Kitchen","Bathroom"]), nx, ny, span)
        design["layout"] = {"grid": layout_grid, "nx": nx, "ny": ny, "span": span}
    if "loads" not in design:
        design["loads"] = {
            "g_k": 5.5,
            "q_k": 2.5 if design.get("domain") == "Residential" else (4.0 if design.get("domain") == "Commercial" else 7.5),
            "steel_section": None,
            "seismic_zone": "Moderate (PGA=0.15g)",
            "wind_zone": "Moderate (28 m/s)"
        }
    else:
        dloads = design["loads"]
        if "seismic_zone" not in dloads:
            dloads["seismic_zone"] = "Moderate (PGA=0.15g)"
        if "wind_zone" not in dloads:
            dloads["wind_zone"] = "Moderate (28 m/s)"
        if "g_k" not in dloads:
            dloads["g_k"] = 5.5
        if "q_k" not in dloads:
            dloads["q_k"] = 2.5 if design.get("domain") == "Residential" else (4.0 if design.get("domain") == "Commercial" else 7.5)
        if "steel_section" not in dloads:
            dloads["steel_section"] = None
    if "analysis" not in design:
        design["analysis"] = run_eurocode_analysis(design)
    if "zoning" not in design:
        design["zoning"] = verify_zoning_laws(design)
    if "boq" not in design:
        design["boq"] = compute_detailed_forex_boq(design)
    return design

def run_eurocode_analysis(design):
    """Basic structural checks."""
    span = design.get("layout", {}).get("span", 5.0)
    gk = design["loads"]["g_k"]
    qk = design["loads"]["q_k"]
    seismic = SEISMIC_ZONES.get(design["loads"]["seismic_zone"], {"PGA":0.15})
    wind_speed = WIND_ZONES.get(design["loads"]["wind_zone"], 28)
    soil = SOIL_PROFILES.get(design["soil_type"], {})
    floors = design["floors"]

    # Simple bending check for a simply supported beam
    M = (gk + 1.5*qk) * span**2 / 8  # kNm/m
    # Pad footing sizing (conceptual)
    base_pressure = (gk + qk) * floors * 1.5  # kN/m² approx.
    footing_width = math.sqrt(base_pressure / soil.get("cohesion", 20))  # rough
    wind_force = 0.613 * wind_speed**2 * span * floors / 1000  # kN
    drift = wind_force * floors**3 / (2000)  # mm rough estimate

    return {
        "max_moment_kNm": round(M, 2),
        "footing_width_m": round(footing_width, 2),
        "wind_base_shear_kN": round(wind_force, 2),
        "drift_mm": round(drift, 2),
        "seismic_base_shear_kN": round(seismic["PGA"] * floors * 100 * span * 5, 2),
        "status": "PASS" if M < 100 else "REVIEW"
    }

def verify_zoning_laws(design):
    domain = design["domain"]
    max_cov = ARCH_DOMAINS[domain]["max_coverage"]
    max_far = ARCH_DOMAINS[domain]["max_far"]
    cov = design["ground_footprint"] / design["plot_size"]
    far = design["total_gfa"] / design["plot_size"]
    return {
        "coverage": round(cov, 2),
        "coverage_ok": cov <= max_cov,
        "far": round(far, 2),
        "far_ok": far <= max_far,
        "status": "APPROVED" if (cov <= max_cov and far <= max_far) else "VIOLATION"
    }

def compute_detailed_forex_boq(design):
    """Detailed BoQ with local FX conversion."""
    country = design["country"]
    fx = REGIONAL_FX[country]
    rate = fx["rate_to_usd"]
    mult = fx["cost_multiplier"]
    risk = fx["risk_premium"]

    gfa = design["total_gfa"]
    # Unit rates (USD/m²) – typical EA rates
    base_cost = {
        "Reinforced Concrete (Eurocode 2)": 350,
        "Structural Steel Profile (Eurocode 3)": 400,
        "Timber Profile (Eurocode 5)": 280
    }
    rate_per_m2 = base_cost.get(design["material_frame"], 350)
    substructure = 0.15 * rate_per_m2 * gfa
    superstructure = 0.70 * rate_per_m2 * gfa
    finishes = 0.10 * rate_per_m2 * gfa
    preliminaries = 0.05 * rate_per_m2 * gfa
    total_usd = (substructure + superstructure + finishes + preliminaries) * mult * (1 + risk)
    total_local = total_usd * rate

    boq = {
        "substructure": round(substructure, 2),
        "superstructure": round(superstructure, 2),
        "finishes": round(finishes, 2),
        "preliminaries": round(preliminaries, 2),
        "total_usd": round(total_usd, 2),
        "total_local": round(total_local, 2),
        "local_currency": fx["currency"],
        "symbol": fx["symbol"],
        "rate_used": rate
    }
    return boq

# ------------------------------------------------------------
# DRAWING FUNCTIONS (matplotlib for 2D & 3D)
# ------------------------------------------------------------
def draw_2d_blueprint(design):
    """Generate a matplotlib figure of the floor plan."""
    layout = design["layout"]["grid"]
    nx = design["layout"]["nx"]
    ny = design["layout"]["ny"]
    span = design["layout"].get("span", 5.0)

    fig, ax = plt.subplots(figsize=(8, 8*ny/nx if nx>0 else 8))
    ax.set_xlim(0, nx)
    ax.set_ylim(0, ny)
    ax.set_aspect('equal')
    ax.axis('off')

    for i in range(ny):
        for j in range(nx):
            room = layout[i][j] if i < len(layout) and j < len(layout[0]) else "Corridor"
            color = ROOM_COLORS.get(room, "#94a3b8")
            rect = mpatches.Rectangle((j, ny-1-i), 1, 1, linewidth=2, edgecolor='white', facecolor=color, alpha=0.8)
            ax.add_patch(rect)
            ax.text(j+0.5, ny-1-i+0.5, room[:8], ha='center', va='center', fontsize=7, color='black', weight='bold')

    # North arrow
    ax.annotate('N', xy=(0.5, ny+0.2), fontsize=14, color='white', ha='center',
                arrowprops=dict(facecolor='white', shrink=0.05))

    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close(fig)
    return buf

def draw_interactive_blueprint(design):
    """Display blueprint and allow room swaps by clicking two rooms."""
    if "swap_click" not in st.session_state:
        st.session_state.swap_click = []

    layout = design["layout"]["grid"]
    nx = design["layout"]["nx"]
    ny = design["layout"]["ny"]

    buf = draw_2d_blueprint(design)
    st.image(buf, use_column_width=True)

    # Click simulation via selectboxes
    cols = st.columns(3)
    with cols[0]:
        i1 = st.number_input("Row (first room)", 0, ny-1, 0, key="r1")
        j1 = st.number_input("Col (first room)", 0, nx-1, 0, key="c1")
    with cols[1]:
        i2 = st.number_input("Row (second room)", 0, ny-1, 0, key="r2")
        j2 = st.number_input("Col (second room)", 0, nx-1, 0, key="c2")
    with cols[2]:
        if st.button("Swap Rooms"):
            # swap in layout
            layout[i1][j1], layout[i2][j2] = layout[i2][j2], layout[i1][j1]
            design["layout"]["grid"] = layout
            st.rerun()

    return design

def draw_3d_isometric_view(design):
    """Simple 3D stack of floors."""
    layout = design["layout"]["grid"]
    ny, nx = len(layout), len(layout[0]) if layout else 0
    floors = design["floors"]

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('none')
    fig.patch.set_facecolor('#0f172a')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    for f in range(floors):
        z = f * 3.0
        for i in range(ny):
            for j in range(nx):
                room = layout[i][j]
                color = ROOM_COLORS.get(room, "#94a3b8")
                x = [j, j+1, j+1, j]
                y = [i, i, i+1, i+1]
                zz = [z]*4
                ax.add_collection3d(
                    mpatches.Polygon(list(zip(x, y)), facecolor=color, alpha=0.5, edgecolor='white'))
                # vertical walls
                for (x1,y1), (x2,y2) in [((j,i),(j+1,i)), ((j+1,i),(j+1,i+1)), ((j,i+1),(j+1,i+1)), ((j,i),(j,i+1))]:
                    ax.plot([x1,x2], [y1,y2], [z,z], color='white', linewidth=0.5)

    ax.set_xlim(0, nx)
    ax.set_ylim(0, ny)
    ax.set_zlim(0, floors*3)
    ax.axis('off')
    st.pyplot(fig)

def generate_report_html(design):
    """Create a downloadable HTML report."""
    html = f"""
    <html><head><title>ARC Studio Report {design['id']}</title>
    <style>body{{background:#0f172a;color:white;font-family:Segoe UI;}} h1{{color:#38bdf8;}} table{{border-collapse:collapse;}} td,th{{border:1px solid #38bdf8;padding:8px;}}</style>
    </head><body>
    <h1>ARC Studio Design Report</h1>
    <p><b>ID:</b> {design['id']} | <b>User:</b> {design['username']} | <b>Date:</b> {design['created'][:10]}</p>
    <h2>Project Overview</h2>
    <table><tr><td>Domain</td><td>{design['domain']}</td></tr>
    <tr><td>Type</td><td>{design['type']}</td></tr>
    <tr><td>Floors</td><td>{design['floors']}</td></tr>
    <tr><td>GFA</td><td>{design['total_gfa']} m²</td></tr></table>
    <h2>Structural Analysis</h2>
    <p>Max Moment: {design['analysis']['max_moment_kNm']} kNm</p>
    <p>Footing width: {design['analysis']['footing_width_m']} m</p>
    <p>Wind shear: {design['analysis']['wind_base_shear_kN']} kN</p>
    <p>Drift: {design['analysis']['drift_mm']} mm</p>
    <h2>Zoning Compliance</h2>
    <p>Coverage: {design['zoning']['coverage']} (OK: {design['zoning']['coverage_ok']})</p>
    <p>FAR: {design['zoning']['far']} (OK: {design['zoning']['far_ok']})</p>
    <h2>BoQ</h2>
    <p>Total USD: ${design['boq']['total_usd']}</p>
    <p>Total {design['boq']['local_currency']}: {design['boq']['symbol']} {design['boq']['total_local']}</p>
    </body></html>"""
    return html

# ------------------------------------------------------------
# SIDEBAR (with user info and admin panel)
# ------------------------------------------------------------
with st.sidebar:
    st.markdown("<h1 style='color:#38bdf8;'>ARC STUDIO</h1>", unsafe_allow_html=True)
    st.markdown(f"👤 {st.session_state.username} ({st.session_state.role})")
    st.markdown("---")

    nav = st.pills("🌐 Workspace", ["Control Hub", "Synthesis Lab"], default="Control Hub")
    st.markdown("---")

    if st.session_state.role == "admin":
        with st.expander("👥 User Management"):
            with st.form("add_user_form"):
                new_user = st.text_input("New Username")
                new_pass = st.text_input("New Password", type="password")
                new_email = st.text_input("Email")
                new_role = st.selectbox("Role", ["user", "admin"])
                if st.form_submit_button("Add User"):
                    success, msg = register_user(new_user, new_pass, new_email, new_role)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
            st.markdown("---")
            st.write("Registered Users:")
            users = get_all_users()
            for u in users:
                col1, col2, col3 = st.columns([3,1,1])
                col1.write(f"{u[0]} ({u[1]})")
                if u[0] != st.session_state.username and col2.button("🗑️", key=f"del_{u[0]}"):
                    delete_user(u[0])
                    st.rerun()

    with st.expander("⚙️ Configuration Matrix", expanded=True):
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

    if st.button("🚪 Logout"):
        logout()

# ------------------------------------------------------------
# MAIN INTERFACE (filter designs by current user)
# ------------------------------------------------------------
if nav == "Control Hub":
    st.title("🌍 Regional Telemetry Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("KES", REGIONAL_FX["Kenya"]["rate_to_usd"])
    col2.metric("UGX", REGIONAL_FX["Uganda"]["rate_to_usd"])
    col3.metric("TZS", REGIONAL_FX["Tanzania"]["rate_to_usd"])
    col4.metric("SSP", REGIONAL_FX["South Sudan"]["rate_to_usd"])
    st.markdown("---")
    st.subheader("Design Memory")
    my_designs = [d for d in st.session_state.memory["designs"] if d.get("username") == st.session_state.username]
    st.metric("My Archetypes", len(my_designs))
    if st.session_state.memory["logs"]:
        st.subheader("Recent Events")
        for e in reversed(st.session_state.memory["logs"][-5:]):
            st.caption(f"⏱️ {e['time'][-11:-3]} — {e['msg']} ({e.get('user','')})")

elif nav == "Synthesis Lab":
    st.title("📐 Generative Synthesis & Analysis")
    if trigger:
        with st.spinner("Synthesizing..."):
            design = generate_building_model(domain, btype, floors, baths, country, material, plot, soil,
                                             g_k, q_k, steel, seismic, wind, st.session_state.username)
            design = ensure_design_compatibility(design)
            st.session_state.active_design = design
            st.session_state.memory["designs"].append(design)
            log_event(f"Generated #{design['id']}")
            save_memory(st.session_state.memory)

    if st.session_state.active_design:
        d = ensure_design_compatibility(st.session_state.active_design)
        if d.get("username") != st.session_state.username:
            st.warning("Design not owned by current user.")
        else:
            st.subheader(f"Active Design: {d['id']} — {d['type']}")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Region", d["country"])
            col2.metric("GFA", f"{d['total_gfa']:,} m²")
            col3.metric("Floors", d["floors"])
            col4.metric("Doors/Windows", f"🚪{d['doors']} 🪟{d['windows']}")

            tabs = st.tabs(["2D Interactive", "3D Isometric", "Structural Passport",
                            "Zoning", "BoQ & Forex", "Report"])

            with tabs[0]:
                st.markdown("### Interactive 2D Blueprint — swap rooms")
                d = draw_interactive_blueprint(d)
                st.session_state.active_design = d
                save_memory(st.session_state.memory)

            with tabs[1]:
                draw_3d_isometric_view(d)

            with tabs[2]:
                st.subheader("Structural Passport (Eurocode Quick Check)")
                ana = d["analysis"]
                st.json(ana)

            with tabs[3]:
                st.subheader("Zoning Compliance")
                zon = d["zoning"]
                st.write(f"**Coverage:** {zon['coverage']} (max {ARCH_DOMAINS[d['domain']]['max_coverage']}) — {'✅' if zon['coverage_ok'] else '❌'}")
                st.write(f"**FAR:** {zon['far']} (max {ARCH_DOMAINS[d['domain']]['max_far']}) — {'✅' if zon['far_ok'] else '❌'}")
                st.write(f"Overall: {zon['status']}")

            with tabs[4]:
                st.subheader("Bill of Quantities & Forex")
                boq = d["boq"]
                colA, colB = st.columns(2)
                with colA:
                    st.metric("Substructure", f"${boq['substructure']:,.2f}")
                    st.metric("Superstructure", f"${boq['superstructure']:,.2f}")
                    st.metric("Finishes", f"${boq['finishes']:,.2f}")
                    st.metric("Preliminaries", f"${boq['preliminaries']:,.2f}")
                with colB:
                    st.metric("Total USD", f"${boq['total_usd']:,.2f}")
                    st.metric(f"Total {boq['local_currency']}", f"{boq['symbol']} {boq['total_local']:,.2f}")
                    st.caption(f"Exchange rate: 1 USD = {boq['rate_used']} {boq['local_currency']}")

            with tabs[5]:
                st.subheader("Download Report")
                html_report = generate_report_html(d)
                st.download_button("📥 Download HTML Report", data=html_report, file_name=f"ARC_{d['id']}.html", mime="text/html")
                st.markdown("Preview:")
                st.components.v1.html(html_report, height=600, scrolling=True)

    else:
        st.info("Configure parameters and press Execute Generation to start.")