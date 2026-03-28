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

# ==================== LOGIN ====================
USERS = {"Rhadmin": "admin123"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

def show_login():
    st.markdown("""
    <style>
    .login-container {
        max-width: 450px;
        margin: 100px auto;
        padding: 40px;
        background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        text-align: center;
        animation: fadeIn 0.5s ease-in;
    }
    .login-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<h1 class="login-title">📊 RH Dashboard </h1>', unsafe_allow_html=True)
        st.markdown('<p style="color:#6c757d; margin-bottom:2rem;">La Pratique Electronique</p>', unsafe_allow_html=True)
        
        username = st.text_input("👤 Nom d'utilisateur", key="login_username")
        password = st.text_input("🔒 Mot de passe", type="password", key="login_password")
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.button("Se connecter", use_container_width=True):
                if username in USERS and USERS[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("❌ Identifiants incorrects")
        
        st.markdown('</div>', unsafe_allow_html=True)
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
    <h3 style="color: #667eea; margin: 0;">La Pratique</h3>
    <h3 style="color: #764ba2; margin: 0;">Electronique</h3>
    <p style="color: #6c757d; font-size: 11px; margin-top: 5px;">Sous-traitance électronique</p>
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

if st.sidebar.button("📥 Exporter PDF", use_container_width=True):
    st.sidebar.success("Export en cours...")

if st.sidebar.button("🚪 Déconnexion", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

page = st.sidebar.radio("Navigation", [
    "🏠 Accueil", "📈 Mouvements", "⭐ Talents", "📋 Admin", "🎯 KPIs", "⚠️ Alertes"
])
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
# ==================== PAGE ADMIN ====================
elif page == "📋 Admin":
    st.markdown('<div class="main-header"><h1>📋 Administration</h1><p>Suivi des indicateurs</p></div>', unsafe_allow_html=True)
    
    # Taux de réponse questionnaires
    st.subheader("📊 Taux de réponse aux questionnaires")
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(questionnaires, x='Periode', y='Taux_Reponse',
                      title="Évolution du taux de participation", markers=True,
                      line_shape='spline')
        fig.add_hline(y=50, line_dash="dash", line_color="red", annotation_text="Seuil alerte 50%")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.metric("📋 Taux moyen", f"{questionnaires['Taux_Reponse'].mean():.1f}%")
        st.metric("📊 Nb questionnaires diffusés", questionnaires['Nb_Diffuses'].sum())
        st.metric("📝 Nb réponses reçues", questionnaires['Nb_Reponses'].sum())
    
    # Entretiens annuels
    st.subheader("📋 Entretiens annuels")
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(entretiens, x='Annee', y='Taux_Realisation',
                     title="Taux de réalisation", text='Taux_Realisation',
                     color='Taux_Realisation',
                     color_continuous_scale=['red','yellow','green'])
        fig.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="Objectif 80%")
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.metric("📊 Taux moyen", f"{entretiens['Taux_Realisation'].mean():.1f}%")
        st.metric("📋 Entretiens planifiés", entretiens['Nb_Planifies'].sum())
        st.metric("✅ Entretiens réalisés", entretiens['Nb_Realises'].sum())
    
    # Contrats arrivant à expiration
    st.subheader("⚠️ Contrats arrivant à expiration (30 jours)")
    if len(contrats_alertes) > 0:
        st.warning(f"{len(contrats_alertes)} contrat(s) expire(nt) dans les 30 jours")
        st.dataframe(contrats_alertes, use_container_width=True)
    else:
        st.success("✅ Aucun contrat n'expire dans les 30 jours")
    
    # Sanctions disciplinaires
    st.subheader("⚖️ Sanctions disciplinaires")
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(sanctions, use_container_width=True)
    with col2:
        st.subheader("📊 Sanctions par service")
        st.dataframe(sanctions_par_service, use_container_width=True)
    
    # Absentéisme
    st.subheader("📊 Taux d'absentéisme par service")
    fig = px.bar(absenteisme, x='Service', y='Taux_Absence', 
                 title="Taux d'absentéisme",
                 color='Taux_Absence',
                 color_continuous_scale=['green','yellow','red'])
    fig.add_hline(y=8, line_dash="dash", line_color="red", annotation_text="Seuil alerte 8%")
    st.plotly_chart(fig, use_container_width=True)

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
st.caption("🎓 La Pratique Electronique | Projet PFE - Souha Ferjani | Business Intelligence PRO")
