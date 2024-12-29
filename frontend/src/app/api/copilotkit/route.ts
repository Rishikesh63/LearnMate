import { NextApiRequest, NextApiResponse } from "next";
import { CopilotKitSDK, LangGraphAgent } from "copilotkit";
import { loadEnvConfig } from "@next/env";
import { graph } from "../../my_agent/agent"; // Import your graph from agent.js or agent.py

// Load environment variables
loadEnvConfig(process.cwd());

const sdk = new CopilotKitSDK({
  agents: [
    new LangGraphAgent({
      name: "study_plan_assistant",
      description: "An assistant that helps users create, modify, and review study plans based on preferences.",
      graph: graph, // Graph from agent.py or agent.js
    }),
  ],
});

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    // Handle different HTTP methods
    if (req.method === "POST") {
      // Example: Handle a POST request to interact with the agent
      const { query } = req.body; // Assuming the request body contains a query

      // Interact with LangGraph agent
      const response = await sdk.query(query);

      res.status(200).json(response);
    } else {
      res.status(405).json({ message: "Method Not Allowed" });
    }
  } catch (error) {
    console.error("Error processing request:", error);
    res.status(500).json({ message: "Internal Server Error" });
  }
}
