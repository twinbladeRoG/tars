export interface IAgentWorkflowEdge {
  source: string;
  target: string;
}

export interface IAgentWorkflowSchemaNode {
  id: string;
  type: 'schema';
  data: string;
}

export interface IAgentWorkflowRunnableNode {
  id: string;
  type: 'runnable';
  data: {
    id: string[];
    name: string;
  };
}

export type IAgentWorkflowNode = IAgentWorkflowSchemaNode | IAgentWorkflowRunnableNode;

export interface IAgentWorkflow {
  mermaid: string;
  state: {
    nodes: Array<IAgentWorkflowNode>;
    edges: Array<IAgentWorkflowEdge>;
  };
}
