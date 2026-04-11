
# 5. Spécification fonctionnelle des écrans et du wizard

## 5.1 Principes UX

L’application doit respecter 8 principes :

1. **progressive disclosure**
   ne montrer que le nécessaire au bon moment.

2. **mode express par défaut**
   pour aller vite en rendez-vous.

3. **mode avancé activable**
   pour affiner sans casser la simplicité globale.

4. **comparaison toujours visible**
   le produit vend une décision, pas juste une saisie.

5. **langage métier non technique**
   avec aide contextuelle discrète.

6. **résultats lisibles immédiatement**
   KPI, gains, ROI, BACS.

7. **traçabilité des hypothèses**
   visible mais non intrusive.

8. **orientation rapport**
   chaque étape alimente directement le PDF final.

---

# 5.2 Navigation globale

## Menu principal recommandé

* Tableau de bord
* Projets
* Modèles de projets
* Rapports
* Catalogue de solutions
* Administration
* Mon compte

## Navigation dans un projet

À l’intérieur d’un projet :

* Vue d’ensemble
* Wizard
* Scénarios
* Comparateur
* Rapports
* Hypothèses
* Historique

---

# 5.3 Tableau de bord

## Objectif

Donner une vue rapide des projets et permettre une reprise immédiate.

## Contenu

* liste des projets récents
* statut
* pays
* type de bâtiment
* date de mise à jour
* scénario de référence
* dernier rapport généré

## Actions

* créer un projet
* ouvrir
* dupliquer
* archiver
* générer un rapport
* créer depuis un modèle

## Filtres

* pays
* statut
* type de bâtiment
* client
* utilisateur créateur

---

# 5.4 Écran “Créer un projet”

## Champs

* nom du projet
* client
* pays
* langue
* type de bâtiment
* objectif
* modèle de projet optionnel
* branding/profil entreprise

## Objectif métier

Créer un conteneur minimal en moins d’1 minute.

## Validations

* nom obligatoire
* pays obligatoire
* type de bâtiment obligatoire

## Résultat

Création du projet + redirection vers le wizard.

---

# 5.5 Vue d’ensemble projet

## Objectif

Servir de page de synthèse avant d’entrer dans le détail.

## Contenu

* nom du projet
* client
* pays
* statut
* progression wizard
* nombre de scénarios
* dernier calcul
* dernier rapport
* bloc “état initial”
* bloc “meilleur scénario”
* bloc “prochaines étapes”

## KPI visibles si calcul déjà disponible

* énergie annuelle estimée
* CO₂
* classe BACS
* économies potentielles
* payback

## Actions

* reprendre le wizard
* ajouter un scénario
* comparer
* générer un rapport
* dupliquer

---

# 5.6 Structure du wizard

Je recommande 10 étapes.

1. Projet
2. Contexte pays & climat
3. Bâtiment
4. Zones & orientation
5. Usages & occupation
6. Systèmes techniques
7. BACS actuel
8. Scénarios / bouquets
9. Résultats comparatifs
10. Rapport

---

# 5.7 Étape 1 — Projet

## Objectif

Poser le cadre administratif et commercial.

## Champs

* nom projet
* client
* référence
* description
* objectif du projet

  * économies d’énergie
  * amélioration BACS
  * décarbonation
  * audit global
  * pré-vente
* type d’utilisateur cible

  * exploitant
  * direction
  * client final
* langue du rapport
* branding

## Mode avancé

* notes internes
* tags
* responsable projet
* date cible

## Sorties utilisées

* page de garde du rapport
* contexte commercial

---

# 5.8 Étape 2 — Contexte pays & climat

## Objectif

Déterminer le cadre de calcul et d’affichage réglementaire.

## Champs express

* pays
* zone climatique standard
* type de cadre

  * France
  * UE générique

## Champs avancés

* altitude
* sévérité chauffage
* sévérité refroidissement
* exposition solaire locale
* prix énergie par défaut
* facteurs CO₂ par défaut
* durée d’analyse économique
* taux d’actualisation

