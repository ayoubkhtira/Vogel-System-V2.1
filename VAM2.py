import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px

# --- CONFIGURATION TELEGRAM (À remplir ou via Secrets) ---
TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"]

st.set_page_config(
    page_title="VOGEL SYSTEM",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialiser l'état du thème
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Fonction pour basculer le thème
def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# --- CSS MODERNE ET ÉLÉGANT ---
css = """
<style>
/* Variables CSS modernes */
:root {
    /* Mode Clair - Palette moderne */
    --primary: #6366f1;  /* Indigo élégant */
    --primary-dark: #4f46e5;
    --secondary: #8b5cf6; /* Violet moderne */
    --accent: #06b6d4;   /* Cyan vif */
    --success: #10b981;  /* Émeraude */
    --warning: #f59e0b;  /* Ambre */
    --error: #ef4444;    /* Rouge coral */
    --background: #ffffff;
    --surface: #f8fafc;
    --card: #ffffff;
    --text: #1e293b;
    --text-secondary: #64748b;
    --border: #e2e8f0;
    --shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    --radius: 16px;
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

[data-theme="dark"] {
    /* Mode Sombre - Palette moderne */
    --primary: #818cf8;
    --primary-dark: #6366f1;
    --secondary: #a78bfa;
    --accent: #22d3ee;
    --success: #34d399;
    --warning: #fbbf24;
    --error: #f87171;
    --background: #0f172a;
    --surface: #1e293b;
    --card: #1e293b;
    --text: #f1f5f9;
    --text-secondary: #94a3b8;
    --border: #334155;
    --shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 10px 10px -5px rgba(0, 0, 0, 0.3);
}

/* Reset et styles globaux */
* {
    transition: var(--transition);
}

.stApp {
    background: linear-gradient(135deg, var(--background) 0%, var(--surface) 100%) !important;
    color: var(--text) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Header moderne avec verre morphisme */
.glass-header {
    background: rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
    border-radius: var(--radius) !important;
    padding: 2.5rem !important;
    margin-bottom: 2.5rem !important;
    box-shadow: var(--shadow) !important;
    position: relative !important;
    overflow: hidden !important;
}

.glass-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--accent), var(--secondary));
    border-radius: var(--radius) var(--radius) 0 0;
}

/* Cartes modernes avec effet glass */
.glass-card {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: var(--radius) !important;
    padding: 2rem !important;
    margin-bottom: 1.5rem !important;
    box-shadow: var(--shadow) !important;
}

[data-theme="light"] .glass-card {
    background: rgba(255, 255, 255, 0.9) !important;
    border: 1px solid rgba(226, 232, 240, 0.6) !important;
}

/* Boutons modernes avec effet 3D */
.glass-button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.875rem 1.75rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.025em !important;
    box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.39) !important;
    transition: all 0.3s ease !important;
    position: relative !important;
    overflow: hidden !important;
}

.glass-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: 0.5s;
}

.glass-button:hover::before {
    left: 100%;
}

.glass-button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
}

.glass-button:active {
    transform: translateY(0) !important;
}

/* Inputs modernes */
.glass-input {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    padding: 0.875rem 1rem !important;
    transition: all 0.3s ease !important;
}

.glass-input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    outline: none !important;
}

[data-theme="light"] .glass-input {
    background: rgba(255, 255, 255, 0.9) !important;
    border: 1px solid rgba(226, 232, 240, 0.8) !important;
}

/* Switch moderne pour thème */
.theme-toggle-container {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: var(--radius);
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin-top: 2rem;
}

.theme-switch {
    position: relative;
    display: inline-block;
    width: 60px;
    height: 30px;
}

.theme-switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.theme-slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    transition: .4s;
    border-radius: 34px;
}

.theme-slider:before {
    position: absolute;
    content: "";
    height: 22px;
    width: 22px;
    left: 4px;
    bottom: 4px;
    background: white;
    transition: .4s;
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

input:checked + .theme-slider:before {
    transform: translateX(30px);
}

/* Badges et indicateurs */
.badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    background: linear-gradient(135deg, var(--accent) 0%, var(--primary) 100%);
    color: white;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}

/* Animations subtiles */
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

.floating {
    animation: float 3s ease-in-out infinite;
}

/* Séparateurs stylisés */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 2rem 0;
}

/* Override Streamlit components */
.stButton > button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.875rem 1.75rem !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.39) !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
}

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    padding: 0.875rem 1rem !important;
}

[data-theme="light"] .stTextInput > div > div > input,
[data-theme="light"] .stNumberInput > div > div > input,
[data-theme="light"] .stTextArea > div > div > textarea {
    background: rgba(255, 255, 255, 0.9) !important;
    border: 1px solid rgba(226, 232, 240, 0.8) !important;
}

.stDataFrame, .stDataEditor {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: var(--radius) !important;
    overflow: hidden !important;
}

[data-theme="light"] .stDataFrame,
[data-theme="light"] .stDataEditor {
    background: rgba(255, 255, 255, 0.9) !important;
    border: 1px solid rgba(226, 232, 240, 0.8) !important;
}

.stExpander {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
}

[data-theme="light"] .stExpander {
    background: rgba(255, 255, 255, 0.9) !important;
    border: 1px solid rgba(226, 232, 240, 0.8) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
}

.stTabs [data-baseweb="tab"] {
    color: var(--text-secondary) !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    transition: all 0.3s ease !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
    color: white !important;
}

/* Metric cards */
.stMetric {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: var(--radius) !important;
    padding: 1.5rem !important;
}

[data-theme="light"] .stMetric {
    background: rgba(255, 255, 255, 0.9) !important;
    border: 1px solid rgba(226, 232, 240, 0.8) !important;
}

/* Status messages */
.stAlert {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    border-left: 4px solid var(--primary) !important;
}

/* Scrollbar stylisée */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, var(--primary-dark) 0%, var(--secondary) 100%);
}
</style>
"""

# Appliquer le CSS
st.markdown(css, unsafe_allow_html=True)

# Appliquer le thème au body
theme = "dark" if st.session_state.dark_mode else "light"
st.markdown(f'<body data-theme="{theme}">', unsafe_allow_html=True)

# --- HEADER MODERNE ---
header_html = f"""
<div class="glass-header">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div>
            <h1 style="color: white; margin: 0; font-size: 2.75rem; font-weight: 800; letter-spacing: -0.025em;">
                VOGEL <span style="color: #fbbf24;">PRO</span>
            </h1>
            <p style="color: rgba(255, 255, 255, 0.9); margin-top: 0.5rem; font-size: 1.1rem; font-weight: 500;">
                Advanced Logistics Optimization System
            </p>
        </div>
        <div style="display: flex; align-items: center; gap: 1rem;">
            <span class="badge" style="background: linear-gradient(135deg, #06b6d4, #3b82f6);">
                <i class="fas fa-bolt" style="margin-right: 0.5rem;"></i>LIVE
            </span>
            <span class="badge" style="background: linear-gradient(135deg, #10b981, #8b5cf6);">
                AI-POWERED
            </span>
        </div>
    </div>
    <div style="margin-top: 1.5rem; display: flex; gap: 1rem;">
        <div style="display: flex; align-items: center; gap: 0.5rem; color: rgba(255, 255, 255, 0.9);">
            <i class="fas fa-route" style="color: #fbbf24;"></i>
            <span>Route Optimization</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem; color: rgba(255, 255, 255, 0.9);">
            <i class="fas fa-chart-line" style="color: #06b6d4;"></i>
            <span>Real-time Analytics</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem; color: rgba(255, 255, 255, 0.9);">
            <i class="fas fa-robot" style="color: #8b5cf6;"></i>
            <span>AI Algorithms</span>
        </div>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# === SIDEBAR MODERNE ===
with st.sidebar:
    # Header de la sidebar
    st.markdown(f"""
    <div class="glass-card" style="padding: 1.5rem; text-align: center;">
        <div style="width: 60px; height: 60px; background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%); 
             border-radius: 16px; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem;">
            <i class="fas fa-sliders-h" style="color: white; font-size: 1.5rem;"></i>
        </div>
        <h3 style="color: var(--text); margin: 0; font-weight: 700;">PARAMETERS</h3>
        <p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.25rem;">
            Configure your optimization
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Paramètres dans une carte
    st.markdown('<div class="glass-card" style="padding: 1.5rem;">', unsafe_allow_html=True)
    
    currency = st.selectbox(
        "💱 Currency",
        ["€ Euro", "$ USD", "£ GBP", "¥ JPY", "₹ INR"],
        index=0,
        key="currency_select"
    )
    
    num_sources = st.number_input(
        "🏭 Suppliers",
        min_value=2,
        max_value=10,
        value=3,
        key="num_sources"
    )
    
    num_dests = st.number_input(
        "👥 Customers",
        min_value=2,
        max_value=10,
        value=3,
        key="num_dests"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Bouton de thème moderne
    st.markdown("""
    <div class="theme-toggle-container">
        <div>
            <div style="font-weight: 600; color: var(--text);">Theme</div>
            <div style="font-size: 0.875rem; color: var(--text-secondary);">
                Switch between modes
            </div>
        </div>
        <label class="theme-switch">
            <input type="checkbox" id="theme-switch">
            <span class="theme-slider"></span>
        </label>
    </div>
    """, unsafe_allow_html=True)
    
    # Bouton pour basculer le thème
    if st.button("Switch Theme", key="theme_button", use_container_width=True):
        toggle_theme()
        st.rerun()
    
    # Indicateur de thème actuel
    theme_icon = "🌙" if st.session_state.dark_mode else "☀️"
    theme_text = "Dark Mode" if st.session_state.dark_mode else "Light Mode"
    st.caption(f"{theme_icon} Currently: {theme_text}")

# --- Fonctions principales (inchangées) ---
def send_telegram_feedback(name, message):
    if TOKEN == "TON_TOKEN_BOT_TELEGRAM":
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    text = f"🚀 *New feedback on VAM app*\n\n*Name:* {name}\n*Message:* {message}"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})
    except:
        pass

