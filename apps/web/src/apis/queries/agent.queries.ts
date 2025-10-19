import { useQuery } from '@tanstack/react-query';

import { getAgentWorkflow } from '../requests/agent.requests';

export const useAgentWorkflow = () =>
  useQuery({
    queryKey: ['agent-workflow'],
    queryFn: async () => {
      const res = await getAgentWorkflow();
      return res;
    },
  });
