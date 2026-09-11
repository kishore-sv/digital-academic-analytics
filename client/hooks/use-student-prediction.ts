"use client";

import { useEffect } from "react";
import { useMyParentProfile } from "@/hooks/use-academic";
import { usePredictForStudent } from "@/hooks/use-predictions";
import { useMyStudentProfile } from "@/hooks/use-students";

export function useMyStudentPrediction(studentId?: string) {
  const { data: myStudent } = useMyStudentProfile();
  const { data: parentProfile } = useMyParentProfile();
  const targetId =
    studentId ??
    myStudent?.id ??
    parentProfile?.linked_student_ids[0] ??
    undefined;

  const { mutate, ...prediction } = usePredictForStudent({ silent: true });

  useEffect(() => {
    if (targetId) {
      mutate(targetId);
    }
  }, [targetId, mutate]);

  return { ...prediction, mutate, studentId: targetId };
}
