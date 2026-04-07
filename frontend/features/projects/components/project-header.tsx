import Link from "next/link";
import type { ProjectResponse } from "@/types/project";

const quickLinks = [
  { segment: "wizard", label: "Ouvrir le wizard" },
  { segment: "scenarios", label: "Voir les scenarios" },
  { segment: "compare", label: "Ouvrir le comparateur" },
  { segment: "reports", label: "Voir les rapports" },
];

type ProjectHeaderProps = {
  project: ProjectResponse;
};

export function ProjectHeader({ project }: ProjectHeaderProps) {
  return (
    <div
      style={{
        border: "1px solid #e5e7eb",
        borderRadius: 20,
        background: "#fff",
        padding: 24,
        display: "grid",
        gap: 20,
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", gap: 24, alignItems: "flex-start" }}>
        <div style={{ display: "grid", gap: 8 }}>
          <div style={{ fontSize: 13, color: "#627084" }}>Projet</div>
          <h1 style={{ margin: 0, fontSize: 32, fontWeight: 700 }}>{project.name}</h1>
          <div style={{ display: "flex", gap: 12, flexWrap: "wrap", color: "#627084", fontSize: 14 }}>
            <span>Client: {project.client_name ?? "-"}</span>
            <span>Statut: {project.status}</span>
            <span>Etape wizard: {project.wizard_step}</span>
          </div>
        </div>

        <div
          style={{
            padding: "8px 12px",
            borderRadius: 999,
            background: "#f8fafc",
            border: "1px solid #d7dee7",
            color: "#14365d",
            fontSize: 13,
            fontWeight: 600,
          }}
        >
          {project.building_type}
        </div>
      </div>

      <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
        {quickLinks.map((link) => (
          <Link
            key={link.segment}
            href={`/projects/${project.id}/${link.segment}`}
            style={{
              display: "inline-flex",
              alignItems: "center",
              justifyContent: "center",
              padding: "10px 14px",
              borderRadius: 10,
              background: "#14365d",
              color: "#fff",
              fontWeight: 600,
            }}
          >
            {link.label}
          </Link>
        ))}
      </div>
    </div>
  );
}
