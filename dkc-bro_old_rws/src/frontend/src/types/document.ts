import { RuleFinding } from "@/types/rule_finding";

export type Document = {
  filename: string;
  findings: RuleFinding[];
  object_type: string;
  timestamp: string;
};
