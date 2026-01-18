# 📈 Explore Your Datasets

Un outil interactif développé avec **Streamlit** pour explorer rapidement vos ensembles de données CSV.  
Ce projet permet de charger un dataset, d’en analyser la structure, de visualiser les distributions, d’évaluer la qualité des données et de générer un rapport PDF synthétique.

---

## ✨ Fonctionnalités

- 📂 **Chargement des données** : importation de fichiers CSV via l’interface Streamlit.  
- 👀 **Aperçu** : affichage des premières lignes du dataset.  
- 📐 **Dimensions** : nombre de lignes et de colonnes.  
- 📑 **Types de variables** : distinction entre variables numériques et catégorielles.  
- ❌ **Valeurs manquantes** : détection et comptage des valeurs nulles.  
- 📊 **Statistiques descriptives** : résumé des colonnes numériques.  
- 🔎 **Valeurs uniques** : aperçu des modalités des variables catégorielles.  
- 📈 **Visualisations** : histogrammes interactifs et matrice de corrélation.  
- ℹ️ **Informations générales** : résumé technique du dataset (`df.info`).  
- 🧠 **Synthèse métier automatique** : évaluation de la qualité globale des données.  
- 📄 **Rapport PDF** : génération automatique d’un rapport d’exploration.

---

## 📂 Organisation du projet

├── app.py                  # Script principal Streamlit
├── Outputs/                # Dossier contenant les rapports PDF générés
├── requirements.txt        # Dépendances du projet
└── README.md               # Documentation du projet


## ▶️ Utilisation

Lancez l’application Streamlit :
streamlit run app.py



## Auteur

Projet réalisé par **Koffi Modeste** dans le cadre d’une montée en compétences en analyse de données.