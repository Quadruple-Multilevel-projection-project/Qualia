# Qualia
https://qnrfirstchpter.blogspot.com

## Ontological Compiler Services

This repository includes a dual-service setup that links a Python ontological kernel
with a Node.js MCP gateway.

### Services
- **Python kernel** (`ontological_kernel.py`): processes text through the seven-layer
  logic and returns a normalized prophetic vector.
- **Node gateway** (`mcp_server.js`): exposes a `/message` endpoint and relays requests
  to the kernel for validation.

### Run with Docker Compose

```bash
docker compose up --build
```

### Local Development

Python:

```bash
python ontological_kernel.py
```

Node:

```bash
npm install
npm start
```
