import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px
import random

# --- CONFIGURATION TELEGRAM (À remplir ou via Secrets) ---
TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"]

st.set_page_config(
    page_title="VOGEL SYSTEM",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS pour le dark/light mode et le switch ---
st.markdown("""
<style>
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --text-color: #333;
    --bg-color: #f8f9fa;
    --card-bg: #ffffff;
    --border-color: #e0e0e0;
}

[data-theme="dark"] {
    --primary-color: #764ba2;
    --secondary-color: #667eea;
    --text-color: #f0f0f0;
    --bg-color: #1a1a1a;
    --card-bg: #2d2d2d;
    --border-color: #444;
}

body {
    background-color: var(--bg-color) !important;
    color: var(--text-color) !important;
    transition: background-color 0.3s, color 0.3s;
}

.stApp {
    background-color: var(--bg-color) !important;
}

/* Style du switch */
.switch-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1rem 0;
    margin-top: 1rem;
    border-top: 1px solid var(--border-color);
}

.switch {
    position: relative;
    display: inline-block;
    width: 60px;
    height: 34px;
}

.switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #667eea;
    transition: .4s;
    border-radius: 34px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 6px;
}

.slider:before {
    position: absolute;
    content: "";
    height: 26px;
    width: 26px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
    z-index: 2;
}

input:checked + .slider {
    background-color: #764ba2;
}

input:checked + .slider:before {
    transform: translateX(26px);
}

.slider i {
    font-size: 14px;
    z-index: 1;
}

.slider .fa-sun {
    color: #ffd700 !important;
}

.slider .fa-moon {
    color: #fff !important;
}

/* Ajustements pour le dark mode */
[data-theme="dark"] .stDataEditor .dataframe {
    box-shadow: 0 20px 45px rgba(255, 107, 53, 0.4) !important;
    background-color: var(--card-bg) !important;
}

[data-theme="dark"] .stButton button {
    background-color: var(--primary-color) !important;
    color: white !important;
}

[data-theme="dark"] .stButton button:hover {
    background-color: var(--secondary-color) !important;
}

[data-theme="dark"] .stTextInput input,
[data-theme="dark"] .stTextArea textarea,
[data-theme="dark"] .stNumberInput input {
    background-color: var(--card-bg) !important;
    color: var(--text-color) !important;
    border-color: var(--border-color) !important;
}
</style>

<script>
// Charger le thème depuis localStorage
function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    document.getElementById('switch').checked = (savedTheme === 'dark');
}

// Basculer le thème
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Attacher l'événement au switch
document.addEventListener('DOMContentLoaded', function() {
    loadTheme();
    const themeSwitch = document.getElementById('switch');
    if (themeSwitch) {
        themeSwitch.addEventListener('change', toggleTheme);
    }
});
</script>
""", unsafe_allow_html=True)

# --- 5. AFFICHAGE DU HEADER (Composant Isolé) ---
header_code = """
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
<style>
    body { margin: 0; padding: 0; background-color: transparent; font-family: 'Roboto', sans-serif; overflow: hidden; }
    .main-header {
        position: relative; padding: 30px; background: #0a0a0a; border-radius: 10px;
        border-left: 12px solid #FF0000; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        min-height: 120px; display: flex; flex-direction: column; justify-content: center;
    }
    #bg-carousel {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-size: cover; background-position: center; opacity: 0.3; transition: background-image 1.5s ease-in-out; z-index: 0;
    }
    .overlay {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.15) 50%);
        background-size: 100% 4px; z-index: 1; pointer-events: none;
    }
    .content { position: relative; z-index: 2; }
    h1 { font-family: 'Orbitron', sans-serif; text-transform: uppercase; letter-spacing: 5px; font-size: 2.2rem; margin: 0; color: #ffffff; text-shadow: 0 0 15px rgba(230, 126, 34, 0.8); }
    .status { color: #FF0000; font-weight: 700; letter-spacing: 4px; font-size: 0.8rem; text-transform: uppercase; margin-top: 10px; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
    .active-dot { display: inline-block; width: 10px; height: 10px; background: #fff; border-radius: 50%; margin-left: 10px; animation: blink 1.5s infinite; box-shadow: 0 0 8px #fff; }
</style>
</head>
<body>
    <div class="main-header">
        <div id="bg-carousel"></div>
        <div class="overlay"></div>
        <div class="content">
            <h1> VOGEL SYSTEM <span style="color:#FF0000;">Pro</span></h1>
            <div class="status">Logistics Intelligence <span class="active-dot"></span></div>
        </div>
    </div>
    <script>
        const images = [
            "https://ts4.mm.bing.net/th?id=OIP.SP1huODTJEKsucmtJ60wdAHaEc&pid=15.1",
            "https://ts1.mm.bing.net/th?id=OIP.eBuuZlc7PE_E6gGNbDVTtAHaE7&pid=15.1",
            "https://ts1.mm.bing.net/th?id=OIP.w3xJ3p8KSGx-PmSJz-HxHwHaE8&pid=15.1",
            "https://ts2.mm.bing.net/th?id=OIP.3lcfFwaiQLjVRmVEnIJgRQHaE7&pid=15.1"
        ];
        let index = 0;
        const bgDiv = document.getElementById('bg-carousel');
        function changeBackground() {
            bgDiv.style.backgroundImage = "url('" + images[index] + "')";
            index = (index + 1) % images.length;
        }
        changeBackground();
        setInterval(changeBackground, 5000);
    </script>
</body>
</html>
"""
components.html(header_code, height=200)

def send_telegram_feedback(name, message):
    if TOKEN == "TON_TOKEN_BOT_TELEGRAM":
        return # Ne rien faire si pas configuré
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
    
    # Sauvegarde dimensions originales
    original_cols = n_cols
    original_rows = n_rows
    
    # Gestion des cas déséquilibrés (Dummy)
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

        # Pénalités Lignes
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

        # Pénalités Colonnes - CORRIGÉ
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
                 # Fallback rare edge case
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

# --- Export Excel ---
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

# --- Visualisation Sankey ---
def plot_sankey(allocation_matrix, source_names, dest_names):
    # Préparation des labels (Sources + Dests)
    labels = source_names + dest_names
    
    # Indices Plotly : Sources [0..n-1], Dests [n..n+m-1]
    source_indices = []
    target_indices = []
    values = []
    custom_data = [] # Pour afficher les infos au survol

    n_sources = len(source_names)
    
    for r in range(allocation_matrix.shape[0]):
        for c in range(allocation_matrix.shape[1]):
            qty = allocation_matrix[r, c]
            if qty > 0:
                source_indices.append(r)
                target_indices.append(n_sources + c) # Offset pour les destinations
                values.append(qty)
                
                # Info bulle
                src_name = source_names[r]
                dst_name = dest_names[c]
                custom_data.append(f"{src_name} → {dst_name}")

    # Création du diagramme
    fig = go.Figure(data=[go.Sankey(
        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = labels,
            color = "blue"
        ),
        link = dict(
            source = source_indices,
            target = target_indices,
            value = values,
            customdata = custom_data,
            hovertemplate='%{customdata}<br />Quantité: %{value}<extra></extra>'
        ))])

    fig.update_layout(title_text="Diagramme de Flux (Sankey)", font_size=12, height=500)
    return fig

