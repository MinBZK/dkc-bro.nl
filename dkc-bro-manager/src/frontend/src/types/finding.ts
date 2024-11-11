export type FindingOverview = {
  document: string;
  result: Result;
  rule: string;
  importance: number;
  error: null | string;
};

export type Result = {
  feedback_message: string | null;
  passed: boolean;
};

export interface GroupedFindings {
  [document: string]: FindingOverview[];
};

export type Finding = {
  result: boolean;
  feedbackMessage: string | null;
  ruleId: string;
  objectType: string;
};
