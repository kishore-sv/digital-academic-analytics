"use client";

import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "@/lib/api";
import type {
  AnalyticsFilters,
  AtRiskSummary,
  AttendancePerformancePoint,
  ChartBucket,
  DepartmentAnalytics,
  DepartmentRiskStack,
  InstitutionalAnalytics,
  PerformanceIndicators,
  PerformanceTrendPoint,
  PassFailTrendPoint,
  PredictionPassFailAnalytics,
  PredictionPerformanceAnalytics,
  PredictionRiskAnalytics,
  RiskDistribution,
  RiskFactorCount,
} from "@/types/analytics";
import { filtersToQuery } from "@/types/analytics";

function withFilters(path: string, filters?: AnalyticsFilters) {
  return `${path}${filters ? filtersToQuery(filters) : ""}`;
}

export function useAnalyticsOverview(filters?: AnalyticsFilters) {
  return useQuery({
    queryKey: ["analytics", "overview", filters],
    queryFn: () =>
      apiFetch<InstitutionalAnalytics>(withFilters("/analytics/overview", filters)),
  });
}

export function useScopedAnalyticsOverview(filters?: AnalyticsFilters) {
  return useQuery({
    queryKey: ["analytics", "scoped", "overview", filters],
    queryFn: () =>
      apiFetch<InstitutionalAnalytics>(
        withFilters("/analytics/scoped/overview", filters),
      ),
  });
}

export function useDepartmentAnalytics(filters?: AnalyticsFilters) {
  return useQuery({
    queryKey: ["analytics", "departments", filters],
    queryFn: () =>
      apiFetch<DepartmentAnalytics[]>(
        withFilters("/analytics/departments", filters),
      ),
  });
}

export function useScopedDepartmentAnalytics(filters?: AnalyticsFilters) {
  return useQuery({
    queryKey: ["analytics", "scoped", "departments", filters],
    queryFn: () =>
      apiFetch<DepartmentAnalytics[]>(
        withFilters("/analytics/scoped/departments", filters),
      ),
  });
}

export function useRiskDistribution(filters?: AnalyticsFilters) {
  return useQuery({
    queryKey: ["analytics", "risk-distribution", filters],
    queryFn: () =>
      apiFetch<RiskDistribution>(
        withFilters("/analytics/risk-distribution", filters),
      ),
  });
}

export function useScopedRiskDistribution(filters?: AnalyticsFilters) {
  return useQuery({
    queryKey: ["analytics", "scoped", "risk-distribution", filters],
    queryFn: () =>
      apiFetch<RiskDistribution>(
        withFilters("/analytics/scoped/risk-distribution", filters),
      ),
  });
}

export function useCGPADistribution(filters?: AnalyticsFilters, scoped = false) {
  const base = scoped ? "/analytics/scoped/cgpa-distribution" : "/analytics/cgpa-distribution";
  return useQuery({
    queryKey: ["analytics", "cgpa-distribution", scoped, filters],
    queryFn: () => apiFetch<ChartBucket[]>(withFilters(base, filters)),
  });
}

export function usePerformanceTrends(filters?: AnalyticsFilters, scoped = false) {
  const base = scoped
    ? "/analytics/scoped/performance-trends"
    : "/analytics/performance-trends";
  return useQuery({
    queryKey: ["analytics", "performance-trends", scoped, filters],
    queryFn: () =>
      apiFetch<PerformanceTrendPoint[]>(withFilters(base, filters)),
  });
}

export function usePassFailTrend(filters?: AnalyticsFilters) {
  return useQuery({
    queryKey: ["analytics", "pass-fail-trend", filters],
    queryFn: () =>
      apiFetch<PassFailTrendPoint[]>(
        withFilters("/analytics/pass-fail-trend", filters),
      ),
  });
}

export function useAttendancePerformance(filters?: AnalyticsFilters, scoped = false) {
  const base = scoped
    ? "/analytics/scoped/attendance-performance"
    : "/analytics/attendance-performance";
  return useQuery({
    queryKey: ["analytics", "attendance-performance", scoped, filters],
    queryFn: () =>
      apiFetch<AttendancePerformancePoint[]>(withFilters(base, filters)),
  });
}

export function usePerformanceIndicators(filters?: AnalyticsFilters) {
  return useQuery({
    queryKey: ["analytics", "performance-indicators", filters],
    queryFn: () =>
      apiFetch<PerformanceIndicators>(
        withFilters("/analytics/performance-indicators", filters),
      ),
  });
}

export function useDepartmentRiskStacks(filters?: AnalyticsFilters, scoped = false) {
  const base = scoped
    ? "/analytics/scoped/department-risk-stacks"
    : "/analytics/department-risk-stacks";
  return useQuery({
    queryKey: ["analytics", "department-risk-stacks", scoped, filters],
    queryFn: () =>
      apiFetch<DepartmentRiskStack[]>(withFilters(base, filters)),
  });
}

export function useRiskFactors(filters?: AnalyticsFilters, scoped = false) {
  const base = scoped ? "/analytics/scoped/risk-factors" : "/analytics/risk-factors";
  return useQuery({
    queryKey: ["analytics", "risk-factors", scoped, filters],
    queryFn: () => apiFetch<RiskFactorCount[]>(withFilters(base, filters)),
  });
}

export function usePredictionPerformance(filters?: AnalyticsFilters) {
  return useQuery({
    queryKey: ["analytics", "predictions", "performance", filters],
    queryFn: () =>
      apiFetch<PredictionPerformanceAnalytics>(
        withFilters("/analytics/predictions/performance", filters),
      ),
  });
}

export function usePredictionPassFail(filters?: AnalyticsFilters) {
  return useQuery({
    queryKey: ["analytics", "predictions", "pass-fail", filters],
    queryFn: () =>
      apiFetch<PredictionPassFailAnalytics>(
        withFilters("/analytics/predictions/pass-fail", filters),
      ),
  });
}

export function usePredictionRisk(filters?: AnalyticsFilters, scoped = false) {
  const base = scoped
    ? "/analytics/scoped/predictions/risk"
    : "/analytics/predictions/risk";
  return useQuery({
    queryKey: ["analytics", "predictions", "risk", scoped, filters],
    queryFn: () =>
      apiFetch<PredictionRiskAnalytics>(withFilters(base, filters)),
  });
}

export function useAtRiskSummary(filters?: AnalyticsFilters) {
  return useQuery({
    queryKey: ["at-risk", "summary", filters],
    queryFn: () =>
      apiFetch<AtRiskSummary>(withFilters("/at-risk/summary", filters)),
  });
}
