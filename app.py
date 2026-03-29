import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
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
    
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        margin-top: 0.5rem;
        font-weight: 500;
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
    
    .trend-up {
        color: #51cf66;
        font-weight: bold;
    }
    
    .trend-down {
        color: #ff6b6b;
        font-weight: bold;
    }
    
    .center-chart {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
    }
    
    .kpi-container {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== LOGIN - DESIGN SPLIT (LOGO GAUCHE / FORMULAIRE DROITE) ====================
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
    
    /* Fond avec animation */
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
    
    /* Container principal */
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        padding: 40px;
    }
    
    /* Carte split - Logo à gauche, formulaire à droite */
    .login-split-card {
        display: flex;
        max-width: 900px;
        width: 100%;
        background: white;
        border-radius: 32px;
        overflow: hidden;
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.3);
    }
    
    /* Partie gauche - Logo et Branding */
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
    
    .brand-description {
        font-size: 12px;
        color: rgba(255,255,255,0.7);
        line-height: 1.5;
    }
    
    /* Partie droite - Formulaire */
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
    
    /* Form Group */
    .form-group {
        margin-bottom: 20px;
    }
    
    .form-label {
        display: block;
        font-size: 13px;
        font-weight: 600;
        color: #334155;
        margin-bottom: 8px;
    }
    
    /* Inputs */
    .stTextInput > div > div > input {
        width: 100%;
        padding: 12px 16px;
        font-size: 14px;
        border: 1.5px solid #e2e8f0;
        border-radius: 12px;
        background: #fafbfc;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        background: white;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #cbd5e1;
        font-size: 13px;
    }
    
    /* Forgot Password */
    .forgot-section {
        text-align: right;
        margin-bottom: 24px;
    }
    
    .forgot-link {
        font-size: 12px;
        color: #667eea;
        text-decoration: none;
        font-weight: 500;
    }
    
    .forgot-link:hover {
        text-decoration: underline;
    }
    
    /* Login Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        font-size: 14px;
        font-weight: 600;
        border-radius: 40px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px -5px rgba(102, 126, 234, 0.4);
    }
    
    /* Footer */
    .footer-section {
        margin-top: 32px;
        padding-top: 20px;
        border-top: 1px solid #edf2f7;
        text-align: center;
    }
    
    .footer-text {
        font-size: 11px;
        color: #94a3b8;
    }
    
    .footer-text a {
        color: #667eea;
        text-decoration: none;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    .stAppDeployButton {display: none;}
    .stStatusWidget {display: none;}
    .viewerBadge_container__1QSob {display: none;}
    
    /* Responsive */
    @media (max-width: 768px) {
        .login-split-card {
            flex-direction: column;
            max-width: 400px;
        }
        .login-left {
            padding: 32px;
        }
        .logo-large {
            width: 80px;
            height: 80px;
        }
        .brand-title {
            font-size: 22px;
        }
    }
    </style>
    
    <div class="login-container">
        <div class="login-split-card">
            <!-- Partie Gauche - Logo et Branding -->
            <div class="login-left">
                <img src="https://raw.githubusercontent.com/souhaferjani-glitch/-RH-Dashboard/main/logo.png" 
                     class="logo-large" 
                     onerror="this.style.display='none'; this.parentElement.innerHTML='<div style=\'width:120px;height:120px;background:rgba(255,255,255,0.2);border-radius:50%;display:inline-flex;align-items:center;justify-content:center;margin-bottom:24px;border:4px solid rgba(255,255,255,0.3)\'><span style=\'font-size:55px;color:white\'>📊</span></div>'">
                <div class="brand-title">RH Dashboard</div>
                <div class="brand-subtitle">La Pratique Electronique</div>
                <div class="brand-description">
                    Sous-traitance électronique<br>
                    Solutions innovantes depuis 2005
                </div>
            </div>
            
            <!-- Partie Droite - Formulaire de connexion -->
            <div class="login-right">
                <div class="welcome-title">Bienvenue</div>
    """, unsafe_allow_html=True)
    
    # Champs de connexion
    st.markdown('<div class="form-group"><label class="form-label">Username</label></div>', unsafe_allow_html=True)
    username = st.text_input("", placeholder="Rhadmin", key="login_username", label_visibility="collapsed")
    
    st.markdown('<div class="form-group"><label class="form-label">Password</label></div>', unsafe_allow_html=True)
    password = st.text_input("", placeholder="••••••••", type="password", key="login_password", label_visibility="collapsed")
    
    # Forgot Password
    st.markdown('<div class="forgot-section"><a href="#" class="forgot-link">Forgot Password?</a></div>', unsafe_allow_html=True)
    
    # Bouton Login
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Login", use_container_width=True):
            if username in USERS and USERS[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
    
    # Footer
    st.markdown("""
                <div class="footer-section">
                    <div class="footer-text">
                        Need help? <a href="#">Contact Support</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    return False

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
    
    # Données absentéisme
    absenteisme = pd.DataFrame({
        'Mois': ['01/2024','02/2024','03/2024','04/2024','05/2024','06/2024'],
        'Service': ['Commercial','Technique','RH','Commercial','Technique','RH'],
        'Taux_Absence': [5.2,6.8,3.5,6.1,7.2,4.2]
    })
    
    # Contrats arrivant à expiration
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

# ==================== NOUVEAUX INDICATEURS ====================

# 1. Taux de départ 1ère année
embauches_an_dernier = effectifs[effectifs['Date_Embauche'] > datetime.now() - timedelta(days=365)]
departs_1ere_annee = len(embauches_an_dernier[~embauches_an_dernier['Date_Sortie'].isna()])
if len(embauches_an_dernier) > 0:
    taux_depart_1ere = (departs_1ere_annee / len(embauches_an_dernier) * 100)
else:
    taux_depart_1ere = 0

# 2. Délai moyen de promotion
if len(promotions) > 0:
    promo_with_embauche = promotions.merge(effectifs[['Matricule', 'Date_Embauche']], 
                                           left_on='Matricule', right_on='Matricule')
    promo_with_embauche['Delai'] = (promo_with_embauche['Date_Promot'] - promo_with_embauche['Date_Embauche']).dt.days / 365.25
    delai_promotion = promo_with_embauche['Delai'].mean()
else:
    delai_promotion = 0

# 3. Mobilité interne (changements de poste)
mobilite_interne = len(promotions)

# 4. Évolution mensuelle des effectifs
effectifs_par_mois = []
for i in range(len(mouvements)):
    cumul_entrees = mouvements['Entrees'].iloc[:i+1].sum()
    cumul_sorties = mouvements['Total_Sorties'].iloc[:i+1].sum()
    effectifs_par_mois.append(cumul_entrees - cumul_sorties)

# 5. Sanctions par service
sanctions_par_service = sanctions.groupby('Service').size().reset_index(name='Nb_Sanctions')

# 6. Score de risque par service
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

# 7. Contrats arrivant à expiration (30 jours)
date_limite = datetime.now() + timedelta(days=30)
contrats_alertes = contrats_expiration[contrats_expiration['Date_Fin'] <= date_limite]

# Prévisions
entrees_ma = mouvements['Entrees'].rolling(window=3, min_periods=1).mean()
sorties_ma = mouvements['Total_Sorties'].rolling(window=3, min_periods=1).mean()
prevision_entrees = entrees_ma.iloc[-1] * 1.05 if len(entrees_ma) > 0 else 0
prevision_sorties = sorties_ma.iloc[-1] * 0.95 if len(sorties_ma) > 0 else 0

# ==================== SIDEBAR AVEC LOGO LOCAL ====================
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <img src="https://raw.githubusercontent.com/souhaferjani-glitch/-RH-Dashboard/main/logo.png" 
         style="width: 80px; height: 80px; border-radius: 50%; margin-bottom: 10px; border: 3px solid #667eea;">
    <h3 style="color: #667eea; margin: 0;">La Pratique Electronique</h3>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown(f"**👤 {st.session_state.username}**")
st.sidebar.markdown("---")
# Filtres
st.sidebar.subheader("📊 Filtres")
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
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{total}</div>
            <div class="metric-label">👥 Effectif Total</div>
            <div class="trend-up">+{total-15} cette année</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{turnover:.1f}%</div>
            <div class="metric-label">📈 Taux de Rotation</div>
            <div class="trend-down">Objectif: <15%</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{len(promotions)}</div>
            <div class="metric-label">⭐ Promotions</div>
            <div class="trend-up">+33% vs 2023</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{departs}</div>
            <div class="metric-label">🚪 Départs</div>
            <div class="trend-down">-2 vs 2023</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # GRAPHIQUE PRINCIPAL AU CENTRE
    st.markdown('<div class="center-chart">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
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
        fig.update_layout(showlegend=False, height=450)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Indicateurs supplémentaires
    st.markdown("---")
    st.subheader("📊 Indicateurs Complémentaires")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Cadres", len(cadres), delta=f"{len(cadres)/total*100:.0f}%")
    with col2:
        st.metric("👩 Femmes", len(actifs[actifs['Sexe']=='F']), delta=f"{len(actifs[actifs['Sexe']=='F'])/total*100:.0f}%")
    with col3:
        st.metric("👨 Hommes", len(actifs[actifs['Sexe']=='H']), delta=f"{len(actifs[actifs['Sexe']=='H'])/total*100:.0f}%")
    with col4:
        st.metric("📊 Taux réponse", f"{questionnaires['Taux_Reponse'].mean():.0f}%", delta="Moyenne")

# ==================== PAGE MOUVEMENTS ====================
elif page == "📈 Mouvements":
    st.markdown('<div class="main-header"><h1>📈 Mouvements du Personnel</h1><p>Entrées, sorties et turnover</p></div>', unsafe_allow_html=True)
    
    # Indicateurs de flux
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write("📥 **Total Entrées**")
        st.write(f"### {mouvements['Entrees'].sum()}")
    with col2:
        st.write("📤 **Total Sorties**")
        st.write(f"### {mouvements['Total_Sorties'].sum()}")
    with col3:
        st.write("⚖️ **Solde Net**")
        st.write(f"### {mouvements['Entrees'].sum() - mouvements['Total_Sorties'].sum()}")
    with col4:
        st.write("🔄 **Turnover**")
        st.write(f"### {turnover:.1f}%")
    
    # Graphique Entrées/Sorties
    fig = go.Figure()
    fig.add_trace(go.Bar(x=mouvements['Mois'].dt.strftime('%b %Y'), y=mouvements['Entrees'], 
                         name='Entrées', marker_color='#51cf66',
                         text=mouvements['Entrees'], textposition='outside'))
    fig.add_trace(go.Bar(x=mouvements['Mois'].dt.strftime('%b %Y'), y=mouvements['Total_Sorties'], 
                         name='Sorties', marker_color='#ff6b6b',
                         text=mouvements['Total_Sorties'], textposition='outside'))
    fig.update_layout(title='Entrées vs Sorties mensuelles', barmode='group', height=450)
    st.plotly_chart(fig, use_container_width=True)
    
    # Motifs de sortie
    st.subheader("📊 Motifs de Sortie")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("📝 **Démission**")
        st.write(f"### {mouvements['Sorties_Dem'].sum()}")
    with col2:
        st.write("👴 **Retraite**")
        st.write(f"### {mouvements['Sorties_Retr'].sum()}")
    with col3:
        st.write("⚖️ **Licenciement**")
        st.write(f"### {mouvements['Sorties_Lice'].sum()}")
    
    # Turnover par service
    st.subheader("📊 Turnover par Service")
    turnover_service = []
    for service in actifs['Service'].unique():
        effectif_service = len(actifs[actifs['Service'] == service])
        departs_service = len(effectifs[(effectifs['Service'] == service) & (~effectifs['Date_Sortie'].isna())])
        taux = (departs_service / effectif_service * 100) if effectif_service > 0 else 0
        turnover_service.append({'Service': service, 'Turnover (%)': round(taux, 1), 'Départs': departs_service})
    st.dataframe(pd.DataFrame(turnover_service), use_container_width=True)
    
    # Évolution mensuelle des effectifs
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
    
    # Taux de départ 1ère année - Version SIMPLE sans st.metric
    st.subheader("📊 Taux de départ durant la première année")
    
    # Calcul direct
    embauches_recentes = effectifs[effectifs['Date_Embauche'] > datetime.now() - timedelta(days=365)]
    if len(embauches_recentes) > 0:
        departs_recents = embauches_recentes['Date_Sortie'].notna().sum()
        taux_calcule = (departs_recents / len(embauches_recentes) * 100)
        st.write(f"### {taux_calcule:.1f}%")
        st.write("**Objectif:** < 20%")
        st.progress(taux_calcule/100)
    else:
        st.write("### 0.0%")
        st.write("**Objectif:** < 20%")
        st.info("ℹ️ Pas d'embauches dans la dernière année")
# ==================== PAGE TALENTS ====================
elif page == "⭐ Talents":
    st.markdown('<div class="main-header"><h1>⭐ Gestion des Talents</h1><p>Promotions et mobilité interne</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 Historique des promotions")
        st.dataframe(promotions, use_container_width=True)
        st.write("📊 **Total promotions**")
        st.write(f"### {len(promotions)}")
    
    with col2:
        st.subheader("⏱️ Délai moyen de promotion")
        # Calcul direct
        if len(promotions) > 0:
            promo_temp = promotions.merge(effectifs[['Matricule', 'Date_Embauche']], 
                                          left_on='Matricule', right_on='Matricule')
            promo_temp['Delai'] = (promo_temp['Date_Promot'] - promo_temp['Date_Embauche']).dt.days / 365.25
            delai_calc = promo_temp['Delai'].mean()
            st.write(f"### {delai_calc:.1f} ans")
            st.write("**Objectif:** < 3 ans")
        else:
            st.write("### Non disponible")
            st.write("**Objectif:** < 3 ans")
        
        st.subheader("🔄 Mobilité interne")
        st.write(f"### {len(promotions)} changements")
        st.write("**Période:** 2024-2025")
    
    if len(promotions) > 0:
        promotions_par_annee = promotions.groupby(promotions['Date_Promot'].dt.year).size().reset_index(name='Nombre')
        promotions_par_annee.columns = ['Année', 'Nombre']
        fig = px.bar(promotions_par_annee, x='Année', y='Nombre', 
                     title="Promotions par année", text='Nombre')
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
# ==================== PAGE ADMIN - VERSION PROFESSIONNELLE ====================
elif page == "📋 Admin":
    st.markdown('<div class="main-header"><h1>📋 Gestion Administrative</h1><p>Suivi des indicateurs administratifs RH</p></div>', unsafe_allow_html=True)
    
    # ==================== INDICATEUR 1: TAUX DE RÉPONSE QUESTIONNAIRES ====================
    st.markdown("---")
    st.subheader("📊 1. Taux de réponse aux questionnaires")
    st.caption("Formule: (Réponses / Diffusés) × 100 | Seuil de vigilance: 50%")
    
    # Calcul du statut
    taux_reponse_moyen = questionnaires['Taux_Reponse'].mean()
    if taux_reponse_moyen >= 75:
        statut_questionnaires = "🟢 Conforme"
        couleur_questionnaires = "#51cf66"
    elif taux_reponse_moyen >= 50:
        statut_questionnaires = "🟡 Vigilance"
        couleur_questionnaires = "#ffd93d"
    else:
        statut_questionnaires = "🔴 Critique"
        couleur_questionnaires = "#ff6b6b"
    
    # Métriques
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {couleur_questionnaires};">{taux_reponse_moyen:.1f}%</div>
            <div class="metric-label">📋 Taux moyen</div>
            <div class="metric-label" style="color: {couleur_questionnaires}; font-size: 11px;">{statut_questionnaires}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #667eea;">{questionnaires['Nb_Diffuses'].sum()}</div>
            <div class="metric-label">📊 Total questionnaires diffusés</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #667eea;">{questionnaires['Nb_Reponses'].sum()}</div>
            <div class="metric-label">📝 Total réponses reçues</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphique d'évolution
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        fig = px.line(questionnaires, x='Periode', y='Taux_Reponse',
                      title="📈 Évolution du taux de participation",
                      markers=True, line_shape='spline')
        fig.update_traces(marker=dict(size=12, symbol='circle', color='#667eea'), line=dict(width=3, color='#667eea'))
        
        # Zone d'alerte colorée
        fig.add_hrect(y0=0, y1=50, line_width=0, fillcolor="#ff6b6b", opacity=0.1, annotation_text="Zone critique", annotation_position="bottom left")
        fig.add_hline(y=50, line_dash="dash", line_color="#ff6b6b", line_width=2)
        fig.add_hline(y=75, line_dash="dash", line_color="#ffd93d", line_width=2, annotation_text="Seuil vigilance 75%", annotation_position="bottom right")
        
        fig.update_layout(height=450, xaxis_title="Période", yaxis_title="Taux de réponse (%)",
                          yaxis_range=[0, 100], plot_bgcolor='white', title_font_size=18, title_x=0.5)
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#ecf0f1')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#ecf0f1')
        st.plotly_chart(fig, use_container_width=True)
    
    # ==================== INDICATEUR 2: ENTRETIENS ANNUELS ====================
    st.markdown("---")
    st.subheader("📋 2. Entretiens annuels")
    st.caption("Formule: (Réalisés / Planifiés) × 100 | Seuil de vigilance: 80%")
    
    taux_entretien_moyen = entretiens['Taux_Realisation'].mean()
    if taux_entretien_moyen >= 90:
        statut_entretien = "🟢 Excellence"
        couleur_entretien = "#51cf66"
    elif taux_entretien_moyen >= 80:
        statut_entretien = "🟢 Conforme"
        couleur_entretien = "#51cf66"
    elif taux_entretien_moyen >= 60:
        statut_entretien = "🟡 Vigilance"
        couleur_entretien = "#ffd93d"
    else:
        statut_entretien = "🔴 Critique"
        couleur_entretien = "#ff6b6b"
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {couleur_entretien};">{taux_entretien_moyen:.1f}%</div>
            <div class="metric-label">📊 Taux moyen de réalisation</div>
            <div class="metric-label" style="color: {couleur_entretien}; font-size: 11px;">{statut_entretien}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #667eea;">{entretiens['Nb_Planifies'].sum()}</div>
            <div class="metric-label">📋 Total entretiens planifiés</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #667eea;">{entretiens['Nb_Realises'].sum()}</div>
            <div class="metric-label">✅ Total entretiens réalisés</div>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        # Couleurs basées sur le seuil
        colors = ['#ff6b6b' if x < 80 else '#51cf66' for x in entretiens['Taux_Realisation']]
        fig = go.Figure()
        fig.add_trace(go.Bar(x=entretiens['Annee'], y=entretiens['Taux_Realisation'],
                             text=entretiens['Taux_Realisation'], textposition='outside',
                             texttemplate='%{text:.1f}%', marker_color=colors,
                             marker_line_color='white', marker_line_width=2))
        fig.add_hline(y=80, line_dash="dash", line_color="#ff6b6b", line_width=2,
                      annotation_text="🎯 Objectif 80%", annotation_position="bottom right")
        fig.update_layout(title="📊 Taux de réalisation des entretiens annuels", height=450,
                          xaxis_title="Année", yaxis_title="Taux de réalisation (%)",
                          yaxis_range=[0, 100], plot_bgcolor='white', title_font_size=18, title_x=0.5)
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#ecf0f1')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#ecf0f1')
        st.plotly_chart(fig, use_container_width=True)
    
    # ==================== INDICATEUR 3: CONTRATS ARRIVANT À EXPIRATION ====================
    st.markdown("---")
    st.subheader("⚠️ 3. Contrats arrivant à expiration (30 jours)")
    st.caption("Liste des contrats dont la date de fin est ≤ J+30")
    
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
    
    # ==================== INDICATEUR 4: SANCTIONS DISCIPLINAIRES ====================
    st.markdown("---")
    st.subheader("⚖️ 4. Sanctions disciplinaires")
    st.caption("Suivi des sanctions par service et par type")
    
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(sanctions, use_container_width=True)
    with col2:
        sanctions_par_service = sanctions.groupby('Service').size().reset_index(name='Nb_Sanctions')
        
        # Statut par service
        max_sanctions = sanctions_par_service['Nb_Sanctions'].max()
        sanctions_par_service['Statut'] = sanctions_par_service['Nb_Sanctions'].apply(
            lambda x: '🔴 Critique' if x == max_sanctions and x > 2 else '🟡 Vigilance' if x > 1 else '🟢 Normal'
        )
        
        fig = px.pie(sanctions_par_service, values='Nb_Sanctions', names='Service',
                     title="Répartition des sanctions par service",
                     hole=0.4, color_discrete_sequence=['#667eea', '#764ba2', '#51cf66', '#ff6b6b', '#ffd93d'])
        fig.update_traces(textposition='inside', textinfo='percent+label',
                          marker=dict(line=dict(color='white', width=2)))
        fig.update_layout(height=400, title_font_size=18, title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)
    
    # ==================== INDICATEUR 5: TAUX D'ABSENTÉISME ====================
    st.markdown("---")
    st.subheader("📊 5. Taux d'absentéisme par service")
    st.caption("Formule: (Nombre de jours d'absence / Effectif) × 100 | Seuil d'alerte: 8%")
    
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        # Couleurs: Vert (<5%), Jaune (5-8%), Rouge (>8%)
        colors_abs = ['#51cf66' if x < 5 else '#ffd93d' if x < 8 else '#ff6b6b' for x in absenteisme['Taux_Absence']]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=absenteisme['Service'], y=absenteisme['Taux_Absence'],
                             text=absenteisme['Taux_Absence'], textposition='outside',
                             texttemplate='%{text:.1f}%', 
                             marker_color=colors_abs,
                             marker_line_color='white', marker_line_width=2))
        
        # Zone rouge au-dessus du seuil
        fig.add_hrect(y0=8, y1=100, line_width=0, fillcolor="#ff6b6b", opacity=0.15)
        fig.add_hline(y=8, line_dash="dash", line_color="#ff6b6b", line_width=3,
                      annotation_text="🔴 SEUIL D'ALERTE 8%", annotation_position="top right",
                      annotation_font_size=12, annotation_font_color="#ff6b6b")
        
        fig.update_layout(title="📈 Taux d'absentéisme par service", height=450,
                          xaxis_title="Service", yaxis_title="Taux d'absentéisme (%)",
                          plot_bgcolor='white', title_font_size=18, title_x=0.5)
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#ecf0f1')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#ecf0f1')
        st.plotly_chart(fig, use_container_width=True)
    
    # Ajouter un résumé des services en alerte
    services_alerte = absenteisme[absenteisme['Taux_Absence'] > 8]['Service'].tolist()
    if services_alerte:
        st.markdown(f"""
        <div class="alert-warning">
            ⚠️ VIGILANCE | Service(s) concerné(s) par l'absentéisme: {', '.join(services_alerte)}
        </div>
        """, unsafe_allow_html=True)
    
    # ==================== RÉCAPITULATIF PROFESSIONNEL ====================
    st.markdown("---")
    st.subheader("📊 Synthèse des indicateurs administratifs")
    
    recap_data = {
        "Indicateur": [
            "Taux de réponse questionnaires",
            "Entretiens annuels",
            "Contrats expiration J+30",
            "Sanctions disciplinaires",
            "Taux d'absentéisme"
        ],
        "Valeur mesurée": [
            f"{taux_reponse_moyen:.1f}%",
            f"{taux_entretien_moyen:.1f}%",
            f"{len(contrats_alertes)} contrat(s)",
            f"{len(sanctions)} sanction(s)",
            f"{absenteisme['Taux_Absence'].mean():.1f}%"
        ],
        "Seuil de référence": [
            "75%",
            "80%",
            "0",
            "-",
            "8%"
        ],
        "Statut": [
            statut_questionnaires,
            statut_entretien,
            "🔴 Critique" if len(contrats_alertes) > 0 else "🟢 Conforme",
            "🟡 À surveiller" if len(sanctions) > 3 else "🟢 Normal",
            "🔴 Critique" if absenteisme['Taux_Absence'].mean() > 8 else "🟡 Vigilance" if absenteisme['Taux_Absence'].mean() > 5 else "🟢 Conforme"
        ],
        "Action recommandée": [
            "Maintenir" if taux_reponse_moyen >= 75 else "Améliorer la communication" if taux_reponse_moyen >= 50 else "Campagne de sensibilisation",
            "Maintenir" if taux_entretien_moyen >= 80 else "Planifier les entretiens manquants",
            "Contacter les responsables" if len(contrats_alertes) > 0 else "Aucune action",
            "Analyse des causes" if len(sanctions) > 3 else "Aucune action",
            "Plan d'action RH" if absenteisme['Taux_Absence'].mean() > 8 else "Surveillance"
        ]
    }
    st.dataframe(pd.DataFrame(recap_data), use_container_width=True, hide_index=True)
# ==================== PAGE KPIs ====================
elif page == "🎯 KPIs":
    st.markdown('<div class="main-header"><h1>🎯 Indicateurs Stratégiques</h1><p>Performance RH</p></div>', unsafe_allow_html=True)
    
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
                   'threshold': {'line': {'color': "red", 'width': 4}, 'value': 80}}))
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
                   'threshold': {'line': {'color': "red", 'width': 4}, 'value': 10}}))
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Score de risque par service
    st.subheader("🎯 Score de risque par service")
    st.dataframe(pd.DataFrame(services_risque), use_container_width=True)
    
    # Graphique des scores
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
st.caption("🎓 La Pratique Electronique | Projet PFE - Souha Ferjani | Business Intelligence")
