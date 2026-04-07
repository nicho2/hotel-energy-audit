"use client";

import Link from "next/link";
import { useProjects } from "../hooks/use-projects";
import type { ProjectListItem } from "@/types/project";

function formatUpdatedAt(value: string) {
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "-";
  }

  return new Intl.DateTimeFormat("fr-FR", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(date);
}

export function ProjectListTable() {
  const { data, isLoading, error } = useProjects();

  if (isLoading) {
    return (
      <div style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", padding: 24 }}>
        Chargement des projets...
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ border: "1px solid #fecaca", borderRadius: 16, background: "#fff", padding: 24, color: "#b91c1c" }}>
        Erreur de chargement des projets.
      </div>
    );
  }

  const projects = data?.data ?? [];

  if (projects.length === 0) {
    return (
      <div style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", padding: 24 }}>
        Aucun projet disponible pour le moment.
      </div>
    );
  }

  return (
    <div style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", overflow: "hidden" }}>
      <table style={{ width: "100%", fontSize: 14, borderCollapse: "collapse" }}>
        <thead style={{ background: "#f9fafb", textAlign: "left" }}>
          <tr>
            <th style={{ padding: 12 }}>Projet</th>
            <th style={{ padding: 12 }}>Client</th>
            <th style={{ padding: 12 }}>Statut</th>
            <th style={{ padding: 12 }}>Etape wizard</th>
            <th style={{ padding: 12 }}>Mise a jour</th>
          </tr>
        </thead>
        <tbody>
          {projects.map((project: ProjectListItem) => (
            <tr key={project.id} style={{ borderTop: "1px solid #e5e7eb" }}>
              <td style={{ padding: 12 }}>
                <Link href={`/projects/${project.id}`}>{project.name}</Link>
              </td>
              <td style={{ padding: 12 }}>{project.client_name ?? "-"}</td>
              <td style={{ padding: 12 }}>{project.status}</td>
              <td style={{ padding: 12 }}>{project.wizard_step}</td>
              <td style={{ padding: 12 }}>{formatUpdatedAt(project.updated_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
