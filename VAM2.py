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
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialiser l'état du thème
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Fonction pour basculer le thème
def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# --- CSS UNIFORME POUR L'APPLICATION ---
css = """
<style>
/* Variables CSS pour les thèmes */
:root {
    /* Mode Clair */
    --primary: #2563eb;
    --secondary: #7c3aed;
    --background: #f8fafc;
    --surface: #ffffff;
    --text: #1e293b;
    --text-secondary: #64748b;
    --border: #e2e8f0;
    --success: #10b981;
    --warning: #f59e0b;
    --error: #ef4444;
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

[data-theme="dark"] {
    /* Mode Sombre */
    --primary: #3b82f6;
    --secondary: #8b5cf6;
    --background: #0f172a;
    --surface: #1e293b;
    --text: #f1f5f9;
    --text-secondary: #94a3b8;
    --border: #334155;
    --success: #34d399;
    --warning: #fbbf24;
    --error: #f87171;
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
}

/* Styles généraux */
* {
    transition: background-color 0.3s ease, border-color 0.3s ease;
}

.stApp {
    background-color: var(--background) !important;
    color: var(--text) !important;
}

/* Header */
.main-header {
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
    color: white !important;
    border-radius: 12px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: var(--shadow);
}

/* Widgets Streamlit */
.stButton > button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 600 !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15) !important;
}

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: var(--surface) !important;
    color: var(--text) !important;
    border: 2px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 0.75rem !important;
}

.stSelectbox > div > div {
    background-color: var(--surface) !important;
    color: var(--text) !important;
    border: 2px solid var(--border) !important;
    border-radius: 8px !important;
}

.stDataFrame {
    background-color: var(--surface) !important;
    border-radius: 12px !important;
    border: 1px solid var(--border) !important;
    overflow: hidden !important;
}

.stExpander {
    background-color: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

.stTabs [data-baseweb="tab-list"] {
    background-color: var(--surface) !important;
    border-radius: 8px !important;
    padding: 4px !important;
}

.stTabs [data-baseweb="tab"] {
    color: var(--text) !important;
}

.stMetric {
    background-color: var(--surface) !important;
    padding: 1rem !important;
    border-radius: 8px !important;
    border: 1px solid var(--border) !important;
}

/* Bouton du thème */
.theme-toggle {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
    background: var(--surface);
    border: 2px solid var(--border);
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.theme-toggle:hover {
    border-color: var(--primary);
}

.theme-switch {
    position: relative;
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
    background-color: white;
    transition: .4s;
    border-radius: 50%;
}

input:checked + .theme-slider:before {
    transform: translateX(30px);
}

.theme-icon {
    font-size: 1.2rem;
}

/* Cartes et conteneurs */
.card {
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow);
}

/* Typographie */
h1, h2, h3, h4, h5, h6 {
    color: var(--text) !important;
}

p {
    color: var(--text-secondary) !important;
}

/* Séparateurs */
hr {
    border-color: var(--border) !important;
    margin: 2rem 0 !important;
}

/* Status messages */
.stAlert {
    border-radius: 8px !important;
    border-left: 4px solid var(--primary) !important;
}

.stSuccess {
    background-color: rgba(16, 185, 129, 0.1) !important;
    border-left-color: var(--success) !important;
}

.stWarning {
    background-color: rgba(245, 158, 11, 0.1) !important;
    border-left-color: var(--warning) !important;
}

.stError {
    background-color: rgba(239, 68, 68, 0.1) !important;
    border-left-color: var(--error) !important;
}
</style>
"""

# Appliquer le CSS
st.markdown(css, unsafe_allow_html=True)

# Appliquer le thème au body
theme = "dark" if st.session_state.dark_mode else "light"
st.markdown(f'<body data-theme="{theme}">', unsafe_allow_html=True)

