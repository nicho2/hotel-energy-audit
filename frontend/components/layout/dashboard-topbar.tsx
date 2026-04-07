"use client";

import { env } from "@/lib/config/env";
import { useAuthContext } from "@/providers/auth-provider";

export function DashboardTopbar() {
  const { user } = useAuthContext();

  return (
    <div
      style={{
        height: 64,
        borderBottom: "1px solid #e5e7eb",
        background: "#fff",
        padding: "0 24px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
      }}
    >
      <div style={{ display: "grid", gap: 2 }}>
        <div style={{ fontWeight: 600 }}>{env.appName}</div>
        <div style={{ fontSize: 13, color: "#627084" }}>Espace de travail MVP</div>
      </div>
      <div style={{ fontSize: 14, color: "#627084" }}>
        {user ? user.email : "Utilisateur non connecte"}
      </div>
    </div>
  );
}
