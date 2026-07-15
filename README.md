# Quantum Knowledge Graph and 3D Reasoning Engine

This local web application is designed for quantum computing research, industry analysis, and knowledge-based forecasting. It brings together a quantum computing knowledge graph, a 3D research map, a 2D knowledge graph, multi-step reasoning, multi-agent simulation, IMA source references, and report export in a single interface.

Default endpoints:

- Local application: http://127.0.0.1:6122/quantum_reasoning.html
- Local API: http://127.0.0.1:6122/api
- Cloud deployment: http://8.153.83.178:6122

## Core Capabilities

### 1. 3D Quantum Research Map

- Visualizes the quantum computing knowledge graph in a 3D globe/vector-space layout.
- Includes node types such as concepts, hardware, algorithms, companies, people, institutions, materials, tools, reports, and quantum error correction (QEC) roadmaps.
- Supports satellite-style nodes around the globe for outer-layer entities such as companies, institutions, tools, people, and reports.
- Lets users select nodes to inspect sources, evidence chains, difficulty, and research evolution paths.
- Supports attack-path filtering. In this project, an "attack path" means a research evolution path, such as the progression from problem definition to an algorithmic breakthrough and then to hardware implementation.
- Supports Chinese and English node labels.
- Supports switching between 3D and 2D maps.

### 2. 2D Knowledge Graph

- The 2D mode embeds the original `quantum_knowledge_graph.html` page.
- The reasoning engine remains available in the right-hand panel in both 2D and 3D modes.
- This mode is useful for quickly finding entities and relationships in dense graph regions.

### 3. Knowledge Reasoning Engine

The reasoning panel on the right supports two modes.

Step-by-step reasoning:

- Parses the question and retrieves a relevant subgraph.
- Performs multi-step logical reasoning over the knowledge graph.
- Produces multidimensional analysis, predictions, confidence scores, supporting evidence, and uncertainty factors.
- Automatically lists relevant references after reasoning, including IMA articles, knowledge bases, related nodes, and chapter or content excerpts.

Multi-agent simulation:

- Dynamically selects relevant entities according to question complexity instead of always using a fixed set of six.
- Generates an agent persona for each relevant entity.
- Runs multiple discussion rounds, after which a coordinator summarizes consensus, disagreements, and the combined prediction.
- Produces a final forecast report, detailed simulation records, and relevant references.
- Uses a local fallback summary when the model does not return a summary for a round, such as round two.

### 4. IMA Sources and Evidence

Graph nodes read source information from metadata. The primary source collections include:

- Quantum Computing Learning Materials
- Quantum Industry Research Reports
- Professor Jin Yirong's Live Course Materials
- Quantum Computing
- Dr. Li's Projects

The post-reasoning reference list attempts to include:

- Document title
- Knowledge base
- Document count
- Related nodes
- Relevant chapters or content excerpts
- Original evidence and related topics

### 5. Report Export

The application supports the following export formats:

- HTML
- PDF
- Word `.docx`

Exported reports include:

- Question, mode, date, and graph size
- Step-by-step reasoning or multi-agent simulation process
- Prediction and confidence score
- Supporting evidence and key factors
- Relevant references
- Document chapters or content excerpts

The export pipeline removes Markdown markers such as `###`, `- **`, and `>` from model output so that reports read like formal research documents.

## Project Structure

```text
QuanKnowledeg/
|-- graph/
|   `-- graph_data.json                # Standalone graph data; only this directory is updated monthly in production
|-- graph_data.json                    # Legacy compatibility file; the service prefers graph/graph_data.json
|-- quantum_reasoning.html             # 3D research map and reasoning interface
|-- quantum_knowledge_graph.html       # Original 2D knowledge graph
|-- reasoning_server.py                # FastAPI backend, reasoning, simulation, and export APIs
|-- package.json                       # Local development scripts
|-- scripts/
|   |-- dev-server.js                  # Static server, API proxy, and backend startup checks
|   `-- update-graph-only.sh           # Production script that synchronizes only graph/
|-- expand_graph*.py                   # Graph expansion scripts
|-- generate_html*.py                  # Legacy HTML generation scripts
|-- server.log                         # Backend runtime log
`-- README.md
```

## Requirements

Recommended environment:

- macOS or Linux
- Node.js 18+
- Python 3.10+
- Access to local port `6122`

Primary Python dependencies:

- `fastapi`
- `uvicorn`
- `httpx`
- `pydantic`
- `python-docx`
- `reportlab`
- `weasyprint` is optional and preferred for PDF generation. When it is unavailable, the system automatically falls back to ReportLab.

Frontend dependencies:

- The page loads Three.js from a CDN.
- The local development server only requires Node.js's built-in `http` module.

## Environment Variables

The backend does not store API keys in the source code. Set the following environment variable before running a reasoning task:

```bash
export DEEPSEEK_API_KEY="your_deepseek_api_key"
```

You can inject this variable through your shell configuration, process manager, or local `.env` workflow. `.env` files are excluded from Git by default.

Alternatively, open **Model Settings** in the upper-right corner of the page and add your own LLM API instead of using the default DeepSeek environment variable. Built-in provider presets include:

- DeepSeek
- OpenAI
- Anthropic Claude
- Google Gemini
- Alibaba Cloud Qwen
- Moonshot Kimi
- Zhipu GLM
- Volcano Engine Doubao
- SiliconFlow
- OpenRouter
- Custom OpenAI-compatible endpoints

After enabling **Use my own LLM API for reasoning**, you must select **Test Model** and pass the connection test before the page allows that model to run step-by-step reasoning or multi-agent simulation. The API key is stored only in the current browser's `localStorage`; it is never written to project files or committed to Git.

## Quick Start

Run the following command from the project root:

```bash
npm run dev
```

By default, the script:

1. Checks whether the current project is already serving `http://127.0.0.1:6122/api/health`.
2. Starts `python3 reasoning_server.py` when no service is running.
3. Serves the frontend, static graph files, and `/api/*` endpoints from port `6122`.

