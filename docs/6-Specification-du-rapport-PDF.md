
# 6. Spécification du rapport PDF

## 6.1 Objectifs du rapport

Le rapport doit servir simultanément à 4 usages :

1. **support commercial**
2. **synthèse d’audit simplifié**
3. **comparaison de scénarios**
4. **trace formelle du calcul réalisé**

Il doit pouvoir être remis à :

* un client,
* une direction d’exploitation,
* un exploitant technique,
* un intégrateur / commercial interne.

---

## 6.2 Types de rapports à produire

Je recommande **2 formats natifs**.

### A. Rapport exécutif

Court, visuel, orienté décision.

#### Cible

* direction
* client final
* commercial

#### Taille cible

* **8 à 15 pages**

#### Usage

* rendez-vous commercial
* présentation de synthèse
* arbitrage rapide

---

### B. Rapport détaillé

Plus complet, avec hypothèses et détails de calcul.

#### Cible

* exploitant
* direction technique
* bureau interne
* archivage

#### Taille cible

* **20 à 40 pages**

#### Usage

* validation interne
* justification d’une préconisation
* base de travail ultérieure

---

## 6.3 Paramètres de génération

L’utilisateur doit pouvoir choisir :

* langue : `FR` / `EN`
* type de rapport : `executive` / `detailed`
* scénario unique ou comparaison multi-scénarios
* branding
* inclusion des hypothèses
* inclusion de la section réglementaire
* inclusion des annexes
* niveau de détail économique

---

# 6.4 Structure générale du rapport

Je recommande cette structure.

## 1. Couverture

## 2. Résumé exécutif

## 3. Contexte du projet

## 4. Description du bâtiment

## 5. État initial estimé

## 6. Analyse BACS actuelle

## 7. Scénarios étudiés

## 8. Comparaison des résultats

## 9. Analyse économique

## 10. Recommandation / plan d’action

## 11. Cadre réglementaire ou contexte pays

## 12. Hypothèses et limites

## 13. Annexes techniques

Le rapport exécutif peut condenser plusieurs sections.

---

# 6.5 Couverture

## Contenu

* logo / branding
* titre du rapport
* nom du projet
* nom du client
* type de bâtiment
* pays
* date
* éventuellement sous-titre :

  * “Audit énergétique simplifié”
  * “Étude de scénarios d’amélioration”
  * “Analyse BACS et ROI”

## Exemple de titre

**Étude d’optimisation énergétique et d’automatisation — Hôtel / bâtiment d’hébergement**

## Variantes

La couverture doit être entièrement personnalisable via le branding :

* logo
* couleurs
* pied de page
* texte légal

---

# 6.6 Résumé exécutif

C’est la section la plus importante.

## Objectif

Donner en 1 à 2 pages :

* le niveau de performance estimé actuel,
* le meilleur potentiel identifié,
* le scénario recommandé,
* les gains attendus,
* le ROI.

## Contenu recommandé

* 5 à 7 KPI majeurs
* 3 messages clés
* 1 tableau de synthèse des scénarios
* 1 recommandation finale

## KPI à afficher

* consommation énergétique estimée annuelle
* économie potentielle (%)
* réduction CO₂ (%)
* classe BACS actuelle
* classe BACS cible
* CAPEX du scénario recommandé
* payback simple
* VAN

## Messages automatiques type

* “Le principal potentiel d’amélioration est concentré sur les chambres et les automatismes associés.”
* “Le scénario recommandé améliore la classe BACS estimée de C à B.”
* “Le temps de retour simple du bouquet recommandé est estimé à X années.”

---

# 6.7 Contexte du projet

## Objectif

Poser le cadre commercial et méthodologique.

## Contenu

* objectif du projet
* profil du client
* pays / contexte
* type de bâtiment
* portée de l’étude
* date de réalisation
* langue du rapport

## Texte standard

Cette section doit aussi rappeler que l’étude est :

* une **estimation simplifiée**,
* fondée sur les données saisies et les hypothèses standard du moteur,
* destinée à l’aide à la décision et à la comparaison de scénarios.

---

# 6.8 Description du bâtiment

## Objectif

Présenter les caractéristiques prises en compte.

## Contenu

* surface totale
* surface chauffée
* surface refroidie
* nombre d’étages
* nombre de chambres
* période de construction
* zone climatique
* compacité
* orientation principale
* services présents :

  * restaurant
  * réunion
  * spa
  * piscine

## Option détaillée

Ajouter un tableau par zone :

* nom zone
* type
* orientation
* surface
* chambres
* conditionnée oui/non
* remarques

## Visuel utile

* diagramme simple de répartition des surfaces par zone
* diagramme de répartition des orientations des chambres

---

# 6.9 État initial estimé

## Objectif

Présenter la situation de départ.

## Contenu

* énergie annuelle totale estimée
* intensité énergétique estimée
* répartition par usage
* répartition par zone
* émissions CO₂
* principaux postes de consommation
* niveau de confiance

## Tableaux recommandés

### Tableau 1 — Synthèse énergétique

| Indicateur             | Valeur |
| ---------------------- | -----: |
| Énergie totale estimée |    ... |
| Intensité énergétique  |    ... |
| CO₂ estimé             |    ... |
| Confiance              |    ... |

