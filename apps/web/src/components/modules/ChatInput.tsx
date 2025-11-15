import React from 'react';
import { Controller, useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { Icon } from '@iconify/react';
import { ActionIcon, Textarea } from '@mantine/core';
import * as yup from 'yup';

import { cn } from '@/lib/utils';

import { ShineBorder } from '../ui/shine-border';

interface ChatInputProps {
  className?: string;
  onSubmit?: (message: string) => void;
  disabled?: boolean;
  isStreaming?: boolean;
  placeholder?: string;
}

const schema = yup.object({
  message: yup.string().required('Required'),
});

const ChatInput: React.FC<ChatInputProps> = ({
  className,
  onSubmit,
  disabled,
  isStreaming,
  placeholder,
}) => {
  const form = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      message: '',
    },
  });

  const handleSubmit = form.handleSubmit((data) => {
    form.reset();
    onSubmit?.(data.message);
  });

  const handleKeyDown = async (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      await handleSubmit();
    }
  };

  return (
    <form
      className={cn(
        className,
        'relative flex items-start gap-x-3 rounded-lg border bg-white p-4 dark:bg-slate-950'
      )}
      onSubmit={handleSubmit}>
      {isStreaming && (
        <ShineBorder borderWidth={2} shineColor={['#A07CFE', '#FE8FB5', '#FFBE7B']} />
      )}

      <Controller
        control={form.control}
        name="message"
        render={({ field, fieldState }) => (
          <Textarea
            className="flex-1"
            error={fieldState.error?.message}
            autosize
            minRows={2}
            maxRows={6}
            {...field}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            placeholder={placeholder}
          />
        )}
      />

      <ActionIcon size="xl" type="submit" disabled={disabled}>
        <Icon icon="mdi:send" className="text-2xl" />
      </ActionIcon>
    </form>
  );
};

export default ChatInput;
