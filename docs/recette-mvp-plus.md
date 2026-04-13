# Recette MVP+

Ce document sert de guide de recette technique et fonctionnelle pour une demonstration MVP+ de Hotel Energy Audit. Il est aligne sur l'etat reel implemente dans le depot au 2026-04-13.

Le backend est le chemin de recette principal. Le frontend fournit aussi des pages dashboard fonctionnelles pour les parcours projet, catalogue et templates, mais la recette ci-dessous reste executable de bout en bout via API.

## Etat Reel Implemente

| Domaine | Etat | Preuve de recette |
| --- | --- | --- |
| Authentification et cloisonnement organisation | Implemente | `test_auth_api.py`, `test_security_api.py` |
| Projets, batiments, zones, systemes | Implemente | `test_projects_api.py`, `test_buildings_api.py`, `test_zones_api.py`, `test_systems_api.py` |
| Wizard express et readiness | Implemente | `test_wizard_api.py`, `test_calculation_readiness_api.py`, `test_readiness_service.py` |
| BACS | Implemente | `test_bacs_api.py` |
| Catalogue de solutions | Implemente | `test_solution_catalog_api.py` |
| Templates projet | Implemente | `test_project_templates_api.py` |
| Scenarios et assignments de solutions | Implemente | `test_scenarios_management_api.py`, `test_calculations_api.py` |
| Moteur energetique V1 simplifie | Implemente | `test_calculation_engine.py`, `test_calculations_api.py` |
| Impacts scenarios et BACS | Implemente | `test_calculations_api.py`, `test_scenarios_management_api.py` |
| Economie ROI, payback, VAN, TRI, cash-flow | Implemente | `test_results_api.py`, `test_calculation_engine.py` |
| Comparateur et scoring explicable | Implemente | `test_scenarios_compare_api.py`, `test_scenario_scoring.py` |
| Reporting executive et detailed | Implemente | `test_reports_api.py` |
| PDF reel stocke et telechargeable | Implemente | `test_reports_api.py` |
| Branding rapport | Implemente | `test_branding_api.py`, `test_reports_api.py` |
| Audit minimal | Implemente | `test_audit_api.py` |
| Donnees de demo | Implemente | `test_seed_all.py`, `test_recette_smoke_api.py` |

Derniere verification locale effectuee dans cette passe:

```powershell
cd backend
py -3.12 -m pytest
```

Resultat observe: `123 passed`.

## Objectif De La Recette

Verifier qu'une personne externe au developpement peut:

- demarrer le backend;
- appliquer les migrations;
- charger un jeu de donnees coherent;
- se connecter;
- consulter les cas de demonstration;
- consulter le catalogue de solutions et les templates;
- verifier la readiness d'un projet;
- calculer un scenario;
- comparer deux scenarios avec un scoring explicable;
- consulter les resultats energetiques, BACS et economiques;
- generer un rapport executif;
- generer un rapport detaille;
- telecharger un PDF stocke;
- controler les protections d'acces principales.

## Prerequis

- Python 3.12
- PostgreSQL accessible
- Un environnement virtuel Python recommande
- Les dependances backend installees
- Une variable `DATABASE_URL` pointee vers la base de recette si la valeur par defaut ne convient pas
- Une variable `SECRET_KEY` stable pour la session de recette
- Optionnel frontend: Node.js compatible avec Next.js 15 et dependances `frontend/` installees

## Preparation Backend

Depuis la racine du depot:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
alembic upgrade head
python scripts/seed_all.py
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Sous Windows avec le launcher Python:

