export const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
export async function POST(req: Request, path: string, init?: RequestInit) {
  const url = `${BACKEND_URL}${path}`;
  return fetch(url, init);
}
