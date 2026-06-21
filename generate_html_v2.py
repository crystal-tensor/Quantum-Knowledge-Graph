#!/usr/bin/env python3
"""
Generate quantum knowledge graph HTML visualization (v2 - expanded)
D3.js v7 force-directed layout with rich interactivity
"""

import json
import os

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
GRAPH_FILE = os.environ.get("GRAPH_DATA_PATH", os.path.join(WORKSPACE, "graph", "graph_data.json"))
OUTPUT_FILE = os.path.join(WORKSPACE, "quantum_knowledge_graph.html")

def load_graph():
    with open(GRAPH_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_html():
    data = load_graph()
    
    # Prepare graph data for embedding
    graph_data = {
        "metadata": data["metadata"],
        "nodes": data["nodes"],
        "edges": data["edges"]
    }
    
    # Category colors and icons
    categories = {
        "concept": {"color": "#4FC3F7", "icon": "💡", "label": "概念"},
        "algorithm": {"color": "#FF8A65", "icon": "⚙️", "label": "算法"},
        "hardware": {"color": "#81C784", "icon": "🔧", "label": "硬件"},
        "company": {"color": "#E57373", "icon": "🏢", "label": "公司"},
        "application": {"color": "#FFD54F", "icon": "🎯", "label": "应用"},
        "person": {"color": "#BA68C8", "icon": "👤", "label": "人物"},
        "protocol": {"color": "#4DB6AC", "icon": "📋", "label": "协议"},
        "tool": {"color": "#90A4AE", "icon": "🛠️", "label": "工具"},
        "material": {"color": "#A1887F", "icon": "🔬", "label": "材料"},
        "theory": {"color": "#7986CB", "icon": "📚", "label": "理论"},
        "organization": {"color": "#F06292", "icon": "🏛️", "label": "机构"},
    }
    
    graph_json = json.dumps(graph_data, ensure_ascii=False)
    categories_json = json.dumps(categories, ensure_ascii=False)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>量子计算知识图谱</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
    background: #0a0e17;
    color: #e0e0e0;
    overflow: hidden;
    height: 100vh;
}}

#app {{
    display: flex;
    height: 100vh;
}}

/* Left panel */
#sidebar {{
    width: 300px;
    min-width: 300px;
    background: linear-gradient(180deg, #0f1523 0%, #0a0e17 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
    display: flex;
    flex-direction: column;
    z-index: 10;
    overflow-y: auto;
}}

.sidebar-header {{
    padding: 20px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}}

.sidebar-header h1 {{
    font-size: 20px;
    font-weight: 700;
    background: linear-gradient(135deg, #4FC3F7, #BA68C8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
}}

.sidebar-header p {{
    font-size: 12px;
    color: #888;
}}

.stats {{
    display: flex;
    gap: 12px;
    margin-top: 12px;
}}

.stat {{
    flex: 1;
    background: rgba(255,255,255,0.04);
    border-radius: 8px;
    padding: 8px;
    text-align: center;
}}

.stat-value {{
    font-size: 18px;
    font-weight: 700;
    color: #4FC3F7;
}}

.stat-label {{
    font-size: 10px;
    color: #666;
    margin-top: 2px;
}}

/* Search */
.search-box {{
    padding: 16px 20px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}}

.search-box input {{
    width: 100%;
    padding: 10px 14px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    color: #e0e0e0;
    font-size: 14px;
    outline: none;
    transition: border-color 0.2s;
}}

.search-box input:focus {{
    border-color: #4FC3F7;
}}

.search-box input::placeholder {{
    color: #555;
}}

/* Filters */
.filters {{
    padding: 16px 20px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    flex: 1;
    overflow-y: auto;
}}

.filters h3 {{
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #666;
    margin-bottom: 12px;
}}

.filter-group {{
    display: flex;
    flex-direction: column;
    gap: 6px;
}}

.filter-item {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 10px;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.2s;
    font-size: 13px;
}}

.filter-item:hover {{
    background: rgba(255,255,255,0.06);
}}

.filter-item.active {{
    background: rgba(255,255,255,0.1);
}}

.filter-dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
}}

