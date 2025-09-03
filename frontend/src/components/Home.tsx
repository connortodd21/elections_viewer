"use client";

import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-50 p-8">
      <h1 className="mb-6 text-4xl font-bold text-blue-700">
        Welcome to Elections Viewer
      </h1>

      <button
        onClick={() => router.push("/us_map")}
        className="rounded-lg bg-blue-600 px-6 py-3 text-lg font-semibold text-white shadow hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400"
      >
        Go to US Map
      </button>

      <div className="mt-8 max-w-xl rounded-lg bg-yellow-100 p-4 text-center text-sm text-yellow-900 shadow">
        <p>
          <strong>Limitations of this project:</strong> <br />
          • Only covers the United States <br />
          • Only includes statewide elections <br />
          • Data is available only at the county level
        </p>
      </div>
    </main>
  );
}
