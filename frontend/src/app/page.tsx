'use client';

import React, { useState } from "react";
import { Tooltip } from 'react-tooltip'
import MapChart from "./map/MapChart";

export default function Home() {

  const [tooltipContent, setTooltipContent] = useState("");

  return (
    <div>
      <Tooltip anchorSelect=".my-anchor-element" place="top">
        {tooltipContent}
      </Tooltip>
      <a className="my-anchor-element">
        <MapChart setTooltipContent={setTooltipContent}/>
      </a>
    </div>
  );
}
