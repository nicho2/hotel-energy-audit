"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { env } from "@/lib/config/env";

const navItems = [
  { href: "/projects", label: "Projets" },
  { href: "/templates", label: "Modeles" },
  { href: "/reports", label: "Rapports" },
  { href: "/catalog", label: "Catalogue" },
  { href: "/admin", label: "Administration" },
];

export function DashboardSidebarNav() {
  const pathname = usePathname();

  return (
    <nav style={{ padding: 16, display: "grid", gap: 24 }}>
      <div style={{ display: "grid", gap: 4 }}>
        <div
          style={{
            fontSize: 12,
            fontWeight: 700,
            letterSpacing: "0.08em",
            color: "#627084",
            textTransform: "uppercase",
          }}
        >
          MVP
        </div>
        <div style={{ fontSize: 18, fontWeight: 700, color: "#142033" }}>{env.appName}</div>
      </div>

      <div style={{ display: "grid", gap: 8 }}>
        {navItems.map((item) => {
          const isActive = pathname === item.href || pathname.startsWith(`${item.href}/`);

          return (
            <Link
              key={item.href}
              href={item.href}
              style={{
                display: "block",
                padding: "10px 12px",
                borderRadius: 10,
                background: isActive ? "#14365d" : "transparent",
                color: isActive ? "#ffffff" : "#142033",
                fontWeight: isActive ? 600 : 500,
              }}
            >
              {item.label}
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
