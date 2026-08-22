import type { StudentSummary } from "@/types/student";

export function useStudents(): {
  students: StudentSummary[];
  isLoading: boolean;
} {
  // TODO: Implement when backend API is ready
  return { students: [], isLoading: false };
}
