import type { ReactNode } from "react";
import { DashboardSidebarNav } from "./dashboard-sidebar-nav";
import { DashboardTopbar } from "./dashboard-topbar";

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div
      style={{
        minHeight: "100vh",
        display: "grid",
        gridTemplateColumns: "260px minmax(0, 1fr)",
        background: "#f4f6f8",
      }}
    >
      <aside style={{ borderRight: "1px solid #e5e7eb", background: "#fff", minHeight: "100vh" }}>
        <DashboardSidebarNav />
      </aside>
      <main style={{ minHeight: "100vh", background: "#f4f6f8" }}>
        <DashboardTopbar />
        <div style={{ padding: 24 }}>{children}</div>
      </main>
    </div>
  );
}