Open:

```text
http://127.0.0.1:6122/quantum_reasoning.html
```

## Start the Backend Manually

To start only the unified service:

```bash
python3 reasoning_server.py
```

Health check:

```bash
curl http://127.0.0.1:6122/api/health
```

Example response:

```json
{
  "status": "ok",
  "base_dir": "/Users/avalok/work/QuanKnowledeg",
  "graph_loaded": true,
  "node_count": 385,
  "edge_count": 1223
}
```

## Alibaba Cloud Deployment

If the server exposes only port `6122`, configure FastAPI to listen on `0.0.0.0:6122`:

```bash
HOST=0.0.0.0 PORT=6122 python3 reasoning_server.py
```

You can also use the project script:

```bash
HOST=0.0.0.0 PORT=6122 npm run dev
```

After allowing inbound TCP traffic on port `6122` in the Alibaba Cloud security group, access the application at:

```text
http://8.153.83.178:6122
```

The root path `/` serves the main page. `/quantum_reasoning.html`, `/quantum_knowledge_graph.html`, `/graph_data.json`, and `/api/*` are all available through the same port. `/graph_data.json` remains available for legacy links, while the service prefers the data in `graph/graph_data.json`.

## Monthly Graph-Only Updates

Monthly graph updates do not require replacing the page code, service code, or model API keys stored in users' browsers. The production service prefers the standalone graph file:

```text
graph/graph_data.json
```

Whenever a graph-related endpoint is requested, the backend checks this file's modification time. If the file has changed, the service automatically reloads it and rebuilds the node, edge, adjacency, and label indexes without restarting `reasoning_server.py`.

After generating a new graph locally, commit `graph/graph_data.json` to GitHub:

```bash
git add graph/graph_data.json
git commit -m "Update graph data"
git push
```

From the project directory on an Alibaba Cloud ECS instance, synchronize only the `graph/` directory from GitHub:

```bash
cd /path/to/QuanKnowledeg
./scripts/update-graph-only.sh
```

If the default GitHub branch is not `main`, or the project directory is different, specify the values explicitly:

```bash
BRANCH=master ./scripts/update-graph-only.sh /path/to/QuanKnowledeg/graph
```

Confirm that the service has loaded the updated graph:

```bash
curl http://127.0.0.1:6122/api/health
```

Inspect `graph_path`, `node_count`, `edge_count`, and `graph_load_error` in the response. Under normal conditions, `graph_path` points to `graph/graph_data.json` and `graph_load_error` is `null`.

## API Reference

### Health Check

```http
GET /api/health
```

### Graph Statistics

```http
GET /api/stats
```

### Full Graph

```http
GET /api/graph/full
```

Parameters:

- `limit_nodes`: defaults to 500
- `limit_edges`: defaults to 2000

### Retrieve a Relevant Subgraph

```http
POST /api/subgraph
```

Example request:

```json
{
  "question": "When will quantum error correction achieve a major breakthrough?",
  "max_nodes": 80
}
```

### Step-by-Step Reasoning

```http
POST /api/reason
```

Returns a Server-Sent Events stream.

Example request:

```json
{
  "question": "Can superconducting quantum computing achieve fault tolerance?",
  "mode": "reasoning",
  "max_nodes": 80,
  "lang": "en",
  "model_config": {
    "provider": "openai",
    "api_kind": "openai",
    "model": "gpt-4.1",
    "base_url": "https://api.openai.com/v1",
    "api_key": "your_api_key"
  }
}
```

`model_config` is optional. When omitted, the backend uses the `DEEPSEEK_API_KEY` environment variable and the default model configuration.

### Multi-Agent Simulation

```http
POST /api/simulate
```

Returns a Server-Sent Events stream.

Example request:

```json
{
  "question": "What are the core devices required for neutral-atom quantum computing?",
  "mode": "simulation",
  "rounds": 3,
  "lang": "en"
}
```

