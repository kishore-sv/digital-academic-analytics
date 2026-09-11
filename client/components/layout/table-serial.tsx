import { TableCell, TableHead } from "@/components/ui/table";

export function TableSerialHead() {
  return <TableHead className="w-12 text-center">#</TableHead>;
}

export function TableSerialCell({
  index,
  start = 1,
}: {
  index: number;
  start?: number;
}) {
  return (
    <TableCell className="w-12 text-center tabular-nums text-muted-foreground">
      {start + index}
    </TableCell>
  );
}

export function serialStart(page = 1, pageSize = 0) {
  return (page - 1) * pageSize + 1;
}
