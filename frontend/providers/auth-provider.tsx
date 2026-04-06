"use client";

import { createContext, useContext, useMemo, useState } from "react";

type AuthUser = {
  id: string;
  email: string;
  role: string;
  organization_id: string;
  preferred_language: string;
} | null;

type AuthContextType = {
  user: AuthUser;
  token: string | null;
  setAuth: (token: string, user: NonNullable<AuthUser>) => void;
  clearAuth: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<AuthUser>(null);

  const value = useMemo(
    () => ({
      user,
      token,
      setAuth: (nextToken: string, nextUser: NonNullable<AuthUser>) => {
        setToken(nextToken);
        setUser(nextUser);
      },
      clearAuth: () => {
        setToken(null);
        setUser(null);
      },
    }),
    [token, user],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuthContext() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuthContext must be used within AuthProvider");
  return ctx;
}
