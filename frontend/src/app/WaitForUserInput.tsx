"use client";

import { useCopilotAction } from "@copilotkit/react-core";
import { CopilotPopup } from "@copilotkit/react-ui";
import { useState } from "react";

export function WaitForUserInput() {
  const [isPopupOpen, setIsPopupOpen] = useState(false);

  const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000";

  useCopilotAction({
    name: "study_plan_assistant",
    available: "remote",
    parameters: [
      {
        name: "query",
        description: "User's study plan query or request for advice",
        type: "string",
        required: true,
      },
    ],
    handler: async ({ query }) => {
      try {
        const response = await fetch(BACKEND_URL, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ query }),
        });

        if (!response.ok) {
          const errorDetails = await response.text();
          throw new Error(`Error: ${response.status} - ${errorDetails}`);
        }

        const data = await response.json();
        return data.result || "No result found for the given query.";
      } catch (error) {
        return `An error occurred: ${error.message}`;
      }
    },
    render: ({ status, result }) => {
      switch (status) {
        case "executing":
        case "inProgress":
          return <div>Loading your study plan...</div>;
        case "complete":
          return (
            <div className="p-4 bg-teal-100 text-teal-700 rounded-lg shadow-md">
              {result || "Your study plan is ready!"}
            </div>
          );
        case "error":
          return <div className="text-red-500">An error occurred while processing your request.</div>;
        default:
          return <div className="text-gray-500">Awaiting your input...</div>;
      }
    },
  });

  return (
    <div className="flex flex-col items-center justify-center min-h-screen w-screen bg-gradient-to-br from-blue-600 to-teal-700 text-black">
      <div className="text-4xl font-extrabold mb-4 animate-fade-in text-white">
        Study Plan Assistant
      </div>

      <div className="text-lg text-gray-200 max-w-lg text-center mb-6">
        Use this tool to organize your study schedule, get advice on the best study methods, 
        or get personalized learning tips. Let's build your path to success!
      </div>

      {isPopupOpen && (
        <CopilotPopup 
          defaultOpen 
          clickOutsideToClose={false} 
          className="rounded-lg shadow-lg border border-teal-500 animate-scale-in"
        />
      )}

      <button 
        aria-label="Start planning your study schedule"
        className="mt-6 px-6 py-3 bg-teal-700 hover:bg-teal-600 focus:ring-4 focus:ring-teal-400 focus:outline-none transition-all duration-300 rounded-full font-semibold shadow-md text-white"
        onClick={() => setIsPopupOpen(true)}
      >
        Start Planning
      </button>
    </div>
  );
}
