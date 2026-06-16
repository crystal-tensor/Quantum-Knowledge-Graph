import json

# Load graph data
with open("/Users/danielcrystal/WorkBuddy/2026-06-13-17-30-18/graph_data.json", "r", encoding="utf-8") as f:
    graph_data = json.load(f)

# Create HTML content
html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>量子计算知识图谱</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0a0e1a; color: #e0e6f0; overflow: hidden; }
#app { display: flex; height: 100vh; }
#canvas-container { flex: 1; position: relative; }
svg { width: 100%; height: 100%; }
#sidebar { width: 380px; background: linear-gradient(180deg, #0f1628 0%, #141c30 100%); border-left: 1px solid #1e2a45; overflow-y: auto; display: flex; flex-direction: column; }
#toolbar { padding: 16px; background: rgba(15, 22, 40, 0.95); border-bottom: 1px solid #1e2a45; backdrop-filter: blur(10px); }
#toolbar h1 { font-size: 18px; color: #7eb8ff; margin-bottom: 12px; font-weight: 600; }
#search-box { width: 100%; padding: 10px 14px; background: #1a2238; border: 1px solid #2a3a5c; border-radius: 8px; color: #e0e6f0; font-size: 14px; outline: none; transition: border-color 0.2s; }
#search-box:focus { border-color: #4a9eff; }
#search-box::placeholder { color: #5a6a8a; }
#stats { display: flex; gap: 8px; margin-top: 12px; flex-wrap: wrap; }
.stat-item { background: #1a2238; padding: 6px 12px; border-radius: 6px; font-size: 12px; color: #8a9ab8; }
.stat-item span { color: #7eb8ff; font-weight: 600; }
#filter-panel { padding: 12px 16px; border-bottom: 1px solid #1e2a45; }
#filter-panel h3 { font-size: 13px; color: #8a9ab8; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }
.filter-group { display: flex; flex-wrap: wrap; gap: 6px; }
.filter-btn { padding: 4px 10px; border-radius: 12px; font-size: 12px; cursor: pointer; border: 1px solid transparent; transition: all 0.2s; background: #1a2238; color: #8a9ab8; }
.filter-btn.active { border-color: currentColor; }
.filter-btn:hover { background: #243050; }
#detail-panel { flex: 1; padding: 16px; overflow-y: auto; }
#detail-panel .empty { text-align: center; color: #4a5a7a; padding: 40px 20px; font-size: 14px; }
#detail-panel .node-detail h2 { font-size: 18px; margin-bottom: 8px; color: #e0e6f0; }
#detail-panel .node-detail .type-badge { display: inline-block; padding: 3px 10px; border-radius: 10px; font-size: 12px; margin-bottom: 12px; }
#detail-panel .node-detail .description { font-size: 14px; color: #a0b0d0; line-height: 1.6; margin-bottom: 16px; }
#detail-panel .node-detail .section-title { font-size: 13px; color: #7eb8ff; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }
#detail-panel .node-detail .relation-list { list-style: none; }
#detail-panel .node-detail .relation-list li { padding: 6px 0; font-size: 13px; color: #8a9ab8; border-bottom: 1px solid #1e2a45; cursor: pointer; }
#detail-panel .node-detail .relation-list li:hover { color: #7eb8ff; }
#detail-panel .node-detail .relation-list li .rel-label { color: #5a6a8a; font-size: 11px; margin-left: 4px; }
#legend { position: absolute; bottom: 20px; left: 20px; background: rgba(15, 22, 40, 0.9); padding: 12px 16px; border-radius: 8px; border: 1px solid #1e2a45; backdrop-filter: blur(10px); }
#legend h4 { font-size: 12px; color: #8a9ab8; margin-bottom: 8px; }
.legend-item { display: flex; align-items: center; gap: 6px; margin-bottom: 4px; font-size: 12px; color: #8a9ab8; }
.legend-dot { width: 10px; height: 10px; border-radius: 50%; }
#kb-filter { padding: 12px 16px; border-bottom: 1px solid #1e2a45; }
#kb-filter h3 { font-size: 13px; color: #8a9ab8; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }
.kb-btn { display: block; width: 100%; text-align: left; padding: 6px 10px; border-radius: 6px; font-size: 12px; color: #8a9ab8; background: transparent; border: none; cursor: pointer; margin-bottom: 4px; transition: all 0.2s; }
.kb-btn:hover, .kb-btn.active { background: #1a2238; color: #7eb8ff; }
#path-finder { padding: 12px 16px; border-bottom: 1px solid #1e2a45; }
#path-finder h3 { font-size: 13px; color: #8a9ab8; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }
.path-input { width: 100%; padding: 8px 10px; background: #1a2238; border: 1px solid #2a3a5c; border-radius: 6px; color: #e0e6f0; font-size: 12px; margin-bottom: 6px; outline: none; }
.path-input:focus { border-color: #4a9eff; }
#path-result { font-size: 12px; color: #7eb8ff; min-height: 20px; margin-top: 4px; }
#tooltip { position: absolute; pointer-events: none; background: rgba(15, 22, 40, 0.95); border: 1px solid #2a3a5c; border-radius: 8px; padding: 10px 14px; font-size: 13px; max-width: 260px; backdrop-filter: blur(10px); z-index: 100; display: none; }
#tooltip .tt-label { color: #e0e6f0; font-weight: 600; margin-bottom: 4px; }
#tooltip .tt-type { font-size: 11px; color: #8a9ab8; margin-bottom: 4px; }
#tooltip .tt-desc { color: #a0b0d0; font-size: 12px; line-height: 1.4; }
/* Scrollbar styling */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0f1628; }
::-webkit-scrollbar-thumb { background: #2a3a5c; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #3a4a6c; }
</style>
</head>
<body>
<div id="app">
  <div id="canvas-container">
    <svg id="graph-svg"></svg>
    <div id="legend"></div>
    <div id="tooltip"></div>
  </div>
  <div id="sidebar">
    <div id="toolbar">
      <h1>⚛️ 量子计算知识图谱</h1>
      <input type="text" id="search-box" placeholder="🔍 搜索知识点...">
      <div id="stats"></div>
    </div>
    <div id="filter-panel">
      <h3>类型筛选</h3>
      <div class="filter-group" id="type-filters"></div>
    </div>
    <div id="detail-panel">
      <div class="empty">点击节点查看详细信息</div>
    </div>
  </div>
</div>
<script>
// Graph data embedded
const graphData = ''' + json.dumps(graph_data, ensure_ascii=False) + ''';

// Node type colors and labels
const typeConfig = {
  concept: { color: '#4a9eff', label: '核心概念', glow: '#4a9eff' },
  algorithm: { color: '#4ade80', label: '量子算法', glow: '#4ade80' },
  hardware: { color: '#f59e0b', label: '硬件技术', glow: '#f59e0b' },
  company: { color: '#f87171', label: '机构/企业', glow: '#f87171' },
  application: { color: '#c084fc', label: '应用领域', glow: '#c084fc' },
  person: { color: '#22d3ee', label: '关键人物', glow: '#22d3ee' },
  protocol: { color: '#facc15', label: '协议/标准', glow: '#facc15' },
  tool: { color: '#f472b6', label: '软件工具', glow: '#f472b6' },
  material: { color: '#a78bfa', label: '物理材料/器件', glow: '#a78bfa' },
  theory: { color: '#60a5fa', label: '理论框架', glow: '#60a5fa' }
};

// State
let activeFilters = new Set(Object.keys(typeConfig));
let selectedNode = null;
let hoveredNode = null;

// Initialize SVG
const width = window.innerWidth - 380;
const height = window.innerHeight;
const svg = d3.select('#graph-svg');
const g = svg.append('g');

// Zoom
const zoom = d3.zoom()
  .scaleExtent([0.1, 4])
  .on('zoom', (event) => g.attr('transform', event.transform));
svg.call(zoom);

// Create force simulation
const simulation = d3.forceSimulation(graphData.nodes)
  .force('link', d3.forceLink(graphData.edges).id(d => d.id).distance(d => 80 + (1-d.weight)*120))
  .force('charge', d3.forceManyBody().strength(d => -200 * (d.properties?.importance || 3)))
  .force('center', d3.forceCenter(width/2, height/2))
  .force('collision', d3.forceCollide().radius(d => getNodeRadius(d) + 5));

// Build node lookup
const nodeMap = {};
graphData.nodes.forEach(n => nodeMap[n.id] = n);

// Build adjacency for quick lookup
const adjMap = {};
graphData.nodes.forEach(n => adjMap[n.id] = new Set());
graphData.edges.forEach(e => {
  const sid = typeof e.source === 'object' ? e.source.id : e.source;
  const tid = typeof e.target === 'object' ? e.target.id : e.target;
  adjMap[sid]?.add(tid);
  adjMap[tid]?.add(sid);
});

function getNodeRadius(d) {
  const imp = d.properties?.importance || 3;
  return 5 + imp * 3;
}

// Draw links
const link = g.append('g')
  .selectAll('line')
  .data(graphData.edges)
  .join('line')
  .attr('stroke', '#1e2a45')
  .attr('stroke-width', d => 1 + d.weight * 1.5)
  .attr('stroke-opacity', 0.6);

// Draw nodes
const node = g.append('g')
  .selectAll('g')
  .data(graphData.nodes)
  .join('g')
  .attr('class', 'node')
  .call(d3.drag()
    .on('start', dragStarted)
    .on('drag', dragged)
    .on('end', dragEnded));

// Glow effect for important nodes
node.filter(d => (d.properties?.importance || 3) >= 4)
  .append('circle')
  .attr('r', d => getNodeRadius(d) + 6)
  .attr('fill', 'none')
  .attr('stroke', d => typeConfig[d.type]?.glow || '#4a9eff')
  .attr('stroke-width', 2)
  .attr('stroke-opacity', 0.2);

// Main circle
node.append('circle')
  .attr('r', d => getNodeRadius(d))
  .attr('fill', d => typeConfig[d.type]?.color || '#4a9eff')
  .attr('fill-opacity', 0.85)
  .attr('stroke', d => d3.color(typeConfig[d.type]?.color || '#4a9eff').brighter(0.5))
  .attr('stroke-width', 1.5)
  .attr('cursor', 'pointer');

// Labels for important nodes
node.filter(d => (d.properties?.importance || 3) >= 3)
  .append('text')
  .text(d => d.label.length > 12 ? d.label.slice(0,12)+'...' : d.label)
  .attr('dx', d => getNodeRadius(d) + 6)
  .attr('dy', 4)
  .attr('fill', '#a0b0d0')
  .attr('font-size', d => (d.properties?.importance || 3) >= 4 ? '11px' : '10px')
  .attr('font-weight', d => (d.properties?.importance || 3) >= 4 ? '600' : '400')
  .style('pointer-events', 'none');

// Interaction
node.on('mouseover', function(event, d) {
  hoveredNode = d;
  const config = typeConfig[d.type] || {};
  d3.select(this).select('circle').transition().duration(150)
    .attr('r', getNodeRadius(d) + 3)
    .attr('fill-opacity', 1);
  // Show tooltip
  const tooltip = document.getElementById('tooltip');
  tooltip.innerHTML = `<div class="tt-label">${d.label}</div><div class="tt-type">${config.label || d.type}</div><div class="tt-desc">${d.description || ''}</div>`;
  tooltip.style.display = 'block';
  tooltip.style.left = (event.offsetX + 15) + 'px';
  tooltip.style.top = (event.offsetY - 10) + 'px';
  // Highlight connected
  const connected = adjMap[d.id] || new Set();
  node.attr('opacity', n => connected.has(n.id) || n.id === d.id ? 1 : 0.2);
  link.attr('stroke-opacity', e => {
    const sid = typeof e.source === 'object' ? e.source.id : e.source;
    const tid = typeof e.target === 'object' ? e.target.id : e.target;
    return (sid === d.id || tid === d.id) ? 0.9 : 0.1;
  }).attr('stroke', e => {
    const sid = typeof e.source === 'object' ? e.source.id : e.source;
    const tid = typeof e.target === 'object' ? e.target.id : e.target;
    return (sid === d.id || tid === d.id) ? config.color : '#1e2a45';
  });
}).on('mouseout', function(event, d) {
  hoveredNode = null;
  d3.select(this).select('circle').transition().duration(150)
    .attr('r', getNodeRadius(d))
    .attr('fill-opacity', 0.85);
  document.getElementById('tooltip').style.display = 'none';
  resetHighlight();
}).on('click', function(event, d) {
  event.stopPropagation();
  selectedNode = d;
  showDetail(d);
});

svg.on('click', () => {
  selectedNode = null;
  resetHighlight();
  document.querySelector('#detail-panel').innerHTML = '<div class="empty">点击节点查看详细信息</div>';
});

function resetHighlight() {
  node.attr('opacity', n => activeFilters.has(n.type) ? 1 : 0.1);
  link.attr('stroke', '#1e2a45').attr('stroke-opacity', 0.5);
}

function showDetail(d) {
  const config = typeConfig[d.type] || {};
  // Find relations
  const outgoing = graphData.edges.filter(e => (typeof e.source === 'object' ? e.source.id : e.source) === d.id);
  const incoming = graphData.edges.filter(e => (typeof e.target === 'object' ? e.target.id : e.target) === d.id);
  
  let html = '<div class="node-detail">';
  html += `<h2>${d.label}</h2>`;
  html += `<span class="type-badge" style="background:${config.color}22;color:${config.color};border:1px solid ${config.color}44">${config.label || d.type}</span>`;
  html += `<p class="description">${d.description || ''}</p>`;
  
  if (outgoing.length > 0) {
    html += '<div class="section-title">→ 出边关系</div><ul class="relation-list">';
    outgoing.forEach(e => {
      const tid = typeof e.target === 'object' ? e.target.id : e.target;
      const tn = nodeMap[tid];
      if (tn) html += `<li data-id="${tid}">${tn.label} <span class="rel-label">${e.label}</span></li>`;
    });
    html += '</ul>';
  }
  if (incoming.length > 0) {
    html += '<div class="section-title">← 入边关系</div><ul class="relation-list">';
    incoming.forEach(e => {
      const sid = typeof e.source === 'object' ? e.source.id : e.source;
      const sn = nodeMap[sid];
      if (sn) html += `<li data-id="${sid}">${sn.label} <span class="rel-label">${e.label}</span></li>`;
    });
    html += '</ul>';
  }
  html += '</div>';
  
  const panel = document.querySelector('#detail-panel');
  panel.innerHTML = html;
  
  // Click on related nodes
  panel.querySelectorAll('.relation-list li').forEach(li => {
    li.addEventListener('click', () => {
      const nid = li.dataset.id;
      const n = nodeMap[nid];
      if (n) {
        selectedNode = n;
        showDetail(n);
        // Center on node
        const nd = graphData.nodes.find(x => x.id === nid);
        if (nd && nd.x && nd.y) {
          svg.transition().duration(500).call(zoom.transform, d3.zoomIdentity.translate(width/2 - nd.x, height/2 - nd.y));
        }
      }
    });
  });
  
  // Highlight this node and connections
  const connected = adjMap[d.id] || new Set();
  node.attr('opacity', n => connected.has(n.id) || n.id === d.id ? 1 : 0.2);
  link.attr('stroke-opacity', e => {
    const sid = typeof e.source === 'object' ? e.source.id : e.source;
    const tid = typeof e.target === 'object' ? e.target.id : e.target;
    return (sid === d.id || tid === d.id) ? 0.9 : 0.1;
  }).attr('stroke', e => {
    const sid = typeof e.source === 'object' ? e.source.id : e.source;
    const tid = typeof e.target === 'object' ? e.target.id : e.target;
    return (sid === d.id || tid === d.id) ? config.color : '#1e2a45';
  });
}

// Drag functions
function dragStarted(event, d) {
  if (!event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x; d.fy = d.y;
}
function dragged(event, d) {
  d.fx = event.x; d.fy = event.y;
}
function dragEnded(event, d) {
  if (!event.active) simulation.alphaTarget(0);
  d.fx = null; d.fy = null;
}

// Simulation tick
simulation.on('tick', () => {
  link.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
    .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
  node.attr('transform', d => `translate(${d.x},${d.y})`);
});

// Stats
function updateStats() {
  const visibleNodes = graphData.nodes.filter(n => activeFilters.has(n.type));
  const visibleEdges = graphData.edges.filter(e => {
    const sid = typeof e.source === 'object' ? e.source.id : e.source;
    const tid = typeof e.target === 'object' ? e.target.id : e.target;
    return nodeMap[sid] && nodeMap[tid] && activeFilters.has(nodeMap[sid].type) && activeFilters.has(nodeMap[tid].type);
  });
  document.getElementById('stats').innerHTML = `
    <div class="stat-item">节点 <span>${visibleNodes.length}</span></div>
    <div class="stat-item">关系 <span>${visibleEdges.length}</span></div>
    <div class="stat-item">类型 <span>${activeFilters.size}</span></div>
  `;
}
updateStats();

// Type filters
const filterDiv = document.getElementById('type-filters');
Object.entries(typeConfig).forEach(([type, cfg]) => {
  const btn = document.createElement('button');
  btn.className = 'filter-btn active';
  btn.style.color = cfg.color;
  btn.style.borderColor = cfg.color;
  btn.textContent = cfg.label;
  btn.addEventListener('click', () => {
    if (activeFilters.has(type)) {
      activeFilters.delete(type);
      btn.classList.remove('active');
      btn.style.borderColor = 'transparent';
    } else {
      activeFilters.add(type);
      btn.classList.add('active');
      btn.style.borderColor = cfg.color;
    }
    applyFilters();
  });
  filterDiv.appendChild(btn);
});

function applyFilters() {
  node.attr('opacity', d => activeFilters.has(d.type) ? 1 : 0.08)
    .select('circle').attr('fill-opacity', d => activeFilters.has(d.type) ? 0.85 : 0.15);
  link.attr('stroke-opacity', e => {
    const sid = typeof e.source === 'object' ? e.source.id : e.source;
    const tid = typeof e.target === 'object' ? e.target.id : e.target;
    return (nodeMap[sid] && nodeMap[tid] && activeFilters.has(nodeMap[sid].type) && activeFilters.has(nodeMap[tid].type)) ? 0.5 : 0.03;
  });
  updateStats();
}

// Search
const searchBox = document.getElementById('search-box');
searchBox.addEventListener('input', (e) => {
  const query = e.target.value.toLowerCase().trim();
  if (!query) {
    resetHighlight();
    return;
  }
  const matches = graphData.nodes.filter(n => n.label.toLowerCase().includes(query) || (n.description||'').toLowerCase().includes(query));
  const matchIds = new Set(matches.map(n => n.id));
  node.attr('opacity', d => matchIds.has(d.id) ? 1 : 0.1);
  link.attr('stroke-opacity', e => {
    const sid = typeof e.source === 'object' ? e.source.id : e.source;
    const tid = typeof e.target === 'object' ? e.target.id : e.target;
    return (matchIds.has(sid) && matchIds.has(tid)) ? 0.7 : 0.03;
  });
});

// Legend
const legendDiv = document.getElementById('legend');
let legendHtml = '<h4>图例</h4>';
Object.entries(typeConfig).forEach(([type, cfg]) => {
  legendHtml += `<div class="legend-item"><div class="legend-dot" style="background:${cfg.color}"></div>${cfg.label}</div>`;
});
legendDiv.innerHTML = legendHtml;

// Initial zoom to fit
setTimeout(() => {
  const bounds = g.node().getBBox();
  if (bounds.width > 0) {
    const scale = Math.min(width / (bounds.width + 100), height / (bounds.height + 100)) * 0.8;
    const tx = width/2 - (bounds.x + bounds.width/2) * scale;
    const ty = height/2 - (bounds.y + bounds.height/2) * scale;
    svg.transition().duration(1000).call(zoom.transform, d3.zoomIdentity.translate(tx, ty).scale(scale));
  }
}, 2000);

// Resize
window.addEventListener('resize', () => {
  // Simple resize handling
  svg.attr('width', window.innerWidth - 380).attr('height', window.innerHeight);
});
</script>
</body>
</html>''';

# Write HTML file
with open("/Users/danielcrystal/WorkBuddy/2026-06-13-17-30-18/quantum_knowledge_graph.html", "w", encoding="utf-8") as f:
    f.write(html)

import os
file_size = os.path.getsize("/Users/danielcrystal/WorkBuddy/2026-06-13-17-30-18/quantum_knowledge_graph.html")
print(f"HTML file created: {file_size/1024:.1f} KB")
print(f"Nodes: {len(graph_data['nodes'])}, Edges: {len(graph_data['edges'])}")
