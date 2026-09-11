"use client";

import Link from "next/link";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
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
import { LoadingState } from "@/components/analytics/loading-state";
import { useAuth } from "@/hooks/use-auth";
import { signupSchema, type SignupFormValues } from "@/lib/auth-schemas";
import { ROUTES } from "@/lib/constants";

export function SignupForm() {
  const { signup, isSigningUp } = useAuth();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SignupFormValues>({
    resolver: zodResolver(signupSchema),
    defaultValues: {
      name: "",
      email: "",
      password: "",
      institution_name: "",
    },
  });

  return (
    <Card className="w-full max-w-sm">
      <CardHeader>
        <CardTitle>Institution Signup</CardTitle>
        <CardDescription>
          Create your institution account. Only Institution Admins can sign up.
        </CardDescription>
      </CardHeader>
      <CardContent>
        {isSigningUp ? (
          <LoadingState message="Creating account..." compact />
        ) : (
          <form
            className="flex flex-col gap-4"
            onSubmit={handleSubmit((values) => signup(values))}
          >
            <div className="flex flex-col gap-2">
              <Label htmlFor="name">Name</Label>
              <Input id="name" type="text" placeholder="Your name" {...register("name")} />
              {errors.name && (
                <p className="text-sm text-destructive">{errors.name.message}</p>
              )}
            </div>
            <div className="flex flex-col gap-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="admin@university.edu"
                {...register("email")}
              />
              {errors.email && (
                <p className="text-sm text-destructive">{errors.email.message}</p>
              )}
            </div>
            <div className="flex flex-col gap-2">
              <Label htmlFor="password">Password</Label>
              <PasswordInput id="password" autoComplete="new-password" {...register("password")} />
              {errors.password && (
                <p className="text-sm text-destructive">{errors.password.message}</p>
              )}
            </div>
            <div className="flex flex-col gap-2">
              <Label htmlFor="institution">University / Institution Name</Label>
              <Input
                id="institution"
                type="text"
                placeholder="University name"
                {...register("institution_name")}
              />
              {errors.institution_name && (
                <p className="text-sm text-destructive">
                  {errors.institution_name.message}
                </p>
              )}
            </div>
            <Button type="submit" className="w-full">
              Create Account
            </Button>
            <p className="text-center text-sm text-muted-foreground">
              Already have an account?{" "}
              <Link
                href={ROUTES.auth.login}
                className="underline underline-offset-4"
              >
                Login
              </Link>
            </p>
          </form>
        )}
      </CardContent>
    </Card>
  );
}
