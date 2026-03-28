# Cellule: Créer app.py (VERSION FINALE SANS AUCUNE ERREUR)
import os

app_content = '''import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Tableau de Bord RH", page_icon="📊", layout="wide")

st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    padding: 25px;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
}
.main-header h1 {
    margin: 0;
    font-size: 28px;
}
.main-header p {
    margin: 8px 0 0 0;
    font-size: 14px;
}
.metric-card {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    border: 1px solid #e9ecef;
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
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>Tableau de Bord RH</h1><p>La Pratique Electronique | Projet PFE - Souha Ferjani</p></div>', unsafe_allow_html=True)

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

st.sidebar.title("La Pratique Electronique")
st.sidebar.markdown("---")
st.sidebar.markdown("Souha Ferjani")
st.sidebar.markdown("Projet PFE - Business Intelligence")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigation", ["Accueil", "Mouvements", "Promotions", "Admin", "Strategique", "Alertes"])

if page == "Accueil":
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Effectif", total)
    with c2: st.metric("Turnover", f"{turnover:.1f}%")
    with c3: st.metric("Promotions", len(promotions))
    with c4: st.metric("Departs", departs)
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(actifs, names='Service', title="Repartition par Service")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(actifs, x='Categorie', title="Cadres vs Non-cadres")
        st.plotly_chart(fig, use_container_width=True)

elif page == "Mouvements":
    st.header("Analyse des Mouvements")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=mouvements['Mois'].dt.strftime('%b %Y'), y=mouvements['Entrees'], name='Entrees', marker_color='green'))
    fig.add_trace(go.Bar(x=mouvements['Mois'].dt.strftime('%b %Y'), y=mouvements['Total_Sorties'], name='Sorties', marker_color='red'))
    fig.update_layout(title='Entrees vs Sorties', barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Entrees", mouvements['Entrees'].sum())
    with col2: st.metric("Sorties", mouvements['Total_Sorties'].sum())
    with col3: st.metric("Solde", mouvements['Entrees'].sum() - mouvements['Total_Sorties'].sum())

elif page == "Promotions":
    st.header("Promotions Internes")
    st.dataframe(promotions, use_container_width=True)

elif page == "Admin":
    st.header("Gestion Administrative")
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(questionnaires, x='Periode', y='Taux_Reponse', title="Taux de reponse", markers=True)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(entretiens, x='Annee', y='Taux_Realisation', title="Entretiens annuels")
        st.plotly_chart(fig, use_container_width=True)
    st.subheader("Sanctions")
    st.dataframe(sanctions, use_container_width=True)

elif page == "Strategique":
    st.header("Indicateurs Strategiques")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Qualite recrutements", f"{qualite:.1f}%")
        st.progress(qualite/100)
    with col2:
        st.metric("Fuite competences", f"{fuite_cadres:.1f}%")
        st.progress(fuite_cadres/100)

elif page == "Alertes":
    st.header("Alertes")
    if turnover > 15: st.error(f"Turnover eleve: {turnover:.1f}%")
    if fuite_cadres > 10: st.error(f"Fuite cadres: {fuite_cadres:.1f}%")
    if qualite < 80: st.warning(f"Qualite recrutements: {qualite:.1f}%")
    if not (turnover > 15 or fuite_cadres > 10 or qualite < 80): st.success("Aucune alerte")

st.markdown("---")
st.caption("La Pratique Electronique | Projet PFE - Souha Ferjani")
'''

with open('/content/app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)

print("✅ app.py cree avec succes!")
print("📁 Fichier: /content/app.py")
