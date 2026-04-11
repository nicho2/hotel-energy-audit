
# 3. Moteur de calcul simplifié

## 3.1 Positionnement du moteur

Le moteur doit produire des **ordres de grandeur crédibles** et surtout des **écarts relatifs fiables** entre :

* état initial,
* scénario A,
* scénario B,
* bouquet complet.

Il doit donc être optimisé pour :

* la **comparaison**,
* la **transparence des hypothèses**,
* la **rapidité de recalcul**,
* la **traçabilité**.

Il ne doit pas chercher à faire de la simulation thermique dynamique horaire.

---

## 3.2 Philosophie générale de calcul

Le calcul repose sur 5 couches successives :

1. **caractérisation simplifiée du bâtiment**
2. **estimation des usages énergétiques de référence**
3. **corrections par zones, orientation, climat et occupation**
4. **application des solutions et fonctions BACS**
5. **conversion en coûts, CO₂ et ROI**

Autrement dit :

**Bâtiment + zones + usages + systèmes + BACS + bouquet = résultats consolidés**

---

## 3.3 Sorties attendues du moteur

Le moteur doit calculer au minimum :

### Résultats énergétiques

* consommation annuelle estimée totale
* consommation annuelle par usage :

  * chauffage
  * refroidissement
  * ventilation
  * ECS
  * éclairage
  * auxiliaires
* consommation par m²
* consommation par zone

### Résultats carbone

* émissions annuelles avant / après
* gain CO₂ absolu et relatif

### Résultats BACS

* classe estimée actuelle
* classe estimée cible
* fonctions présentes / absentes / ajoutées
* gains attribuables à l’automatisation

### Résultats économiques

* CAPEX
* OPEX annuel
* économies annuelles
* payback simple
* VAN
* TRI
* cash-flow simplifié

### Résultats commerciaux

* score projet
* top actions contributrices
* plan d’action priorisé

---

# 3.4 Structure logique du calcul

## Étape 1 — baseline bâtiment

Construire un état initial à partir de :

* typologie bâtiment
* période de construction
* climat
* surface
* nombre d’étages
* nombre de chambres
* zones
* systèmes existants
* profils d’usage

## Étape 2 — baseline énergétique par usage

Calculer les besoins/consommations de référence :

* chauffage
* refroidissement
* ventilation
* ECS
* éclairage
* auxiliaires

## Étape 3 — baseline BACS

Déterminer :

* fonctions présentes
* classe BACS actuelle
* potentiel d’amélioration

## Étape 4 — application scénario

Appliquer un bouquet :

* solutions techniques
* fonctions BACS supplémentaires
* réglages chambres
* ciblage zones / orientation

## Étape 5 — consolidation

Produire :

* avant / après
* gains
* économies
* ROI
* messages de synthèse

---

# 3.5 Méthode de calcul du baseline énergétique

## 3.5.1 Principe

Le moteur ne calcule pas directement par conduction détaillée par paroi comme un moteur réglementaire complet.
Il utilise une approche **semi-physique simplifiée** :

* une **intensité énergétique de référence** par usage,
* corrigée par des **facteurs multiplicatifs**,
* puis répartie par zones.

### Forme générale

Pour chaque usage `u` :

[
E_u = E_{ref,u} \times F_{climat} \times F_{enveloppe} \times F_{occupation} \times F_{systeme} \times F_{zone/orientation} \times F_{BACS}
]

Cette structure est simple, explicable, et adaptée à un outil d’audit rapide.

---

## 3.5.2 Usages calculés

### A. Chauffage

Basé sur :

* climat
* période de construction
* compacité
* surface chauffée
* orientation/zones
* consignes
* infiltration
* qualité enveloppe
* efficacité système
* régulation

### B. Refroidissement

Basé sur :

* climat de refroidissement
* orientation solaire
* surface vitrée
* exposition solaire
* occupation
* charges internes
* consignes
* présence de climatisation
* régulation

### C. Ventilation

Basé sur :

* typologie des zones
* intensité d’usage
* présence ou non de ventilation mécanique
* récupération éventuelle
* pilotage horaire / occupation

### D. ECS

