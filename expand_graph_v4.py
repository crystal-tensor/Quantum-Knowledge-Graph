#!/usr/bin/env python3
"""
Phase 3: Dense cross-linking to boost edge count to 800+
Focus on creating rich interconnections between existing nodes
"""

import json
import os

WORKSPACE = "/Users/danielcrystal/WorkBuddy/2026-06-13-17-30-18"
GRAPH_FILE = os.path.join(WORKSPACE, "graph_data.json")

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
    
    # Build label->id map
    label_to_id = {}
    for n in nodes:
        label_to_id[n['label']] = n['id']
        # Also add simplified versions for matching
        simplified = n['label'].split(' (')[0].split(' - ')[0].strip()
        if simplified not in label_to_id:
            label_to_id[simplified] = n['id']
    
    def safe_add_edge(src_label, tgt_label, rel, weight=1.0):
        src_id = label_to_id.get(src_label)
        tgt_id = label_to_id.get(tgt_label)
        if not src_id:
            # Try partial match
            for n in nodes:
                if src_label in n['label']:
                    src_id = n['id']
                    break
        if not tgt_id:
            for n in nodes:
                if tgt_label in n['label']:
                    tgt_id = n['id']
                    break
        if src_id and tgt_id:
            add_edge(edges, src_id, tgt_id, rel, weight)
    
    # ============================================================
    # Comprehensive cross-linking
    # ============================================================
    
    # 1. Company-technology platform relationships (comprehensive)
    company_tech = [
        ("IBM", "量子体积", "developed_by", 4),
        ("IBM", "Qiskit", "developed_by", 5),
        ("IBM", "IBM Eagle处理器", "developed_by", 5),
        ("IBM", "IBM Condor处理器", "developed_by", 5),
        ("IBM", "IBM Heron处理器", "developed_by", 5),
        ("IBM", "量子云平台", "developed_by", 3),
        ("谷歌", "Cirq", "developed_by", 4),
        ("谷歌", "Sycamore处理器", "developed_by", 5),
        ("谷歌", "Willow", "developed_by", 5),
        ("谷歌", "量子优越性", "enables", 5),
        ("微软", "拓扑量子计算", "researches", 4),
        ("微软", "马约拉纳零模", "researches", 3),
        ("英伟达", "量子机器学习", "enables", 3),
        ("英伟达", "量子-经典混合框架", "enables", 3),
        ("霍尼韦尔", "Quantinuum", "developed_by", 4),
        ("中科大", "九章光量子计算机", "developed_by", 5),
        ("中科大", "祖冲之三号", "developed_by", 5),
        ("中科大", "量子通信", "researches", 4),
        ("中科大", "量子密钥分发", "researches", 4),
        ("中科大", "光量子计算", "researches", 4),
        ("北京量子信息科学研究院", "超导量子比特", "researches", 5),
        ("北京量子信息科学研究院", "量子计算产业化", "researches", 4),
        ("本源量子", "超导量子比特", "uses", 4),
        ("本源量子", "量子计算与编程入门", "developed_by", 4),
        ("本源量子", "量子编程", "enables", 4),
        ("国仪量子", "量子传感", "enables", 4),
        ("国仪量子", "NV色心", "uses", 3),
    ]
    
    for src, tgt, rel, w in company_tech:
        safe_add_edge(src, tgt, rel, w)
    
    # 2. Core quantum concepts dense web
    concept_web = [
        # Quantum computing fundamentals
        ("量子比特", "叠加态", "uses", 5),
        ("量子比特", "量子纠缠", "uses", 5),
        ("量子比特", "量子门", "uses", 5),
        ("量子比特", "量子测量", "uses", 5),
        ("叠加态", "波函数坍缩", "related_to", 5),
        ("量子纠缠", "Bell态", "enables", 5),
        ("量子纠缠", "EPR对", "enables", 5),
        ("量子纠缠", "量子隐形传态", "enables", 5),
        ("量子纠缠", "量子密钥分发", "enables", 5),
        ("量子测量", "波函数坍缩", "related_to", 5),
        ("量子测量", "量子态层析", "uses", 4),
        ("量子门", "CNOT门", "uses", 5),
        ("量子门", "Hadamard门", "uses", 5),
        ("量子门", "通用门集", "part_of", 4),
        ("量子门", "门保真度", "determines", 4),
        ("量子电路", "量子门", "uses", 5),
        ("量子电路", "量子算法", "implements", 4),
        ("量子电路", "变分量子电路", "part_of", 3),
        ("量子算法", "Shor算法", "part_of", 5),
        ("量子算法", "Grover搜索算法", "part_of", 5),
        ("量子算法", "VQE", "part_of", 5),
        ("量子算法", "QAOA", "part_of", 5),
        ("量子算法", "量子傅里叶变换", "uses", 4),
        ("量子算法", "量子相位估计", "uses", 4),
        ("量子算法", "量子随机行走", "uses", 3),
        ("量子算法", "量子退火算法", "part_of", 4),
        
        # Error correction web
        ("量子纠错", "表面码", "uses", 5),
        ("量子纠错", "逻辑量子比特", "enables", 5),
        ("量子纠错", "量子纠错阈值定理", "related_to", 5),
        ("量子纠错", "容错量子计算", "enables", 5),
        ("量子纠错", "量子噪声", "addresses", 5),
        ("量子纠错", "退相干", "addresses", 5),
        
        # Physical qubit platforms web
        ("超导量子比特", "约瑟夫森结", "uses", 5),
        ("超导量子比特", "稀释制冷机", "uses", 5),
        ("超导量子比特", "Transmon", "is_type_of", 5),
        ("超导量子比特", "Circuit QED", "uses", 5),
        ("超导量子比特", "量子比特操控", "uses", 4),
        ("超导量子比特", "量子比特读取", "uses", 4),
        ("超导量子比特", "低温CMOS", "uses", 3),
        ("离子阱量子比特", "Quantinuum", "uses", 4),
        ("离子阱量子比特", "因斯布鲁克大学", "researches", 3),
        ("离子阱量子比特", "激光冷却", "uses", 3),
        ("中性原子量子比特", "光学镊子", "uses", 3),
        ("中性原子量子比特", "中性原子分区架构", "uses", 3),
        ("中性原子量子比特", "QuEra Computing", "uses", 4),
        ("中性原子量子比特", "Pasqal", "uses", 4),
        ("硅基量子比特", "量子点", "uses", 4),
        ("硅基量子比特", "自旋量子比特", "is_type_of", 4),
        ("硅基量子比特", "西岭芯片", "uses", 3),
        ("光量子计算", "PsiQuantum", "uses", 4),
        ("光量子计算", "九章光量子计算机", "uses", 5),
        ("拓扑量子计算", "任意子", "uses", 5),
        ("拓扑量子计算", "马约拉纳零模", "uses", 4),
        ("拓扑量子计算", "拓扑绝缘体", "uses", 3),
        ("拓扑量子计算", "微软", "researches", 4),
        
        # Application domains web
        ("量子化学模拟", "VQE", "uses", 5),
        ("量子化学模拟", "量子模拟", "uses", 4),
        ("量子化学模拟", "量子药物发现", "enables", 4),
        ("量子药物发现", "混合量子药物发现管线", "uses", 4),
        ("量子药物发现", "QureGenAI", "developed_by", 3),
        ("量子金融", "量子组合优化", "uses", 4),
        ("量子金融", "QAOA", "uses", 3),
        ("量子金融", "量子优化", "uses", 3),
        ("量子机器学习", "PennyLane", "uses", 4),
        ("量子机器学习", "变分量子电路", "uses", 4),
        ("量子机器学习", "量子深度学习", "part_of", 4),
        ("量子优化", "量子退火算法", "uses", 3),
        ("量子优化", "量子组合优化", "part_of", 4),
        ("量子传感", "量子精密测量", "enables", 4),
        ("量子传感", "NV色心", "uses", 3),
        ("量子密码学", "后量子密码学", "related_to", 4),
        ("量子密码学", "Shor算法", "addresses", 4),
        ("量子密码学", "量子密钥分发", "uses", 5),
        
        # Theory foundations web
        ("量子力学", "薛定谔方程", "part_of", 5),
        ("量子力学", "海森堡不确定性原理", "part_of", 5),
        ("量子力学", "波粒二象性", "part_of", 5),
        ("量子力学", "普朗克常数", "part_of", 4),
        ("量子力学", "量子隧穿效应", "part_of", 4),
        ("量子力学", "玻尔量子论", "derives_from", 3),
        ("量子力学", "德布罗意波", "part_of", 4),
        ("量子力学", "量子计算", "enables", 5),
        ("量子力学", "密度矩阵", "uses", 4),
        
        # Scaling challenges
        ("量子计算", "退相干", "challenged_by", 5),
        ("量子计算", "量子噪声", "challenged_by", 5),
        ("量子计算", "量子纠错", "addresses", 5),
        ("量子计算", "NISQ时代", "part_of", 3),
        ("量子计算", "量子优势", "enables", 4),
        ("量子计算", "量子计算产业化", "enables", 4),
        ("量子计算", "量子比特", "uses", 5),
        ("量子计算", "量子门", "uses", 5),
        ("量子计算", "量子电路", "uses", 5),
        ("量子计算", "量子算法", "uses", 5),
        ("量子计算", "量子编程", "uses", 4),
        ("量子计算", "量子测量", "uses", 5),
        ("量子计算", "量子比特体系", "uses", 4),
        
        # Programming tools chain
        ("量子编程", "Qiskit", "uses", 5),
        ("量子编程", "Cirq", "uses", 4),
        ("量子编程", "PennyLane", "uses", 3),
        ("量子编程", "本源量子云平台", "uses", 3),
        ("量子编程", "量子电路", "uses", 5),
        ("量子编程", "量子算法", "implements", 5),
        
        # Communication chain
        ("量子通信", "量子密钥分发", "uses", 5),
        ("量子通信", "量子网络", "uses", 4),
        ("量子通信", "量子中继器", "uses", 4),
        ("量子通信", "量子互联网", "enables", 4),
        ("量子通信", "量子隐形传态", "uses", 4),
        ("量子通信", "量子不可克隆定理", "related_to", 4),
        
        # Hardware-platform dense links
        ("超导量子比特", "量子计算", "implements", 5),
        ("离子阱量子比特", "量子计算", "implements", 5),
        ("中性原子量子比特", "量子计算", "implements", 4),
        ("光量子计算", "量子计算", "implements", 4),
        ("硅基量子比特", "量子计算", "implements", 3),
        ("拓扑量子计算", "量子计算", "implements", 3),
        ("量子退火算法", "D-Wave", "uses", 5),
        
        # People-concept dense
        ("金贻荣", "量子工程学", "developed_by", 5),
        ("金贻荣", "超导量子比特", "researches", 5),
        ("金贻荣", "Circuit QED", "researches", 4),
        ("金贻荣", "量子比特读取", "researches", 4),
        ("金贻荣", "量子比特操控", "researches", 4),
        ("郭光灿", "量子光学", "researches", 5),
        ("郭光灿", "量子通信", "researches", 4),
        ("郭光灿", "量子信息", "researches", 5),
        
        # DiVincenzo criteria to all platforms
        ("迪文森佐准则", "超导量子比特", "applies_to", 4),
        ("迪文森佐准则", "离子阱量子比特", "applies_to", 4),
        ("迪文森佐准则", "中性原子量子比特", "applies_to", 3),
        ("迪文森佐准则", "硅基量子比特", "applies_to", 3),
        ("迪文森佐准则", "拓扑量子计算", "applies_to", 3),
        
        # Quantum computing competitive landscape
        ("超导量子比特", "离子阱量子比特", "competes_with", 4),
        ("超导量子比特", "中性原子量子比特", "competes_with", 3),
        ("超导量子比特", "光量子计算", "competes_with", 3),
        ("离子阱量子比特", "中性原子量子比特", "competes_with", 3),
        ("IBM", "谷歌", "competes_with", 5),
        ("IBM", "微软", "competes_with", 4),
        ("相干科技", "本源量子", "competes_with", 3),
        ("Quantinuum", "QuEra Computing", "competes_with", 3),
        ("PsiQuantum", "九章光量子计算机", "competes_with", 2),
        
        # Benchmark and standard links
        ("量子体积", "量子性能分级标准", "part_of", 4),
        ("量子体积", "门保真度", "related_to", 3),
        ("量子体积", "相干时间", "related_to", 3),
        ("量子性能分级标准", "量子基准测试", "part_of", 4),
        ("量子基准测试", "量子计算产业化", "enables", 3),
        
        # Quantum internet chain
        ("量子互联网", "量子中继器", "uses", 4),
        ("量子互联网", "量子存储器", "uses", 4),
        ("量子互联网", "量子网络", "uses", 4),
        ("量子互联网", "代尔夫特理工大学", "researches", 3),
        
        # Industry chain
        ("量子计算产业化", "量子云平台", "enables", 4),
        ("量子计算产业化", "量子编程", "enables", 4),
        ("量子计算产业化", "量子软件", "enables", 3),
        ("量子计算产业化", "量子芯片", "enables", 4),
        ("量子计算产业化", "量子优势", "related_to", 4),
        ("量子计算产业化", "容错量子计算", "enables", 5),
        
        # Key reports as knowledge base links
        ("光子盒研究院", "2026全球量子计算产业发展展望", "developed_by", 4),
        ("CQCC", "2024-2025年度CQCC量子计算产业报告", "developed_by", 4),
        ("中关村量子产业联盟", "量子计算：掌握未来", "developed_by", 4),
        
        # T1/T2 specific platform links
        ("T1弛豫时间", "超导量子比特", "determines", 4),
        ("T2退相干时间", "超导量子比特", "determines", 4),
        ("T1弛豫时间", "离子阱量子比特", "determines", 3),
        ("T2退相干时间", "离子阱量子比特", "determines", 3),
        
        # Quantum chip fabrication
        ("量子芯片", "量子比特制备", "uses", 4),
        ("量子芯片", "良品率", "determines", 3),
        ("量子芯片", "量子比特串扰", "related_to", 3),
        
        # Quantum simulation applications
        ("量子模拟", "超导配对关联", "enables", 3),
        ("量子模拟", "量子材料科学", "enables", 4),
        ("量子模拟", "量子化学模拟", "enables", 5),
        
        # Quantum deep learning chain
        ("量子深度学习", "变分量子电路", "uses", 4),
        ("量子深度学习", "PennyLane", "uses", 3),
        ("量子深度学习", "量子机器学习", "part_of", 4),
        
        # Error correction strategies
        ("表面码", "超导量子比特", "applies_to", 5),
        ("表面码", "逻辑量子比特", "enables", 5),
        ("逻辑量子比特", "容错量子计算", "enables", 5),
        ("量子纠错码", "表面码", "part_of", 4),
        ("量子纠错码", "量子纠错", "part_of", 5),
        
        # More institution links
        ("芝加哥大学", "量子信息", "researches", 3),
        ("MIT", "超导量子比特", "researches", 4),
        ("Stanford University", "量子传感", "researches", 3),
        ("代尔夫特理工大学", "超导量子比特", "researches", 3),
        
        # Quantum bus and resonator links
        ("量子总线", "谐振腔", "uses", 5),
        ("量子总线", "超导量子比特", "uses", 4),
        ("量子总线", "Circuit QED", "part_of", 4),
        ("Circuit QED", "量子比特操控", "enables", 4),
        ("Circuit QED", "量子比特读取", "enables", 4),
        ("Circuit QED", "腔量子电动力学", "derives_from", 5),
        
        # Hybrid quantum-classical links
        ("量子-经典混合框架", "NISQ时代", "enables", 4),
        ("量子-经典混合框架", "VQE", "uses", 4),
        ("量子-经典混合框架", "QAOA", "uses", 4),
        ("量子-经典混合框架", "量子-经典单片全集成", "derives_from", 3),
        
        # Quantum advantage demonstrations
        ("量子优越性", "Sycamore处理器", "enables", 5),
        ("量子优势", "Willow", "enables", 5),
        ("量子优势", "祖冲之三号", "enables", 4),
        ("量子优势", "九章光量子计算机", "enables", 5),
        ("量子优势", "量子计算产业化", "enables", 4),
        
        # Country/region strategy links
        ("谷歌", "美国量子战略", "part_of", 3),
        ("IBM", "美国量子战略", "part_of", 3),
        ("微软", "美国量子战略", "part_of", 3),
        ("相干科技", "中国量子战略", "part_of", 3),
        ("本源量子", "中国量子战略", "part_of", 3),
        ("中科大", "中国量子战略", "part_of", 3),
        ("IQM Quantum", "欧洲量子战略", "part_of", 2),
        ("Pasqal", "欧洲量子战略", "part_of", 2),
        ("Oxford Quantum Circuits", "欧洲量子战略", "part_of", 2),
    ]
    
    for src, tgt, rel, w in concept_web:
        safe_add_edge(src, tgt, rel, w)
    
    # Update metadata
    data['metadata']['node_count'] = len(nodes)
    data['metadata']['edge_count'] = len(edges)
    data['metadata']['last_updated'] = '2026-06-13'
    data['metadata']['expansion_notes'] = 'Phase 3: 密集交叉链接，目标800+边'
    
    save_graph(data)
    print(f"Final: {len(nodes)} nodes, {len(edges)} edges")
    
    # Stats
    type_counts = {}
    for n in nodes:
        t = n['type']
        type_counts[t] = type_counts.get(t, 0) + 1
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

if __name__ == '__main__':
    main()
