# Cellule: Créer app.py (VERSION FINALE PROFESSIONNELLE)
import os

os.makedirs('/content/RH_Dashboard', exist_ok=True)

app_content = '''import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Tableau de Bord RH - La Pratique Electronique", page_icon="📊", layout="wide")

st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    padding: 25px;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
.main-header h1 {
    margin: 0;
    font-size: 28px;
    font-weight: 600;
}
.main-header p {
    margin: 8px 0 0 0;
    font-size: 14px;
    opacity: 0.9;
}
.metric-card {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
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
    background: #f8d7da;
    border-left: 4px solid #dc3545;
    padding: 15px;
    margin: 10px 0;
    border-radius: 10px;
}
.alert-warning {
    background: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 15px;
    margin: 10px 0;
    border-radius: 10px;
}
.success-card {
    background: #d4edda;
    border-left: 4px solid #28a745;
    padding: 15px;
    margin: 10px 0;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(\'\'\'
<div class="main-header">
    <h1>📊 Tableau de Bord RH</h1>
    <p>La Pratique Electronique | Projet PFE - Souha Ferjani | Business Intelligence</p>
</div>
\'\'\', unsafe_allow_html=True)

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

st.sidebar.title("🏢 La Pratique Electronique")
st.sidebar.markdown("---")
st.sidebar.markdown("**Présenté par:** Souha Ferjani")
st.sidebar.markdown("**Projet PFE - Business Intelligence**")
st.sidebar.markdown("**MiT-Nabeul**")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigation", [
    "🏠 Accueil",
    "📈 Mouvements", 
    "⭐ Promotions",
    "📋 Administration",
    "🎯 Stratégique",
    "⚠️ Alertes"
])

if page == "🏠 Accueil":
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Effectif Total", total)
    with col2:
        st.metric("📈 Taux de Rotation", f"{turnover:.1f}%")
    with col3:
        st.metric("⭐ Promotions", len(promotions))
    with col4:
        st.metric("🚪 Départs", departs)
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(actifs, names='Service', title="Répartition par Service", hole=0.3)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(actifs, x='Categorie', title="Cadres vs Non-cadres", color='Categorie')
        st.plotly_chart(fig, use_container_width=True)

elif page == "📈 Mouvements":
    st.header("📈 Analyse des Mouvements")
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=mouvements['Mois'].dt.strftime('%b %Y'), y=mouvements['Entrees'], name='Entrées', marker_color='#2ecc71', text=mouvements['Entrees'], textposition='outside'))
    fig.add_trace(go.Bar(x=mouvements['Mois'].dt.strftime('%b %Y'), y=mouvements['Total_Sorties'], name='Sorties', marker_color='#e74c3c', text=mouvements['Total_Sorties'], textposition='outside'))
    fig.update_layout(title='Entrées vs Sorties mensuelles', barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📥 Total Entrées", mouvements['Entrees'].sum())
    with col2:
        st.metric("📤 Total Sorties", mouvements['Total_Sorties'].sum())
    with col3:
        st.metric("⚖️ Solde Net", mouvements['Entrees'].sum() - mouvements['Total_Sorties'].sum())

elif page == "⭐ Promotions":
    st.header("⭐ Promotions Internes")
    st.dataframe(promotions, use_container_width=True)

elif page == "📋 Administration":
    st.header("📋 Gestion Administrative")
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(questionnaires, x='Periode', y='Taux_Reponse', title="Taux de réponse aux questionnaires", markers=True)
        fig.add_hline(y=50, line_dash="dash", line_color="red", annotation_text="Seuil 50%")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(entretiens, x='Annee', y='Taux_Realisation', title="Entretiens annuels", text='Taux_Realisation')
        fig.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="Objectif 80%")
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("⚖️ Sanctions disciplinaires")
    st.dataframe(sanctions, use_container_width=True)

elif page == "🎯 Stratégique":
    st.header("🎯 Indicateurs Stratégiques")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("✅ Qualité des recrutements", f"{qualite:.1f}%")
        st.progress(qualite/100)
    with col2:
        st.metric("💨 Fuite des compétences", f"{fuite_cadres:.1f}%")
        st.progress(fuite_cadres/100)

elif page == "⚠️ Alertes":
    st.header("⚠️ Alertes Automatiques")
    
    alertes = []
    if turnover > 15:
        alertes.append(("🔴 CRITIQUE", f"Turnover élevé: {turnover:.1f}% > 15%"))
    if fuite_cadres > 10:
        alertes.append(("🔴 CRITIQUE", f"Fuite des cadres: {fuite_cadres:.1f}% > 10%"))
    if qualite < 80:
        alertes.append(("🟡 ATTENTION", f"Qualité recrutements: {qualite:.1f}% < 80%"))
    
    if alertes:
        for type_alerte, message in alertes:
            if "🔴" in type_alerte:
                st.error(message)
            else:
                st.warning(message)
    else:
        st.success("✅ Aucune alerte critique détectée")

st.markdown("---")
st.caption("📊 La Pratique Electronique | Projet PFE - Souha Ferjani | Business Intelligence | MiT-Nabeul")
'''

with open('/content/RH_Dashboard/app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)

print("✅ app.py créé avec succès!")
print("📁 Fichier: /content/RH_Dashboard/app.py")
