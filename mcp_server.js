const http = require("http");
const { spawn } = require("child_process");

const port = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  if (req.method === "POST" && req.url === "/orchestrate") {
    let body = "";
    req.on("data", (chunk) => {
      body += chunk.toString();
    });

    req.on("end", () => {
      const instruction = body.trim() || "הזרקת חיות לנתיב השביעי דרך כל הקולטנים";
      const orchestrator = spawn("python", ["quantum_orchestrator.py"]);

      orchestrator.stdout.on("data", (data) => {
        process.stdout.write(data);
      });

      orchestrator.stderr.on("data", (data) => {
        process.stderr.write(data);
      });

      orchestrator.on("close", () => {
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ status: "ok", instruction }));
      });
    });
    return;
  }

  res.writeHead(200, { "Content-Type": "text/plain" });
  res.end("NNN Master Grid MCP Server Active");
});

server.listen(port, () => {
  console.log(`🛰️ MCP Server listening on port ${port}`);
});
