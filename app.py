import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="RH Dashboard", page_icon="📊", layout="wide")

# ==================== CONFIGURATION LOGIN ====================
USERS = {
    "Rhadmin": "admin123",
    
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

def show_login():
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 30px;
        background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        text-align: center;
    }
    .login-title {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 30px;
        font-size: 32px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<h1 class="login-title">📊 RH Dashboard</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color:#666;">La Pratique Electronique</p>', unsafe_allow_html=True)
        
        username = st.text_input("👤 Nom d'utilisateur", key="login_username")
        password = st.text_input("🔒 Mot de passe", type="password", key="login_password")
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            login_btn = st.button("Se connecter", use_container_width=True)
        
        if login_btn:
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

# ==================== STYLE CSS AVANCÉ ====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.main-header {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    padding: 25px;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.metric-card {
    background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    border: 1px solid #e9ecef;
    transition: transform 0.3s;
}
.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}

.metric-value {
    font-size: 32px;
    font-weight: 700;
    color: #1e3c72;
}

.metric-label {
    font-size: 14px;
    color: #6c757d;
    margin-top: 5px;
}

.alert-danger {
    background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
    border-left: 4px solid #dc3545;
    padding: 15px;
    margin: 10px 0;
    border-radius: 10px;
    font-weight: 500;
}
.alert-warning {
    background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%);
    border-left: 4px solid #ffc107;
    padding: 15px;
    margin: 10px 0;
    border-radius: 10px;
    font-weight: 500;
}
.success-card {
    background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
    border-left: 4px solid #28a745;
    padding: 15px;
    margin: 10px 0;
    border-radius: 10px;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

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

# ==================== CALCULS KPI ====================
actifs = effectifs[effectifs['Date_Sortie'].isna()]
total = len(actifs)
departs = len(effectifs[~effectifs['Date_Sortie'].isna()])
turnover = (departs / len(effectifs) * 100) if len(effectifs) > 0 else 0

cadres = effectifs[effectifs['Categorie'] == 'Cadre']
departs_cadres = len(cadres[~cadres['Date_Sortie'].isna()])
fuite_cadres = (departs_cadres / len(cadres) * 100) if len(cadres) > 0 else 0

recents = effectifs[effectifs['Date_Embauche'] > datetime.now() - pd.Timedelta(days=365)]
qualite = (len(recents[recents['Date_Sortie'].isna()]) / len(recents) * 100) if len(recents) > 0 else 0

mouvements['Total_Sorties'] = mouvements['Sorties_Dem'] + mouvements['Sorties_Retr'] + mouvements['Sorties_Lice']

# ==================== SIDEBAR ====================
st.sidebar.title("📊 RH Dashboard")
st.sidebar.markdown("### La Pratique Electronique")
st.sidebar.markdown(f"**👤 {st.session_state.username}**")
st.sidebar.markdown("---")

if st.sidebar.button("🚪 Déconnexion", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", [
    "🏠 Accueil", "📈 Mouvements", "⭐ Promotions", "📋 Admin", "🎯 Stratégique", "⚠️ Alertes"
])

# ==================== PAGE ACCUEIL ====================
if page == "🏠 Accueil":
    st.markdown('<div class="main-header"><h1>📊 Tableau de Bord RH</h1><p>La Pratique Electronique</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{total}</div><div class="metric-label">👥 Effectif Total</div></div>', unsafe_allow_html=True)
    with col2:
        color = "green" if turnover < 15 else "orange" if turnover < 25 else "red"
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:{color}">{turnover:.1f}%</div><div class="metric-label">📈 Taux Rotation</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(promotions)}</div><div class="metric-label">⭐ Promotions</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{departs}</div><div class="metric-label">🚪 Départs</div></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(actifs, names='Service', title="🏢 Répartition par Service", 
                     hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_traces(textposition='inside', textinfo='percent+label', 
                          marker=dict(line=dict(color='white', width=2)))
        fig.update_layout(showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(actifs.groupby('Categorie').size().reset_index(name='nb'), 
                     x='Categorie', y='nb', color='Categorie',
                     title="👥 Cadres vs Non-cadres",
                     color_discrete_sequence=['#1e3c72', '#2a5298'])
        fig.update_traces(textposition='outside', texttemplate='%{y}')
        fig.update_layout(showlegend=False, yaxis_title="Effectif")
        st.plotly_chart(fig, use_container_width=True)

# ==================== PAGE MOUVEMENTS (VERSION AVANCÉE) ====================
elif page == "📈 Mouvements":
    st.markdown('<div class="main-header"><h1>📈 Analyse des Mouvements</h1><p>Suivi des entrées et sorties</p></div>', unsafe_allow_html=True)
    
    # Graphique en barres avec couleurs professionnelles
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=mouvements['Mois'].dt.strftime('%b %Y'),
        y=mouvements['Entrees'],
        name='Entrées',
        marker_color='#2ecc71',
        marker_line_color='white',
        marker_line_width=2,
        text=mouvements['Entrees'],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Entrées: %{y}<extra></extra>'
    ))
    fig.add_trace(go.Bar(
        x=mouvements['Mois'].dt.strftime('%b %Y'),
        y=mouvements['Total_Sorties'],
        name='Sorties',
        marker_color='#e74c3c',
        marker_line_color='white',
        marker_line_width=2,
        text=mouvements['Total_Sorties'],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Sorties: %{y}<extra></extra>'
    ))
    fig.update_layout(
        title=dict(text='📊 Évolution des entrées et sorties', font=dict(size=20)),
        barmode='group',
        xaxis_title="Mois",
        yaxis_title="Nombre",
        plot_bgcolor='white',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#ecf0f1')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#ecf0f1')
    st.plotly_chart(fig, use_container_width=True)
    
    # Cartes de statistiques
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:#2ecc71">{mouvements["Entrees"].sum()}</div><div class="metric-label">📥 Total Entrées</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:#e74c3c">{mouvements["Total_Sorties"].sum()}</div><div class="metric-label">📤 Total Sorties</div></div>', unsafe_allow_html=True)
    with col3:
        solde = mouvements["Entrees"].sum() - mouvements["Total_Sorties"].sum()
        color = "#2ecc71" if solde > 0 else "#e74c3c"
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:{color}">{solde:+d}</div><div class="metric-label">⚖️ Solde Net</div></div>', unsafe_allow_html=True)
    
    # Graphique en courbes pour la tendance
    st.markdown("---")
    st.subheader("📈 Tendance mensuelle")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=mouvements['Mois'].dt.strftime('%b %Y'),
        y=mouvements['Entrees'],
        name='Entrées',
        mode='lines+markers',
        line=dict(color='#2ecc71', width=3),
        marker=dict(size=10, symbol='circle'),
        fill='tozeroy',
        fillcolor='rgba(46, 204, 113, 0.2)'
    ))
    fig2.add_trace(go.Scatter(
        x=mouvements['Mois'].dt.strftime('%b %Y'),
        y=mouvements['Total_Sorties'],
        name='Sorties',
        mode='lines+markers',
        line=dict(color='#e74c3c', width=3),
        marker=dict(size=10, symbol='circle'),
        fill='tozeroy',
        fillcolor='rgba(231, 76, 60, 0.2)'
    ))
    fig2.update_layout(plot_bgcolor='white', hovermode='x unified')
    fig2.update_xaxes(showgrid=True, gridcolor='#ecf0f1')
    fig2.update_yaxes(showgrid=True, gridcolor='#ecf0f1')
    st.plotly_chart(fig2, use_container_width=True)

