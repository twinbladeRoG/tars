import type { ICandidate } from '@/types';

import http from '../http';

export const getCandidate = (id: string) => http.get<ICandidate>(`/api/candidate/${id}`);

export const getCandidates = () => http.get<Array<ICandidate>>(`/api/candidate`);
