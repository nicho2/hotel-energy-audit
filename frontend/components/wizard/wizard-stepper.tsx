import type { WizardStep } from "@/types/wizard";

export function WizardStepper({ steps }: { steps: WizardStep[] }) {
  return (
    <div style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", padding: 16 }}>
      <div style={{ display: "grid", gap: 12 }}>
        {steps.map((item, index) => (
          <div key={item.code} style={{ display: "flex", justifyContent: "space-between" }}>
            <div style={{ fontWeight: 600 }}>{index + 1}. {item.label}</div>
            <div style={{ color: "#6b7280", fontSize: 14 }}>{item.status}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
