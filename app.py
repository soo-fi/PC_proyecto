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

# =============================================================================
# 1. CONFIGURACIÓN INICIAL DE LA PÁGINA
# =============================================================================
st.set_page_config(
    page_title="Análisis Discursivo: Segunda Vuelta Perú 2026",
    page_icon="🇵🇪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main-title {
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
@st.cache_data
def cargar_datos():
    df = pd.read_excel("base_articulos.xlsx").fillna("")
    # Formatear fecha para eliminar "00:00:00"
    df.loc[:, "fecha"] = pd.to_datetime(df.loc[:, "fecha"], errors="coerce").dt.strftime("%Y-%m-%d").fillna("")
    return df

df_articulos = cargar_datos()

# Contar artículos por diario usando .loc
total_art = len(df_articulos)
cant_peru21 = len(df_articulos.loc[df_articulos.loc[:, "diario"] == "Perú21", :])
cant_larep = len(df_articulos.loc[df_articulos.loc[:, "diario"] == "La República", :])

# =============================================================================
# 3. PORTADA / HERO SECTION (CON FOTOS DE LOS CANDIDATOS)
# =============================================================================
st.markdown('<p class="main-title">Discurso Mediático y Voto en la Segunda Vuelta Perú 2026</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Análisis computacional del lenguaje y emociones en columnas de opinión de Perú21 y La República sobre Keiko Fujimori y Roberto Sánchez.</p>', unsafe_allow_html=True)

col_keiko, col_corpus, col_sanchez = st.columns([1.2, 1.4, 1.2])

# --- BLOQUE IZQUIERDO: KEIKO FUJIMORI ---
with col_keiko:
    with st.container(border=True):
        c_foto_k, c_info_k = st.columns([1, 1.3])
        with c_foto_k:
            st.image("assets/foto_keiko.png", use_container_width=True)  # <--- FOTO DE KEIKO
        with c_info_k:
            st.metric(label="Keiko Fujimori", value="50,135%", delta="Segunda Vuelta")

# --- BLOQUE CENTRAL: RESUMEN DE ARTÍCULOS Y ORACIONES ---
with col_corpus:
    with st.container(border=True):
        c_art, c_ora = st.columns(2)
        with c_art:
            st.metric(
                label="Artículos Analizados",
                value=total_art,
                delta=f"Perú21: {cant_peru21} | La República: {cant_larep}"
            )
        with c_ora:
            st.metric(
                label="Oraciones Filtradas",
                value="[COMPLETAR]",  # <--- PON AQUÍ EL TOTAL DE ORACIONES FILTRADAS
                delta="Menciones exclusivas"
            )

# --- BLOQUE DERECHO: ROBERTO SÁNCHEZ ---
with col_sanchez:
    with st.container(border=True):
        c_foto_s, c_info_s = st.columns([1, 1.3])
        with c_foto_s:
            st.image("assets/foto_sanchez.png", use_container_width=True)  # <--- FOTO DE SÁNCHEZ
        with c_info_s:
            st.metric(label="Roberto Sánchez", value="49,641%", delta="Segunda Vuelta")

st.divider()
# =============================================================================
# 4. NAVEGACIÓN PRINCIPAL POR PESTAÑAS
# =============================================================================
tab_contexto, tab_nubes, tab_pastel, tab_mapa, tab_metodologia = st.tabs([
    "📰 1. Contexto y Corpus",
    "☁️ 2. Narrativa Mediática (Nubes)",
    "📊 3. Polaridad y Emociones (Pastel)",
    "🗺️ 4. Mapa Electoral",
    "⚙️ 5. Metodología y Conclusiones"
])

# -----------------------------------------------------------------------------
# PESTAÑA 1: CONTEXTO, PERFIL DE DIARIOS (LOGOS + DUEÑOS) Y BASE DE DATOS
# -----------------------------------------------------------------------------
with tab_contexto:
    st.header("Presentación de la Investigación")
    st.write("""
    Esta investigación analiza cómo dos de los principales diarios de circulación nacional en el Perú construyeron 
    la narrativa pública en torno a **Keiko Fujimori** y **Roberto Sánchez** durante la segunda vuelta presidencial de 2026.
    """)

    st.subheader("Perfil de los Diarios Analizados")
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
            * **Línea Editorial:** En enero de 2023, Empresa Editora El Comercio acordó vender la marca Perú21 a Media Chirimoya S.A.C., haciéndose efectivo en febrero de ese año.
            * **Historia Política:** [Completar trayectoria y postura frente al escenario político peruano].
            """)
            
            st.link_button("🌐 Visitar sitio web de Perú21", "https://peru21.pe/", use_container_width=True)

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
            * **Línea Editorial:** [Completar orientación editorial, ej. centroizquierda, progresista].
            * **Historia Política:** [Completar trayectoria y postura frente al escenario político peruano].
            """)
            
            st.link_button("🌐 Visitar sitio web de La República", "https://larepublica.pe/politicas-y-estandares#estructura-empresarial-y-fundacion", use_container_width=True)

    
    st.divider()

    # --- EXPLORADOR INTERACTIVO DE LA BASE DE DATOS (USANDO .loc) ---
