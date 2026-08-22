export interface PerformancePrediction {
  studentId: string;
  predictedMarks: number;
  predictedGrade: string;
  performanceCategory: string;
}

export interface RiskPrediction {
  studentId: string;
  riskLevel: "low" | "medium" | "high";
  riskProbability: number;
}

export interface PassFailPrediction {
  studentId: string;
  outcome: "pass" | "fail";
  probability: number;
}
