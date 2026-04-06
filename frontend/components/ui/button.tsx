import { ButtonHTMLAttributes } from "react";

export function Button({ children, ...props }: ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      {...props}
      style={{
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        borderRadius: 8,
        padding: "10px 16px",
        fontSize: 14,
        fontWeight: 600,
        background: "#111827",
        color: "#fff",
        border: "1px solid #111827",
        cursor: "pointer",
      }}
    >
      {children}
    </button>
  );
}
