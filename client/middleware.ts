import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

import { ROLE_DASHBOARD } from "@/lib/session";

const PUBLIC_PATHS = ["/", "/login", "/signup"];

const ROLE_ROUTE_PREFIX: Record<string, string> = {
  institution_admin: "/admin",
  student: "/student",
  faculty: "/faculty",
  parent: "/parent",
};

function isPublicPath(pathname: string) {
  return PUBLIC_PATHS.some(
    (path) => pathname === path || pathname.startsWith(`${path}/`),
  );
}

function getProtectedPrefix(pathname: string) {
  return Object.values(ROLE_ROUTE_PREFIX).find((prefix) =>
    pathname.startsWith(prefix),
  );
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const sessionRole = request.cookies.get("session_role")?.value;

  if (isPublicPath(pathname)) {
    if (sessionRole && (pathname === "/login" || pathname === "/signup")) {
      const dashboard = ROLE_DASHBOARD[sessionRole] ?? "/";
      return NextResponse.redirect(new URL(dashboard, request.url));
    }
    return NextResponse.next();
  }

  const protectedPrefix = getProtectedPrefix(pathname);
  if (!protectedPrefix) {
    return NextResponse.next();
  }

  if (!sessionRole) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("from", pathname);
    return NextResponse.redirect(loginUrl);
  }

  const allowedPrefix = ROLE_ROUTE_PREFIX[sessionRole];
  if (allowedPrefix && !pathname.startsWith(allowedPrefix)) {
    const dashboard = ROLE_DASHBOARD[sessionRole] ?? "/login";
    return NextResponse.redirect(new URL(dashboard, request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|.*\\..*).*)"],
};
