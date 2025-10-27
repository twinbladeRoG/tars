import { Controller, useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { Button, Card, Text } from '@mantine/core';
import { type FileWithPath, MIME_TYPES } from '@mantine/dropzone';
import { notifications } from '@mantine/notifications';
import * as yup from 'yup';

import { useUploadFile } from '@/apis/queries/file-storage.queries';

import DropFileInput from '../shared/form/DropFileInput';

const ACCEPTED_FILE_TYPES: string[] = [
  MIME_TYPES.pdf,
  MIME_TYPES.docx,
  MIME_TYPES.csv,
  MIME_TYPES.xlsx,
];

const schema = yup.object({
  files: yup
    .array()
    .of(
      yup.mixed().test({
        test: (value) => {
          const file = value as FileWithPath;
          return ACCEPTED_FILE_TYPES.includes(file.type);
        },
        message: 'Only PDF and DOCX files are allowed',
        name: 'is-valid-file-type',
      })
    )
    .min(1, 'At least one file should be uploaded')
    .required('At least one file should be uploaded'),
});

const UploadForm = () => {
  const form = useForm<yup.InferType<typeof schema>>({
    resolver: yupResolver(schema),
    defaultValues: {
      files: [],
    },
  });

  const uploadFile = useUploadFile();

  const handleSubmit = form.handleSubmit((data) => {
    for (const file of data.files) {
      uploadFile.mutate(file as FileWithPath, {
        onSuccess: () => {
          form.reset();
        },
        onError: (err) => {
          notifications.show({
            color: 'red',
            message: err.message,
          });
        },
      });
    }
  });

  return (
    <Card mb="lg">
      <form onSubmit={handleSubmit}>
        <Controller
          control={form.control}
          name="files"
          render={({ field, fieldState }) => (
            <DropFileInput
              accept={ACCEPTED_FILE_TYPES}
              mb={'lg'}
              value={field.value as FileWithPath[]}
              onDrop={field.onChange}
              error={fieldState.error?.message}>
              <div>
                <Text size="xl" inline>
                  Upload files to Knowledge Base
                </Text>
                <Text size="sm" c="dimmed" inline mt={7}>
                  Only PDF and DOCX files are allowed.
                </Text>
              </div>
            </DropFileInput>
          )}
        />

        <Button fullWidth type="submit" loading={uploadFile.isPending}>
          Upload
        </Button>
      </form>
    </Card>
  );
};

export default UploadForm;
