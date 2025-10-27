import type { IEnqueueDocumentRequest, ITaskStatus } from '@/types';

import http from '../http';

export const enqueueDocument = (payload: IEnqueueDocumentRequest) =>
  http.post<ITaskStatus>('/api/knowledge-base', payload);

export const getTaskStatus = (taskId: string) =>
  http.get<ITaskStatus>(`/api/knowledge-base/status/${taskId}`);
