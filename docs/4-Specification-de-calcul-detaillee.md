

# 4. Spécification de calcul détaillée

## 4.1 Principes de conception

Le moteur V1 doit reposer sur trois niveaux :

### Niveau 1 — intensités de référence

On part d’une **intensité énergétique de référence** par usage :

* chauffage,
* refroidissement,
* ventilation,
* ECS,
* éclairage,
* auxiliaires.

### Niveau 2 — facteurs correctifs

On applique des coefficients liés à :

* climat,
* période de construction,
* compacité,
* occupation,
* zone,
* orientation,
* système,
* BACS.

### Niveau 3 — effets scénario

On applique ensuite :

* fonctions BACS,
* solutions techniques,
* bouquets,
* effets combinés,
* règles de priorité.

---
# 4.2 Variables globales d’entrée

## 4.2.1 Données projet

* pays
* langue
* type de bâtiment d’hébergement
* objectif projet

## 4.2.2 Données bâtiment

* surface totale
* surface chauffée
* surface refroidie
* nombre d’étages
* nombre de chambres
* période de construction
* compacité
* orientation principale

## 4.2.3 Données zones

* type de zone
* orientation
* surface
* nombre de chambres si applicable
* taux de vitrage
* exposition solaire
* infiltration
* consignes chauffage/refroidissement

## 4.2.4 Données usages

* taux d’occupation moyen
* saisonnalité
* présence restaurant
* présence spa
* présence piscine
* présence salles de réunion

## 4.2.5 Données systèmes

* type chauffage
* type refroidissement
* ventilation
* ECS
* éclairage
* niveau de régulation

## 4.2.6 Données BACS

* fonctions présentes
* fonctions cibles
* mode manuel ou auto

## 4.2.7 Données économiques

* prix énergie
* inflation énergie
* taux d’actualisation
* période d’analyse
* subventions
* maintenance
* CAPEX

---

# 4.3 Intensités de référence par usage

Ces intensités sont des **valeurs produit V1 proposées** pour un bâtiment d’hébergement “moyen”, avant correction.

## 4.3.1 Tableau des intensités de référence

| Usage           |       Symbole |          Unité | Valeur V1 proposée |
| --------------- | ------------: | -------------: | -----------------: |
| Chauffage       |  `I_heat_ref` |      kWh/m².an |                 85 |
| Refroidissement |  `I_cool_ref` |      kWh/m².an |                 18 |
| Ventilation     |  `I_vent_ref` |      kWh/m².an |                 12 |
| ECS             |   `I_dhw_ref` | kWh/chambre.an |               2200 |
| Éclairage       | `I_light_ref` |      kWh/m².an |                 22 |
| Auxiliaires     |   `I_aux_ref` |      kWh/m².an |                 10 |

## 4.3.2 Remarques

* `I_dhw_ref` est exprimé **par chambre**, car c’est plus pertinent pour l’hôtellerie.
* les autres usages sont exprimés **par m²**.
* ces valeurs doivent être **paramétrables par pays et par profil d’usage**.

---

# 4.4 Coefficients climatiques

## 4.4.1 Indice de climat chauffage

| Niveau climat chauffage | Code | `F_climat_heat` |
| ----------------------- | ---: | --------------: |
| Très doux               |   H1 |            0.75 |
| Doux                    |   H2 |            0.90 |
| Moyen                   |   H3 |            1.00 |
| Froid                   |   H4 |            1.15 |
| Très froid              |   H5 |            1.30 |

## 4.4.2 Indice de climat refroidissement

| Niveau climat refroidissement | Code | `F_climat_cool` |
| ----------------------------- | ---: | --------------: |
| Très faible                   |   C1 |            0.60 |
| Faible                        |   C2 |            0.80 |
| Moyen                         |   C3 |            1.00 |
| Fort                          |   C4 |            1.20 |
| Très fort                     |   C5 |            1.40 |

## 4.4.3 Règle

Chaque `ClimateZone` doit fournir :

* un indice chauffage,
* un indice refroidissement,
* un indice solaire.

---

# 4.5 Coefficients période de construction / enveloppe

## 4.5.1 Tableau proposé

| Période    | `F_construction_heat` | `F_construction_cool` |
| ---------- | --------------------: | --------------------: |
| avant 1975 |                  1.35 |                  1.10 |
| 1975–1990  |                  1.20 |                  1.05 |
| 1991–2005  |                  1.05 |                  1.00 |
| 2006–2012  |                  0.92 |                  0.95 |
| après 2012 |                  0.82 |                  0.90 |