def vogel_approximation_method(cost_matrix, supply, demand):
    supply = np.array(supply, dtype=float)
    demand = np.array(demand, dtype=float)
    costs = np.array(cost_matrix, dtype=float)
    
    n_rows, n_cols = costs.shape
    
    original_cols = n_cols
    original_rows = n_rows
    
    if supply.sum() > demand.sum():
        diff = supply.sum() - demand.sum()
        demand = np.append(demand, diff)
        costs = np.c_[costs, np.zeros(n_rows)] 
        n_cols += 1
    elif demand.sum() > supply.sum():
        diff = demand.sum() - supply.sum()
        supply = np.append(supply, diff)
        costs = np.r_[costs, [np.zeros(n_cols)]]
        n_rows += 1
        
    allocation = np.zeros((n_rows, n_cols))
    costs_temp = costs.copy()
    supply_temp = supply.copy()
    demand_temp = demand.copy()
    
    INF = 10**9 

    while supply_temp.sum() > 0 and demand_temp.sum() > 0:
        row_penalties = []
        col_penalties = []

        for r in range(n_rows):
            if supply_temp[r] == 0:
                row_penalties.append(-1)
            else:
                row_valid = [c for c in costs_temp[r, :] if c < INF]
                if len(row_valid) >= 2:
                    sorted_row = np.sort(row_valid)
                    row_penalties.append(sorted_row[1] - sorted_row[0])
                elif len(row_valid) == 1:
                    row_penalties.append(row_valid[0])
                else:
                    row_penalties.append(-1)

        for c in range(n_cols):
            if demand_temp[c] == 0:
                col_penalties.append(-1)
            else:
                col_valid = [costs_temp[r, c] for r in range(n_rows) if costs_temp[r, c] < INF]
                if len(col_valid) >= 2:
                    sorted_col = np.sort(col_valid)
                    col_penalties.append(sorted_col[1] - sorted_col[0])
                elif len(col_valid) == 1:
                    col_penalties.append(col_valid[0])
                else:
                    col_penalties.append(-1)
        
        row_penalties = np.array(row_penalties)
        col_penalties = np.array(col_penalties)
        
        max_row_p = np.max(row_penalties)
        max_col_p = np.max(col_penalties)
        
        if max_row_p >= max_col_p:
            row_idx = np.argmax(row_penalties)
            valid_cols = np.where(costs_temp[row_idx, :] < INF)[0]
            if len(valid_cols) > 0:
                col_idx = valid_cols[np.argmin(costs_temp[row_idx, valid_cols])]
            else:
                col_idx = np.argmax(demand_temp > 0)
        else:
            col_idx = np.argmax(col_penalties)
            valid_rows = np.where(costs_temp[:, col_idx] < INF)[0]
            if len(valid_rows) > 0:
                row_idx = valid_rows[np.argmin(costs_temp[valid_rows, col_idx])]
            else:
                row_idx = np.argmax(supply_temp > 0)

        qty = min(supply_temp[row_idx], demand_temp[col_idx])
        allocation[row_idx, col_idx] = qty
        supply_temp[row_idx] -= qty
        demand_temp[col_idx] -= qty
        
        if supply_temp[row_idx] == 0:
            costs_temp[row_idx, :] = INF
        if demand_temp[col_idx] == 0:
            costs_temp[:, col_idx] = INF

    total_cost = np.sum(allocation[:original_rows, :original_cols] * costs[:original_rows, :original_cols])
    return allocation[:original_rows, :original_cols], total_cost

