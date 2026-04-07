import { env } from "@/lib/config/env";

export function Topbar() {
  return (
    <div style={{ height: "64px", borderBottom: "1px solid #e5e7eb", background: "#fff", padding: "0 24px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
      <div style={{ fontWeight: 600 }}>{env.appName}</div>
      <div style={{ fontSize: "14px", color: "#6b7280" }}>Utilisateur connecté</div>
    </div>
  );
}