## 4.5.2 Logique

* plus le bâtiment est ancien, plus le besoin chauffage augmente ;
* pour le refroidissement, l’effet est plus modéré ;
* un mode avancé pourra remplacer ce coefficient par une saisie plus fine de l’enveloppe.

---

# 4.6 Coefficients de compacité

## 4.6.1 Tableau

| Niveau compacité | `F_compacity_heat` |
| ---------------- | -----------------: |
| Très compact     |               0.90 |
| Compact          |               0.97 |
| Moyen            |               1.00 |
| Peu compact      |               1.08 |
| Très peu compact |               1.18 |

## 4.6.2 Détermination

La V1 peut utiliser :

* soit une saisie utilisateur,
* soit une estimation à partir :

  * nombre d’étages,
  * surface,
  * forme générale.

---

# 4.7 Coefficients d’infiltration / étanchéité

## 4.7.1 Tableau

| Niveau infiltration | `F_infiltration_heat` | `F_infiltration_cool` |
| ------------------- | --------------------: | --------------------: |
| Faible              |                  0.92 |                  0.98 |
| Moyenne             |                  1.00 |                  1.00 |
| Forte               |                  1.10 |                  1.04 |
| Très forte          |                  1.20 |                  1.08 |

---

# 4.8 Coefficients de consigne

## 4.8.1 Chauffage

Référence V1 : **21°C**

[
F_{setpoint,heat} = 1 + 0.05 \times (T_{heat} - 21)
]

Exemples :

* 20°C → 0.95
* 21°C → 1.00
* 22°C → 1.05
* 23°C → 1.10

## 4.8.2 Refroidissement

Référence V1 : **24°C**

[
F_{setpoint,cool} = 1 - 0.06 \times (T_{cool} - 24)
]

Exemples :

* 23°C → 1.06
* 24°C → 1.00
* 25°C → 0.94
* 26°C → 0.88

---

# 4.9 Coefficients d’orientation et d’exposition solaire

## 4.9.1 Chauffage

| Orientation | `F_orientation_heat` |
| ----------- | -------------------: |
| Nord        |                 1.08 |
| Est         |                 1.02 |
| Sud         |                 0.94 |
| Ouest       |                 1.00 |
| Mixte       |                 1.00 |

## 4.9.2 Refroidissement

| Orientation | `F_orientation_cool` |
| ----------- | -------------------: |
| Nord        |                 0.88 |
| Est         |                 1.00 |
| Sud         |                 1.18 |
| Ouest       |                 1.12 |
| Mixte       |                 1.00 |

## 4.9.3 Exposition solaire

| Niveau     | `F_solar` |
| ---------- | --------: |
| Faible     |      0.90 |
| Moyenne    |      1.00 |
| Forte      |      1.12 |
| Très forte |      1.22 |

---

# 4.10 Coefficients de vitrage

## 4.10.1 Ratio vitrage simplifié

Référence V1 : **25 %**

[
F_{glazing,cool} = 1 + 0.8 \times (R_{glazing} - 0.25)
]

avec `R_glazing` exprimé en ratio.

Exemples :

* 15 % → 0.92
* 25 % → 1.00
* 35 % → 1.08
* 45 % → 1.16

Pour le chauffage, effet plus faible :

[
F_{glazing,heat} = 1 + 0.3 \times (R_{glazing} - 0.25)
]

---

# 4.11 Coefficients d’occupation

## 4.11.1 Référence

Référence taux d’occupation hôtel : **70 %**

[
F_{occ} = 0.75 + 0.5 \times Occ
]

avec `Occ` entre 0 et 1.

Exemples :

* 50 % → 1.00
* 70 % → 1.10
* 90 % → 1.20

## 4.11.2 Application par usage

| Usage           | Application occupation |
| --------------- | ---------------------- |
| Chauffage       | modérée                |
| Refroidissement | forte                  |
| Ventilation     | forte                  |
| ECS             | très forte             |
| Éclairage       | modérée                |
| Auxiliaires     | faible à modérée       |

---

# 4.12 Profils par type de zone

## 4.12.1 Coefficients zone par usage

### Chauffage

| Type de zone | `F_zone_heat` |
| ------------ | ------------: |
| Chambres     |          1.00 |
| Circulations |          0.75 |
| Lobby        |          1.10 |
| Restaurant   |          1.05 |
| Réunion      |          0.95 |
| Technique    |          0.50 |
| Spa          |          1.15 |
| Piscine      |          1.35 |