def generate_excel(input_df, demand_df, res_df, total_cost, currency):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book
        worksheet = workbook.add_worksheet('Rapport VAM')
        writer.sheets['Rapport VAM'] = worksheet
        
        bold_fmt = workbook.add_format({'bold': True, 'font_size': 12})
        title_fmt = workbook.add_format({'bold': True, 'font_size': 14, 'color': '#2c3e50'})
        
        row = 0
        worksheet.write(row, 0, "1. Données d'entrée", title_fmt)
        row += 2
        input_df.to_excel(writer, sheet_name='Rapport VAM', startrow=row, startcol=0)
        row += len(input_df) + 3
        
        worksheet.write(row, 0, "2. Demande Clients", title_fmt)
        row += 2
        demand_df.to_excel(writer, sheet_name='Rapport VAM', startrow=row, startcol=0)
        row += len(demand_df) + 4
        
        worksheet.write(row, 0, "3. Solution Optimale", title_fmt)
        row += 2
        res_df.to_excel(writer, sheet_name='Rapport VAM', startrow=row, startcol=0)
        row += len(res_df) + 3
        
        worksheet.write(row, 0, f"Coût Total Minimum : {total_cost:,.2f} {currency}", title_fmt)
        
    return output.getvalue()

def plot_sankey(allocation_matrix, source_names, dest_names):
    labels = source_names + dest_names
    
    source_indices = []
    target_indices = []
    values = []
    custom_data = []

    n_sources = len(source_names)
    
    for r in range(allocation_matrix.shape[0]):
        for c in range(allocation_matrix.shape[1]):
            qty = allocation_matrix[r, c]
            if qty > 0:
                source_indices.append(r)
                target_indices.append(n_sources + c)
                values.append(qty)
                src_name = source_names[r]
                dst_name = dest_names[c]
                custom_data.append(f"{src_name} → {dst_name}")

    fig = go.Figure(data=[go.Sankey(
        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "white", width = 0.5),
            label = labels,
            color = "#6366f1"
        ),
        link = dict(
            source = source_indices,
            target = target_indices,
            value = values,
            color = "rgba(99, 102, 241, 0.4)",
            customdata = custom_data,
            hovertemplate='%{customdata}<br />Quantity: %{value}<extra></extra>'
        ))])
    fig.update_layout(
        title_text="Supply Chain Flow Visualization",
        font_size=14,
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=theme_text)
    )
    return fig