## Aides

* info-bulles sur la différence France / UE générique
* rappel que la V1 reste estimative

## Règles UX

Changer le pays peut recalculer :

* catalogue par défaut
* hypothèses pays
* texte réglementaire du rapport

---

# 5.9 Étape 3 — Bâtiment

## Objectif

Décrire le bâtiment au niveau global.

## Champs express

* surface totale
* surface chauffée
* surface refroidie
* nombre d’étages
* nombre de chambres
* période de construction
* compacité
* orientation principale
* présence restaurant
* présence salle de réunion
* présence spa
* présence piscine

## Champs avancés

* année de construction
* hauteur moyenne
* altitude
* commentaire enveloppe
* niveau supposé d’isolation
* niveau supposé d’étanchéité
* bâtiment rénové partiellement ou non

## Validations

* surfaces cohérentes
* nombre de chambres > 0 pour un hôtel
* surface chauffée ≤ surface totale

## Aide UI

Un bandeau “impact estimatif” peut afficher en direct :

* chauffage plutôt élevé / moyen / faible
* refroidissement potentiellement sensible ou non
* ECS importante ou très importante

---

# 5.10 Étape 4 — Zones & orientation

## Objectif

Découper le bâtiment en zones utiles au calcul.

## Philosophie

En mode express, on propose un **zoning assisté**.
En mode avancé, l’utilisateur peut éditer finement.

## Mode express

Assistant automatique :

* chambres nord
* chambres sud
* chambres est
* chambres ouest
* circulations
* lobby
* restaurant
* réunion
* techniques

L’utilisateur ajuste :

* surface
* nombre de chambres
* ratio vitrage
* exposition
* conditionnement

## Champs par zone

* nom
* type
* orientation
* étage optionnel
* surface
* nombre de chambres
* ratio vitrage
* infiltration
* exposition solaire
* chauffée oui/non
* refroidie oui/non

## Champs avancés

* volume
* consigne chauffage
* consigne refroidissement
* abaissement nuit
* profil d’occupation spécifique

## Validations

* somme surfaces zones ≈ surface totale ou chauffée
* nombre total de chambres zones = nombre de chambres global ± tolérance

## UX utile

* vue tableau
* vue cartes
* vue mini-schématique simplifiée

---

# 5.11 Étape 5 — Usages & occupation

## Objectif

Qualifier les rythmes d’usage.

## Champs express

* taux d’occupation annuel moyen
* saisonnalité

  * stable
  * été fort
  * hiver fort
  * très saisonnier
* intensité d’usage chambres
* restaurant actif oui/non
* séminaires / réunion oui/non
* ECS :

  * standard
  * élevée
  * très élevée

## Champs avancés

* profil mensuel
* profil semaine/week-end
* horaires restaurant
* fréquence ménage / housekeeping
* taux de rotation chambres
* occupation par type de zone

## Cas métier hôtel

Section dédiée :

* chambres inoccupées en journée ?
* check-in/check-out marqués ?
* usage nocturne important ?
* occupation irrégulière ?

## Impact UI

Montrer un encart :

* “vos hypothèses d’occupation influencent surtout ECS, refroidissement et ventilation”.

---

# 5.12 Étape 6 — Systèmes techniques

## Objectif

Décrire les systèmes existants avec un langage simple.

## Sous-sections

* chauffage
* refroidissement
* ventilation
* ECS
* éclairage
* auxiliaires / pompes / ventilateurs
* supervision / GTB existante

## Champs express par système

* technologie
* source d’énergie
* niveau de performance
* centralisé ou non
* niveau de régulation
* âge estimé

## Exemples de sélecteurs

### Chauffage

* chaudière gaz
* PAC
* réseau chaleur
* électrique
* autre

### Refroidissement

* split / DRV
* groupe froid
* PAC réversible
* pas de froid
* autre

### Ventilation

* naturelle
* simple flux
* double flux
* CTA
* pas de ventilation mécanique

### ECS

