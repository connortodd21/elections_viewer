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

interface MapChartProps {
  setTooltipContent: React.Dispatch<React.SetStateAction<string>>;
}

const MapChart = (props : MapChartProps) => {

  const [county_results, setCounties] = useState<DSVRowString<string>[]>([]); 
  const [counties_by_state, setCountiesByState] = useState([])

  useEffect(() => {
    // https://www.bls.gov/lau/
    csv("/statewide_results.csv").then(county_results => {
      setCounties(county_results.map(county => county))
    });
  }, []);

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
