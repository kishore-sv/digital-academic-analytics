interface RecommendationListProps {
  title: string;
  items: string[];
}

export function RecommendationList({ title, items }: RecommendationListProps) {
  if (!items.length) return null;

  return (
    <div className="space-y-2">
      <h3 className="text-sm font-medium">{title}</h3>
      <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}
