import type { PerformanceSummary } from "@/types/performance";

export function usePerformance(): {
  performance: PerformanceSummary | null;
  isLoading: boolean;
} {
  // TODO: Implement when backend API is ready
  return { performance: null, isLoading: false };
}