st.subheader("🔎 Buscador de Columnistas y sus Artículos")

    # Extraer lista única de autores individuales (separando coautorías con "|")
todos_autores = sorted(list({
    autor.strip()
    for fila in df_articulos.loc[:, "autor"]
    for autor in str(fila).split("|")
    if autor.strip() != ""
}))

col_bus1, col_bus2 = st.columns([1, 2])
with col_bus1:
    diario_sel = st.selectbox("Filtrar por diario:", ["Todos", "Perú21", "La República"])
with col_bus2:
    autor_sel = st.selectbox(
        "Selecciona o escribe el nombre de un columnista:",
        ["-- Selecciona un autor --"] + todos_autores
    )

if autor_sel != "-- Selecciona un autor --":
    df_autor = df_articulos.loc[
        df_articulos.loc[:, "autor"].str.contains(autor_sel, case=False, na=False), :
    ].copy()

    if diario_sel != "Todos":
        df_autor = df_autor.loc[df_autor.loc[:, "diario"] == diario_sel, :]

    if not df_autor.empty:
        st.markdown(f"**Artículos encontrados de {autor_sel} ({len(df_autor)}):**")
            
        st.dataframe(
            df_autor.loc[:, ["fecha", "diario", "título", "url"]],
            column_config={
                "fecha": "Fecha de Publicación",
                "diario": "Diario",
                "título": "Título del Artículo",
                "url": st.column_config.LinkColumn("Enlace", display_text="Leer artículo 🔗")
            },
            use_container_width=True,
            hide_index=True
            )
    else:
            st.info(f"{autor_sel} no tiene artículos registrados en {diario_sel}.")
else:
    st.caption("Selecciona o escribe el nombre de un columnista para visualizar los títulos y fechas de sus artículos analizados.")