Très important pour l’hôtellerie.
Basé sur :

* nombre de chambres
* taux d’occupation
* profil hôtelier
* présence restaurant/spa/piscine
* technologie ECS
* pilotage ECS

### E. Éclairage

Basé sur :

* surface par zone
* type d’espace
* niveau technologique
* durée d’usage
* détection / gradation / programmation

### F. Auxiliaires

Basé sur :

* complexité des systèmes
* ventilation/pompes
* fonctionnement
* présence de variation de vitesse / optimisation

---

# 3.6 Méthode de calcul simplifiée par usage

## 3.6.1 Chauffage

### Formule conceptuelle

[
E_{heat} = A_{chauffee} \times I_{heat,ref} \times F_{climat} \times F_{construction} \times F_{compacite} \times F_{infiltration} \times F_{consigne} \times F_{regulation}
]

### Variables principales

* `A_chauffee` : surface chauffée
* `I_heat_ref` : intensité chauffage de référence
* `F_climat` : sévérité climatique
* `F_construction` : qualité enveloppe estimée selon période
* `F_compacite` : bâtiment compact ou non
* `F_infiltration` : niveau d’étanchéité supposé
* `F_consigne` : température de consigne
* `F_regulation` : qualité de régulation

### Exemple métier

Un hôtel ancien, peu compact, avec chambres nord/sud, régulation faible et programmation absente aura un `E_heat` sensiblement plus élevé qu’un hôtel récent avec gestion par chambre et abaissement nocturne.

---

## 3.6.2 Refroidissement

### Formule conceptuelle

[
E_{cool} = A_{refroidie} \times I_{cool,ref} \times F_{climat,cool} \times F_{solar} \times F_{vitrage} \times F_{occupation} \times F_{consigne,cool} \times F_{control}
]

### Variables clés

* orientation
* exposition solaire
* ratio vitrage
* occupation zones
* présence de chambres sud
* mode nuit
* coupure sur absence
* fenêtre ouverte

### Point fort produit

La prise en compte des **chambres sud** et des stratégies du type :

* **absence**
* **fenêtre ouverte**
* **mode nuit**
  doit être explicite, car c’est très parlant commercialement et cohérent avec la logique des fonctions d’automatisation.

---

## 3.6.3 Ventilation

### Formule conceptuelle

[
E_{vent} = A \times I_{vent,ref} \times F_{usage} \times F_{horaire} \times F_{pilotage} \times F_{recuperation}
]

### Variables

* type de zone
* fonctionnement continu ou horaire
* présence d’asservissement
* détection présence / CO₂
* récupération chaleur éventuelle

---

## 3.6.4 ECS

### Formule conceptuelle

[
E_{dhw} = N_{rooms} \times Occ \times I_{dhw,room} \times F_{services} \times F_{systeme} \times F_{control}
]

### Variables

* nombre de chambres
* taux d’occupation
* profil hôtelier
* restaurant
* spa / piscine
* rendement production ECS
* bouclage / pertes estimées
* programmation / optimisation

### Important

Dans l’hôtellerie, l’ECS doit être traitée comme un poste majeur, souvent plus déterminant qu’en tertiaire classique.

---

## 3.6.5 Éclairage

### Formule conceptuelle

[
E_{light} = \sum_{zones} (A_z \times I_{light,z} \times H_z \times F_{techno} \times F_{control})
]

### Variables

* type de zone
* durée d’usage
* techno éclairage
* détection présence
* extinction horaire
* gradation / lumière du jour

---

## 3.6.6 Auxiliaires

Approche simplifiée :

* pourcentage des autres usages,
* ou intensité forfaitaire selon complexité système.

Cela restera suffisant en V1.

---

# 3.7 Décomposition par zones et orientation

## 3.7.1 Principe

Le moteur doit d’abord répartir la surface et les usages par zones :

* chambres nord
* chambres sud
* chambres est
* chambres ouest
* lobby
* restaurant
* réunion
* circulation
* techniques

Ensuite, il applique des coefficients spécifiques.

## 3.7.2 Pourquoi c’est crucial

Cela permet de démontrer concrètement :