.filter-count {{
    margin-left: auto;
    color: #555;
    font-size: 11px;
}}

/* Source KB list */
.source-kbs {{
    padding: 16px 20px;
    border-top: 1px solid rgba(255,255,255,0.06);
}}

.source-kbs h3 {{
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #666;
    margin-bottom: 8px;
}}

.kb-item {{
    font-size: 12px;
    color: #888;
    padding: 3px 0;
    display: flex;
    align-items: center;
    gap: 6px;
}}

.kb-item::before {{
    content: "📚";
    font-size: 10px;
}}

/* Main graph area */
#graph-container {{
    flex: 1;
    position: relative;
    overflow: hidden;
}}

svg {{
    width: 100%;
    height: 100%;
}}

/* Node styles */
.node {{
    cursor: pointer;
}}

.node circle {{
    stroke-width: 2;
    transition: r 0.2s;
}}

.node:hover circle {{
    filter: brightness(1.3);
}}

.node text {{
    font-size: 11px;
    fill: #ccc;
    pointer-events: none;
    text-anchor: middle;
    font-weight: 500;
}}

/* Node selected state */
.node.selected circle {{
    stroke: #fff !important;
    stroke-width: 3px !important;
    filter: drop-shadow(0 0 8px rgba(255,255,255,0.4)) !important;
}}

.node.dimmed circle {{
    opacity: 0.15;
}}
.node.dimmed text {{
    opacity: 0.15;
}}

/* Link styles */
.link {{
    stroke-opacity: 0.25;
    fill: none;
    transition: stroke-opacity 0.2s;
}}

.link.highlighted {{
    stroke-opacity: 0.85;
    stroke-width: 2.5px !important;
}}

.link.dimmed {{
    stroke-opacity: 0.05;
}}

/* Tooltip */
#tooltip {{
    position: absolute;
    display: none;
    background: rgba(15, 21, 35, 0.95);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 10px;
    padding: 14px 16px;
    max-width: 350px;
    pointer-events: none;
    z-index: 100;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}}

.tooltip-type {{
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
    opacity: 0.7;
}}

.tooltip-label {{
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 6px;
    color: #fff;
}}

.tooltip-desc {{
    font-size: 12px;
    line-height: 1.5;
    color: #aaa;
}}

.tooltip-importance {{
    margin-top: 8px;
    display: flex;
    align-items: center;
    gap: 4px;
}}

.tooltip-importance .star {{
    color: #FFD54F;
    font-size: 12px;
}}

.tooltip-importance .star.empty {{
    color: #333;
}}

.tooltip-sources {{
    margin-top: 8px;
    font-size: 10px;
    color: #666;
    padding-top: 8px;
    border-top: 1px solid rgba(255,255,255,0.06);
}}

/* Detail panel */
#detail-panel {{
    position: absolute;
    right: -400px;
    top: 0;
    width: 380px;
    height: 100%;
    background: linear-gradient(180deg, #0f1523 0%, #0a0e17 100%);
    border-left: 1px solid rgba(255,255,255,0.1);
    z-index: 50;
    transition: right 0.3s ease;
    overflow-y: auto;
    padding: 24px;
}}

#detail-panel.open {{
    right: 0;
}}

.detail-close {{
    position: absolute;
    top: 16px;
    right: 16px;
    background: none;
    border: none;
    color: #888;
    font-size: 20px;
    cursor: pointer;
    padding: 4px;
}}

.detail-close:hover {{
    color: #fff;
}}

.detail-type {{
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
}}

.detail-label {{
    font-size: 22px;
    font-weight: 700;
    color: #fff;
    margin-bottom: 12px;
}}

.detail-desc {{
    font-size: 14px;
    line-height: 1.7;
    color: #aaa;
    margin-bottom: 20px;
}}

.detail-section {{
    margin-bottom: 20px;
}}

.detail-section h4 {{
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #666;
    margin-bottom: 10px;
}}

.detail-connections {{
    display: flex;
    flex-direction: column;
    gap: 6px;
}}

.detail-connection {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 10px;
    background: rgba(255,255,255,0.04);
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.2s;
}}

