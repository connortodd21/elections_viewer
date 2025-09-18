'use client';

import React, { useState } from 'react';
import { ComposableMap, Geographies, Geography, ZoomableGroup } from '@mdworld/react-simple-maps';
import { Dialog } from '@headlessui/react';
import { geoCentroid } from 'd3-geo';
import DetailedCounty from '../election/DetailedCounty';
import { Tooltip } from 'react-tooltip';
import 'react-tooltip/dist/react-tooltip.css';
import DetailedState from '../election/DetailedState';
import { getSwingCounties } from '@/api/counties';
import { County } from '@/interfaces/county';

const STATES_URL = 'https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json';
const COUNTIES_URL = 'https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json';

const Map = () => {

    const [currentState, setCurrentState] = useState<string | null>(null);
    const [position, setPosition] = useState<{ coordinates: [number, number]; zoom: number }>({
        coordinates: [-97, 38], // US center
        zoom: 1.5,
    });
    const [mapKey, setMapKey] = useState(0); // force re-render for reset
    const [isDetailedCountyOpen, setIsDetailedCountyOpen] = useState(false);
    const [countyData, setCountyData] = useState<County>({ name: '', fips: '' });
    const [tooltipContent, setTooltipContent] = useState('');
    const [stateCentroids, setStateCentroids] = useState<Record<string, [number, number]>>({});
    const [currentStateName, setCurrentStateName] = useState<string | null>(null);
    const [showingSwing, setShowingSwing] = useState(false);
    const [swingCounties, setSwingCounties] = useState<County[]>([]);
    const [loadingSwing, setLoadingSwing] = useState(false);

    const handleStateClick = (geo: any) => {
        const centroid = geoCentroid(geo) as [number, number];
        setPosition({ coordinates: centroid, zoom: 3.5 });
        setCurrentState(geo.id);
        setCurrentStateName(geo.properties.name); 
        setStateCentroids((prev) => ({ ...prev, [geo.id]: centroid })); 
    };

    // Back to US (always clears state + resets zoom)
    const backToUS = () => {
        setPosition({ coordinates: [-97, 38], zoom: 1.5 });
        setCurrentState(null);
        setCurrentStateName(null);
        setShowingSwing(false)
        setSwingCounties([])
        setLoadingSwing(false)
        setMapKey((k) => k + 1);
    };

    // Recenter either recenter current state or US
    const recenter = () => {
        if (currentState) {
            setPosition({
                coordinates: stateCentroids[currentState] || [-97, 38],
                zoom: 3.5,
            });
        } else {
            setPosition({ coordinates: [-97, 38], zoom: 1.5 });
        }
        setMapKey((k) => k + 1);
    };


    const { refetch: refetchSwing } = getSwingCounties(currentStateName ?? '')

    const handleToggleSwing = async () => {
        if (!showingSwing && currentStateName) {
            setLoadingSwing(true);
            setShowingSwing(true);  
            if(swingCounties.length === 0) {
                try {
                    const result = await refetchSwing(); 
                    if (result.data) {
                        setSwingCounties(result.data);
                    }
                } catch (err) {
                    console.error('Failed to fetch swing counties', err);
                } finally {
                    setLoadingSwing(false);
                }
            }
            setLoadingSwing(false);
        } else {
            setShowingSwing(false);
        }
    };

    const closeDialog = () => setIsDetailedCountyOpen(false);

    return (
        <>
            {/* Detailed County Dialog */}
            <Dialog open={isDetailedCountyOpen} onClose={closeDialog} className="relative z-10">
                <div className="fixed inset-0 bg-black/30" />
                <div className="fixed inset-0 flex items-center justify-center p-4">
                    <DetailedCounty closeDialog={closeDialog} detailedCountyData={countyData} />
                </div>
            </Dialog>

            {/* Map Container */}
            <div
                className="my-anchor-element relative bg-gray-100 rounded-lg shadow-inner"
                style={{ width: '100%', height: 700 }}
            >
                {/* State label (only when zoomed into a state) */}
                {currentStateName && (
                    <div className="absolute top-2 left-1/2 transform -translate-x-1/2 z-10 bg-white/80 px-4 py-1 rounded-md shadow font-semibold text-gray-800">
                        {currentStateName}
                    </div>
                )}
                {/* Back button top-left, only show when we are viewing a state */}
                {currentState && (
                    <button
                        onClick={backToUS}
                        className="absolute top-2 left-2 z-10 rounded-lg bg-blue-600 px-3 py-1 text-white font-semibold shadow hover:bg-blue-700"
                    >
                        Back to US
                    </button>
                )}

                {/* Swing counties button */}
                {currentState && (
                    <button
                        onClick={handleToggleSwing}
                        className="absolute top-12 left-2 z-10 rounded-lg bg-[#6A0DAD] px-3 py-1 text-white font-semibold shadow hover:bg-[#7B1FA2]"
                        disabled={loadingSwing}
                    >
                        {showingSwing ? 'Clear Map' : 'Show Swing Counties'}
                    </button>
                )}

                {/* Always show bottom-right Recenter button */}
                <button
                    onClick={recenter}
                    className="absolute bottom-2 right-2 z-10 rounded-lg bg-gray-700 px-3 py-1 text-white font-semibold shadow hover:bg-gray-800"
                >
                    Re-center
                </button>

                <div className="relative flex w-full h-full">
                    <div className="flex-1 relative">
                        <ComposableMap
                            projection="geoAlbersUsa"
                            width={600}
                            height={900}
                            style={{ width: '100%', height: '100%' }}
                            preserveAspectRatio="xMidYMid meet"
                        >
                            <ZoomableGroup key={mapKey} center={position.coordinates} zoom={position.zoom}>
                                <Geographies geography={currentState ? COUNTIES_URL : STATES_URL}>
                                {({ geographies }) =>
                                    geographies.map((geo) => {
                                        if (currentState && geo.id.slice(0, 2) !== currentState) return null;
                                        const name = geo.properties.name;
                                        const isSwingCounty = showingSwing && swingCounties.some(c => c.fips === geo.id);

                                        return (
                                            <Geography
                                                key={geo.rsmKey}
                                                geography={geo}
                                                data-tooltip-id="county-tooltip"
                                                data-tooltip-content={name}
                                                onMouseEnter={() => {
                                                    setTooltipContent(name);
                                                    if (currentState) setCountyData({ name: name, fips: geo.id });
                                                }}
                                                onMouseOut={() => setTooltipContent('')}
                                                onClick={() => {
                                                    if (!currentState) handleStateClick(geo);
                                                    else setIsDetailedCountyOpen(true);
                                                }}
                                                style={{
                                                    default: { fill: isSwingCounty ? '#9370DB' : '#B0B0B0', stroke: '#555555', strokeWidth: 0.5, outline: 'none' },
                                                    hover: { fill: '#F53', stroke: '#666', strokeWidth: 0.7, outline: 'none' },
                                                    pressed: { fill: '#E42', stroke: '#444', strokeWidth: 0.7, outline: 'none' },
                                                }}
                                            />
                                        );
                                    })
                                }
                                </Geographies>
                            </ZoomableGroup>
                        </ComposableMap>
                    </div>
                    {/* State overall results  */}
                    {currentStateName && (
                        <div className="absolute top-2 right-2">
                            <DetailedState stateName={currentStateName} />
                        </div>
                    )}
                </div>
            </div>

            {/* Tooltip */}
            <Tooltip
                id="county-tooltip"
                anchorSelect=".my-anchor-element [data-tooltip-id='county-tooltip']"
                clickable
                float
            >
                {tooltipContent}
            </Tooltip>
        </>
    );
};

export default Map;
