"use client";

import type { FormEvent } from "react";
import { useState } from "react";
import { ApiError } from "@/lib/api-client/errors";
import { useAuthContext } from "@/providers/auth-provider";
import { useI18n } from "@/providers/i18n-provider";
import { AdminGuard } from "./admin-guard";
import { useAdminUsers } from "../hooks/use-admin-users";
import type { AdminUserCreatePayload } from "@/types/admin";

const inputStyle = {
  width: "100%",
  borderRadius: 8,
  border: "1px solid #d1d5db",
  padding: "10px 12px",
  fontSize: 14,
  background: "#fff",
} as const;

function formatDate(value: string, language: string) {
  return new Intl.DateTimeFormat(language === "en" ? "en-US" : "fr-FR", {
    dateStyle: "medium",
  }).format(new Date(value));
}

export function AdminUsersPage() {
  const { language, t } = useI18n();
  const { user: currentUser } = useAuthContext();
  const { users, createUser, deactivateUser } = useAdminUsers();
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [form, setForm] = useState<AdminUserCreatePayload>({
    email: "",
    password: "",
    first_name: "",
    last_name: "",
    role: "member",
    preferred_language: "fr",
  });

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitError(null);
    try {
      await createUser.mutateAsync({
        ...form,
        first_name: form.first_name?.trim() || null,
        last_name: form.last_name?.trim() || null,
      });
      setForm({ email: "", password: "", first_name: "", last_name: "", role: "member", preferred_language: "fr" });
    } catch (error) {
      setSubmitError(error instanceof ApiError ? error.message : t("admin.users.createError"));
    }
  };

  const handleDeactivate = async (userId: string) => {
    setSubmitError(null);
    try {
      await deactivateUser.mutateAsync(userId);
    } catch (error) {
      setSubmitError(error instanceof ApiError ? error.message : t("admin.users.deactivateError"));
    }
  };

  return (
    <AdminGuard>
      <div style={{ display: "grid", gap: 20 }}>
        <div style={{ display: "grid", gap: 6 }}>
          <div style={{ fontSize: 13, color: "#627084", textTransform: "uppercase", letterSpacing: 0 }}>{t("admin.eyebrow")}</div>
          <h1 style={{ margin: 0, fontSize: 30, fontWeight: 800 }}>{t("admin.users.title")}</h1>
          <p style={{ margin: 0, color: "#627084", maxWidth: 760 }}>{t("admin.users.description")}</p>
        </div>

        <form onSubmit={handleSubmit} style={{ border: "1px solid #e5e7eb", borderRadius: 8, background: "#fff", padding: 20, display: "grid", gap: 14 }}>
          <div style={{ fontSize: 18, fontWeight: 800 }}>{t("admin.users.createTitle")}</div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 12 }}>
            <input required type="email" style={inputStyle} placeholder={t("admin.users.email")} value={form.email} onChange={(event) => setForm((current) => ({ ...current, email: event.target.value }))} />
            <input required type="password" minLength={8} style={inputStyle} placeholder={t("admin.users.password")} value={form.password} onChange={(event) => setForm((current) => ({ ...current, password: event.target.value }))} />
            <select style={inputStyle} value={form.role} onChange={(event) => setForm((current) => ({ ...current, role: event.target.value }))}>
              <option value="member">{t("admin.roles.member")}</option>
              <option value="org_admin">{t("admin.roles.org_admin")}</option>
            </select>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: 12 }}>
            <input style={inputStyle} placeholder={t("admin.users.firstName")} value={form.first_name ?? ""} onChange={(event) => setForm((current) => ({ ...current, first_name: event.target.value }))} />
            <input style={inputStyle} placeholder={t("admin.users.lastName")} value={form.last_name ?? ""} onChange={(event) => setForm((current) => ({ ...current, last_name: event.target.value }))} />
            <select style={inputStyle} value={form.preferred_language} onChange={(event) => setForm((current) => ({ ...current, preferred_language: event.target.value }))}>
              <option value="fr">FR</option>
              <option value="en">EN</option>
            </select>
          </div>
          {submitError ? <div style={{ color: "#b91c1c" }}>{submitError}</div> : null}
          <div style={{ display: "flex", justifyContent: "flex-end" }}>
            <button type="submit" disabled={createUser.isPending} style={{ borderRadius: 8, border: "1px solid #14365d", background: "#14365d", color: "#fff", padding: "10px 14px", fontWeight: 800 }}>
              {createUser.isPending ? t("admin.users.creating") : t("admin.users.create")}
            </button>
          </div>
        </form>

        {users.isLoading ? <div>{t("admin.users.loading")}</div> : null}
        {users.error ? <div style={{ color: "#b91c1c" }}>{t("admin.users.error")}</div> : null}
        {(users.data?.data ?? []).length === 0 && !users.isLoading ? <div style={{ border: "1px dashed #cbd5e1", borderRadius: 8, padding: 24, color: "#627084" }}>{t("admin.users.empty")}</div> : null}
        {(users.data?.data ?? []).length > 0 ? (
          <section style={{ border: "1px solid #e5e7eb", borderRadius: 8, background: "#fff", overflowX: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
              <thead>
                <tr style={{ background: "#f8fafc", textAlign: "left" }}>
                  {[t("admin.users.email"), t("admin.users.name"), t("admin.users.role"), t("admin.users.status"), t("admin.users.created"), t("common.actions")].map((label) => (
                    <th key={label} style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>{label}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {(users.data?.data ?? []).map((user) => (
                  <tr key={user.id}>
                    <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>{user.email}</td>
                    <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>{[user.first_name, user.last_name].filter(Boolean).join(" ") || "-"}</td>
                    <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>{t(`admin.roles.${user.role}`)}</td>
                    <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>{user.is_active ? t("admin.users.active") : t("admin.users.inactive")}</td>
                    <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>{formatDate(user.created_at, language)}</td>
                    <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>
                      <button type="button" disabled={!user.is_active || user.id === currentUser?.id || deactivateUser.isPending} onClick={() => handleDeactivate(user.id)} style={{ borderRadius: 8, border: "1px solid #fecaca", background: "#fff", color: "#b91c1c", padding: "8px 12px", fontWeight: 700 }}>
                        {t("admin.users.deactivate")}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        ) : null}
      </div>
    </AdminGuard>
  );
}
