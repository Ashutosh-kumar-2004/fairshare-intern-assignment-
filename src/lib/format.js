export function formatDate(date) {
  if (date instanceof Date && !Number.isNaN(date.getTime())) {
    return date.toLocaleDateString("en-IN", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  }
  
  if (typeof date === "string") {
    return date.slice(0, 10);
  }
  return String(date);
}
export function dateValue(date) { 
  const parsedDate = new Date(date);
  return !isNaN(parsedDate.getTime()) ? parsedDate.getTime() : 0;
}
