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

# ------------------------------------------------------------
# CUSTOM THEME (keep your existing CSS block)
# ------------------------------------------------------------
st.set_page_config(
    page_title="Arc Studio | Oculus Rift",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Insert your full CSS here (copy from original)
st.markdown("<style>/* your existing CSS */</style>", unsafe_allow_html=True)

# ------------------------------------------------------------
# DATABASE SETUP (User Management)
# ------------------------------------------------------------
USER_DB = Path("arc_users.db")

def init_user_db():
    """Create users table if not exists."""
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
    # Create default admin account if table is empty
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
        c.execute("INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, 'admin', 'admin@arc.studio')",
                  ("admin", admin_hash))
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username: str, password: str) -> tuple[bool, str]:
    """Returns (success, role) or (False, None)."""
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

def register_user(username: str, password: str, email: str = "", role: str = "user") -> tuple[bool, str]:
    """Returns (success, message)."""
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
    """Admin: fetch all users."""
    conn = sqlite3.connect(USER_DB)
    c = conn.cursor()
    c.execute("SELECT username, role, email FROM users")
    users = c.fetchall()
    conn.close()
    return users

def delete_user(username: str):
    """Admin: delete a user (except themselves)."""
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
# RUN AUTH CHECK (show login if not authenticated)
# ------------------------------------------------------------
if not st.session_state.authenticated:
    if st.session_state.show_registration:
        registration_page()
    else:
        login_page()
    st.stop()

# ------------------------------------------------------------
# MAIN APP (AFTER AUTHENTICATION)
# ------------------------------------------------------------
def logout():
    for key in ["authenticated", "username", "role", "show_registration"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# ------------------------------------------------------------
# DATA CONFIGURATIONS (unchanged)
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

# ------------------------------------------------------------
# STATE MANAGEMENT (now per-user designs)
# ------------------------------------------------------------
MEMORY_FILE = Path("arc_studio_v20.json")

def load_memory():
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    # Structure: {"designs": [], "logs": []}
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

# Compatibility fix as before
def ensure_design_compatibility(design):
    # ... (unchanged, keep the same function)
    # (I'm omitting the full body for brevity – it's the same as original)
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

# (Include all the other functions from original: generate_intelligent_layout, generate_building_model,
# run_eurocode_analysis, verify_zoning_laws, compute_detailed_forex_boq,
# draw_interactive_blueprint, draw_2d_blueprint_static, draw_3d_isometric_view, generate_report_html)
# I'll reference them but not rewrite here due to length – copy from original code exactly,
# only add the 'username' field to design dict.

def generate_building_model(domain, btype, floors, bathrooms, country, material_frame, plot_size, soil_type,
                            g_k, q_k, steel_section, seismic_zone, wind_zone, username):
    # Same as before, but we add a 'username' key to the design dict
    # ... existing code to create the design dict ...
    design = {
        "id": str(uuid.uuid4())[:6].upper(),
        "username": username,  # <--- associate with user
        "domain": domain,
        "type": btype,
        # ... all other fields ...
    }
    return design

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
            # Admin can add users, view, delete
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
        # Check if design belongs to current user (just in case)
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
                            "Zoning", "BoQ & Forex", "Schedule", "History & Compare"])

            with tabs[0]:
                st.markdown("### Interactive 2D Blueprint — click two rooms to swap")
                d = draw_interactive_blueprint(d)
                st.session_state.active_design = d
                save_memory(st.session_state.memory)  # update changed design in memory

            with tabs[1]:
                draw_3d_isometric_view(d)

            with tabs[2]:
                # Structural passport (unchanged)
                pass
            # ... (rest of tabs unchanged, but make sure they use d)

    else:
        st.info("Configure parameters and execute synthesis.")
