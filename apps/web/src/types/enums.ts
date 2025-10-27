export type ObjectValues<T> = T[keyof T];

export const EXTRACTION_STATUS = {
  FAILURE: 'FAILURE',
  PENDING: 'PENDING',
  RECEIVED: 'RECEIVED',
  RETRY: 'RETRY',
  REVOKED: 'REVOKED',
  STARTED: 'STARTED',
  SUCCESS: 'SUCCESS',
} as const;

export type ExtractionStatus = ObjectValues<typeof EXTRACTION_STATUS>;
