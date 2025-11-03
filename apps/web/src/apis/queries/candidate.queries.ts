import { useQuery } from '@tanstack/react-query';

import { getCandidate, getCandidates } from '../requests/candidate.requests';

export const useCandidate = (id: string) =>
  useQuery({
    queryKey: ['candidate', id],
    queryFn: async () => {
      return await getCandidate(id);
    },
    enabled: !!id,
  });

export const useCandidates = () =>
  useQuery({
    queryKey: ['candidates'],
    queryFn: async () => {
      return await getCandidates();
    },
  });