# === SIDEBAR SIMPLE MODERNE ===
with st.sidebar:
    st.markdown("""
    <div style='
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 0 20px 20px 0;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102,126,234,0.3);
        margin-bottom: 1.5rem;
    '>
        <h2 style='
            color: white; 
            margin: 0; 
            font-size: 1.4rem; 
            font-weight: 700;
            letter-spacing: 1px;
        '>
            ⚙️ PARAMÈTRES
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    currency = st.text_input("💱 Devise", value="€", help="€, $, £")
    num_sources = st.number_input("🏭 Fournisseurs", min_value=2, value=3, format="%d")
    num_dests = st.number_input("👥 Clients", min_value=2, value=3, format="%d")
    
    # --- SWITCH DARK/LIGHT MODE ---
    st.markdown('<div class="switch-container">', unsafe_allow_html=True)
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
        <label class="switch">
            <input type="checkbox" id="switch">
            <span class="slider round">
                <i class="fas fa-sun"></i>
                <i class="fas fa-moon"></i>
            </span>
        </label>
        <span style="color: var(--text-color); font-weight: 500;">Mode Sombre</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<style>
.stDataEditor .dataframe {
    box-shadow: 0 15px 35px rgba(255,71,87,0.2) !important;
    border-radius: 12px !important;
    border-left: 4px solid #ff4757 !important;
}
.dark .stDataEditor .dataframe {
    box-shadow: 0 20px 45px rgba(255,107,53,0.4) !important;
}
</style>
""", unsafe_allow_html=True)

st.subheader("2. Personnalisation des Noms")
col1, col2 = st.columns(2)
with col1:
    source_names = []
    with st.expander("Noms des Fournisseurs", expanded=False):
        for i in range(num_sources):
            source_names.append(st.text_input(f"Fournisseur {i+1}", value=f"Usine {i+1}", key=f"src_{i}"))
with col2:
    dest_names = []
    with st.expander("Noms des Clients", expanded=False):
        for i in range(num_dests):
            dest_names.append(st.text_input(f"Client {i+1}", value=f"Client {i+1}", key=f"dst_{i}"))

st.subheader("3. Saisie des Coûts et Capacités")
df_structure = pd.DataFrame(0.0, index=source_names, columns=dest_names + ["OFFRE (Capacité)"])
st.caption(f"Entrez les coûts unitaires ({currency}) et la capacité de chaque fournisseur.")
input_df = st.data_editor(df_structure, key="input_matrix", use_container_width=True)

st.caption("Entrez la demande pour chaque client.")
demand_structure = pd.DataFrame(0.0, index=["DEMANDE"], columns=dest_names)
demand_df = st.data_editor(demand_structure, key="demand_matrix", use_container_width=True)

