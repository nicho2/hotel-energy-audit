"use client";

import type { FormEvent } from "react";
import { useEffect, useMemo, useState } from "react";
import { ApiError } from "@/lib/api-client/errors";
import { BrandMark } from "@/features/branding/components/brand-mark";
import { useI18n } from "@/providers/i18n-provider";
import type { AdminBrandingCreatePayload } from "@/types/admin";
import type { BrandingProfile } from "@/types/branding";
import { AdminGuard } from "./admin-guard";
import { useAdminBranding } from "../hooks/use-admin-branding";

const inputStyle = {
  width: "100%",
  borderRadius: 8,
  border: "1px solid #d1d5db",
  padding: "10px 12px",
  fontSize: 14,
  background: "#fff",
} as const;

const emptyForm: AdminBrandingCreatePayload = {
  name: "",
  company_name: "",
  accent_color: "#14365d",
  logo_text: "",
  contact_email: "",
  cover_tagline: "",
  footer_note: "",
  is_default: false,
};

function toForm(profile: BrandingProfile): AdminBrandingCreatePayload {
  return {
    name: profile.name,
    company_name: profile.company_name,
    accent_color: profile.accent_color,
    logo_text: profile.logo_text ?? "",
    contact_email: profile.contact_email ?? "",
    cover_tagline: profile.cover_tagline ?? "",
    footer_note: profile.footer_note ?? "",
    is_default: profile.is_default,
  };
}

function toPayload(form: AdminBrandingCreatePayload): AdminBrandingCreatePayload {
  return {
    ...form,
    logo_text: form.logo_text?.trim() || null,
    contact_email: form.contact_email?.trim() || null,
    cover_tagline: form.cover_tagline?.trim() || null,
    footer_note: form.footer_note?.trim() || null,
  };
}

