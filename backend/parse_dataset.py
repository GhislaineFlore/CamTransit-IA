import os
import re
import csv
import pdfplumber

# Configuration des chemins d'accès
DOSSIER_PDF = "./dataset_provisoires"
FICHIER_OUTPUT_CSV = "historique_provisoires_camcis.csv"

def extraire_donnees_dun_pdf(chemin_pdf):
    """ Ouvre un PDF provisoire CAMCIS et en extrait les couples (Description, Code SH) """
    lignes_extraites = []
    
    try:
        with pdfplumber.open(chemin_pdf) as pdf:
            for page in pdf.pages:
                texte_page = page.extract_text() or ""
                
                # Expression régulière pour détecter les lignes de tarification douanière.
                # Motif recherché : Un code SH à 8 chiffres, suivi d'une description textuelle, se terminant par des valeurs numériques.
                motif_camcis = re.findall(r"(\d{8})\s+([A-Za-z\s().\-\d]+?)\s+([\d,.\s]+)", texte_page)
                
                for match in motif_camcis:
                    code_sh = match[0]
                    description = match[1].strip()
                    
                    # Filtre de nettoyage pour éliminer les bruits ou les mots trop courts
                    if len(description) > 5 and not description.isupper():
                        # Nettoyer les espaces superflus
                        description_propre = re.sub(r'\s+', ' ', description)
                        lignes_extraites.append({
                            "description_facture": description_propre,
                            "code_sh_valide": code_sh
                        })
    except Exception as e:
        print(f"⚠️ Impossible de lire le fichier {os.path.basename(chemin_pdf)} : {str(e)}")
        
    return lignes_extraites

def compiler_le_dataset():
    """ Parcourt le dossier de stockage et centralise toutes les données dans le CSV global """
    if not os.path.exists(DOSSIER_PDF):
        print(f"❌ Le dossier '{DOSSIER_PDF}' n'existe pas. Veuillez le créer avec 'mkdir dataset_provisoires'.")
        return

    fichiers = [f for f in os.listdir(DOSSIER_PDF) if f.lower().endswith('.pdf')]
    
    if not fichiers:
        print(f"ℹ️ Aucun fichier PDF trouvé dans '{DOSSIER_PDF}'. Glissez-y vos documents provisoires pour commencer.")
        return

    print(f"🔍 Analyse en cours de {len(fichiers)} fichiers provisoires CAMCIS...")
    
    tout_le_dataset = []
    for nom_fichier in fichiers:
        chemin_complet = os.path.join(DOSSIER_PDF, nom_fichier)
        donnees_fichier = extraire_donnees_dun_pdf(chemin_complet)
        tout_le_dataset.extend(donnees_fichier)
        print(f"✅ {nom_fichier} traité ({len(donnees_fichier)} articles extraits).")

    if not tout_le_dataset:
        print("❌ Aucune donnée tarifaire valide n'a pu être extraite des PDF.")
        return

    # Écriture finale dans le fichier CSV d'entraînement
    champs = ["description_facture", "code_sh_valide"]
    try:
        with open(FICHIER_OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=champs)
            writer.writeheader()
            writer.writerows(tout_le_dataset)
        print(f"\n🚀 SÉCURITÉ ET STRUCTURATION TERMINÉES !")
        print(f"📊 Le fichier '{FICHIER_OUTPUT_CSV}' contient désormais {len(tout_le_dataset)} exemples d'entraînement.")
    except Exception as e:
        print(f"❌ Erreur lors de l'écriture du fichier CSV : {str(e)}")

if __name__ == "__main__":
    compiler_le_dataset()
