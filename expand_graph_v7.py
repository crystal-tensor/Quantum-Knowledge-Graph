#!/usr/bin/env python3
"""
Phase 6: Final push to 800+ edges
Add every remaining meaningful relationship
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
    edges.append({"source": source, "target": target, "label": rel_type, "weight": float(weight)})

def main():
    data = load_graph()
    nodes = data['nodes']
    edges = data['edges']
    
    print(f"Starting: {len(nodes)} nodes, {len(edges)} edges")
    
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
    
    # Systematic linking: each company → its main tech platform
    company_tech = [
        # Chinese companies
        ("相干科技", "超导量子比特", "uses", 5),
        ("相干科技", "金贻荣", "led_by", 5),
        ("相干科技", "北京量子信息科学研究院", "spun_off_from", 5),
        ("相干科技", "Willow", "competes_with", 3),
        ("相干科技", "超导量子比特", "uses", 5),
        ("相干科技", "金贻荣", "led_by", 4),
        ("相干科技", "北京量子信息科学研究院", "spun_off_from", 5),
        ("中微达信", "低温CMOS", "develops", 5),
        ("中微达信", "蜀山系列芯片", "develops", 5),
        ("国仪量子", "量子精密测量", "develops", 5),
        ("国仪量子", "NV色心", "uses", 4),
        ("本源量子", "超导量子比特", "uses", 4),
        ("本源量子", "郭国平", "led_by", 5),
        ("本源量子", "本源量子云平台", "develops", 5),
        ("瀚海凌潮", "量子云平台", "develops", 3),
        ("QureGenAI", "量子化学模拟", "develops", 3),
        ("QureGenAI", "量子药物发现", "applies", 4),
        
        # International companies
        ("谷歌", "超导量子比特", "uses", 5),
        ("谷歌", "Sycamore处理器", "develops", 5),
        ("谷歌", "Willow", "develops", 5),
        ("谷歌", "Cirq", "develops", 4),
        ("IBM", "超导量子比特", "uses", 5),
        ("IBM", "量子体积", "proposes", 4),
        ("IBM", "Qiskit", "develops", 5),
        ("微软", "拓扑量子计算", "researches", 5),
        ("微软", "马约拉纳零模", "researches", 4),
        ("英伟达", "NVentures", "has", 4),
        ("英伟达", "量子-经典混合框架", "enables", 4),
        ("霍尼韦尔", "Quantinuum", "founded", 4),
        ("Quantinuum", "Quantinuum Helios", "develops", 5),
        ("D-Wave", "量子退火算法", "develops", 5),
        ("Rigetti Computing", "超导量子比特", "uses", 4),
        ("Xanadu", "PennyLane", "develops", 5),
        ("Xanadu", "光量子计算", "uses", 4),
        ("PsiQuantum", "光量子计算", "uses", 5),
        ("PsiQuantum", "硅光子", "uses", 4),
        ("Atom Computing", "中性原子量子比特", "uses", 5),
        ("QuEra Computing", "中性原子量子比特", "uses", 5),
        ("Pasqal", "中性原子量子比特", "uses", 5),
        ("IQM Quantum", "超导量子比特", "uses", 5),
        ("Quantum Motion", "硅基量子比特", "uses", 5),
        ("Oxford Quantum Circuits", "超导量子比特", "uses", 5),
    ]
    
    for src, tgt, rel, w in company_tech:
        safe_add(src, tgt, rel, w)
    
    # Systematic linking: each person → their expertise
    person_expertise = [
        ("金贻荣", "超导量子比特", "specializes_in", 5),
        ("金贻荣", "Circuit QED", "specializes_in", 4),
        ("金贻荣", "量子比特读取", "specializes_in", 4),
        ("金贻荣", "量子比特操控", "specializes_in", 4),
        ("金贻荣", "量子工程学", "translates", 4),
        ("郭国平", "量子编程", "specializes_in", 5),
        ("郭国平", "量子计算与编程入门", "authors", 4),
        ("郭光灿", "量子光学", "specializes_in", 5),
        ("郭光灿", "量子信息", "pioneers", 5),
        ("郭光灿", "量子通信", "researches", 4),
        ("陈昭昀", "量子编程", "specializes_in", 3),
        ("Alexandre Blais", "Circuit QED", "pioneers", 5),
        ("Alexandre Blais", "腔量子电动力学", "extends", 4),
        ("David D. Awschalom", "量子传感", "specializes_in", 4),
        ("David D. Awschalom", "量子信息硬件", "reviews", 4),
        ("William D. Oliver", "超导量子比特", "specializes_in", 4),
        ("William D. Oliver", "量子纠错", "researches", 3),
        ("A.M. Zagoskin", "量子工程学", "authors", 4),
        ("苏汝铿", "量子力学", "teaches", 3),
        ("龙沛洵", "量子计算原理", "teaches", 2),
    ]
    
    for src, tgt, rel, w in person_expertise:
        safe_add(src, tgt, rel, w)
    
    # Algorithm → concept → application chain (complete)
    algo_chains = [
        ("Shor算法", "整数分解", "solves", 5),
        ("Shor算法", "RSA加密", "threatens", 5),
        ("Shor算法", "后量子密码学", "motivates", 5),
        ("Grover搜索算法", "数据库搜索", "solves", 4),
        ("Grover搜索算法", "二次加速", "achieves", 5),
        ("量子傅里叶变换", "Shor算法", "enables", 5),
        ("量子傅里叶变换", "周期发现", "solves", 4),
        ("量子相位估计", "本征值问题", "solves", 5),
        ("量子相位估计", "量子化学模拟", "enables", 4),
        ("VQE", "分子基态能量", "solves", 5),
        ("VQE", "变分量子电路", "uses", 5),
        ("QAOA", "组合优化", "solves", 5),
        ("QAOA", "变分量子电路", "uses", 4),
        ("量子退火算法", "Ising模型", "solves", 4),
        ("量子退火算法", "量子优化", "implements", 5),
        ("量子蒙特卡洛", "量子多体系统", "solves", 3),
        ("量子神经网络", "模式识别", "solves", 3),
        ("量子随机行走", "搜索加速", "enables", 3),
    ]
    
    for src, tgt, rel, w in algo_chains:
        safe_add(src, tgt, rel, w)
    
    # Application → real-world use case
    app_uses = [
        ("量子化学模拟", "新药设计", "enables", 4),
        ("量子化学模拟", "催化剂优化", "enables", 3),
        ("量子化学模拟", "材料合成", "enables", 3),
        ("量子金融", "投资组合优化", "solves", 4),
        ("量子金融", "风险分析", "solves", 3),
        ("量子金融", "期权定价", "solves", 3),
        ("量子机器学习", "分类问题", "solves", 3),
        ("量子机器学习", "生成模型", "uses", 3),
        ("量子优化", "物流调度", "solves", 3),
        ("量子优化", "网络优化", "solves", 3),
        ("量子密码学", "安全通信", "enables", 5),
        ("量子传感", "磁场测量", "enables", 3),
        ("量子传感", "重力测量", "enables", 3),
        ("量子精密测量", "导航定位", "enables", 3),
        ("量子精密测量", "医学成像", "enables", 3),
    ]
    
    for src, tgt, rel, w in app_uses:
        safe_add(src, tgt, rel, w)
    
    # Hardware → detailed spec links
    hw_specs = [
        ("Sycamore处理器", "53比特", "has", 5),
        ("Willow", "105比特", "has", 5),
        ("IBM Eagle处理器", "127比特", "has", 5),
        ("IBM Condor处理器", "433比特", "has", 5),
        ("祖冲之三号", "105比特", "has", 5),
        ("九章光量子计算机", "76光子", "has", 5),
        ("Transmon", "约瑟夫森结", "built_from", 5),
        ("Transmon", "电荷量子比特", "improves_on", 4),
    ]
    
    for src, tgt, rel, w in hw_specs:
        safe_add(src, tgt, rel, w)
    
    # Concept → prerequisite concept (knowledge chain)
    prereqs = [
        ("量子计算", "线性代数", "requires", 3),
        ("量子计算", "概率论", "requires", 3),
        ("量子算法", "量子门", "requires", 5),
        ("量子算法", "量子电路", "requires", 5),
        ("量子纠错", "量子门", "requires", 5),
        ("量子纠错", "量子测量", "requires", 4),
        ("Circuit QED", "量子电动力学", "built_on", 5),
        ("Circuit QED", "超导量子比特", "uses", 5),
        ("表面码", "二维量子比特阵列", "requires", 4),
        ("拓扑量子计算", "拓扑学", "requires", 3),
        ("拓扑量子计算", "量子场论", "requires", 3),
        ("VQE", "变分法", "requires", 3),
        ("QAOA", "组合优化", "requires", 3),
        ("量子机器学习", "机器学习", "requires", 3),
        ("量子机器学习", "量子电路", "requires", 4),
        ("量子密钥分发", "量子不可克隆定理", "relies_on", 5),
        ("量子密钥分发", "BB84协议", "implements", 5),
    ]
    
    for src, tgt, rel, w in prereqs:
        safe_add(src, tgt, rel, w)
    
    # Platform-specific details
    platform_details = [
        ("超导量子比特", "微秒级相干时间", "has", 3),
        ("超导量子比特", "高门保真度", "has", 3),
        ("超导量子比特", "快速门操作", "has", 3),
        ("离子阱量子比特", "秒级相干时间", "has", 3),
        ("离子阱量子比特", "全连接", "has", 3),
        ("离子阱量子比特", "慢门操作", "has", 3),
        ("中性原子量子比特", "可扩展", "has", 3),
        ("中性原子量子比特", "里德伯阻塞", "uses", 4),
        ("光量子计算", "室温运行", "has", 3),
        ("光量子计算", "难以存储", "limitation", 3),
        ("硅基量子比特", "CMOS兼容", "has", 3),
        ("硅基量子比特", "长相干时间", "has", 3),
    ]
    
    for src, tgt, rel, w in platform_details:
        safe_add(src, tgt, rel, w)
    
    # Organization → research focus
    org_research = [
        ("北京量子信息科学研究院", "超导量子比特", "focuses_on", 5),
        ("北京量子信息科学研究院", "量子计算产业化", "focuses_on", 4),
        ("MIT", "量子纠错", "focuses_on", 4),
        ("MIT", "容错量子计算", "focuses_on", 4),
        ("芝加哥大学", "量子传感", "focuses_on", 4),
        ("芝加哥大学", "量子网络", "focuses_on", 3),
        ("代尔夫特理工大学", "量子互联网", "focuses_on", 5),
        ("代尔夫特理工大学", "超导量子比特", "focuses_on", 4),
        ("因斯布鲁克大学", "离子阱量子比特", "focuses_on", 5),
        ("斯坦福大学", "量子光学", "focuses_on", 3),
    ]
    
    for src, tgt, rel, w in org_research:
        safe_add(src, tgt, rel, w)
    
    # Remaining concept cross-links
    remaining = [
        ("量子噪声", "NISQ时代", "defines", 4),
        ("NISQ时代", "VQE", "best_algorithm", 5),
        ("NISQ时代", "QAOA", "best_algorithm", 5),
        ("容错量子计算", "量子计算产业化", "enables", 5),
        ("容错量子计算", "逻辑量子比特", "uses", 5),
        ("容错量子计算", "量子纠错阈值定理", "relies_on", 5),
        ("量子计算产业化", "量子云平台", "requires", 4),
        ("量子计算产业化", "量子软件", "requires", 4),
        ("量子计算产业化", "量子芯片", "requires", 4),
        ("量子互联网", "量子中继器", "requires", 4),
        ("量子互联网", "量子存储器", "requires", 4),
        ("量子网络", "量子纠缠", "uses", 4),
        ("量子密钥分发", "量子纠缠", "uses", 4),
        ("BB84协议", "量子密钥分发", "implements", 5),
        ("量子比特操控", "CNOT门", "uses", 4),
        ("量子比特操控", "Hadamard门", "uses", 4),
        ("量子比特操控", "门保真度", "measures", 4),
        ("量子比特读取", "读取保真度", "measures", 4),
        ("量子比特读取", "频分复用读取", "uses", 4),
        ("量子比特读取", "参量放大器", "uses", 4),
    ]
    
    for src, tgt, rel, w in remaining:
        safe_add(src, tgt, rel, w)
    
    # Update metadata
    data['metadata']['node_count'] = len(nodes)
    data['metadata']['edge_count'] = len(edges)
    data['metadata']['last_updated'] = '2026-06-13'
    save_graph(data)
    
    print(f"Final: {len(nodes)} nodes, {len(edges)} edges")
    
    # Edge type distribution
    edge_type_counts = {}
    for e in edges:
        t = e.get('label', 'unknown')
        edge_type_counts[t] = edge_type_counts.get(t, 0) + 1
    print(f"\nEdge types ({len(edge_type_counts)} unique):")
    for t, c in sorted(edge_type_counts.items(), key=lambda x: -x[1])[:25]:
        print(f"  {t}: {c}")

if __name__ == '__main__':
    main()
