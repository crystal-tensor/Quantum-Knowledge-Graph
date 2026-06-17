# 量子知识图谱 · 3D 推演引擎

这是一个面向量子计算研究、产业分析和知识推演的本地 Web 应用。项目把量子计算知识图谱、3D 研究地图、二维知识图谱、多步骤推理、多智能体模拟、IMA 来源文献列表和报告导出整合到同一个界面中。

默认入口：

- 前端页面：http://127.0.0.1:6122/quantum_reasoning.html
- 后端 API：http://127.0.0.1:6123

## 核心能力

### 1. 3D 量子研究地图

- 以三维地球/向量空间式布局展示量子计算知识图谱。
- 图谱节点包含概念、硬件、算法、公司、人物、机构、材料、工具、报告、QEC 路线等类型。
- 支持地球外围卫星式节点，用于展示公司、机构、工具、人物、报告等外层实体。
- 支持点击节点查看来源、证据链、难度、研究演进路径。
- 支持攻击路径筛选。这里的“攻击路径”指研究演进路线，例如从问题提出到算法突破，再到硬件实现的知识推进路径。
- 支持中文 / EN 节点语言切换。
- 支持 3D / 2D 地图切换。

### 2. 二维知识图谱

- 2D 模式会嵌入原始 `quantum_knowledge_graph.html` 页面。
- 右侧知识推演引擎在 2D 和 3D 模式下都会保留。
- 适合在密集节点关系中快速查找实体和关联。

### 3. 知识推演引擎

右侧推演面板支持两种模式。

逐步推理：

- 从问题解析开始，检索相关子图。
- 基于知识图谱进行多步骤逻辑推演。
- 输出多维度分析、预测结论、置信度、支撑证据和不确定因素。
- 推演完成后自动列出相关文献列表，包含 IMA 文章、知识库、关联节点和章节/内容片段。

多智能体模拟：

- 根据问题复杂度动态选择相关实体，不固定为 6 个。
- 为每个相关实体生成智能体人设。
- 多轮讨论后由协调者总结共识、分歧和综合预测。
- 模拟完成后输出最终预测报告、模拟详细列表和相关文献列表。
- 第 2 轮等轮次摘要如果模型没有返回，系统会使用本地兜底摘要。

### 4. IMA 来源与证据

图谱节点会从元数据中读取来源信息，主要来自以下知识库：

- 量子计算学习材料
- 量子产业研究报告
- 金贻荣老师的直播课件
- 量子计算
- 李博士的项目

推演后的相关文献列表会尽量列出：

- 文档标题
- 所属知识库
- 文档数
- 关联节点
- 涉及章节或内容片段
- 原始证据和关联主题

### 5. 报告导出

支持导出以下格式：

- HTML
- PDF
- Word `.docx`

导出内容包括：

- 问题、模式、日期和图谱规模
- 逐步推理过程或多智能体模拟过程
- 预测结论和置信度
- 支撑证据与关键因素
- 相关文献列表
- 文献章节/内容片段

导出报告会清洗模型输出中的 Markdown 标记，例如 `###`、`- **`、`>` 等，使报告更像正式研究文档。

## 项目结构

```text
QuanKnowledeg/
├── graph_data.json                    # 主知识图谱数据
├── quantum_reasoning.html             # 3D 研究地图 + 推演引擎主页面
├── quantum_knowledge_graph.html       # 原二维知识图谱页面
├── reasoning_server.py                # FastAPI 后端、推演、模拟、导出接口
├── package.json                       # 本地开发脚本
├── scripts/
│   └── dev-server.js                  # 前端静态服务 + API 代理 + 后端启动检查
├── expand_graph*.py                   # 图谱扩展脚本
├── generate_html*.py                  # 历史 HTML 生成脚本
├── server.log                         # 后端运行日志
└── README.md
```

## 环境要求

推荐环境：

- macOS / Linux
- Node.js 18+
- Python 3.10+
- 可访问本地端口 `6122` 和 `6123`

Python 依赖主要包括：

- `fastapi`
- `uvicorn`
- `httpx`
- `pydantic`
- `python-docx`
- `reportlab`
- `weasyprint` 可选，用于优先生成 PDF。如果不可用，系统会自动使用 ReportLab 兜底。

