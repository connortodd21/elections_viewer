export interface StateResult {
  year: string;
  election: string;
  state: string;
  raw_votes_D: string;
  raw_votes_R: string;
  d_candidate: string;
  r_candidate: string;
}

// Empty template object
export const emptyStateResult: StateResult = {
  year: "",
  election: "",
  state: "",
  raw_votes_D: "",
  raw_votes_R: "",
  d_candidate: "",
  r_candidate: "",
};