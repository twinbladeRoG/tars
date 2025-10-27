export interface IBaseEntity {
  id: string;
  created_at: string;
  updated_at: string;
}

export interface IPagination {
  page: number;
  limit: number;
  total_pages: number;
  total_count: number;
  has_next: boolean;
  has_previous: boolean;
}
