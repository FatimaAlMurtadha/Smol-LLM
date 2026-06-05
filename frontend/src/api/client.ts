// here is the most important component that connect both side
export const API_URL = "http://127.0.0.1:8000/"; // change this to your backend url if it's different
import type { UploadResponse } from "../interfaces/upload";
import type { AskResponse } from "../interfaces/ask";

export async function uploadCSV(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_URL}/data/upload`, {
    method: "POST",
    body: formData,
  });

  return res.json();
}

export async function askQuestion(question: string): Promise<AskResponse> {
  const res = await fetch(`${API_URL}/ai/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  return res.json();
}