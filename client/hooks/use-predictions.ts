import type {
  PerformancePrediction,
  RiskPrediction,
} from "@/types/prediction";

export function usePredictions(): {
  performance: PerformancePrediction | null;
  risk: RiskPrediction | null;
  isLoading: boolean;
} {
  // TODO: Implement when backend API is ready
  return { performance: null, risk: null, isLoading: false };
}
