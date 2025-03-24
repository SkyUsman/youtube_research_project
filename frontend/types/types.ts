export type RadioOption = "yes" | "no" | "skip" | null;
export type Status = "idle" | "started" | "done";

export type CommentResponse = {
  id: number;
  comment: string;
};

export type SurveyResponse = {
  id: number;
  response: RadioOption;
};
