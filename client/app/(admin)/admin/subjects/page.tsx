import { redirect } from "next/navigation";
import { ROUTES } from "@/lib/constants";

export default function AdminSubjectsPage() {
  redirect(ROUTES.admin.courses);
}
