import { useMutation, useQuery } from '@tanstack/react-query';

import type { IEnqueueDocumentRequest, IIngestDocumentsRequest } from '@/types';

import {
  enqueueDocument,
  getTaskStatus,
  ingestDocuments,
} from '../requests/knowledge-base.requests';

export const useEnqueueDocument = () => {
  return useMutation({
    mutationFn: async (data: IEnqueueDocumentRequest) => {
      const res = await enqueueDocument(data);
      return res;
    },
  });
};

export const useTaskStatus = (taskId: string) =>
  useQuery({
    queryKey: ['task', taskId],
    queryFn: async () => {
      const res = await getTaskStatus(taskId);
      return res;
    },
  });

export const useIngestDocuments = () => {
  return useMutation({
    mutationFn: async (data: IIngestDocumentsRequest) => {
      const res = await ingestDocuments(data);
      return res;
    },
  });
};
