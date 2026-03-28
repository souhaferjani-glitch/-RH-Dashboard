import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Tableau de Bord RH", page_icon="📊", layout="wide")

# Style CSS
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    padding: 20px;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
}
.metric-card {
    background-color: #f0f2f6;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}
.alert-danger {
    background-color: #f8d7da;
    border-left: 4px solid #dc3545;
    padding: 10px;
    margin: 10px 0;
    border-radius: 5px;
}
.alert-warning {
    background-color: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 10px;
    margin: 10px 0;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

# Chargement des données
@st.cache_data
def load_data():
    # Données effectifs
    effectifs = pd.DataFrame({
        'Matricule': ['EMP001', 'EMP002', 'EMP003', 'EMP004', 'EMP005', 'EMP006', 'EMP007', 'EMP008', 'EMP009', 'EMP010', 'EMP011', 'EMP012', 'EMP013', 'EMP014', 'EMP015'],
        'Date_Embauche': ['2020-01-01', '2021-06-15', '2022-03-10', '2023-09-05', '2021-01-20', '2023-07-01', '2022-11-15', '2020-05-10', '2024-02-01', '2021-08-15', '2023-03-20', '2022-12-05', '2021-07-10', '2023-09-01', '2022-04-15'],
        'Date_Sortie': ['', '2024-12-01', '', '', '2024-10-15', '', '2025-03-31', '', '', '', '2025-02-28', '', '', '', '2025-01-15'],
        'Motif_Sortie': ['', 'Démission', '', '', 'Retraite', '', 'Démission', '', '', '', 'Licenciement', '', '', '', 'Démission'],
        'Service': ['Commercial', 'RH', 'Technique', 'Commercial', 'Administration', 'Technique', 'Commercial', 'RH', 'Technique', 'Administration', 'Commercial', 'Technique', 'RH', 'Commercial', 'Technique'],
        'Categorie': ['Cadre', 'Non cadre', 'Cadre', 'Non cadre', 'Cadre', 'Non cadre', 'Cadre', 'Cadre', 'Non cadre', 'Non cadre', 'Non cadre', 'Cadre', 'Non cadre', 'Cadre', 'Non cadre'],
        'Sexe': ['H', 'F', 'H', 'F', 'H', 'F', 'F', 'F', 'H', 'F', 'H', 'H', 'F', 'H', 'F']
    })
    
    # Conversion des dates
    effectifs['Date_Embauche'] = pd.to_datetime(effectifs['Date_Embauche'])
    effectifs['Date_Sortie'] = pd.to_datetime(effectifs['Date_Sortie'], errors='coerce')
    
    # Mouvements mensuels
    mouvements = pd.DataFrame({
        'Mois': ['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01', '2024-05-01', '2024-06-01'],
        'Entrees': [2, 1, 3, 0, 2, 1],
        'Sorties_Dem': [1, 0, 2, 1, 0, 2],
        'Sorties_Retr': [0, 1, 0, 0, 0, 0],
        'Sorties_Lice': [0, 0, 1, 0, 0, 0]
    })
    mouvements['Mois'] = pd.to_datetime(mouvements['Mois'])
    
    # Promotions
    promotions = pd.DataFrame({
        'Matricule': ['EMP001', 'EMP003', 'EMP008', 'EMP012'],
        'Date_Promot': ['2025-01-01', '2024-03-15', '2024-12-01', '2024-06-10'],
        'Ancien_Grade': ['Commercial Senior', 'Technicien', 'Assistant RH', 'Ingénieur'],
        'Nouveau_Grade': ['Directeur Commercial', 'Technicien Principal', 'Responsable RH', 'Ingénieur Principal']
    })
    promotions['Date_Promot'] = pd.to_datetime(promotions['Date_Promot'])
    
    # Questionnaires
    questionnaires = pd.DataFrame({
        'Periode': ['01/2024', '02/2024', '03/2024', '04/2024', '05/2024', '06/2024'],
        'Taux_Reponse': [84, 76, 90, 80, 88, 78]
    })
    
    # Entretiens
    entretiens = pd.DataFrame({
        'Annee': [2023, 2024, 2025],
        'Taux_Realisation': [90, 86.4, 86.7]
    })
    
    # Sanctions
    sanctions = pd.DataFrame({
        'Date': ['2024-01-15', '2024-02-20', '2024-03-10', '2024-04-05', '2024-05-12'],
        'Service': ['Commercial', 'Technique', 'RH', 'Commercial', 'Technique'],
        'Type': ['Avertissement', 'Blâme', 'Avertissement', 'Mise à pied', 'Blâme']
    })
    sanctions['Date'] = pd.to_datetime(sanctions['Date'])
    
    return effectifs, mouvements, promotions, questionnaires, entretiens, sanctions

effectifs, mouvements, promotions, questionnaires, entretiens, sanctions = load_data()

# Calculs des KPI
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

# Sidebar
st.sidebar.title("📊 Tableau de Bord RH")
st.sidebar.markdown("### La Pratique Electronique")
st.sidebar.markdown("**Présenté par:** Souha Ferjani")
st.sidebar.markdown("**Projet PFE - Business Intelligence**")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigation", [
    "🏠 Vue d'ensemble",
    "📈 Mouvements & Turnover", 
    "⭐ Promotions",
    "📋 Gestion Administrative",
    "🎯 Indicateurs Stratégiques",
    "⚠️ Alertes"
])

