"use client";

import type { ReactNode } from "react";
import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { env } from "@/lib/config/env";
import type { AuthSession, AuthUser } from "@/types/auth";

type AuthContextType = {
  isReady: boolean;
  user: AuthUser | null;
  token: string | null;
  setAuth: (token: string, user: AuthUser) => void;
  clearAuth: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isReady, setIsReady] = useState(false);
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<AuthUser | null>(null);

  useEffect(() => {
    try {
      const storedSession = window.localStorage.getItem(env.authStorageKey);

      if (storedSession) {
        const session = JSON.parse(storedSession) as AuthSession;
        setToken(session.token);
        setUser(session.user);
      }
    } catch {
      window.localStorage.removeItem(env.authStorageKey);
    } finally {
      setIsReady(true);
    }
  }, []);

  const value = useMemo(
    () => ({
      isReady,
      user,
      token,
      setAuth: (nextToken: string, nextUser: AuthUser) => {
        const session: AuthSession = {
          token: nextToken,
          user: nextUser,
        };

        setToken(nextToken);
        setUser(nextUser);
        window.localStorage.setItem(env.authStorageKey, JSON.stringify(session));
      },
      clearAuth: () => {
        setToken(null);
        setUser(null);
        window.localStorage.removeItem(env.authStorageKey);
      },
    }),
    [isReady, token, user],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuthContext() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuthContext must be used within AuthProvider");
  return ctx;
}
