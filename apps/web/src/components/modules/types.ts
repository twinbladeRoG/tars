import type { ICandidateWithResume, ICandidateWithScore, IFile } from '@/types';

export interface IMessage {
  id: string;
  role: 'bot' | 'user';
  message: string;
  reason?: string;
  isLoading?: boolean;
  isError?: boolean;
  isStreaming?: boolean;
  citations?: Array<IFile>;
  candidates?: Array<ICandidateWithScore>;
  resumeCandidates?: Array<ICandidateWithResume>;
}
