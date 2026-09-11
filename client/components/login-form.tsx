"use client";

import Link from "next/link";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm, useWatch } from "react-hook-form";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { PasswordInput } from "@/components/ui/password-input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { LoadingState } from "@/components/analytics/loading-state";
import { useAuth } from "@/hooks/use-auth";
import { loginSchema, type LoginFormValues } from "@/lib/auth-schemas";
import { ROUTES } from "@/lib/constants";

const ROLE_ITEMS = [
  { value: "institution_admin", label: "Institution Admin" },
  { value: "student", label: "Student" },
  { value: "faculty", label: "Faculty" },
  { value: "parent", label: "Parent" },
] as const;

export function LoginForm() {
  const { login, isLoggingIn } = useAuth();
  const {
    register,
    handleSubmit,
    setValue,
    control,
    formState: { errors },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      role: "institution_admin",
      identifier: "",
      password: "",
    },
  });

  const role = useWatch({ control, name: "role" });

  return (
    <Card className="w-full max-w-sm">
      <CardHeader>
        <CardTitle>Login</CardTitle>
        <CardDescription>
          Sign in to your account. Only admins can sign up.
        </CardDescription>
      </CardHeader>
      <CardContent>
        {isLoggingIn ? (
          <LoadingState message="Signing in..." compact />
        ) : (
          <form
            className="flex flex-col gap-4"
            onSubmit={handleSubmit((values) => login(values))}
          >
            <div className="flex flex-col gap-2">
              <Label htmlFor="role">Role</Label>
              <Select
                items={ROLE_ITEMS}
                value={role}
                onValueChange={(value) =>
                  setValue("role", value as LoginFormValues["role"])
                }
              >
                <SelectTrigger id="role">
                  <SelectValue placeholder="Select role" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="institution_admin">Institution Admin</SelectItem>
                  <SelectItem value="student">Student</SelectItem>
                  <SelectItem value="faculty">Faculty</SelectItem>
                  <SelectItem value="parent">Parent</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="flex flex-col gap-2">
              <Label htmlFor="identifier">
                {role === "student" ? "Roll Number" : "Email"}
              </Label>
              <Input
                id="identifier"
                type={role === "student" ? "text" : "email"}
                placeholder={
                  role === "student" ? "20240001" : "admin@demo.com"
                }
                {...register("identifier")}
              />
              {errors.identifier && (
                <p className="text-sm text-destructive">{errors.identifier.message}</p>
              )}
            </div>
            <div className="flex flex-col gap-2">
              <Label htmlFor="password">Password</Label>
              <PasswordInput id="password" {...register("password")} />
              {errors.password && (
                <p className="text-sm text-destructive">{errors.password.message}</p>
              )}
            </div>
            <Button type="submit" className="w-full">
              Login
            </Button>
            {role === "institution_admin" && (
              <p className="text-center text-sm text-muted-foreground">
                Don&apos;t have an account?{" "}
                <Link
                  href={ROUTES.auth.signup}
                  className="underline underline-offset-4"
                >
                  Sign up
                </Link>
              </p>
            )}
          </form>
        )}
      </CardContent>
    </Card>
  );
}