# -----------------------------------------------------------------------------
# PESTAÑA 2: LAS 4 NUBES DE PALABRAS + FOTOS DE CANDIDATOS + INTERPRETACIONES
# -----------------------------------------------------------------------------
with tab_nubes:
    st.header("Palabras más asociadas a cada candidato por diario")
    subtab_keiko, subtab_sanchez = st.tabs(["Keiko Fujimori", "Roberto Sánchez"])

    with subtab_keiko:
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
                <div class="interpretacion-box">
                <b>Interpretación:</b> [Escribe aquí tu análisis sobre las palabras clave de Perú21 sobre Keiko].
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.subheader("La República — Keiko Fujimori")
            st.image("assets/nube_keiko_larepublica.png", use_container_width=True)  # <--- AQUÍ INGRESAS TU GRÁFICO 2
            st.markdown("""
                <div class="interpretacion-box">
                <b>Interpretación:</b> [Escribe aquí tu análisis sobre las palabras clave de La República sobre Keiko].
                </div>
            """, unsafe_allow_html=True)

    with subtab_sanchez:
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
                <div class="interpretacion-box">
                <b>Interpretación:</b> [Escribe aquí tu análisis sobre las palabras clave de Perú21 sobre Sánchez].
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.subheader("La República — Roberto Sánchez")
            st.image("assets/nube_sanchez_larepublica.png", use_container_width=True)  # <--- AQUÍ INGRESAS TU GRÁFICO 4
            st.markdown("""
                <div class="interpretacion-box">
                <b>Interpretación:</b> [Escribe aquí tu análisis sobre las palabras clave de La República sobre Sánchez].
                </div>
            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PESTAÑA 3: LOS 4 GRÁFICOS DE PASTEL + INTERPRETACIONES
# -----------------------------------------------------------------------------
with tab_pastel:
    st.header("Análisis de Sentimientos: Tono editorial hacia cada candidato")

    st.subheader("📰 Diario Perú21")
    f1_col1, f1_col2 = st.columns(2)
    with f1_col1:
        st.markdown("**Sentimientos hacia Keiko Fujimori (Perú21)**")
        st.image("assets/pastel_keiko_peru21.png", use_container_width=True)  # <--- AQUÍ INGRESAS TU GRÁFICO 5
        st.markdown("""
            <div class="interpretacion-box">
            <b>Interpretación:</b> [Explica aquí los porcentajes hacia Keiko en Perú21].
            </div>
        """, unsafe_allow_html=True)

    with f1_col2:
        st.markdown("**Sentimientos hacia Roberto Sánchez (Perú21)**")
        st.image("assets/pastel_sanchez_peru21.png", use_container_width=True)  # <--- AQUÍ INGRESAS TU GRÁFICO 6
        st.markdown("""
            <div class="interpretacion-box">
            <b>Interpretación:</b> [Explica aquí los porcentajes hacia Sánchez en Perú21].
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("📰 Diario La República")
    f2_col1, f2_col2 = st.columns(2)
    with f2_col1:
        st.markdown("**Sentimientos hacia Keiko Fujimori (La República)**")
        st.image("assets/pastel_keiko_larepublica.png", use_container_width=True)  # <--- AQUÍ INGRESAS TU GRÁFICO 7
        st.markdown("""
            <div class="interpretacion-box">
            <b>Interpretación:</b> [Explica aquí los porcentajes hacia Keiko en La República].
            </div>
        """, unsafe_allow_html=True)

    with f2_col2:
        st.markdown("**Sentimientos hacia Roberto Sánchez (La República)**")
        st.image("assets/pastel_sanchez_larepublica.png", use_container_width=True)  # <--- AQUÍ INGRESAS TU GRÁFICO 8
        st.markdown("""
            <div class="interpretacion-box">
            <b>Interpretación:</b> [Explica aquí los porcentajes hacia Sánchez en La República].
            </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PESTAÑA 4: MAPA DE DISTRIBUCIÓN DE VOTOS + INTERPRETACIÓN
# -----------------------------------------------------------------------------
with tab_mapa:
    st.header("Distribución de Votos en la Segunda Vuelta — Perú 2026")
    col_mapa, col_texto_mapa = st.columns([3, 2])

    with col_mapa:
        # 1. Abre y lee tu archivo HTML (asegúrate de usar encoding="utf-8" para las tildes)
        with open("assets/mapa_votos_peru.html", "r", encoding="utf-8") as f:  # <--- AQUÍ INGRESAS TU MAPA HTML
            codigo_html_mapa = f.read()
        
        # 2. Muestra el mapa interactivo en la web (ajusta 'height' según el alto de tu mapa)
        st.components.v1.html(codigo_html_mapa, height=550, scrolling=False)

    with col_texto_mapa:
        st.subheader("Interpretación Territorial y Mediática")
        st.markdown("""
            <div class="interpretacion-box">
            <b>Análisis de resultados:</b><br><br>
            [Escribe aquí tu interpretación cruzando el mapa electoral con el discurso de ambos diarios].
            </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PESTAÑA 5: METODOLOGÍA Y CONCLUSIONES
# -----------------------------------------------------------------------------
with tab_metodologia:
    st.header("Metodología de Trabajo y Síntesis")
    col_met1, col_met2 = st.columns(2)
    with col_met1:
        st.subheader("Flujo de Procesamiento (Python)")
        st.markdown("""
        * **Corpus:** Artículos de opinión extraídos de *Perú21* y *La República*.
        * **Depuración y Segmentación:** Limpieza de texto, eliminación de *stopwords* y extracción de oraciones por candidato.
        * **Modelado de Sentimientos:** Clasificación mediante `pysentimiento` (`POS`, `NEG`, `NEU`).
        * **Visualización:** Nubes de palabras, gráficos de proporción y cartografía electoral.
        """)
    with col_met2:
        st.subheader("Conclusiones Principales")
        st.markdown("""
            <div class="interpretacion-box">
            [Redacta aquí las conclusiones generales de tu estudio].
            </div>
        """, unsafe_allow_html=True)