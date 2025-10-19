import React, { useMemo } from 'react';
import { Icon } from '@iconify/react/dist/iconify.js';
import { Accordion, Loader, Skeleton } from '@mantine/core';
import Markdown from 'marked-react';

import { cn } from '@/lib/utils';

import renderer from '../markdown';

import type { IMessage } from './types';

interface SplitMessage {
  content: string | null;
  thought?: string;
  isThinking?: boolean;
}

const ChatMessage: React.FC<IMessage> = ({
  message,
  reason,
  isError,
  isLoading,
  isStreaming,
  role,
}) => {
  const isUser = role === 'user';
  // for reasoning model, we split the message into content and thought
  // TODO: implement this as remark/rehype plugin in the future
  const { content, thought, isThinking }: SplitMessage = useMemo(() => {
    if (message === null || isUser) return { content: message };

    let actualContent = '';
    let thought = '';
    let isThinking = false;

    const hasOpeningThinkTag = message.includes('<think>');
    const hasClosingThinkTag = message.includes('</think>');

    let thinkSplit: string[] = [];

    if (hasOpeningThinkTag && hasClosingThinkTag) {
      thinkSplit = message.split('<think>', 2);
      actualContent += thinkSplit[0];
    } else if (hasClosingThinkTag && !hasOpeningThinkTag) {
      thinkSplit = ['', message];
    } else {
      return { content: message };
    }

    while (thinkSplit[1] !== undefined) {
      // <think> tag found
      thinkSplit = thinkSplit[1].split('</think>', 2);
      thought += thinkSplit[0];
      isThinking = true;
      if (thinkSplit[1] !== undefined) {
        // </think> closing tag found
        isThinking = false;
        thinkSplit = thinkSplit[1].split('<think>', 2);
        actualContent += thinkSplit[0];
      }
    }

    return { content: actualContent, thought, isThinking };
  }, [message, isUser]);

  return (
    <div
      className={cn('max-w-[80%] rounded-lg p-4', {
        'self-end bg-gray-900': isUser,
        'self-start': !isUser,
        'bg-red-950': isError,
        'min-w-3/4': isLoading,
      })}>
      {isLoading ? <Skeleton height={40} /> : null}

      {!isLoading && !isUser && (reason || thought) ? (
        <Accordion
          defaultValue={null}
          mb="md"
          classNames={{
            label: '!py-2',
          }}>
          <Accordion.Item value="thought">
            <Accordion.Control icon={<Icon icon="mdi:thought-bubble" />}>
              Thought {isThinking ? <Loader /> : null}
            </Accordion.Control>
            <Accordion.Panel className="">
              {reason ? <Markdown renderer={renderer}>{reason}</Markdown> : null}
              {thought ? <Markdown renderer={renderer}>{thought}</Markdown> : null}
            </Accordion.Panel>
          </Accordion.Item>
        </Accordion>
      ) : null}

      <Markdown renderer={renderer}>{content}</Markdown>

      {isStreaming && !isUser ? (
        <div className="mt-2">
          <Skeleton height={16} radius="sm" />
          <Skeleton height={16} mt={12} radius="sm" />
          <Skeleton height={16} mt={12} width="70%" radius="sm" />
        </div>
      ) : null}
    </div>
  );
};

export default ChatMessage;
