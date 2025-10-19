import type { IAgentWorkflow } from '@/types/entities';

import http from '../http';

export const getAgentWorkflow = () => http.get<IAgentWorkflow>('/api/agent/workflow');
