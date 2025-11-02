import React, { useMemo } from 'react';
import { Icon } from '@iconify/react/dist/iconify.js';
import { Accordion, ActionIcon, Button, Loader, ScrollArea, Skeleton } from '@mantine/core';
import { useClipboard } from '@mantine/hooks';
import Markdown from 'marked-react';

import { cn } from '@/lib/utils';
import type { IFile } from '@/types';

import renderer from '../markdown';

import type { IMessage } from './types';

interface SplitMessage {
  content: string | null;
  thought?: string;
  isThinking?: boolean;
}

export interface ChatMessageProps extends IMessage {
  onClickCitation: (file: IFile) => void;
}

const ChatMessage: React.FC<ChatMessageProps> = ({
  message,
  reason,
  isError,
  isLoading,
  isStreaming,
  role,
  citations,
  onClickCitation,
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

  const clipboard = useClipboard({ timeout: 500 });

  return (
    <div
      className={cn('flex max-w-[80%] flex-col', {
        'self-end': isUser,
        'self-start': !isUser,
        'bg-red-950': isError,
        'min-w-3/4': isLoading,
      })}>
      <div
        className={cn('mb-2 rounded-lg', {
          'bg-gray-900 p-4': isUser,
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

        {citations && citations.length > 0 ? (
          <ScrollArea.Autosize mah={300} mt="md">
            <div className="flex">
              {citations?.map((citation) => (
                <Button
                  key={citation.id}
                  mr="md"
                  variant="light"
                  onClick={() => onClickCitation(citation)}>
                  <p className="whitespace-nowrap">{citation.original_filename}</p>
                </Button>
              ))}
            </div>
          </ScrollArea.Autosize>
        ) : null}
      </div>

      <ActionIcon
        disabled={isLoading || isStreaming}
        className={isUser ? 'self-end' : 'self-start'}
        variant="subtle"
        color={clipboard.copied ? 'teal' : 'blue'}
        onClick={() => clipboard.copy(content)}>
        <Icon icon={clipboard.copied ? 'mdi:check' : 'mdi:content-copy'} />
      </ActionIcon>
    </div>
  );
};

export default ChatMessage;
