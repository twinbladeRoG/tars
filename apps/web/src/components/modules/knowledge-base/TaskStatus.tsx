import React, { useMemo } from 'react';
import { Icon } from '@iconify/react';
import {
  ActionIcon,
  Badge,
  Card,
  type DefaultMantineColor,
  Divider,
  ScrollArea,
  Text,
} from '@mantine/core';

import { useTaskStatus } from '@/apis/queries/knowledge-base.queries';
import { EXTRACTION_STATUS } from '@/types';

interface TaskStatusProps {
  taskId: string;
}

const TaskStatus: React.FC<TaskStatusProps> = ({ taskId }) => {
  const task = useTaskStatus(taskId);

  const extractionStatusColor = useMemo((): DefaultMantineColor => {
    switch (task.data?.status) {
      case EXTRACTION_STATUS.FAILURE:
        return 'red';
      case EXTRACTION_STATUS.PENDING:
        return 'yellow';
      case EXTRACTION_STATUS.RECEIVED:
        return 'green';
      case EXTRACTION_STATUS.RETRY:
        return 'orange';
      case EXTRACTION_STATUS.REVOKED:
        return 'red';
      case EXTRACTION_STATUS.STARTED:
        return 'green';
      case EXTRACTION_STATUS.SUCCESS:
        return 'green';
      default:
        return 'gray';
    }
  }, [task.data]);

  return (
    <Card>
      <p className="mb-3">Task: {task.data?.task_id}</p>
      <div className="mb-7 flex items-center justify-between gap-4">
        <Badge color={extractionStatusColor}>{task.data?.status}</Badge>

        <ActionIcon onClick={() => task.refetch()} loading={task.isFetching}>
          <Icon icon="mdi:refresh" />
        </ActionIcon>
      </div>

      <ScrollArea h={250}>
        <Text size="xs">{task.data?.content}</Text>
      </ScrollArea>

      <Divider className="my-4" />
    </Card>
  );
};

export default TaskStatus;
