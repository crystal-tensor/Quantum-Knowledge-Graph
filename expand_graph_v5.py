#!/usr/bin/env python3
"""
Phase 4: Add more cross-links to boost edge count to 800+
Focus on adding dense relationships between related concepts
"""

import json
import os

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
GRAPH_FILE = os.environ.get("GRAPH_DATA_PATH", os.path.join(WORKSPACE, "graph", "graph_data.json"))

def load_graph():
    with open(GRAPH_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_graph(data):
    with open(GRAPH_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_edge(edges, source, target, rel_type, weight=1.0):
    for e in edges:
        if e['source'] == source and e['target'] == target and e.get('label', '') == rel_type:
            return
        # Also check reverse
        if e['source'] == target and e['target'] == source and e.get('label', '') == rel_type:
            return
    edges.append({
        "source": source,
        "target": target,
        "label": rel_type,
        "weight": float(weight)
    })

def main():
    data = load_graph()
    nodes = data['nodes']
    edges = data['edges']
    
    print(f"Starting: {len(nodes)} nodes, {len(edges)} edges")
    
    # Build label->id map (fuzzy)
    label_to_id = {}
    for n in nodes:
        lbl = n['label']
        label_to_id[lbl] = n['id']
        # Simplified
        simp = lbl.split(' (')[0].split(' - ')[0].strip()
        if simp not in label_to_id:
            label_to_id[simp] = n['id']
    
    def safe_add(src_label, tgt_label, rel, weight=1.0):
        src_id = label_to_id.get(src_label)
        tgt_id = label_to_id.get(tgt_label)
        if not src_id:
            for n in nodes:
                if src_label in n['label']:
                    src_id = n['id']
                    break
        if not tgt_id:
            for n in nodes:
                if tgt_label in n['label']:
                    tgt_id = n['id']
                    break
        if src_id and tgt_id and src_id != tgt_id:
            add_edge(edges, src_id, tgt_id, rel, weight)
    
    # ============================================================
    # DENSE cross-links: connect ALL remaining important pairs
    # ============================================================
    
    # Core concept pairs (bidirectional relationships)
    core_pairs = [
        # Quantum computing fundamentals - all pairs
        ("量子比特", "叠加态", "uses", 5),
        ("量子比特", "量子纠缠", "uses", 5),
        ("量子比特", "量子门", "uses", 5),
        ("量子比特", "量子测量", "uses", 5),
        ("量子比特", "量子电路", "uses", 5),
        ("量子比特", "量子算法", "uses", 4),
        ("叠加态", "波函数坍缩", "related_to", 4),
        ("量子纠缠", "Bell态", "enables", 5),
        ("量子纠缠", "EPR对", "enables", 5),
        ("量子纠缠", "量子隐形传态", "enables", 5),
        ("量子测量", "波函数坍缩", "related_to", 5),
        ("量子门", "CNOT门", "uses", 5),
        ("量子门", "Hadamard门", "uses", 4),
        ("量子电路", "量子算法", "implements", 4),
        ("量子算法", "量子编程", "implements", 4),
        ("量子算法", "量子优势", "enables", 4),
        
        # Platform comparisons
        ("超导量子比特", "离子阱量子比特", "competes_with", 4),
        ("超导量子比特", "中性原子量子比特", "competes_with", 3),
        ("超导量子比特", "光量子计算", "competes_with", 3),
        ("离子阱量子比特", "中性原子量子比特", "competes_with", 3),
        ("超导量子比特", "硅基量子比特", "competes_with", 3),
        
        # Error correction chain
        ("量子纠错", "量子纠错码", "uses", 5),
        ("量子纠错", "表面码", "uses", 5),
        ("量子纠错", "逻辑量子比特", "enables", 5),
        ("量子纠错", "容错量子计算", "enables", 5),
        ("量子纠错", "量子噪声", "addresses", 5),
        ("量子纠错阈值定理", "量子纠错", "related_to", 5),
        ("容错量子计算", "逻辑量子比特", "uses", 5),
        ("表面码", "逻辑量子比特", "enables", 5),
        
        # Applications
        ("量子化学模拟", "量子药物发现", "enables", 4),
        ("量子化学模拟", "量子材料科学", "enables", 4),
        ("量子化学模拟", "VQE", "uses", 5),
        ("量子金融", "量子组合优化", "uses", 4),
        ("量子金融", "QAOA", "uses", 3),
        ("量子机器学习", "量子深度学习", "part_of", 4),
        ("量子机器学习", "变分量子电路", "uses", 4),
        ("量子优化", "QAOA", "uses", 4),
        ("量子优化", "量子组合优化", "uses", 3),
        ("量子传感", "量子精密测量", "enables", 4),
        ("量子密码学", "量子密钥分发", "uses", 5),
        ("量子密码学", "后量子密码学", "related_to", 4),
        
        # Hardware
        ("超导量子比特", "约瑟夫森结", "uses", 5),
        ("超导量子比特", "稀释制冷机", "uses", 5),
        ("超导量子比特", "Transmon", "is_type_of", 5),
        ("离子阱量子比特", "激光冷却", "uses", 3),
        ("中性原子量子比特", "光学镊子", "uses", 3),
        ("硅基量子比特", "量子点", "uses", 4),
        ("光量子计算", "PsiQuantum", "uses", 4),
        
        # Companies
        ("IBM", "Qiskit", "developed_by", 5),
        ("谷歌", "Cirq", "developed_by", 4),
        ("谷歌", "量子优越性", "enables", 5),
        ("Quantinuum", "离子阱量子比特", "uses", 5),
        ("本源量子", "量子编程", "enables", 4),
        ("相干科技", "北京量子信息科学研究院", "derives_from", 5),
        
        # People
        ("金贻荣", "量子工程学", "related_to", 5),
        ("郭国平", "本源量子", "founded_by", 5),
        ("郭光灿", "量子信息", "researches", 5),
        
        # Communication
        ("量子通信", "量子密钥分发", "uses", 5),
        ("量子通信", "量子网络", "uses", 4),
        ("量子网络", "量子中继器", "uses", 4),
        ("量子互联网", "量子网络", "is_type_of", 4),
        
        # Theory
        ("量子力学", "薛定谔方程", "part_of", 5),
        ("量子力学", "海森堡不确定性原理", "part_of", 5),
        ("量子力学", "量子计算", "enables", 5),
        
        # NISQ
        ("NISQ时代", "VQE", "uses", 4),
        ("NISQ时代", "QAOA", "uses", 4),
        ("NISQ时代", "量子噪声", "challenged_by", 4),
        
        # Scaling
        ("量子计算产业化", "量子云平台", "enables", 4),
        ("量子计算产业化", "量子优势", "related_to", 4),
        ("量子计算产业化", "容错量子计算", "enables", 4),
    ]
    
    for src, tgt, rel, w in core_pairs:
        safe_add(src, tgt, rel, w)
    
    # ============================================================
    # More cross-links for all remaining concept pairs
    # ============================================================
    
    more_pairs = [
        # Concept pairs - algorithms
        ("Shor算法", "量子优势", "enables", 4),
        ("Shor算法", "量子傅里叶变换", "uses", 5),
        ("Shor算法", "量子相位估计", "uses", 4),
        ("Grover搜索算法", "量子随机行走", "related_to", 3),
        ("量子随机行走", "量子算法设计", "uses", 3),
        ("量子相位估计", "Shor算法", "part_of", 4),
        ("VQE", "量子化学模拟", "enables", 5),
        ("VQE", "量子药物发现", "enables", 4),
        ("QAOA", "量子组合优化", "solves", 4),
        
        # Hardware detailed
        ("Sycamore处理器", "谷歌", "made_by", 5),
        ("IBM Eagle处理器", "IBM", "made_by", 5),
        ("IBM Condor处理器", "IBM", "made_by", 5),
        ("九章光量子计算机", "中科大", "made_by", 5),
        ("祖冲之三号", "中科大", "made_by", 5),
        ("Willow", "谷歌", "made_by", 5),
        
        # Benchmark
        ("量子体积", "量子性能分级标准", "part_of", 4),
        ("量子基准测试", "量子性能分级标准", "uses", 4),
        
        # DiVincenzo for all platforms
        ("DiVincenzo准则", "超导量子比特", "applies_to", 4),
        ("DiVincenzo准则", "离子阱量子比特", "applies_to", 4),
        ("DiVincenzo准则", "量子比特体系", "defines", 4),
        
        # T1/T2 for platforms
        ("T1弛豫时间", "退相干", "related_to", 4),
        ("T2退相干时间", "退相干", "related_to", 4),
        ("T1弛豫时间", "超导量子比特", "determines", 4),
        ("T2退相干时间", "离子阱量子比特", "determines", 3),
        
        # More error correction
        ("Magic State Distillation", "容错量子计算", "part_of", 4),
        ("量子纠错码", "表面码", "includes", 4),
        
        # Communication detailed
        ("量子密钥分发", "量子不可克隆定理", "enables", 4),
        ("量子中继器", "量子存储器", "uses", 4),
        ("量子互联网", "代尔夫特理工大学", "researched_at", 3),
        
        # Materials
        ("NV色心", "量子传感", "enables", 4),
        ("量子点", "自旋量子比特", "enables", 4),
        ("拓扑绝缘体", "马约拉纳零模", "hosts", 4),
        
        # Tools detailed
        ("Qiskit", "量子电路", "uses", 4),
        ("Cirq", "量子电路", "uses", 4),
        ("PennyLane", "变分量子电路", "uses", 4),
        
        # Noise
        ("量子噪声", "去极化噪声", "includes", 4),
        ("量子噪声", "振幅阻尼", "includes", 4),
        ("量子噪声", "相位阻尼", "includes", 4),
        ("退相干", "量子噪声", "causes", 4),
        
        # Circuit QED
        ("Circuit QED", "谐振腔", "uses", 5),
        ("谐振腔", "量子总线", "is_type_of", 4),
        ("量子总线", "超导量子比特", "connects", 4),
        
        # Annealing
        ("量子退火算法", "D-Wave", "uses", 5),
        ("量子退火算法", "量子优化", "related_to", 3),
        
        # Reports
        ("光子盒研究院", "量子计算产业化", "reports_on", 4),
        ("CQCC量子计算大会", "量子计算产业化", "reports_on", 4),
        
        # Country strategies
        ("谷歌", "美国量子战略", "part_of", 3),
        ("IBM", "美国量子战略", "part_of", 3),
        ("微软", "美国量子战略", "part_of", 3),
        ("相干科技", "中国量子战略", "part_of", 3),
        ("本源量子", "中国量子战略", "part_of", 3),
        
        # Mixed states
        ("混合态", "纯态", "contrasts_with", 3),
        ("密度矩阵", "约化密度矩阵", "related_to", 3),
        ("量子态层析", "密度矩阵", "reconstructs", 4),
        
        # GHZ and entanglement
        ("GHZ态", "多比特纠缠态", "is_type_of", 4),
        ("多比特纠缠态", "量子纠缠", "manifests", 4),
        
        # Additional edges for completeness
        ("量子傅里叶变换", "量子相位估计", "enables", 4),
        ("量子相位估计", "量子算法", "part_of", 3),
        ("变分量子电路", "VQE", "uses", 5),
        ("变分量子电路", "NISQ时代", "enables", 4),
        
        # Fabrication chain
        ("量子芯片", "量子比特制备", "requires", 4),
        ("量子比特制备", "良品率", "determines", 4),
        ("量子比特串扰", "多量子芯片互连", "affects", 3),
        
        # Quantum advantage milestones
        ("量子优越性", "Sycamore处理器", "demonstrated_on", 5),
        ("量子优势", "祖冲之三号", "demonstrated_on", 4),
        ("量子优势", "九章光量子计算机", "demonstrated_on", 4),
        
        # Country comparison
        ("中国量子战略", "美国量子战略", "competes_with", 4),
        ("欧洲量子战略", "美国量子战略", "competes_with", 3),
        
        # Application details
        ("量子材料科学", "分子模拟", "uses", 3),
        ("量子模拟", "费米-哈伯德模型", "applies_to", 4),
        ("量子模拟", "超导配对关联", "studies", 3),
        
        # Deep learning chain
        ("量子深度学习", "变分量子电路", "uses", 4),
        ("量子深度学习", "PennyLane", "enables", 3),
        
        # Qubit types - Transmon is main
        ("Transmon", "电荷量子比特", "derived_from", 3),
        ("Transmon", "磁通量子比特", "related_to", 3),
        ("磁通量子比特", "超导量子比特", "is_type_of", 3),
        ("电荷量子比特", "超导量子比特", "is_type_of", 3),
        
        # Organizations and research
        ("MIT", "超导量子比特", "researches", 4),
        ("MIT", "量子纠错", "researches", 3),
        ("芝加哥大学", "量子传感", "researches", 3),
        ("斯坦福大学", "NV色心", "researches", 2),
        
        # PsiQuantum and others
        ("PsiQuantum", "硅光子", "uses", 4),
        ("QuEra Computing", "中性原子分区架构", "uses", 3),
        ("Pasqal", "中性原子量子比特", "develops", 4),
    ]
    
    for src, tgt, rel, w in more_pairs:
        safe_add(src, tgt, rel, w)
    
    # ============================================================
    # Create additional useful links
    # ============================================================
    
    extra_pairs = [
        # Measurements
        ("量子测量", "量子态层析", "uses", 3),
        ("量子态层析", "密度矩阵", "produces", 4),
        
        # Gate calibration
        ("量子门校准", "门保真度", "improves", 4),
        ("门保真度", "量子电路", "determines", 3),
        
        # Software stack
        ("量子编程", "量子软件", "is_part_of", 4),
        ("量子软件", "量子云平台", "runs_on", 3),
        
        # More cross-platform links
        ("超导量子比特", "量子比特操控", "requires", 4),
        ("超导量子比特", "量子比特读取", "requires", 4),
        ("离子阱量子比特", "量子比特操控", "requires", 3),
        ("中性原子量子比特", "量子比特操控", "requires", 3),
        
        # Error budget
        ("量子噪声", "门保真度", "degrades", 4),
        ("退相干", "门保真度", "degrades", 4),
        ("退相干", "读取保真度", "degrades", 3),
        
        # Algorithm comparison
        ("Shor算法", "Grover搜索算法", "competes_with", 3),
        ("VQE", "QAOA", "competes_with", 2),
        
        # Reports cross-links
        ("2026全球量子计算产业发展展望", "量子计算产业化", "describes", 4),
        ("2024-2025年度CQCC量子计算产业报告", "量子计算产业化", "describes", 3),
        ("量子计算：掌握未来", "量子计算产业化", "describes", 3),
        
        # Kitaev chain (for Majorana)
        ("Kitaev链", "马约拉纳零模", "hosts", 4),
        ("拓扑量子计算", "Kitaev链", "uses", 3),
        
        # RCS (Linear cross-entropy benchmarking)
        ("交叉熵基准测试", "量子优越性", "measures", 4),
        ("线性交叉熵基准测试", "量子优越性", "measures", 4),
        
        # Neutral atom - optical tweezer
        ("光学镊子", "中性原子量子比特", "traps", 4),
        ("里德伯态", "中性原子量子比特", "uses", 3),
        
        # Additional concepts
        ("量子体积", "门保真度", "depends_on", 3),
        ("量子体积", "相干时间", "depends_on", 3),
        ("量子性能分级标准", "量子体积", "includes", 3),
        
        # VQE detailed
        ("VQE", "自适应VQE", "improves", 3),
        ("VQE", "量子子空间展开", "related_to", 3),
        
        # QAOA detailed
        ("QAOA", "数字退火", "related_to", 3),
        ("QAOA", "变分算法", "is_type_of", 4),
        
        # Countries
        ("中国", "中国量子战略", "has", 4),
        ("美国", "美国量子战略", "has", 4),
        ("欧盟", "欧洲量子战略", "has", 3),
        
        # Data from IMA reports
        ("光子盒研究院", "2025全球量子计算产业发展展望", "publishes", 4),
        ("中关村量子产业联盟", "量子计算：掌握未来", "authors", 4),
    ]
    
    for src, tgt, rel, w in extra_pairs:
        safe_add(src, tgt, rel, w)
    
    # ============================================================
    # Statistics
    # ============================================================
    
    # Count node types
    type_counts = {}
    for n in nodes:
        t = n['type']
        type_counts[t] = type_counts.get(t, 0) + 1
    
    print(f"Final: {len(nodes)} nodes, {len(edges)} edges")
    print("\nNode type distribution:")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")
    
    edge_type_counts = {}
    for e in edges:
        t = e.get('label', 'unknown')
        edge_type_counts[t] = edge_type_counts.get(t, 0) + 1
    print(f"\nEdge type distribution (top 20):")
    for t, c in sorted(edge_type_counts.items(), key=lambda x: -x[1])[:20]:
        print(f"  {t}: {c}")
    
    # Save
    data['metadata']['node_count'] = len(nodes)
    data['metadata']['edge_count'] = len(edges)
    data['metadata']['last_updated'] = '2026-06-13'
    save_graph(data)
    print(f"\nSaved to {GRAPH_FILE}")

if __name__ == '__main__':
    main()
