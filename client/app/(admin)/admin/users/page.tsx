"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { PasswordInput } from "@/components/ui/password-input";
import { Label } from "@/components/ui/label";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { DeleteConfirmButton } from "@/components/layout/delete-confirm-button";
import { DataListPage } from "@/components/layout/data-list-page";
import { TableSerialCell, TableSerialHead } from "@/components/layout/table-serial";
import {
  useCreateAdminUser,
  useDeleteUser,
  useUpdateUser,
  useUsers,
} from "@/hooks/use-users";

export default function AdminUsersPage() {
  const { data, isLoading, error } = useUsers();
  const users = data?.data ?? [];
  const createUser = useCreateAdminUser();
  const updateUser = useUpdateUser();
  const deleteUser = useDeleteUser();
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({ email: "", password: "" });

  const handleCreate = async () => {
    try {
      await createUser.mutateAsync(form);
      setOpen(false);
      setForm({ email: "", password: "" });
    } catch {
      // Error toast handled by mutation hook.
    }
  };

  return (
    <DataListPage
      title="Admin Users"
      description="Manage institution admin accounts."
      isLoading={isLoading}
      error={error}
      isEmpty={users.length === 0}
      emptyTitle="No admin users found"
    >
      <div className="mb-4 flex justify-end">
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger render={<Button />}>Add Admin</DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add Institution Admin</DialogTitle>
            </DialogHeader>
            <div className="space-y-3">
              <div className="space-y-1">
                <Label>Email</Label>
                <Input
                  type="email"
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                />
              </div>
              <div className="space-y-1">
                <Label>Password</Label>
                <PasswordInput
                  autoComplete="new-password"
                  value={form.password}
                  onChange={(e) => setForm({ ...form, password: e.target.value })}
                />
              </div>
              <Button onClick={handleCreate} disabled={createUser.isPending}>
                Create
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableSerialHead />
            <TableHead>Email</TableHead>
            <TableHead>Role</TableHead>
            <TableHead>Status</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {users.map((user, index) => (
            <TableRow key={user.id}>
              <TableSerialCell index={index} />
              <TableCell>{user.email ?? "—"}</TableCell>
              <TableCell>{user.role}</TableCell>
              <TableCell>
                {user.is_login_enabled ? "Enabled" : "Disabled"}
              </TableCell>
              <TableCell className="space-x-2 text-right">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() =>
                    updateUser.mutate({
                      id: user.id,
                      is_login_enabled: !user.is_login_enabled,
                    })
                  }
                >
                  {user.is_login_enabled ? "Disable" : "Enable"}
                </Button>
                <DeleteConfirmButton
                  itemName={user.email ?? user.role}
                  onConfirm={() => deleteUser.mutate(user.id)}
                  pending={deleteUser.isPending}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </DataListPage>
  );
}
