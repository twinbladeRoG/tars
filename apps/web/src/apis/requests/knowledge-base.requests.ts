import type {
  IEnqueueDocumentRequest,
  IIngestDocumentsRequest,
  IKnowledgeBaseDocument,
  IKnowledgeBaseDocumentWithFile,
} from '@/types';

import http from '../http';

export const enqueueDocument = (payload: IEnqueueDocumentRequest) =>
  http.post<IKnowledgeBaseDocument>('/api/knowledge-base', payload);

export const getTaskStatus = (taskId: string) =>
  http.get<IKnowledgeBaseDocument>(`/api/knowledge-base/status/${taskId}`);

export const ingestDocuments = (payload: IIngestDocumentsRequest) =>
  http.post<unknown>('/api/knowledge-base/ingest', payload);

export const getKnowledgeBases = () =>
  http.get<Array<IKnowledgeBaseDocumentWithFile>>('/api/knowledge-base/');

export const removeKnowledgeBase = (id: string) => http.delete<null>(`/api/knowledge-base/${id}`);

export const getKnowledgeBaseByFileId = (id: string) =>
  http.get<IKnowledgeBaseDocument>(`/api/knowledge-base/file/${id}`);

export const getKnowledgeBaseById = (id: string) =>
  http.get<IKnowledgeBaseDocument>(`/api/knowledge-base/${id}`);