前端依赖：

- 页面通过 CDN 加载 Three.js。
- 本地开发服务只需要 Node.js 原生 `http` 模块。

## 环境变量

后端不会在代码中保存 API Key。运行推演前需要在本机环境中设置：

```bash
export DEEPSEEK_API_KEY="your_deepseek_api_key"
```

也可以在自己的 shell 配置、进程管理器或本地 `.env` 工作流中注入该变量。`.env` 文件默认不会提交到 Git。

也可以不使用默认 DeepSeek 环境变量，直接在页面右上角点击“模型设置”，添加自己的大模型 API。当前内置预设包括：

- DeepSeek
- OpenAI
- Anthropic Claude
- Google Gemini
- 阿里通义千问 Qwen
- Moonshot Kimi
- 智谱 GLM
- 火山方舟 Doubao
- SiliconFlow
- OpenRouter
- 自定义 OpenAI 兼容接口

启用“使用我自己的大模型 API 进行推演”后，必须点击“测试模型”并测试通过，页面才允许用该模型运行逐步推理或多智能体模拟。API Key 只保存在当前浏览器的 `localStorage` 中，不会写入项目文件，也不会被 Git 提交。

## 启动方式

在项目根目录执行：

```bash
npm run dev
```

默认会：

1. 检查 `http://127.0.0.1:6123/api/health` 是否已有当前项目后端。
2. 如果没有后端，会启动 `python3 reasoning_server.py`。
3. 启动前端静态服务，默认监听 `http://127.0.0.1:6122`。
4. 如果 6122 被占用，会自动尝试下一个端口。

打开：

```text
http://127.0.0.1:6122/quantum_reasoning.html
```

## 手动启动后端

如果只想启动后端：

```bash
python3 reasoning_server.py
```

健康检查：

```bash
curl http://127.0.0.1:6123/api/health
```

正常返回示例：

```json
{
  "status": "ok",
  "base_dir": "/Users/avalok/work/QuanKnowledeg",
  "graph_loaded": true,
  "node_count": 385,
  "edge_count": 1223
}
```

## 常用 API

### 健康检查

```http
GET /api/health
```

### 图谱统计

```http
GET /api/stats
```

### 获取完整图谱

```http
GET /api/graph/full
```

参数：

- `limit_nodes`：默认 500
- `limit_edges`：默认 2000

### 根据问题检索相关子图

```http
POST /api/subgraph
```

请求示例：

```json
{
  "question": "量子纠错何时突破",
  "max_nodes": 80
}
```

### 逐步推理

```http
POST /api/reason
```

返回 Server-Sent Events 流。

请求示例：

```json
{
  "question": "超导量子能否实现容错？",
  "mode": "reasoning",
  "max_nodes": 80,
  "lang": "zh",
  "model_config": {
    "provider": "openai",
    "api_kind": "openai",
    "model": "gpt-4.1",
    "base_url": "https://api.openai.com/v1",
    "api_key": "your_api_key"
  }
}
```

`model_config` 可省略。省略时后端使用 `DEEPSEEK_API_KEY` 环境变量和默认模型配置。

### 多智能体模拟

```http
POST /api/simulate
```

返回 Server-Sent Events 流。

### 大模型配置接口

获取前端可用厂商预设：

```http
GET /api/models/providers
```

测试用户填写的大模型配置：

```http
POST /api/models/test
```

请求示例：

```json
{
  "provider": "qwen",
  "api_kind": "openai",
  "model": "qwen-plus",
  "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
  "api_key": "your_api_key"
}
```

请求示例：

```json
{
  "question": "中性原子核心设备有哪些？",
  "mode": "simulation",
  "rounds": 3,
  "lang": "zh"
}
```

### IMA 相关文献

```http
POST /api/ima/references
```

请求示例：

```json
{
  "question": "量子纠错路线图",
  "subgraph_nodes": ["node_318", "node_604"]
}
```

### 导出报告

```http
POST /api/export/report
```

请求字段：

- `question`：问题
- `mode`：`reasoning` 或 `simulation`
- `steps`：逐步推理步骤
- `prediction`：预测结论
- `ima_references`：相关文献列表
- `lang`：`zh` 或 `en`
- `format`：`html`、`pdf` 或 `docx`
- `export_dir`：导出目录，默认 `~/Downloads`
- `simulation_data`：多智能体模拟过程数据

