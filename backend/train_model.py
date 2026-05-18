import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. Charger l'historique des provisoires extraits
# Ce fichier contient deux colonnes : 'description_facture' et 'code_sh_valide'
data = pd.read_csv("historique_provisoires_camcis.csv")

X = data['description_facture']  # Le texte de la facture (Ex: "IACM 36KV circuit breaker")
y = data['code_sh_valide']       # La bonne décision prise par l'humain (Ex: "85353000")

# 2. Vectorisation (Transformer le texte en nombres compréhensibles par l'IA)
vectorizer = TfidfVectorizer()
X_numerique = vectorizer.fit_transform(X)

# 3. Choix et Entraînement du modèle (Algorithme Random Forest)
model_ia = RandomForestClassifier(n_estimators=100)
model_ia.fit(X_numerique, y)

# 4. Sauvegarder l'IA entraînée dans des fichiers physiques fichiers .pkl
joblib.dump(model_ia, 'moteur_prediction_sh.pkl')
joblib.dump(vectorizer, 'vectoriseur_texte.pkl')

print("🧠 IA entraînée avec succès d'après l'historique de l'agence !")
