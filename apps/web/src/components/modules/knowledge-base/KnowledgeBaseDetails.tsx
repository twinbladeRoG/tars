import React from 'react';
import { Divider, Text, Title } from '@mantine/core';

import { useKnowledgeBaseByFileId } from '@/apis/queries/knowledge-base.queries';
import type { IFile } from '@/types';

interface KnowledgeBaseDetailsProps {
  file: IFile;
  className?: string;
}

const KnowledgeBaseDetails: React.FC<KnowledgeBaseDetailsProps> = ({ className, file }) => {
  const knowledgeBase = useKnowledgeBaseByFileId(file.id);

  return (
    <div className={className}>
      <Title order={4}>{file.original_filename}</Title>
      <Divider my="sm" />
      <Text size="sm">{knowledgeBase.data?.content}</Text>
    </div>
  );
};

export default KnowledgeBaseDetails;