```powershell
cd backend
py -3.12 -m pip install -e ".[dev]"
py -3.12 -m alembic upgrade head
py -3.12 scripts/seed_all.py
py -3.12 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

## Preparation Frontend Optionnelle

Le frontend peut etre utilise pour une demonstration produit des pages dashboard.

```powershell
cd frontend
npm install
npm run dev
```

Pages utiles pour la recette:

- `/catalog`: catalogue de solutions avec recherche, filtres, familles et impacts.
- `/templates`: templates projet avec creation basique.
- `/projects`: liste et creation de projets, dont creation depuis template.
- `/reports`: acces aux rapports generes selon les parcours disponibles dans l'interface.

## Comptes De Demonstration

Le script `scripts/seed_all.py` cree:

- admin: `demo@hotel-energy-audit.example.com` / `admin1234`
- utilisateur commercial: `sales@hotel-energy-audit.example.com` / `sales1234`
- admin organisation partenaire: `partner@hotel-energy-audit.example.com` / `partner1234`

## Cas De Demonstration

Les projets de demo attendus sont:

- `DEMO-HOTEL-001`: hotel urbain standard, restaurant et salles de reunion.
- `DEMO-HOTEL-SW-001`: hotel expose sud/ouest, utile pour parler refroidissement, confort chambres et orientation.
- `DEMO-RESIDENCE-001`: residence d'hebergement avec spa/piscine et logique de plan d'investissement.

Chaque projet est charge en statut `ready`, avec:

- un batiment;
- plusieurs zones;
- plusieurs systemes techniques;
- une evaluation BACS;
- deux scenarios;
- des assignments de solutions sur les scenarios cibles;
- des calculs persistants exploitables pour comparaison et reporting.

## Etapes De Validation Fonctionnelle API

### 1. Sante API

Ouvrir:

`GET /health`

Resultat attendu:

- reponse `status=ok`.

### 2. Connexion

Endpoint:

`POST /api/v1/auth/login`

Payload:

```json
{
  "email": "demo@hotel-energy-audit.example.com",
  "password": "admin1234"
}
```

Resultat attendu:

- reponse standardisee `data / meta / errors`;
- token bearer present;
- utilisateur `org_admin`.

### 3. Projets Demo

Endpoint:

`GET /api/v1/projects`

Resultat attendu:

- les trois references `DEMO-HOTEL-001`, `DEMO-HOTEL-SW-001`, `DEMO-RESIDENCE-001`;
- projets rattaches a l'organisation du compte connecte.

### 4. Detail Projet

Endpoint:

`GET /api/v1/projects/{project_id}`

Resultat attendu:

- projet lisible;
- statut `ready`;
- type batiment coherent avec la reference;
- champs pays/climat/template coherents quand renseignes.

### 5. Batiment, Zones, Systemes Et BACS

Endpoints:

- `GET /api/v1/projects/{project_id}/building`
- `GET /api/v1/projects/{project_id}/zones`
- `GET /api/v1/projects/{project_id}/systems`
- `GET /api/v1/projects/{project_id}/bacs/current/summary`

Resultat attendu:

- donnees non vides;
- zones avec surfaces, usages et orientations;
- systemes avec type, energie et niveau d'efficacite;
- BACS avec classe estimee et fonctions selectionnees.

### 6. Readiness Calcul

Endpoint:

`GET /api/v1/projects/{project_id}/calculation-readiness`

Resultat attendu:

- projet demo calculable;
- blocages absents ou explicitement listes;
- warnings et niveau de confiance disponibles.

### 7. Catalogue De Solutions

Endpoint:

`GET /api/v1/projects/solutions/catalog?country=FR&family=bacs&building_type=hotel`

Resultat attendu:

- catalogue non vide;
- familles et impacts exposes;
- solutions actives seulement par defaut;
- filtres pays, famille et type de batiment appliques.

### 8. Templates Projet

Endpoints:

- `GET /api/v1/project-templates`
- `POST /api/v1/project-templates`
- `POST /api/v1/projects` avec `template_id`

Resultat attendu:

- templates listables;
- creation et modification possibles pour l'organisation;
- creation projet depuis template conserve `template_id` et initialise le parcours express.

### 9. Scenarios Et Solutions

Endpoints:

- `GET /api/v1/projects/{project_id}/scenarios`
- `GET /api/v1/projects/{project_id}/scenarios/{scenario_id}/solutions`
- `POST /api/v1/projects/{project_id}/scenarios/{scenario_id}/solutions`

Resultat attendu:

- deux scenarios sur les projets demo;
- un scenario de reference;
- un scenario cible avec solutions selectionnees;
- les assignments restent lisibles meme si une solution catalogue devient inactive.

### 10. Calculer Un Scenario

Endpoint:

`POST /api/v1/projects/{project_id}/scenarios/{scenario_id}/calculate`

Resultat attendu:

- `calculation_run_id` cree;
- `engine_version` renseigne;
- `input_snapshot` present;
- resultats par usage et par zone persistants;
- messages et warnings explicites;
- variation des sorties selon projet, zones, systemes, BACS et solutions selectionnees.

### 11. Comparer Les Scenarios

Endpoint:

`POST /api/v1/projects/{project_id}/scenarios/compare`

Payload:

```json
{
  "scenario_ids": ["<scenario_id_1>", "<scenario_id_2>"]
}
```

Resultat attendu:

- deux lignes comparees;
- un scenario recommande;
- score conserve pour retrocompatibilite;
- breakdown explicable du score avec contributions energie, BACS, ROI et CAPEX;
- message de recommandation coherent avec les contributions dominantes.

### 12. Consulter Le Dernier Resultat

Endpoint:

`GET /api/v1/projects/{project_id}/scenarios/{scenario_id}/results/latest`

Resultat attendu:

- consommation baseline et scenario;
- resultats par usage et zone;
- classe BACS baseline et scenario;
- CAPEX, OPEX, economies, payback, VAN, TRI et cash-flow simplifie;
- hypotheses economiques tracees;
- cas non calculables representes explicitement.

### 13. Generer Un Rapport Executif

Endpoint:

`POST /api/v1/reports/executive/{calculation_run_id}/generate`

Resultat attendu:

- rapport `executive`;
- statut `generated`;
- `mime_type=application/pdf`;
- fichier stocke et telechargeable;
- contenu incluant contexte, resume KPI, batiment, BACS, resultats, recommandations, methodologie et limites.

### 14. Generer Un Rapport Detaille

Endpoint:

`POST /api/v1/reports/detailed/{calculation_run_id}/generate?language=fr&include_assumptions=true&include_regulatory_section=true&include_annexes=true`

Resultat attendu:

- rapport `detailed`;
- statut `generated`;
- PDF distinct;
- sections contexte, batiment, etat initial, zones, systemes, BACS, comparaison, economie, recommandations, hypotheses, limites, reglementaire et annexes selon options.

### 15. Generation Generique De Rapport

Endpoint:

`POST /api/v1/projects/{project_id}/reports`

Payload exemple:

```json
{
  "scenario_id": "<scenario_id>",
  "calculation_run_id": "<calculation_run_id>",
  "report_type": "detailed",
  "language": "fr",
  "include_assumptions": true,
  "include_regulatory_section": true,
  "include_annexes": true
}
```

Resultat attendu:

- reponse `201`;
- metadonnees `GeneratedReport` persistantes;
- options de sections respectees.

### 16. Telecharger Un Rapport

Endpoint:

`GET /api/v1/reports/{report_id}/download`

Resultat attendu:

- reponse `application/pdf`;
- contenu commence par `%PDF-1.4`;
- `Content-Disposition` contient le nom de fichier.

### 17. Cloisonnement Organisationnel

Avec le compte partenaire:

1. se connecter via `partner@hotel-energy-audit.example.com`;
2. tenter d'ouvrir un projet de l'organisation demo;
3. lister projets, rapports et ressources admin.

Resultat attendu:

- les projets d'une autre organisation ne sont pas lisibles;
- les ressources propres a l'organisation partenaire restent accessibles;
- les operations admin sont limitees par role.

## Validation Produit Frontend Optionnelle

Demarrer le backend puis le frontend. Depuis le navigateur:

1. se connecter avec le compte demo;
2. ouvrir `/catalog`;
3. chercher une solution BACS ou HVAC;
4. filtrer par famille et verifier les impacts affiches;
5. ouvrir `/templates`;
6. creer un template simple;
7. creer un projet depuis ce template;
8. ouvrir le dashboard projets et verifier que le projet est present.

Resultat attendu:

- les pages `/catalog` et `/templates` ne sont pas des placeholders;
- les donnees sont chargees via les endpoints backend;
- les etats loading, empty et error sont geres;
- le parcours reste compatible avec le mode express.

## Validation Technique Rapide

Depuis `backend/`:

```bash
python -m ruff check app tests scripts
python -m pytest tests/test_recette_smoke_api.py tests/test_seed_all.py
python -m pytest
```

Sous Windows:

```powershell
py -3.12 -m ruff check app tests scripts
py -3.12 -m pytest tests/test_recette_smoke_api.py tests/test_seed_all.py
py -3.12 -m pytest
```

Resultat attendu:

- lint sans erreur;
- smoke test recette vert;
- suite backend complete verte.

Validation frontend optionnelle:

```powershell
cd frontend
npm run build
```

Resultat attendu:

- build Next.js sans erreur.

## Points De Vigilance

- Le moteur reste une estimation annuelle simplifiee: ce n'est pas une simulation thermique dynamique.
- Les rapports et calculs ne constituent pas une attestation reglementaire.
- Le PDF est maintenant un vrai artefact PDF genere depuis les templates HTML, mais le renderer interne reste volontairement simple et oriente MVP.
- Les resultats de demo sont persistants pour securiser la demonstration; il faut recalculer un scenario pour verifier la chaine de calcul de bout en bout.
- Le scoring comparateur est explicable et versionne via assumptions, mais il reste un outil d'aide a la decision, pas une optimisation automatique avancee.
- Les hypotheses, snapshots et versions doivent rester visibles pour toute comparaison commerciale.
