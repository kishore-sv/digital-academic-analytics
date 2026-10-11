export function formatYearNumber(yearNumber: number): string {
  if (yearNumber < 1) return `Year ${yearNumber}`;
  const mod100 = yearNumber % 100;
  const suffix =
    mod100 >= 11 && mod100 <= 13
      ? "th"
      : ({ 1: "st", 2: "nd", 3: "rd" } as Record<number, string>)[
          yearNumber % 10
        ] ?? "th";
  return `${yearNumber}${suffix} Year`;
}
