'use no memo'; // !HOTFIX for TanStack Table with React Compiler - https://github.com/TanStack/table/issues/5567#issuecomment-2442997182

import { Fragment, useMemo } from 'react';
import { Icon } from '@iconify/react';
import {
  ActionIcon,
  Anchor,
  Badge,
  Card,
  CopyButton,
  Divider,
  Skeleton,
  Table,
  Text,
  Title,
} from '@mantine/core';
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  getExpandedRowModel,
  useReactTable,
} from '@tanstack/react-table';
import dayjs from 'dayjs';

import { useCandidates } from '@/apis/queries/candidate.queries';
import { formatMonths } from '@/lib/utils';
import type { ICandidate } from '@/types';

const columnHelper = createColumnHelper<ICandidate>();

const CandidateTable = () => {
  const candidates = useCandidates();

  const columns = useMemo(
    () => [
      columnHelper.accessor('id', {
        header: ({ table }) => (
          <ActionIcon
            variant="light"
            color="green"
            {...{
              onClick: table.getToggleAllRowsExpandedHandler(),
            }}>
            {table.getIsAllRowsExpanded() ? (
              <Icon icon="mdi:chevron-down-circle" />
            ) : (
              <Icon icon="mdi:chevron-right-circle" />
            )}
          </ActionIcon>
        ),
        cell: ({ row }) => (
          <div
            style={{
              paddingLeft: `${(row.depth + 1) * 8}px`,
            }}>
            <div>
              {row.getCanExpand() ? (
                <ActionIcon
                  variant="subtle"
                  {...{
                    onClick: row.getToggleExpandedHandler(),
                    style: { cursor: 'pointer' },
                  }}>
                  {row.getIsExpanded() ? (
                    <Icon icon="mdi:chevron-down-circle" />
                  ) : (
                    <Icon icon="mdi:chevron-right-circle" />
                  )}
                </ActionIcon>
              ) : (
                '🔵'
              )}
            </div>
          </div>
        ),
      }),
      columnHelper.accessor('name', {
        header: 'Name',
        cell: (info) => <Text size="sm">{info.getValue()}</Text>,
      }),
      columnHelper.accessor('email', {
        header: 'Email',
        cell: (info) => (
          <div className="flex items-center">
            <Anchor size="sm" href={`mailto:${info.getValue()}`}>
              {info.getValue()}
            </Anchor>

            <CopyButton value={info.getValue()} timeout={2000}>
              {({ copied, copy }) => (
                <ActionIcon color={copied ? 'teal' : 'gray'} variant="subtle" onClick={copy}>
                  {copied ? <Icon icon="mdi:check-all" /> : <Icon icon="mdi:content-copy" />}
                </ActionIcon>
              )}
            </CopyButton>
          </div>
        ),
      }),
      columnHelper.accessor('contact', {
        header: 'Contact',
        cell: (info) => (
          <div className="flex items-center">
            <Anchor size="sm" href={`mailto:${info.getValue()}`}>
              {info.getValue()}
            </Anchor>

            {info.getValue() ? (
              <CopyButton value={info.getValue() ?? ''} timeout={2000}>
                {({ copied, copy }) => (
                  <ActionIcon color={copied ? 'teal' : 'gray'} variant="subtle" onClick={copy}>
                    {copied ? <Icon icon="mdi:check-all" /> : <Icon icon="mdi:content-copy" />}
                  </ActionIcon>
                )}
              </CopyButton>
            ) : null}
          </div>
        ),
      }),
      columnHelper.accessor('years_of_experience', {
        header: 'Experience',
        cell: (info) => <Text size="sm">{`${info.getValue()} years`}</Text>,
      }),
    ],
    []
  );

  const data = useMemo(() => candidates.data ?? [], [candidates.data]);

  const table = useReactTable({
    data: data,
    columns,
    getRowId: (row) => row.id,
    getRowCanExpand: (row) => !!row.id,
    getCoreRowModel: getCoreRowModel(),
    getExpandedRowModel: getExpandedRowModel(),
  });

  return (
    <Card>
      <Card.Section withBorder inheritPadding py="xs">
        <div className="flex items-center justify-between">
          <Title order={5}>Candidates</Title>

          <ActionIcon onClick={() => candidates.refetch()}>
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
          {candidates.isLoading ? (
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
            <Fragment key={row.id}>
              <Table.Tr key={row.id}>
                {row.getVisibleCells().map((cell) => (
                  <Table.Td key={cell.id}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </Table.Td>
                ))}
              </Table.Tr>

              {row.getIsExpanded() && (
                <Table.Tr>
                  <Table.Td colSpan={row.getVisibleCells().length}>
                    <Title order={6} mb="sm">
                      Skills
                    </Title>

                    <div className="flex flex-wrap items-center gap-2">
                      {row.original.skills.map((skill) => (
                        <Badge size="xs" radius="sm" key={skill}>
                          {skill}
                        </Badge>
                      ))}
                    </div>

                    {row.original.certifications.length > 0 ? (
                      <>
                        <Divider my="sm" />

                        <Title order={4}>Certifications</Title>

                        <ul className="flex list-disc flex-wrap items-center gap-2">
                          {row.original.certifications.map((cert) => (
                            <li className="text-sm" key={cert}>
                              {cert}
                            </li>
                          ))}
                        </ul>
                      </>
                    ) : null}

                    <Divider my="sm" />

                    <div className="mb-3 flex items-center gap-2">
                      <Title order={4}>Experience</Title>
                      <Badge size="xs">{row.original.years_of_experience} years</Badge>
                    </div>

                    <div className="flex flex-col gap-2">
                      {row.original.experiences.map((exp, index) => (
                        // eslint-disable-next-line @eslint-react/no-array-index-key, react-x/no-array-index-key
                        <Card bg="gray.9" radius="sm" key={index}>
                          <Title order={5}>{exp.role}</Title>
                          <Title order={6}>{exp.company}</Title>
                          <Text size="xs">
                            Start Date:{' '}
                            {exp.start_date ? dayjs(exp.start_date).format('DD MMM, YYYY') : 'N/A'}
                          </Text>
                          <Text size="xs">
                            End Date:{' '}
                            {exp.end_date ? dayjs(exp.end_date).format('DD MMM, YY') : 'N/A'}
                          </Text>
                          <Text size="xs" mb="xs">
                            Duration: {formatMonths(exp.months_in_experience ?? 0)}
                          </Text>
                          <div className="mb-2 flex flex-wrap items-center gap-2">
                            {exp.skills?.split(',').map((skill) => (
                              <Badge size="xs" radius="sm" key={skill}>
                                {skill}
                              </Badge>
                            ))}
                          </div>
                          <Text size="xs">{exp.additional_info}</Text>
                        </Card>
                      ))}
                    </div>

                    <Divider my="sm" />
                  </Table.Td>
                </Table.Tr>
              )}
            </Fragment>
          ))}
        </Table.Tbody>
      </Table>
    </Card>
  );
};

export default CandidateTable;
