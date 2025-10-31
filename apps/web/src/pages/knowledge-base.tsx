import { useState } from 'react';
import { Title } from '@mantine/core';
import { notifications } from '@mantine/notifications';

import { useIngestDocuments } from '@/apis/queries/knowledge-base.queries';
import KnowledgeBaseDocuments from '@/components/modules/knowledge-base/KnowledgeBaseDocuments';
import TaskStatus from '@/components/modules/knowledge-base/TaskStatus';
import UserDocumentList from '@/components/modules/knowledge-base/UserDocumentList';
import type { IKnowledgeBaseDocument } from '@/types';

const KnowledgeBasePage = () => {
  const [task, setTask] = useState<IKnowledgeBaseDocument | null>(null);

  const ingest = useIngestDocuments();

  const handleIngest = (documentIds: string[]) => {
    ingest.mutate(
      { documents: documentIds },
      {
        onError: (e) => {
          notifications.show({
            color: 'red',
            message: e.message,
          });
        },
      }
    );
  };

  return (
    <div>
      <Title order={4} mb="md">
        Documents
      </Title>

      <UserDocumentList
        className="mb-4"
        onEnqueue={setTask}
        onIngest={handleIngest}
        isIngesting={ingest.isPending}
      />

      {task?.task_id ? <TaskStatus className="mb-4" taskId={task?.task_id} /> : null}

      <KnowledgeBaseDocuments />
    </div>
  );
};

export default KnowledgeBasePage;
