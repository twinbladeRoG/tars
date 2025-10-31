'use no memo'; // !HOTFIX for TanStack Table with React Compiler - https://github.com/TanStack/table/issues/5567#issuecomment-2442997182

import { useMemo, useState } from 'react';
import { Link } from 'react-router';
import { Icon } from '@iconify/react';
import {
  Anchor,
  Card,
  Checkbox,
  Divider,
  Pagination,
  Select,
  Skeleton,
  Table,
} from '@mantine/core';
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  type PaginationState,
  type RowSelectionState,
  useReactTable,
} from '@tanstack/react-table';
import dayjs from 'dayjs';

import { useUserFiles } from '@/apis/queries/file-storage.queries';
import { bytesToSize, getFileIcon } from '@/lib/utils';
import type { IFile } from '@/types';

import UserDocumentAction from './UserDocumentAction';

const columnHelper = createColumnHelper<IFile>();

const UserDocuments = () => {
  const [pagination, setPagination] = useState<PaginationState>({
    pageIndex: 0,
    pageSize: 10,
  });
  const documents = useUserFiles(pagination.pageIndex, pagination.pageSize);

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
      columnHelper.accessor('filename', {
        header: 'File',
        cell: (info) => (
          <Anchor
            component={Link}
            to={`/extraction/${info.row.original.id}`}
            title={info.getValue()}>
            <div className="flex items-center gap-2">
              <Icon icon={getFileIcon(info.row.original.content_type)} className="text-2xl" />
              <span className="text-sm">{info.row.original.original_filename}</span>
            </div>
          </Anchor>
        ),
      }),
      columnHelper.accessor('content_length', {
        header: 'Size',
        cell: (info) => bytesToSize(info.getValue()),
      }),
      columnHelper.accessor('created_at', {
        header: 'Uploaded On',
        cell: (info) => dayjs(info.getValue()).format('DD MMM YYYY'),
      }),
      columnHelper.display({
        id: 'actions',
        header: () => <p className="text-center">Actions</p>,
        cell: (info) => <UserDocumentAction document={info.row.original} />,
      }),
    ],
    []
  );

  const data = useMemo(() => documents.data?.data ?? [], [documents.data]);

  const table = useReactTable({
    data: data,
    columns,
    rowCount: documents.data?.pagination.total_count ?? 0,
    getCoreRowModel: getCoreRowModel(),
    onRowSelectionChange: setRowSelection,
    state: {
      pagination,
      rowSelection,
    },
    onPaginationChange: setPagination,
    getRowId: (row) => row.id,
    manualPagination: true,
  });

  return (
    <Card>
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
          {documents.isLoading ? (
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

      <Divider mb="lg" />

      <div className="flex items-center gap-4">
        <Pagination
          size="xs"
          value={pagination.pageIndex + 1}
          onChange={(value) => table.setPageIndex(value - 1)}
          total={table.getPageCount()}
        />

        <Select
          size="xs"
          w={80}
          data={['5', '10', '20', '30', '40', '50']}
          value={String(pagination.pageSize)}
          onChange={(value) => {
            if (value) table.setPageSize(+value);
          }}
        />

        <span className="ml-auto flex items-center gap-1 text-xs">
          <div>Page</div>
          <strong>
            {table.getState().pagination.pageIndex + 1} of {table.getPageCount().toLocaleString()}
          </strong>
        </span>
      </div>
    </Card>
  );
};

export default UserDocuments;
