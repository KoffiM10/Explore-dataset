import streamlit as st
import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF

# =========================
# FONCTION UTILITAIRE PDF
# =========================
def clean_text_for_pdf(text):
    if isinstance(text, str):
        return text.encode("latin-1", "ignore").decode("latin-1")
    return text

# =========================
# CONFIGURATION STREAMLIT
# =========================
st.set_page_config(
    page_title="Exploration Dataset",
    page_icon="🔍",
    layout="wide"
)

st.title("📈 Explore your datasets")

# =========================
# SIDEBAR — UPLOAD
# =========================
st.sidebar.header("📂 Chargement des données")

uploaded_file = st.sidebar.file_uploader(
    "Importer un fichier (CSV ou Excel)",
    type=["csv", "xlsx"]
)

if uploaded_file is None:
    st.info("Veuillez importer un fichier CSV ou Excel pour commencer.")
    st.stop()

# =========================
# GESTION DES FICHIERS EXCEL
# =========================
sheet_name = None
if uploaded_file.name.endswith(".xlsx"):
    excel_file = pd.ExcelFile(uploaded_file)
    sheet_name = st.sidebar.selectbox(
        "📄 Choisir la feuille Excel",
        excel_file.sheet_names
    )

# =========================
# CACHE DE CHARGEMENT
# =========================
@st.cache_data
def load_data(file, sheet=None):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file, sheet_name=sheet)

try:
    df = load_data(uploaded_file, sheet_name)
except Exception as e:
    st.error(f"Erreur lors du chargement du fichier : {e}")
    st.stop()

# =========================
# APERÇU
# =========================
st.subheader("👀 Aperçu des données")
st.dataframe(df.head())

# =========================
# DIMENSIONS
# =========================
st.subheader("📐 Dimensions")
st.write(f"Lignes : **{df.shape[0]}**")
st.write(f"Colonnes : **{df.shape[1]}**")

# =========================
# TYPES
# =========================
num_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

st.subheader("📑 Types de variables")
st.write("Numériques :", num_cols)
st.write("Catégorielles :", cat_cols)

# =========================
# QUALITÉ DES DONNÉES
# =========================
st.subheader("❌ Valeurs manquantes")
missing_df = df.isnull().sum().reset_index()
missing_df.columns = ["Colonne", "Valeurs manquantes"]
st.dataframe(missing_df)

total_missing = int(df.isnull().sum().sum())

# =========================
# STATISTIQUES
# =========================
st.subheader("📊 Statistiques descriptives")
if num_cols:
    st.dataframe(df[num_cols].describe())
else:
    st.warning("Aucune variable numérique.")

# =========================
# VISUALISATION
# =========================
st.subheader("📈 Distribution")

if num_cols:
    selected_col = st.selectbox("Choisir une variable", num_cols)
    fig, ax = plt.subplots()
    sns.histplot(df[selected_col].dropna(), kde=True, ax=ax)
    st.pyplot(fig)

# =========================
# CORRÉLATIONS
# =========================
st.subheader("🔗 Corrélations")

if len(num_cols) > 1:
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(df[num_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

# =========================
# INFO
# =========================
st.subheader("ℹ️ Informations générales")
buffer = io.StringIO()
df.info(buf=buffer)
st.text(buffer.getvalue())

# =========================
# SYNTHÈSE
# =========================
st.subheader("🧠 Synthèse métier")

data_quality = (
    "Bonne" if total_missing == 0
    else "Moyenne" if total_missing < 0.05 * df.size
    else "Faible"
)

st.markdown(f"""
- **{df.shape[0]} lignes**
- **{df.shape[1]} colonnes**
- **{len(num_cols)} variables numériques**
- **{len(cat_cols)} variables catégorielles**
- **{total_missing} valeurs manquantes**
- **Qualité des données : {data_quality}**
""")

# =========================
# PDF
# =========================
st.subheader("📄 Rapport PDF")

if st.button("📥 Générer le rapport PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    report_text = f"""
Rapport d'exploration du dataset

- Lignes : {df.shape[0]}
- Colonnes : {df.shape[1]}
- Variables numériques : {len(num_cols)}
- Variables catégorielles : {len(cat_cols)}
- Valeurs manquantes : {total_missing}
- Qualité des données : {data_quality}
"""

    pdf.multi_cell(0, 8, clean_text_for_pdf(report_text))
    pdf_bytes = pdf.output(dest="S").encode("latin1")

    st.download_button(
        "📥 Télécharger le PDF",
        data=pdf_bytes,
        file_name="exploration_report.pdf",
        mime="application/pdf"
    )
