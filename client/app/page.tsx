import Link from "next/link";
import { buttonVariants } from "@/components/ui/button";
import { ROUTES } from "@/lib/constants";

export default function HomePage() {
  return (
    <div className="flex flex-1 flex-col items-center justify-center gap-6 p-8">
      <div className="text-center">
        <h1 className="text-3xl font-bold tracking-tight">
          PRJ_649 — Academic Analytics
        </h1>
        <p className="mt-2 text-muted-foreground">
          Digital Academic Performance Monitoring and Institutional Analytics
          System
        </p>
      </div>
      <div className="flex gap-4">
        <Link href={ROUTES.auth.login} className={buttonVariants()}>
          Login
        </Link>
        <Link
          href={ROUTES.auth.signup}
          className={buttonVariants({ variant: "outline" })}
        >
          Institution Signup
        </Link>
      </div>
    </div>
  );
}