* qu’une action sur les **chambres sud** a plus d’effet sur le refroidissement,
* qu’une fonction **fenêtre ouverte** touche surtout certaines zones,
* qu’un profil **absence chambre** agit sur chauffage/refroidissement et parfois ventilation/éclairage.

---

# 3.8 Calcul du baseline BACS

## 3.8.1 Référence méthodologique

La logique doit suivre les familles de fonctions de l’**EN ISO 52120-1**, qui relie les fonctions d’automatisation et de contrôle à la performance énergétique des bâtiments. Des outils industriels utilisent déjà cette logique pour classer les bâtiments en A/B/C/D et estimer des gains.

## 3.8.2 Mécanisme

Le questionnaire renseigne :

* présence de programmation horaire
* régulation locale
* supervision centralisée
* monitoring
* détection présence
* coupure sur fenêtre ouverte
* mode absence
* optimisation ECS
* variation de vitesse
* etc.

Chaque réponse alimente :

* un **score par domaine**
* une **classe BACS estimée**
* une **liste de fonctions absentes mais pertinentes**

## 3.8.3 Sortie

* `estimated_bacs_class_current`
* `bacs_gap_to_target`
* `high_impact_missing_functions`

---

# 3.9 Calcul des gains BACS

## 3.9.1 Principe

Les gains BACS ne doivent pas être appliqués comme une réduction globale arbitraire unique.
Ils doivent être appliqués :

* par **usage**,
* éventuellement par **zone**,
* avec **règles d’éligibilité**.

## 3.9.2 Exemples de logique

* **absence chambre** : impact sur chauffage, refroidissement, parfois éclairage
* **fenêtre ouverte** : impact sur chauffage/refroidissement des chambres concernées
* **mode nuit** : impact sur chauffage/refroidissement selon consignes
* **programmation horaire ventilation** : impact sur ventilation et auxiliaires
* **détection présence circulations** : impact éclairage
* **suivi énergétique / supervision** : impact plus diffus, plutôt sur optimisation globale

## 3.9.3 Règle de calcul recommandée

Chaque fonction BACS fournit un `impact model` :

* usages concernés,
* type de zones concernées,
* conditions d’application,
* facteur de gain par défaut,
* borne min/max.

---

# 3.10 Calcul des gains des solutions techniques

## 3.10.1 Principe

Chaque solution du catalogue contient un modèle d’impact, par exemple :

* gain direct en %
* gain forfaitaire
* gain dépendant du système existant
* gain dépendant de la zone

## 3.10.2 Cas typiques

* LED + détection → éclairage
* PAC → chauffage/refroidissement
* récupération ventilation → ventilation/chauffage
* régulation terminale → chauffage/refroidissement
* isolation → chauffage principalement
* calorifuge ECS → ECS
* GTB / supervision → optimisation transverse

---

# 3.11 Gestion des gains combinés

C’est un point essentiel.

## 3.11.1 Problème

On ne peut pas additionner naïvement :

* 10 % + 15 % + 20 % = 45 %

Cela surévalue presque toujours les gains.

## 3.11.2 Règle recommandée

Appliquer les gains **séquentiellement sur un résiduel** :

[
E_{after} = E_{before} \times (1-g_1) \times (1-g_2) \times (1-g_3)
]

### Exemple

* base = 100
* gain 1 = 10 %
* gain 2 = 20 %

Résultat :
[
100 \times 0.90 \times 0.80 = 72
]

Gain total = 28 %, pas 30 %.

## 3.11.3 Avantage

* plus réaliste
* simple à expliquer
* évite le double comptage

---

# 3.12 Gestion des incompatibilités et dépendances

Le moteur doit intégrer 3 notions :

### A. Prérequis

Exemple :

* une supervision avancée suppose une base de comptage / remontée

### B. Exclusivité

Exemple :

* deux solutions incompatibles sur le même système

### C. Rendement décroissant

Exemple :

* une régulation pièce par pièce apporte moins si un pilotage avancé est déjà présent

Cela doit être porté par les métadonnées du catalogue.

---

# 3.13 Calcul des coûts et du ROI

## 3.13.1 Coûts annuels énergie

