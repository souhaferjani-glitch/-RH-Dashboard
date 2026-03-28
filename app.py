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
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
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
    
    .trend-up {
        color: #51cf66;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .trend-down {
        color: #ff6b6b;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    /* Navigation horizontale */
    .nav-container {
        background: white;
        border-radius: 50px;
        padding: 0.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    
    .nav-button {
        padding: 0.7rem 1.8rem;
        border-radius: 40px;
        font-weight: 500;
        transition: all 0.3s ease;
        cursor: pointer;
        background: transparent;
        border: none;
        color: #6c757d;
        font-size: 0.9rem;
    }
    
    .nav-button.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);
    }
    
    .nav-button:hover:not(.active) {
        background: #f8f9fa;
        color: #667eea;
    }
    
    .logout-btn {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #ff6b6b;
        color: white;
        border: none;
        border-radius: 40px;
        padding: 0.5rem 1rem;
        font-size: 0.8rem;
        cursor: pointer;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        z-index: 1000;
    }
    
    .logout-btn:hover {
        background: #ee5a5a;
        transform: scale(1.05);
    }
    
    .center-chart {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# ==================== LOGIN ====================
USERS = {"admin": "admin123", "souha": "souha2025", "rh": "rh123"}

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

# ==================== NAVIGATION HORIZONTALE ====================
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
nav_options = ["🏠 Acceuil", "📈 Analytics", "⭐ Talents", "📋 Admin", "🎯 KPIs", "⚠️ Alertes"]
selected_nav = st.radio("", nav_options, horizontal=True, label_visibility="collapsed")

# Bouton déconnexion en bas à droite
st.markdown(f'<button class="logout-btn" onclick="window.location.reload()">🚪 Déconnexion</button>', unsafe_allow_html=True)

# Pour la déconnexion via Python
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🚪 Déconnexion", key="logout_btn", help="Se déconnecter"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# ==================== HEADER ====================
st.markdown('<div class="main-header"><h1>📊 Tableau de Bord RH</h1><p>La Pratique Electronique - Version PRO</p></div>', unsafe_allow_html=True)

# ==================== KPIS ====================
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

# ==================== GRAPHIQUE PRINCIPAL AU CENTRE ====================
st.markdown('<div class="center-chart">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    effectifs_service = actifs.groupby('Service').size().reset_index(name='Effectif')
    fig = px.pie(effectifs_service, values='Effectif', names='Service', 
                 title="🏢 Répartition par Service",
                 hole=0.4, 
                 color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_traces(textposition='inside', textinfo='percent+label',
                      marker=dict(line=dict(color='white', width=2)))
    fig.update_layout(showlegend=False, height=450)
    st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ==================== CONTENU SELON NAVIGATION ====================
if selected_nav == "📈 Analytics":
    st.markdown("---")
    st.subheader("📈 Analyse des Mouvements")
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=mouvements['Mois'].dt.strftime('%b %Y'), 
                         y=mouvements['Entrees'], 
                         name='Entrées', 
                         marker_color='#51cf66',
                         text=mouvements['Entrees'],
                         textposition='outside'))
    fig.add_trace(go.Bar(x=mouvements['Mois'].dt.strftime('%b %Y'), 
                         y=mouvements['Total_Sorties'], 
                         name='Sorties', 
                         marker_color='#ff6b6b',
                         text=mouvements['Total_Sorties'],
                         textposition='outside'))
    fig.update_layout(title='Entrées vs Sorties mensuelles', 
                      barmode='group',
                      height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Entrées", mouvements['Entrees'].sum())
    with col2:
        st.metric("Total Sorties", mouvements['Total_Sorties'].sum())
    with col3:
        solde = mouvements['Entrees'].sum() - mouvements['Total_Sorties'].sum()
        st.metric("Solde Net", f"{solde:+d}")

elif selected_nav == "⭐ Talents":
    st.markdown("---")
    st.subheader("⭐ Promotions Internes")
    st.dataframe(promotions, use_container_width=True)
    
    if len(promotions) > 0:
        promotions_par_annee = promotions.groupby(promotions['Date_Promot'].dt.year).size().reset_index(name='Nombre')
        promotions_par_annee.columns = ['Année', 'Nombre']
        fig = px.bar(promotions_par_annee, x='Année', y='Nombre', 
                     title="Promotions par année", text='Nombre')
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

elif selected_nav == "📋 Admin":
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(questionnaires, x='Periode', y='Taux_Reponse', 
                      title="Taux de réponse aux questionnaires", 
                      markers=True, line_shape='spline')
        fig.add_hline(y=50, line_dash="dash", line_color="red", 
                      annotation_text="Seuil alerte 50%")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(entretiens, x='Annee', y='Taux_Realisation', 
                     title="Entretiens annuels", 
                     text='Taux_Realisation',
                     color='Taux_Realisation',
                     color_continuous_scale=['red','yellow','green'])
        fig.add_hline(y=80, line_dash="dash", line_color="red", 
                      annotation_text="Objectif 80%")
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("⚖️ Sanctions disciplinaires")
    st.dataframe(sanctions, use_container_width=True)

elif selected_nav == "🎯 KPIs":
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Qualité des recrutements")
        st.metric(f"{qualite:.1f}%", delta="Objectif >80%")
        st.progress(qualite/100)
    
    with col2:
        st.subheader("💨 Fuite des compétences")
        st.metric(f"{fuite_cadres:.1f}%", delta="Objectif <10%")
        st.progress(fuite_cadres/100)
    
    st.markdown("---")
    st.subheader("🎯 Score de risque par service")
    risques = []
    for s in actifs['Service'].unique():
        effectif = len(actifs[actifs['Service'] == s])
        departs_s = len(effectifs[(effectifs['Service'] == s) & (~effectifs['Date_Sortie'].isna())])
        turnover_s = (departs_s / effectif * 100) if effectif > 0 else 0
        niveau = "🟢 Faible" if turnover_s < 10 else "🟡 Moyen" if turnover_s < 20 else "🔴 Élevé"
        risques.append({'Service': s, 'Turnover': round(turnover_s, 1), 'Niveau': niveau})
    
    st.dataframe(pd.DataFrame(risques), use_container_width=True)

elif selected_nav == "⚠️ Alertes":
    st.markdown("---")
    st.subheader("⚠️ Alertes Automatiques")
    
    alertes = []
    if turnover > 15:
        alertes.append(("🔴 CRITIQUE", f"Turnover élevé: {turnover:.1f}%", "Seuil > 15%"))
    if fuite_cadres > 10:
        alertes.append(("🔴 CRITIQUE", f"Fuite des cadres: {fuite_cadres:.1f}%", "Seuil > 10%"))
    if qualite < 80:
        alertes.append(("🟡 ATTENTION", f"Qualité recrutements: {qualite:.1f}%", "Seuil < 80%"))
    if entretiens['Taux_Realisation'].iloc[-1] < 80:
        alertes.append(("🟡 ATTENTION", f"Entretiens annuels: {entretiens['Taux_Realisation'].iloc[-1]}%", "Seuil < 80%"))
    
    if alertes:
        for type_a, msg, seuil in alertes:
            if "🔴" in type_a:
                st.error(f"{type_a} | {msg} | {seuil}")
            else:
                st.warning(f"{type_a} | {msg} | {seuil}")
    else:
        st.success("✅ Aucune alerte critique détectée")

st.markdown("---")
st.caption("🎓 La Pratique Electronique | Projet PFE - Souha Ferjani | Business Intelligence PRO")
