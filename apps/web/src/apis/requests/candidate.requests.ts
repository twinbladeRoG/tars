import type { ICandidateWithKnowledgeBase } from '@/types';

import http from '../http';

export const getCandidate = (id: string) =>
  http.get<ICandidateWithKnowledgeBase>(`/api/candidate/${id}`);
