# python3 -m venv .venv
# pip install Streamlit
# pip install streamlit_option_menu
# pip install streamlit.components.v1
# python -m streamlit hello
# python -m streamlit run app.py
# python -m pip install openpyxl
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components

import pandas as pd
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Grenze:ital,wght@0,100..900;1,100..900&family=IM+Fell+French+Canon+SC&family=Libre+Baskerville:ital,wght@0,400..700;1,400..700&display=swap');

    html, body, [class*="css"], h1, h2, h3, p, div, span {
        font-family: 'Libre Baskerville', monospace !important;
    }
    </style>
""", unsafe_allow_html=True)

# =============================================================================
# 1. CONFIGURACIÓN INICIAL DE LA PÁGINA
# =============================================================================
st.set_page_config(
    page_title="Análisis discursivo: Segunda Vuelta Perú 2026",
    page_icon="🇵🇪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    main-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .interpretacion-box {
        background-color: #F8FAFC;
        border-left: 4px solid #334155;
        padding: 1rem 1.2rem;
        border-radius: 6px;
        margin-top: 0.8rem;
        margin-bottom: 1.5rem;
        color: #1E293B;
        font-size: 0.95rem;
    }
    </style>
""", unsafe_allow_html=True)

# =============================================================================
# 2. CARGA DE BASE DE DATOS DE ARTÍCULOS Y COLUMNISTAS
# =============================================================================
def cargar_datos():
    df_articulos = pd.read_excel("base_de_datos.xlsx").fillna("")
    # Formatear fecha para eliminar "00:00:00"
    df_articulos["fecha"] = df_articulos.loc[:, "fecha"].astype(str).str.slice(0, 10)
    return df_articulos

df_articulos = cargar_datos()


# Contar artículos por diario usando .loc
total_art = len(df_articulos)
cant_peru21 = len(df_articulos.loc[df_articulos.loc[:, "diario"] == "Perú21", :])
cant_larep = len(df_articulos.loc[df_articulos.loc[:, "diario"] == "La República", :])

# =============================================================================
# 3. PORTADA / HERO SECTION (CON FOTOS DE LOS CANDIDATOS)
# =============================================================================
st.markdown('<h1 class="main-title" style="text-align: center; font-size: 5rem;"> Prensa y polarización: el discurso de opinión en la segunda vuelta Perú 2026 </h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Análisis computacional de los artículos de opinión publicados por los diarios Perú21 y La República sobre los candidatos presidenciales Keiko Fujimori y Roberto Sánchez en las tres semanas previas a la segunda vuelta presidencial 2026 .</p>', unsafe_allow_html=True)

col_keiko, col_corpus, col_sanchez = st.columns([1.2, 1.4, 1.2])

# --- BLOQUE IZQUIERDO: KEIKO FUJIMORI ---
with col_keiko:
    with st.container(border=True):
        c_foto_k, c_info_k = st.columns([1, 1.3])
        with c_foto_k:
            st.image("assets/foto_keiko.png", use_container_width=True)  # <--- FOTO DE KEIKO
        with c_info_k:
            st.metric(label="Keiko Fujimori", value="50,135%", delta="Votos-Segunda vuelta")

# --- BLOQUE CENTRAL: RESUMEN DE ARTÍCULOS Y ORACIONES ---
with col_corpus:
    with st.container(border=True):
        c_art, c_ora = st.columns(2)
        with c_art:
            st.metric(
                label="Artículos analizados",
                value=total_art,
                delta=f"P21: {cant_peru21} | LR: {cant_larep}"
            )
        with c_ora:
            st.metric(
                label="Oraciones analizadas",
                value="264",  # <--- PON AQUÍ LA SUMA TOTAL DE ORACIONES DE AMBOS DIARIOS
                delta="P21: 114 | LR: 150 " # <--- COMPLETA CON LOS DE LA REPÚBLICA
            )

# --- BLOQUE DERECHO: ROBERTO SÁNCHEZ ---
with col_sanchez:
    with st.container(border=True):
        c_foto_s, c_info_s = st.columns([1, 1.3])
        with c_foto_s:
            st.image("assets/foto_sanchez.png", use_container_width=True)  # <--- FOTO DE SÁNCHEZ
        with c_info_s:
            st.metric(label="Roberto Sánchez", value="49,641%", delta="Votos-Segunda vuelta")

