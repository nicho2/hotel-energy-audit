

# 🧾 Cahier des charges — Application d’audit énergétique hôtel (V1)

## 1. Objectif du produit

Développer une **application web d’aide à la décision** permettant :

* d’estimer les **déperditions et consommations énergétiques** d’un bâtiment d’hébergement existant,
* de simuler des **scénarios d’amélioration** (techniques + BACS),
* de comparer des **bouquets de solutions**,
* de calculer un **ROI multi-indicateurs**,
* de générer un **rapport professionnel (PDF)**.

⚠️ Positionnement assumé :

* **outil d’estimation simplifiée**, non réglementaire,
* orienté **commercial / exploitant**,
* basé sur **abaques, normes et règles métier** (ISO 52016, EN ISO 52120, EPBD).

---

## 2. Périmètre fonctionnel

### Cible

* Bâtiments d’hébergement existants :

  * hôtels,
  * résidences,
  * appart-hôtels,
  * structures assimilées.

### Utilisateurs

* exploitants,
* commerciaux,
* intégrateurs GTB/BACS.

---

## 3. Architecture fonctionnelle globale

### Modules principaux

1. Gestion des projets
2. Wizard de saisie
3. Moteur de calcul simplifié
4. Module BACS
5. Module scénarios / solutions
6. Module ROI
7. Comparateur
8. Générateur de rapport
9. Administration / catalogue
10. Gestion utilisateurs & marque blanche

---

## 4. Modèle de données (niveau conceptuel)

### Entités principales

* Project
* Building
* Zone
* System (CVC, ECS, éclairage…)
* BACSProfile
* Scenario
* Solution
* EconomicModel
* ResultSet
* Report

---

## 5. Wizard utilisateur (UX cœur produit)

### Étapes

1. Projet
2. Contexte (pays, climat)
3. Bâtiment
4. Zones & orientations
5. Usages & occupation
6. Systèmes techniques
7. BACS actuel
8. Scénarios
9. Résultats
10. Rapport

### UX

* sauvegarde automatique
* duplication projet/scénario
* comparaison multi-scénarios
* mode **express / avancé**

---

## 6. Description du bâtiment

### Données minimales (mode express)

* surface totale
* nombre d’étages
* nombre de chambres
* année / période construction
* localisation (zone climatique)
* orientation principale

### Mode avancé

* ratio vitrage
* isolation par paroi
* taux d’infiltration
* consignes de température
* surfaces par orientation (N/S/E/O)
* zoning fonctionnel

---

## 7. Modélisation des zones

### Types de zones

* chambres (critique)
* circulations
* lobby
* restauration
* salles réunion
* techniques

### Spécificité chambres

* taux d’occupation
* mode absence
* ouverture fenêtre
* mode nuit
* housekeeping

👉 Élément différenciant clé du produit

---

## 8. Moteur de calcul énergétique

### Principe

Simulation simplifiée basée sur :

* abaques
* coefficients standards
* facteurs correctifs

### Calculs

* chauffage
* refroidissement
* ventilation
* ECS
* éclairage
* auxiliaires

### Facteurs pris en compte

* climat
* orientation
* enveloppe
* occupation
* systèmes
* automatismes

### Sorties

* kWh/an par usage
* kWh/m²
* estimation CO₂

---

## 9. Module BACS

### Référence

* logique EN ISO 52120 (classes A/B/C/D)

### Fonctionnement

#### 1. Détection automatique

via questionnaire :

* régulation chauffage
* gestion ventilation
* pilotage éclairage
* supervision
* suivi énergétique
* détection présence

#### 2. Résultat

* classe actuelle estimée

#### 3. Simulation cible

* ajout fonctions → recalcul gains

### Exemple

* détection présence chambres → -X%
* régulation pièce par pièce → -Y%
* gestion horaire → -Z%

---

## 10. Catalogue de solutions

### Structure d’une solution

* nom
* description
* applicable si…
* gains énergétiques (% ou absolu)
* impact BACS
* CAPEX
* maintenance
* durée de vie
* impact CO₂

### Types

* BACS / GTB
* CVC
* enveloppe
* éclairage
* ECS
* optimisation

### Particularité

* catalogue **générique**
* * catalogue **spécifique par pays**
* * catalogue **personnalisable entreprise**

---

## 11. Module scénarios

### Fonctionnalités

* création de scénarios multiples
* combinaison de solutions (bouquets)
* comparaison côte à côte

---

## 12. Module ROI

### Indicateurs

* Payback simple
* VAN (valeur actuelle nette)
* TRI
* cash-flow

### Inputs

* CAPEX
* prix énergie
* inflation
* taux actualisation
* maintenance
* remplacement
* subventions
* durée de vie

### Outputs

* ROI global
* ROI par solution
* ROI par bouquet

---

## 13. Comparateur

### Visualisations

* avant / après
* scénarios multiples
* gains énergétiques
* gains CO₂
* gains €€
* impact BACS

---

## 14. Rapport (PDF prioritaire)

### Contenu

#### 1. Synthèse exécutive

* score global
* gains principaux
* ROI

#### 2. Description bâtiment

#### 3. État initial

#### 4. Analyse BACS

#### 5. Scénarios comparés

#### 6. ROI

#### 7. Plan d’action priorisé

#### 8. Hypothèses

---

## 15. Gestion projets

* création / duplication
* modèles de projets
* versionning
* partage
* historique

---

## 16. Gestion utilisateurs

* rôles (admin, user, viewer)
* accès projets
* multi-utilisateurs

---

## 17. Marque blanche

### Niveau V1

* logo
* couleurs
* pied de page
* catalogue solutions
* mentions légales

### Évolution possible

* domaine dédié
* templates rapport custom

---

## 18. Multi-pays

### V1

* France
* UE générique

### Paramètres

* climat
* prix énergie
* cadre réglementaire affiché

---

## 19. Exigences non fonctionnelles

### Performance

* réponse < 2s
* recalcul rapide

### UX

* simple
* pédagogique
* visuel

### Transparence

* hypothèses visibles
* calculs explicables

---

## 20. Architecture technique (recommandée)

### Front

* React / Next.js

### Backend

* Python (FastAPI) ou Node.js

### Calcul

* microservice dédié

### DB

* PostgreSQL

### Export PDF

* génération serveur (HTML → PDF)

---

## 21. Roadmap

### V1

* audit simplifié
* BACS estimatif
* ROI
* PDF
* wizard

### V2

* import Excel
* connexion GTB réelle
* calibration données réelles
* API externe

---

## 22. Positionnement marché

Produit positionné comme :

* outil de **pré-audit rapide**
* outil **commercial différenciant**
* outil de **préconisation énergétique**

---

## 23. Points forts différenciants

* focus **hôtellerie**
* gestion fine des **chambres**
* lien direct **BACS → gains énergétiques**
* approche **bouquet + ROI**
* simplicité + crédibilité

---