[
Cost_{energy} = \sum_{u} E_u \times Price_{energy,u}
]

Selon le mix :

* électricité
* gaz
* réseau chaleur

## 3.13.2 Économies annuelles

[
Savings_{annual} = Cost_{before} - Cost_{after}
]

## 3.13.3 Payback simple

[
Payback = \frac{CAPEX - Subsidies}{Savings_{annual} + MaintenanceSavings}
]

## 3.13.4 VAN

Calculée sur une période donnée avec :

* taux d’actualisation
* inflation énergie
* maintenance
* remplacements

## 3.13.5 TRI

Calcul standard à partir des cash-flows.

## 3.13.6 Pourquoi ces trois indicateurs

Pour un exploitant/commercial :

* **payback** = lecture immédiate
* **VAN** = arbitrage sérieux
* **TRI** = utile pour projets plus structurés

---

# 3.14 Calcul CO₂

## 3.14.1 Principe

[
CO2 = \sum_{sources} E_{source} \times Factor_{CO2,source}
]

Les facteurs doivent venir du `CountryProfile` / `AssumptionSet`.
Le résultat doit être fourni :

* avant
* après
* gain absolu
* gain relatif

## 3.14.2 Intérêt

Permet une lecture alignée avec la trajectoire décarbonation européenne de l’EPBD.

---

# 3.15 Calcul du score global projet

Je recommande un **score composite** sur 100, non réglementaire, purement commercial.

## Structure proposée

* 35 % performance énergétique
* 20 % performance économique
* 20 % maturité BACS
* 15 % impact CO₂
* 10 % simplicité de déploiement

Cela permet d’avoir :

* un visuel simple,
* un classement des scénarios,
* un angle commercial lisible.

---

# 3.16 Gestion des incertitudes

Le moteur doit afficher :

* hypothèses utilisées
* niveau de confiance
* facteurs les plus sensibles

## Recommandation

Ajouter pour certains résultats une **plage indicative** :

* basse
* centrale
* haute

Sans faire une vraie simulation Monte Carlo en V1.

---

# 3.17 Pseudocode du calcul

```text
1. Charger projet, bâtiment, zones, usages, systèmes
2. Charger pays, climat, hypothèses, catalogue
3. Construire baseline par usage et par zone
4. Évaluer BACS actuel
5. Initialiser scénario = baseline
6. Pour chaque solution du bouquet :
    - vérifier applicabilité
    - appliquer impact par usage/zone
    - gérer dépendances/incompatibilités
7. Recalculer classe BACS cible
8. Consolider consommations avant/après
9. Convertir en coûts et CO₂
10. Calculer ROI
11. Calculer score global
12. Générer messages de synthèse et top gains
13. Enregistrer snapshots + résultats
```

---

# 3.18 Messages métier générés automatiquement

Le moteur doit aussi produire des phrases prêtes pour le rapport, par exemple :

* “Le poste chauffage reste dominant dans l’état actuel.”
* “Les chambres sud concentrent le principal potentiel de réduction du refroidissement.”
* “Le bouquet proposé améliore la classe BACS estimée de C vers B.”
* “La stratégie absence + fenêtre ouverte + mode nuit constitue le principal levier sur les chambres.”
* “Le temps de retour simple du bouquet est estimé à 4,8 ans.”

C’est important pour une restitution commerciale.

---

# 3.19 Paramètres à rendre configurables

À ne pas figer dans le code :

* intensités de référence par usage
* coefficients climat
* coefficients enveloppe
* coefficients occupation
* coefficients orientation
* facteurs de gains BACS
* facteurs CO₂
* paramètres économiques
* bornes et planchers/plafonds de gains

---

# 3.20 Décisions de conception que je recommande de figer

Je recommande de figer ceci :

* moteur **annuel simplifié**
* calcul **par usage + par zone**
* orientation intégrée
* **chambres** traitées comme zone métier centrale
* gains **séquentiels sur résiduel**
* BACS calculé par **fonctions élémentaires**
* ROI = **payback + VAN + TRI**
* score global commercial
* hypothèses et snapshots toujours visibles

---