.detail-connection:hover {{
    background: rgba(255,255,255,0.08);
}}

.detail-connection .dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}}

.detail-connection .rel-label {{
    font-size: 10px;
    color: #666;
    margin-left: auto;
}}

/* Zoom controls */
.zoom-controls {{
    position: absolute;
    bottom: 20px;
    right: 20px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    z-index: 20;
}}

.zoom-btn {{
    width: 36px;
    height: 36px;
    background: rgba(15, 21, 35, 0.8);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    color: #aaa;
    font-size: 18px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
}}

.zoom-btn:hover {{
    background: rgba(255,255,255,0.1);
    color: #fff;
}}

/* Loading */
#loading {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    z-index: 200;
}}

#loading .spinner {{
    width: 40px;
    height: 40px;
    border: 3px solid rgba(79, 195, 247, 0.2);
    border-top-color: #4FC3F7;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin: 0 auto 12px;
}}

@keyframes spin {{
    to {{ transform: rotate(360deg); }}
}}

#loading p {{
    color: #666;
    font-size: 14px;
}}

/* Legend (bottom-left) */
.legend {{
    position: absolute;
    bottom: 20px;
    left: 20px;
    background: rgba(15, 21, 35, 0.85);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 12px 16px;
    z-index: 20;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    max-width: 500px;
}}

.legend-item {{
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 11px;
    color: #888;
    cursor: pointer;
    padding: 2px 6px;
    border-radius: 4px;
    transition: background 0.2s;
}}

.legend-item:hover {{
    background: rgba(255,255,255,0.06);
}}

.legend-dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
}}

/* Info badge */
.info-badge {{
    position: absolute;
    top: 16px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(15, 21, 35, 0.85);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 12px;
    color: #888;
    z-index: 20;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.3s;
}}

.info-badge.visible {{
    opacity: 1;
}}

/* Scrollbar */
::-webkit-scrollbar {{
    width: 4px;
}}
::-webkit-scrollbar-track {{
    background: transparent;
}}
::-webkit-scrollbar-thumb {{
    background: rgba(255,255,255,0.1);
    border-radius: 2px;
}}
::-webkit-scrollbar-thumb:hover {{
    background: rgba(255,255,255,0.2);
}}
</style>
</head>
<body>
<div id="app">
    <div id="sidebar">
        <div class="sidebar-header">
            <h1>量子计算知识图谱</h1>
            <p>基于5个IMA知识库构建</p>
            <div class="stats">
                <div class="stat">
                    <div class="stat-value" id="node-count">{data["metadata"]["node_count"]}</div>
                    <div class="stat-label">知识节点</div>
                </div>
                <div class="stat">
                    <div class="stat-value" id="edge-count">{data["metadata"]["edge_count"]}</div>
                    <div class="stat-label">关系边</div>
                </div>
                <div class="stat">
                    <div class="stat-value" id="type-count">{len(categories)}</div>
                    <div class="stat-label">实体类型</div>
                </div>
            </div>
        </div>
        <div class="search-box">
            <input type="text" id="search-input" placeholder="🔍 搜索节点..." autocomplete="off">
        </div>
        <div class="filters">
            <h3>节点类型筛选</h3>
            <div class="filter-group" id="filter-group"></div>
        </div>
        <div class="source-kbs">
            <h3>数据来源 (IMA知识库)</h3>
            <div class="kb-item">量子计算学习材料 (96篇)</div>
            <div class="kb-item">量子产业研究报告 (106篇)</div>
            <div class="kb-item">金贻荣老师的直播课件 (79篇)</div>
            <div class="kb-item">量子计算 (44篇)</div>
            <div class="kb-item">李博士的项目 (111篇)</div>
        </div>
    </div>
    <div id="graph-container">
        <div id="loading">
            <div class="spinner"></div>
            <p>正在构建知识图谱...</p>
        </div>
        <svg id="graph-svg"></svg>
        <div class="legend" id="legend"></div>
        <div class="zoom-controls">
            <button class="zoom-btn" id="zoom-in" title="放大">+</button>
            <button class="zoom-btn" id="zoom-out" title="缩小">−</button>
            <button class="zoom-btn" id="zoom-reset" title="重置">⟲</button>
        </div>
        <div class="info-badge" id="info-badge"></div>
        <div id="tooltip"></div>
        <div id="detail-panel">
            <button class="detail-close" id="detail-close">✕</button>
            <div id="detail-content"></div>
        </div>
    </div>