* ballon
* production centralisée
* PAC ECS
* solaire + appoint
* autre

### Éclairage

* LED
* mixte
* fluorescent
* ancien

## Champs avancés

* puissance
* distribution
* terminals
* récupération
* bouclage ECS
* variation de vitesse
* horaires

## UX

Chaque système a un statut visuel :

* performant
* standard
* perfectible
* inconnu

---

# 5.13 Étape 7 — BACS actuel

## Objectif

Évaluer automatiquement la maturité actuelle.

## Structure

Questionnaire par domaines :

* chauffage
* refroidissement
* ventilation
* ECS
* éclairage
* supervision
* monitoring énergétique
* automatisation chambre

## Format des questions

* Oui / Non / Partiel / Inconnu
* parfois avec portée :

  * tout le bâtiment
  * certaines zones
  * seulement chambres
  * seulement espaces communs

## Exemples

### Chambres

* mode absence ?
* détection fenêtre ouverte ?
* mode nuit ?
* badge/carte présence ?
* limitation consigne ?

### Chauffage/froid

* programmation horaire ?
* régulation locale ?
* supervision centralisée ?
* abaissement automatique ?

### Ventilation

* horaire ?
* présence ?
* CO₂ ?

### Monitoring

* sous-comptage ?
* alertes dérive ?
* tableaux de bord ?

## Résultat à l’écran

* score global BACS
* classe estimée A/B/C/D
* niveau de confiance
* top fonctions manquantes

## Possibilité

* modification manuelle de la classe finale
* affichage “calculée / modifiée”

---

# 5.14 Étape 8 — Scénarios / bouquets

## Objectif

Construire les variantes d’amélioration.

## Composants d’écran

* colonne gauche : bibliothèque de solutions
* centre : scénario en cours
* droite : impact estimatif live

## Types de scénarios proposés

* scénario de référence
* optimisation chambres
* optimisation BACS
* optimisation éclairage
* optimisation ventilation
* bouquet complet
* scénario personnalisé

## Actions

* ajouter une solution
* cibler tout le bâtiment
* cibler une zone
* cibler un système
* dupliquer un scénario
* comparer

## Bibliothèque de solutions

Filtres :

* famille
* pays
* usage
* impact ROI
* impact BACS
* applicable à l’hôtel ou non

## Sur chaque solution

* description
* gains attendus
* CAPEX indicatif
* usages affectés
* impact BACS
* conditions d’applicabilité

## Cas métier clé

L’utilisateur doit pouvoir construire vite un scénario du type :

* chambres sud : mode absence + fenêtre ouverte + mode nuit
* circulations : détection présence éclairage
* ventilation : horaire + CO₂
* ECS : optimisation température/bouclage

---

# 5.15 Étape 9 — Résultats comparatifs

## Objectif

Donner une lecture immédiate et commerciale.

## En-tête KPI

Pour chaque scénario :

* énergie avant / après
* économies %
* CO₂ avant / après
* CAPEX
* économies annuelles
* payback
* VAN
* TRI
* classe BACS avant / après

## Vues recommandées

### Vue 1 — Cartes KPI

Affichage synthétique.

### Vue 2 — Tableau comparatif

Colonnes = scénarios
Lignes = usages, coûts, CO₂, BACS.

### Vue 3 — Répartition par usage

* chauffage
* refroidissement
* ventilation
* ECS
* éclairage
* auxiliaires

### Vue 4 — Répartition par zone

Très importante commercialement.

### Vue 5 — Top leviers

Liste des actions les plus contributives.

## Messages automatiques

Exemples :

* poste dominant
* zone la plus contributive
* meilleure rentabilité
* plus fort impact BACS
* scénario recommandé

---

# 5.16 Étape 10 — Rapport

## Objectif

Produire un livrable immédiatement exploitable.

## Options

* rapport court
* rapport détaillé

## Paramètres

* langue
* branding
* scénario seul ou comparaison multi-scénarios
* inclure hypothèses
* inclure annexes techniques
* inclure section réglementaire