### Refroidissement

| Type de zone | `F_zone_cool` |
| ------------ | ------------: |
| Chambres     |          1.00 |
| Circulations |          0.60 |
| Lobby        |          1.20 |
| Restaurant   |          1.15 |
| Réunion      |          1.10 |
| Technique    |          0.40 |
| Spa          |          1.10 |
| Piscine      |          0.70 |

### Éclairage

| Type de zone | `F_zone_light` |
| ------------ | -------------: |
| Chambres     |           1.00 |
| Circulations |           0.80 |
| Lobby        |           1.25 |
| Restaurant   |           1.20 |
| Réunion      |           1.10 |
| Technique    |           0.70 |
| Spa          |           1.10 |
| Piscine      |           0.90 |

### Ventilation

| Type de zone | `F_zone_vent` |
| ------------ | ------------: |
| Chambres     |          1.00 |
| Circulations |          0.60 |
| Lobby        |          1.10 |
| Restaurant   |          1.30 |
| Réunion      |          1.20 |
| Technique    |          0.50 |
| Spa          |          1.25 |
| Piscine      |          1.40 |

---

# 4.13 Formules détaillées par usage

## 4.13.1 Chauffage

### Formule bâtiment/zone

[
E_{heat,z} = A_z \times I_{heat,ref} \times F_{climat,heat} \times F_{construction,heat} \times F_{compacity} \times F_{infiltration,heat} \times F_{setpoint,heat} \times F_{orientation,heat} \times F_{zone,heat} \times F_{system,heat} \times F_{BACS,heat}
]

### `F_system_heat` proposé

| Niveau système chauffage | `F_system_heat` |
| ------------------------ | --------------: |
| Très performant          |            0.80 |
| Performant               |            0.90 |
| Standard                 |            1.00 |
| Faible                   |            1.12 |
| Très faible              |            1.25 |

---

## 4.13.2 Refroidissement

[
E_{cool,z} = A_z \times I_{cool,ref} \times F_{climat,cool} \times F_{solar} \times F_{glazing,cool} \times F_{setpoint,cool} \times F_{orientation,cool} \times F_{zone,cool} \times F_{occ,cool} \times F_{system,cool} \times F_{BACS,cool}
]

### `F_system_cool`

| Niveau système froid | `F_system_cool` |
| -------------------- | --------------: |
| Très performant      |            0.82 |
| Performant           |            0.92 |
| Standard             |            1.00 |
| Faible               |            1.10 |
| Très faible          |            1.22 |

---

## 4.13.3 Ventilation

[
E_{vent,z} = A_z \times I_{vent,ref} \times F_{zone,vent} \times F_{occ,vent} \times F_{schedule,vent} \times F_{system,vent} \times F_{BACS,vent}
]

### `F_schedule_vent`

| Fonctionnement                 | `F_schedule_vent` |
| ------------------------------ | ----------------: |
| Continu                        |              1.15 |
| Journée étendue                |              1.00 |
| Horaire optimisé               |              0.88 |
| Asservi présence / qualité air |              0.75 |

---

## 4.13.4 ECS

[
E_{dhw} = N_{rooms} \times I_{dhw,ref} \times F_{occ,dhw} \times F_{services,dhw} \times F_{system,dhw} \times F_{BACS,dhw}
]

### `F_occ_dhw`

[
F_{occ,dhw} = 0.50 + Occ
]

Exemples :

* 50 % → 1.00
* 70 % → 1.20
* 90 % → 1.40

### `F_services_dhw`

| Services présents          | `F_services_dhw` |
| -------------------------- | ---------------: |
| Aucun service additionnel  |             1.00 |
| Restaurant                 |             1.08 |
| Spa                        |             1.18 |
| Piscine                    |             1.12 |
| Restaurant + spa           |             1.24 |
| Restaurant + spa + piscine |             1.32 |

### `F_system_dhw`

| Niveau système ECS | `F_system_dhw` |
| ------------------ | -------------: |
| Très performant    |           0.82 |
| Performant         |           0.92 |
| Standard           |           1.00 |
| Faible             |           1.10 |
| Très faible        |           1.20 |

---

## 4.13.5 Éclairage

[
E_{light,z} = A_z \times I_{light,ref} \times F_{zone,light} \times F_{schedule,light} \times F_{tech,light} \times F_{BACS,light}
]

### `F_tech_light`

