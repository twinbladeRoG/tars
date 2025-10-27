import type { FileWithPath } from '@mantine/dropzone';
import { keepPreviousData, useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import type { IFileFilterQuery } from '@/types';

import { getFile, getUsersFiles, removeFile, uploadFile } from '../requests/files-storage.requests';

export const useUploadFile = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (file: File | FileWithPath) => {
      const res = await uploadFile(file);
      return res;
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['user-files'] });
    },
  });
};

export const useUserFiles = (page = 0, limit = 10, filter?: IFileFilterQuery) =>
  useQuery({
    queryKey: ['user-files', page, limit, filter],
    queryFn: async () => {
      const res = await getUsersFiles(page, limit, filter);
      return res;
    },
    placeholderData: keepPreviousData,
  });

export const useRemoveFile = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (fileId: string) => {
      const res = await removeFile(fileId);
      return res;
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['user-files'] });
    },
  });
};

export const useFile = (fileId: string) =>
  useQuery({
    queryKey: ['file', fileId],
    queryFn: async () => {
      const res = await getFile(fileId);
      return res;
    },
  });
