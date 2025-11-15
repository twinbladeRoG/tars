/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-unsafe-member-access */
/* eslint-disable @typescript-eslint/no-floating-promises */

/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import { useCallback, useEffect, useMemo } from 'react';
import { Button, useMantineColorScheme } from '@mantine/core';
import {
  Background,
  Controls,
  type Edge,
  Handle,
  type Node,
  Panel,
  Position,
  ReactFlow,
  useEdgesState,
  useNodesState,
  useReactFlow,
} from '@xyflow/react';
import ELK, { type ElkNode } from 'elkjs/lib/elk.bundled.js';

import { cn } from '@/lib/utils';
import type { IAgentWorkflow } from '@/types/entities';

import '@xyflow/react/dist/style.css';

const elk = new ELK();

const defaultOptions = {
  'elk.algorithm': 'org.eclipse.elk.mrtree',
  'elk.layered.spacing.nodeNodeBetweenLayers': 100,
  'elk.spacing.nodeNode': 80,
};

const useLayoutedElements = () => {
  const { getNodes, setNodes, getEdges, fitView } = useReactFlow();

  const getLayoutedElements = useCallback(
    (options: ElkNode['layoutOptions']) => {
      const layoutOptions = { ...defaultOptions, ...options };
      const graph = {
        id: 'root',
        layoutOptions: layoutOptions,
        children: getNodes().map((node) => ({
          ...node,
          width: node?.measured?.width,
          height: node?.measured?.height,
        })),
        edges: getEdges(),
      };

      elk.layout(graph as unknown as ElkNode).then(({ children }) => {
        // By mutating the children in-place we saves ourselves from creating a
        // needless copy of the nodes array.
        const nodes =
          children?.map((node) => ({
            ...node,
            position: { x: node.x, y: node.y },
          })) ?? [];

        setNodes(nodes as Node[]);

        fitView({ duration: 1000 });
      });
    },
    [getNodes, getEdges, fitView, setNodes]
  );

  return { getLayoutedElements };
};

interface AgentNodeProps {
  data: {
    label: string;
    isActive: boolean;
    isVisited?: boolean | null;
  };
}

const AgentNode: React.FC<AgentNodeProps> = ({ data }) => {
  const isStartNode = useMemo(() => data.label === '__start__', [data.label]);
  const isEndNode = useMemo(() => data.label === '__end__', [data.label]);

  return (
    <div
      className={cn('relative w-full rounded border bg-blue-700/20 px-3 py-2', {
        'bg-blue-400 dark:bg-blue-700': data.isVisited && !(isStartNode || isEndNode),
        'bg-teal-600/20': isStartNode,
        'bg-emerald-600/20': isEndNode,
        'bg-green-600': data.isVisited && (isStartNode || isEndNode),
        'animate-pulse bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600':
          data.isActive && isStartNode,
        'animate-pulse bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500':
          data.isActive && !isEndNode && !isStartNode,
        'flex size-10 items-center justify-center rounded-full border-0': isStartNode || isEndNode,
      })}>
      {!isStartNode && <Handle type="target" position={Position.Top} />}

      {!isStartNode && !isEndNode ? (
        <p
          className={cn('text-xs whitespace-nowrap', {
            'font-bold': data.isActive || data.isVisited,
          })}>
          {data.label}
        </p>
      ) : null}

      {isStartNode ? (
        <p
          className={cn('text-xs whitespace-nowrap', {
            'font-bold': data.isActive || data.isVisited,
          })}>
          start
        </p>
      ) : null}

      {isEndNode ? (
        <p
          className={cn('text-xs whitespace-nowrap', {
            'font-bold': data.isActive || data.isVisited,
          })}>
          end
        </p>
      ) : null}

      {!isEndNode && <Handle type="source" position={Position.Bottom} id="a" />}
    </div>
  );
};

const nodeTypes = {
  schema: AgentNode,
  runnable: AgentNode,
};

interface AgentGraphProps {
  graph: IAgentWorkflow['state'];
  visitedNodes?: string[];
}

const AgentGraph: React.FC<AgentGraphProps> = ({ graph, visitedNodes }) => {
  const { fitView } = useReactFlow();
  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);
  const { getLayoutedElements } = useLayoutedElements();
  const { colorScheme } = useMantineColorScheme();

  useEffect(() => {
    const newNodes = graph.nodes
      .map((node: any, index: number) => {
        switch (node.type) {
          case 'schema': {
            return {
              id: node.id,
              data: { label: node.data, isActive: false },
              position: { x: 0, y: 100 * index },
              type: 'schema',
            };
          }
          case 'runnable': {
            return {
              id: node.id,
              data: {
                label: node.data.name,
                isActive: false,
              },
              position: { x: 0, y: 100 * index },
              type: 'runnable',
            };
          }
          default:
            // !IMPORTANT: Signifies END node
            return {
              id: node.id,
              data: {
                label: node.id,
                isActive: false,
              },
              position: { x: 0, y: 100 * index },
              type: 'runnable',
            };
        }
      })
      .filter((node) => node !== null);

    const newEdges = graph.edges.map((edge) => ({
      id: `${edge.source}-${edge.target}`,
      source: edge.source,
      target: edge.target,
      animated: false,
    }));

    setNodes(newNodes);
    setEdges(newEdges);

    const timeout = setTimeout(() => {
      getLayoutedElements({
        'elk.algorithm': 'org.eclipse.elk.mrtree',
      });
    }, 200);

    return () => {
      clearTimeout(timeout);
    };
  }, [graph, fitView, setEdges, setNodes, getLayoutedElements]);

  useEffect(() => {
    if (visitedNodes) {
      setNodes((prev) => {
        return prev.map((node) => {
          return {
            ...node,
            data: {
              ...node.data,
              isActive: visitedNodes[visitedNodes.length - 1] === node.id,
              isVisited: visitedNodes.includes(node.id) ? true : !!node.data?.isVisited,
            },
          };
        });
      });
    }
  }, [visitedNodes, setNodes]);

  return (
    <div className="w-full flex-1">
      <ReactFlow
        colorMode={colorScheme === 'dark' ? 'dark' : 'light'}
        nodeTypes={nodeTypes}
        nodes={nodes}
        onNodesChange={onNodesChange}
        edges={edges}
        onEdgesChange={onEdgesChange}
        fitView>
        <Background />
        <Controls />

        <Panel position="top-right">
          <div className="flex gap-3">
            <Button
              size="compact-sm"
              onClick={() =>
                getLayoutedElements({
                  'elk.algorithm': 'layered',
                  'elk.direction': 'DOWN',
                })
              }>
              Vertical
            </Button>
            <Button
              size="compact-sm"
              onClick={() =>
                getLayoutedElements({
                  'elk.algorithm': 'layered',
                  'elk.direction': 'RIGHT',
                })
              }>
              Horizontal
            </Button>
            <Button
              size="compact-sm"
              onClick={() =>
                getLayoutedElements({
                  'elk.algorithm': 'org.eclipse.elk.mrtree',
                })
              }>
              Tree
            </Button>
          </div>
        </Panel>
      </ReactFlow>
    </div>
  );
};

export default AgentGraph;
