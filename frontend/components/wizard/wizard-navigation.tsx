type WizardNavigationProps = {
  canGoPrevious: boolean;
  canGoNext: boolean;
  onPrevious: () => void;
  onNext: () => void;
  isSaving?: boolean;
};

export function WizardNavigation({
  canGoPrevious,
  canGoNext,
  onPrevious,
  onNext,
  isSaving = false,
}: WizardNavigationProps) {
  return (
    <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
      <button
        type="button"
        onClick={onPrevious}
        disabled={!canGoPrevious || isSaving}
        style={{
          borderRadius: 10,
          border: "1px solid #d1d5db",
          background: "#fff",
          padding: "10px 14px",
          fontWeight: 600,
          cursor: !canGoPrevious || isSaving ? "not-allowed" : "pointer",
        }}
      >
        Precedent
      </button>

      <button
        type="button"
        onClick={onNext}
        disabled={!canGoNext || isSaving}
        style={{
          borderRadius: 10,
          border: "1px solid #14365d",
          background: "#14365d",
          color: "#fff",
          padding: "10px 14px",
          fontWeight: 600,
          cursor: !canGoNext || isSaving ? "not-allowed" : "pointer",
        }}
      >
        {isSaving ? "Enregistrement..." : "Suivant"}
      </button>
    </div>
  );
}
