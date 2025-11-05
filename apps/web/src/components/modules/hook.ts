import { useCallback, useState } from 'react';
import { type EventSourceMessage } from '@microsoft/fetch-event-source';

import type { ICandidateWithScore, IFile } from '@/types';

import type { IMessage } from './types';

const useChatMessages = () => {
  const [messages, setMessages] = useState<IMessage[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [visitedNodes, setVisitedNodes] = useState<string[]>([]);

  const appendVisitedNode = (node: string) => {
    setVisitedNodes((previousNodes) => {
      const lastVisitedNode = previousNodes[previousNodes.length - 1];
      if (lastVisitedNode === node) return previousNodes;
      return [...previousNodes, node];
    });
  };

  const updateMessage = useCallback(
    (
      message: EventSourceMessage,
      botMessageId: string,
      options:
        | {
            onDone?: () => void;
            onNodeChange?: (node: string) => void;
          }
        | undefined
    ) => {
      // eslint-disable-next-line no-console
      console.log('Event:', message.event, message.data);

      switch (message.event) {
        case 'conversationId': {
          const id = message.data;
          setConversationId(id);
          break;
        }

        case 'citations': {
          const data = JSON.parse(message.data) as Array<IFile>;
          setMessages((prev) =>
            prev.map((message) => {
              if (message.id !== botMessageId) return message;

              return {
                ...message,
                citations: data,
              } satisfies IMessage;
            })
          );
          break;
        }

        case 'candidates': {
          const data = JSON.parse(message.data) as Array<ICandidateWithScore>;
          setMessages((prev) =>
            prev.map((message) => {
              if (message.id !== botMessageId) return message;

              return {
                ...message,
                candidates: data,
              } satisfies IMessage;
            })
          );
          break;
        }

        case 'message': {
          const data = JSON.parse(message.data) as { text: string };

          setMessages((prev) =>
            prev.map((message) => {
              if (message.id !== botMessageId) return message;

              return {
                ...message,
                id: botMessageId,
                message: data.text,
                isLoading: false,
                role: 'bot',
                isStreaming: true,
              } satisfies IMessage;
            })
          );
          break;
        }

        case 'reason': {
          const data = JSON.parse(message.data) as { text: string };

          setMessages((prev) =>
            prev.map((message) => {
              if (message.id !== botMessageId) return message;

              return {
                ...message,
                id: botMessageId,
                reason: data.text,
                isLoading: false,
                role: 'bot',
                isStreaming: true,
              } satisfies IMessage;
            })
          );

          break;
        }

        case 'node': {
          const data = message.data;
          options?.onNodeChange?.(data);
          break;
        }

        case 'error': {
          const data = message.data;

          setMessages((prev) =>
            prev.map((message) => {
              if (message.id !== botMessageId) return message;

              return {
                ...message,
                id: botMessageId,
                message: data,
                isLoading: false,
                isStreaming: true,
                isError: true,
              } satisfies IMessage;
            })
          );
          break;
        }

        case 'done': {
          setMessages((prev) =>
            prev.map((message) => {
              if (message.id !== botMessageId) return message;

              return {
                ...message,
                isStreaming: false,
              } satisfies IMessage;
            })
          );

          options?.onDone?.();
          break;
        }
      }
    },
    []
  );

  return {
    messages,
    setMessages,
    updateMessage,
    conversationId,
    setConversationId,
    visitedNodes,
    appendVisitedNode,
    setVisitedNodes,
  } as const;
};

export default useChatMessages;
