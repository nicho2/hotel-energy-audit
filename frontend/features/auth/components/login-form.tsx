"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { loginSchema, LoginFormValues } from "../schemas/login-schema";
import { login } from "../api/login";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useAuthContext } from "@/providers/auth-provider";

export function LoginForm() {
  const { setAuth } = useAuthContext();
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (values: LoginFormValues) => {
    const response: any = await login(values);
    setAuth(response.data.access_token, response.data.user);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} style={{ display: "grid", gap: 16, width: "100%", maxWidth: 380 }}>
      <div>
        <Input placeholder="Email" type="email" {...register("email")} />
        {errors.email ? <p style={{ color: "#dc2626", fontSize: 12 }}>{errors.email.message}</p> : null}
      </div>
      <div>
        <Input placeholder="Mot de passe" type="password" {...register("password")} />
        {errors.password ? <p style={{ color: "#dc2626", fontSize: 12 }}>{errors.password.message}</p> : null}
      </div>
      <Button type="submit" disabled={isSubmitting}>Se connecter</Button>
    </form>
  );
}