if st.button("🚀 Lancer l'Optimisation et Visualiser", type="primary", use_container_width=True):
    try:
        costs = input_df.iloc[:, :-1].values
        supply = input_df.iloc[:, -1].values
        demand = demand_df.iloc[0, :].values
        
        if np.any(costs < 0) or np.any(supply < 0) or np.any(demand < 0):
            st.error("Les valeurs doivent être positives.")
        else:
            allocation, total_cost = vogel_approximation_method(costs, supply, demand)
            
            # --- Préparation des Labels Finaux (avec Dummy si nécessaire) ---
            final_sources = source_names.copy()
            final_dests = dest_names.copy()
            
            if allocation.shape[0] > len(source_names):
                final_sources.append("Fictif (Offre)")
            if allocation.shape[1] > len(dest_names):
                final_dests.append("Fictif (Demande)")
                
            res_df = pd.DataFrame(allocation, index=final_sources[:allocation.shape[0]], columns=final_dests[:allocation.shape[1]])
            
            st.divider()
            
            # --- TABS POUR RÉSULTATS & VISUALISATION ---
            tab1, tab2, tab3 = st.tabs(["📋 Tableau des Résultats", "📊 Visualisation des Flux", "📥 Export Excel"])
            
            with tab1:
                st.subheader("Plan de Transport Optimal")
                st.metric(label="Coût Total Minimum", value=f"{total_cost:,.2f} {currency}")
                
                def highlight_cells(val):
                    return 'background-color: #d4edda; color: black' if val > 0 else ''
                st.dataframe(res_df.style.applymap(highlight_cells), use_container_width=True)
                
            with tab2:
                st.subheader("Flux Physiques (Source → Destination)")
                sankey_fig = plot_sankey(allocation, final_sources[:allocation.shape[0]], final_dests[:allocation.shape[1]])
                st.plotly_chart(sankey_fig, use_container_width=True)
                
                st.divider()
                st.subheader("Détail des Coûts par Fournisseur")
                # Calcul des coûts par ligne pour graphique
                # Attention: dimensions de costs vs allocation peuvent différer si dummy
                real_rows = min(costs.shape[0], allocation.shape[0])
                real_cols = min(costs.shape[1], allocation.shape[1])
                
                cost_per_source = []
                for r in range(real_rows):
                    row_cost = np.sum(allocation[r, :real_cols] * costs[r, :real_cols])
                    cost_per_source.append(row_cost)
                
                # Création Bar Chart
                bar_fig = px.bar(
                    x=source_names[:real_rows], 
                    y=cost_per_source,
                    labels={'x': 'Fournisseur', 'y': f'Coût ({currency})'},
                    title="Coût total généré par Fournisseur",
                    color=cost_per_source,
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(bar_fig, use_container_width=True)

            with tab3:
                st.subheader("Télécharger le rapport")
                excel_data = generate_excel(input_df, demand_df, res_df, total_cost, currency)
                st.download_button(
                    label="📄 Télécharger le rapport Excel (.xlsx)",
                    data=excel_data,
                    file_name="rapport_vam_transport_visu.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            
    except Exception as e:
        st.error(f"Erreur de calcul : {e}")

# --- SECTION AVIS & TELEGRAM ---
st.divider()
st.subheader("💬 Votre Avis")

with st.form("feedback_form", clear_on_submit=True):
    name = st.text_input("👤 Votre Nom (ou entreprise)")
    msg = st.text_area("✍️ Votre commentaire ou suggestion")
    
    # Bouton d'envoi
    submit_button = st.form_submit_button("🚀 Envoyer l'avis", type="primary", use_container_width=True)

    if submit_button:
        if msg:
            # 1. Animation de chargement pendant l'appel API
            with st.status("Transmission de votre message ...", expanded=False) as status:
                success = send_telegram_feedback(name, msg)
                status.update(label="Message transmis avec succès ! ✅", state="complete")
            
            # 2. Petite notification discrète en bas à droite
            st.toast(f"Merci {name if name else ''} ! Avis reçu.", icon='📩')
            # Message de succès final
            st.success("✅ Votre avis a été envoyé et sera consulté par l'équipe.")
        else:
            st.warning("⚠️ Le champ commentaire ne peut pas être vide.")

# --- JavaScript pour charger le thème initial ---
components.html("""
<script>
// Fonction pour initialiser le thème
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    const switchElement = document.getElementById('switch');
    if (switchElement) {
        switchElement.checked = (savedTheme === 'dark');
    }
}

// Attacher l'événement au switch
function attachSwitchListener() {
    const themeSwitch = document.getElementById('switch');
    if (themeSwitch) {
        themeSwitch.addEventListener('change', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }
}

// Initialiser quand la page est chargée
document.addEventListener('DOMContentLoaded', function() {
    initTheme();
    attachSwitchListener();
});

// Réessayer après un court délai au cas où les éléments ne seraient pas encore chargés
setTimeout(() => {
    initTheme();
    attachSwitchListener();
}, 100);
</script>
""", height=0)
