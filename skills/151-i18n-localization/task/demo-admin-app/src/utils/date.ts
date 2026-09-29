export function formatDate(d: Date): string {
  return `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`;
}

export function formatMoney(n: number): string {
  return '¥' + n.toFixed(2);
}