</div>

<script>
const GRAPH_DATA = {graph_json};
const CATEGORIES = {categories_json};

// State
let activeFilters = new Set(Object.keys(CATEGORIES));
let selectedNode = null;
let simulation = null;
let nodeElements, linkElements, textElements;

// Initialize
document.addEventListener('DOMContentLoaded', init);

function init() {{
    buildFilters();
    buildLegend();
    initGraph();
    setupSearch();
    setupZoom();
    
    // Hide loading after graph renders
    setTimeout(() => {{
        document.getElementById('loading').style.display = 'none';
    }}, 1500);
}}

function buildFilters() {{
    const group = document.getElementById('filter-group');
    const typeCounts = {{}};
    GRAPH_DATA.nodes.forEach(n => {{
        typeCounts[n.type] = (typeCounts[n.type] || 0) + 1;
    }});
    
    Object.entries(CATEGORIES).forEach(([type, info]) => {{
        const count = typeCounts[type] || 0;
        if (count === 0) return;
        const item = document.createElement('div');
        item.className = 'filter-item active';
        item.dataset.type = type;
        item.innerHTML = `
            <span class="filter-dot" style="background:${{info.color}}"></span>
            <span>${{info.icon}} ${{info.label}}</span>
            <span class="filter-count">${{count}}</span>
        `;
        item.addEventListener('click', () => toggleFilter(type, item));
        group.appendChild(item);
    }});
}}

function buildLegend() {{
    const legend = document.getElementById('legend');
    Object.entries(CATEGORIES).forEach(([type, info]) => {{
        const item = document.createElement('div');
        item.className = 'legend-item';
        item.innerHTML = `<span class="legend-dot" style="background:${{info.color}}"></span>${{info.label}}`;
        legend.appendChild(item);
    }});
}}

function toggleFilter(type, element) {{
    if (activeFilters.has(type)) {{
        activeFilters.delete(type);
        element.classList.remove('active');
    }} else {{
        activeFilters.add(type);
        element.classList.add('active');
    }}
    updateGraph();
}}

function getVisibleData() {{
    const searchTerm = document.getElementById('search-input').value.toLowerCase().trim();
    const visibleNodes = GRAPH_DATA.nodes.filter(n => {{
        if (!activeFilters.has(n.type)) return false;
        if (searchTerm && !n.label.toLowerCase().includes(searchTerm) && 
            !n.description.toLowerCase().includes(searchTerm)) return false;
        return true;
    }});
    const visibleIds = new Set(visibleNodes.map(n => n.id));
    const visibleEdges = GRAPH_DATA.edges.filter(e => 
        visibleIds.has(e.source) && visibleIds.has(e.target)
    );
    return {{ nodes: visibleNodes, edges: visibleEdges }};
}}

function initGraph() {{
    const container = document.getElementById('graph-container');
    const width = container.clientWidth;
    const height = container.clientHeight;
    
    const svg = d3.select('#graph-svg')
        .attr('width', width)
        .attr('height', height);
    
    // Defs for glow effect
    const defs = svg.append('defs');
    Object.entries(CATEGORIES).forEach(([type, info]) => {{
        const filter = defs.append('filter')
            .attr('id', `glow-${{type}}`)
            .attr('x', '-50%').attr('y', '-50%')
            .attr('width', '200%').attr('height', '200%');
        filter.append('feGaussianBlur')
            .attr('stdDeviation', '3')
            .attr('result', 'blur');
        filter.append('feFlood')
            .attr('flood-color', info.color)
            .attr('flood-opacity', '0.3');
        filter.append('feComposite')
            .attr('in2', 'blur')
            .attr('operator', 'in');
        const merge = filter.append('feMerge');
        merge.append('feMergeNode');
        merge.append('feMergeNode').attr('in', 'SourceGraphic');
    }});
    
    const g = svg.append('g');
    
    // Zoom
    const zoom = d3.zoom()
        .scaleExtent([0.1, 4])
        .on('zoom', (event) => {{
            g.attr('transform', event.transform);
        }});
    svg.call(zoom);
    
    // Store zoom reference
    window.graphZoom = zoom;
    window.graphSvg = svg;
    window.graphG = g;
    
    // Initial render
    renderGraph(g, width, height);
}}

