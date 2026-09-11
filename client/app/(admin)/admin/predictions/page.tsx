"use client";

import { useState } from "react";
import { EmptyState } from "@/components/analytics/empty-state";
import { LoadingState } from "@/components/analytics/loading-state";
import { PredictionCard } from "@/components/analytics/prediction-card";
import { StudentPredictionRunner } from "@/components/analytics/student-prediction-runner";
import { PageHeader } from "@/components/layout/page-header";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { usePredictAll } from "@/hooks/use-predictions";

export default function AdminPredictionsPage() {
  const { mutate, data, isPending, error } = usePredictAll();
  const [form, setForm] = useState({
    CA_mark: 75,
    MID_mark: 70,
    attendance_percentage: 85,
    study_hours_per_week: 15,
    assignment_completion_pct: 90,
    previous_sgpa: 7.5,
    previous_cgpa: 7.2,
    backlog_count: 0,
    course_credits: 3,
    course_type: "THEORY",
    branch: "CSE",
    semester: 5,
  });

  return (
    <div className="space-y-6">
      <PageHeader
        title="ML Predictions"
        description="Run predictions on real student data or test with manual features."
      />

      <Tabs defaultValue="student">
        <TabsList>
          <TabsTrigger value="student">Student Data</TabsTrigger>
          <TabsTrigger value="manual">Manual Features</TabsTrigger>
        </TabsList>
        <TabsContent value="student" className="mt-4">
          <StudentPredictionRunner />
        </TabsContent>
        <TabsContent value="manual" className="mt-4 space-y-4">
          <div className="grid gap-4 sm:grid-cols-3">
            {(["CA_mark", "MID_mark", "attendance_percentage"] as const).map(
              (key) => (
                <div key={key} className="space-y-1">
                  <Label>{key}</Label>
                  <Input
                    type="number"
                    value={form[key]}
                    onChange={(e) =>
                      setForm({ ...form, [key]: parseFloat(e.target.value) })
                    }
                  />
                </div>
              ),
            )}
          </div>
          <Button onClick={() => mutate(form)} disabled={isPending}>
            {isPending ? "Predicting..." : "Run Prediction"}
          </Button>
          {isPending && <LoadingState />}
          {error && <EmptyState title="Prediction failed" />}
          {data && <PredictionCard predictions={data} />}
        </TabsContent>
      </Tabs>
    </div>
  );
}
