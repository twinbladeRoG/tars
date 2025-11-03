import React from 'react';
import { Icon } from '@iconify/react';
import {
  ActionIcon,
  Anchor,
  Badge,
  Card,
  CopyButton,
  Divider,
  ScrollArea,
  Text,
  Title,
} from '@mantine/core';
import dayjs from 'dayjs';

import { useKnowledgeBase } from '@/apis/queries/knowledge-base.queries';
import type { ICandidate } from '@/types';

interface CandidateDetailsProps {
  candidate: ICandidate;
  className?: string;
}

const CandidateDetails: React.FC<CandidateDetailsProps> = ({ candidate, className }) => {
  const knowledgeBase = useKnowledgeBase(candidate.knowledge_base_document_id);

  const formatMonths = (totalMonths: number) => {
    const years = Math.floor(totalMonths / 12);
    const months = totalMonths % 12;

    if (years && months)
      return `${years} year${years > 1 ? 's' : ''} ${months} month${months > 1 ? 's' : ''}`;
    if (years) return `${years} year${years > 1 ? 's' : ''}`;
    return `${months} month${months > 1 ? 's' : ''}`;
  };

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

      <Title order={4}>Skills</Title>

      <div className="flex flex-wrap items-center gap-2">
        {candidate.skills.map((skill) => (
          <Badge size="xs" radius="sm" key={skill}>
            {skill}
          </Badge>
        ))}
      </div>

      <Divider my="sm" />

      <div className="mb-3 flex items-center gap-2">
        <Title order={4}>Experience</Title>
        <Badge size="xs">{candidate.years_of_experience} years</Badge>
      </div>

      <div className="flex flex-col gap-2">
        {candidate.experiences.map((exp, index) => (
          // eslint-disable-next-line @eslint-react/no-array-index-key, react-x/no-array-index-key
          <Card radius="sm" key={index}>
            <Title order={5}>{exp.role}</Title>
            <Title order={6}>{exp.company}</Title>
            <Text size="xs">
              Start Date: {exp.start_date ? dayjs(exp.start_date).format('DD MMM, YYYY') : 'N/A'}
            </Text>
            <Text size="xs">
              End Date: {exp.end_date ? dayjs(exp.end_date).format('DD MMM, YY') : 'N/A'}
            </Text>
            <Text size="xs" mb="xs">
              Duration: {formatMonths(exp.months_in_experience ?? 0)}
            </Text>
            <div className="mb-2 flex flex-wrap items-center gap-2">
              {exp.skills?.split(',').map((skill) => (
                <Badge size="xs" radius="sm" key={skill}>
                  {skill}
                </Badge>
              ))}
            </div>
            <Text size="xs">{exp.additional_info}</Text>
          </Card>
        ))}
      </div>

      <Divider my="sm" />

      <Title order={4}>Certifications</Title>

      <div className="flex flex-wrap items-center gap-2">
        {candidate.certifications.map((cert) => (
          <Badge size="xs" radius="sm" key={cert}>
            {cert}
          </Badge>
        ))}
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
