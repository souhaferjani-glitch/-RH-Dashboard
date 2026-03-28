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

# ==================== STYLE CSS AVANCÉ ====================
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
    
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .trend-up {
        color: #51cf66;
        font-weight: bold;
    }
    
    .trend-down {
        color: #ff6b6b;
        font-weight: bold;
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
        st.markdown('<h1 class="login-title">📊 RH Dashboard PRO</h1>', unsafe_allow_html=True)
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
        'Taux_Reponse': [84,76,90,80,88,78]
    })
    
    entretiens = pd.DataFrame({
        'Annee': [2023,2024,2025],
        'Taux_Realisation': [90,86.4,86.7]
    })
    
    sanctions = pd.DataFrame({
        'Date': ['2024-01-15','2024-02-20','2024-03-10','2024-04-05','2024-05-12'],
        'Service': ['Commercial','Technique','RH','Commercial','Technique'],
        'Type': ['Avertissement','Blâme','Avertissement','Mise à pied','Blâme']
    })
    sanctions['Date'] = pd.to_datetime(sanctions['Date'])
    
    return effectifs, mouvements, promotions, questionnaires, entretiens, sanctions

effectifs, mouvements, promotions, questionnaires, entretiens, sanctions = load_data()

# ==================== CALCULS AVANCÉS ====================
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

# Prévisions (tendance)
entrees_ma = mouvements['Entrees'].rolling(window=3, min_periods=1).mean()
sorties_ma = mouvements['Total_Sorties'].rolling(window=3, min_periods=1).mean()
prevision_entrees = entrees_ma.iloc[-1] * 1.05
prevision_sorties = sorties_ma.iloc[-1] * 0.95

# ==================== SIDEBAR AVANCÉE ====================
st.sidebar.title("🎯 RH Dashboard ")
st.sidebar.markdown("### La Pratique Electronique")
st.sidebar.markdown(f"**👤 {st.session_state.username}**")
st.sidebar.markdown("---")


# Période
periode = st.sidebar.selectbox("📅 Période", ["6 mois", "Année", "2 ans"], index=0)

# Export
if st.sidebar.button("📥 Exporter PDF", use_container_width=True):
    st.sidebar.success("Export en cours...")

