import { NextRequest } from "next/server";

export async function POST(req: NextRequest) {
  const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
  const body = await req.text();
  const res = await fetch(`${BACKEND_URL}/api/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body,
  });
  const txt = await res.text();
  return new Response(txt, {
    status: res.status,
    headers: { "Content-Type": res.headers.get("content-type") || "application/json" },
  });
}
