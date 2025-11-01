import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import type { IEnqueueDocumentRequest, IIngestDocumentsRequest } from '@/types';

import {
  enqueueDocument,
  getKnowledgeBaseByFileId,
  getKnowledgeBases,
  getTaskStatus,
  ingestDocuments,
  removeKnowledgeBase,
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
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: IIngestDocumentsRequest) => {
      const res = await ingestDocuments(data);
      return res;
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['knowledge-bases'] });
    },
  });
};

export const useKnowledgeBases = () =>
  useQuery({
    queryKey: ['knowledge-bases'],
    queryFn: async () => {
      const res = await getKnowledgeBases();
      return res;
    },
  });

export const useRemoveKnowledgeBase = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string) => {
      return removeKnowledgeBase(id);
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['knowledge-bases'] });
    },
  });
};

export const useKnowledgeBaseByFileId = (id: string) =>
  useQuery({
    queryKey: ['knowledge-base-file', id],
    queryFn: async () => {
      const res = await getKnowledgeBaseByFileId(id);
      return res;
    },
  });