## Prévisualisation

L’écran doit montrer :

* sommaire
* couverture
* résumé exécutif
* aperçu des graphiques

## Actions

* générer PDF
* télécharger
* régénérer
* historiser

---

# 5.17 Écran Comparateur hors wizard

## Objectif

Comparer librement plusieurs scénarios après la saisie.

## Fonctionnalités

* sélectionner 2 à 5 scénarios
* choisir indicateurs affichés
* mettre en avant le scénario de référence
* exporter visuel ou PDF

## Vues

* tableau
* radar de scores
* barres avant/après
* plan d’action priorisé

---

# 5.18 Écran Hypothèses

## Objectif

Rendre l’outil transparent.

## Contenu

* hypothèses pays
* climat
* intensités de référence
* coefficients utilisés
* fonctions BACS appliquées
* paramètres économiques
* version du moteur

## UX

Pas destiné au commercial en premier niveau, mais accessible.

---

# 5.19 Écran Historique

## Objectif

Tracer les modifications.

## Contenu

* qui a modifié quoi
* derniers calculs
* changements de scénarios
* génération de rapports
* version catalogue/hypothèses

---

# 5.20 Écran Modèles de projets

## Objectif

Accélérer la création.

## Fonctionnalités

* créer un modèle
* dupliquer un modèle
* définir un zoning standard
* définir des usages standard
* définir un jeu de solutions favori

## Exemples de modèles

* hôtel urbain standard
* hôtel avec restaurant
* hôtel avec spa
* résidence hôtelière

---

# 5.21 Écran Catalogue de solutions

## Objectif

Administrer la bibliothèque.

## Fonctions

* voir catalogue global
* voir catalogue pays
* voir catalogue entreprise
* ajouter une offre commerciale
* activer/désactiver
* éditer gains / CAPEX / durée de vie / pays

## Filtres

* pays
* type bâtiment
* famille
* impact BACS
* commercial / standard

---

# 5.22 Écran Administration

## Sous-sections

* utilisateurs
* rôles
* branding
* paramètres pays
* hypothèses moteur
* messages automatiques
* modèles de rapport

## Important

Les paramètres de calcul doivent être séparés des paramètres purement UI.

---

# 5.23 Validations UX globales

## Règles

* autosave permanent
* avertissement si zones incohérentes
* avertissement si trop de données manquantes
* possibilité de calcul avec données incomplètes, mais avec badge :

  * confiance faible
  * confiance moyenne
  * confiance élevée

## États des champs

* renseigné
* estimé
* par défaut
* inconnu

C’est très utile pour la confiance utilisateur.

---

# 5.24 Mode express vs avancé

## Mode express

Visible par défaut :

* peu de champs
* listes simples
* hypothèses standard
* rapide

## Mode avancé

Déployable section par section :

* plus de paramètres
* coefficients ajustables
* profils détaillés
* zones fines
* réglages économiques détaillés

## Règle UX

Le passage en avancé ne doit jamais casser le flux express.

---

# 5.25 Aides contextuelles

Chaque étape doit proposer :

* une phrase “à quoi sert cette étape”
* une phrase “ce qui influence le plus le résultat”
* des info-bulles simples
* éventuellement un lien “voir les hypothèses”

---

# 5.26 États du projet

## États recommandés

* brouillon
* en cours
* prêt à calculer
* calculé
* rapport généré
* archivé

---

# 5.27 Responsive

## Recommandation

* desktop prioritaire
* tablette acceptable
* mobile limité à consultation légère

Vu la richesse des écrans, un vrai usage mobile de production ne me paraît pas prioritaire.

---

# 5.28 Décisions UX que je recommande de figer

Je recommande de figer :

* wizard en **10 étapes**
* **mode express par défaut**
* **mode avancé par section**
* zoning assisté
* questionnaire BACS visuel
* comparateur multi-scénarios
* rapport court + détaillé
* hypothèses accessibles mais secondaires
* positionnement très **commercial**

---
