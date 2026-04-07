import { CreateProjectForm } from "@/features/projects/components/create-project-form";

export default function NewProjectPage() {
  return (
    <div style={{ display: "grid", gap: 24 }}>
      <div style={{ display: "grid", gap: 8 }}>
        <h1 style={{ fontSize: 32, fontWeight: 600, margin: 0 }}>Nouveau projet</h1>
        <p style={{ margin: 0, color: "#627084", maxWidth: 720 }}>
          Renseigner le minimum necessaire pour initialiser un projet MVP puis poursuivre sur le detail projet et le wizard.
        </p>
      </div>
      <CreateProjectForm />
    </div>
  );
}
