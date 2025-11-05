import type { IBaseEntity } from './common';
import type { ExtractionStatus } from './enums';

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

export interface IUser extends IBaseEntity {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface IFile extends IBaseEntity {
  filename: string;
  content_type: string;
  content_length: number;
  original_filename: string;
  owner_id: string;
}

export interface ITaskStatus {
  task_id: string;
  state: ExtractionStatus;
  status: ExtractionStatus;
  result?: string | null;
  retries: number | null;
  completed_at?: string | null;
}

export interface IKnowledgeBaseDocument extends IBaseEntity {
  file_id: string;
  status?: ExtractionStatus | null;
  task_id?: string | null;
  content?: string | null;
}

export interface IKnowledgeBaseDocumentWithFile extends IKnowledgeBaseDocument {
  file: IFile;
}

export interface ICandidateExperience {
  months_in_experience?: number;
  company: string;
  start_date?: string;
  end_date?: string;
  skills?: string;
  role: string;
  additional_info?: string;
}

export interface ICandidate extends IBaseEntity {
  email: string;
  name: string;
  contact?: string;
  years_of_experience?: number;

  skills: Array<string>;
  experiences: Array<ICandidateExperience>;
  certifications: Array<string>;

  knowledge_base_document_id: string;
}

export interface ICandidateWithKnowledgeBase extends ICandidate {
  knowledge_base_document: IKnowledgeBaseDocument;
}

export interface ICandidateWithScore extends ICandidate {
  score: number;
}