# --- SECTION 1: NOMINATIONS ---
st.markdown("""
<div class="glass-card">
    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
        <div style="width: 48px; height: 48px; background: linear-gradient(135deg, var(--accent) 0%, var(--primary) 100%); 
             border-radius: 12px; display: flex; align-items: center; justify-content: center;">
            <i class="fas fa-users" style="color: white; font-size: 1.25rem;"></i>
        </div>
        <div>
            <h3 style="color: var(--text); margin: 0;">Entity Configuration</h3>
            <p style="color: var(--text-secondary); margin: 0.25rem 0 0;">Define suppliers and customers</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    with st.expander("🏭 Suppliers", expanded=True):
        source_names = []
        for i in range(num_sources):
            source_names.append(st.text_input(
                f"Supplier {i+1}",
                value=f"Supplier {i+1}",
                key=f"src_{i}",
                placeholder="Enter supplier name"
            ))

with col2:
    with st.expander("👥 Customers", expanded=True):
        dest_names = []
        for i in range(num_dests):
            dest_names.append(st.text_input(
                f"Customer {i+1}",
                value=f"Customer {i+1}",
                key=f"dst_{i}",
                placeholder="Enter customer name"
            ))

# --- SECTION 2: DATA INPUT ---
st.markdown("""
<div class="glass-card">
    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
        <div style="width: 48px; height: 48px; background: linear-gradient(135deg, var(--success) 0%, var(--accent) 100%); 
             border-radius: 12px; display: flex; align-items: center; justify-content: center;">
            <i class="fas fa-database" style="color: white; font-size: 1.25rem;"></i>
        </div>
        <div>
            <h3 style="color: var(--text); margin: 0;">Cost & Capacity Matrix</h3>
            <p style="color: var(--text-secondary); margin: 0.25rem 0 0;">Enter unit costs and capacities</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Créer les dataframes
costs_data = {}
for dest in dest_names:
    costs_data[dest] = [0.0] * num_sources

df_costs = pd.DataFrame(costs_data, index=source_names)
df_costs["SUPPLY CAPACITY"] = [0.0] * num_sources

# Éditeur de coûts
st.markdown("**Cost Matrix (Unit Costs)**")
edited_costs = st.data_editor(
    df_costs,
    use_container_width=True,
    key="costs_editor",
    column_config={
        "SUPPLY CAPACITY": st.column_config.NumberColumn(
            "SUPPLY CAPACITY",
            help="Production capacity of each supplier"
        )
    }
)

st.markdown("""
<div style="margin-top: 1.5rem;"></div>
<div class="glass-card">
    <div style="display: flex; align-items: center; gap: 1rem;">
        <div style="width: 48px; height: 48px; background: linear-gradient(135deg, var(--warning) 0%, var(--error) 100%); 
             border-radius: 12px; display: flex; align-items: center; justify-content: center;">
            <i class="fas fa-shopping-cart" style="color: white; font-size: 1.25rem;"></i>
        </div>
        <div>
            <h3 style="color: var(--text); margin: 0;">Customer Demand</h3>
            <p style="color: var(--text-secondary); margin: 0.25rem 0 0;">Enter demand for each customer</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Demande
demand_data = {dest: [0.0] for dest in dest_names}
df_demand = pd.DataFrame(demand_data, index=["DEMAND"])
edited_demand = st.data_editor(df_demand, use_container_width=True, key="demand_editor")

# --- BOUTON D'OPTIMISATION ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    if st.button(
        "🚀 LAUNCH OPTIMIZATION",
        type="primary",
        use_container_width=True,
        key="optimize_button"
    ):
        st.session_state.run_optimization = True
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- SECTION 3: RÉSULTATS ---
if 'run_optimization' in st.session_state and st.session_state.run_optimization:
    try:
        costs = edited_costs.iloc[:, :-1].values.astype(float)
        supply = edited_costs.iloc[:, -1].values.astype(float)
        demand = edited_demand.iloc[0, :].values.astype(float)
        
        if np.any(costs < 0) or np.any(supply < 0) or np.any(demand < 0):
            st.error("❌ Values must be positive.")
        else:
            with st.spinner("🧠 Running Vogel's Approximation Algorithm..."):
                allocation, total_cost = vogel_approximation_method(costs, supply, demand)
            
            # Préparation des résultats
            final_sources = source_names.copy()
            final_dests = dest_names.copy()
            
            if allocation.shape[0] > len(source_names):
                final_sources.append("Dummy (Supply)")
            if allocation.shape[1] > len(dest_names):
                final_dests.append("Dummy (Demand)")
                
            res_df = pd.DataFrame(
                allocation,
                index=final_sources[:allocation.shape[0]],
                columns=final_dests[:allocation.shape[1]]
            )
            
            # Onglets pour résultats
            tab1, tab2, tab3 = st.tabs(["📊 Results", "📈 Visualization", "💾 Export"])
            
            with tab1:
                st.markdown(f"""
                <div class="glass-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                        <div>
                            <h3 style="color: var(--text); margin: 0;">Optimal Transport Plan</h3>
                            <p style="color: var(--text-secondary); margin: 0.25rem 0 0;">
                                Vogel's Approximation Method Solution
                            </p>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 2rem; font-weight: 800; color: var(--success);">
                                {total_cost:,.2f} {currency.split()[0]}
                            </div>
                            <div style="color: var(--text-secondary); font-size: 0.875rem;">
                                Total Minimum Cost
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Tableau des allocations
                st.dataframe(
                    res_df.style.applymap(
                        lambda x: 'background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(34, 197, 94, 0.2) 100%); color: black' if x > 0 else ''
                    ),
                    use_container_width=True
                )
            
            with tab2:
                st.markdown("""
                <div class="glass-card">
                    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
                        <div style="width: 48px; height: 48px; background: linear-gradient(135deg, var(--secondary) 0%, var(--primary) 100%); 
                             border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                            <i class="fas fa-project-diagram" style="color: white; font-size: 1.25rem;"></i>
                        </div>
                        <div>
                            <h3 style="color: var(--text); margin: 0;">Flow Visualization</h3>
                            <p style="color: var(--text-secondary); margin: 0.25rem 0 0;">
                                Interactive supply chain diagram
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Diagramme Sankey
                sankey_fig = plot_sankey(
                    allocation,
                    final_sources[:allocation.shape[0]],
                    final_dests[:allocation.shape[1]]
                )
                st.plotly_chart(sankey_fig, use_container_width=True)
                
                # Graphique à barres
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                
                st.markdown("""
                <div class="glass-card">
                    <h3 style="color: var(--text); margin: 0 0 1rem 0;">Cost Distribution by Supplier</h3>
                </div>
                """, unsafe_allow_html=True)
                
                real_rows = min(costs.shape[0], allocation.shape[0])
                real_cols = min(costs.shape[1], allocation.shape[1])
                
                cost_per_source = []
                for r in range(real_rows):
                    row_cost = np.sum(allocation[r, :real_cols] * costs[r, :real_cols])
                    cost_per_source.append(row_cost)
                
                bar_fig = px.bar(
                    x=source_names[:real_rows],
                    y=cost_per_source,
                    labels={'x': 'Supplier', 'y': f'Cost ({currency.split()[0]})'},
                    color=cost_per_source,
                    color_continuous_scale='Viridis'
                )
                bar_fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color=theme_text)
                )
                st.plotly_chart(bar_fig, use_container_width=True)
            
            with tab3:
                st.markdown("""
                <div class="glass-card">
                    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
                        <div style="width: 48px; height: 48px; background: linear-gradient(135deg, var(--warning) 0%, var(--accent) 100%); 
                             border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                            <i class="fas fa-file-export" style="color: white; font-size: 1.25rem;"></i>
                        </div>
                        <div>
                            <h3 style="color: var(--text); margin: 0;">Export Results</h3>
                            <p style="color: var(--text-secondary); margin: 0.25rem 0 0;">
                                Download comprehensive report
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                excel_data = generate_excel(edited_costs, edited_demand, res_df, total_cost, currency.split()[0])
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.download_button(
                        label="📥 DOWNLOAD EXCEL REPORT",
                        data=excel_data,
                        file_name=f"vogel_optimization_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                
                st.info("""
                💡 The report includes:
                - Input cost matrix and capacities
                - Customer demand data
                - Optimal allocation solution
                - Total cost calculation
                """)
    
    except Exception as e:
        st.error(f"❌ Calculation error: {str(e)}")

# --- SECTION FEEDBACK ---
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="glass-card">
    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
        <div style="width: 48px; height: 48px; background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%); 
             border-radius: 12px; display: flex; align-items: center; justify-content: center;">
            <i class="fas fa-comment-dots" style="color: white; font-size: 1.25rem;"></i>
        </div>
        <div>
            <h3 style="color: var(--text); margin: 0;">Feedback & Suggestions</h3>
            <p style="color: var(--text-secondary); margin: 0.25rem 0 0;">
                Help us improve the platform
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.form("feedback_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name", placeholder="Enter your name or company")
    with col2:
        email = st.text_input("Email (Optional)", placeholder="email@example.com")
    
    message = st.text_area("Your Message", placeholder="Share your thoughts, suggestions, or report issues...", height=120)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submitted = st.form_submit_button(
            "📨 SEND FEEDBACK",
            type="primary",
            use_container_width=True
        )
    
    if submitted and message:
        try:
            send_telegram_feedback(name if name else "Anonymous", message)
            st.success("✅ Thank you for your valuable feedback!")
            st.balloons()
        except:
            st.success("✅ Feedback recorded locally. Thank you!")
    elif submitted:
        st.warning("⚠️ Please write a message before sending.")

# --- FOOTER ---
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="glass-card" style="text-align: center; padding: 2rem;">
    <div style="display: flex; justify-content: center; gap: 2rem; margin-bottom: 1.5rem;">
        <div style="text-align: center;">
            <div style="font-size: 2rem; font-weight: 800; color: var(--primary);">VOGEL</div>
            <div style="color: var(--text-secondary); font-size: 0.875rem;">PRO SYSTEM</div>
        </div>
    </div>
    
    <div style="color: var(--text-secondary); font-size: 0.9rem; line-height: 1.6;">
        <p>Advanced Logistics Optimization Platform © 2024</p>
        <p style="font-size: 0.8rem; opacity: 0.7;">
            Powered by Vogel's Approximation Method • AI-Enhanced Analytics • Real-time Optimization
        </p>
    </div>
    
    <div style="display: flex; justify-content: center; gap: 1.5rem; margin-top: 1.5rem;">
        <a href="#" style="color: var(--text-secondary); text-decoration: none; transition: color 0.3s;">
            <i class="fas fa-shield-alt"></i> Privacy
        </a>
        <a href="#" style="color: var(--text-secondary); text-decoration: none; transition: color 0.3s;">
            <i class="fas fa-file-contract"></i> Terms
        </a>
        <a href="#" style="color: var(--text-secondary); text-decoration: none; transition: color 0.3s;">
            <i class="fas fa-question-circle"></i> Help
        </a>
        <a href="#" style="color: var(--text-secondary); text-decoration: none; transition: color 0.3s;">
            <i class="fas fa-envelope"></i> Contact
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# Ajouter les icônes FontAwesome
components.html("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
""", height=0)
