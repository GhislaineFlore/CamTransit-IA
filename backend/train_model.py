import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. CORRECTION V3 : Charger le nouveau fichier CSV unifié et multi-systèmes
data = pd.read_csv("historique_prov_besc_guce.csv")

# ==========================================
# MOTEUR IA 1 : CLASSIFICATION DU CODE SH (Texte)
# ==========================================
X_texte = data['description_facture']
y_sh = data['code_sh_valide']

vectorizer = TfidfVectorizer()
X_texte_num = vectorizer.fit_transform(X_texte)

model_sh = RandomForestClassifier(n_estimators=50, random_state=42)
model_sh.fit(X_texte_num, y_sh)

# ==========================================
# MOTEUR IA 2 : DÉTECTION DE FRAUDE ET LITIGES (Numérique)
# ==========================================
# L'IA compare si les noms matchent (1 si oui, 0 si non) et l'écart de colis
# Ces données proviennent dynamiquement des dossiers CAMCIS, GUCE et BESC
data['match_importateur'] = (data['imp_camcis'] == data['imp_guce']).astype(int)
data['ecart_colis'] = abs(data['colis_camcis'] - data['colis_besc'])

X_fraude = data[['match_importateur', 'ecart_colis']]
y_fraude = data['est_fraude']

model_fraude = RandomForestClassifier(n_estimators=30, random_state=42)
model_fraude.fit(X_fraude, y_fraude)

# ==========================================
# SAUVEGARDE DES TROIS CERVEAUX COMPACTS (.pkl)
# ==========================================
joblib.dump(model_sh, 'moteur_prediction_sh.pkl')
joblib.dump(vectorizer, 'vectoriseur_texte.pkl')
joblib.dump(model_fraude, 'moteur_detection_fraude.pkl')

print("🧠 IA V3 Multi-Systèmes entraînée avec succès (CAMCIS + BESC + GUCE) !")
