import type { WizardStep } from "@/types/wizard";

type WizardStepperProps = {
  steps: WizardStep[];
  activeStepCode?: string;
  onSelectStep?: (stepCode: string) => void;
};

function getStepAccent(status: WizardStep["status"], isActive: boolean) {
  if (isActive) {
    return { background: "#14365d", color: "#ffffff" };
  }

  if (status === "completed") {
    return { background: "#e7f6ec", color: "#166534" };
  }

  if (status === "current") {
    return { background: "#e8eef7", color: "#14365d" };
  }

  return { background: "#f8fafc", color: "#627084" };
}

export function WizardStepper({ steps, activeStepCode, onSelectStep }: WizardStepperProps) {
  return (
    <div style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", padding: 16 }}>
      <div style={{ display: "grid", gap: 12 }}>
        {steps.map((item) => {
          const isActive = activeStepCode === item.code;
          const accent = getStepAccent(item.status, isActive);

          return (
            <button
              key={item.code}
              type="button"
              onClick={() => onSelectStep?.(item.code)}
              style={{
                display: "grid",
                gap: 8,
                width: "100%",
                textAlign: "left",
                border: "1px solid #e5e7eb",
                borderRadius: 12,
                background: "#fff",
                padding: 12,
                cursor: onSelectStep ? "pointer" : "default",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", gap: 12, alignItems: "center" }}>
                <div style={{ fontWeight: 600 }}>{item.step}. {item.name}</div>
                <div
                  style={{
                    fontSize: 13,
                    fontWeight: 600,
                    borderRadius: 999,
                    padding: "4px 8px",
                    ...accent,
                  }}
                >
                  {item.status}
                </div>
              </div>
              {item.validations.length > 0 ? (
                <div style={{ fontSize: 12, color: "#627084" }}>{item.validations[0]?.message}</div>
              ) : null}
            </button>
          );
        })}
      </div>
    </div>
  );
}
