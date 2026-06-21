#!/usr/bin/env python3
"""
Phase 5: Add missing node types + cross-links to reach 800+ edges
Focus on: missing concepts, more cross-domain links
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

def get_next_id(nodes):
    max_id = 0
    for n in nodes:
        num = int(n['id'].replace('node_', ''))
        if num > max_id:
            max_id = num
    return f"node_{max_id + 1}"

def add_node(nodes, label, ntype, desc, importance=3, source_kbs=None, source_docs=None, related_terms=None):
    for n in nodes:
        if n['label'] == label:
            return n['id']
    nid = get_next_id(nodes)
    node = {
        "id": nid,
        "label": label,
        "type": ntype,
        "description": desc,
        "properties": {
            "importance": importance,
            "source_documents": source_docs or [],
            "related_terms": related_terms or []
        }
    }
    if source_kbs:
        node["properties"]["source_knowledge_bases"] = source_kbs
    nodes.append(node)
    return nid

def add_edge(edges, source, target, rel_type, weight=1.0):
    for e in edges:
        if e['source'] == source and e['target'] == target and e.get('label', '') == rel_type:
            return
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
    
    # ============================================================
    # Add missing key concepts from quantum computing
    # ============================================================
    
    new_nodes = [
        ("Kitaev链", "concept", "在一维拓扑超导体中实现马约拉纳零模的模型链", 4, 
         ["7441506466037417"], ["拓扑量子计算研究报告"], ["马约拉纳零模", "拓扑超导"]),
        ("里德伯态 (Rydberg State)", "concept", "中性原子中高能激发态，用于中性原子量子计算中的相互作用", 4,
         ["7408677623443647"], ["Enduring_Quantum_Logic.pdf"], ["中性原子", "里德伯阻塞"]),
        ("里德伯阻塞 (Rydberg Blockade)", "concept", "中性原子中里德伯态之间的相互作用导致只能激发一个原子的现象", 4,
         ["7408677623443647"], ["中性原子量子计算"], ["里德伯态", "量子门"]),
        ("光学镊子 (Optical Tweezer)", "hardware", "用聚焦激光束捕获和操控中性原子的装置", 4,
         ["7408677623443647"], ["QuEra Computing"], ["中性原子", "光学捕获"]),
        ("磁通量子比特 (Flux Qubit)", "concept", "用磁通量子的超导量子比特类型，相比Transmon有更多能级参与", 3,
         ["7408677623443647"], ["超导量子计算"], ["超导量子比特", "磁通"]),
        ("电荷量子比特 (Charge Qubit)", "concept", "以电荷为自由度的超导量子比特，对电荷噪声敏感", 3,
         ["7408677623443647"], ["超导量子计算"], ["库珀对", "电荷涨落"]),
        ("硅光子 (Silicon Photonics)", "hardware", "在硅芯片上集成光路的技术，PsiQuantum光量子计算的基础", 3,
         ["7408677623443647"], ["PsiQuantum"], ["光量子计算", "硅基"]),
        ("量子中继器 (Quantum Repeater)", "hardware", "延长量子通信距离的设备，利用纠缠交换和量子存储", 4,
         ["7408677623443647"], ["量子通信"], ["量子网络", "量子存储"]),
        ("交叉熵基准测试 (XEB)", "protocol", "衡量量子处理器性能的基准测试方法，谷歌Sycamore实验使用", 5,
         ["7408677623443647"], ["量子优越性", "Sycamore"], ["量子基准测试"]),
        ("线性交叉熵基准测试 (Linear XEB)", "protocol", "XEB的线性版本，更易于计算", 3,
         ["7408677623443647"], ["量子优越性"], ["交叉熵基准测试"]),
        ("量子子空间展开 (Quantum Subspace Expansion)", "algorithm", "VQE的改进算法，通过子空间展开提高精度", 3,
         ["7408677623443647"], ["VQE"], ["量子化学模拟"]),
        ("自适应VQE (ADAPT-VQE)", "algorithm", "自适应地构建量子电路的VQE变体", 3,
         ["7408677623443647"], ["VQE"], ["量子化学模拟"]),
        ("变分量子电路 (VQC)", "concept", "使用经典-量子混合优化来训练参数的量子电路", 4,
         ["7408677623443647"], ["VQE", "QAOA"], ["变分算法"]),
        ("量子神经网络 (QNN)", "algorithm", "用量子电路模拟神经网络的模型", 3,
         ["7408677623443647"], ["量子机器学习"], ["量子深度学习"]),
        ("哈密顿量 (Hamiltonian)", "theory", "描述量子系统总能量的算符，量子模拟的核心对象", 5,
         ["7408677623443647"], ["量子模拟"], ["薛定谔方程", "本征值"]),
        ("海森堡模型 (Heisenberg Model)", "theory", "描述自旋相互作用的量子多体模型", 4,
         ["7408677623443647"], ["量子模拟", "量子磁性"], ["哈密顿量"]),
        ("量子蒙特卡洛 (Quantum Monte Carlo)", "algorithm", "用于量子多体系统数值计算的蒙特卡洛方法", 3,
         ["7408677623443647"], ["量子模拟"], ["数值计算"]),
        ("张量网络 (Tensor Network)", "theory", "高效表示多体量子态的数学工具", 4,
         ["7408677623443647"], ["量子模拟", "多体物理"], ["矩阵乘积态"]),
        ("D-Wave", "company", "加拿大量子退火计算公司，量子优化领域的领军企业", 4,
         ["7425064727240963"], ["2026全球量子计算"], ["量子退火", "量子优化"]),
        ("Rigetti Computing", "company", "美国超导量子计算公司，开发量子云服务", 3,
         ["7425064727240963"], ["2025全球量子计算"], ["超导量子比特"]),
        ("Xanadu", "company", "加拿大量子计算公司，专注光量子计算和PennyLane平台", 4,
         ["7425064727240963"], ["量子机器学习"], ["光量子计算", "PennyLane"]),
        ("中国", "concept", "量子计算的重要国家力量，在超导和光量子方向处于领先地位", 4, 
         ["7425064727240963"], ["中国量子战略"], ["量子竞争"]),
        ("美国", "concept", "量子计算全球领先国家，在超导、离子阱、中性原子多路线并进", 4,
         ["7425064727240963"], ["美国量子战略"], ["量子竞争"]),
        ("欧盟", "concept", "量子计算的重要力量，推动量子旗舰计划和EuroHPC", 3,
         ["7425064727240963"], ["欧洲量子战略"], ["量子旗舰"]),
        ("EuroHPC", "organization", "欧盟高性能计算联合事业，推动欧洲量子计算发展", 2,
         ["7425064727240963"], ["欧洲量子战略"], ["HPC"]),
        ("量子旗舰 (Quantum Flagship)", "organization", "欧盟量子技术旗舰研究计划", 3,
         ["7425064727240963"], ["欧洲量子战略"], ["欧盟"]),
        ("美国量子战略 (National Quantum Initiative)", "concept", "美国国家级量子倡议，协调量子计算研发投资", 4,
         ["7425064727240963"], ["美国量子战略"], ["NQI"]),
        ("中国量子战略", "concept", "中国国家级量子科技战略，重点发展超导和光量子计算", 4,
         ["7425064727240963"], ["中国"], ["十四五规划"]),
        ("NISQ (Noisy Intermediate-Scale Quantum)", "concept", "有噪声中等规模量子时代，当前量子计算所处阶段", 5,
         ["7408677623443647"], ["量子计算"], ["NISQ时代"]),
        ("库珀对 (Cooper Pair)", "concept", "超导体中配对的电子对，超导量子比特的基本载体", 4,
         ["7408677623443647"], ["超导量子比特", "约瑟夫森结"], ["超导"]),
        ("量子体积 (Quantum Volume)", "protocol", "IBM提出的衡量量子计算机整体性能的综合指标", 4,
         ["7408677623443647"], ["量子基准测试"], ["IBM", "量子性能"]),
        ("随机基准测试 (Randomized Benchmarking)", "protocol", "测量量子门平均错误率的实验方法", 4,
         ["7408677623443647"], ["量子基准测试"], ["门保真度"]),
        ("量子逻辑门 (Quantum Logic Gate)", "concept", "实现量子态变换的基本操作，包括单比特门和两比特门", 5,
         ["7408677623443647"], ["量子门"], ["量子电路"]),
        ("泡利矩阵 (Pauli Matrices)", "theory", "描述单量子比特算符的基矩阵：X、Y、Z", 4,
         ["7408677623443647"], ["量子门", "量子力学"], ["X门", "Y门", "Z门"]),
        ("Bloch球 (Bloch Sphere)", "concept", "可视化单量子比特状态的几何表示", 4,
         ["7408677623443647"], ["量子比特"], ["Bloch矢量"]),
    ]
    
    new_ids = []
    for n in new_nodes:
        nid = add_node(nodes, n[0], n[1], n[2], n[3], n[4], n[5], n[6])
        new_ids.append(nid)
    
    # Build label map
    label_to_id = {}
    for n in nodes:
        label_to_id[n['label']] = n['id']
        simp = n['label'].split(' (')[0].split(' - ')[0].strip()
        if simp not in label_to_id:
            label_to_id[simp] = n['id']
    
    def safe_add(src, tgt, rel, w=1.0):
        src_id = label_to_id.get(src) or next((n['id'] for n in nodes if src in n['label']), None)
        tgt_id = label_to_id.get(tgt) or next((n['id'] for n in nodes if tgt in n['label']), None)
        if src_id and tgt_id and src_id != tgt_id:
            add_edge(edges, src_id, tgt_id, rel, w)
    
    # ============================================================
    # New edges connecting the new nodes
    # ============================================================
    
    new_edges = [
        # Kitaev chain
        ("Kitaev链", "马约拉纳零模", "hosts", 4),
        ("Kitaev链", "拓扑量子计算", "part_of", 3),
        ("Kitaev链", "一维拓扑超导", "describes", 3),
        
        # Rydberg
        ("里德伯态", "中性原子量子比特", "enables", 5),
        ("里德伯阻塞", "里德伯态", "from", 4),
        ("里德伯阻塞", "中性原子量子比特", "enables", 4),
        
        # Optical tweezer
        ("光学镊子", "中性原子量子比特", "traps", 5),
        ("光学镊子", "QuEra Computing", "uses", 4),
        ("光学镊子", "Pasqal", "uses", 3),
        
        # Flux/Charge qubits
        ("磁通量子比特", "超导量子比特", "is_type_of", 4),
        ("磁通量子比特", "Transmon", "competes_with", 3),
        ("电荷量子比特", "超导量子比特", "is_type_of", 4),
        ("电荷量子比特", "库珀对", "uses", 3),
        
        # Silicon photonics
        ("硅光子", "PsiQuantum", "uses", 4),
        ("硅光子", "光量子计算", "enables", 4),
        
        # Quantum repeater
        ("量子中继器", "量子网络", "enables", 5),
        ("量子中继器", "量子存储器", "uses", 4),
        ("量子中继器", "量子互联网", "part_of", 4),
        
        # XEB
        ("交叉熵基准测试", "量子优越性", "measures", 5),
        ("交叉熵基准测试", "量子基准测试", "part_of", 4),
        ("线性交叉熵基准测试", "交叉熵基准测试", "is_type_of", 3),
        ("交叉熵基准测试", "谷歌", "used_by", 4),
        ("交叉熵基准测试", "Sycamore处理器", "used_on", 4),
        
        # ADAPT-VQE / QSE
        ("量子子空间展开", "VQE", "improves", 3),
        ("自适应VQE", "VQE", "improves", 3),
        ("自适应VQE", "量子化学模拟", "enables", 3),
        
        # VQC
        ("变分量子电路", "VQE", "uses", 4),
        ("变分量子电路", "QAOA", "related_to", 3),
        ("变分量子电路", "NISQ", "runs_on", 4),
        
        # QNN
        ("量子神经网络", "量子机器学习", "is_type_of", 3),
        ("量子神经网络", "变分量子电路", "uses", 3),
        
        # Hamiltonian
        ("哈密顿量", "薛定谔方程", "solves", 5),
        ("哈密顿量", "量子模拟", "central_to", 5),
        ("海森堡模型", "哈密顿量", "is_type_of", 4),
        ("海森堡模型", "量子模拟", "applies_to", 4),
        
        # Tensor networks
        ("张量网络", "量子模拟", "enables", 4),
        ("张量网络", "多体物理", "applies_to", 3),
        
        # Companies
        ("D-Wave", "量子退火算法", "develops", 5),
        ("D-Wave", "量子优化", "leads", 4),
        ("Rigetti Computing", "超导量子比特", "uses", 4),
        ("Rigetti Computing", "量子云服务", "provides", 3),
        ("Xanadu", "光量子计算", "develops", 4),
        ("Xanadu", "PennyLane", "develops", 5),
        
        # Countries
        ("中国", "中科院", "has", 4),
        ("中国", "相干科技", "has", 4),
        ("美国", "谷歌", "has", 4),
        ("美国", "IBM", "has", 4),
        ("美国", "微软", "has", 3),
        ("欧盟", "IQM Quantum", "has", 3),
        ("欧盟", "Pasqal", "has", 3),
        ("EuroHPC", "欧盟", "part_of", 3),
        ("量子旗舰", "欧盟", "part_of", 3),
        
        # NISQ/NISQ era
        ("NISQ", "量子计算", "era_of", 5),
        ("NISQ", "VQE", "era_for", 4),
        ("NISQ", "QAOA", "era_for", 4),
        ("NISQ时代", "NISQ", "is", 5),
        
        # Cooper pair
        ("库珀对", "约瑟夫森结", "carried_by", 4),
        ("库珀对", "超导量子比特", "carries", 4),
        
        # Quantum Volume / RB
        ("量子体积", "IBM", "proposed_by", 4),
        ("随机基准测试", "门保真度", "measures", 4),
        ("随机基准测试", "量子基准测试", "part_of", 4),
        
        # Quantum logic gate / Pauli / Bloch
        ("量子逻辑门", "量子门", "is", 5),
        ("量子逻辑门", "量子电路", "builds", 4),
        ("泡利矩阵", "量子门", "basis_for", 4),
        ("Bloch球", "量子比特", "visualizes", 4),
        
        # More cross-links
        ("Hadamard门", "泡利矩阵", "related_to", 3),
        ("CNOT门", "超导量子比特", "implements_on", 4),
        ("T门", "量子纠错", "requires", 4),
        ("S门", "超导量子比特", "implements_on", 3),
        ("T门", "Hadamard门", "related_to", 3),
        ("S门", "相位门", "is_type_of", 3),
        
        # Reports - connect to years
        ("2026全球量子计算产业发展展望", "2025年全球量子产业", "updates", 3),
        ("2025全球量子计算产业发展展望", "量子产业报告", "is_a", 3),
        ("2024-2025年度CQCC量子计算产业报告", "量子产业报告", "is_a", 3),
        
        # Connect "量子退火" to "量子优化"
        ("量子退火算法", "量子优化", "solves", 5),
        ("量子退火算法", "D-Wave", "developed_by", 5),
        
        # More "量子模拟" links
        ("量子模拟", "哈密顿量", "simulates", 5),
        ("量子模拟", "海森堡模型", "applies_to", 3),
        ("量子模拟", "张量网络", "uses", 3),
        
        # Canoncial papers
        ("Shor1994", "Shor算法", "authored", 5),
        ("Feynman1982", "量子模拟", "proposed", 5),
        
        # Connect "离子阱" to "Quantinuum" specifically
        ("离子阱量子比特", "Quantinuum", "used_by", 4),
        ("离子阱量子比特", "霍尼韦尔", "used_by", 3),
        
        # "量子精密测量" to sensors
        ("量子精密测量", "NV色心", "uses", 4),
        ("量子精密测量", "里德伯态", "uses", 3),
        ("量子精密测量", "原子钟", "improves", 3),
        
        # "超导配对关联" to specific experiment
        ("超导配对关联", "Quantinuum Helios", "observed_on", 4),
        ("超导配对关联", "超导", "related_to", 3),
    ]
    
    for src, tgt, rel, w in new_edges:
        safe_add(src, tgt, rel, w)
    
    # Add "原子钟" as node if it wasn't already added
    clock_id = add_node(nodes, "原子钟 (Atomic Clock)", "application", 
                    "利用量子精密测量实现的超高精度时间基准，基于原子的量子跃迁", 3,
                    ["7408677623443647"], ["量子精密测量"], ["原子干涉"])
    safe_add("量子精密测量", "原子钟", "enables", 3)
    safe_add("原子钟", "NV色心", "uses", 2)
    
    # ============================================================
    # Final dense cross-linking pass
    # ============================================================
    
    final_edges = [
        # "量子计算" core links (ensure all concepts connect to core)
        ("量子计算", "量子比特", "uses", 5),
        ("量子计算", "量子电路", "uses", 5),
        ("量子计算", "量子算法", "uses", 5),
        ("量子计算", "量子编程", "uses", 4),
        ("量子计算", "NISQ", "era_of", 5),
        ("量子计算", "量子优势", "enables", 5),

        # "超导量子比特" dense links
        ("超导量子比特", "量子逻辑门", "executes", 4),
        ("超导量子比特", "Bloch球", "represents", 3),

        # Ensure all companies link to "量子计算产业化"
        ("相干科技", "量子计算产业化", "drives", 4),
        ("本源量子", "量子计算产业化", "drives", 3),
        ("Rigetti Computing", "量子计算产业化", "drives", 3),
        ("D-Wave", "量子计算产业化", "drives", 3),
        ("Xanadu", "量子计算产业化", "drives", 3),

        # All qubit types to "量子比特体系"
        ("磁通量子比特", "量子比特体系", "part_of", 3),
        ("电荷量子比特", "量子比特体系", "part_of", 3),
        ("拓扑量子计算", "量子比特体系", "alternative_in", 3),

        # Protocol dense links
        ("随机基准测试", "交叉熵基准测试", "compared_to", 3),
        ("量子性能分级标准", "随机基准测试", "includes", 3),

        # "哈密顿量" dense
        ("哈密顿量", "变分量子本征求解器", "solved_by", 4),

        # Reports to "量子产业报告"
        ("量子计算：掌握未来", "量子产业报告", "is_a", 3),
        ("量子黎明：全球霸权竞赛", "量子产业报告", "is_a", 3),

        # "Quantum Dawn" etc
        ("Quantum_Dawn_Global_Strategy", "量子产业报告", "is_a", 3),
        ("Quantum_Computing_Tipping_Point", "量子产业报告", "is_a", 3),
    ]
    
    for src, tgt, rel, w in final_edges:
        safe_add(src, tgt, rel, w)
    
    # ============================================================
    # Statistics
    # ============================================================
    
    print(f"Final: {len(nodes)} nodes, {len(edges)} edges")
    
    type_counts = {}
    for n in nodes:
        t = n['type']
        type_counts[t] = type_counts.get(t, 0) + 1
    print("\nNode types:")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")
    
    edge_type_counts = {}
    for e in edges:
        t = e.get('label', 'unknown')
        edge_type_counts[t] = edge_type_counts.get(t, 0) + 1
    print(f"\nEdge types (top 20):")
    for t, c in sorted(edge_type_counts.items(), key=lambda x: -x[1])[:20]:
        print(f"  {t}: {c}")
    
    data['metadata']['node_count'] = len(nodes)
    data['metadata']['edge_count'] = len(edges)
    data['metadata']['last_updated'] = '2026-06-13'
    save_graph(data)
    print(f"\nSaved to {GRAPH_FILE}")

if __name__ == '__main__':
    main()
