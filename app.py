import streamlit as st
import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF

# =========================
# CONFIGURATION STREAMLIT
# =========================
st.set_page_config(
    page_title="Exploration Dataset",
    page_icon="🔍",
    layout="wide"
)

st.title("📈Explore your datasets")

# =========================
# UPLOAD DU DATASET
# =========================
st.sidebar.header("📂 Chargement des données")

uploaded_file = st.sidebar.file_uploader(
    "Importer un fichier CSV",
    type=["csv"]
)

if uploaded_file is None:
    st.info("Veuillez importer un fichier CSV pour commencer.")
    st.stop()

# =========================
# LECTURE DU DATASET
# =========================
try:
    df = pd.read_csv(uploaded_file)
except Exception as e:
    st.error(f"Erreur lors du chargement du fichier : {e}")
    st.stop()

# =========================
# APERÇU DES DONNÉES
# =========================
st.subheader("👀 Aperçu des données")
st.dataframe(df.head())

# =========================
# DIMENSIONS
# =========================
st.subheader("📐 Dimensions")
st.write(f"Nombre de lignes : **{df.shape[0]}**")
st.write(f"Nombre de colonnes : **{df.shape[1]}**")

# =========================
# TYPES DE VARIABLES
# =========================
num_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

st.subheader("📑 Types de variables")
st.write("**Variables numériques :**", num_cols)
st.write("**Variables catégorielles :**", cat_cols)

# =========================
# QUALITÉ DES DONNÉES
# =========================
st.subheader("❌ Valeurs manquantes")
missing_df = df.isnull().sum().reset_index()
missing_df.columns = ["Colonne", "Valeurs manquantes"]
st.dataframe(missing_df)

# =========================
# STATISTIQUES DESCRIPTIVES
# =========================
st.subheader("📊 Statistiques descriptives (numériques)")
if num_cols:
    st.dataframe(df[num_cols].describe())
else:
    st.warning("Aucune variable numérique détectée.")

# =========================
# VALEURS UNIQUES
# =========================
st.subheader("🔎 Valeurs uniques (aperçu)")
for col in cat_cols:
    st.write(f"**{col}** — {df[col].nunique()} valeurs uniques")
    st.write(df[col].unique()[:10])

# =========================
# VISUALISATIONS
# =========================
st.subheader("📈 Visualisations")

if num_cols:
    selected_col = st.selectbox("Choisir une variable numérique", num_cols)

    fig, ax = plt.subplots()
    sns.histplot(df[selected_col], kde=True, ax=ax)
    ax.set_title(f"Distribution de {selected_col}")
    st.pyplot(fig)

# =========================
# CORRÉLATION
# =========================
st.subheader("🔗 Corrélations")

if len(num_cols) > 1:
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        df[num_cols].corr(),
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        ax=ax
    )
    ax.set_title("Matrice de corrélation")
    st.pyplot(fig)
else:
    st.info("Pas assez de variables numériques pour une corrélation.")

# =========================
# INFORMATIONS GÉNÉRALES
# =========================
st.subheader("ℹ️ Informations générales")

buffer = io.StringIO()
df.info(buf=buffer)
st.text(buffer.getvalue())

# =========================
# SYNTHÈSE MÉTIER AUTOMATIQUE
# =========================
st.subheader("🧠 Synthèse métier automatique")

total_missing = df.isnull().sum().sum()
data_quality = "Bonne" if total_missing == 0 else "Moyenne" if total_missing < (0.05 * df.size) else "Faible"

st.markdown(f"""
- Dataset de **{df.shape[0]} lignes** et **{df.shape[1]} colonnes**
- **{len(num_cols)} variables numériques**
- **{len(cat_cols)} variables catégorielles**
- **{total_missing} valeurs manquantes**
- **Qualité globale des données : {data_quality}**
""")

# =========================
# GÉNÉRATION DU PDF
# =========================
st.subheader("📄 Génération du rapport PDF")

if st.button("📥 Générer le rapport PDF"):

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "Rapport d'exploration du dataset", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 8, f"""
Résumé exécutif :
- Nombre de lignes : {df.shape[0]}
- Nombre de colonnes : {df.shape[1]}
- Variables numériques : {len(num_cols)}
- Variables catégorielles : {len(cat_cols)}
- Valeurs manquantes : {total_missing}
- Qualité des données : {data_quality}

Recommandations :
- Nettoyer les valeurs manquantes si nécessaire
- Analyser les variables clés
- Passer à une analyse exploratoire approfondie
""")

    pdf.output("Outputs/exploration_report.pdf")

    st.success("✅ Rapport PDF généré avec succès (exploration_report.pdf)")
