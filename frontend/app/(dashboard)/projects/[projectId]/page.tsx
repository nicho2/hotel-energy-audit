export default async function ProjectDetailPage({
  params,
}: {
  params: Promise<{ projectId: string }>;
}) {
  const { projectId } = await params;

  return (
    <div style={{ display: "grid", gap: 24 }}>
      <h1 style={{ fontSize: 32, fontWeight: 600 }}>Projet {projectId}</h1>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16 }}>
        <div style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", padding: 16 }}>Énergie</div>
        <div style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", padding: 16 }}>CO₂</div>
        <div style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", padding: 16 }}>BACS</div>
        <div style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", padding: 16 }}>ROI</div>
      </div>
    </div>
  );
}
