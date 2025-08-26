'use client';

import React, { useState } from "react";
import { Tooltip } from 'react-tooltip'
import MapChart from "./components/MapChart";

export default function Home() {

  const [tooltipContent, setTooltipContent] = useState("");

  return (
    <div>
      <Tooltip anchorSelect=".my-anchor-element" clickable float>
        {tooltipContent}
      </Tooltip>
      <MapChart setTooltipContent={setTooltipContent} />
    </div>
  );
}
