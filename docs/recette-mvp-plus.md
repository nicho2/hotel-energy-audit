# Recette MVP+

Ce document sert de guide de recette technique et fonctionnelle pour une demonstration MVP+ du backend Hotel Energy Audit.

## Objectif De La Recette

Verifier qu'une personne externe au developpement peut :

- demarrer le backend;
- charger un jeu de donnees coherent;
- se connecter;
- consulter les cas de demonstration;
- comparer deux scenarios;
- generer un rapport executif;
- generer un rapport detaille;
- controler les protections d'acces principales.

## Prerequis

- Python 3.12
- PostgreSQL accessible
- Un environnement virtuel Python
- Les dependances backend installees
- Une variable `DATABASE_URL` pointee vers la base de recette si la valeur par defaut ne convient pas
- Une variable `SECRET_KEY` stable pour la session de recette

Le frontend peut etre demarre pour une demonstration produit, mais cette recette reste executable via API backend uniquement.

## Preparation Backend

Depuis la racine du depot :

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
alembic upgrade head
python scripts/seed_all.py
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Sous Windows avec le launcher Python :

```powershell
cd backend
py -3.12 -m pip install -e ".[dev]"
py -3.12 -m alembic upgrade head
py -3.12 scripts/seed_all.py
py -3.12 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

## Comptes De Demonstration

Le script `scripts/seed_all.py` cree :

- admin : `demo@hotel-energy-audit.example.com` / `admin1234`
- utilisateur commercial : `sales@hotel-energy-audit.example.com` / `sales1234`
- admin organisation partenaire : `partner@hotel-energy-audit.example.com` / `partner1234`

## Cas De Demonstration

Les projets de demo attendus sont :

- `DEMO-HOTEL-001` : hotel urbain standard, restaurant et salles de reunion.
- `DEMO-HOTEL-SW-001` : hotel expose sud/ouest, utile pour parler refroidissement, confort chambres et orientation.
- `DEMO-RESIDENCE-001` : residence d'hebergement avec spa/piscine et logique de plan d'investissement.

Chaque projet est charge en statut `ready`, avec :

- un batiment;
- au moins trois zones;
- au moins trois systemes;
- une evaluation BACS;
- deux scenarios;
- deux calculs persistants.

## Etapes De Validation Fonctionnelle

1. Ouvrir `GET /health`

Resultat attendu : reponse `status=ok`.

2. Se connecter via `POST /api/v1/auth/login`

Payload :

```json
{
  "email": "demo@hotel-energy-audit.example.com",
  "password": "admin1234"
}
```

Resultat attendu : un token bearer et un utilisateur `org_admin`.

3. Lister les projets via `GET /api/v1/projects`

Resultat attendu : les trois references `DEMO-HOTEL-001`, `DEMO-HOTEL-SW-001`, `DEMO-RESIDENCE-001`.

4. Ouvrir un projet demo via `GET /api/v1/projects/{project_id}`

Resultat attendu : projet lisible, statut `ready`, type batiment coherent avec la reference.

5. Consulter batiment, zones, systemes et BACS

Endpoints :

- `GET /api/v1/projects/{project_id}/building`
- `GET /api/v1/projects/{project_id}/zones`
- `GET /api/v1/projects/{project_id}/systems`
- `GET /api/v1/projects/{project_id}/bacs/current/summary`

Resultat attendu : donnees non vides, BACS avec classe estimee.

6. Lister les scenarios via `GET /api/v1/projects/{project_id}/scenarios`

Resultat attendu : deux scenarios, dont un scenario de reference.

7. Comparer les scenarios via `POST /api/v1/projects/{project_id}/scenarios/compare`

Payload :

```json
{
  "scenario_ids": ["<scenario_id_1>", "<scenario_id_2>"]
}
```

Resultat attendu : deux lignes comparees et un scenario recommande.

8. Consulter le dernier resultat d'un scenario via `GET /api/v1/projects/{project_id}/scenarios/{scenario_id}/results/latest`

Resultat attendu : consommation, economie, CAPEX et messages disponibles.

9. Generer un rapport executif

Endpoint :

`POST /api/v1/reports/executive/{calculation_run_id}/generate`

Resultat attendu : rapport `executive`, statut `generated`, fichier PDF telechargeable.

10. Generer un rapport detaille

Endpoint :

`POST /api/v1/reports/detailed/{calculation_run_id}/generate?language=fr`

Resultat attendu : rapport `detailed`, statut `generated`, fichier PDF distinct.

11. Telecharger un rapport

Endpoint :

`GET /api/v1/reports/{report_id}/download`

Resultat attendu : reponse `application/pdf`.

## Validation Technique Rapide

Depuis `backend/` :

```bash
python -m ruff check app tests scripts
python -m pytest tests/test_recette_smoke_api.py tests/test_seed_all.py
python -m pytest
```

Sous Windows :

```powershell
py -3.12 -m ruff check app tests scripts
py -3.12 -m pytest tests/test_recette_smoke_api.py tests/test_seed_all.py
py -3.12 -m pytest
```

Resultat attendu :

- lint sans erreur;
- smoke test recette vert;
- suite backend complete verte.

## Points De Vigilance

- Le PDF est encore genere par le pipeline placeholder HTML -> artefact PDF simple; ne pas presenter cela comme un moteur de composition PDF final.
- Les calculs de demo sont des resultats persistants de seed pour securiser la demonstration, pas une simulation reglementaire.
- Le moteur reste une estimation annuelle simplifiee.
- Les controles d'acces sont organisationnels; les comptes demo et partenaire permettent de valider le cloisonnement.