function renderGraph(g, width, height) {{
    const {{ nodes, edges }} = getVisibleData();
    
    // Clear
    g.selectAll('*').remove();
    
    if (simulation) simulation.stop();
    
    // Build link data with proper source/target
    const nodeMap = {{}};
    nodes.forEach(n => nodeMap[n.id] = n);
    
    const links = edges.filter(e => nodeMap[e.source] && nodeMap[e.target])
        .map(e => ({{
            source: e.source,
            target: e.target,
            label: e.label,
            weight: e.weight || 1
        }}));
    
    // Simulation - optimized for 1000+ edge graph
    simulation = d3.forceSimulation(nodes)
        .force('link', d3.forceLink(links).id(d => d.id).distance(d => {{
            return 100 + (1 - (d.weight || 1)) * 80;
        }}).strength(0.15))
        .force('charge', d3.forceManyBody().strength(-350).distanceMax(500))
        .force('center', d3.forceCenter(width / 2, height / 2).strength(0.05))
        .force('collision', d3.forceCollide().radius(d => getNodeRadius(d) + 8))
        .force('x', d3.forceX(width / 2).strength(0.03))
        .force('y', d3.forceY(height / 2).strength(0.03));
    
    // Links
    linkElements = g.append('g')
        .attr('class', 'links')
        .selectAll('line')
        .data(links)
        .join('line')
        .attr('class', 'link')
        .attr('stroke', d => {{
            const srcNode = nodeMap[d.source.id || d.source];
            const tgtNode = nodeMap[d.target.id || d.target];
            if (srcNode && tgtNode) {{
                const srcColor = CATEGORIES[srcNode.type]?.color || '#555';
                const tgtColor = CATEGORIES[tgtNode.type]?.color || '#555';
                return srcColor;
            }}
            return '#333';
        }})
        .attr('stroke-width', d => Math.max(0.5, (d.weight || 1) * 1.5));
    
    // Nodes
    nodeElements = g.append('g')
        .attr('class', 'nodes')
        .selectAll('g')
        .data(nodes)
        .join('g')
        .attr('class', 'node')
        .call(d3.drag()
            .on('start', dragStarted)
            .on('drag', dragged)
            .on('end', dragEnded))
        .on('click', (event, d) => {{
            event.stopPropagation();
            selectNode(d);
        }})
        .on('mouseover', (event, d) => showTooltip(event, d))
        .on('mouseout', hideTooltip);
    
    // Node circles
    nodeElements.append('circle')
        .attr('r', d => getNodeRadius(d))
        .attr('fill', d => {{
            const cat = CATEGORIES[d.type];
            return cat ? cat.color : '#555';
        }})
        .attr('stroke', d => {{
            const cat = CATEGORIES[d.type];
            return cat ? d3.color(cat.color).brighter(0.5) : '#777';
        }})
        .attr('stroke-width', d => d.properties?.importance >= 4 ? 2.5 : 1.5)
        .attr('filter', d => d.properties?.importance >= 5 ? `url(#glow-${{d.type}})` : null);
    
    // Node labels
    textElements = nodeElements.append('text')
        .text(d => {{
            const label = d.label;
            return label.length > 12 ? label.substring(0, 11) + '…' : label;
        }})
        .attr('dy', d => getNodeRadius(d) + 14)
        .attr('font-size', d => d.properties?.importance >= 4 ? '12px' : '10px')
        .attr('fill', d => {{
            const cat = CATEGORIES[d.type];
            return cat ? cat.color : '#aaa';
        }});
    
    // Tick
    simulation.on('tick', () => {{
        linkElements
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);
        
        nodeElements
            .attr('transform', d => `translate(${{d.x}},${{d.y}})`);
    }});
}}

