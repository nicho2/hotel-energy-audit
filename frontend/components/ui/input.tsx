import { InputHTMLAttributes } from "react";

export function Input(props: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      {...props}
      style={{
        width: "100%",
        borderRadius: 8,
        border: "1px solid #d1d5db",
        padding: "10px 12px",
        fontSize: 14,
        background: "#fff",
      }}
    />
  );
}