# --- HEADER SIMPLIFIÉ ---
header_html = f"""
<div class="main-header">
    <h1 style="color: white; margin: 0; font-size: 2.5rem; font-weight: 700;">VOGEL SYSTEM <span style="color: #ff6b35;">Pro</span></h1>
    <p style="color: rgba(255, 255, 255, 0.9); margin-top: 0.5rem; font-size: 1.1rem;">Logistics Intelligence Platform</p>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# === SIDEBAR SIMPLIFIÉ ===
with st.sidebar:
    # Header de la sidebar
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem; border-radius: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin-bottom: 2rem;">
        <h2 style="color: white; margin: 0; font-size: 1.5rem;">⚙️ PARAMÈTRES</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Paramètres principaux
    currency = st.selectbox("💱 Devise", ["€", "$", "£", "¥", "₹"], index=0)
    num_sources = st.number_input("🏭 Nombre de Fournisseurs", min_value=2, max_value=10, value=3)
    num_dests = st.number_input("👥 Nombre de Clients", min_value=2, max_value=10, value=3)
    
    # Séparateur
    st.markdown("---")
    
    # Bouton de thème simplifié
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        current_theme = "🌙 Sombre" if st.session_state.dark_mode else "☀️ Clair"
        if st.button(f"{current_theme}", use_container_width=True):
            toggle_theme()
            st.rerun()

# --- Fonctions principales (inchangées) ---
def send_telegram_feedback(name, message):
    if TOKEN == "TON_TOKEN_BOT_TELEGRAM":
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    text = f"🚀 *Nouvel avis sur l'app VAM*\n\n*Nom:* {name}\n*Message:* {message}"
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
            line = dict(color = "black", width = 0.5),
            label = labels,
            color = "#3b82f6"
        ),
        link = dict(
            source = source_indices,
            target = target_indices,
            value = values,
            customdata = custom_data,
            hovertemplate='%{customdata}<br />Quantité: %{value}<extra></extra>'
        ))])
    fig.update_layout(
        title_text="Diagramme de Flux (Sankey)",
        font_size=12,
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# --- SECTION PRINCIPALE DE L'APPLICATION ---

# Section 1: Personnalisation des noms
st.markdown("""
<div class="card">
    <h3>👥 Personnalisation des Noms</h3>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    with st.expander("🏭 Fournisseurs", expanded=True):
        source_names = []
        for i in range(num_sources):
            source_names.append(st.text_input(f"Fournisseur {i+1}", value=f"Usine {i+1}", key=f"src_{i}"))

with col2:
    with st.expander("👥 Clients", expanded=True):
        dest_names = []
        for i in range(num_dests):
            dest_names.append(st.text_input(f"Client {i+1}", value=f"Client {i+1}", key=f"dst_{i}"))

# Section 2: Saisie des données
st.markdown("""
<div class="card">
    <h3>💰 Saisie des Coûts et Capacités</h3>
    <p>Entrez les coûts unitaires ({}) et la capacité de chaque fournisseur</p>
</div>
""".format(currency), unsafe_allow_html=True)

# Créer le dataframe pour les coûts
costs_data = {}
for dest in dest_names:
    costs_data[dest] = [0.0] * num_sources

df_costs = pd.DataFrame(costs_data, index=source_names)
df_costs["OFFRE (Capacité)"] = [0.0] * num_sources

# Éditeur de données pour les coûts
edited_costs = st.data_editor(
    df_costs,
    use_container_width=True,
    key="costs_editor",
    column_config={
        "OFFRE (Capacité)": st.column_config.NumberColumn(
            "OFFRE (Capacité)",
            help="Capacité de production du fournisseur"
        )
    }
)

st.markdown("""
<div class="card">
    <h3>📋 Demande des Clients</h3>
</div>
""", unsafe_allow_html=True)

# Créer le dataframe pour la demande
demand_data = {dest: [0.0] for dest in dest_names}
df_demand = pd.DataFrame(demand_data, index=["DEMANDE"])

# Éditeur de données pour la demande
edited_demand = st.data_editor(
    df_demand,
    use_container_width=True,
    key="demand_editor"
)

# Bouton d'optimisation
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Lancer l'Optimisation", type="primary", use_container_width=True):
        st.session_state.run_optimization = True

