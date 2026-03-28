import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="RH Dashboard", layout="wide")

st.title("📊 Tableau de Bord RH")
st.markdown("### La Pratique Electronique - Projet PFE Souha Ferjani")

# Données (intégrées directement)
data = {
    'Matricule': ['EMP001', 'EMP002', 'EMP003', 'EMP004', 'EMP005', 'EMP006', 'EMP007'],
    'Service': ['Commercial', 'RH', 'Technique', 'Commercial', 'RH', 'Technique', 'Commercial'],
    'Categorie': ['Cadre', 'Non cadre', 'Cadre', 'Non cadre', 'Cadre', 'Non cadre', 'Cadre'],
    'Sexe': ['H', 'F', 'H', 'F', 'H', 'F', 'F']
}
df = pd.DataFrame(data)

# Mouvements
mouvements = pd.DataFrame({
    'Mois': ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun'],
    'Entrees': [2, 1, 3, 0, 2, 1],
    'Sorties': [1, 1, 3, 1, 0, 2]
})

# Promotions
promos = pd.DataFrame({
    'Employe': ['EMP001', 'EMP003', 'EMP008'],
    'Date': ['01/01/2025', '15/03/2024', '01/12/2024'],
    'Nouveau_Grade': ['Directeur', 'Technicien Principal', 'Responsable RH']
})

# KPIs
total = len(df)
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["Accueil", "Effectifs", "Mouvements", "Promotions"])

if page == "Accueil":
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("👥 Effectif", total)
    with col2: st.metric("📈 Turnover", "12.5%")
    with col3: st.metric("⭐ Promotions", len(promos))
    
    fig = px.pie(df, names='Service', title="Répartition par Service")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Effectifs":
    st.dataframe(df)
    fig = px.bar(df, x='Service', title="Effectifs par Service", color='Categorie')
    st.plotly_chart(fig, use_container_width=True)

elif page == "Mouvements":
    fig = px.bar(mouvements, x='Mois', y=['Entrees', 'Sorties'], title="Entrées vs Sorties", barmode='group')
    st.plotly_chart(fig, use_container_width=True)

elif page == "Promotions":
    st.dataframe(promos)