### Tableau 2 — Répartition par usage

| Usage           | kWh/an |   % |
| --------------- | -----: | --: |
| Chauffage       |    ... | ... |
| Refroidissement |    ... | ... |
| Ventilation     |    ... | ... |
| ECS             |    ... | ... |
| Éclairage       |    ... | ... |
| Auxiliaires     |    ... | ... |

### Tableau 3 — Répartition par zone

| Zone          | kWh/an |   % | Commentaire |
| ------------- | -----: | --: | ----------- |
| Chambres sud  |    ... | ... | ...         |
| Chambres nord |    ... | ... | ...         |
| Lobby         |    ... | ... | ...         |

## Messages automatiques

* poste dominant
* sensibilité à l’occupation
* sensibilité à l’orientation
* importance de l’ECS

---

# 6.10 Analyse BACS actuelle

## Objectif

Rendre la logique BACS compréhensible et actionnable.

## Contenu

* score BACS global estimé
* classe actuelle estimée
* niveau de confiance
* score par domaine
* fonctions présentes
* fonctions absentes à fort impact

## Tableau recommandé

| Domaine                | Score | Niveau | Commentaire |
| ---------------------- | ----: | -----: | ----------- |
| Chauffage              |   ... |    ... | ...         |
| Refroidissement        |   ... |    ... | ...         |
| Ventilation            |   ... |    ... | ...         |
| ECS                    |   ... |    ... | ...         |
| Éclairage              |   ... |    ... | ...         |
| Supervision            |   ... |    ... | ...         |
| Monitoring             |   ... |    ... | ...         |
| Automatisation chambre |   ... |    ... | ...         |

## Bloc essentiel

**Top fonctions manquantes**

* mode absence chambres
* fenêtre ouverte
* programmation ventilation
* détection présence éclairage
* supervision énergétique

---

# 6.11 Scénarios étudiés

## Objectif

Présenter clairement les bouquets construits.

## Pour chaque scénario

* nom
* description
* logique du bouquet
* zones concernées
* systèmes concernés
* impact attendu

## Tableau recommandé

| Scénario              | Description courte          | Cible principale |
| --------------------- | --------------------------- | ---------------- |
| Référence             | État actuel                 | bâtiment         |
| Optimisation chambres | Automatismes chambres       | chambres         |
| BACS + ventilation    | Pilotage GTB et ventilation | chambres + CTA   |
| Bouquet complet       | Ensemble cohérent           | bâtiment         |

## Bon usage

Cette section doit être très lisible.
Elle prépare mentalement le lecteur avant le comparatif chiffré.

---

# 6.12 Comparaison des résultats

C’est le cœur décisionnel du rapport.

## Objectif

Comparer plusieurs scénarios sur un format immédiatement compréhensible.

## Tableau maître recommandé

| Indicateur              | Référence | Scénario A | Scénario B | Scénario C |
| ----------------------- | --------: | ---------: | ---------: | ---------: |
| Énergie totale (kWh/an) |       ... |        ... |        ... |        ... |
| Économies (%)           |         - |        ... |        ... |        ... |
| CO₂ (kg/an)             |       ... |        ... |        ... |        ... |
| Réduction CO₂ (%)       |         - |        ... |        ... |        ... |
| Classe BACS             |         C |          B |          B |          A |
| CAPEX                   |         - |        ... |        ... |        ... |
| Économies annuelles (€) |         - |        ... |        ... |        ... |
| Payback simple          |         - |        ... |        ... |        ... |
| VAN                     |         - |        ... |        ... |        ... |
| TRI                     |         - |        ... |        ... |        ... |

## Visuels recommandés

* barres avant/après énergie
* barres avant/après CO₂
* waterfall simplifié des gains
* histogramme CAPEX / économies
* radar synthétique des scénarios

## Messages automatiques

* meilleur scénario économique
* meilleur scénario énergétique
* meilleur scénario BACS
* meilleur compromis global

---

# 6.13 Analyse économique

## Objectif

Donner une lecture financière claire.

## Contenu

* CAPEX
* économies annuelles
* économies maintenance
* payback simple
* VAN
* TRI
* hypothèses économiques
* subventions intégrées ou non

## Tableau recommandé

| Indicateur économique       | Valeur |
| --------------------------- | -----: |
| CAPEX                       |    ... |
| Économies énergie annuelles |    ... |
| Économies maintenance       |    ... |
| Payback simple              |    ... |
| VAN                         |    ... |
| TRI                         |    ... |
| Période d’analyse           |    ... |

## Variante détaillée

Inclure un tableau de cash-flow simplifié par année.

## Message important

Le rapport doit distinguer :

* **rentabilité immédiate**
* **rentabilité long terme**
* **effet combiné énergie + maintenance + décarbonation**

---

# 6.14 Recommandation / plan d’action

## Objectif

Ne pas laisser le lecteur avec seulement des chiffres.

## Contenu

* scénario recommandé
* justification
* top actions à mettre en œuvre
* priorisation
* quick wins
* actions structurantes

## Tableau recommandé

