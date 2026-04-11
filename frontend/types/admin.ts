export type AdminUser = {
  id: string;
  organization_id: string;
  email: string;
  first_name: string | null;
  last_name: string | null;
  role: string;
  preferred_language: string;
  is_active: boolean;
  created_at: string;
};

export type AdminUserCreatePayload = {
  email: string;
  password: string;
  first_name: string | null;
  last_name: string | null;
  role: string;
  preferred_language: string;
};

export type AdminBrandingCreatePayload = {
  name: string;
  company_name: string;
  accent_color: string;
  logo_text: string | null;
  contact_email: string | null;
  cover_tagline: string | null;
  footer_note: string | null;
  is_default: boolean;
};

export type AdminBrandingUpdatePayload = Partial<AdminBrandingCreatePayload>;