export function AdminBrandingPage() {
  const { t } = useI18n();
  const { branding, createBranding, updateBranding } = useAdminBranding();
  const profiles = useMemo(() => branding.data?.data ?? [], [branding.data?.data]);
  const defaultProfile = profiles.find((profile) => profile.is_default) ?? profiles[0] ?? null;
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const selectedProfile = profiles.find((profile) => profile.id === selectedId) ?? null;
  const [form, setForm] = useState<AdminBrandingCreatePayload>(emptyForm);
  const [submitError, setSubmitError] = useState<string | null>(null);

  useEffect(() => {
    if (!selectedId && defaultProfile) {
      setSelectedId(defaultProfile.id);
      setForm(toForm(defaultProfile));
    }
  }, [defaultProfile, selectedId]);

  const startCreate = () => {
    setSelectedId(null);
    setForm(emptyForm);
    setSubmitError(null);
  };

  const handleSelect = (profile: BrandingProfile) => {
    setSelectedId(profile.id);
    setForm(toForm(profile));
    setSubmitError(null);
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitError(null);

    try {
      if (selectedProfile) {
        await updateBranding.mutateAsync({ profileId: selectedProfile.id, payload: toPayload(form) });
      } else {
        await createBranding.mutateAsync(toPayload(form));
      }
    } catch (error) {
      setSubmitError(error instanceof ApiError ? error.message : t("admin.branding.saveError"));
    }
  };

  return (
    <AdminGuard>
      <div style={{ display: "grid", gap: 20 }}>
        <div style={{ display: "grid", gap: 6 }}>
          <div style={{ fontSize: 13, color: "#627084", textTransform: "uppercase", letterSpacing: 0 }}>{t("admin.eyebrow")}</div>
          <h1 style={{ margin: 0, fontSize: 30, fontWeight: 800 }}>{t("admin.branding.title")}</h1>
          <p style={{ margin: 0, color: "#627084", maxWidth: 760 }}>{t("admin.branding.description")}</p>
        </div>

        {branding.isLoading ? <div>{t("admin.branding.loading")}</div> : null}
        {branding.error ? <div style={{ color: "#b91c1c" }}>{t("admin.branding.error")}</div> : null}

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))", gap: 16 }}>
          <section style={{ border: "1px solid #e5e7eb", borderRadius: 8, background: "#fff", padding: 16, display: "grid", gap: 12, alignContent: "start" }}>
            <div style={{ display: "flex", justifyContent: "space-between", gap: 12, alignItems: "center" }}>
              <div style={{ fontSize: 18, fontWeight: 800 }}>{t("admin.branding.profiles")}</div>
              <button type="button" onClick={startCreate} style={{ borderRadius: 8, border: "1px solid #14365d", background: "#14365d", color: "#fff", padding: "8px 10px", fontWeight: 800 }}>
                {t("admin.branding.new")}
              </button>
            </div>
            {profiles.length === 0 && !branding.isLoading ? <div style={{ border: "1px dashed #cbd5e1", borderRadius: 8, padding: 16, color: "#627084" }}>{t("admin.branding.empty")}</div> : null}
            {profiles.map((profile) => (
              <button
                key={profile.id}
                type="button"
                onClick={() => handleSelect(profile)}
                style={{
                  borderRadius: 8,
                  border: selectedProfile?.id === profile.id ? "2px solid #14365d" : "1px solid #e5e7eb",
                  background: "#fff",
                  padding: 12,
                  textAlign: "left",
                }}
              >
                <BrandMark profile={profile} size="sm" />
                {profile.is_default ? <div style={{ marginTop: 8, color: "#166534", fontSize: 12, fontWeight: 800 }}>{t("branding.defaultBadge")}</div> : null}
              </button>
            ))}
          </section>

          <form onSubmit={handleSubmit} style={{ border: "1px solid #e5e7eb", borderRadius: 8, background: "#fff", padding: 20, display: "grid", gap: 14 }}>
            <div style={{ display: "grid", gap: 6 }}>
              <div style={{ fontSize: 18, fontWeight: 800 }}>{selectedProfile ? t("admin.branding.editTitle") : t("admin.branding.createTitle")}</div>
              <BrandMark profile={selectedProfile} />
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 12 }}>
              <input required style={inputStyle} placeholder={t("admin.branding.name")} value={form.name} onChange={(event) => setForm((current) => ({ ...current, name: event.target.value }))} />
              <input required style={inputStyle} placeholder={t("admin.branding.companyName")} value={form.company_name} onChange={(event) => setForm((current) => ({ ...current, company_name: event.target.value }))} />
              <input required type="color" aria-label={t("admin.branding.accentColor")} style={{ ...inputStyle, minHeight: 42 }} value={form.accent_color} onChange={(event) => setForm((current) => ({ ...current, accent_color: event.target.value }))} />
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 12 }}>
              <input style={inputStyle} placeholder={t("admin.branding.logoText")} maxLength={12} value={form.logo_text ?? ""} onChange={(event) => setForm((current) => ({ ...current, logo_text: event.target.value }))} />
              <input type="email" style={inputStyle} placeholder={t("admin.branding.contactEmail")} value={form.contact_email ?? ""} onChange={(event) => setForm((current) => ({ ...current, contact_email: event.target.value }))} />
            </div>
            <textarea style={{ ...inputStyle, minHeight: 76 }} placeholder={t("admin.branding.coverTagline")} value={form.cover_tagline ?? ""} onChange={(event) => setForm((current) => ({ ...current, cover_tagline: event.target.value }))} />
            <textarea style={{ ...inputStyle, minHeight: 76 }} placeholder={t("admin.branding.footerNote")} value={form.footer_note ?? ""} onChange={(event) => setForm((current) => ({ ...current, footer_note: event.target.value }))} />
            <label style={{ display: "flex", alignItems: "center", gap: 8, color: "#142033", fontWeight: 700 }}>
              <input type="checkbox" checked={form.is_default} onChange={(event) => setForm((current) => ({ ...current, is_default: event.target.checked }))} />
              {t("admin.branding.isDefault")}
            </label>
            {submitError ? <div style={{ color: "#b91c1c" }}>{submitError}</div> : null}
            <div style={{ display: "flex", justifyContent: "flex-end" }}>
              <button type="submit" disabled={createBranding.isPending || updateBranding.isPending} style={{ borderRadius: 8, border: "1px solid #14365d", background: "#14365d", color: "#fff", padding: "10px 14px", fontWeight: 800 }}>
                {createBranding.isPending || updateBranding.isPending ? t("admin.branding.saving") : t("common.save")}
              </button>
            </div>
          </form>
        </div>
      </div>
    </AdminGuard>
  );
}
