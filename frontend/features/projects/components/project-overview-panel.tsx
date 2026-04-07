"use client";

import { ProjectHeader } from "./project-header";
import { ProjectOverviewCards } from "./project-overview-cards";
import { useProject } from "../hooks/use-project";
import type { ProjectOverviewCard } from "@/types/project";

function buildOverviewCards(wizardStep: number): ProjectOverviewCard[] {
  return [
    {
      key: "energy",
      label: "Energie",
      value: "--",
      helper: "KPI placeholder en attente du moteur de calcul.",
    },
    {
      key: "co2",
      label: "CO2",
      value: "--",
      helper: "Sera remplace par le resultat du scenario de reference.",
    },
    {
      key: "bacs",
      label: "BACS",
      value: `Etape ${wizardStep}`,
      helper: "Indicateur temporaire avant le vrai scoring BACS.",
    },
    {
      key: "roi",
      label: "ROI",
      value: "--",
      helper: "Placeholder pret pour les gains et temps de retour.",
    },
  ];
}

type ProjectOverviewPanelProps = {
  projectId: string;
};

export function ProjectOverviewPanel({ projectId }: ProjectOverviewPanelProps) {
  const { data, error, isLoading } = useProject(projectId);

  if (isLoading) {
    return (
      <div style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", padding: 24 }}>
        Chargement du projet...
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ border: "1px solid #fecaca", borderRadius: 16, background: "#fff", padding: 24, color: "#b91c1c" }}>
        Erreur de chargement du projet.
      </div>
    );
  }

  const project = data?.data;

  if (!project) {
    return (
      <div style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", padding: 24 }}>
        Projet introuvable.
      </div>
    );
  }

  return (
    <div style={{ display: "grid", gap: 24 }}>
      <ProjectHeader project={project} />
      <ProjectOverviewCards cards={buildOverviewCards(project.wizard_step)} />
    </div>
  );
}
