import { type FileWithPath } from '@mantine/dropzone';

import type { IFile, IFileFilterQuery, IPagination } from '@/types';

import http from '../http';

export const getUsersFiles = async (page = 0, limit = 10, filter?: IFileFilterQuery) => {
  const params = new URLSearchParams({
    page: String(page),
    limit: String(limit),
  });

  if (filter?.search) params.append('search', filter.search);
  if (filter?.file_types) {
    filter.file_types.forEach((item) => {
      params.append('file_types', item);
    });
  }

  return http.get<{ data: Array<IFile>; pagination: IPagination }>(
    `/api/file-storage/?${params.toString()}`
  );
};

export const uploadFile = (file: File | FileWithPath) => {
  const headers = new Headers();
  const formData = new FormData();
  formData.append('file', file);

  return http.post<IFile>('/api/file-storage/', formData, { headers });
};

export const removeFile = (fileId: string) => http.delete(`/api/file-storage/${fileId}`);

export const getFile = (fileId: string) => http.get<IFile>(`/api/file-storage/${fileId}`);
