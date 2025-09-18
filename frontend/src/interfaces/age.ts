export interface AgeGroupData {
  YEAR: number;
  FIPS: string;
  "20-24": number;
  "25-29": number;
  "30-34": number;
  "35-39": number;
  "40-44": number;
  "45-49": number;
  "50-54": number;
  "55-59": number;
  "60-64": number;
  "65-69": number;
  "70-74": number;
  "75-79": number;
  "80-84": number;
  "85+": number;
}

// Empty template
export const emptyAgeGroupPopulation: AgeGroupData = {
  YEAR: 0,
  FIPS: "",
  "20-24": 0,
  "25-29": 0,
  "30-34": 0,
  "35-39": 0,
  "40-44": 0,
  "45-49": 0,
  "50-54": 0,
  "55-59": 0,
  "60-64": 0,
  "65-69": 0,
  "70-74": 0,
  "75-79": 0,
  "80-84": 0,
  "85+": 0,
};
