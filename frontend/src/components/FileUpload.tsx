import { useState } from "react";
import { uploadCSV } from "../api/client";
import type { StatsResponse } from "../interfaces/stats";

interface FileUploadProps {
  onStats: (stats: StatsResponse["stats"]) => void;
}

export function FileUpload({ onStats }: FileUploadProps) {
  const [file, setFile] = useState<File | null>(null);

   async function handleSubmit(e: React.FormEvent) {
     e.preventDefault();
     if (!file) return;
     const result = await uploadCSV(file);
     onStats(result.stats);
   }

  return (
    <section className="Upload CSV data">
      <form onSubmit={handleSubmit}>
        <label htmlFor="csv-file" className="btn-choose file">
          VÄLJ EN CSV FIL
        </label>
        <input
          id="csv-file"
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
        <button type="submit" className="btn">
          LADD A UPP
        </button>
      </form>
    </section>
  );
}