| Priorité | Action                          | Impact énergie | Impact BACS | CAPEX | ROI | Complexité |
| -------- | ------------------------------- | -------------: | ----------: | ----: | --: | ---------: |
| 1        | Automatisation chambres         |            ... |         ... |   ... | ... |        ... |
| 2        | Détection présence circulations |            ... |         ... |   ... | ... |        ... |
| 3        | Pilotage ventilation            |            ... |         ... |   ... | ... |        ... |

## Rendu attendu

Très commercial, très concret.

---

# 6.15 Cadre réglementaire / contexte pays

## Objectif

Adapter le discours au client.

## Cas France

Afficher une section orientée :

* contexte national
* rappel sur les systèmes d’automatisation/contrôle
* décret BACS comme point d’attention informatif
* sans prétendre faire une conformité réglementaire exhaustive

## Cas UE générique

Afficher une section orientée :

* EPBD / Green Deal
* décarbonation
* performance énergétique
* automatisation et pilotage
* intérêt de la modernisation

## Règle

Cette section doit être **pédagogique**, pas juridique.

---

# 6.16 Hypothèses et limites

Section indispensable.

## Contenu

* nature simplifiée de l’outil
* données saisies par l’utilisateur
* hypothèses standard utilisées
* coefficients par défaut
* limites de précision
* finalité comparative et d’aide à la décision

## Tableau recommandé

| Domaine   | Hypothèse principale                      |
| --------- | ----------------------------------------- |
| Climat    | zone climatique standard                  |
| Enveloppe | période de construction                   |
| ECS       | profil hôtelier standard                  |
| BACS      | questionnaire déclaratif                  |
| Économie  | prix énergie standard + hypothèses projet |

## Texte type

L’étude produite constitue une estimation simplifiée destinée à comparer des scénarios d’amélioration. Elle ne remplace pas une étude réglementaire complète ni une simulation thermique dynamique détaillée.

---

# 6.17 Annexes techniques

## Rapport détaillé uniquement

Peut contenir :

* détail des zones
* détail des usages
* détail des fonctions BACS
* détail des solutions appliquées
* hypothèses économiques
* version moteur
* version hypothèses
* version catalogue
* date/calcul/trace

## Tableau utile

| Élément                | Version |
| ---------------------- | ------- |
| Moteur de calcul       | ...     |
| Jeu d’hypothèses       | ...     |
| Catalogue de solutions | ...     |
| Date de calcul         | ...     |

---

# 6.18 Graphiques recommandés

Je recommande de standardiser un petit nombre de graphiques.

## Graphique 1

Répartition énergétique par usage

## Graphique 2

Comparaison avant/après par scénario

## Graphique 3

Réduction CO₂ par scénario

## Graphique 4

CAPEX vs économies annuelles

## Graphique 5

Score BACS par domaine

## Graphique 6

Répartition du potentiel par zone

Pas plus. Un rapport surchargé devient vite moins lisible.

---

# 6.19 Ton rédactionnel

Le ton doit être :

* professionnel,
* sobre,
* orienté décision,
* non académique,
* non trop technique.

## Style recommandé

* phrases courtes
* formulations affirmatives prudentes
* vocabulaire métier accessible
* pas de jargon normatif excessif

## Exemples

Préférer :

* “Le chauffage constitue le principal poste de consommation estimé”
  à
* “Le besoin énergétique de chauffage end-use représente la dominante de l’enveloppe consommatoire”

---

# 6.20 Variantes exécutif vs détaillé

## Rapport exécutif

Garder :

* couverture
* résumé exécutif
* description bâtiment courte
* état initial synthétique
* analyse BACS synthétique
* comparaison scénarios
* ROI
* recommandation
* limites très courtes

## Rapport détaillé

Ajouter :

* description zones
* détail systèmes
* détail BACS par domaine
* hypothèses complètes
* annexes techniques
* historique/version

---

# 6.21 Règles de génération automatique de texte

Le moteur doit fournir des blocs textuels réutilisables :

* synthèse énergétique
* synthèse BACS
* synthèse économique
* recommandation
* avertissements
* limites

Ces blocs doivent être :

* paramétrables,
* traduisibles FR/EN,
* non écrits en dur dans le template PDF.

---

# 6.22 Éléments à mettre en évidence visuellement

Le rapport doit toujours faire ressortir :

* scénario recommandé
* économie potentielle
* réduction CO₂
* classe BACS cible
* payback
* top 3 actions

C’est le cœur du message commercial.

---

# 6.23 Éléments de traçabilité

Le rapport détaillé doit comporter en pied ou annexe :

* ID projet
* ID scénario
* date/heure génération
* utilisateur générateur
* version moteur
* version hypothèses
* version catalogue

Cela évite toute ambiguïté ultérieure.

---

# 6.24 Décisions que je recommande de figer

Je recommande de figer :

* 2 formats : **executive** et **detailed**
* PDF prioritaire
* résumé exécutif très visible
* comparateur multi-scénarios au centre
* section BACS dédiée
* section ROI dédiée
* section hypothèses obligatoire
* section cadre pays adaptable
* ton rédactionnel sobre et commercial

---
