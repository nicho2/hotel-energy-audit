import Link from "next/link";
import { ProjectListTable } from "@/features/projects/components/project-list-table";
import { Button } from "@/components/ui/button";

export default function ProjectsPage() {
  return (
    <div style={{ display: "grid", gap: 24 }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <h1 style={{ fontSize: 32, fontWeight: 600 }}>Projets</h1>
        <Link href="/projects/new">
          <Button>Nouveau projet</Button>
        </Link>
      </div>
      <ProjectListTable />
    </div>
  );
}