## 图谱数据说明

主图谱文件是 `graph_data.json`。常见字段包括：

- `nodes`：节点列表
- `edges`：关系边列表
- `metadata`：图谱元信息

节点常见字段：

- `id`：节点 ID
- `label`：中文显示名
- `label_en`：英文显示名，如果存在
- `type`：节点类型
- `description`：节点描述
- `properties.importance`：重要度
- `properties.source_documents`：来源文档
- `properties.source_knowledge_bases`：来源知识库
- `properties.evidence`：证据文本
- `properties.related_terms`：关联主题

边常见字段：

- `source`：源节点 ID
- `target`：目标节点 ID
- `label`：关系类型
- `weight`：关系权重

## 前端交互说明

### 3D / 2D 切换

- `3D`：显示升级后的三维研究地图。
- `2D`：显示原始二维知识图谱页面。

### 中文 / EN 切换

- 切换 3D 图谱节点显示语言。
- 该按钮位于地图右上区域，与 3D / 2D 切换按钮同一高度。

### 研究路径按钮

页面底部包含多个路径筛选按钮：

- 算法突破路线
- NISQ 应用路线
- 纠错容错路线
- 硬件实现路线
- 密码攻防路线

这些按钮用于突出相关研究演进路线。

## 导出报告注意事项

如果 PDF 导出失败，系统会先尝试 WeasyPrint，再自动回退到 ReportLab。导出接口会把报告保存到 `export_dir`，同时返回文件下载响应。

如果浏览器提示“请先完成一次推演再导出报告”，请确认：

1. 右侧推演已经出现最终预测结论。
2. 当前页面没有在 `/api/export/report` 这样的接口地址上，而是在 `/quantum_reasoning.html`。
3. 刷新页面后重新推演一次。

## 常见问题

### 页面打不开

先检查服务：

```bash
curl http://127.0.0.1:6123/api/health
```

如果 6122 代理不通，再检查后端：

```bash
curl http://127.0.0.1:6123/api/health
```

如果后端未启动：

```bash
python3 reasoning_server.py
```

或重新启动完整开发服务：

```bash
npm run dev
```

### 端口被占用

前端服务会从 6122 开始自动寻找可用端口。后端默认使用 6123，如果 6123 被其他项目占用，可以设置：

```bash
BACKEND_PORT=6124 npm run dev
```

### 图谱没有显示

检查：

- `graph_data.json` 是否存在。
- 浏览器控制台是否有 Three.js CDN 加载错误。
- `/api/health` 中 `graph_loaded` 是否为 `true`。

### 导出报告没有文献

导出依赖当前推演过程中的实体、证据和本地图谱来源元数据。如果没有文献，通常说明相关节点缺少 `source_documents` 或 `source_knowledge_bases` 字段。可以在 `graph_data.json` 中补充节点来源元数据。

## 开发注意事项

- 不要直接改动用户正在编辑的无关文件。
- 前端主要逻辑集中在 `quantum_reasoning.html`。
- 后端推理、模拟、IMA 引用和导出集中在 `reasoning_server.py`。
- 修改前端后通常刷新浏览器即可生效。
- 修改后端后需要重启 `reasoning_server.py`。
- 导出报告涉及 HTML、Word、PDF 三套生成逻辑，改格式时需要同步检查三种格式。

## 当前默认配置

- 前端端口：`6122`
- 后端端口：`6123`
- 默认导出目录：`~/Downloads`
- 默认推演模型：`deepseek-v4-pro`
- 默认图谱文件：`graph_data.json`

## 维护建议

- 增加新报告时，优先把报告标题、章节摘要和关键结论写入 `source_documents`、`evidence` 和 `description`。
- 图谱扩展脚本建议保留版本号，例如 `expand_graph_v10.py`，避免覆盖历史构建逻辑。
- 如果后续接入真实 IMA API，可以把 `/api/ima/references` 从当前的图谱元数据检索升级为真实知识库检索。
- 若继续扩展 3D 地图，建议把节点布局、颜色、路径和渲染逻辑拆分出独立 JS 模块，降低 `quantum_reasoning.html` 的维护压力。