st.divider()
# =============================================================================
# 4. NAVEGACIÓN PRINCIPAL POR PESTAÑAS
# =============================================================================
tab_contexto, tab_nubes, tab_pastel, tab_mapa, tab_metodologia = st.tabs([
    "📰 1. Contexto y corpus",
    "☁️ 2. Análisis léxico",
    "📊 3. Análisis de sentimientos",
    "🗺️ 4. Mapa electoral",
    "⚙️ 5. Metodología y conclusiones"
])

# -----------------------------------------------------------------------------
# PESTAÑA 1: CONTEXTO, PERFIL DE DIARIOS (LOGOS + DUEÑOS) Y BASE DE DATOS
# -----------------------------------------------------------------------------
with tab_contexto:
    st.header("Presentación de la investigación")
    st.write("""
    Esta investigación analiza cómo dos de los principales diarios de circulación nacional en el Perú construyeron 
    la narrativa pública en torno a **Keiko Fujimori** y **Roberto Sánchez** durante la segunda vuelta presidencial de 2026.
    """)

    st.subheader("Perfil de los diarios analizados")
    col_d1, col_d2 = st.columns(2)

    with col_d1:
        with st.container(border=True):
            # Fila superior: 3 subcolumnas para centrar el logo
            _, col_logo1, _ = st.columns([1, 2, 1])
            with col_logo1:
                st.image("assets/logo_peru21.png", use_container_width=True)
            
            st.divider()
            
            col_dueno1_foto, col_dueno1_info = st.columns([2, 2])
            with col_dueno1_foto:
                st.image(
                    "assets/dueno_peru21.png",
                    width=250,
                    caption="Directora general: Cecilia Valenzuela"
                )
            with col_dueno1_info:
                st.markdown("**Grupo Propietario:**")
                st.write("Media Chirimoya S.A.C.")
            
            st.markdown(""" 
            * **Línea Editorial:** Perú21 se identifica a sí misma como un diario comprometida con la defensa de la democracia, del libre mercado, la libertad y los derechos civiles. Luego de pasar a manos de Cecilia Valenzuela, señalan que su informacion va dirigida especialmente a la "élites" entendidas, por ejemplo, los sectores de liderazgo.
            * **Historia Política:** Fundado en el 2002 por Bernardo Boca Rey, el diario fue parte del grupo El Comercio hasta su venta en el año 2023. Dió seguimiento a la transición democrática en el año 2000 y fue siguiendo los gobiernos de los presidentes desde aquel año.
            """)
            
            st.link_button("🌐 Visitar sitio web de Perú21", "https://peru21.pe/quienes-somos/", use_container_width=True)

    # --- TARJETA DIARIO 2: LA REPÚBLICA ---
    with col_d2:
        with st.container(border=True):
            # Fila superior: 3 subcolumnas para centrar el logo
            _, col_logo2, _ = st.columns([0.5, 3, 0.5])
            with col_logo2:
                st.image("assets/logo_larepublica.png", use_container_width=True)
            
            st.divider()
            
            col_dueno2_foto, col_dueno2_info = st.columns([2,2])
            with col_dueno2_foto:
                st.image(
                    "assets/dueno_larepublica.png",
                    width=250,
                    caption="Director General: Gustavo Mohme Seminario"
                )
            with col_dueno2_info:
                st.markdown("**Grupo Propietario:**")
                st.write("Grupo La República Publicaciones - Propiedad de la familia Mohme Seminario")
            
            st.markdown("""
            * **Línea Editorial:** La República mantiene una linea editorial progresista, enfocado en la defensa de los derechos humanos, la democracia y la justicia social.
            * **Historia Política:** Fundado en la década de los 80, La República ha mantenido desde sus inicios una postura de oposición frente a los partidos conervadores. Actuó como opositor al gobierno de Fujimori (padre) y hasta el día de hoy como crítico del fujimorismo.
            """)
            
            st.link_button("🌐 Visitar sitio web de La República", "https://larepublica.pe/politicas-y-estandares#estructura-empresarial-y-fundacion", use_container_width=True)
    st.divider()
