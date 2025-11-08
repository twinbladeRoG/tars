import React, { useMemo } from 'react';
import { Icon } from '@iconify/react';
import { ActionIcon, Anchor, CopyButton, Divider, Text, Title } from '@mantine/core';
import DOMPurify from 'dompurify';

import type { ICandidateWithResume } from '@/types';

interface ResumeCandidateDetailsProps {
  candidate: ICandidateWithResume;
  className?: string;
}

const ResumeCandidateDetails: React.FC<ResumeCandidateDetailsProps> = ({
  candidate,
  className,
}) => {
  function highlightChunks(text: string, chunks: string[]) {
    let updated = text;

    chunks.forEach((chunk) => {
      const escaped = chunk.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const regex = new RegExp(escaped, 'gi');

      updated = updated.replace(
        regex,
        (match) => `<span class="text-black bg-yellow-200">${match}</span>`
      );
    });

    return updated;
  }

  const safeHtml = useMemo(
    () =>
      DOMPurify.sanitize(
        highlightChunks(candidate.knowledge_base_document.content ?? '', candidate.chunks)
      ),
    [candidate]
  );

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

      {candidate.knowledge_base_document ? (
        <>
          <Title order={4} mb="md">
            Resume Content
          </Title>
          {/* eslint-disable-next-line @eslint-react/dom/no-dangerously-set-innerhtml */}
          <div className="text-sm" dangerouslySetInnerHTML={{ __html: safeHtml }} />
        </>
      ) : (
        <Text>Knowledge Base not found</Text>
      )}
    </div>
  );
};

export default ResumeCandidateDetails;
