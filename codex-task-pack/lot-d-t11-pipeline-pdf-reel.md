# Codex Task Template

## Metadata
- Task ID: LOT-D-T11
- Epic: Recalage MVP initial vs implémentation actuelle
- Feature: Génération PDF réelle
- Priority: P0
- Owner: Backend Reporting
- Status: todo
- Related files:
  - `backend/app/services/report_service.py`
  - `backend/app/reporting/builders/*`
  - `backend/app/reporting/templates/*`
  - `backend/tests/test_reports_api.py`
- Dependencies:
  - LOT-C-T07
  - LOT-C-T09

## Context
Le service de rapport écrit aujourd’hui un PDF placeholder textuel.
Les specs 0/6 demandent un rapport professionnel (executive + detailed) exploitable commercialement.
Cette tâche remplace le placeholder par un vrai pipeline HTML->PDF, sans casser les contrats API.

## Objective
Produire de vrais PDF à partir des templates HTML existants, stockés et téléchargeables via les endpoints en place.

## In scope
- Remplacer `_render_placeholder_pdf` par un renderer HTML->PDF.
- Conserver séparation builders de contexte / rendu.
- Gérer branding, langue, options d’inclusion (hypothèses, annexes, réglementaire).
- Garantir intégrité stockage, métadonnées et téléchargement.

## Out of scope
- Mise en page ultra premium multi-templates.
- Génération asynchrone distribuée.

## Inputs / references
- `AGENTS.md`
- `docs/6-Specification-du-rapport-PDF.md`
- `docs/1-Architecture-technique-detaille.md`
- `docs/7-Architecture-fonctionnelle-detaillee-des-API-backend.md`
- Additional docs:
  - `docs/backend-reporting.md`

## Implementation notes
- Choisir une librairie stable et documentée pour HTML->PDF.
- Prévoir fallback contrôlé en cas d’échec rendu.
- Rebouclage:
  1. Vérifier sections attendues du rapport (exec/détaillé).
  2. Vérifier conformité API (`GeneratedReportResponse` inchangé sauf enrichissements compatibles).
  3. Vérifier qualité minimale des PDF en lecture client.

## Acceptance criteria
- [ ] Un PDF réel est généré depuis le HTML de rapport.
- [ ] Les endpoints existants (generate/list/download) restent opérationnels.
- [ ] Le PDF inclut branding + sections choisies selon paramètres.

## Tests to add or update
- [ ] Tests intégration report generation + download.
- [ ] Tests vérifiant métadonnées et type MIME du fichier généré.

## Deliverables
- [ ] Pipeline HTML->PDF opérationnel.
- [ ] Service report mis à jour.
- [ ] Tests de non-régression reporting.

## Definition of done
- [ ] Code implemented
- [ ] Tests pass
- [ ] Docs updated if needed
- [ ] No architecture drift introduced
