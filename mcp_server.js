import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import axios from "axios";
import express from "express";

const app = express();
app.use(express.json());

const server = new Server(
  {
    name: "amne-deployment-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {
        analyze_proposition: {
          description: "מנתח היגדים דרך שבע שכבות אבולעפיה",
          inputSchema: {
            type: "object",
            properties: { text: { type: "string" } },
            required: ["text"],
          },
        },
      },
    },
  }
);

const kernelUrl = process.env.KERNEL_URL || "http://localhost:5000";

async function callPythonKernel(text) {
  try {
    const response = await axios.post(`${kernelUrl}/analyze`, { text });
    return response.data;
  } catch (error) {
    return { error: "Disconnected from Active Intellect (Python Kernel)" };
  }
}

app.post("/message", async (req, res) => {
  console.log("AMNE Filter: Processing inbound message...");

  const userText = req.body.text ?? "";
  const analysis = await callPythonKernel(userText);

  if (analysis.status === "INVALID_PALACE") {
    console.log("REJECTED: הארמון מכוער - דחיית פירוש לא מדויק.");
    res.status(400).send({ error: "Insufficient Midot for processing" });
    return;
  }

  if (analysis.error) {
    res.status(502).send({ error: analysis.error });
    return;
  }

  console.log("ACCEPTED: שכל פועל מאושר.");
  res.json({
    status: "Prophecy_Aligned",
    analysis,
  });
});

app.get("/sse", async (_req, res) => {
  const transport = new SSEServerTransport("/message", res);
  await server.connect(transport);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`[AMNE-ARCHITECTON] MCP Gateway running on port ${PORT}`);
  console.log(`Linked to Python Kernel on port ${kernelUrl}.`);
});
