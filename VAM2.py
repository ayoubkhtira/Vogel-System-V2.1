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

# --- 5. AFFICHAGE DU HEADER (Composant Isolé) ---
header_code = """
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
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
            "https://ts2.mm.bing.net/th?id=OIP.3lcfFwaiQLjVRmVEnIJgRQHaE7&pid=15.1",
            
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

    
# --- Fonction Logique VAM ---
st.set_page_config(
    page_title="VOGEL SYSTEM",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded" # Optionnel : garde le menu ouvert
)




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

        # Pénalités Colonnes
        for c in range(n_cols):
            if demand_temp[c] == 0:
                col_penalties.append(-1)
            else:
                col_valid = [r for r in costs_temp[:, c] if r < INF]
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
    return allocation, total_cost

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

# --- Interface Utilisateur ---




# === SIDEBAR VOGEL SYSTEM PRO - SHADOW ROUGE ===
with st.sidebar:
    # Header VOGEL SYSTEM style
    st.markdown("""
    <div style='
        padding: 2.5rem 2rem;
        background: linear-gradient(135deg, #0f172a 0%, #1a1a2e 100%);
        border-radius: 0 25px 25px 0;
        border-left: 8px solid #ff4757;
        box-shadow: 0 25px 60px rgba(255,71,87,0.4);
        text-align: center;
        position: relative;
        overflow: hidden;
        margin-bottom: 2rem;
    '>
        <h2 style='
            font-family: "Orbitron", monospace;
            font-size: 1.8rem;
            font-weight: 900;
            margin: 0;
            background: linear-gradient(45deg, #ffffff 0%, #ff6b35 50%, #ff4757 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 4px;
            text-transform: uppercase;
        '>
            <i class="fas fa-cogs" style="margin-right: 15px; color: #ff4757; font-size: 1.4rem;"></i>
            VOGEL SYSTEM
        </h2>
        <p style='
            color: #ff6b6b;
            font-family: "Orbitron", monospace;
            font-size: 0.85rem;
            font-weight: 700;
            margin: 10px 0 0 0;
            letter-spacing: 2px;
            text-transform: uppercase;
        '>CONFIGURATION PRO</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Devise - Shadow Rouge Simple
    currency = st.text_input(
        "💱 Symbole de la devise",
        value="€",
        help="€, $, £, ¥",
        label_visibility="collapsed"
    )
    
    # Fournisseurs - Shadow Rouge Simple  
    num_sources = st.number_input(
        "🏭 Nombre de Fournisseurs",
        min_value=2, 
        value=3,
        step=1,
        format="%d",
        help="Nombre d'usines/sources"
    )
    
    # Clients - Shadow Rouge Simple
    num_dests = st.number_input(
        "👥 Nombre de Clients",
        min_value=2, 
        value=3,
        step=1,
        format="%d",
        help="Nombre de destinations/clients"
    )
    
    # Footer Status
    st.markdown("""
    <div style='
        padding: 1.5rem 1.5rem;
        background: linear-gradient(90deg, #ff4757 0%, #ff6b35 100%);
        border-radius: 0 15px 15px 0;
        text-align: center;
        box-shadow: 0 15px 40px rgba(255,71,87,0.4);
        margin-top: 2rem;
    '>
        <div style='
            color: white;
            font-family: "Orbitron", monospace;
            font-size: 0.9rem;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        '>
            <i class="fas fa-check-circle" style="margin-right: 8px;"></i>
            PRÊT À OPTIMISER
        </div>
    </div>
    """, unsafe_allow_html=True)

# === CSS SHADOW ROUGE UNIQUEMENT SUR DATA EDITORS ===
st.markdown("""
<style>
/* SHADOW ROUGE UNIQUEMENT SUR BOÎTES DE SAISIE */
.stDataEditor .dataframe {
    box-shadow: 0 20px 50px rgba(255,71,87,0.3) !important;
    border-radius: 15px !important;
    border-left: 5px solid #ff4757 !important;
    background: rgba(255,255,255,0.95) !important;
    backdrop-filter: blur(15px) !important;
}

.dark .stDataEditor .dataframe {
    background: rgba(26,32,44,0.95) !important;
    box-shadow: 0 25px 60px rgba(255,107,53,0.5) !important;
}

/* TYPO VOGEL SYSTEM */
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    font-family: "Orbitron", monospace !important;
}

/* INPUTS Sidebar Clean */
[data-testid="stSidebar"] .stTextInput > div > div > input,
[data-testid="stSidebar"] .stNumberInput > div > div > input {
    border-radius: 12px !important;
    border: 2px solid rgba(255,71,87,0.2) !important;
    padding: 12px 16px !important;
    background: rgba(255,255,255,0.9) !important;
}

.dark [data-testid="stSidebar"] .stTextInput > div > div > input,
.dark [data-testid="stSidebar"] .stNumberInput > div > div > input {
    background: rgba(30,41,59,0.9) !important;
    border-color: rgba(255,107,53,0.4) !important;
    color: #f1f5f9 !important;
}
</style>
""", unsafe_allow_html=True)

    
    col1, col2 = st.columns([1, 6])
    with col1:
        st.markdown("<div style='font-size: 1.4rem; color: #ff4757; margin-bottom: 0.5rem;'><i class='fas fa-euro-sign'></i></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<label style='font-weight: 600; color: #1f2937; margin-bottom: 0.5rem; font-size: 0.95rem;'>💱 Symbole de la devise</label>", unsafe_allow_html=True)
    
    currency = st.text_input(
        "", 
        value="€",
        label_visibility="collapsed",
        placeholder="€, $, £, ¥",
        help="Symbol monétaire pour l'affichage des coûts",
        key="currency_input"
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Section Fournisseurs - Progressif
    st.markdown("""
    <div style='
        background: rgba(255,255,255,0.8);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        border: 1px solid rgba(226,232,240,0.6);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    '>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 6])
    with col1:
        st.markdown("<div style='font-size: 1.4rem; color: #00d4aa; margin-bottom: 0.5rem;'><i class='fas fa-industry'></i></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<label style='font-weight: 600; color: #1f2937; margin-bottom: 0.5rem; font-size: 0.95rem;'>🏭 Nombre de Fournisseurs</label>", unsafe_allow_html=True)
    
    num_sources = st.number_input(
        "",
        min_value=2, 
        value=3, 
        step=1,
        format="%d",
        label_visibility="collapsed",
        help="Nombre d'usines/sources d'approvisionnement",
        key="sources_input"
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Section Clients - Animé
    st.markdown("""
    <div style='
        background: rgba(255,255,255,0.8);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        border: 1px solid rgba(226,232,240,0.6);
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    '>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 6])
    with col1:
        st.markdown("<div style='font-size: 1.4rem; color: #ff6b35; margin-bottom: 0.5rem;'><i class='fas fa-users'></i></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<label style='font-weight: 600; color: #1f2937; margin-bottom: 0.5rem; font-size: 0.95rem;'>👥 Nombre de Clients</label>", unsafe_allow_html=True)
    
    num_dests = st.number_input(
        "",
        min_value=2, 
        value=3, 
        step=1,
        format="%d",
        label_visibility="collapsed",
        help="Nombre de points de demande/clients finaux",
        key="dests_input"
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer Sidebar avec bouton Reset
    st.markdown("""
    <div style='
        padding: 1.5rem;
        background: linear-gradient(145deg, rgba(0,212,170,0.1) 0%, rgba(0,184,148,0.1) 100%);
        border-radius: 16px;
        border: 2px solid rgba(0,212,170,0.3);
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,212,170,0.2);
        margin-top: 1rem;
    '>
        <div style='font-size: 0.85rem; color: #059669; font-weight: 600; margin-bottom: 1rem;'>
            <i class='fas fa-check-circle'></i> Configuration prête
        </div>
        <button onclick='window.location.reload()' style='
            background: linear-gradient(135deg, #00d4aa, #00b894);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 10px 24px;
            font-weight: 600;
            cursor: pointer;
            font-family: inherit;
            box-shadow: 0 8px 25px rgba(0,212,170,0.4);
            transition: all 0.3s ease;
        ' onmouseover='this.style.transform="translateY(-2px)"; this.style.boxShadow="0 12px 35px rgba(0,212,170,0.6)"' 
        onmouseout='this.style.transform="translateY(0)"; this.style.boxShadow="0 8px 25px rgba(0,212,170,0.4)"'>
            🔄 Reset Config
        </button>
    </div>
    """, unsafe_allow_html=True)

# === CSS DARK MODE pour la sidebar ===
st.markdown("""
<style>
/* DARK MODE SIDEBAR */
.dark [data-testid="stSidebar"] {
    background: linear-gradient(145deg, #1a1a2e 0%, #16213e 100%) !important;
}
.dark .sidebar-card {
    background: rgba(26,32,44,0.9) !important;
    border-color: rgba(51,65,85,0.8) !important;
}
.dark .sidebar-header {
    background: linear-gradient(145deg, rgba(26,32,44,0.95) 0%, rgba(15,23,42,0.9) 100%) !important;
}
.dark input, .dark textarea {
    background: rgba(30,41,59,0.8) !important;
    color: #f1f5f9 !important;
    border-color: rgba(51,65,85,0.8) !important;
}
.dark label {
    color: #e2e8f0 !important;
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
                
            res_df = pd.DataFrame(allocation, index=final_sources, columns=final_dests)
            
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
                sankey_fig = plot_sankey(allocation, final_sources, final_dests)
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








