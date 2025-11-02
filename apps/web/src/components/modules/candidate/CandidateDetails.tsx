import React from 'react';
import { Icon } from '@iconify/react';
import { ActionIcon, Anchor, CopyButton, Divider, ScrollArea, Text, Title } from '@mantine/core';

import { useKnowledgeBase } from '@/apis/queries/knowledge-base.queries';
import type { ICandidate } from '@/types';

interface CandidateDetailsProps {
  candidate: ICandidate;
  className?: string;
}

const CandidateDetails: React.FC<CandidateDetailsProps> = ({ candidate, className }) => {
  const knowledgeBase = useKnowledgeBase(candidate.knowledge_base_document_id);
  return (
    <div className={className}>
      <Title order={4}>{candidate.name}</Title>

      <div className="flex items-center">
        <Text size="sm" mr="sm">
          Email: <Anchor href={`mailto:${candidate.email}`}>{candidate.email}</Anchor>
        </Text>

        <CopyButton value={candidate.email} timeout={2000}>
          {({ copied, copy }) => (
            <ActionIcon color={copied ? 'teal' : 'gray'} variant="subtle" onClick={copy}>
              {copied ? <Icon icon="mdi:check-all" /> : <Icon icon="mdi:content-copy" />}
            </ActionIcon>
          )}
        </CopyButton>
      </div>

      <div className="flex items-center">
        <Text size="sm" mr="sm">
          Contact: <Anchor href={`tel:${candidate.contact}`}>{candidate.contact}</Anchor>
        </Text>

        {candidate.contact ? (
          <CopyButton value={candidate.contact} timeout={2000}>
            {({ copied, copy }) => (
              <ActionIcon color={copied ? 'teal' : 'gray'} variant="subtle" onClick={copy}>
                {copied ? <Icon icon="mdi:check-all" /> : <Icon icon="mdi:content-copy" />}
              </ActionIcon>
            )}
          </CopyButton>
        ) : null}
      </div>

      <Divider my="sm" />

      {knowledgeBase.data ? (
        <>
          <Title order={4} mb="md">
            Resume Content
          </Title>
          <ScrollArea.Autosize mah={300} className="bg-gray-800 p-4">
            <Text size="sm">{knowledgeBase.data.content}</Text>
          </ScrollArea.Autosize>
        </>
      ) : (
        <Text>Knowledge Base not found</Text>
      )}
    </div>
  );
};

export default CandidateDetails;
