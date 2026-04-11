export type BrandingProfile = {
  id: string;
  organization_id: string;
  name: string;
  company_name: string;
  accent_color: string;
  logo_text: string | null;
  contact_email: string | null;
  cover_tagline: string | null;
  footer_note: string | null;
  is_default: boolean;
  created_at: string;
};