# PAGE 1: Vue d'ensemble
if page == "🏠 Vue d'ensemble":
    st.markdown('<div class="main-header"><h1>📊 Tableau de Bord RH</h1><p>La Pratique Electronique</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("👥 Effectif Total", total)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("📈 Taux de Rotation", f"{turnover:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("⭐ Promotions", len(promotions))
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🚪 Départs", departs)
        st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(actifs, names='Service', title="Répartition par Service", hole=0.3)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(actifs, x='Categorie', title="Cadres vs Non-cadres", color='Categorie')
        st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("📋 Liste des employés"):
        st.dataframe(actifs[['Matricule', 'Service', 'Categorie', 'Sexe']], use_container_width=True)

# PAGE 2: Mouvements
elif page == "📈 Mouvements & Turnover":
    st.header("📈 Analyse des Mouvements")
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=mouvements['Mois'].dt.strftime('%b %Y'), y=mouvements['Entrees'], name='Entrées', marker_color='green'))
    fig.add_trace(go.Bar(x=mouvements['Mois'].dt.strftime('%b %Y'), y=mouvements['Total_Sorties'], name='Sorties', marker_color='red'))
    fig.update_layout(title='Entrées vs Sorties', barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Total Entrées", mouvements['Entrees'].sum())
    with col2: st.metric("Total Sorties", mouvements['Total_Sorties'].sum())
    with col3: st.metric("Taux Rotation", f"{turnover:.1f}%")

# PAGE 3: Promotions
elif page == "⭐ Promotions":
    st.header("⭐ Promotions Internes")
    st.dataframe(promotions, use_container_width=True)

# PAGE 4: Gestion Administrative
elif page == "📋 Gestion Administrative":
    st.header("📋 Gestion Administrative")
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(questionnaires, x='Periode', y='Taux_Reponse', title="Taux de réponse", markers=True)
        fig.add_hline(y=50, line_dash="dash", line_color="red")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(entretiens, x='Annee', y='Taux_Realisation', title="Entretiens annuels", text='Taux_Realisation')
        fig.add_hline(y=80, line_dash="dash", line_color="red")
        st.plotly_chart(fig, use_container_width=True)
    st.subheader("⚖️ Sanctions")
    st.dataframe(sanctions, use_container_width=True)

# PAGE 5: Indicateurs Stratégiques
elif page == "🎯 Indicateurs Stratégiques":
    st.header("🎯 Indicateurs Stratégiques")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("✅ Qualité recrutements", f"{qualite:.1f}%")
        st.progress(qualite/100)
    with col2:
        st.metric("💨 Fuite compétences", f"{fuite_cadres:.1f}%")
        st.progress(fuite_cadres/100)

# PAGE 6: Alertes
elif page == "⚠️ Alertes":
    st.header("⚠️ Alertes Automatiques")
    alertes = []
    if turnover > 15: alertes.append(("🔴 CRITIQUE", f"Turnover: {turnover:.1f}% > 15%"))
    if fuite_cadres > 10: alertes.append(("🔴 CRITIQUE", f"Fuite cadres: {fuite_cadres:.1f}% > 10%"))
    if qualite < 80: alertes.append(("🟡 ATTENTION", f"Qualité: {qualite:.1f}% < 80%"))
    
    if alertes:
        for type_a, msg in alertes:
            if "🔴" in type_a:
                st.error(msg)
            else:
                st.warning(msg)
    else:
        st.success("✅ Aucune alerte")

st.markdown("---")
st.caption("La Pratique Electronique | Projet PFE - Souha Ferjani | Business Intelligence")
