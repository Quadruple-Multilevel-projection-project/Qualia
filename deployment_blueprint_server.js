import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import express from "express";

const app = express();
const server = new Server(
  {
    name: "deployment-blueprint-server",
    version: "1.0.0",
  },
  {
    capabilities: { resources: {}, tools: {}, prompts: {} },
  }
);

// TODO: add GitHub API integration logic here.

app.get("/sse", async (req, res) => {
  const transport = new SSEServerTransport("/message", res);
  await server.connect(transport);
});

app.listen(3000, () => console.log("MCP Server running on port 3000"));
