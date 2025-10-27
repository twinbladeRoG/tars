import React from 'react';
import { Icon } from '@iconify/react';
import { ActionIcon } from '@mantine/core';
import { notifications } from '@mantine/notifications';

import { useEnqueueDocument } from '@/apis/queries/knowledge-base.queries';
import type { IFile, IKnowledgeBaseDocument } from '@/types';

interface UserExtractActionProps {
  document: IFile;
  onEnqueue?: (task: IKnowledgeBaseDocument) => void;
}

const UserExtractAction: React.FC<UserExtractActionProps> = ({ document, onEnqueue }) => {
  const enqueueDocument = useEnqueueDocument();

  const handleExtract = () => {
    enqueueDocument.mutate(
      { file_id: document.id },
      {
        onSuccess: (data) => {
          onEnqueue?.(data);
        },
        onError: (error) => {
          notifications.show({
            color: 'red',
            message: error?.message,
          });
        },
      }
    );
  };

  return (
    <div className="flex justify-end gap-2">
      <ActionIcon
        variant="light"
        color="blue"
        title="Extract"
        disabled={enqueueDocument.isPending}
        loading={enqueueDocument.isPending}
        onClick={handleExtract}>
        <Icon icon="ri:file-zip-fill" />
      </ActionIcon>
    </div>
  );
};

export default UserExtractAction;
