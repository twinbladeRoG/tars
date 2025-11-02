import { useState } from 'react';

import TaskStatus from '@/components/modules/knowledge-base/TaskStatus';
import UploadForm from '@/components/modules/knowledge-base/UploadForm';
import UserDocuments from '@/components/modules/knowledge-base/UserDocuments';
import type { IKnowledgeBaseDocument } from '@/types';

const DocumentsPage = () => {
  const [task, setTask] = useState<IKnowledgeBaseDocument | null>(null);

  return (
    <div>
      <UploadForm />

      <UserDocuments className="mb-7" onEnqueue={setTask} />

      {task?.task_id ? <TaskStatus className="mb-4" taskId={task?.task_id} /> : null}
    </div>
  );
};

export default DocumentsPage;
