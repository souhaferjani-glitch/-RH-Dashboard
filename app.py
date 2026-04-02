    col1, col2 = st.columns(2)
    
    with col1:
        # Premier graphique (à gauche)
        effectifs_filtres = actifs[actifs['Service'].isin(service_filter) & 
                                    actifs['Categorie'].isin(categorie_filter) & 
                                    actifs['Sexe'].isin(sexe_filter)]
        effectifs_service = effectifs_filtres.groupby('Service').size().reset_index(name='Effectif')
        fig1 = px.bar(effectifs_service, x='Service', y='Effectif', 
                      title="📊 Effectifs par Service",
                      color='Service',
                      color_discrete_sequence=px.colors.qualitative.Set3)
        fig1.update_layout(height=400)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Deuxième graphique (à droite)
        effectifs_cat = effectifs_filtres.groupby('Categorie').size().reset_index(name='Effectif')
        fig2 = px.pie(effectifs_cat, values='Effectif', names='Categorie', 
                      title="👥 Répartition Cadres/Non-cadres",
                      hole=0.4,
                      color_discrete_sequence=['#667eea', '#764ba2'])
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Graphique central - Répartition par Service (agrandi et centré)
    st.markdown("---")
    st.markdown('<div class="section-title">🏢 Répartition détaillée par Service</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        fig = px.pie(effectifs_service, values='Effectif', names='Service', 
                     title="🏢 Répartition par Service",
                     hole=0.4, 
                     color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_traces(textposition='inside', textinfo='percent+label',
                          marker=dict(line=dict(color='white', width=2)))
        fig.update_layout(
            height=500,
            title_font_size=24,
            title_x=0.5,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2)
        )
        st.plotly_chart(fig, use_container_width=True)
