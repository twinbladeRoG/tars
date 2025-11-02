import { useQuery } from '@tanstack/react-query';

import { getCandidate } from '../requests/candidate.requests';

export const useCandidate = (id: string) =>
  useQuery({
    queryKey: ['candidate', id],
    queryFn: async () => {
      return await getCandidate(id);
    },
    enabled: !!id,
  });
