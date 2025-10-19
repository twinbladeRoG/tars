export interface IMessage {
  id: string;
  role: 'bot' | 'user';
  message: string;
  reason?: string;
  isLoading?: boolean;
  isError?: boolean;
  isStreaming?: boolean;
}
