import { useState, memo, useEffect } from 'react'

import { CountyResult } from "./DetailedCounty";

interface DetailedElectionResultProps {
    electionResult: CountyResult
}

const D = "D"
const R = "R"

const DetailedElectionResult = (props : DetailedElectionResultProps) => {

    const [winner, setWinner] = useState(""); 

    useEffect(() => { 
        props.electionResult.raw_votes_D > props.electionResult.raw_votes_R
        ? setWinner(D)
        : setWinner(R)
    }, []);

    const highlightWinner = (party: string) => {
        return winner == party ? 'yellow': 'none' 
    }

    console.log(props.electionResult)

    return (
        <li key={props.electionResult.county+"_"+props.electionResult.year+"_"+props.electionResult.election} style={{ color: 'green', fontWeight: 'bold' }}>
            {props.electionResult.year} {" "} 
            <div style={{ color: 'blue', fontWeight: 'bold', backgroundColor: highlightWinner(D) }}> {props.electionResult.d_candidate} {" "} {props.electionResult.raw_votes_D}
            </div>
            <div style={{ color: 'red', fontWeight: 'bold', backgroundColor: highlightWinner(R) }}>
                {props.electionResult.r_candidate} {" "} {props.electionResult.raw_votes_R}
            </div>
        </li>
    )
}

export default memo(DetailedElectionResult);
