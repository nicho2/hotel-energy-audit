import type { ReactNode } from "react";

type FeedbackTone = "neutral" | "info" | "warning" | "error" | "success";

const toneStyles: Record<FeedbackTone, { border: string; background: string; color: string }> = {
  neutral: { border: "#e5e7eb", background: "#fff", color: "#334155" },
  info: { border: "#bfdbfe", background: "#eff6ff", color: "#1d4ed8" },
  warning: { border: "#fde68a", background: "#fffbeb", color: "#92400e" },
  error: { border: "#fecaca", background: "#fff", color: "#b91c1c" },
  success: { border: "#bbf7d0", background: "#f0fdf4", color: "#166534" },
};

type FeedbackBlockProps = {
  title?: string;
  children: ReactNode;
  tone?: FeedbackTone;
  compact?: boolean;
};

export function FeedbackBlock({ title, children, tone = "neutral", compact = false }: FeedbackBlockProps) {
  const styles = toneStyles[tone];

  return (
    <div
      style={{
        border: `1px solid ${styles.border}`,
        borderRadius: 8,
        background: styles.background,
        color: styles.color,
        padding: compact ? 14 : 20,
        display: "grid",
        gap: title ? 6 : 0,
      }}
    >
      {title ? <div style={{ fontWeight: 800 }}>{title}</div> : null}
      <div style={{ color: tone === "neutral" ? "#627084" : styles.color }}>{children}</div>
    </div>
  );
}

export function FieldError({ children }: { children?: ReactNode }) {
  if (!children) {
    return null;
  }

  return (
    <p style={{ margin: 0, color: "#b91c1c", fontSize: 12, fontWeight: 600 }}>
      {children}
    </p>
  );
}