# =========================================================================
# BLOQUE A: EXPLORACIÓN VISUAL POR DIARIO (GALERÍA DE COLUMNISTAS)
# =========================================================================
    st.subheader("📰 Galería de columnistas por diario")
    diario_galeria = st.selectbox(
        "Selecciona un diario para ver a sus columnistas:",
        ["Perú21", "La República"],
        key="select_diario_galeria"
        )
            
    if diario_galeria != "-- Selecciona un diario --":
        df_diario = df_articulos.loc[df_articulos.loc[:, "diario"] == diario_galeria, :].copy()
                    
        # Construir diccionario único de {autor_individual: foto_individual}
        autores_diario = {}
        for _, row in df_diario.iterrows():
            lista_autores = [a.strip() for a in str(row.loc["autor"]).split("|")]
            lista_fotos = [f.strip() for f in str(row.get("foto_url", "")).split("|")]
                        
            for i, nombre_autor in enumerate(lista_autores):
                if nombre_autor != "" and nombre_autor not in autores_diario:
                    foto = lista_fotos[i] if i < len(lista_fotos) and lista_fotos[i] != "" else "https://via.placeholder.com/100?text=Autor"
                    autores_diario[nombre_autor] = foto
            
        st.markdown(f"**Columnistas de {diario_galeria} ({len(autores_diario)}):**")
                  
        # Mostrar fotos en cuadrícula de 5 columnas
        cols_gal = st.columns(5)
        for idx, (nombre, foto) in enumerate(sorted(autores_diario.items())):
           with cols_gal[idx % 5]:
               with st.container(border=True):
                   st.image(foto, use_container_width=True)
                   st.markdown(f"**{nombre}**")
    else:
        st.caption("Elige un diario en el menú superior para desplegar las fotografías de todos sus columnistas.")
            
    st.divider()
            
    # =========================================================================
    # BLOQUE B: BUSCADOR POR AUTOR (FOTO DEL AUTOR + SUS ARTÍCULOS)
    # =========================================================================
    st.subheader("🔎 Buscador de artículos por columnista")
            
    # Mapear cada autor individual con su foto en todo el corpus
    mapa_fotos_autores = {}
    for _, row in df_articulos.iterrows():
        lista_autores = [a.strip() for a in str(row.loc["autor"]).split("|")]
        lista_fotos = [f.strip() for f in str(row.get("foto_url", "")).split("|")]
        for i, nombre_autor in enumerate(lista_autores):
            if nombre_autor != "" and nombre_autor not in mapa_fotos_autores:
                foto = lista_fotos[i] if i < len(lista_fotos) and lista_fotos[i] != "" else "https://via.placeholder.com/120?text=Autor"
                mapa_fotos_autores[nombre_autor] = foto
            
    todos_autores = sorted(list(mapa_fotos_autores.keys()))
            
    autor_sel = st.selectbox(
        "Selecciona o escribe el nombre de un columnista:",
        ["-- Selecciona un columnista --"] + todos_autores,
        key="select_autor_busqueda"
    )
            
    if autor_sel != "-- Selecciona un columnista --":
        df_autor = df_articulos.loc[
           df_articulos.loc[:, "autor"].str.contains(autor_sel, case=False, na=False), :
        ].copy()
            
        # Dividir en dos columnas: Izquierda (Foto del autor) | Derecha (Sus artículos)
        col_perfil, col_lista_art = st.columns([1, 3.5])
            
        with col_perfil:
            with st.container(border=True):
                st.image(mapa_fotos_autores[autor_sel], use_container_width=True)
                st.markdown(f"### {autor_sel}")
                st.caption(f"Total de columnas: {len(df_autor)}")
            
        with col_lista_art:
            st.markdown(f"**Artículos publicados por {autor_sel}:**")
            st.dataframe(
                df_autor.loc[:, ["fecha", "diario", "título", "url"]],
                column_config={
                    "fecha": "Fecha",
                    "diario": "Diario",
                    "título": "Título del Artículo",
                    "url": st.column_config.LinkColumn("Enlace", display_text="Leer artículo 🔗")
                },
                   use_container_width=True,
                   hide_index=True
            )
    else:
        st.caption("Selecciona o escribe el nombre de un columnista para ver su fotografía junto con el listado de sus artículos.")

