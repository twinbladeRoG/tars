import React from 'react';
import { Icon } from '@iconify/react';
import { ActionIcon, Text } from '@mantine/core';
import { modals } from '@mantine/modals';
import { notifications } from '@mantine/notifications';

import { useRemoveFile } from '@/apis/queries/file-storage.queries';
import { useEnqueueDocument } from '@/apis/queries/knowledge-base.queries';
import type { IFile, IKnowledgeBaseDocument } from '@/types';

interface UserDocumentActionProps {
  document: IFile;
  onEnqueue?: (task: IKnowledgeBaseDocument) => void;
}

const UserDocumentAction: React.FC<UserDocumentActionProps> = ({ onEnqueue, document }) => {
  const removeFile = useRemoveFile();
  const enqueueDocument = useEnqueueDocument();

  const handleRemoveFile = () => {
    modals.openConfirmModal({
      title: 'Are you sure you want to delete is file?',
      children: (
        <Text size="sm">
          This action cannot be undone. All data related to this file will be lost.
        </Text>
      ),
      labels: { confirm: 'Confirm', cancel: 'Cancel' },
      onCancel: () => {},
      onConfirm: () => {
        removeFile.mutate(document.id, {
          onError: (err) => {
            notifications.show({
              color: 'red',
              message: err.message,
            });
          },
        });
      },
    });
  };

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

      <ActionIcon
        variant="light"
        color="red"
        disabled={removeFile.isPending}
        loading={removeFile.isPending}
        onClick={handleRemoveFile}>
        <Icon icon="mdi:trash" />
      </ActionIcon>
    </div>
  );
};

export default UserDocumentAction;
