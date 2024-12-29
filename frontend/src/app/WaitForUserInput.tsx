"use client";

import { useCopilotAction } from "@copilotkit/react-core";
import { CopilotPopup } from "@copilotkit/react-ui";
import { useState } from "react";

export function WaitForUserInput() {
  const [isPopupOpen, setIsPopupOpen] = useState(false);

  // Use Copilot action for learning assistance (e.g., topic scheduling or feedback)
  useCopilotAction({
    name: "StudyPlanAssistant", // Action related to study planning
    available: "remote", // Ensure the action is available remotely
    parameters: [
      {
        name: "query", // You can customize the query depending on your use case
        description: "User's study plan query or request for advice",
        type: "string",
        required: true,
      },
    ],
    handler: async ({ query }) => {
      // Use backend (LangGraph agent) to process the query
      const response = await fetch("http://127.0.0.1:8000", {  // Replace with your backend URL
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error('Error processing your query.');
      }

      const data = await response.json();
      return data.result || "No result found for the given query.";
    },
    render: ({ status, result }) => {
      if (status === 'executing' || status === 'inProgress') {
        // Show loading view while action is executing
        return <div>Loading...</div>;
      } else if (status === 'complete') {
        // Show result once the action is complete (Study Plan, Tips, etc.)
        return <div className="p-4 bg-teal-100 text-teal-700 rounded-lg shadow-md">{result}</div>;
      } else {
        return <div className="text-red-500">No information available for the given query.</div>;
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
          defaultOpen={true} 
          clickOutsideToClose={false} 
          className="rounded-lg shadow-lg border border-teal-500 animate-scale-in"
        />
      )}

      <button 
        className="mt-6 px-6 py-3 bg-teal-700 hover:bg-teal-600 focus:ring-4 focus:ring-teal-400 focus:outline-none transition-all duration-300 rounded-full font-semibold shadow-md text-white"
        onClick={() => setIsPopupOpen(true)}
      >
        Start Planning
      </button>
    </div>
  );
}
