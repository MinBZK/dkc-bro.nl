export type FindingOverview = {
  filename: string;
  findings: Finding[];
};

export type Finding = {
  result: boolean;
  feedbackMessage: string;
  ruleId: string;
  objectType: string;
};
