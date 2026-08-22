"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ROUTES } from "@/lib/constants";

export function SignupForm() {
  return (
    <Card className="w-full max-w-sm">
      <CardHeader>
        <CardTitle>Institution Signup</CardTitle>
        <CardDescription>
          Create your institution account. Only Institution Admins can sign up.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form
          className="flex flex-col gap-4"
          onSubmit={(e) => e.preventDefault()}
        >
          <div className="flex flex-col gap-2">
            <Label htmlFor="name">Name</Label>
            <Input id="name" type="text" placeholder="Your name" required />
          </div>
          <div className="flex flex-col gap-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="admin@university.edu"
              required
            />
          </div>
          <div className="flex flex-col gap-2">
            <Label htmlFor="password">Password</Label>
            <Input id="password" type="password" required />
          </div>
          <div className="flex flex-col gap-2">
            <Label htmlFor="institution">University / Institution Name</Label>
            <Input
              id="institution"
              type="text"
              placeholder="University name"
              required
            />
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
      </CardContent>
    </Card>
  );
}
