import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px

# --- CONFIGURATION TELEGRAM ---
TOKEN = st.secrets.get("TELEGRAM_TOKEN", "")
CHAT_ID = st.secrets.get("TELEGRAM_CHAT_ID", "")

st.set_page_config(
    page_title="VOGEL SYSTEM",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS MODERNE ET ÉLÉGANT ---
st.markdown("""
<style>
/* Variables globales */
:root {
    --primary: #3B82F6;
    --primary-dark: #2563EB;
    --secondary: #8B5CF6;
    --accent: #06B6D4;
    --success: #10B981;
    --warning: #F59E0B;
    --error: #EF4444;
    --background: #FFFFFF;
    --surface: #F8FAFC;
    --text: #1F2937;
    --text-secondary: #6B7280;
    --border: #E5E7EB;
    --radius: 12px;
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* Style général */
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    background-attachment: fixed !important;
}

.main-container {
    background: rgba(255, 255, 255, 0.95) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 20px !important;
    padding: 20px !important;
    margin: 20px !important;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1) !important;
}

/* Header */
.glass-header {
    background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%) !important;
    color: white !important;
    border-radius: 16px !important;
    padding: 2.5rem !important;
    margin-bottom: 2rem !important;
    box-shadow: 0 10px 40px rgba(59, 130, 246, 0.3) !important;
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
    background: linear-gradient(90deg, #06B6D4, #8B5CF6);
}

/* Cartes */
.glass-card {
    background: white !important;
    border-radius: var(--radius) !important;
    padding: 1.5rem !important;
    margin-bottom: 1rem !important;
    border: 1px solid var(--border) !important;
    box-shadow: var(--shadow) !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease !important;
}

.glass-card:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1) !important;
}

/* Boutons */
.stButton > button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3) !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    border-radius: 10px !important;
    border: 2px solid var(--border) !important;
    padding: 0.75rem !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
}

/* Tableaux */
.stDataFrame, .stDataEditor {
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    border: 1px solid var(--border) !important;
}

/* Onglets */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px !important;
    background-color: var(--surface) !important;
    border-radius: 12px !important;
    padding: 8px !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
    color: white !important;
}

/* Métriques */
.stMetric {
    background: white !important;
    border-radius: var(--radius) !important;
    padding: 1rem !important;
    border: 1px solid var(--border) !important;
}

/* Expanders */
.stExpander {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
}

/* Sidebar */
.css-1d391kg {
    background: white !important;
}

section[data-testid="stSidebar"] > div {
    background: white !important;
    padding: 20px !important;
}

/* Alerts */
.stAlert {
    border-radius: var(--radius) !important;
    border-left: 4px solid var(--primary) !important;
}

/* Séparateurs */
hr {
    margin: 2rem 0 !important;
    border: none !important;
    border-top: 1px solid var(--border) !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--surface);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: var(--primary);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--primary-dark);
}
</style>
""", unsafe_allow_html=True)

# --- HEADER SIMPLIFIÉ ---
st.markdown("""
<div class="glass-header">
    <div style="text-align: center;">
        <h1 style="color: white; margin: 0; font-size: 2.5rem; font-weight: 800;">
            VOGEL <span style="color: #FBBF24;">PRO</span>
        </h1>
    </div>
</div>
""", unsafe_allow_html=True)

# === SIDEBAR SIMPLIFIÉ ===
with st.sidebar:
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 1.5rem;">
        <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%); 
             border-radius: 12px; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem;">
            <i class="fas fa-sliders-h" style="color: white; font-size: 1.5rem;"></i>
        </div>
        <h3 style="color: #1F2937; margin: 0; font-weight: 700;">PARAMETERS</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Paramètres
    st.markdown('<div class="glass-card" style="padding: 1.5rem;">', unsafe_allow_html=True)
    currency = st.selectbox("💱 Currency", ["€ Euro", "$ USD", "£ GBP", "¥ JPY", "₹ INR"])
    num_sources = st.number_input("🏭 Suppliers", min_value=2, max_value=10, value=3)
    num_dests = st.number_input("👥 Customers", min_value=2, max_value=10, value=3)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Fonctions principales ---