# Section 3: Résultats
if 'run_optimization' in st.session_state and st.session_state.run_optimization:
    try:
        costs = edited_costs.iloc[:, :-1].values.astype(float)
        supply = edited_costs.iloc[:, -1].values.astype(float)
        demand = edited_demand.iloc[0, :].values.astype(float)
        
        if np.any(costs < 0) or np.any(supply < 0) or np.any(demand < 0):
            st.error("❌ Les valeurs doivent être positives.")
        else:
            with st.spinner("Calcul en cours..."):
                allocation, total_cost = vogel_approximation_method(costs, supply, demand)
            
            # Préparation des résultats
            final_sources = source_names.copy()
            final_dests = dest_names.copy()
            
            if allocation.shape[0] > len(source_names):
                final_sources.append("Fictif (Offre)")
            if allocation.shape[1] > len(dest_names):
                final_dests.append("Fictif (Demande)")
                
            res_df = pd.DataFrame(
                allocation,
                index=final_sources[:allocation.shape[0]],
                columns=final_dests[:allocation.shape[1]]
            )
            
            st.markdown("---")
            
            # Onglets pour les résultats
            tab1, tab2, tab3 = st.tabs(["📊 Résultats", "📈 Visualisation", "💾 Export"])
            
            with tab1:
                st.markdown(f"""
                <div class="card">
                    <h3>✅ Plan de Transport Optimal</h3>
                    <div style="font-size: 1.5rem; color: var(--success); font-weight: bold;">
                        Coût Total Minimum: {total_cost:,.2f} {currency}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Afficher le tableau des allocations
                st.dataframe(
                    res_df.style.applymap(
                        lambda x: 'background-color: #d4edda; color: black' if x > 0 else ''
                    ),
                    use_container_width=True
                )
            
            with tab2:
                st.markdown("""
                <div class="card">
                    <h3>📊 Visualisation des Flux</h3>
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
                st.markdown("---")
                st.markdown("""
                <div class="card">
                    <h3>📊 Répartition des Coûts par Fournisseur</h3>
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
                    labels={'x': 'Fournisseur', 'y': f'Coût ({currency})'},
                    title="",
                    color=cost_per_source,
                    color_continuous_scale='Blues'
                )
                bar_fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(bar_fig, use_container_width=True)
            
            with tab3:
                st.markdown("""
                <div class="card">
                    <h3>💾 Export des Résultats</h3>
                </div>
                """, unsafe_allow_html=True)
                
                excel_data = generate_excel(edited_costs, edited_demand, res_df, total_cost, currency)
                
                st.download_button(
                    label="📥 Télécharger le Rapport Excel",
                    data=excel_data,
                    file_name=f"rapport_vam_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                
                st.info("📋 Le rapport contient toutes les données d'entrée, la solution optimale et les résultats détaillés.")
    
    except Exception as e:
        st.error(f"❌ Erreur lors du calcul : {str(e)}")

# --- SECTION FEEDBACK ---
st.markdown("---")
st.markdown("""
<div class="card">
    <h3>💬 Votre Avis</h3>
    <p>Partagez vos commentaires pour améliorer l'application</p>
</div>
""", unsafe_allow_html=True)

with st.form("feedback_form", clear_on_submit=True):
    name = st.text_input("👤 Votre nom ou entreprise")
    message = st.text_area("💭 Votre message", height=100)
    
    submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
    with submit_col2:
        submitted = st.form_submit_button("📨 Envoyer", type="primary", use_container_width=True)
    
    if submitted and message:
        try:
            send_telegram_feedback(name if name else "Anonyme", message)
            st.success("✅ Merci pour votre feedback !")
            st.balloons()
        except:
            st.warning("⚠️ Impossible d'envoyer le message, mais il a été enregistré localement.")
    elif submitted:
        st.warning("⚠️ Veuillez écrire un message avant d'envoyer.")

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: var(--text-secondary); padding: 2rem 0;">
    <p>VOGEL SYSTEM Pro © 2024 | Logistics Intelligence Platform</p>
    <p style="font-size: 0.9rem;">Développé avec ❤️ pour optimiser votre logistique</p>
</div>
""", unsafe_allow_html=True)