function getNodeRadius(d) {{
    const importance = d.properties?.importance || 3;
    return 6 + importance * 3;
}}

function updateGraph() {{
    const container = document.getElementById('graph-container');
    const width = container.clientWidth;
    const height = container.clientHeight;
    const g = window.graphG;
    renderGraph(g, width, height);
}}

function dragStarted(event, d) {{
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}}

function dragged(event, d) {{
    d.fx = event.x;
    d.fy = event.y;
}}

function dragEnded(event, d) {{
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}}

function showTooltip(event, d) {{
    const tooltip = document.getElementById('tooltip');
    const cat = CATEGORIES[d.type] || {{ label: d.type, color: '#555' }};
    const importance = d.properties?.importance || 3;
    
    let starsHtml = '';
    for (let i = 1; i <= 5; i++) {{
        starsHtml += `<span class="star ${{i <= importance ? '' : 'empty'}}">★</span>`;
    }}
    
    let sourcesHtml = '';
    const kbs = d.properties?.source_knowledge_bases || [];
    if (kbs.length > 0) {{
        const kbNames = {{"7412047272751870":"量子计算学习材料","7425064727240963":"量子产业研究报告","7411640966326739":"金贻荣老师直播课件","7408677623443647":"量子计算","7441506466037417":"李博士的项目"}};
        const names = kbs.map(id => kbNames[id] || id).join(', ');
        sourcesHtml = `<div class="tooltip-sources">📚 来源: ${{names}}</div>`;
    }}
    
    tooltip.innerHTML = `
        <div class="tooltip-type" style="color:${{cat.color}}">${{cat.icon}} ${{cat.label}}</div>
        <div class="tooltip-label">${{d.label}}</div>
        <div class="tooltip-desc">${{d.description}}</div>
        <div class="tooltip-importance">${{starsHtml}}</div>
        ${{sourcesHtml}}
    `;
    
    tooltip.style.display = 'block';
    const rect = document.getElementById('graph-container').getBoundingClientRect();
    let x = event.clientX - rect.left + 15;
    let y = event.clientY - rect.top - 10;
    if (x + 350 > rect.width) x = x - 370;
    if (y + 200 > rect.height) y = y - 200;
    tooltip.style.left = x + 'px';
    tooltip.style.top = y + 'px';
}}

function hideTooltip() {{
    document.getElementById('tooltip').style.display = 'none';
}}

