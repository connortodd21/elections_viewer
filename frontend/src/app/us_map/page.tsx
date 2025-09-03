"use client"; 

import dynamic from "next/dynamic";
import ReactQueryProvider from "../../components/ReactQueryProvider";

const Map = dynamic(() => import("../../components/map/Map"), { ssr: false });

export default function USMapPage() {
  return (
    <ReactQueryProvider>
      <main className="flex min-h-screen flex-col items-center justify-center bg-gray-50 p-8">
        <h1 className="mb-6 text-3xl font-bold text-blue-700">US Interactive Map</h1>
        <Map />
      </main>
    </ReactQueryProvider>
  );
}