# -----------------------------------------------------------------------------
# PESTAÑA 2: LAS 4 NUBES DE PALABRAS + FOTOS DE CANDIDATOS + INTERPRETACIONES
# -----------------------------------------------------------------------------
with tab_nubes: 
    st.header("Nubes de palabras")

    vista_nubes = st.radio(
        label="Selecciona el nivel de análisis:",
        options=[
            "🌐 Panorama general por diario",
            "🟠 Keiko Fujimori",
            "🔴 Roberto Sánchez"
        ],
        horizontal=True,
        key="selector_vista_nubes"
    )

    st.divider()
    
# --- SUB-PESTAÑA 1: PANORAMA GENERAL DE AMBOS DIARIOS ---
    if vista_nubes == "🌐 Panorama general por diario":
            st.markdown("#### Palabras más repetidas en los artículos de opinión por periódico")
            st.caption(
                "Las nubes de palabras muestran el universo léxico general de las columnas de opinión analizadas. "
                "Esto permite identificar qué candidatura concentra mayor atención en la agenda de cada diario."
            )
    
            col_p21, col_lr = st.columns(2, gap="large")
    
            # --- TARJETA 1: PERÚ21 ---
            with col_p21:
                with st.container(border=True):
                    st.markdown("#### 📰 Perú21")
                    st.image(
                        "assets/nube_peru21.png",
                        caption="Nube léxica general — Columnas de Perú21 (2026)",
                        use_container_width=True
                    )
    
                    # Indicadores de visibilidad (ajusta los valores según tus conteos exactos)
                    m1, m2 = st.columns(2)
                    m1.metric(label="Menciones a Keiko", value="36 oraciones")
                    m2.metric(label="Menciones a Sánchez", value="90 oraciones")

                    st.info(
                        "**Foco editorial:** En Perú21 se observa una marcada asimetría en la atención mediática. "
                        "**Roberto Sánchez** domina el centro del debate con más del doble de menciones que "
                        "**Keiko Fujimori**, lo que refleja una agenda de opinión enfocada prioritariamente en el "
                        "el candidato de Juntos por el Perú."
                    )
    
            # --- TARJETA 2: LA REPÚBLICA ---
            with col_lr:
                with st.container(border=True):
                    st.markdown("#### 📰 La República")
                    st.image(
                        "assets/nube_larepublica.png",
                        caption="Nube léxica general — Columnas de La República (2026)",
                        use_container_width=True
                    )
    
                    # Indicadores de visibilidad (reemplaza 'XX' con tus conteos reales de La República)
                    m3, m4 = st.columns(2)
                    m3.metric(label="Menciones a Keiko", value="45 oraciones")
                    m4.metric(label="Menciones a Sánchez", value="114 oraciones")
                    
    
                    st.info(
                        "**Foco editorial:** De modo similar a Perú21, en La República " 
                        "**Roberto Sánchez** concentra más del doble de menciones que su contrincante **Keiko Fujimori**," 
                        "siendo el foco de la atención editorial previo a la segunda vuelta." 
                    )               
                
        
    # 2. VENTANAS: KEIKO FUJIMORI
    elif vista_nubes == "🟠 Keiko Fujimori":
        # Pega aquí (con 8 espacios de sangría) el código que ya tienes para las nubes de Keiko
        # Encabezado visual de Keiko Fujimori
        head_k1, head_k2 = st.columns([1, 7])
        with head_k1:
            st.image("assets/foto_keiko.png", width=150)  # <--- AQUÍ INGRESAS LA FOTO DE KEIKO
        with head_k2:
            st.subheader("Candidata: Keiko Fujimori")
            st.caption("Comparativa de términos más frecuentes asociados a su candidatura en la prensa escrita.")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Perú21 — Keiko Fujimori")
            st.image("assets/nube_keiko_peru21.png", use_container_width=True)  # <--- AQUÍ INGRESAS TU GRÁFICO 1
            st.markdown("""
                <div class="interpretacion-box" style="text-align: justify;">
                <b>Interpretación:</b> El gráfico muestra las palabras que más se repiten en los corpus de texto del diario Perú21. La palabra que más se repite es "Keiko", seguido de Sánchez, quien era su contriacnte en la segunda vuelta presidencial 2026. Seguido a esto, encontramos "Castillo" que lo usan para recordar las pasadas elecciones presidenciales del 2022 en donde Keiko Fujimori y Pedro Castillo se enfrentaron. la palabra "reinvidica" podemos relacionarlo con que Keiko queire imitar un gobierno al de su padre, Alberto Fujimori, ex-presidente del Perú, acusado de violeaciones de derechosn humanos y corrupción. Por último, debido a su corte liberal económico, Perú21 pedía votar por la lideresa de Fuerza Popular, quien era un signo de estabilidad económica. 
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.subheader("La República — Keiko Fujimori")
            st.image("assets/nube_keiko_larepublica.png", use_container_width=True)  # <--- AQUÍ INGRESAS TU GRÁFICO 2
            st.markdown("""
                <div class="interpretacion-box" style="text-align: justify;">
                <b>Interpretación:</b> El gráfico podemos observar las palabras que mas se repiten las columnas de opinión analizadas. Vemos como se repite el nombre "Keiko", acompañado de "Sánchez" quien es fue su contricante en la segunda vuelta de las elecciones presidenciales. Otra palabra repetida es "padre", esta palabra se relaciona con el hecho de que Keiko Fujimori es la hija del ex-presidente Alberto Fujimori, cuestionado por violaciones a derechos humanos y corrupción. La palabra "congreso" se puede relacionar con los cuestionamientos hacia las bancadas del Congreso de Fuerza Popular desde el año 2016, acusadas de obtruccionismo hacia los gobiernos de turno. 
                </div>
            """, unsafe_allow_html=True)

        pass

    # 3. VENTANAS: ROBERTO SÁNCHEZ
    elif vista_nubes == "🔴 Roberto Sánchez":
        # Pega aquí (con 8 espacios de sangría) el código que ya tienes para las nubes de Sánchez
        # Encabezado visual de Roberto Sánchez
        head_s1, head_s2 = st.columns([1, 7])
        with head_s1:
            st.image("assets/foto_sanchez.png", width=150)  # <--- AQUÍ INGRESAS LA FOTO DE SÁNCHEZ
        with head_s2:
            st.subheader("Candidato: Roberto Sánchez")
            st.caption("Comparativa de términos más frecuentes asociados a su candidatura en la prensa escrita.")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Perú21 — Roberto Sánchez")
            st.image("assets/nube_sanchez_peru21.png", use_container_width=True)  # <--- AQUÍ INGRESAS TU GRÁFICO 3
            st.markdown("""
                <div class="interpretacion-box" style="text-align: justify;">
                <b>Interpretación:</b> El gráfico muestra las palabras que mas se repiten en el corpus de texto que se obtuvo de las columnas de opinión de Perú21. Acompañando a Sánchez se observa la palabra "castillo" y "antauro". Durante la campaña presidencial de Sánchez intentó reinvidicar la figura del ex-presidente Pedro Castillo a través del sobrero chotano. Así mismo, el ex-militar estuvo estrechamente vinculado a Roberto Sánchez, esto aún cuando Humala es cuestionado por algunas declaraciones sobre derechos humanos, mujeres y derechos LGTBQ+. Por últmo, se encuentra la palabra "francke" el ciual hace referencia al ex-ministro de economía del gobierno de Pedro Castillo. Francke también estuvo vinculado a la campaña de Juntos por el Perú, actuando como representante de las propuestas económicas del partido.
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.subheader("La República — Roberto Sánchez")
            st.image("assets/nube_sanchez_larepublica.png", use_container_width=True)  # <--- AQUÍ INGRESAS TU GRÁFICO 4
            st.markdown("""
                <div class="interpretacion-box" style="text-align: justify;">
                <b>Interpretación:</b> En el gráfico podemos observar las palabras que se mas se repiten a partir de las oraciones que mencionan a ROberto Sánchez en las columnas de opinión de La República. La palbra más repetida es la palabra "Sánchez", seguido de "castillo", palabra que podemos relaionarlo conn el candidato de Juntos por el Perú debido a que durante su campaña electoral, Sánchez intentó reinvidicar la figura del ex-presidente Pedro Castillo (destituido por un intento de golpe de estado fallido) a travé del sombrero, el mismo que usaba Castillo en su campaña presidencial del 2021. Otra palabra que se repite es "antauro", esto por la pólemica conexión entre el candidatos Roberto Sánchez con el ex-militar Antauro Humala, hermano de Ollanta Humala, conocido por liderar el famoso Andahuaylazo. La pólemica surge debido a declaraciones cuestionadas por parte de Humala. Al final de la carrera electoral, Sánchez trató de deslindarse de Antauro, sin embargo, esto le costó las elecciones debido a la peligrosidad que el ex-militar representa.  
                </div>
            """, unsafe_allow_html=True)
        pass
# -----------------------------------------------------------------------------
# PESTAÑA 3: LOS 4 GRÁFICOS DE PASTEL + INTERPRETACIONES
# -----------------------------------------------------------------------------
with tab_pastel:
    st.header("Tono editorial hacia cada candidato")

    st.subheader("📰 Diario Perú21")
    f1_col1, f1_col2 = st.columns(2)
    with f1_col1:
        st.markdown("**Sentimientos hacia Keiko Fujimori (Perú21)**")
        st.image("assets/pastel_keiko_peru21.png", use_container_width=True)  # <--- AQUÍ INGRESAS TU GRÁFICO 5
        st.markdown("""
            <div class="interpretacion-box" style="text-align: justify;">
            <b>Interpretación:</b> El analizador de sentimientos arrojó, sobre las oraciones en donde se menciona a Keiko Fujimori de la columnas de opinión, un total de 63.9% de sentimientos negativos hacia la lideresa de Fuerza Popular. Los sentimientos positivos solo suben al 2.8%, mientars que, los sentimientos neutro obtienen un porcentaje de 33.3%. Viendo los resultados podemos identifcar que en las oraciones en donde se menciona a Fujimori se habla de manera o se refieren de manera negativa hacia ella, lo negativo predomina en las columnas de opinión.   .
            </div>
        """, unsafe_allow_html=True)

    with f1_col2:
        st.markdown("**Sentimientos hacia Roberto Sánchez (Perú21)**")
        st.image("assets/pastel_sanchez_peru21.png", use_container_width=True)  # <--- AQUÍ INGRESAS TU GRÁFICO 6
        st.markdown("""
            <div class="interpretacion-box" style="text-align: justify;">
            <b>Interpretación:</b> En el gráfico se puede observar que el líder de Juntos por el Perú obtuvo un 73.3% de sentimientos negativos, la diferencia con el porcentaje que obtuvo Keiko es de 9.4%, en donde Sánchez obtiene mas sentimientos negativos a través de las columnas de opinión de este diario. Sin embargo, obtiene una diferencia sobre Keiko de 2.8% en sentimientos positivos. Por último, el porcentaje neutro en el líder de Juntos por el perú cambia, obteniendo así un prcentaje de 21.1%, a diferencia de Keiko que obtuvo un 33.3%.
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("📰 Diario La República")
    f2_col1, f2_col2 = st.columns(2)
    with f2_col1:
        st.markdown("**Sentimientos hacia Keiko Fujimori (La República)**")
        st.image("assets/pastel_keiko_larepublica.png", use_container_width=True)  # <--- AQUÍ INGRESAS TU GRÁFICO 7
        st.markdown("""
            <div class="interpretacion-box" style="text-align: justify;">
            <b>Interpretación:</b> El gráfico muestra que en las oraciones en donde se mencionan Keiko Fujimori en La República hay una tendencia de referirse a ella de modo neutral y negativo, los cuales muestra un porcentaje de 46.7%. Por otro lado, los sentimientos identificados solo se muestran en un 6.7%, más que el porcentaje en Perú21 (2.8%). Los resultados de este análisis pueden resultar un poco confuso sobre todo por el historial antifujimorista que posee La República. Una respuesta a estos resultados podría ser que después del historial de Pedro Castillo en el gobierno, Keiko Fujimori se presente como una estabiolidad económica y social, luego de las vacancias constantes desde el 2020, que inició con Martín Vizcarra.
            </div>
        """, unsafe_allow_html=True)

    with f2_col2:
        st.markdown("**Sentimientos hacia Roberto Sánchez (La República)**")
        st.image("assets/pastel_sanchez_larepublica.png", use_container_width=True)  # <--- AQUÍ INGRESAS TU GRÁFICO 8
        st.markdown("""
            <div class="interpretacion-box" style="text-align: justify;">
            <b>Interpretación:</b> Este gráfico se muestra diferente ante los demás debido a que no se identificó algún sentimiento positivo en las oraciones en donde se menciona a Roberto Sanchez. Los sentimientos negativos alcanzan el 65.8%, mientras que los sentimientos neutrales alcanzan el 34.2%. Este gráfico tambien se puede mostrar un poco confuso, sin embargo, Sánchez en su campaña electoral representó inestabiidad económica y social por los antecedentes del gobierno de Pedro Castillo.
            </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PESTAÑA 4: MAPA DE DISTRIBUCIÓN DE VOTOS + INTERPRETACIÓN
# -----------------------------------------------------------------------------
with tab_mapa:
    st.header("Distribución de votos en la segunda vuelta — Perú 2026")
    col_mapa, col_texto_mapa = st.columns([3, 2])

    with col_mapa:
        # 1. Abre y lee tu archivo HTML (asegúrate de usar encoding="utf-8" para las tildes)
        with open("assets/mapa_votos_peru.html", "r", encoding="utf-8") as f:  # <--- AQUÍ INGRESAS TU MAPA HTML
            codigo_html_mapa = f.read()
        
        # 2. Muestra el mapa interactivo en la web (ajusta 'height' según el alto de tu mapa)
        st.components.v1.html(codigo_html_mapa, height=550, scrolling=False)

    with col_texto_mapa:
        st.subheader("Interpretación territorial y mediática")
        st.markdown("""
            <div class="interpretacion-box" style="text-align: justify;">
            <b>Análisis de resultados:</b><br><br>
            El mapa muestra las regiones en donde ganó Keiko Fujimori y Roberto Sánchez. La lideresa de Fuerza Popular logró una victoria en 9 de 25 regiones en el Perú, mientras que el lider de Juntos por el Perú logró una victoria en 16 regiones. Podemos observar que la tendencia se divide así: Keiko Fujimori triunfó sobre todo en regiones del Norte, en Lima e Ica, Roberto Sánchez obtuvo el apoyo de regiones del Centro y Sur del Perú especialmente. Si solo se contabilizará los votos del Perú, el ganador habría sido Roberto Sánchez, sin embargo, Keiko Fujimori salió ganadora de las elecciones presidenciales 2026 gracias a los votos de los peruanos en el extranjero.
            </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PESTAÑA 5: METODOLOGÍA Y CONCLUSIONES
# -----------------------------------------------------------------------------
with tab_metodologia:
    st.header("Metodología de trabajo y síntesis")
    col_met1, col_met2 = st.columns(2)
    with col_met1:
        st.subheader("Flujo de procesamiento (Python)")
        st.markdown("""
        * **Corpus:** Artículos de opinión extraídos de *Perú21* y *La República*.
        * **Depuración y Segmentación:** Limpieza de texto, eliminación de *stopwords* y extracción de oraciones por candidato.
        * **Modelado de Sentimientos:** Clasificación mediante `pysentimiento` (`POS`, `NEG`, `NEU`).
        * **Visualización:** Nubes de palabras, gráficos de proporción y cartografía electoral.
        """)
    with col_met2:
        st.subheader("Conclusiones principales")
        st.markdown("""
        * *Se observa que las columnas de opinión de los dos diarios analizados meustran de manera diferente a cada candidato.*
        * *A través de los gráficos de pastel podemos observar como son los sentimientos de las palabras cuando se refieren a Keiko Fujimori o Roberto Sánchez. En Perú21, se refieren de manera negativa hacia los dos, pero más a Sánchez. En La República se refieren de manera a los dos candidatos, pero hay un porcentaje pequeño de sentimientos positivos hacia Keiko, aunque el procentaje de sentimientos negativos y neutros son iguales, y con Sánchez no hay referencias positivas.* 
        * **Modelado de Sentimientos:**
        * **Visualización:**
        """)
