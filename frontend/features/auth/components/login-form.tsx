"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { loginSchema, LoginFormValues } from "../schemas/login-schema";
import { login } from "../api/login";
import { ApiError } from "@/lib/api-client/errors";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useAuthContext } from "@/providers/auth-provider";
import { useI18n } from "@/providers/i18n-provider";

export function LoginForm() {
  const router = useRouter();
  const { isReady, setAuth, token, user } = useAuthContext();
  const { t } = useI18n();
  const [submitError, setSubmitError] = useState<string | null>(null);
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  });

  useEffect(() => {
    if (isReady && token && user) {
      router.replace("/projects");
    }
  }, [isReady, router, token, user]);

  const onSubmit = async (values: LoginFormValues) => {
    setSubmitError(null);

    try {
      const response = await login(values);
      setAuth(response.data.access_token, response.data.user);
      router.push("/projects");
    } catch (error) {
      setSubmitError(error instanceof ApiError ? error.message : t("login.submitError"));
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} style={{ display: "grid", gap: 16, width: "100%", maxWidth: 380 }}>
      <div>
        <Input placeholder={t("login.emailPlaceholder")} type="email" {...register("email")} />
        {errors.email ? <p style={{ color: "#dc2626", fontSize: 12 }}>{errors.email.message}</p> : null}
      </div>
      <div>
        <Input placeholder={t("login.passwordPlaceholder")} type="password" {...register("password")} />
        {errors.password ? <p style={{ color: "#dc2626", fontSize: 12 }}>{errors.password.message}</p> : null}
      </div>
      {submitError ? <p style={{ color: "#dc2626", fontSize: 13, margin: 0 }}>{submitError}</p> : null}
      <Button type="submit" disabled={isSubmitting}>
        {isSubmitting ? t("login.submitting") : t("login.submit")}
      </Button>
    </form>
  );
}
