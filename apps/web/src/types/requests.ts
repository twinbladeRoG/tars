export interface ILoginRequest {
  username: string;
  password: string;
}

export interface ITokenResponse {
  access_token: string;
  refresh_token: string;
}

export interface IFileFilterQuery {
  search?: string;
  file_types?: string[];
}

export interface IEnqueueDocumentRequest {
  file_id: string;
}

export interface IIngestDocumentsRequest {
  documents: string[];
}
