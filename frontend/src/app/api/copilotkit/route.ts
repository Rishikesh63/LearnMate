import { NextRequest } from "next/server";
import {
  CopilotRuntime,
  GoogleGenerativeAIAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { ChatGoogleGenerativeAI } from "@langchain/google-genai";

// Initialize Gemini (Google Generative AI)
const gemini = new ChatGoogleGenerativeAI({
  model: "gemini-1.5-flash",
  temperature: 0,
  maxRetries: 2,
});

const serviceAdapter = new GoogleGenerativeAIAdapter(gemini);

const remoteEndpointURL = process.env.REMOTE_ACTION_URL || "http://localhost:8000/copilotkit";

const runtime = new CopilotRuntime({
  remoteEndpoints: [
    {
      url: remoteEndpointURL,
    },
  ],
});

export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};