# ==================== PAGE PROMOTIONS ====================
elif page == "⭐ Promotions":
    st.markdown('<div class="main-header"><h1>⭐ Promotions Internes</h1><p>Évolution des carrières</p></div>', unsafe_allow_html=True)
    st.dataframe(promotions, use_container_width=True)

# ==================== PAGE ADMIN ====================
elif page == "📋 Admin":
    st.markdown('<div class="main-header"><h1>📋 Gestion Administrative</h1><p>Suivi des indicateurs RH</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(questionnaires, x='Periode', y='Taux_Reponse', 
                      title="📊 Taux de réponse aux questionnaires",
                      markers=True, line_shape='spline')
        fig.add_hline(y=50, line_dash="dash", line_color="red", 
                      annotation_text="Seuil alerte 50%")
        fig.update_layout(plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(entretiens, x='Annee', y='Taux_Realisation', 
                     title="📋 Entretiens annuels",
                     text='Taux_Realisation', color='Taux_Realisation',
                     color_continuous_scale=['red', 'yellow', 'green'])
        fig.add_hline(y=80, line_dash="dash", line_color="red", 
                      annotation_text="Objectif 80%")
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("⚖️ Sanctions disciplinaires")
    st.dataframe(sanctions, use_container_width=True)

# ==================== PAGE STRATÉGIQUE ====================
elif page == "🎯 Stratégique":
    st.markdown('<div class="main-header"><h1>🎯 Indicateurs Stratégiques</h1><p>Pilotage RH avancé</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=qualite,
            title={'text': "Qualité des recrutements"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={'axis': {'range': [0, 100]},
                   'bar': {'color': "#2ecc71"},
                   'steps': [{'range': [0, 50], 'color': "#f8d7da"},
                             {'range': [50, 80], 'color': "#fff3cd"},
                             {'range': [80, 100], 'color': "#d4edda"}],
                   'threshold': {'line': {'color': "red", 'width': 4}, 'value': 80}}))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=fuite_cadres,
            title={'text': "Fuite des compétences"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={'axis': {'range': [0, 30]},
                   'bar': {'color': "#e74c3c"},
                   'steps': [{'range': [0, 5], 'color': "#d4edda"},
                             {'range': [5, 10], 'color': "#fff3cd"},
                             {'range': [10, 30], 'color': "#f8d7da"}],
                   'threshold': {'line': {'color': "red", 'width': 4}, 'value': 10}}))
        st.plotly_chart(fig, use_container_width=True)

# ==================== PAGE ALERTES ====================
elif page == "⚠️ Alertes":
    st.markdown('<div class="main-header"><h1>⚠️ Alertes Automatiques</h1><p>Détection des risques RH</p></div>', unsafe_allow_html=True)
    
    alertes = []
    if turnover > 15:
        alertes.append(("🔴 CRITIQUE", f"Turnover élevé: {turnover:.1f}%", "Seuil > 15%"))
    if fuite_cadres > 10:
        alertes.append(("🔴 CRITIQUE", f"Fuite des cadres: {fuite_cadres:.1f}%", "Seuil > 10%"))
    if qualite < 80:
        alertes.append(("🟡 ATTENTION", f"Qualité recrutements: {qualite:.1f}%", "Seuil < 80%"))
    
    if alertes:
        for type_a, msg, seuil in alertes:
            if "🔴" in type_a:
                st.markdown(f'<div class="alert-danger"><strong>{type_a}</strong><br>{msg}<br><span style="font-size:12px">{seuil}</span></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="alert-warning"><strong>{type_a}</strong><br>{msg}<br><span style="font-size:12px">{seuil}</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="success-card">✅ Aucune alerte critique détectée. Tous les indicateurs sont dans les normes.</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("🎓 La Pratique Electronique | Projet PFE - Souha Ferjani | Business Intelligence")
