export type AuthUser = {
  id: string;
  email: string;
  role: string;
  organization_id: string;
  preferred_language: string;
};

export type AuthSession = {
  token: string;
  user: AuthUser;
};
