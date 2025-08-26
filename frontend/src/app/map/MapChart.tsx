'use client';

import React, { useState, useEffect, memo } from "react";
import {
  ComposableMap,
  Geographies,
  Geography
} from "@mdworld/react-simple-maps";
import { Dialog } from '@headlessui/react'

import DetailedCounty from "./DetailedCounty"

const geoUrl = "https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json";

interface MapChartProps {
  setTooltipContent: React.Dispatch<React.SetStateAction<string>>;
}

export interface CountyData {
  countyName: string;
  fips: string
}

const MapChart = (props : MapChartProps) => {

  const closeDialog = () => {
    setIsDetailedCountyOpen(false)
  }

  const [isDeailedCountyOpen, setIsDetailedCountyOpen] = useState(false)
  const [countyData, setCountyData] = useState<CountyData>({
    countyName: "",
    fips: ""
  })

  useEffect(() => {  }, []);

  return (
    <>
      <div>
        <Dialog open={isDeailedCountyOpen} as="div" className="relative z-10 focus:outline-none" onClose={closeDialog} __demoMode>
          <DetailedCounty setIsDetailedCountyOpen={setIsDetailedCountyOpen} detailedCountyData={countyData} ></DetailedCounty>
        </Dialog>
      </div>
      <div className="my-anchor-element">
        <ComposableMap projection="geoAlbersUsa">
            <Geographies geography={geoUrl}>
              {({ geographies }) =>
                geographies.map((geo) => {
                  let countyName = geo.properties.name;
                  return (
                    <Geography
                      id={geo.properties.name}
                      key={geo.rsmKey}
                      geography={geo}
                      onMouseEnter={() => {
                        props.setTooltipContent(countyName);
                        setCountyData({"countyName": countyName, "fips": geo.id})
                      }}
                      onMouseOut={() => {
                        props.setTooltipContent("")
                      }}
                      onClick={() => {
                        setIsDetailedCountyOpen(true)
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
                  )
                })
              }
            </Geographies>
        </ComposableMap>
      </div>
    </>
  );
};

export default memo(MapChart);
