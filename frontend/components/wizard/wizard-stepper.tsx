export function WizardStepper({ steps }: { steps: { step: number; name: string; status: string }[] }) {
  return (
    <div style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", padding: 16 }}>
      <div style={{ display: "grid", gap: 12 }}>
        {steps.map((item) => (
          <div key={item.step} style={{ display: "flex", justifyContent: "space-between" }}>
            <div style={{ fontWeight: 600 }}>{item.step}. {item.name}</div>
            <div style={{ color: "#6b7280", fontSize: 14 }}>{item.status}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