function selectNode(d) {{
    selectedNode = d;
    const panel = document.getElementById('detail-panel');
    const content = document.getElementById('detail-content');
    const cat = CATEGORIES[d.type] || {{ label: d.type, color: '#555' }};
    
    // Highlight related nodes/edges, dim others
    const connectedIds = new Set([d.id]);
    const connectedEdgeIndices = new Set();
    const edgeData = linkElements.data();
    
    edgeData.forEach((e, i) => {{
        const srcId = e.source.id || e.source;
        const tgtId = e.target.id || e.target;
        if (srcId === d.id || tgtId === d.id) {{
            connectedIds.add(srcId);
            connectedIds.add(tgtId);
            connectedEdgeIndices.add(i);
        }}
    }});
    
    nodeElements.classed('selected', n => n.id === d.id)
        .classed('dimmed', n => !connectedIds.has(n.id));
    
    linkElements.classed('highlighted', (e, i) => connectedEdgeIndices.has(i))
        .classed('dimmed', (e, i) => !connectedEdgeIndices.has(i));
    
    textElements.classed('dimmed', n => !connectedIds.has(n.id));
    
    // Find connections
    const connections = [];
    GRAPH_DATA.edges.forEach(e => {{
        if (e.source === d.id) {{
            const target = GRAPH_DATA.nodes.find(n => n.id === e.target);
            if (target) connections.push({{ node: target, direction: 'out', label: e.label }});
        }} else if (e.target === d.id) {{
            const source = GRAPH_DATA.nodes.find(n => n.id === e.source);
            if (source) connections.push({{ node: source, direction: 'in', label: e.label }});
        }}
    }});
    
    const importance = d.properties?.importance || 3;
    let starsHtml = '';
    for (let i = 1; i <= 5; i++) {{
        starsHtml += `<span class="star ${{i <= importance ? '' : 'empty'}}" style="font-size:14px">★</span>`;
    }}
    
    let connectionsHtml = connections.slice(0, 30).map(c => {{
        const cCat = CATEGORIES[c.node.type] || {{ color: '#555' }};
        const relLabel = c.direction === 'out' ? c.label : `← ${{c.label}}`;
        return `
            <div class="detail-connection" data-node-id="${{c.node.id}}">
                <span class="dot" style="background:${{cCat.color}}"></span>
                <span>${{c.node.label}}</span>
                <span class="rel-label">${{relLabel}}</span>
            </div>
        `;
    }}).join('');
    
    if (connections.length > 30) {{
        connectionsHtml += `<div style="font-size:11px;color:#555;padding:6px">...还有${{connections.length - 30}}个连接</div>`;
    }}
    
    content.innerHTML = `
        <div class="detail-type" style="color:${{cat.color}}">${{cat.icon}} ${{cat.label}}</div>
        <div class="detail-label">${{d.label}}</div>
        <div class="detail-desc">${{d.description}}</div>
        <div style="margin-bottom:20px">${{starsHtml}}</div>
        <div class="detail-section">
            <h4>关联节点 (${{connections.length}})</h4>
            <div class="detail-connections">${{connectionsHtml}}</div>
        </div>
    `;
    
    panel.classList.add('open');
    
    // Click connection to navigate
    content.querySelectorAll('.detail-connection').forEach(el => {{
        el.addEventListener('click', () => {{
            const nodeId = el.dataset.nodeId;
            const node = GRAPH_DATA.nodes.find(n => n.id === nodeId);
            if (node) selectNode(node);
        }});
    }});
}}

function clearHighlights() {{
    nodeElements.classed('selected', false).classed('dimmed', false);
    linkElements.classed('highlighted', false).classed('dimmed', false);
    textElements.classed('dimmed', false);
}}

// Close detail panel
document.getElementById('detail-close').addEventListener('click', () => {{
    document.getElementById('detail-panel').classList.remove('open');
    selectedNode = null;
    clearHighlights();
}});

// Search
function setupSearch() {{
    const input = document.getElementById('search-input');
    let timeout;
    input.addEventListener('input', () => {{
        clearTimeout(timeout);
        timeout = setTimeout(updateGraph, 300);
    }});
}}

// Zoom controls
function setupZoom() {{
    document.getElementById('zoom-in').addEventListener('click', () => {{
        window.graphSvg.transition().duration(300).call(
            window.graphZoom.scaleBy, 1.3
        );
    }});
    document.getElementById('zoom-out').addEventListener('click', () => {{
        window.graphSvg.transition().duration(300).call(
            window.graphZoom.scaleBy, 0.7
        );
    }});
    document.getElementById('zoom-reset').addEventListener('click', () => {{
        window.graphSvg.transition().duration(500).call(
            window.graphZoom.transform, d3.zoomIdentity
        );
    }});
}}

// Click on empty space to deselect
document.getElementById('graph-container').addEventListener('click', (e) => {{
    if (e.target.tagName === 'svg' || e.target.tagName === 'SVG') {{
        document.getElementById('detail-panel').classList.remove('open');
        selectedNode = null;
        clearHighlights();
    }}
}});

// Resize handler
window.addEventListener('resize', () => {{
    const container = document.getElementById('graph-container');
    const svg = d3.select('#graph-svg')
        .attr('width', container.clientWidth)
        .attr('height', container.clientHeight);
}});
</script>
</body>
</html>'''
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    file_size = os.path.getsize(OUTPUT_FILE)
    print(f"Generated: {OUTPUT_FILE}")
    print(f"File size: {file_size / 1024:.1f} KB")
    print(f"Nodes: {data['metadata']['node_count']}")
    print(f"Edges: {data['metadata']['edge_count']}")

if __name__ == '__main__':
    generate_html()
