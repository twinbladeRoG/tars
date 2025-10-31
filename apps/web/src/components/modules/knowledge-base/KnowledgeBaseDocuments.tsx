'use no memo'; // !HOTFIX for TanStack Table with React Compiler - https://github.com/TanStack/table/issues/5567#issuecomment-2442997182

import { useMemo, useState } from 'react';
import { Link } from 'react-router';
import { Icon } from '@iconify/react';
import { ActionIcon, Anchor, Badge, Card, Checkbox, Skeleton, Table, Title } from '@mantine/core';
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  type RowSelectionState,
  useReactTable,
} from '@tanstack/react-table';
import dayjs from 'dayjs';

import { useKnowledgeBases } from '@/apis/queries/knowledge-base.queries';
import { getExtractionStatusColor, getFileIcon } from '@/lib/utils';
import type { IKnowledgeBaseDocumentWithFile } from '@/types';

import KnowledgeBaseActions from './KnowledgeBaseActions';

const columnHelper = createColumnHelper<IKnowledgeBaseDocumentWithFile>();

const KnowledgeBaseDocuments = () => {
  const knowledgeBases = useKnowledgeBases();
  const [rowSelection, setRowSelection] = useState<RowSelectionState>({});

  const columns = useMemo(
    () => [
      columnHelper.accessor('id', {
        header: ({ table }) => (
          <Checkbox
            checked={table.getIsAllRowsSelected()}
            indeterminate={table.getIsSomeRowsSelected()}
            onChange={table.getToggleAllRowsSelectedHandler()}
          />
        ),
        cell: ({ row }) => (
          <Checkbox
            checked={row.getIsSelected()}
            disabled={!row.getCanSelect()}
            onChange={row.getToggleSelectedHandler()}
          />
        ),
      }),
      columnHelper.accessor('file', {
        header: 'File',
        cell: (info) => (
          <Anchor
            component={Link}
            to={`/extraction/${info.getValue().id}`}
            title={info.getValue().filename}>
            <div className="flex items-center gap-2">
              <Icon icon={getFileIcon(info.getValue().content_type)} className="text-2xl" />
              <span className="text-sm">{info.getValue().original_filename}</span>
            </div>
          </Anchor>
        ),
      }),
      columnHelper.accessor('status', {
        header: 'Size',
        cell: (info) => (
          <Badge color={getExtractionStatusColor(info.getValue())}>{info.getValue()}</Badge>
        ),
      }),
      columnHelper.accessor('created_at', {
        header: 'Uploaded On',
        cell: (info) => dayjs(info.getValue()).format('DD MMM YYYY'),
      }),
      columnHelper.display({
        id: 'actions',
        header: () => <p className="text-center">Actions</p>,
        cell: (info) => <KnowledgeBaseActions knowledgeBase={info.row.original} />,
      }),
    ],
    []
  );

  const data = useMemo(() => knowledgeBases.data ?? [], [knowledgeBases.data]);

  const table = useReactTable({
    data: data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    onRowSelectionChange: setRowSelection,
    state: {
      rowSelection,
    },
    getRowId: (row) => row.id,
  });

  return (
    <Card>
      <Card.Section withBorder inheritPadding py="xs">
        <div className="flex items-center justify-between">
          <Title order={5}>Knowledge Base</Title>

          <ActionIcon onClick={() => knowledgeBases.refetch()}>
            <Icon icon="mdi:refresh" />
          </ActionIcon>
        </div>
      </Card.Section>
      <Table>
        <Table.Thead>
          {table.getHeaderGroups().map((headerGroup) => (
            <Table.Tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <Table.Th key={header.id}>
                  {header.isPlaceholder
                    ? null
                    : flexRender(header.column.columnDef.header, header.getContext())}
                </Table.Th>
              ))}
            </Table.Tr>
          ))}
        </Table.Thead>

        <Table.Tbody>
          {knowledgeBases.isLoading ? (
            <>
              <Table.Tr>
                <Table.Td colSpan={columns.length}>
                  <Skeleton height={30} radius="sm" />
                </Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td colSpan={columns.length}>
                  <Skeleton height={30} radius="sm" />
                </Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td colSpan={columns.length}>
                  <Skeleton height={30} radius="sm" />
                </Table.Td>
              </Table.Tr>
            </>
          ) : null}

          {table.getRowModel().rows.length === 0 ? (
            <Table.Tr>
              <Table.Td colSpan={columns.length} align="center">
                No documents uploaded yet
              </Table.Td>
            </Table.Tr>
          ) : null}

          {table.getRowModel().rows.map((row) => (
            <Table.Tr key={row.id}>
              {row.getVisibleCells().map((cell) => (
                <Table.Td key={cell.id}>
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </Table.Td>
              ))}
            </Table.Tr>
          ))}
        </Table.Tbody>
      </Table>
    </Card>
  );
};

export default KnowledgeBaseDocuments;
