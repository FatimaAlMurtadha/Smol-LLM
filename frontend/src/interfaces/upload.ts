import type { ColumnStats } from "./stats";

export interface UploadResponse {
    message: string;
  stats: Record<string, ColumnStats>;
}