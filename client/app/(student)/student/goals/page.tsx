"use client";

import { useState } from "react";
import { PageHeader } from "@/components/layout/page-header";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Progress } from "@/components/ui/progress";
import { LoadingState } from "@/components/analytics/loading-state";
import { DeleteConfirmButton } from "@/components/layout/delete-confirm-button";
import {
  useCreateGoal,
  useDeleteGoal,
  useGoals,
  useUpdateGoal,
} from "@/hooks/use-goals";
import { useGoalGuidance } from "@/hooks/use-student-performance";

function GoalCard({
  goalType,
  label,
  targetInput,
  setTargetInput,
}: {
  goalType: "cgpa" | "sgpa";
  label: string;
  targetInput: string;
  setTargetInput: (v: string) => void;
}) {
  const { data: goals, isLoading } = useGoals();
  const createGoal = useCreateGoal();
  const updateGoal = useUpdateGoal();
  const deleteGoal = useDeleteGoal();

  const goal = goals?.find((g) => g.goal_type === goalType);
  const current = goal?.current_value ?? 0;
  const target = goal?.target_value ?? (parseFloat(targetInput) || 0);
  const progress = target > 0 ? Math.min(100, (current / target) * 100) : 0;
  const { data: guidance } = useGoalGuidance(
    goalType === "cgpa" ? target : undefined,
  );

  const handleSetGoal = () => {
    const value = parseFloat(targetInput);
    if (goal) {
      updateGoal.mutate({ id: goal.id, target_value: value });
    } else {
      createGoal.mutate({ goal_type: goalType, target_value: value });
    }
  };

  if (isLoading) return <LoadingState />;

  return (
    <Card>
      <CardHeader>
        <CardTitle>{label} Progress</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex justify-between text-sm">
          <span>Current: {current.toFixed(2)}</span>
          <span>Target: {target.toFixed(2)}</span>
        </div>
        <Progress value={progress} />
        <div className="flex items-end gap-2">
          <div className="flex-1 space-y-1">
            <Label>Target {goalType.toUpperCase()}</Label>
            <Input
              type="number"
              step="0.1"
              min="0"
              max="10"
              value={targetInput}
              onChange={(e) => setTargetInput(e.target.value)}
            />
          </div>
          <Button
            onClick={handleSetGoal}
            disabled={createGoal.isPending || updateGoal.isPending}
          >
            {goal ? "Update" : "Set Goal"}
          </Button>
          {goal && (
            <DeleteConfirmButton
              label="Remove"
              confirmLabel="Remove"
              title="Remove goal"
              description={`Are you sure you want to remove your ${label} goal? This action cannot be undone.`}
              variant="outline"
              size="default"
              onConfirm={() => deleteGoal.mutate(goal.id)}
              pending={deleteGoal.isPending}
            />
          )}
        </div>
        {goalType === "cgpa" && guidance && guidance.guidance.length > 0 && (
          <div className="rounded-md border bg-muted/40 p-3 space-y-1">
            <p className="text-sm font-medium">Guidance</p>
            {guidance.guidance.map((line, i) => (
              <p key={i} className="text-sm text-muted-foreground">{line}</p>
            ))}
            {guidance.required_sgpa_hint != null && (
              <p className="text-sm">
                Suggested target SGPA: <strong>{guidance.required_sgpa_hint.toFixed(2)}</strong>
              </p>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export default function StudentGoalsPage() {
  const [targetCgpa, setTargetCgpa] = useState("8.0");
  const [targetSgpa, setTargetSgpa] = useState("8.0");

  return (
    <div className="space-y-6">
      <PageHeader
        title="Academic Goals"
        description="Set and track your CGPA and SGPA targets."
      />
      <GoalCard
        goalType="cgpa"
        label="CGPA"
        targetInput={targetCgpa}
        setTargetInput={setTargetCgpa}
      />
      <GoalCard
        goalType="sgpa"
        label="SGPA"
        targetInput={targetSgpa}
        setTargetInput={setTargetSgpa}
      />
    </div>
  );
}
