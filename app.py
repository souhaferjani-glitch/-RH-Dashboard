import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import time
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="RH Dashboard - La Pratique Electronique",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== STYLE CSS ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Modern Card - Design uniforme pour toutes les cartes */
    .modern-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 1.5rem;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        border: 1px solid #eef2f6;
        text-align: center;
        height: 100%;
    }
    
    .modern-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.15);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .kpi-value {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
    }
    
    .kpi-label {
        font-size: 0.85rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 500;
    }
    
    .trend-up {
        color: #10b981;
        font-size: 0.75rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    .trend-down {
        color: #ef4444;
        font-size: 0.75rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    .alert-critical {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%);
        border-left: 4px solid #dc3545;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
        color: white;
        font-weight: 500;
        animation: pulse 2s infinite;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #ffd93d 0%, #ffc107 100%);
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
        color: #333;
        font-weight: 500;
    }
    
    .success-card {
        background: linear-gradient(135deg, #51cf66 0%, #40c057 100%);
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
        color: white;
        font-weight: 500;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
        display: inline-block;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
        border-right: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stat-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        background: #f8fafc;
        border-radius: 1rem;
        margin: 0.5rem 0;
    }
    /* ========== STYLE POUR MODE SOMBRE (DÉTECTION AUTOMATIQUE) ========== */
@media (prefers-color-scheme: dark) {
    [data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0, 255, 255, 0.3);
    }
    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stMarkdown *,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .css-1c6f4el,
    [data-testid="stSidebar"] .css-1c6f4el * {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div,
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] div {
        background-color: rgba(255, 255, 255, 0.15);
        border-color: rgba(0, 255, 255, 0.3);
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox svg,
    [data-testid="stSidebar"] .stMultiSelect svg {
        fill: #00ffff !important;
    }
}
    /* Correction de la couleur du texte dans le sidebar */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] * {
        color: #1e293b !important;
    }
</style>
</style>
""", unsafe_allow_html=True)

# ==================== FONCTION POUR COMPTEUR ANIMÉ ====================
def animated_counter(target_value, prefix="", suffix="", duration=1.0):
    """Affiche un compteur animé qui compte de 0 à la valeur cible"""
    if "counted" not in st.session_state:
        st.session_state.counted = {}
    
    key = f"{prefix}_{target_value}_{suffix}"
    
    if key not in st.session_state.counted:
        # Animation en JavaScript
        counter_html = f"""
        <div class="kpi-value" id="counter_{id(key)}">
            <span id="number_{id(key)}">0</span>
        </div>
        <script>
            (function() {{
                var target = {target_value};
                var duration = {duration * 1000};
                var stepTime = 20;
                var steps = duration / stepTime;
                var increment = target / steps;
                var current = 0;
                var element = document.getElementById('number_{id(key)}');
                var timer = setInterval(function() {{
                    current += increment;
                    if (current >= target) {{
                        current = target;
                        clearInterval(timer);
                    }}
                    element.innerText = Math.floor(current);
                }}, stepTime);
            }})();
        </script>
        """
        st.markdown(counter_html, unsafe_allow_html=True)
        st.session_state.counted[key] = True
    else:
        st.markdown(f'<div class="kpi-value">{prefix}{target_value}{suffix}</div>', unsafe_allow_html=True)
    
    return target_value

# ==================== LOGIN - DESIGN SPLIT ====================
USERS = {"Rhadmin": "admin123"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

def show_login():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        animation: gradientBG 8s ease infinite;
    }
    
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        padding: 40px;
    }
    
    .login-split-card {
        display: flex;
        max-width: 900px;
        width: 100%;
        background: white;
        border-radius: 32px;
        overflow: hidden;
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.3);
    }
    
    .login-left {
        flex: 1;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 48px 32px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    
    .logo-large {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        margin-bottom: 24px;
        border: 4px solid rgba(255,255,255,0.3);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    
    .brand-title {
        font-size: 28px;
        font-weight: 800;
        color: white;
        margin-bottom: 8px;
    }
    
    .brand-subtitle {
        font-size: 14px;
        color: rgba(255,255,255,0.8);
        margin-bottom: 16px;
    }
    
    .login-right {
        flex: 1;
        padding: 48px 40px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .welcome-title {
        font-size: 28px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 32px;
        text-align: center;
    }
    
    .stTextInput > div > div > input {
        width: 100%;
        padding: 12px 16px;
        font-size: 14px;
        border: 1.5px solid #e2e8f0;
        border-radius: 12px;
        background: #fafbfc;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        font-weight: 600;
        border-radius: 40px;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    @media (max-width: 768px) {
        .login-split-card {
            flex-direction: column;
            max-width: 400px;
        }
        .login-left { padding: 32px; }
        .logo-large { width: 80px; height: 80px; }
        .brand-title { font-size: 22px; }
    }
    </style>
    
    <div class="login-container">
        <div class="login-split-card">
            <div class="login-left">
                <img src="https://raw.githubusercontent.com/souhaferjani-glitch/-RH-Dashboard/main/logo.png" 
                     class="logo-large" 
                     onerror="this.style.display='none'; this.parentElement.innerHTML='<div style=\'width:120px;height:120px;background:rgba(255,255,255,0.2);border-radius:50%;display:inline-flex;align-items:center;justify-content:center;margin-bottom:24px;border:4px solid rgba(255,255,255,0.3)\'><span style=\'font-size:55px;color:white\'>📊</span></div>'">
                <div class="brand-title">RH Dashboard</div>
                <div class="brand-subtitle">La Pratique Electronique</div>
            </div>
            <div class="login-right">
                <div class="welcome-title">Bienvenue</div>
    """, unsafe_allow_html=True)
    
    username = st.text_input("", placeholder="Rhadmin", key="login_username", label_visibility="collapsed")
    password = st.text_input("", placeholder="••••••••", type="password", key="login_password", label_visibility="collapsed")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Login", use_container_width=True):
            if username in USERS and USERS[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
    
    st.markdown("""
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if not st.session_state.logged_in:
    show_login()
    st.stop()

# ==================== CHARGEMENT DES DONNÉES ====================
@st.cache_data
def load_data():
    effectifs = pd.DataFrame({
        'Matricule': ['EMP001','EMP002','EMP003','EMP004','EMP005','EMP006','EMP007','EMP008','EMP009','EMP010','EMP011','EMP012','EMP013','EMP014','EMP015'],
        'Date_Embauche': ['2020-01-01','2021-06-15','2022-03-10','2023-09-05','2021-01-20','2023-07-01','2022-11-15','2020-05-10','2024-02-01','2021-08-15','2023-03-20','2022-12-05','2021-07-10','2023-09-01','2022-04-15'],
        'Date_Sortie': ['','2024-12-01','','','2024-10-15','','2025-03-31','','','','2025-02-28','','','','2025-01-15'],
        'Motif_Sortie': ['','Démission','','','Retraite','','Démission','','','','Licenciement','','','','Démission'],
        'Service': ['Commercial','RH','Technique','Commercial','Administration','Technique','Commercial','RH','Technique','Administration','Commercial','Technique','RH','Commercial','Technique'],
        'Categorie': ['Cadre','Non cadre','Cadre','Non cadre','Cadre','Non cadre','Cadre','Cadre','Non cadre','Non cadre','Non cadre','Cadre','Non cadre','Cadre','Non cadre'],
        'Sexe': ['H','F','H','F','H','F','F','F','H','F','H','H','F','H','F']
    })
    effectifs['Date_Embauche'] = pd.to_datetime(effectifs['Date_Embauche'])
    effectifs['Date_Sortie'] = pd.to_datetime(effectifs['Date_Sortie'], errors='coerce')
    
    mouvements = pd.DataFrame({
        'Mois': ['2024-01-01','2024-02-01','2024-03-01','2024-04-01','2024-05-01','2024-06-01'],
        'Entrees': [2,1,3,0,2,1],
        'Sorties_Dem': [1,0,2,1,0,2],
        'Sorties_Retr': [0,1,0,0,0,0],
        'Sorties_Lice': [0,0,1,0,0,0]
    })
    mouvements['Mois'] = pd.to_datetime(mouvements['Mois'])
    
    promotions = pd.DataFrame({
        'Matricule': ['EMP001','EMP003','EMP008','EMP012'],
        'Date_Promot': ['2025-01-01','2024-03-15','2024-12-01','2024-06-10'],
        'Ancien_Grade': ['Commercial Senior','Technicien','Assistant RH','Ingénieur'],
        'Nouveau_Grade': ['Directeur Commercial','Technicien Principal','Responsable RH','Ingénieur Principal']
    })
    promotions['Date_Promot'] = pd.to_datetime(promotions['Date_Promot'])
    
    questionnaires = pd.DataFrame({
        'Periode': ['01/2024','02/2024','03/2024','04/2024','05/2024','06/2024'],
        'Nb_Diffuses': [50,50,50,50,50,50],
        'Nb_Reponses': [42,38,45,40,44,39],
        'Taux_Reponse': [84,76,90,80,88,78]
    })
    
    entretiens = pd.DataFrame({
        'Annee': [2023,2024,2025],
        'Nb_Planifies': [20,22,15],
        'Nb_Realises': [18,19,13],
        'Taux_Realisation': [90,86.4,86.7]
    })
    
    sanctions = pd.DataFrame({
        'Date': ['2024-01-15','2024-02-20','2024-03-10','2024-04-05','2024-05-12'],
        'Service': ['Commercial','Technique','RH','Commercial','Technique'],
        'Type': ['Avertissement','Blâme','Avertissement','Mise à pied','Blâme']
    })
    sanctions['Date'] = pd.to_datetime(sanctions['Date'])
    
    absenteisme = pd.DataFrame({
        'Mois': ['01/2024','02/2024','03/2024','04/2024','05/2024','06/2024'],
        'Service': ['Commercial','Technique','RH','Commercial','Technique','RH'],
        'Taux_Absence': [5.2,6.8,3.5,6.1,7.2,4.2]
    })
    
    contrats_expiration = pd.DataFrame({
        'Matricule': ['EMP004', 'EMP009', 'EMP014'],
        'Date_Fin': pd.to_datetime(['2026-04-15', '2026-04-20', '2026-05-01']),
        'Type': ['CDD', 'CDD', 'CDD'],
        'Service': ['Commercial', 'Technique', 'Commercial']
    })
    
    return effectifs, mouvements, promotions, questionnaires, entretiens, sanctions, absenteisme, contrats_expiration

effectifs, mouvements, promotions, questionnaires, entretiens, sanctions, absenteisme, contrats_expiration = load_data()

# ==================== CALCULS ====================
actifs = effectifs[effectifs['Date_Sortie'].isna()]
total = len(actifs)
departs = len(effectifs[~effectifs['Date_Sortie'].isna()])
turnover = (departs / len(effectifs) * 100) if len(effectifs) > 0 else 0

cadres = effectifs[effectifs['Categorie'] == 'Cadre']
departs_cadres = len(cadres[~cadres['Date_Sortie'].isna()])
fuite_cadres = (departs_cadres / len(cadres) * 100) if len(cadres) > 0 else 0

recents = effectifs[effectifs['Date_Embauche'] > datetime.now() - timedelta(days=365)]
qualite = (len(recents[recents['Date_Sortie'].isna()]) / len(recents) * 100) if len(recents) > 0 else 0

mouvements['Total_Sorties'] = mouvements['Sorties_Dem'] + mouvements['Sorties_Retr'] + mouvements['Sorties_Lice']

embauches_an_dernier = effectifs[effectifs['Date_Embauche'] > datetime.now() - timedelta(days=365)]
departs_1ere_annee = len(embauches_an_dernier[~embauches_an_dernier['Date_Sortie'].isna()])
taux_depart_1ere = (departs_1ere_annee / len(embauches_an_dernier) * 100) if len(embauches_an_dernier) > 0 else 0

if len(promotions) > 0:
    promo_with_embauche = promotions.merge(effectifs[['Matricule', 'Date_Embauche']], 
                                           left_on='Matricule', right_on='Matricule')
    promo_with_embauche['Delai'] = (promo_with_embauche['Date_Promot'] - promo_with_embauche['Date_Embauche']).dt.days / 365.25
    delai_promotion = promo_with_embauche['Delai'].mean()
else:
    delai_promotion = 0

services_risque = []
for service in actifs['Service'].unique():
    effectif_service = len(actifs[actifs['Service'] == service])
    departs_service = len(effectifs[(effectifs['Service'] == service) & (~effectifs['Date_Sortie'].isna())])
    turnover_service = (departs_service / effectif_service * 100) if effectif_service > 0 else 0
    
    sanctions_service = len(sanctions[sanctions['Service'] == service])
    taux_sanctions = (sanctions_service / effectif_service * 100) if effectif_service > 0 else 0
    
    absences = absenteisme[absenteisme['Service'] == service]['Taux_Absence'].mean() if service in absenteisme['Service'].values else 0
    
    score_risque = (turnover_service * 0.4) + (taux_sanctions * 0.3) + (absences * 0.3)
    niveau = "🟢 Faible" if score_risque < 10 else "🟡 Moyen" if score_risque < 20 else "🔴 Élevé"
    services_risque.append({
        'Service': service, 
        'Turnover (%)': round(turnover_service, 1),
        'Sanctions (%)': round(taux_sanctions, 1),
        'Absentéisme (%)': round(absences, 1),
        'Score Risque': round(score_risque, 1),
        'Niveau': niveau
    })

date_limite = datetime.now() + timedelta(days=30)
contrats_alertes = contrats_expiration[contrats_expiration['Date_Fin'] <= date_limite]

# ==================== SIDEBAR ====================
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <img src="https://raw.githubusercontent.com/souhaferjani-glitch/-RH-Dashboard/main/logo.png" 
         <div style="background: linear-gradient(135deg, #0ea5e9, #6366f1); width: 70px; height: 70px; border-radius: 1rem; margin: 0 auto; display: flex; align-items: center; justify-content: center;">
    <h3 style="color: #667eea; margin: 0;">La Pratique Electronique</h3>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown(f"**👤 {st.session_state.username}**")
st.sidebar.markdown("---")

service_filter = st.sidebar.multiselect("Service", actifs['Service'].unique(), default=actifs['Service'].unique())
categorie_filter = st.sidebar.multiselect("Catégorie", actifs['Categorie'].unique(), default=actifs['Categorie'].unique())
sexe_filter = st.sidebar.multiselect("Sexe", actifs['Sexe'].unique(), default=actifs['Sexe'].unique())

page = st.sidebar.radio("Navigation", [
    "🏠 Accueil", "📈 Mouvements", "⭐ Talents", "📋 Admin", "🎯 KPIs", "⚠️ Alertes"
])

st.sidebar.markdown("---")
if st.sidebar.button("📥 Exporter PDF", use_container_width=True):
    st.sidebar.success("Export en cours...")
if st.sidebar.button("🚪 Déconnexion", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()
st.sidebar.markdown("---")
st.sidebar.caption("© 2025 - La Pratique Electronique")
st.sidebar.caption("Version 2.0 - Business Intelligence")

# ==================== PAGE ACCUEIL ====================
if page == "🏠 Accueil":
    st.markdown('<div class="main-header"><h1>📊 Tableau de Bord RH</h1><p> - La Pratique Electronique - </p></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">👥 EFFECTIF TOTAL</div>
            <div class="kpi-value">{total}</div>
            <div class="trend-up">▲ +{total-15} cette année</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">📈 TAUX DE ROTATION</div>
            <div class="kpi-value">{turnover:.1f}%</div>
            <div class="trend-down">▼ Objectif: &lt;15%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">⭐ PROMOTIONS</div>
            <div class="kpi-value">{len(promotions)}</div>
            <div class="trend-up">▲ +33% vs 2023</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">🚪 DÉPARTS</div>
            <div class="kpi-value">{departs}</div>
            <div class="trend-down">▼ -2 vs 2023</div>
        </div>
        """, unsafe_allow_html=True)
# ========== GRAPHIQUE CENTRÉ ==========
    st.markdown("---")
    
    # Centrer le graphique avec des colonnes vides à gauche et à droite
    col_left, col_center, col_right = st.columns([1, 3, 1])
    
    with col_center:
        effectifs_filtres = actifs[actifs['Service'].isin(service_filter) & 
                                    actifs['Categorie'].isin(categorie_filter) & 
                                    actifs['Sexe'].isin(sexe_filter)]
        effectifs_service = effectifs_filtres.groupby('Service').size().reset_index(name='Effectif')
        fig = px.pie(effectifs_service, values='Effectif', names='Service', 
                     title="🏢 Répartition par Service",
                     hole=0.4, 
                     color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_traces(textposition='inside', textinfo='percent+label',
                          marker=dict(line=dict(color='white', width=2)))
        fig.update_layout(height=450, title_font_size=20, title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    st.markdown('<div class="section-title">📊 Démographie</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">👨‍💼 CADRES</div>
            <div class="kpi-value">{len(cadres)}</div>
            <div class="trend-up">{len(cadres)/total*100:.0f}% du total</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">👩 FEMMES</div>
            <div class="kpi-value">{len(actifs[actifs['Sexe']=='F'])}</div>
            <div class="trend-up">{len(actifs[actifs['Sexe']=='F'])/total*100:.0f}% du total</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">👨 HOMMES</div>
            <div class="kpi-value">{len(actifs[actifs['Sexe']=='H'])}</div>
            <div class="trend-up">{len(actifs[actifs['Sexe']=='H'])/total*100:.0f}% du total</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">📊 TAUX RÉPONSE</div>
            <div class="kpi-value">{questionnaires['Taux_Reponse'].mean():.0f}%</div>
            <div class="trend-up">Moyenne</div>
        </div>
        """, unsafe_allow_html=True)
# ==================== PAGE MOUVEMENTS ====================
elif page == "📈 Mouvements":
    st.markdown('<div class="main-header"><h1>📈 Mouvements du Personnel</h1><p>Entrées, sorties et turnover</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">📥 TOTAL ENTRÉES</div>
            <div class="kpi-value">{mouvements['Entrees'].sum()}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">📤 TOTAL SORTIES</div>
            <div class="kpi-value">{mouvements['Total_Sorties'].sum()}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">⚖️ SOLDE NET</div>
            <div class="kpi-value">{mouvements['Entrees'].sum() - mouvements['Total_Sorties'].sum()}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">🔄 TURNOVER</div>
            <div class="kpi-value">{turnover:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=mouvements['Mois'].dt.strftime('%b %Y'), y=mouvements['Entrees'], 
                         name='Entrées', marker_color='#667eea',
                         text=mouvements['Entrees'], textposition='outside'))
    fig.add_trace(go.Bar(x=mouvements['Mois'].dt.strftime('%b %Y'), y=mouvements['Total_Sorties'], 
                         name='Sorties', marker_color='#ff6b6b',
                         text=mouvements['Total_Sorties'], textposition='outside'))
    fig.update_layout(title='Entrées vs Sorties mensuelles', barmode='group', height=450)
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📊 Motifs de Sortie")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">📝 DÉMISSION</div>
            <div class="kpi-value">{mouvements['Sorties_Dem'].sum()}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">👴 RETRAITE</div>
            <div class="kpi-value">{mouvements['Sorties_Retr'].sum()}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">⚖️ LICENCIEMENT</div>
            <div class="kpi-value">{mouvements['Sorties_Lice'].sum()}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.subheader("📊 Turnover par Service")
    turnover_service = []
    for service in actifs['Service'].unique():
        effectif_service = len(actifs[actifs['Service'] == service])
        departs_service = len(effectifs[(effectifs['Service'] == service) & (~effectifs['Date_Sortie'].isna())])
        taux = (departs_service / effectif_service * 100) if effectif_service > 0 else 0
        turnover_service.append({'Service': service, 'Turnover (%)': round(taux, 1), 'Départs': departs_service})
    st.dataframe(pd.DataFrame(turnover_service), use_container_width=True)
    
    st.subheader("📈 Évolution Mensuelle des Effectifs")
    effectifs_par_mois = []
    for i in range(len(mouvements)):
        cumul_entrees = mouvements['Entrees'].iloc[:i+1].sum()
        cumul_sorties = mouvements['Total_Sorties'].iloc[:i+1].sum()
        effectifs_par_mois.append(cumul_entrees - cumul_sorties)
    fig = px.line(x=mouvements['Mois'].dt.strftime('%b %Y'), y=effectifs_par_mois,
                  markers=True, title="Évolution des effectifs")
    fig.update_layout(xaxis_title='Mois', yaxis_title='Effectif')
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📊 Taux de départ durant la première année")
    embauches_recentes = effectifs[effectifs['Date_Embauche'] > datetime.now() - timedelta(days=365)]
    if len(embauches_recentes) > 0:
        departs_recents = embauches_recentes['Date_Sortie'].notna().sum()
        taux_calcule = (departs_recents / len(embauches_recentes) * 100)
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-value">{taux_calcule:.1f}%</div>
            <div class="kpi-label">Objectif: &lt; 20%</div>
            <progress value="{taux_calcule}" max="100" style="width: 100%; height: 8px; border-radius: 4px;"></progress>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="modern-card">
            <div class="kpi-value">0.0%</div>
            <div class="kpi-label">Objectif: &lt; 20%</div>
            <p style="color: #64748b;">ℹ️ Pas d'embauches dans la dernière année</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== PAGE TALENTS ====================
elif page == "⭐ Talents":
    st.markdown('<div class="main-header"><h1>⭐ Gestion des Talents</h1><p>Promotions et mobilité interne</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">⭐ TOTAL PROMOTIONS</div>
            <div class="kpi-value">{len(promotions)}</div>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(promotions, use_container_width=True)
    
    with col2:
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">⏱️ DÉLAI MOYEN DE PROMOTION</div>
            <div class="kpi-value">{delai_promotion:.1f} ans</div>
            <div class="trend-up">Objectif: &lt; 3 ans</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">🔄 MOBILITÉ INTERNE</div>
            <div class="kpi-value">{len(promotions)} changements</div>
            <div class="kpi-label">Période: 2024-2025</div>
        </div>
        """, unsafe_allow_html=True)
    
    if len(promotions) > 0:
        promotions_par_annee = promotions.groupby(promotions['Date_Promot'].dt.year).size().reset_index(name='Nombre')
        promotions_par_annee.columns = ['Année', 'Nombre']
        fig = px.bar(promotions_par_annee, x='Année', y='Nombre', title="Promotions par année", text='Nombre')
        fig.update_traces(marker_color='pink', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

# ==================== PAGE ADMIN ====================
elif page == "📋 Admin":
    st.markdown('<div class="main-header"><h1>📋 Gestion Administrative</h1><p>Suivi des indicateurs administratifs RH</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📊 1. Taux de réponse aux questionnaires")
    st.caption("Formule: (Réponses / Diffusés) × 100 | Seuil de vigilance: 50%")
    
    taux_reponse_moyen = questionnaires['Taux_Reponse'].mean()
    if taux_reponse_moyen >= 75:
        statut_questionnaires = "🟢 Conforme"
    elif taux_reponse_moyen >= 50:
        statut_questionnaires = "🟡 Vigilance"
    else:
        statut_questionnaires = "🔴 Critique"
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">📋 TAUX MOYEN</div>
            <div class="kpi-value">{taux_reponse_moyen:.1f}%</div>
            <div>{statut_questionnaires}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">📊 QUESTIONNAIRES DIFFUSÉS</div>
            <div class="kpi-value">{questionnaires['Nb_Diffuses'].sum()}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">📝 RÉPONSES REÇUES</div>
            <div class="kpi-value">{questionnaires['Nb_Reponses'].sum()}</div>
        </div>
        """, unsafe_allow_html=True)
    
    fig = px.line(questionnaires, x='Periode', y='Taux_Reponse',
                  title="📈 Évolution du taux de participation",
                  markers=True, line_shape='spline')
    fig.update_traces(marker=dict(size=12, symbol='circle', color='#667eea'), line=dict(width=3, color='#667eea'))
    fig.add_hline(y=75, line_dash="dash", line_color="#ffd93d", annotation_text="Seuil vigilance 75%")
    fig.add_hline(y=50, line_dash="dash", line_color="#ff6b6b", annotation_text="Zone critique")
    fig.update_layout(height=450, yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📋 2. Entretiens annuels")
    st.caption("Formule: (Réalisés / Planifiés) × 100 | Seuil de vigilance: 80%")
    
    taux_entretien_moyen = entretiens['Taux_Realisation'].mean()
    if taux_entretien_moyen >= 80:
        statut_entretien = "🟢 Conforme"
    elif taux_entretien_moyen >= 60:
        statut_entretien = "🟡 Vigilance"
    else:
        statut_entretien = "🔴 Critique"
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">📊 TAUX DE RÉALISATION</div>
            <div class="kpi-value">{taux_entretien_moyen:.1f}%</div>
            <div>{statut_entretien}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">📋 ENTRETIENS PLANIFIÉS</div>
            <div class="kpi-value">{entretiens['Nb_Planifies'].sum()}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="modern-card">
            <div class="kpi-label">✅ ENTRETIENS RÉALISÉS</div>
            <div class="kpi-value">{entretiens['Nb_Realises'].sum()}</div>
        </div>
        """, unsafe_allow_html=True)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=entretiens['Annee'], y=entretiens['Taux_Realisation'],
                         text=entretiens['Taux_Realisation'], texttemplate='%{text:.1f}%',
                         marker_color='#667eea', marker_line_color='white', marker_line_width=2))
    fig.add_hline(y=80, line_dash="dash", line_color="#ff6b6b", annotation_text="🎯 Objectif 80%")
    fig.update_layout(title="Taux de réalisation des entretiens annuels", height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("⚠️ 3. Contrats arrivant à expiration (30 jours)")
    
    if len(contrats_alertes) > 0:
        st.markdown(f"""
        <div class="alert-critical">
            🚨 ALERTE CRITIQUE | {len(contrats_alertes)} contrat(s) expire(nt) dans les 30 jours
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(contrats_alertes, use_container_width=True)
    else:
        st.markdown("""
        <div class="success-card">
            ✅ AUCUNE ALERTE | Aucun contrat n'expire dans les 30 jours
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("⚖️ 4. Sanctions disciplinaires")
    
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(sanctions, use_container_width=True)
    with col2:
        sanctions_par_service = sanctions.groupby('Service').size().reset_index(name='Nb_Sanctions')
        fig = px.pie(sanctions_par_service, values='Nb_Sanctions', names='Service',
                     title="Sanctions par service", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📊 5. Taux d'absentéisme par service")
    
    fig = px.bar(absenteisme, x='Service', y='Taux_Absence', title="Taux d'absentéisme", text='Taux_Absence')
    fig.add_hline(y=8, line_dash="dash", line_color="#ef4444", annotation_text="Seuil d'alerte 8%")
    st.plotly_chart(fig, use_container_width=True)

# ==================== PAGE KPIs ====================
elif page == "🎯 KPIs":
    st.markdown('<div class="main-header"><h1>🎯 Indicateurs Stratégiques</h1><p>Performance RH et score de risque</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=qualite,
            title={'text': "Qualité des recrutements", 'font': {'size': 18}},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={'axis': {'range': [0, 100]},
                   'bar': {'color': "#51cf66"},
                   'steps': [{'range': [0, 50], 'color': '#ff6b6b'},
                             {'range': [50, 80], 'color': '#ffd93d'},
                             {'range': [80, 100], 'color': '#51cf66'}],
                   'threshold': {'value': 80, 'line': {'color': "red", 'width': 4}}}))
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=fuite_cadres,
            title={'text': "Fuite des compétences", 'font': {'size': 18}},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={'axis': {'range': [0, 30]},
                   'bar': {'color': "#ff6b6b"},
                   'steps': [{'range': [0, 5], 'color': '#51cf66'},
                             {'range': [5, 10], 'color': '#ffd93d'},
                             {'range': [10, 30], 'color': '#ff6b6b'}],
                   'threshold': {'value': 10, 'line': {'color': "red", 'width': 4}}}))
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("🎯 Score de risque par service")
    st.dataframe(pd.DataFrame(services_risque), use_container_width=True)
    
    fig = px.bar(pd.DataFrame(services_risque), x='Service', y='Score Risque', 
                 title="Score de risque par service",
                 color='Score Risque',
                 color_continuous_scale=['green', 'yellow', 'red'])
    st.plotly_chart(fig, use_container_width=True)

# ==================== PAGE ALERTES ====================
elif page == "⚠️ Alertes":
    st.markdown('<div class="main-header"><h1>⚠️ Système d\'Alertes</h1><p>Détection automatique des risques</p></div>', unsafe_allow_html=True)
    
    alertes = []
    if turnover > 15:
        alertes.append(("🔴 CRITIQUE", f"Turnover élevé: {turnover:.1f}% (Seuil > 15%)", "Plan de rétention urgent"))
    if fuite_cadres > 10:
        alertes.append(("🔴 CRITIQUE", f"Fuite des cadres: {fuite_cadres:.1f}% (Seuil > 10%)", "Entretiens de départ"))
    elif fuite_cadres > 5:
        alertes.append(("🟡 ATTENTION", f"Fuite des cadres: {fuite_cadres:.1f}% (Seuil > 5%)", "Surveiller les départs"))
    if qualite < 80:
        alertes.append(("🟡 ATTENTION", f"Qualité recrutements: {qualite:.1f}% (Seuil < 80%)", "Améliorer processus d'intégration"))
    if taux_depart_1ere > 20:
        alertes.append(("🔴 CRITIQUE", f"Départs 1ère année: {taux_depart_1ere:.1f}% (Seuil > 20%)", "Revoir programme d'intégration"))
    elif taux_depart_1ere > 15:
        alertes.append(("🟡 ATTENTION", f"Départs 1ère année: {taux_depart_1ere:.1f}% (Seuil > 15%)", "Améliorer onboarding"))
    if questionnaires['Taux_Reponse'].mean() < 50:
        alertes.append(("🟡 ATTENTION", f"Taux réponse questionnaires: {questionnaires['Taux_Reponse'].mean():.1f}% (Seuil < 50%)", "Relancer les enquêtes"))
    if entretiens['Taux_Realisation'].mean() < 80:
        alertes.append(("🟡 ATTENTION", f"Entretiens annuels: {entretiens['Taux_Realisation'].mean():.1f}% (Seuil < 80%)", "Planifier les entretiens manquants"))
    
    # Alertes services à risque
    for service in services_risque:
        if service['Score Risque'] > 15:
            alertes.append(("🔴 CRITIQUE", f"Service {service['Service']} à risque: Score {service['Score Risque']}", "Diagnostic approfondi"))
    
    # Contrats expiration
    if len(contrats_alertes) > 0:
        alertes.append(("🟡 ATTENTION", f"{len(contrats_alertes)} contrat(s) expire(nt) dans 30 jours", "Contacter les responsables"))
    
    if alertes:
        st.subheader(f"🚨 {len(alertes)} alerte(s) détectée(s)")
        for niveau, message, action in alertes:
            if "🔴" in niveau:
                st.markdown(f'<div class="alert-critical">🚨 {niveau}<br>{message}<br>📋 Action: {action}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="alert-warning">⚠️ {niveau}<br>{message}<br>📋 Action: {action}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="success-card">✅ Aucune alerte critique. Tous les indicateurs sont sous contrôle.</div>', unsafe_allow_html=True)
st.markdown("---")
st.caption("🎓 La Pratique Electronique | Projet PFE - Souha Ferjani | Business Intelligence ")
