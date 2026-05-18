-- =====================================================================
-- CONFIGURATION DE LA BASE DE DONNÉES : CamTransit-IA
-- Auteur : Ghislaine Flore - Stage Génie Logiciel
-- Objectif : Gestion dynamique des taxes CAMCIS et historique dossiers
-- =====================================================================

-- 1. NETTOYAGE DES ANCIENNES TABLES (Pour les tests de réinstallation)
DROP TABLE IF EXISTS article_liquide CASCADE;
DROP TABLE IF EXISTS dossier_transit CASCADE;
DROP TABLE IF EXISTS tarif_douanier_cemac CASCADE;
DROP TABLE IF EXISTS parametre_taxe_connexe CASCADE;

-- =====================================================================
-- TABLE 1 : PARAMÈTRES DES TAXES CONNEXES (Mises à jour Loi des Finances)
-- =====================================================================
CREATE TABLE parametre_taxe_connexe (
    id SERIAL PRIMARY KEY,
    code_taxe VARCHAR(10) NOT NULL UNIQUE, -- Ex: 'CIA', 'CAD', 'TCI'
    libelle_taxe VARCHAR(100) NOT NULL,    -- Ex: 'Centime Additionnel Douanier'
    taux_applicable DECIMAL(7,5) NOT NULL, -- Ex: 0.10000 pour 10%
    date_derniere_maj TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Injection des taux réels constants extraits de vos documents CAMCIS
INSERT INTO parametre_taxe_connexe (code_taxe, libelle_taxe, taux_applicable) VALUES
('CAD', 'Centime Additionnel Douanier (sur le DDI)', 0.10000),
('CIA', 'Taxe Communautaire d Integration A', 0.00136),
('CIB', 'Taxe Communautaire d Integration B', 0.00064),
('CCI', 'Contribution Communautaire d Integration I', 0.00272),
('CCB', 'Contribution Communautaire d Integration B', 0.00128),
('TIB', 'Taxe d Integration de Base', 0.00192),
('TCI', 'Taxe Communautaire d Integration Globale', 0.00408),
('PRO', 'Redevance de Promotion Douaniere', 0.00050);

-- =====================================================================
-- TABLE 2 : TARIF DOUANIER CEMAC (Positions Tarifaires & Taxes de Base)
-- =====================================================================
CREATE TABLE tarif_douanier_cemac (
    code_sh VARCHAR(10) PRIMARY KEY,       -- Ex: '85353000' (Code à 8 chiffres)
    libelle_marchandise VARCHAR(255) NOT NULL,
    taux_ddi DECIMAL(5,4) NOT NULL,        -- Droit de Douane à l Importation (Ex: 0.10 ou 0.20)
    taux_tva DECIMAL(5,4) NOT NULL,        -- Taxe sur la Valeur Ajoutée (Ex: 0.1750)
    taux_pct DECIMAL(5,4) NOT NULL,        -- Précompte sur Achat (Ex: 0.1000)
    taux_dea DECIMAL(5,4) DEFAULT 0.0100,  -- Droit d Accise (Ex: 0.0100)
    date_maj TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Injection des positions tarifaires réelles du dossier EAST INDIA lues sur vos fiches
INSERT INTO tarif_douanier_cemac (code_sh, libelle_marchandise, taux_ddi, taux_tva, taux_pct) VALUES
('85353000', 'IACM 36KV WITH EARTHING SWITCH', 0.1000, 0.1750, 0.1000),
('85354000', 'PARA FOUDRE SURGE ARRESTER LIGHTNING', 0.1000, 0.1750, 0.1000),
('85362000', 'COFFRET CIRCUIT BREAKER HP CONTROL BOX', 0.2000, 0.1750, 0.1000);

-- =====================================================================
-- TABLE 3 : DOSSIERS DE TRANSIT (Historique complet des analyses agents)
-- =====================================================================
CREATE TABLE dossier_transit (
    id_dossier SERIAL PRIMARY KEY,
    reference_facture VARCHAR(50) NOT NULL UNIQUE, -- Ex: 'EIUL/043/PERACE/25-26'
    nom_agent VARCHAR(100) NOT NULL,               -- Ex: 'TCHATA MARIUS'
    nom_importateur VARCHAR(150) NOT NULL,          -- Ex: 'EAST INDIA UDYOG LIMITED'
    valeur_fob_eur DECIMAL(15,2) NOT NULL,
    valeur_caf_cfa DECIMAL(15,2) NOT NULL,          -- Assiette fiscale globale calculee
    poids_brut_kg DECIMAL(10,2) NOT NULL,
    nombre_colis INT NOT NULL,
    total_taxes_camcis_cfa DECIMAL(15,2) NOT NULL,  -- Le resultat final à 14 millions
    score_ia_conformite DECIMAL(3,2) NOT NULL,     -- Ex: 1.00 ou 0.65
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================================
-- TABLE 4 : ARTICLES LIQUIDÉS LIGNE PAR LIGNE (Relation Many-to-One)
-- =====================================================================
CREATE TABLE article_liquide (
    id_article SERIAL PRIMARY KEY,
    id_dossier INT REFERENCES dossier_transit(id_dossier) ON DELETE CASCADE,
    code_sh VARCHAR(10) REFERENCES tarif_douanier_cemac(code_sh),
    base_taxable_cfa DECIMAL(15,2) NOT NULL,
    montant_ddi_calcule DECIMAL(15,2) NOT NULL,
    montant_tva_calcule DECIMAL(15,2) NOT NULL,
    montant_annexes_calcule DECIMAL(15,2) NOT NULL
);
