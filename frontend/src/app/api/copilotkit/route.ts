import { NextRequest } from "next/server";
import {
  CopilotRuntime,
  OpenAIAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import OpenAI from "openai";

// Check if copilotRuntimeNextJSAppRouterEndpoint is correctly imported
console.log(copilotRuntimeNextJSAppRouterEndpoint);

// Define the endpoint URL
const remoteEndpointURL =
  process.env.REMOTE_ACTION_URL || "http://localhost:8000/copilotkit";

// Initialize OpenAI client
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY, // Ensure this is set in your .env
});

// Create an OpenAI Adapter
const openAIAdapter = new OpenAIAdapter({ openai });

// Initialize CopilotRuntime with the adapter and remote endpoints
const copilotKit = new CopilotRuntime({
  agents: [openAIAdapter],
  remoteEndpoints: [
    {
      url: remoteEndpointURL,
    },
  ],
});

export const POST = async (req: NextRequest) => {
  // Check if copilotKit is properly initialized
  console.log(copilotKit);

  // Use copilotRuntimeNextJSAppRouterEndpoint to handle requests
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime: copilotKit,
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};
