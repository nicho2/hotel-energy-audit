import Link from "next/link";

export default function HomePage() {
  return (
    <main
      style={{
        minHeight: "100vh",
        display: "grid",
        placeItems: "center",
        padding: 24,
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: 720,
          border: "1px solid #d7dee7",
          borderRadius: 24,
          background: "#ffffff",
          boxShadow: "0 10px 30px rgba(20, 32, 51, 0.08)",
          padding: 32,
          display: "grid",
          gap: 16,
        }}
      >
        <div style={{ display: "grid", gap: 8 }}>
          <span style={{ color: "#627084", fontSize: 14 }}>Frontend MVP</span>
          <h1 style={{ margin: 0, fontSize: 36, lineHeight: 1.1 }}>Hotel Energy Audit</h1>
          <p style={{ margin: 0, color: "#627084", fontSize: 16 }}>
            Base Next.js du parcours MVP avec providers globaux, App Router et placeholders propres pour les modules backend encore en cours.
          </p>
        </div>
        <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
          <Link
            href="/login"
            style={{
              display: "inline-flex",
              alignItems: "center",
              justifyContent: "center",
              borderRadius: 12,
              padding: "12px 18px",
              background: "#14365d",
              color: "#ffffff",
              fontWeight: 600,
            }}
          >
            Aller a la connexion
          </Link>
          <Link
            href="/projects"
            style={{
              display: "inline-flex",
              alignItems: "center",
              justifyContent: "center",
              borderRadius: 12,
              padding: "12px 18px",
              border: "1px solid #d7dee7",
              background: "#f8fafc",
              color: "#142033",
              fontWeight: 600,
            }}
          >
            Ouvrir les projets
          </Link>
        </div>
      </div>
    </main>
  );
}