| Technologie éclairage | `F_tech_light` |
| --------------------- | -------------: |
| LED + gradation       |           0.65 |
| LED                   |           0.78 |
| Mixte                 |           0.92 |
| Fluorescent           |           1.00 |
| Ancien / halogène     |           1.20 |

---

## 4.13.6 Auxiliaires

[
E_{aux} = (E_{heat}+E_{cool}+E_{vent}) \times R_{aux}
]

### `R_aux`

| Complexité installation | `R_aux` |
| ----------------------- | ------: |
| Faible                  |    0.05 |
| Standard                |    0.08 |
| Élevée                  |    0.11 |
| Très élevée             |    0.14 |

---

# 4.14 Règles métier spécifiques chambres

Les chambres sont un différenciateur majeur du produit.

## 4.14.1 Fonctions chambres à modéliser

* absence
* fenêtre ouverte
* mode nuit
* présence par badge/carte
* remise en confort avant occupation
* consigne hiver/été spécifique

## 4.14.2 Gains V1 proposés par fonction

| Fonction                     | Chauffage | Refroidissement | Éclairage |
| ---------------------------- | --------: | --------------: | --------: |
| Mode absence                 |       8 % |            10 % |       0 % |
| Fenêtre ouverte              |       6 % |             7 % |       0 % |
| Mode nuit                    |       4 % |             3 % |       0 % |
| Détection présence éclairage |       0 % |             0 % |      18 % |
| Carte chambre / badge        |       3 % |             4 % |      12 % |

## 4.14.3 Conditions d’application

* s’applique aux zones `guest_rooms`
* `fenêtre ouverte` n’agit que si chauffage ou climatisation existe
* `mode nuit` s’applique seulement si système pilotable
* `badge chambre` suppose occupation intermittente

## 4.14.4 Formule

Les gains s’appliquent **séquentiellement** :

[
F_{BACS,room} = \prod_{i=1}^{n}(1-g_i)
]

Exemple chauffage chambre :

* absence = 8 %
* fenêtre ouverte = 6 %
* nuit = 4 %

[
F = 0.92 \times 0.94 \times 0.96 = 0.830
]

Gain total ≈ **17.0 %**

---

# 4.15 Règles métier orientation + chambre

## 4.15.1 Sur-refroidissement chambres sud

Pour les chambres sud et ouest :

* appliquer `F_orientation_cool` majoré,
* et prioriser les solutions :

  * mode absence,
  * mode nuit,
  * limitation solaire,
  * fenêtre ouverte,
  * régulation pièce par pièce.

## 4.15.2 Règle prioritaire rapport

Si une zone `guest_rooms` orientée sud ou ouest représente > 20 % de la surface refroidie, le moteur doit pouvoir générer :

> “Les chambres exposées sud/ouest concentrent une part importante du potentiel d’optimisation du refroidissement.”

---

# 4.16 Calcul BACS détaillé

## 4.16.1 Structure par domaines

Je recommande 8 domaines :

1. chauffage
2. refroidissement
3. ventilation
4. ECS
5. éclairage
6. supervision
7. monitoring énergétique
8. automatisation chambre

## 4.16.2 Score de domaine

Chaque domaine reçoit un score 0–100.

### Exemple de pondération

| Domaine                | Poids |
| ---------------------- | ----: |
| Chauffage              |    18 |
| Refroidissement        |    14 |
| Ventilation            |    12 |
| ECS                    |    10 |
| Éclairage              |    12 |
| Supervision            |    12 |
| Monitoring             |    10 |
| Automatisation chambre |    12 |

## 4.16.3 Score global

[
Score_{BACS} = \sum (Poids_d \times Score_d) / 100
]

## 4.16.4 Conversion en classe

| Score global | Classe |
| ------------ | -----: |
| 85–100       |      A |
| 65–84        |      B |
| 40–64        |      C |
| < 40         |      D |

Cette conversion est une **règle produit V1**, pas une transcription réglementaire officielle.

---

# 4.17 Fonctions BACS standards V1

## 4.17.1 Chauffage

* programmation horaire
* régulation pièce par pièce
* abaissement nocturne
* détection ouverture fenêtre
* optimisation relance
* limitation consigne

## 4.17.2 Refroidissement

* programmation horaire
* régulation terminale
* mode absence
* mode nuit
* verrouillage fenêtre ouverte
* limitation consigne été

## 4.17.3 Ventilation

* horaire
* débit réduit hors occupation
* asservissement présence
* asservissement CO₂
* récupération chaleur optimisée

