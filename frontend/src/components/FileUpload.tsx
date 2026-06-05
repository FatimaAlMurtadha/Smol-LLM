import { useState } from "react";
import { uploadCSV } from "../api/client";
import type { StatsResponse } from "../interfaces/stats";

interface FileUploadProps {
  onStats: (stats: StatsResponse["stats"]) => void;
}

export function FileUpload({ onStats }: FileUploadProps) {
  const [file, setFile] = useState<File | null>(null);

  async function handleUpload() {
    if (!file) return;
    const result = await uploadCSV(file);
    onStats(result.stats);
  }

  return (
    <div className="card">
      <h2>Ladda upp en CSV fil</h2>
      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      <button className="btn" onClick={handleUpload}>
        Uppladda
      </button>
    </div>
  );
}