### LLM Configuration APIs

Get the provider presets available to the frontend:

```http
GET /api/models/providers
```

Test a user-supplied LLM configuration:

```http
POST /api/models/test
```

Example request:

```json
{
  "provider": "qwen",
  "api_kind": "openai",
  "model": "qwen-plus",
  "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
  "api_key": "your_api_key"
}
```

### IMA References

```http
POST /api/ima/references
```

Example request:

```json
{
  "question": "Quantum error correction roadmap",
  "subgraph_nodes": ["node_318", "node_604"]
}
```

### Export a Report

```http
POST /api/export/report
```

Request fields:

- `question`: research question
- `mode`: `reasoning` or `simulation`
- `steps`: step-by-step reasoning records
- `prediction`: prediction result
- `ima_references`: relevant reference list
- `lang`: `zh` or `en`
- `format`: `html`, `pdf`, or `docx`
- `export_dir`: export directory; defaults to `~/Downloads`
- `simulation_data`: multi-agent simulation process data

## Graph Data

The main graph file is `graph/graph_data.json`. Common top-level fields include:

- `nodes`: node list
- `edges`: relationship edge list
- `metadata`: graph metadata

Common node fields:

- `id`: node ID
- `label`: Chinese display name
- `label_en`: English display name, when available
- `type`: node type
- `description`: node description
- `properties.importance`: importance score
- `properties.source_documents`: source documents
- `properties.source_knowledge_bases`: source knowledge bases
- `properties.evidence`: evidence text
- `properties.related_terms`: related topics

Common edge fields:

- `source`: source node ID
- `target`: target node ID
- `label`: relationship type
- `weight`: relationship weight

## Frontend Controls

### 3D / 2D Toggle

- `3D`: displays the enhanced 3D research map.
- `2D`: displays the original 2D knowledge graph page.

### Chinese / English Toggle

- Switches the display language of nodes in the 3D graph.
- The control is in the upper-right area of the map, aligned with the 3D / 2D toggle.

### Research Path Controls

The bottom of the page includes several path filters:

- Algorithm Breakthrough Path
- NISQ Application Path
- Error Correction and Fault Tolerance Path
- Hardware Implementation Path
- Cryptography Attack and Defense Path

These controls highlight the corresponding research evolution paths.

## Report Export Notes

For PDF exports, the system first attempts to use WeasyPrint and automatically falls back to ReportLab when necessary. The export endpoint saves the report in `export_dir` and returns the file as a download response.

If the browser reports that you must complete a reasoning task before exporting, verify that:

1. A final prediction appears in the right-hand reasoning panel.
2. The browser is on `/quantum_reasoning.html`, not an API endpoint such as `/api/export/report`.
3. You refresh the page and run the reasoning task again.

## Troubleshooting

### The Page Does Not Open

Check the service:

```bash
curl http://127.0.0.1:6122/api/health
```

If the backend is not running:

```bash
python3 reasoning_server.py
```

Or restart the full development service:

```bash
npm run dev
```

### Port Already in Use

The project uses port `6122` by default. If another project is using that port, stop the conflicting process first. For cloud deployments, also confirm that the security group allows inbound traffic on port `6122`.

```bash
lsof -nP -iTCP:6122 -sTCP:LISTEN
```

### The Graph Does Not Appear

Check that:

- `graph/graph_data.json` exists.
- The browser console does not report a Three.js CDN loading error.
- `graph_loaded` is `true` in the `/api/health` response.

### Exported Reports Do Not Include References

Report references depend on the entities, evidence, and local graph source metadata in the current reasoning task. Missing references usually indicate that relevant nodes do not contain `source_documents` or `source_knowledge_bases`. Add the missing source metadata to those nodes in `graph/graph_data.json`.

## Development Notes

- Do not modify unrelated files currently being edited by a user.
- Most frontend logic is in `quantum_reasoning.html`.
- Backend reasoning, simulation, IMA references, and export logic are in `reasoning_server.py`.
- Frontend changes usually take effect after refreshing the browser.
- Backend changes require restarting `reasoning_server.py`; replacing only `graph/graph_data.json` does not.
- Report export has separate HTML, Word, and PDF generation paths. Check all three formats when changing report formatting.

## Current Defaults

- Unified service port: `6122`
- Default export directory: `~/Downloads`
- Default reasoning model: `deepseek-v4-pro`
- Default graph file: `graph/graph_data.json`

## Maintenance Recommendations

- When adding a new report, store its title, chapter summary, and key conclusions in `source_documents`, `evidence`, and `description`.
- Keep version numbers in graph expansion script names, such as `expand_graph_v10.py`, to preserve historical build logic.
- If the project later integrates a live IMA API, upgrade `/api/ima/references` from graph metadata lookup to live knowledge-base retrieval.
- As the 3D map grows, extract node layout, color, path, and rendering logic into separate JavaScript modules to reduce the maintenance burden in `quantum_reasoning.html`.