if st.sidebar.button("🚪 Déconnexion", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()
    
# Navigation
page = st.sidebar.radio("Navigation", [
    "🏠 Acceuil", "📈 Analytics", "⭐ Talents", "📋 Admin", "🎯 KPIs", "⚠️ Alertes"
])
st.sidebar.markdown("---")
st.sidebar.caption("© 2025 - La Pratique Electronique")
st.sidebar.caption("Version 2.0 - Business Intelligence")


# ==================== PAGE Acceuil ====================
if page == "🏠 Acceuil":
    st.markdown('<div class="main-header"><h1>📊 Tableau de Bord RH</h1><p>La Pratique Electronique - Version PRO</p></div>', unsafe_allow_html=True)
    
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
    
    # Graphiques avancés
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(actifs, names='Service', title="🏢 Répartition par Service",
                     hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_traces(textposition='inside', textinfo='percent+label',
                          marker=dict(line=dict(color='white', width=2)))
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Graphique 3D
        fig = px.scatter_3d(actifs, x=actifs.groupby('Service').size().index,
                            y=actifs.groupby('Service').size().values,
                            z=range(len(actifs.groupby('Service').size())),
                            title="Distribution 3D des Services",
                            color=actifs.groupby('Service').size().index)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# ==================== PAGE ANALYTICS ====================
elif page == "📈 Analytics":
    st.markdown('<div class="main-header"><h1>📈 Analyse Avancée</h1><p>Visualisation des tendances</p></div>', unsafe_allow_html=True)
    
    # Graphique interactif
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=mouvements['Mois'], y=mouvements['Entrees'],
                             mode='lines+markers', name='Entrées',
                             line=dict(color='#51cf66', width=3),
                             marker=dict(size=10, symbol='circle')))
    fig.add_trace(go.Scatter(x=mouvements['Mois'], y=mouvements['Total_Sorties'],
                             mode='lines+markers', name='Sorties',
                             line=dict(color='#ff6b6b', width=3),
                             marker=dict(size=10, symbol='circle')))
    fig.add_trace(go.Scatter(x=mouvements['Mois'], y=entrees_ma,
                             mode='lines', name='Tendance Entrées',
                             line=dict(color='#51cf66', width=2, dash='dash')))
    fig.add_trace(go.Scatter(x=mouvements['Mois'], y=sorties_ma,
                             mode='lines', name='Tendance Sorties',
                             line=dict(color='#ff6b6b', width=2, dash='dash')))
    fig.update_layout(title='Évolution des mouvements avec tendances',
                      xaxis_title='Mois', yaxis_title='Nombre',
                      hovermode='x unified', height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Prévisions
    st.subheader("🔮 Prévisions")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📥 Prévision Entrées", f"{prevision_entrees:.0f}", "+5%")
    with col2:
        st.metric("📤 Prévision Sorties", f"{prevision_sorties:.0f}", "-5%")

# ==================== PAGE TALENTS ====================
elif page == "⭐ Talents":
    st.markdown('<div class="main-header"><h1>⭐ Gestion des Talents</h1><p>Promotions et mobilité interne</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 Historique des promotions")
        st.dataframe(promotions, use_container_width=True)
    
    with col2:
        st.subheader("📊 Statistiques")
        fig = go.Figure(go.Funnel(
            y=['Cadres', 'Non-cadres', 'Promotions'],
            x=[len(cadres), len(actifs)-len(cadres), len(promotions)],
            textinfo="value+percent initial"))
        fig.update_layout(title="Pyramide des talents")
        st.plotly_chart(fig, use_container_width=True)

# ==================== PAGE ADMIN ====================
elif page == "📋 Admin":
    st.markdown('<div class="main-header"><h1>📋 Administration</h1><p>Suivi des indicateurs</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(questionnaires, x='Periode', y='Taux_Reponse',
                      title="Taux de réponse", markers=True,
                      line_shape='spline')
        fig.add_hline(y=50, line_dash="dash", line_color="red")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(entretiens, x='Annee', y='Taux_Realisation',
                     title="Entretiens annuels", text='Taux_Realisation',
                     color='Taux_Realisation',
                     color_continuous_scale=['red','yellow','green'])
        fig.add_hline(y=80, line_dash="dash", line_color="red")
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("⚖️ Sanctions disciplinaires")
    st.dataframe(sanctions, use_container_width=True)

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

# ==================== PAGE ALERTES ====================
elif page == "⚠️ Alertes":
    st.markdown('<div class="main-header"><h1>⚠️ Système d\'Alertes</h1><p>Détection automatique des risques</p></div>', unsafe_allow_html=True)
    
    alertes = []
    if turnover > 15:
        alertes.append(("CRITIQUE", f"Turnover élevé: {turnover:.1f}%", "Plan de rétention urgent"))
    if fuite_cadres > 10:
        alertes.append(("CRITIQUE", f"Fuite des cadres: {fuite_cadres:.1f}%", "Entretiens de départ"))
    if qualite < 80:
        alertes.append(("ATTENTION", f"Qualité recrutements: {qualite:.1f}%", "Améliorer processus"))
    
    if alertes:
        for niveau, message, action in alertes:
            if "CRITIQUE" in niveau:
                st.markdown(f'<div class="alert-critical">🚨 {niveau} | {message}<br>📋 Action: {action}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="alert-warning">⚠️ {niveau} | {message}<br>📋 Action: {action}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="success-card">✅ Aucune alerte critique. Tous les indicateurs sont sous contrôle.</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("🎓 La Pratique Electronique | Projet PFE - Souha Ferjani | Business Intelligence PRO")
