import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import time
import warnings
import base64
import os
import json

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="RH Dashboard - La Pratique Electronique",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== SESSION STATE POUR LA CONFIGURATION ====================
if "config" not in st.session_state:
    st.session_state.config = {
        "langue": "Français",
        "theme": "Clair",
        "primary_color": "#667eea",
        "font": "Inter",
        "chart_size": 450,
        "alert_turnover": True,
        "alert_contrats": True,
        "rapport_mensuel": False,
        "notifications": True
    }

# ==================== FONCTION POUR CHARGER LE LOGO ====================
def get_logo_base64():
    logo_paths = ["logo.png", "logo.PNG", "assets/logo.png", "images/logo.png"]
    for path in logo_paths:
        if os.path.exists(path):
            with open(path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    return None

LOGO_BASE64 = get_logo_base64()

# ==================== FONCTION POUR APPLIQUER LA CONFIGURATION ====================
def apply_config():
    # Appliquer la police
    if st.session_state.config["font"] != "Inter":
        st.markdown(f"""
        <style>
            * {{ font-family: '{st.session_state.config["font"]}', sans-serif !important; }}
        </style>
        """, unsafe_allow_html=True)
    
    # Appliquer la couleur principale
    primary = st.session_state.config["primary_color"]
    st.markdown(f"""
    <style>
        .main-header {{ background: linear-gradient(135deg, {primary} 0%, #764ba2 100%); }}
        .kpi-value {{ background: linear-gradient(135deg, {primary} 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .stButton > button {{ background: linear-gradient(135deg, {primary} 0%, #764ba2 100%); }}
        .section-title {{ border-bottom-color: {primary}; }}
    </style>
    """, unsafe_allow_html=True)
    
    # Appliquer le thème
    if st.session_state.config["theme"] == "Sombre":
        st.markdown("""
        <style>
            .stApp { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); }
            .modern-card { background: rgba(255,255,255,0.08); backdrop-filter: blur(10px); border-color: rgba(0,255,255,0.2); }
            .modern-card:hover { border-color: rgba(0,255,255,0.6); }
            .kpi-label { color: rgba(255,255,255,0.7); }
            [data-testid="stSidebar"] { background: rgba(0,0,0,0.4); backdrop-filter: blur(15px); border-right: 1px solid rgba(0,255,255,0.3); }
            [data-testid="stSidebar"] * { color: rgba(255,255,255,0.9) !important; }
            .config-section { background: rgba(255,255,255,0.08); border-color: rgba(0,255,255,0.2); }
            .config-title { color: #00ffff; border-bottom-color: #00ffff; }
            .glass-header { background: rgba(0,0,0,0.3); backdrop-filter: blur(10px); border-color: rgba(0,255,255,0.2); }
            .glass-header h1 { color: #00ffff; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%); }
            .modern-card { background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); border-color: #eef2f6; }
            .kpi-label { color: #6c757d; }
            [data-testid="stSidebar"] { background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%); border-right: 1px solid rgba(102,126,234,0.1); }
            [data-testid="stSidebar"] * { color: #1e293b !important; }
            .config-section { background: white; border-color: #eef2f6; }
            .config-title { color: #0f172a; border-bottom-color: #e2e8f0; }
            .glass-header { background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); border-color: rgba(255,255,255,0.18); }
            .glass-header h1 { color: #0f172a; }
        </style>
        """, unsafe_allow_html=True)

# ==================== STYLE CSS ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
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
    
    .modern-card {
        border-radius: 1.5rem;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        text-align: center;
        height: 100%;
    }
    
    .modern-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.15);
    }
    
    .kpi-value {
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0.5rem 0;
    }
    
    .kpi-label {
        font-size: 0.85rem;
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
        display: inline-block;
    }
    
    .stButton > button {
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
    
    .glass-header {
        padding: 2rem;
        border-radius: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
        text-align: center;
    }
    
    .config-section {
        border-radius: 1.5rem;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .config-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid;
    }
</style>
""", unsafe_allow_html=True)

# Appliquer la config
apply_config()

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
st.sidebar.markdown(f"""
<div style="text-align: center; margin-bottom: 20px;">
    <img src="https://raw.githubusercontent.com/souhaferjani-glitch/-RH-Dashboard/main/logo.png" 
         style="width: 80px; height: 80px; border-radius: 50%; margin-bottom: 10px; border: 3px solid {st.session_state.config['primary_color']};">
    <h3 style="color: {st.session_state.config['primary_color']}; margin: 0;">La Pratique Electronique</h3>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown(f"**👤 {st.session_state.username}**")
st.sidebar.markdown("---")

service_filter = st.sidebar.multiselect("Service", actifs['Service'].unique(), default=actifs['Service'].unique())
categorie_filter = st.sidebar.multiselect("Catégorie", actifs['Categorie'].unique(), default=actifs['Categorie'].unique())
sexe_filter = st.sidebar.multiselect("Sexe", actifs['Sexe'].unique(), default=actifs['Sexe'].unique())

page = st.sidebar.radio("Navigation", [
    "🏠 Accueil", "📈 Mouvements", "⭐ Talents", "📋 Admin", "🎯 KPIs", "⚠️ Alertes", "⚙️ Configuration"
])

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Déconnexion", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()
st.sidebar.markdown("---")
st.sidebar.caption("© 2025 - La Pratique Electronique")
st.sidebar.caption("Version 3.0 - Configuration")

# ==================== PAGE ACCUEIL ====================
if page == "🏠 Accueil":
    st.markdown(f'<div class="main-header"><h1>📊 Tableau de Bord RH</h1><p> - La Pratique Electronique - </p></div>', unsafe_allow_html=True)
    
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
    
    st.markdown("---")
    
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
        fig.update_layout(height=st.session_state.config["chart_size"], title_font_size=20, title_x=0.5)
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
                         name='Entrées', marker_color=st.session_state.config["primary_color"],
                         text=mouvements['Entrees'], textposition='outside'))
    fig.add_trace(go.Bar(x=mouvements['Mois'].dt.strftime('%b %Y'), y=mouvements['Total_Sorties'], 
                         name='Sorties', marker_color='#ff6b6
