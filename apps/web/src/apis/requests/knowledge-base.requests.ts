import type {
  IEnqueueDocumentRequest,
  IIngestDocumentsRequest,
  IKnowledgeBaseDocument,
} from '@/types';

import http from '../http';

export const enqueueDocument = (payload: IEnqueueDocumentRequest) =>
  http.post<IKnowledgeBaseDocument>('/api/knowledge-base', payload);

export const getTaskStatus = (taskId: string) =>
  http.get<IKnowledgeBaseDocument>(`/api/knowledge-base/status/${taskId}`);

export const ingestDocuments = (payload: IIngestDocumentsRequest) =>
  http.post<unknown>('/api/knowledge-base/ingest', payload);
