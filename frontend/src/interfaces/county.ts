export interface CountyResult {
  year: string;
  election: string;
  county: string;
  raw_votes_D: string;
  raw_votes_R: string;
  d_candidate: string;
  r_candidate: string;
}

// Empty template object
export const emptyCountyResult: CountyResult = {
  year: "",
  election: "",
  county: "",
  raw_votes_D: "",
  raw_votes_R: "",
  d_candidate: "",
  r_candidate: "",
};

export interface County {
    name: string,
    FIPS: string
}

export const emptyCounty: County = {
    name: "",
    FIPS: ""
}