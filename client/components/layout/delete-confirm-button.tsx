"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";

interface DeleteConfirmButtonProps {
  onConfirm: () => void;
  pending?: boolean;
  itemName?: string;
  title?: string;
  description?: string;
  label?: string;
  confirmLabel?: string;
  variant?: "ghost" | "outline" | "destructive";
  size?: "sm" | "default";
  className?: string;
}

export function DeleteConfirmButton({
  onConfirm,
  pending = false,
  itemName,
  title = "Confirm delete",
  description,
  label = "Delete",
  confirmLabel = "Delete",
  variant = "ghost",
  size = "sm",
  className,
}: DeleteConfirmButtonProps) {
  const [open, setOpen] = useState(false);

  const dialogDescription =
    description ??
    (itemName
      ? `Are you sure you want to delete "${itemName}"? This action cannot be undone.`
      : "Are you sure you want to delete this item? This action cannot be undone.");

  const handleConfirm = () => {
    onConfirm();
    setOpen(false);
  };

  return (
    <>
      <Button
        type="button"
        variant={variant}
        size={size}
        className={className}
        onClick={() => setOpen(true)}
        disabled={pending}
      >
        {label}
      </Button>
      <AlertDialog open={open} onOpenChange={setOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>{title}</AlertDialogTitle>
            <AlertDialogDescription>{dialogDescription}</AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel disabled={pending}>Cancel</AlertDialogCancel>
            <AlertDialogAction
              variant="destructive"
              onClick={handleConfirm}
              disabled={pending}
            >
              {pending ? "Deleting..." : confirmLabel}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
}
