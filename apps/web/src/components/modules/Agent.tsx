import React, { useLayoutEffect, useRef, useState } from 'react';
import { Link } from 'react-router';
import { Icon } from '@iconify/react';
import { ActionIcon, Divider, ScrollArea, Tabs, Tooltip } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { EventStreamContentType, fetchEventSource } from '@microsoft/fetch-event-source';
import { ReactFlowProvider } from '@xyflow/react';
import { v4 as uuid } from 'uuid';

import { useAgentWorkflow } from '@/apis/queries/agent.queries';
import { cn } from '@/lib/utils';

import AgentGraph from './AgentGraph';
import ChatInput from './ChatInput';
import ChatMessage from './ChatMessage';
import useChatMessages from './hook';
import Mermaid from './Mermaid';
import type { IMessage } from './types';

interface AgentProps {
  className?: string;
}

const API_URL = import.meta.env.VITE_API_URL;

const Agent: React.FC<AgentProps> = ({ className }) => {
  const workflow = useAgentWorkflow();
  const scrollRef = useRef<HTMLDivElement | null>(null);
  const [isStreaming, setIsStreaming] = useState(false);

  const {
    messages,
    setMessages,
    updateMessage,
    conversationId,
    setConversationId,
    visitedNodes,
    appendVisitedNode,
    setVisitedNodes,
  } = useChatMessages();

  const handleSubmit = async (message: string, hasInterrupt: boolean = false) => {
    const botMessageId = uuid();
    setIsStreaming(true);
    setVisitedNodes([]);

    setMessages((prev) => [
      ...prev,
      {
        id: uuid(),
        role: 'user',
        message,
      } satisfies IMessage,
      {
        id: botMessageId,
        role: 'bot',
        message: '',
        isLoading: true,
      } satisfies IMessage,
    ]);

    const ctrl = new AbortController();

    const messageToSent = hasInterrupt
      ? (messages.find((m) => m.role === 'user')?.message ?? 'Hi')
      : message;

    await fetchEventSource(`${API_URL}/api/agent/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: messageToSent,
        conversation_id: conversationId,
        interrupt_response: hasInterrupt ? { message: message } : undefined,
      }),
      signal: ctrl.signal,
      // eslint-disable-next-line @typescript-eslint/require-await
      async onopen(response) {
        if (response.ok && response.headers.get('content-type') === EventStreamContentType) {
          appendVisitedNode('__start__');
          return;
        } else if (response.status >= 400 && response.status < 500 && response.status !== 429) {
          notifications.show({
            color: 'red',
            message: 'Fatal error occurred!',
          });
        } else {
          notifications.show({
            color: 'yellow',
            message: 'Retry again!',
          });
        }
      },
      onerror(err) {
        setMessages((prev) =>
          prev.map((message) => {
            if (message.id !== botMessageId) return message;

            return {
              ...message,
              id: botMessageId,
              message: err as string,
              isLoading: false,
              role: 'bot',
            } satisfies IMessage;
          })
        );
        ctrl.abort();
      },
      onclose() {
        //
      },
      onmessage(ev) {
        updateMessage(ev, botMessageId, {
          onDone: () => {
            ctrl.abort();
            appendVisitedNode('__end__');
            setIsStreaming(false);
          },
          onNodeChange: (node: string) => {
            appendVisitedNode(node);
          },
        });
      },
    });
  };

  useLayoutEffect(() => {
    scrollRef.current!.scrollTo({
      top: scrollRef.current!.scrollHeight,
      behavior: 'smooth',
    });
  }, [messages]);

  const handleClearConversation = () => {
    setMessages([]);
    setConversationId(null);
  };

  return (
    <section className={cn(className, 'grid grid-cols-[1fr_380px] gap-4')}>
      <div className="flex w-full flex-col overflow-y-auto">
        <div className="flex w-full items-center gap-4">
          <h1 className="font-bold">Agent Chat</h1>

          <Tooltip label="New Conversation">
            <ActionIcon variant="subtle" ml="auto" onClick={handleClearConversation}>
              <Icon icon="mdi:chat-plus" className="text-2xl" />
            </ActionIcon>
          </Tooltip>

          <Tooltip label="Knowledge Base">
            <ActionIcon variant="subtle" to="/knowledge-base" component={Link}>
              <Icon icon="streamline-plump-color:database-flat" className="text-2xl" />
            </ActionIcon>
          </Tooltip>
        </div>

        <Divider className="my-3" />

        <ScrollArea.Autosize offsetScrollbars viewportRef={scrollRef} className="mb-4">
          <div className="flex flex-col gap-y-3">
            {messages.map((message) => (
              <ChatMessage key={message.id} {...message} />
            ))}
          </div>
        </ScrollArea.Autosize>

        <ChatInput className="mt-auto" onSubmit={handleSubmit} disabled={isStreaming} />
      </div>

      <Tabs
        defaultValue="graph"
        keepMounted={false}
        classNames={{
          root: '!flex !flex-col',
          panel: '!grow h-full flex flex-col',
        }}>
        <Tabs.List>
          <Tabs.Tab value="graph">Graph</Tabs.Tab>
          <Tabs.Tab value="mermaid">Mermaid</Tabs.Tab>
        </Tabs.List>

        <Tabs.Panel value="graph">
          {workflow.data?.state ? (
            <ReactFlowProvider>
              <AgentGraph graph={workflow.data.state} visitedNodes={visitedNodes} />
            </ReactFlowProvider>
          ) : null}
        </Tabs.Panel>

        <Tabs.Panel value="mermaid">
          <div className="rounded-2xl border border-amber-400 bg-amber-50/20 py-7">
            {workflow.data?.mermaid ? <Mermaid>{workflow.data.mermaid}</Mermaid> : null}
          </div>
        </Tabs.Panel>
      </Tabs>
    </section>
  );
};

export default Agent;
