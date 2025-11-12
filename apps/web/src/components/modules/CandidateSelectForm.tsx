import React from 'react';
import { Controller, useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { Button, Select } from '@mantine/core';
import * as yup from 'yup';

import { cn } from '@/lib/utils';
import type { ICandidate } from '@/types';

interface CandidateSelectFormProps {
  candidates?: Array<ICandidate>;
  className?: string;
  onSubmit?: (candidateId: string) => void;
  isStreaming?: boolean;
}

const schema = yup.object({
  candidateId: yup.string().required('Required'),
});

const CandidateSelectForm: React.FC<CandidateSelectFormProps> = ({
  candidates,
  className,
  onSubmit,
  isStreaming = false,
}) => {
  const form = useForm({
    resolver: yupResolver(schema),
    defaultValues: { candidateId: undefined },
  });

  const handleSubmit = form.handleSubmit((data) => {
    onSubmit?.(data.candidateId);
  });

  if (isStreaming) return null;
  if (candidates && candidates.length == 0) return null;

  return (
    <form
      className={cn(className, 'flex gap-3 rounded-lg bg-gray-300 p-4 dark:bg-gray-600')}
      onSubmit={handleSubmit}>
      <Controller
        control={form.control}
        name="candidateId"
        render={({ field, fieldState }) => (
          <Select
            className="flex-1"
            data={candidates?.map((c) => ({ label: c.name, value: c.id }))}
            placeholder="Select Candidate"
            value={field.value}
            onChange={field.onChange}
            error={fieldState.error?.message}
          />
        )}
      />

      <Button className="shrink" type="submit">
        Select
      </Button>
    </form>
  );
};

export default CandidateSelectForm;
