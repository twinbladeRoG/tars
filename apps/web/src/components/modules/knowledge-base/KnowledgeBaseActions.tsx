import React from 'react';
import { Icon } from '@iconify/react';
import { ActionIcon, Text } from '@mantine/core';
import { modals } from '@mantine/modals';
import { notifications } from '@mantine/notifications';
import { useQueryClient } from '@tanstack/react-query';

import { useRemoveKnowledgeBase, useTaskStatus } from '@/apis/queries/knowledge-base.queries';
import type { IKnowledgeBaseDocumentWithFile } from '@/types';

interface KnowledgeBaseActionsProps {
  knowledgeBase: IKnowledgeBaseDocumentWithFile;
}

const KnowledgeBaseActions: React.FC<KnowledgeBaseActionsProps> = ({ knowledgeBase }) => {
  const remove = useRemoveKnowledgeBase();
  const task = useTaskStatus(knowledgeBase.task_id);
  const queryClient = useQueryClient();

  const handleRemoveFile = () => {
    modals.openConfirmModal({
      title: 'Are you sure you want to delete is file?',
      children: <Text size="sm">This action cannot be undone</Text>,
      labels: { confirm: 'Confirm', cancel: 'Cancel' },
      onCancel: () => {},
      onConfirm: () => {
        remove.mutate(knowledgeBase.id, {
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

  const handleRefresh = async () => {
    await task.refetch();
    await queryClient.invalidateQueries({ queryKey: ['knowledge-bases'] });
  };

  return (
    <div className="flex justify-end gap-2">
      {knowledgeBase.task_id ? (
        <ActionIcon
          variant="light"
          disabled={task.isFetching}
          loading={task.isFetching}
          onClick={handleRefresh}>
          <Icon icon="mdi:refresh" />
        </ActionIcon>
      ) : null}

      <ActionIcon
        variant="light"
        color="red"
        disabled={remove.isPending}
        loading={remove.isPending}
        onClick={handleRemoveFile}>
        <Icon icon="mdi:trash" />
      </ActionIcon>
    </div>
  );
};

export default KnowledgeBaseActions;
