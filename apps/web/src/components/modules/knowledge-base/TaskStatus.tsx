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
import { getExtractionStatusColor } from '@/lib/utils';

interface TaskStatusProps {
  taskId: string;
  className?: string;
}

const TaskStatus: React.FC<TaskStatusProps> = ({ taskId, className }) => {
  const task = useTaskStatus(taskId);

  const extractionStatusColor = useMemo((): DefaultMantineColor => {
    return getExtractionStatusColor(task.data?.status);
  }, [task.data]);

  return (
    <Card className={className}>
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
