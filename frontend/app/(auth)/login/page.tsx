import { LoginForm } from "@/features/auth/components/login-form";

export default function LoginPage() {
  return (
    <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", padding: 24 }}>
      <div style={{ width: "100%", maxWidth: 480, border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", padding: 32 }}>
        <h1 style={{ fontSize: 28, fontWeight: 600, marginBottom: 24 }}>Connexion</h1>
        <LoginForm />
      </div>
    </div>
  );
}
