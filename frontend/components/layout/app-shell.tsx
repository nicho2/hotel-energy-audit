import { SidebarNav } from "./sidebar-nav";
import { Topbar } from "./topbar";

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div style={{ minHeight: "100vh", display: "grid", gridTemplateColumns: "260px 1fr" }}>
      <aside style={{ borderRight: "1px solid #e5e7eb", background: "#fff" }}>
        <SidebarNav />
      </aside>
      <main style={{ minHeight: "100vh", background: "#f9fafb" }}>
        <Topbar />
        <div style={{ padding: "24px" }}>{children}</div>
      </main>
    </div>
  );
}
