# 📦 VOGEL SYSTEM - Optimisation Logistique

Cette application est un solveur basé sur la **Méthode d'Approximation de Vogel (VAM)**. Elle permet de minimiser les coûts de transport entre plusieurs sources et destinations.

## ✨ Fonctionnalités
- 🚛 **Algorithme VAM** : Calcul d'une solution de base quasi-optimale.
- 📊 **Visualisation** : Diagrammes de Sankey interactifs (Plotly).
- 📥 **Export** : Téléchargement des résultats au format Excel.
- 💬 **Feedback** : Système d'avis connecté en temps réel via un Bot Telegram.

## 🛠️ Installation
1. Clonez le dépôt
2. Installez les dépendances : `pip install -r requirements.txt`
3. Lancez l'app : `streamlit run VAM.py`

## 🔒 Sécurité
Les clés API Telegram sont gérées via les `Secrets` de Streamlit pour garantir la confidentialité des données.