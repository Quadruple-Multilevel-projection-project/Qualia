# Qualia

Portable blueprint for the "Chok Gvul HaYam" engine. This repo ships a semantic dictionary, a dual-cluster Docker deployment, and a Python integration script.

## Repository Contents

- `dictionary.json`: Portable ontology dictionary mapped to the 26-node cubic X geometry.
- `docker-compose.yml`: Spins up 8 dual servers (Logic + Quantum) plus the singularity hub.
- `integration.py`: Integrates the dictionary with the dual-cluster infrastructure.

## Quick Start

### 1) Prepare the dictionary

The dictionary is already checked in as `dictionary.json`. If you need to customize it, edit the file directly.

### 2) Start the 8-node dual cluster

```bash
docker compose up -d
```

This will start:

- 4 Logic servers (`amne-kernel:latest`)
- 4 Quantum servers (`amne-quantum-sim:latest`)
- 1 hub (`amne-hub:latest`) exposed on `http://localhost:3000`

### 3) Run the integration script

```bash
python integration.py
```

Example output:

```text
Loading Dictionary Configuration...
Understanding_ID_123456789
```

## First-Time Setup Notes

- Ensure Docker Engine (or Docker Desktop) is installed and running.
- If `docker compose` is not available, use `docker-compose` with the same arguments.
- The container images must exist locally or be available in your registry.
- The hub depends on the four Logic servers; it will wait until they are reachable.

## Troubleshooting

- **Images not found:** confirm the `amne-kernel`, `amne-quantum-sim`, and `amne-hub` images are present in your registry.
- **Port already in use:** change `3000:3000` in `docker-compose.yml` to another host port.
- **Dictionary changes not reflected:** re-run the integration script after editing `dictionary.json`.

## License

See `LICENSE`.
