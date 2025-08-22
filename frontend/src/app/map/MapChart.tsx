'use client';

import React, { useState, useEffect } from "react";
import {
  ComposableMap,
  Geographies,
  Geography
} from "@mdworld/react-simple-maps";
import { scaleLinear } from "d3-scale";
import { csv } from "d3-fetch";
import type { DSVRowString } from 'd3-dsv';

const geoUrl = "https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json";

  /**
   * 
  {
    "type":"Polygon",
    "arcs":[[1614,1615,1616,1617,1618,1619]],
    "id":"26161",
    "properties":{
      "name":"Washtenaw"
    } 
  },
   */


interface MapChartProps {
  setTooltipContent: React.Dispatch<React.SetStateAction<string>>;
}

const MapChart = (props : MapChartProps) => {

  const [county_results, setCountyResults] = useState<DSVRowString<string>[]>([]); 
  const [counties_by_state, setCountiesByState] = useState([])
  const [county_data, setCountyData] = useState([])

  const getCountyData = async(county: string) => {
    console.log("data from server")
    const response = await fetch(`http://localhost:5000/api/get_election_results_for_county/` + county)
    setCountyResults(await response.json())
  }
  

  useEffect(() => {  }, []);

  return (
    <div data-tip="">
      <ComposableMap projection="geoAlbersUsa">
          <Geographies geography={geoUrl}>
            {({ geographies }) =>
              geographies.map((geo) => (
                <Geography
                  key={geo.rsmKey}
                  geography={geo}
                  onMouseEnter={() => {
                    props.setTooltipContent(geo.properties.name);
                    getCountyData(geo.properties.name)
                  }}
                  style={{
                    default: {
                      fill: "#D6D6DA",
                      outline: "none"
                    },
                    hover: {
                      fill: "#F53",
                      outline: "none"
                    },
                    pressed: {
                      fill: "#E42",
                      outline: "none"
                    }
                  }}
                />
              ))
            }
          </Geographies>
      </ComposableMap>
    </div>
  );
};

export default MapChart;