## 4.17.4 ECS

* programmation ECS
* optimisation température
* réduction pertes bouclage
* supervision ECS
* alarme dérive

## 4.17.5 Éclairage

* LED
* détection présence
* extinction horaire
* gradation
* asservissement lumière du jour

## 4.17.6 Supervision / monitoring

* GTB centralisée
* alarmes
* sous-comptage
* tableaux de bord
* suivi dérives
* reporting énergétique

---

# 4.18 Gains BACS par domaine — valeurs V1 proposées

## 4.18.1 Chauffage

| Fonction                   | Gain proposé |
| -------------------------- | -----------: |
| Programmation horaire      |          5 % |
| Régulation pièce par pièce |          7 % |
| Abaissement nocturne       |          4 % |
| Fenêtre ouverte            |          6 % |
| Optimisation relance       |          3 % |

## 4.18.2 Refroidissement

| Fonction              | Gain proposé |
| --------------------- | -----------: |
| Programmation horaire |          4 % |
| Régulation terminale  |          6 % |
| Mode absence          |          8 % |
| Mode nuit             |          3 % |
| Fenêtre ouverte       |          5 % |

## 4.18.3 Ventilation

| Fonction                  | Gain proposé |
| ------------------------- | -----------: |
| Horaire optimisé          |          8 % |
| Présence                  |         10 % |
| CO₂                       |         12 % |
| Réduction hors occupation |          7 % |

## 4.18.4 ECS

| Fonction                 | Gain proposé |
| ------------------------ | -----------: |
| Programmation ECS        |          3 % |
| Optimisation température |          4 % |
| Réduction bouclage       |          6 % |
| Supervision dérive       |          2 % |

## 4.18.5 Éclairage

| Fonction           | Gain proposé |
| ------------------ | -----------: |
| Détection présence |         15 % |
| Extinction horaire |          8 % |
| Gradation          |         10 % |
| Lumière du jour    |         12 % |

---

# 4.19 Règles de combinaison des gains

## 4.19.1 Règle générale

Application sur résiduel :

[
E_{after} = E_{before} \times \prod_{i}(1-g_i)
]

## 4.19.2 Plafonds de gains par usage

Pour éviter des résultats irréalistes, fixer des plafonds V1 :

| Usage           | Plafond gain cumulé |
| --------------- | ------------------: |
| Chauffage       |                40 % |
| Refroidissement |                40 % |
| Ventilation     |                45 % |
| ECS             |                25 % |
| Éclairage       |                60 % |
| Auxiliaires     |                35 % |

## 4.19.3 Rendement décroissant

Si deux fonctions proches existent, réduire la seconde de 25 %.

Exemple :

* présence
* badge chambre

alors le second gain devient :
[
g_2' = g_2 \times 0.75
]

---

# 4.20 Catalogue de solutions — règles d’impact V1

## 4.20.1 Exemples de solutions

| Solution                     | Usage principal           |       Gain proposé |           CAPEX indicatif |
| ---------------------------- | ------------------------- | -----------------: | ------------------------: |
| GTB/BACS de base             | multi-usage               |             5–12 % |              paramétrable |
| Automatisation chambre       | chauffage/froid/éclairage |            10–25 % |               par chambre |
| Détection présence éclairage | éclairage                 |            10–20 % |                  par zone |
| Relamping LED                | éclairage                 |            20–35 % |                    par m² |
| Régulation terminale         | chauffage/froid           |             5–12 % |          par chambre/zone |
| Horaire ventilation          | ventilation               |             5–10 % |              par CTA/zone |
| CO₂ ventilation              | ventilation               |             8–15 % |                  par zone |
| Optimisation ECS             | ECS                       |             3–10 % | forfait / local technique |
| Calorifuge ECS               | ECS                       |              3–8 % |                   forfait |
| PAC performante              | chauffage/froid           | fort effet système |         projet spécifique |

## 4.20.2 Modèle d’impact JSON type

```json
{
  "applies_to": ["guest_rooms", "lobby"],
  "uses": ["heating", "cooling", "lighting"],
  "gain_model": {
    "type": "percentage",
    "default": {
      "heating": 0.10,
      "cooling": 0.12,
      "lighting": 0.15
    },
    "orientation_bonus": {
      "south": {
        "cooling": 0.03
      },
      "west": {
        "cooling": 0.02
      }
    }
  },
  "constraints": {
    "requires_controlled_terminal": false
  }
}
```

---

# 4.21 Règles économiques par défaut

