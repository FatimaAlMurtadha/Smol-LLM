export interface ColumnStats{
    count: number;
    mean: number;
    std: number;
    min: number;
    "25%": number;
    "50%": number;
    "75%": number;
    max: number;
}

export interface StatsResponse {
    stats : Record<string, ColumnStats>;
}