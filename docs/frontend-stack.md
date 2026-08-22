# Frontend Stack

Client-side libraries, patterns, and auth session handling for the Next.js application.

**These libraries are not yet installed.** This document is the implementation specification.

## Required Libraries

| Library | Version target | Purpose | Install command (future) |
|---------|---------------|---------|--------------------------|
| `@tanstack/react-query` | v5 | Server state, caching, mutations, loading/error states | `bun add @tanstack/react-query` |
| `react-hook-form` | latest | Form state management | `bun add react-hook-form` |
| `zod` | latest | Schema validation | `bun add zod` |
| `@hookform/resolvers` | latest | Zod resolver for react-hook-form | `bun add @hookform/resolvers` |

## Why These Libraries

### TanStack Query

Four role-based portals (admin, student, faculty, parent) each make multiple API calls. Raw `fetch` + `useEffect` leads to:
- Duplicate requests across components
- No shared loading/error state
- Manual cache invalidation after mutations
- Stale data after create/update operations

TanStack Query provides caching, deduplication, background refetch, and mutation hooks out of the box.

### react-hook-form + zod

shadcn/ui forms are designed to pair with react-hook-form for state and zod for validation. Required for:
- Login form (role selector + credentials)
- Admin signup form
- Institution setup form
- Student goal-setting form
- Admin user creation forms

## Provider Setup (planned)

```tsx
// app/providers.tsx (future)
"use client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 60_000, retry: 1 },
  },
});

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}
```

Wrap in root `layout.tsx` alongside existing `TooltipProvider`.

## Auth Session Handling

JWT tokens are stored in **httpOnly cookies** set by the FastAPI backend — not in `localStorage` or `sessionStorage`. This prevents XSS from stealing auth tokens.

### How the Client Reads Auth State

The client does not decode the JWT directly. Instead:

1. On app load, call `GET /api/auth/me` (cookie sent automatically by the browser)
2. Backend decodes JWT, returns `{ user_id, role, institution_id, name }`
3. `useAuth` hook stores this in React state / TanStack Query cache
4. On `401` from `/api/auth/me`, redirect to `/login`

### Token Refresh

When an API call returns `401` with code `AUTH_TOKEN_EXPIRED`:
1. Call `POST /api/auth/refresh` (refresh cookie sent automatically)
2. Backend issues new access token cookie
3. Retry the original request

### Route Protection

Next.js middleware (`middleware.ts`) checks for the `access_token` cookie and validates the role against the route prefix:

| Route prefix | Allowed roles | Redirect on mismatch |
|-------------|---------------|---------------------|
| `/admin/*` | `admin` | `/login` |
| `/student/*` | `student` | `/login` |
| `/faculty/*` | `faculty` | `/login` |
| `/parent/*` | `parent` | `/login` |
| `/login`, `/signup` | unauthenticated only | role dashboard if already logged in |

Middleware runs on the Edge — it checks cookie presence only. Full role validation happens server-side on every API call.

## Data Fetching Pattern (planned)

```tsx
// hooks/use-students.ts (future implementation)
import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "@/lib/api";

export function useStudents(page = 1, limit = 20) {
  return useQuery({
    queryKey: ["students", page, limit],
    queryFn: () => apiFetch(`/students?page=${page}&limit=${limit}`),
  });
}
```

## Form Pattern (planned)

```tsx
// Example: login form with zod validation (future)
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const loginSchema = z.object({
  identifier: z.string().min(1),
  password: z.string().min(8),
  role: z.enum(["admin", "student", "faculty", "parent"]),
});
```

## API Client

`client/lib/api.ts` will be updated to:
- Send requests with `credentials: "include"` (required for httpOnly cookies)
- Handle `401` → refresh → retry logic
- Parse the pagination envelope from [api-conventions.md](api-conventions.md)

## Related Documentation

- [Security](security.md)
- [Authentication](authentication.md)
- [API Conventions](api-conventions.md)
- [Authorization](authorization.md)
