# Codex Task Template

## Metadata
- Task ID: LOT-D-T12
- Epic: Recalage MVP initial vs implémentation actuelle
- Feature: Contenu rapports executive/detailed
- Priority: P1
- Owner: Backend Reporting (+ Frontend preview si nécessaire)
- Status: todo
- Related files:
  - `backend/app/reporting/templates/executive/**`
  - `backend/app/reporting/templates/detailed/**`
  - `backend/app/reporting/builders/executive_report_builder.py`
  - `backend/app/reporting/builders/detailed_report_builder.py`
  - `backend/tests/test_reports_api.py`
- Dependencies:
  - LOT-D-T11

## Context
Les templates existent mais certaines sections/KPI/messages restent génériques et partiellement alignés avec la spec rapport (doc 6).
Le rapport est un différenciateur commercial clé du MVP.
Cette tâche finalise le contenu métier et la structure de restitution.

## Objective
Aligner les rapports `executive` et `detailed` avec la structure, KPI et messages attendus par les specs initiales.

## In scope
- Compléter sections (contexte, bâtiment, état initial, BACS, scénarios, comparaison, économie, reco, hypothèses, limites, annexes).
- Ajouter KPI prioritaires (énergie, CO2, BACS actuelle/cible, CAPEX, payback, VAN).
- Normaliser messages automatiques et disclaimers “estimation simplifiée”.
- Vérifier cohérence FR/EN et branding.

## Out of scope
- Réécriture complète design graphique corporate.
- Génération de graphiques avancés non indispensables MVP.

## Inputs / references
- `AGENTS.md`
- `docs/6-Specification-du-rapport-PDF.md`
- `docs/0-cahier-des-charges-initial.md`
- `docs/3-Moteur-de-calcul-simplifie.md`
- Additional docs:
  - `docs/backend-reporting.md`

## Implementation notes
- Prioriser lisibilité direction/commercial pour rapport exécutif.
- Garder traçabilité hypothèses pour rapport détaillé.
- Rebouclage:
  1. Checklist section par section vs doc 6.
  2. Vérifier disponibilité réelle des données sources (pas de faux KPI).
  3. Ajuster builders si données manquantes nécessaires.

## Acceptance criteria
- [ ] Les deux formats couvrent la structure cible définie dans doc 6.
- [ ] Les KPI majeurs sont correctement calculés et affichés.
- [ ] Les disclaimers méthodologiques sont explicites et cohérents.

## Tests to add or update
- [ ] Tests de rendu HTML (présence sections clés).
- [ ] Tests API rapport validant options d’inclusion et contenu.

## Deliverables
- [ ] Templates executive/detailed alignés.
- [ ] Builders reporting enrichis.
- [ ] Tests de validation de contenu.

## Definition of done
- [ ] Code implemented
- [ ] Tests pass
- [ ] Docs updated if needed
- [ ] No architecture drift introduced
