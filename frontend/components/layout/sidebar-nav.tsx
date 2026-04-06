import Link from "next/link";

export function SidebarNav() {
  return (
    <nav style={{ padding: "16px", display: "grid", gap: "8px" }}>
      <Link href="/projects">Projets</Link>
      <Link href="/templates">Modèles</Link>
      <Link href="/reports">Rapports</Link>
      <Link href="/catalog">Catalogue</Link>
      <Link href="/admin">Administration</Link>
    </nav>
  );
}