## 4.21.1 Valeurs V1 proposées

| Paramètre               |    Valeur V1 |
| ----------------------- | -----------: |
| Taux d’actualisation    |          6 % |
| Inflation énergie       |          3 % |
| Période d’analyse       |       15 ans |
| Taux maintenance annuel | 2 % du CAPEX |
| Dégradation performance |     0.5 %/an |

Ces valeurs doivent être surchargeables par pays et par projet.

## 4.21.2 Formules

### Coût énergie

[
Cost_{energy} = \sum(E_s \times P_s)
]

### Payback simple

[
Payback = \frac{CAPEX - Subsidies}{Savings_{energy}+Savings_{maintenance}}
]

### VAN

[
NPV = \sum_{t=0}^{n} \frac{CF_t}{(1+r)^t}
]

### TRI

taux `r` tel que :
[
0 = \sum_{t=0}^{n} \frac{CF_t}{(1+r)^t}
]

---

# 4.22 CO₂ — valeurs de structure

Les facteurs CO₂ doivent venir du `CountryProfile` et non être codés en dur.
Le cadre européen pousse bien à intégrer la trajectoire de réduction d’émissions dans l’analyse bâtiment.

### Structure

```json
{
  "electricity": 0.055,
  "gas": 0.227,
  "district_heating": 0.120
}
```

Les valeurs ci-dessus ne sont qu’un **exemple de structure**, pas des valeurs de référence à figer sans validation pays.

---

# 4.23 Gestion des incertitudes

## 4.23.1 Niveaux de confiance proposés

| Confiance | Critère                                              |
| --------- | ---------------------------------------------------- |
| Haute     | mode avancé, zones bien renseignées, systèmes connus |
| Moyenne   | mode express avec données principales                |
| Faible    | nombreuses hypothèses par défaut                     |

## 4.23.2 Fourchette indicative

Produire :

* résultat bas = central × 0.9
* résultat central
* résultat haut = central × 1.1

En V1, c’est suffisant.

---

# 4.24 Messages automatiques générés par règles

## 4.24.1 Exemples de déclencheurs

### Chauffage dominant

Si chauffage > 35 % de la consommation totale :

> “Le chauffage constitue le premier poste de consommation estimé.”

### ECS dominant

Si ECS > 25 % :

> “L’ECS représente un levier important pour ce bâtiment d’hébergement.”

### Chambres sud prioritaires

Si chambres sud/ouest > 20 % surface refroidie :

> “Les chambres les plus exposées au soleil concentrent un potentiel élevé d’optimisation estivale.”

### Gain BACS significatif

Si passage C→B ou B→A :

> “Le scénario améliore significativement la maturité d’automatisation du bâtiment.”

---

# 4.25 Exemple complet de calcul

## Données

* surface chauffée : 4 000 m²
* 80 chambres
* climat chauffage H3
* climat refroidissement C3
* période 1975–1990
* compacité moyenne
* infiltration moyenne
* chambres sud = 1 000 m²
* taux occupation = 70 %
* chauffage standard
* climatisation standard

## Chauffage chambres sud

[
E = 1000 \times 85 \times 1.00 \times 1.20 \times 1.00 \times 1.00 \times 1.00 \times 0.94 \times 1.00 \times 1.00 \times 1.00
]

[
E = 95,880 \text{ kWh/an}
]

## Avec scénario chambre :

* absence 8 %
* fenêtre ouverte 6 %
* nuit 4 %

[
F = 0.92 \times 0.94 \times 0.96 = 0.830
]

[
E_{after} = 95,880 \times 0.830 = 79,580 \text{ kWh/an}
]

Gain :
[
16,300 \text{ kWh/an}
]

---

# 4.26 Paramètres à exposer dans l’admin

L’administrateur doit pouvoir modifier :

* intensités de référence
* coefficients climat
* coefficients construction
* coefficients orientation
* gains fonctions BACS
* plafonds de gains
* paramètres économiques
* facteurs CO₂
* messages automatiques
* scores BACS
* seuils de classes BACS

---

# 4.27 Ce que je recommande de figer maintenant

Je recommande de figer les choix suivants :

* calcul **annuel**
* base **m² + chambre**
* ECS centrée sur le **nombre de chambres**
* orientation traitée au niveau **zone**
* coefficients simples et explicables
* gains BACS **par fonction**
* gains combinés **sur résiduel**
* plafonds de sécurité par usage
* économie = **payback + VAN + TRI**
* règles/messages automatiques intégrés

---
