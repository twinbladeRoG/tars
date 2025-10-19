import React from 'react';
import { Anchor, Code, Divider, Table, Title } from '@mantine/core';
import { ReactRenderer } from 'marked-react';

const renderer = {
  list(children: React.ReactNode, ordered: boolean) {
    if (ordered) return <ol className="my-2 list-inside list-decimal">{children}</ol>;
    return <ul className="my-2 list-inside list-disc">{children}</ul>;
  },
  code(code: React.ReactNode) {
    return (
      <Code block my="md">
        {code}
      </Code>
    );
  },
  table(children) {
    return (
      <div className="mb-4 max-w-[60dvw] overflow-x-auto">
        <Table withTableBorder withColumnBorders className="!w-full !max-w-[400px]">
          {children}
        </Table>
      </div>
    );
  },
  tableBody(children) {
    return <Table.Tbody>{children}</Table.Tbody>;
  },
  tableHeader(children) {
    return <Table.Thead>{children}</Table.Thead>;
  },
  tableRow(children) {
    return <Table.Tr>{children}</Table.Tr>;
  },
  tableCell(children) {
    return <Table.Td>{children}</Table.Td>;
  },
  heading(children, level) {
    return <Title order={level}>{children}</Title>;
  },
  link(href, text) {
    return (
      <Anchor href={href} target="_blank">
        {text}
      </Anchor>
    );
  },
  hr() {
    return <Divider my="lg" />;
  },
} satisfies Partial<ReactRenderer>;

export default renderer;
