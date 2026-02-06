#!/usr/bin/env node
"use strict";

const http = require("http");

const args = new Set(process.argv.slice(2));
const isHealthCheck = args.has("--health-check");
const port = process.env.PORT ? Number(process.env.PORT) : 7070;

const server = http.createServer((req, res) => {
  if (req.url === "/health") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ status: "ok", protocol: "MCP", mode: "SSE" }));
    return;
  }

  res.writeHead(200, { "Content-Type": "text/plain" });
  res.end("MCP Server running.");
});

if (isHealthCheck) {
  server.listen(port, () => {
    http.get(`http://localhost:${port}/health`, (resp) => {
      resp.on("data", () => {});
      resp.on("end", () => {
        server.close();
      });
    });
  });
} else {
  server.listen(port, () => {
    console.log(`MCP server listening on ${port}`);
  });
}
