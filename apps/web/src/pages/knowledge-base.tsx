import { useState } from 'react';
import { Title } from '@mantine/core';

import TaskStatus from '@/components/modules/knowledge-base/TaskStatus';
import UserDocumentList from '@/components/modules/knowledge-base/UserDocumentList';
import type { IKnowledgeBaseDocument } from '@/types';

const KnowledgeBasePage = () => {
  const [task, setTask] = useState<IKnowledgeBaseDocument | null>(null);

  return (
    <div>
      <Title order={4} mb="md">
        Documents
      </Title>

      <UserDocumentList className="mb-4" onEnqueue={setTask} />

      {task?.task_id ? <TaskStatus taskId={task?.task_id} /> : null}
    </div>
  );
};

export default KnowledgeBasePage;