def send_telegram_feedback(name, message):
    if not TOKEN or TOKEN == "TON_TOKEN_BOT_TELEGRAM":
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
        worksheet.write(row, 0, "1. Input Data", title_fmt)
        row += 2
        input_df.to_excel(writer, sheet_name='Rapport VAM', startrow=row, startcol=0)
        row += len(input_df) + 3
        
        worksheet.write(row, 0, "2. Customer Demand", title_fmt)
        row += 2
        demand_df.to_excel(writer, sheet_name='Rapport VAM', startrow=row, startcol=0)
        row += len(demand_df) + 4
        
        worksheet.write(row, 0, "3. Optimal Solution", title_fmt)
        row += 2
        res_df.to_excel(writer, sheet_name='Rapport VAM', startrow=row, startcol=0)
        row += len(res_df) + 3
        
        worksheet.write(row, 0, f"Total Minimum Cost: {total_cost:,.2f} {currency}", title_fmt)
        
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
                custom_data.append(f"{source_names[r]} → {dest_names[c]}")
    
    fig = go.Figure(data=[go.Sankey(
        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "white", width = 0.5),
            label = labels,
            color = "#3B82F6"
        ),
        link = dict(
            source = source_indices,
            target = target_indices,
            value = values,
            color = "rgba(59, 130, 246, 0.4)",
            customdata = custom_data,
            hovertemplate='%{customdata}<br />Quantity: %{value}<extra></extra>'
        ))])
    fig.update_layout(
        title_text="Supply Chain Flow",
        font_size=14,
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# --- SECTION 1: CONFIGURATION ---
st.markdown("""
<div class="glass-card">
    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
        <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%); 
             border-radius: 12px; display: flex; align-items: center; justify-content: center;">
            <i class="fas fa-users" style="color: white; font-size: 1.25rem;"></i>
        </div>
        <div>
            <h3 style="color: #1F2937; margin: 0;">Entity Configuration</h3>
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
                key=f"src_{i}"
            ))

with col2:
    with st.expander("👥 Customers", expanded=True):
        dest_names = []
        for i in range(num_dests):
            dest_names.append(st.text_input(
                f"Customer {i+1}",
                value=f"Customer {i+1}",
                key=f"dst_{i}"
            ))

# --- SECTION 2: DATA INPUT ---
st.markdown("""
<div class="glass-card">
    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
        <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #10B981 0%, #06B6D4 100%); 
             border-radius: 12px; display: flex; align-items: center; justify-content: center;">
            <i class="fas fa-database" style="color: white; font-size: 1.25rem;"></i>
        </div>
        <div>
            <h3 style="color: #1F2937; margin: 0;">Cost & Capacity Matrix</h3>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Cost matrix
costs_data = {}
for dest in dest_names:
    costs_data[dest] = [0.0] * num_sources

df_costs = pd.DataFrame(costs_data, index=source_names)
df_costs["SUPPLY CAPACITY"] = [0.0] * num_sources

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

# Demand
st.markdown("""
<div class="glass-card">
    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
        <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #F59E0B 0%, #EF4444 100%); 
             border-radius: 12px; display: flex; align-items: center; justify-content: center;">
            <i class="fas fa-shopping-cart" style="color: white; font-size: 1.25rem;"></i>
        </div>
        <div>
            <h3 style="color: #1F2937; margin: 0;">Customer Demand</h3>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

demand_data = {dest: [0.0] for dest in dest_names}
df_demand = pd.DataFrame(demand_data, index=["DEMAND"])
edited_demand = st.data_editor(df_demand, use_container_width=True, key="demand_editor")

# --- OPTIMIZATION BUTTON ---
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button(
        "🚀 LAUNCH OPTIMIZATION",
        type="primary",
        use_container_width=True,
        key="optimize_button"
    ):
        st.session_state.run_optimization = True

# --- SECTION 3: RESULTS ---
if 'run_optimization' in st.session_state and st.session_state.run_optimization:
    try:
        costs = edited_costs.iloc[:, :-1].values.astype(float)
        supply = edited_costs.iloc[:, -1].values.astype(float)
        demand = edited_demand.iloc[0, :].values.astype(float)
        
        if np.any(costs < 0) or np.any(supply < 0) or np.any(demand < 0):
            st.error("❌ Values must be positive.")
        else:
            with st.spinner("🧠 Running optimization algorithm..."):
                allocation, total_cost = vogel_approximation_method(costs, supply, demand)
            
            # Prepare results
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
            
            # Tabs for results
            tab1, tab2, tab3 = st.tabs(["📊 Results", "📈 Visualization", "💾 Export"])
            
            with tab1:
                st.markdown(f"""
                <div class="glass-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                        <div>
                            <h3 style="color: #1F2937; margin: 0;">Optimal Transport Plan</h3>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 2rem; font-weight: 800; color: #10B981;">
                                {total_cost:,.2f} {currency.split()[0]}
                            </div>
                            <div style="color: #6B7280; font-size: 0.875rem;">
                                Total Minimum Cost
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Allocation table
                st.dataframe(
                    res_df.style.applymap(
                        lambda x: 'background-color: #D1FAE5; color: #065F46; font-weight: 600;' if x > 0 else ''
                    ),
                    use_container_width=True
                )
            
            with tab2:
                st.markdown("""
                <div class="glass-card">
                    <h3 style="color: #1F2937; margin: 0 0 1rem 0;">Supply Chain Flow Visualization</h3>
                </div>
                """, unsafe_allow_html=True)
                
                sankey_fig = plot_sankey(
                    allocation,
                    final_sources[:allocation.shape[0]],
                    final_dests[:allocation.shape[1]]
                )
                st.plotly_chart(sankey_fig, use_container_width=True)
                
                # Cost distribution
                st.markdown("---")
                st.markdown("""
                <div class="glass-card">
                    <h3 style="color: #1F2937; margin: 0 0 1rem 0;">Cost Distribution by Supplier</h3>
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
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(bar_fig, use_container_width=True)
            
            with tab3:
                st.markdown("""
                <div class="glass-card">
                    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                        <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #F59E0B 0%, #06B6D4 100%); 
                             border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                            <i class="fas fa-file-export" style="color: white; font-size: 1.25rem;"></i>
                        </div>
                        <div>
                            <h3 style="color: #1F2937; margin: 0;">Export Results</h3>
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
    
    except Exception as e:
        st.error(f"❌ Calculation error: {str(e)}")

# --- FEEDBACK SECTION ---
st.markdown("---")
st.markdown("""
<div class="glass-card">
    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
        <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%); 
             border-radius: 12px; display: flex; align-items: center; justify-content: center;">
            <i class="fas fa-comment-dots" style="color: white; font-size: 1.25rem;"></i>
        </div>
        <div>
            <h3 style="color: #1F2937; margin: 0;">Feedback</h3>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.form("feedback_form", clear_on_submit=True):
    name = st.text_input("Your Name", placeholder="Enter your name")
    message = st.text_area("Your Message", placeholder="Share your thoughts...", height=100)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submitted = st.form_submit_button("📨 SEND FEEDBACK", type="primary", use_container_width=True)
    
    if submitted and message:
        try:
            send_telegram_feedback(name if name else "Anonymous", message)
            st.success("✅ Thank you for your feedback!")
        except:
            st.success("✅ Feedback recorded. Thank you!")
    elif submitted:
        st.warning("⚠️ Please write a message before sending.")

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 2rem 0;">
    <p style="font-size: 0.9rem;">VOGEL PRO SYSTEM © 2024</p>
</div>
""", unsafe_allow_html=True)

# Ajouter FontAwesome
components.html("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
""", height=0)
