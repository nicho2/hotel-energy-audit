"use client";

import Link from "next/link";
import { useProjects } from "../hooks/use-projects";

export function ProjectTable() {
  const { data, isLoading, error } = useProjects();

  if (isLoading) return <div>Chargement...</div>;
  if (error) return <div>Erreur de chargement.</div>;

  const projects = (data as any)?.data ?? [];

  return (
    <div style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", overflow: "hidden" }}>
      <table style={{ width: "100%", fontSize: 14, borderCollapse: "collapse" }}>
        <thead style={{ background: "#f9fafb", textAlign: "left" }}>
          <tr>
            <th style={{ padding: 12 }}>Projet</th>
            <th style={{ padding: 12 }}>Client</th>
            <th style={{ padding: 12 }}>Statut</th>
            <th style={{ padding: 12 }}>Étape</th>
          </tr>
        </thead>
        <tbody>
          {projects.map((project: any) => (
            <tr key={project.id} style={{ borderTop: "1px solid #e5e7eb" }}>
              <td style={{ padding: 12 }}>
                <Link href={`/projects/${project.id}`}>{project.name}</Link>
              </td>
              <td style={{ padding: 12 }}>{project.client_name ?? "-"}</td>
              <td style={{ padding: 12 }}>{project.status}</td>
              <td style={{ padding: 12 }}>{project.wizard_step}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
