#!/usr/bin/env python3
"""
Phase 2 expansion: Add more entities and dense cross-links
Target: 350+ nodes, 800+ edges
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
    edges.append({
        "source": source,
        "target": target,
        "label": rel_type,
        "weight": float(weight)
    })

def find_node_id(nodes, label):
    for n in nodes:
        if n['label'] == label:
            return n['id']
    return None

def main():
    data = load_graph()
    nodes = data['nodes']
    edges = data['edges']
    
    print(f"Starting: {len(nodes)} nodes, {len(edges)} edges")
    
    # ============================================================
    # PHASE A: Add more entities from IMA searches (remaining)
    # ============================================================
    
    new_entities = [
        # More companies
        ("PsiQuantum", "company", "美国光量子计算公司，目标构建百万量子比特光量子计算机", 3, ["7408677623443647"], ["英伟达投资的量子计算公司.pdf"], ["光量子", "硅光子"]),
        ("Atom Computing", "company", "美国中性原子量子计算公司，NVentures投资对象", 3, ["7408677623443647"], ["英伟达投资的量子计算公司.pdf"], ["中性原子"]),
        ("IQM Quantum", "company", "芬兰超导量子计算公司，欧洲领先的量子计算企业", 3, ["7425064727240963"], ["2026全球量子计算产业发展展望.pdf"], ["超导量子比特"]),
        ("Quantum Motion", "company", "英国硅基量子计算公司，专注硅自旋量子比特", 2, ["7425064727240963"], ["2025全球量子计算产业发展展望.pdf"], ["硅基量子比特"]),
        ("Oxford Quantum Circuits", "company", "英国超导量子计算公司，采用3D同轴架构", 2, ["7425064727240963"], ["2025全球量子计算产业发展展望.pdf"], ["超导量子比特"]),
        ("QuEra Computing", "company", "美国中性原子量子计算公司，与哈佛大学合作", 3, ["7408677623443647"], ["Enduring_Quantum_Logic.pdf"], ["中性原子"]),
        ("Pasqal", "company", "法国中性原子量子计算公司，欧洲中性原子技术先驱", 3, ["7425064727240963"], ["2025全球量子计算产业发展展望.pdf"], ["中性原子"]),
        ("百度量子计算", "company", "百度量子计算研究所，开发量脉、量易伏等平台", 3, ["7425064727240963"], ["2026全球量子计算产业发展展望.pdf"], ["量子云平台", "量子机器学习"]),
        ("阿里巴巴达摩院量子实验室", "company", "阿里巴巴旗下量子计算研究机构", 2, ["7425064727240963"], ["2025全球量子计算产业发展展望.pdf"], ["超导量子比特"]),
        ("腾讯量子实验室", "company", "腾讯旗下量子计算研究团队", 2, ["7425064727240963"], ["2026全球量子计算产业发展展望.pdf"], ["量子模拟"]),
        ("华为量子计算", "company", "华为量子计算研究团队，开发HiQ量子计算框架", 2, ["7425064727240963"], ["2026全球量子计算产业发展展望.pdf"], ["量子模拟", "HiQ"]),
        ("ColdQuanta/Infleqtion", "company", "美国中性原子量子技术公司，更名后为Infleqtion", 2, ["7408677623443647"], ["Enduring_Quantum_Logic.pdf"], ["中性原子"]),
        
        # More organizations
        ("芝加哥大学", "organization", "量子信息科学研究重镇，Science综述合作机构", 2, ["7408677623443647"], ["量子技术正加速从实验室走向现实世界.pdf"], ["量子硬件"]),
        ("代尔夫特理工大学", "organization", "荷兰量子计算研究中心，QuTech所在地", 2, ["7408677623443647"], ["量子技术正加速从实验室走向现实世界.pdf"], ["量子互联网"]),
        ("因斯布鲁克大学", "organization", "奥地利离子阱量子计算研究中心", 2, ["7408677623443647"], ["量子技术正加速从实验室走向现实世界.pdf"], ["离子阱"]),
        ("MIT", "organization", "麻省理工学院，William Oliver等超导量子计算专家所在", 3, ["7408677623443647"], ["Challenges and opportunities for quantum information hardware.pdf"], ["超导量子比特"]),
        ("Stanford University", "organization", "斯坦福大学，量子信息科学研究重镇", 2, ["7408677623443647"], ["量子技术正加速从实验室走向现实世界.pdf"], ["量子传感"]),
        
        # More concepts
        ("量子密钥分发 (QKD)", "concept", "利用量子力学原理实现安全的密钥分发，是量子通信的核心技术", 4, ["7408677623443647"], ["量子技术正加速从实验室走向现实世界.pdf"], ["量子通信", "BB84"]),
        ("量子网络", "concept", "通过量子纠缠和量子中继器连接远距离量子节点的网络", 3, ["7408677623443647"], ["量子技术正加速从实验室走向现实世界.pdf"], ["量子通信", "量子中继器"]),
        ("量子中继器", "concept", "延长量子通信距离的关键设备，利用量子存储和纠缠交换", 3, ["7408677623443647"], ["量子技术正加速从实验室走向现实世界.pdf"], ["量子网络", "量子存储"]),
        ("量子存储器", "concept", "存储量子态信息的器件，是量子中继器和量子网络的关键组件", 3, ["7408677623443647"], ["Challenges and opportunities for quantum information hardware.pdf"], ["量子中继器", "量子网络"]),
        ("量子互联网", "concept", "通过量子链路连接多个量子处理器形成的分布式量子计算网络", 3, ["7408677623443647"], ["量子技术正加速从实验室走向现实世界.pdf"], ["量子网络", "量子通信"]),
        ("量子优势 (Quantum Advantage)", "concept", "量子计算机在特定任务上超越经典计算机的能力展示", 5, ["7408677623443647"], ["Quantum_Computing_Tipping_Point_Strategic_Outlook.pdf"], ["量子优越性", "计算能力"]),
        ("量子优越性 (Quantum Supremacy)", "concept", "量子计算机完成经典计算机实际上无法完成的任务，与量子优势类似", 4, ["7408677623443647"], ["龙沛洵报告"], ["量子优势", "计算能力"]),
        ("噪声", "concept", "量子计算中的各种噪声源，包括去极化噪声、振幅阻尼噪声、相位阻尼噪声", 3, ["7408677623443647"], ["龙沛洵报告"], ["NISQ", "量子纠错"]),
        ("去极化噪声 (Depolarizing Noise)", "concept", "量子比特以一定概率被完全随机化的噪声模型", 3, ["7408677623443647"], ["龙沛洵报告"], ["噪声", "量子纠错"]),
        ("振幅阻尼 (Amplitude Damping)", "concept", "量子比特从|1⟩态弛豫到|0⟩态的噪声模型", 3, ["7408677623443647"], ["龙沛洵报告"], ["T1时间", "退相干"]),
        ("相位阻尼 (Phase Damping)", "concept", "量子比特失去相位信息的噪声模型", 3, ["7408677623443647"], ["龙沛洵报告"], ["T2时间", "退相干"]),
        ("T1弛豫时间", "concept", "量子比特能量弛豫时间，从|1⟩态衰减到|0⟩态的时间常数", 4, ["7411640966326739"], ["量子比特体系研讨.txt"], ["相干时间", "振幅阻尼"]),
        ("T2退相干时间", "concept", "量子比特相位退相干时间，叠加态相位信息丢失的时间常数", 4, ["7411640966326739"], ["量子比特体系研讨.txt"], ["相干时间", "相位阻尼"]),
        ("量子门集", "concept", "量子计算中用于实现任意量子操作的一组基本量子门", 3, ["7411640966326739"], ["量子比特体系研讨.txt"], ["通用门集", "完备性"]),
        ("通用门集", "concept", "能够组合实现任意量子操作的最小门集合，如{H, S, CNOT, T}", 3, ["7411640966326739"], ["量子比特体系研讨.txt"], ["量子门集", "完备性"]),
        ("量子傅里叶变换 (QFT)", "algorithm", "Shor算法的核心子程序，将量子态在计算基和傅里叶基之间变换", 4, ["7408677623443647"], ["龙沛洵报告"], ["Shor算法", "相位估计"]),
        ("量子相位估计 (QPE)", "algorithm", "估计酉算子特征值的量子算法，是许多量子算法的子程序", 4, ["7408677623443647"], ["龙沛洵报告"], ["Shor算法", "QFT"]),
        ("变分量子本征求解器 (VQE)", "algorithm", "NISQ时代最重要的量子算法之一，用于求解分子基态能量", 5, ["7408677623443647"], ["龙沛洵报告"], ["NISQ", "量子化学"]),
        ("量子近似优化算法 (QAOA)", "algorithm", "NISQ时代的量子优化算法，用于组合优化问题", 4, ["7408677623443647"], ["龙沛洵报告"], ["NISQ", "组合优化"]),
        ("量子随机行走 (Quantum Walk)", "algorithm", "经典随机行走的量子推广，是设计量子算法的重要工具", 3, ["7408677623443647"], ["龙沛洵报告"], ["搜索算法", "量子算法设计"]),
        ("Grover搜索算法", "algorithm", "在无序数据库中搜索的量子算法，提供二次加速", 5, ["7408677623443647"], ["龙沛洵报告"], ["搜索", "二次加速"]),
        ("量子态层析 (Quantum State Tomography)", "concept", "通过多次测量重构未知量子态的技术", 3, ["7408677623443647"], ["量子工程学_构建与控制.pdf"], ["量子测量", "密度矩阵"]),
        ("密度矩阵 (Density Matrix)", "concept", "描述量子系统状态的数学工具，可表示混合态", 3, ["7408677623443647"], ["量子力学(苏汝铿版).pdf"], ["量子态", "混合态"]),
        ("混合态 (Mixed State)", "concept", "量子系统的不纯态，用密度矩阵描述，与纯态相对", 3, ["7408677623443647"], ["量子力学(苏汝铿版).pdf"], ["密度矩阵", "纯态"]),
        ("纯态 (Pure State)", "concept", "可用单一态矢量描述的量子态，是叠加态的特例", 3, ["7408677623443647"], ["量子力学(苏汝铿版).pdf"], ["混合态", "态矢量"]),
        ("约化密度矩阵 (Reduced Density Matrix)", "concept", "描述复合量子系统子系统的状态，由对其他子系统求迹得到", 3, ["7408677623443647"], ["量子力学(苏汝铿版).pdf"], ["密度矩阵", "部分迹"]),
        ("Bell态 (Bell State)", "concept", "两量子比特的最大纠缠态，如|Φ+⟩=(|00⟩+|11⟩)/√2", 4, ["7408677623443647"], ["量子力学(苏汝铿版).pdf"], ["量子纠缠", "EPR对"]),
        ("EPR对 (EPR Pair)", "concept", "Einstein-Podolsky-Rosen悖论中描述的量子纠缠对", 4, ["7408677623443647"], ["量子力学(苏汝铿版).pdf"], ["Bell态", "量子纠缠"]),
        ("量子不可克隆定理 (No-Cloning Theorem)", "concept", "不可能完美复制未知量子态的基本定理", 4, ["7408677623443647"], ["量子计算_掌握未来.pdf"], ["量子通信", "量子密码"]),
        ("海森堡不确定性原理", "theory", "不可能同时精确测量共轭物理量对（如位置和动量）的基本量子力学原理", 5, ["7408677623443647"], ["量子力学(苏汝铿版).pdf"], ["测量", "量子力学基础"]),
        ("普朗克常数", "concept", "量子力学的基本常数h，表征量子化尺度", 4, ["7408677623443647"], ["量子力学(苏汝铿版).pdf"], ["量子化", "基本常数"]),
        ("德布罗意波", "concept", "物质粒子的波动性，波长λ=h/p", 3, ["7408677623443647"], ["量子力学(苏汝铿版).pdf"], ["波粒二象性", "物质波"]),
        ("波粒二象性 (Wave-Particle Duality)", "concept", "微观粒子同时具有波动性和粒子性的量子力学基本原理", 5, ["7408677623443647"], ["量子计算_掌握未来.pdf"], ["德布罗意波", "双缝实验"]),
        ("玻尔量子论", "theory", "玻尔提出的原子模型，量子力学的前身", 3, ["7408677623443647"], ["量子力学(苏汝铿版).pdf"], ["能级", "量子跃迁"]),
        ("量子隧穿效应 (Quantum Tunneling)", "concept", "量子粒子穿越经典力学不允许的势垒的现象", 4, ["7408677623443647"], ["量子计算_掌握未来.pdf"], ["势垒", "量子效应"]),
        ("量子点 (Quantum Dot)", "material", "半导体中限制电子在三维空间的人造原子，是量子比特的候选实现", 3, ["7408677623443647"], ["Challenges and opportunities for quantum information hardware.pdf"], ["硅基量子比特", "自旋量子比特"]),
        ("NV色心 (NV Center)", "material", "金刚石中氮-空位缺陷中心，是量子传感的重要平台", 3, ["7408677623443647"], ["Challenges and opportunities for quantum information hardware.pdf"], ["量子传感", "量子精密测量"]),
        ("拓扑绝缘体 (Topological Insulator)", "material", "体态绝缘但表面态导电的材料，是拓扑量子计算的候选平台", 3, ["7441506466037417"], ["拓扑量子计算研究报告.docx"], ["拓扑量子计算", "马约拉纳零模"]),
        ("约瑟夫森结 (Josephson Junction)", "material", "两块超导体通过薄绝缘层连接形成的量子器件，是超导量子比特的基本构件", 5, ["7408677623443647"], ["量子工程学.pdf"], ["超导量子比特", "Transmon"]),
        ("谐振腔", "hardware", "在Circuit QED中作为量子总线连接超导量子比特的微波谐振器", 3, ["7408677623443647"], ["Circuit_Quantum_Electrodynamics.pdf"], ["Circuit QED", "量子总线"]),
        
        # More hardware/products
        ("Sycamore处理器", "hardware", "谷歌2019年宣布实现量子优越性的53比特超导量子处理器", 5, ["7408677623443647"], ["龙沛洵报告"], ["谷歌", "超导量子比特"]),
        ("IBM Eagle处理器", "hardware", "IBM 127比特超导量子处理器", 4, ["7425064727240963"], ["2025全球量子计算产业发展展望.pdf"], ["IBM", "超导量子比特"]),
        ("IBM Condor处理器", "hardware", "IBM 433比特超导量子处理器", 4, ["7425064727240963"], ["2026全球量子计算产业发展展望.pdf"], ["IBM", "超导量子比特"]),
        ("IBM Heron处理器", "hardware", "IBM模块化量子处理器，支持QPU互连", 3, ["7425064727240963"], ["2026全球量子计算产业发展展望.pdf"], ["IBM", "模块化架构"]),
        ("九章光量子计算机", "hardware", "中科大潘建伟团队研制的光量子计算原型机，实现量子优越性", 5, ["7408677623443647"], ["Quantum_Computing_Tipping_Point_Strategic_Outlook.pdf"], ["光量子", "中科大"]),
        ("Atom Computing中性原子处理器", "hardware", "Atom Computing开发的中性原子量子处理器", 2, ["7408677623443647"], ["Enduring_Quantum_Logic.pdf"], ["中性原子", "Atom Computing"]),
        
        # More applications
        ("量子密码学", "application", "利用量子力学原理设计和分析的密码学方案", 4, ["7408677623443647"], ["龙沛洵报告"], ["量子密钥分发", "后量子密码"]),
        ("后量子密码学 (PQC)", "application", "抵抗量子计算攻击的经典密码学方案，NIST已标准化", 4, ["7408677623443647"], ["Quantum_Computing_Tipping_Point_Strategic_Outlook.pdf"], ["Shor算法", "密码学"]),
        ("量子机器学习 (QML)", "application", "利用量子计算加速机器学习任务的交叉领域", 4, ["7408677623443647"], ["Quantum Deep Learning: 郭国平.pdf"], ["变分量子电路", "NISQ"]),
        ("量子优化", "application", "利用量子计算求解优化问题的应用方向", 3, ["7408677623443647"], ["量子增强认知推荐算法-修改稿1210.pdf"], ["QAOA", "组合优化"]),
        
        # Tools/software
        ("Cirq", "tool", "Google开发的量子计算编程框架", 3, ["7408677623443647"], ["龙沛洵报告"], ["量子编程", "谷歌"]),
        ("PennyLane", "tool", "Xanadu开发的量子机器学习编程框架", 3, ["7408677623443647"], ["Quantum Deep Learning: 郭国平.pdf"], ["量子机器学习", "变分量子电路"]),
        ("Qiskit", "tool", "IBM开发的量子计算开源编程框架", 4, ["7408677623443647"], ["龙沛洵报告"], ["量子编程", "IBM"]),
        ("HiQ量子计算框架", "tool", "华为开发的量子计算模拟框架", 2, ["7425064727240963"], ["2026全球量子计算产业发展展望.pdf"], ["量子模拟", "华为"]),
        
        # Additional concepts from lectures
        ("超导量子比特能谱", "concept", "超导量子比特的能级结构，包括基态、第一激发态等", 3, ["7411640966326739"], ["量子比特体系研讨.txt"], ["Transmon", "能级"]),
        ("量子比特串扰 (Crosstalk)", "concept", "不同量子比特之间不期望的耦合和干扰", 3, ["7408677623443647"], ["多量子芯片互连方案调研.pdf"], ["噪声", "多比特"]),
        ("量子门校准 (Gate Calibration)", "concept", "精确设置量子门参数以实现高保真度操作的过程", 3, ["7411640966326739"], ["量子比特体系研讨.txt"], ["门保真度", "量子比特操控"]),
        ("量子比特制备 (Qubit Fabrication)", "concept", "制造量子比特芯片的工艺过程", 3, ["7408677623443647"], ["China_s_Quantum_Computing_Leader.pdf"], ["超导量子比特", "芯片加工"]),
        ("良品率 (Yield)", "concept", "量子芯片制造中功能正常的量子比特比例", 3, ["7408677623443647"], ["Quantum_Scaling_Architecture.pdf"], ["量子比特制备", "规模化"]),
        ("多比特纠缠态 (Multi-qubit Entanglement)", "concept", "三个或更多量子比特之间的纠缠态，如GHZ态和W态", 3, ["7408677623443647"], ["量子工程学_构建与控制.pdf"], ["量子纠缠", "GHZ态"]),
        ("GHZ态", "concept", "Greenberger-Horne-Zeilinger态，多量子比特的最大纠缠态", 3, ["7408677623443647"], ["量子力学(苏汝铿版).pdf"], ["多比特纠缠态", "Bell态"]),
        ("量子纠错阈值定理 (Threshold Theorem)", "theory", "当物理错误率低于阈值时，可以通过增加物理比特数无限降低逻辑错误率", 5, ["7408677623443647"], ["量子工程学_构建与控制.pdf"], ["量子纠错", "逻辑量子比特"]),
        ("容错量子计算 (Fault-Tolerant QC)", "concept", "通过量子纠错实现可靠计算，是量子计算长期目标", 5, ["7408677623443647"], ["龙沛洵报告"], ["量子纠错", "逻辑量子比特"]),
        ("Magic State Distillation", "algorithm", "制备高质量T门所需魔法态的过程，是容错量子计算的关键子程序", 3, ["7408677623443647"], ["量子工程学_构建与控制.pdf"], ["容错量子计算", "T门"]),
    ]
    
    for e in new_entities:
        add_node(nodes, e[0], e[1], e[2], e[3], e[4], e[5], e[6])
    
    # ============================================================
    # PHASE B: Dense cross-linking between ALL nodes
    # ============================================================
    
    # Build a label->id map for fast lookup
    label_to_id = {}
    for n in nodes:
        label_to_id[n['label']] = n['id']
    
    # Define relationship rules as (source_label, target_label, relation, weight)
    dense_rels = [
        # Algorithm-concept relationships
        ("量子傅里叶变换 (QFT)", "量子傅里叶变换", "is_type_of", 5),
        ("量子相位估计 (QPE)", "量子傅里叶变换 (QFT)", "uses", 5),
        ("Shor算法", "量子傅里叶变换 (QFT)", "uses", 5),
        ("Shor算法", "量子相位估计 (QPE)", "uses", 5),
        ("Shor算法", "量子密码学", "applies_to", 4),
        ("Shor算法", "后量子密码学 (PQC)", "related_to", 4),
        ("Shor算法", "量子优势 (Quantum Advantage)", "enables", 4),
        ("Grover搜索算法", "量子随机行走 (Quantum Walk)", "related_to", 3),
        ("变分量子本征求解器 (VQE)", "量子化学模拟", "applies_to", 5),
        ("变分量子本征求解器 (VQE)", "量子药物发现", "applies_to", 4),
        ("变分量子本征求解器 (VQE)", "NISQ时代", "related_to", 4),
        ("QAOA (量子近似优化算法)", "量子组合优化", "applies_to", 4),
        ("QAOA (量子近似优化算法)", "量子金融", "applies_to", 3),
        ("QAOA (量子近似优化算法)", "NISQ时代", "related_to", 4),
        ("QAOA (量子近似优化算法)", "量子近似优化算法 (QAOA)", "is_type_of", 5),
        ("变分量子本征求解器 (VQE)", "变分量子本征求解器", "is_type_of", 5),
        
        # Concept-concept dense links
        ("量子优势 (Quantum Advantage)", "量子优越性 (Quantum Supremacy)", "related_to", 5),
        ("量子优势 (Quantum Advantage)", "Sycamore处理器", "enables", 4),
        ("量子优势 (Quantum Advantage)", "九章光量子计算机", "enables", 4),
        ("量子优越性 (Quantum Supremacy)", "Sycamore处理器", "enables", 5),
        ("量子不可克隆定理 (No-Cloning Theorem)", "量子密钥分发 (QKD)", "enables", 4),
        ("量子不可克隆定理 (No-Cloning Theorem)", "量子通信", "enables", 4),
        ("海森堡不确定性原理", "量子测量", "related_to", 5),
        ("海森堡不确定性原理", "量子计算", "related_to", 3),
        ("波粒二象性 (Wave-Particle Duality)", "德布罗意波", "related_to", 5),
        ("波粒二象性 (Wave-Particle Duality)", "量子力学", "part_of", 4),
        ("玻尔量子论", "量子力学", "derives_from", 3),
        ("量子隧穿效应 (Quantum Tunneling)", "约瑟夫森结 (Josephson Junction)", "enables", 4),
        ("量子隧穿效应 (Quantum Tunneling)", "量子计算", "related_to", 3),
        
        # People-institution
        ("Alexandre Blais", "Circuit QED", "developed_by", 5),
        ("David D. Awschalom", "芝加哥大学", "part_of", 2),
        ("William D. Oliver", "MIT", "part_of", 3),
        
        # Hardware-platform links
        ("Sycamore处理器", "谷歌", "developed_by", 5),
        ("Sycamore处理器", "超导量子比特 (Transmon)", "uses", 5),
        ("IBM Eagle处理器", "IBM", "developed_by", 5),
        ("IBM Eagle处理器", "超导量子比特 (Transmon)", "uses", 5),
        ("IBM Condor处理器", "IBM", "developed_by", 5),
        ("IBM Condor处理器", "超导量子比特 (Transmon)", "uses", 5),
        ("IBM Heron处理器", "IBM", "developed_by", 4),
        ("IBM Heron处理器", "量子互连 (Quantum Interconnect)", "enables", 4),
        ("九章光量子计算机", "光量子计算", "uses", 5),
        ("九章光量子计算机", "中科大", "developed_by", 5),
        ("Willow", "谷歌", "developed_by", 5),
        ("Willow", "超导量子比特 (Transmon)", "uses", 5),
        ("祖冲之三号", "中科大", "developed_by", 5),
        ("祖冲之三号", "超导量子比特 (Transmon)", "uses", 5),
        ("Atom Computing中性原子处理器", "中性原子量子比特", "uses", 4),
        ("Atom Computing中性原子处理器", "Atom Computing", "developed_by", 4),
        
        # T1/T2 and coherence
        ("T1弛豫时间", "振幅阻尼 (Amplitude Damping)", "related_to", 5),
        ("T2退相干时间", "相位阻尼 (Phase Damping)", "related_to", 5),
        ("T1弛豫时间", "相干时间 (Coherence Time)", "part_of", 5),
        ("T2退相干时间", "相干时间 (Coherence Time)", "part_of", 5),
        ("T2退相干时间", "退相干 (Decoherence)", "related_to", 5),
        ("T1弛豫时间", "退相干 (Decoherence)", "related_to", 4),
        
        # QKD and quantum communication
        ("量子密钥分发 (QKD)", "量子通信", "part_of", 5),
        ("量子网络", "量子互联网", "part_of", 4),
        ("量子中继器", "量子网络", "enables", 5),
        ("量子存储器", "量子中继器", "enables", 4),
        ("量子网络", "量子通信", "part_of", 4),
        ("量子互联网", "量子通信", "part_of", 4),
        
        # Topological quantum computing deep links
        ("拓扑绝缘体 (Topological Insulator)", "马约拉纳零模 (Majorana Zero Mode)", "enables", 4),
        ("拓扑绝缘体 (Topological Insulator)", "拓扑保护 (Topological Protection)", "enables", 4),
        
        # NV center and sensing
        ("NV色心 (NV Center)", "量子传感", "enables", 4),
        ("NV色心 (NV Center)", "量子精密测量", "enables", 4),
        ("量子传感", "量子精密测量", "related_to", 4),
        
        # Josephson junction
        ("约瑟夫森结 (Josephson Junction)", "超导量子比特 (Transmon)", "part_of", 5),
        ("约瑟夫森结 (Josephson Junction)", "量子隧穿效应 (Quantum Tunneling)", "uses", 4),
        
        # Quantum dot
        ("量子点 (Quantum Dot)", "硅基量子比特", "enables", 4),
        ("量子点 (Quantum Dot)", "自旋量子比特", "enables", 3),
        
        # Error correction deep links
        ("量子纠错阈值定理 (Threshold Theorem)", "容错量子计算 (Fault-Tolerant QC)", "enables", 5),
        ("容错量子计算 (Fault-Tolerant QC)", "量子纠错", "uses", 5),
        ("容错量子计算 (Fault-Tolerant QC)", "逻辑量子比特 (Logical Qubit)", "uses", 5),
        ("Magic State Distillation", "容错量子计算 (Fault-Tolerant QC)", "part_of", 4),
        
        # Dense state/measurement links
        ("密度矩阵 (Density Matrix)", "混合态 (Mixed State)", "related_to", 5),
        ("密度矩阵 (Density Matrix)", "纯态 (Pure State)", "related_to", 5),
        ("混合态 (Mixed State)", "纯态 (Pure State)", "related_to", 4),
        ("约化密度矩阵 (Reduced Density Matrix)", "密度矩阵 (Density Matrix)", "part_of", 4),
        ("约化密度矩阵 (Reduced Density Matrix)", "量子纠缠 (Entanglement)", "related_to", 4),
        ("Bell态 (Bell State)", "EPR对 (EPR Pair)", "related_to", 5),
        ("Bell态 (Bell State)", "量子纠缠 (Entanglement)", "part_of", 5),
        ("GHZ态", "多比特纠缠态 (Multi-qubit Entanglement)", "is_type_of", 4),
        ("GHZ态", "量子纠缠 (Entanglement)", "part_of", 4),
        ("量子态层析 (Quantum State Tomography)", "密度矩阵 (Density Matrix)", "uses", 4),
        ("量子态层析 (Quantum State Tomography)", "量子测量", "uses", 4),
        
        # Crosstalk and scaling
        ("量子比特串扰 (Crosstalk)", "量子噪声 (Quantum Noise)", "part_of", 4),
        ("量子比特串扰 (Crosstalk)", "多量子芯片互连方案调研", "related_to", 3),
        ("良品率 (Yield)", "量子比特制备 (Qubit Fabrication)", "related_to", 4),
        ("量子门校准 (Gate Calibration)", "门保真度 (Gate Fidelity)", "related_to", 5),
        ("超导量子比特能谱", "超导量子比特 (Transmon)", "part_of", 4),
        
        # Tools and companies
        ("Qiskit", "IBM", "developed_by", 5),
        ("Cirq", "谷歌", "developed_by", 4),
        ("PennyLane", "量子机器学习 (QML)", "applies_to", 4),
        ("PennyLane", "变分量子本征求解器 (VQE)", "applies_to", 3),
        ("HiQ量子计算框架", "华为量子计算", "developed_by", 4),
        ("百度量子计算", "量子机器学习 (QML)", "applies_to", 3),
        
        # Institution-technology
        ("代尔夫特理工大学", "量子互联网", "researches", 3),
        ("因斯布鲁克大学", "离子阱量子比特", "researches", 3),
        ("芝加哥大学", "量子传感", "researches", 3),
        
        # More company-technology links
        ("PsiQuantum", "光量子计算", "uses", 5),
        ("QuEra Computing", "中性原子量子比特", "uses", 5),
        ("QuEra Computing", "中性原子分区架构", "uses", 3),
        ("Pasqal", "中性原子量子比特", "uses", 5),
        ("IQM Quantum", "超导量子比特 (Transmon)", "uses", 5),
        ("Quantum Motion", "硅基量子比特", "uses", 5),
        ("Oxford Quantum Circuits", "超导量子比特 (Transmon)", "uses", 5),
        ("ColdQuanta/Inflektions", "中性原子量子比特", "uses", 4),
        ("Atom Computing", "中性原子量子比特", "uses", 5),
        
        # Quantum computing paradigm links
        ("NISQ时代", "量子优势 (Quantum Advantage)", "related_to", 4),
        ("NISQ时代", "量子计算产业化", "related_to", 3),
        ("后量子密码学 (PQC)", "Shor算法", "addresses", 4),
        ("量子密码学", "量子密钥分发 (QKD)", "uses", 4),
        ("量子密码学", "量子不可克隆定理 (No-Cloning Theorem)", "uses", 3),
        ("量子机器学习 (QML)", "量子深度学习 (Quantum Deep Learning)", "part_of", 4),
        ("量子机器学习 (QML)", "变分量子本征求解器 (VQE)", "uses", 3),
        ("量子优化", "QAOA (量子近似优化算法)", "uses", 4),
        ("量子优化", "量子退火算法", "related_to", 3),
        
        # Source knowledge base cross-links
        ("量子计算产业化", "光子盒研究院", "developed_by", 3),
        ("量子计算产业化", "CQCC量子计算产业报告", "related_to", 3),
        ("量子计算产业化", "2026全球量子计算产业发展展望", "related_to", 3),
        
        # Physical foundations
        ("普朗克常数", "量子力学", "part_of", 4),
        ("德布罗意波", "量子力学", "part_of", 4),
        ("薛定谔方程 (Schrödinger Equation)", "量子力学", "part_of", 5),
        ("海森堡不确定性原理", "量子力学", "part_of", 5),
        ("波函数坍缩 (Wave Function Collapse)", "量子测量", "part_of", 5),
        
        # Error correction chain
        ("噪声", "退相干 (Decoherence)", "related_to", 4),
        ("噪声", "去极化噪声 (Depolarizing Noise)", "part_of", 4),
        ("噪声", "振幅阻尼 (Amplitude Damping)", "part_of", 4),
        ("噪声", "相位阻尼 (Phase Damping)", "part_of", 4),
        ("量子噪声 (Quantum Noise)", "噪声", "is_type_of", 4),
        ("量子噪声 (Quantum Noise)", "量子纠错", "related_to", 5),
        ("量子噪声 (Quantum Noise)", "NISQ时代", "related_to", 4),
        
        # Quantum gate and operation links
        ("量子门集", "通用门集", "part_of", 4),
        ("通用门集", "Hadamard门", "part_of", 4),
        ("通用门集", "CNOT门", "part_of", 4),
        ("通用门集", "T门", "part_of", 4),
        ("T门", "Magic State Distillation", "related_to", 4),
        
        # More company-concept links
        ("阿里达摩院量子实验室", "超导量子比特 (Transmon)", "uses", 3),
        ("腾讯量子实验室", "量子模拟 (Quantum Simulation)", "applies_to", 3),
        ("华为量子计算", "量子模拟 (Quantum Simulation)", "applies_to", 3),
        
        # Quantum hardware scaling
        ("良品率 (Yield)", "多量子芯片互连方案调研", "related_to", 3),
        ("量子比特串扰 (Crosstalk)", "可调耦合器", "related_to", 3),
        ("量子比特串扰 (Crosstalk)", "量子比特操控", "related_to", 3),
        
        # Algorithm-application dense links
        ("量子模拟 (Quantum Simulation)", "量子材料科学", "applies_to", 4),
        ("量子模拟 (Quantum Simulation)", "量子化学模拟", "applies_to", 4),
        ("量子模拟 (Quantum Simulation)", "费米-哈伯德模型 (Fermi-Hubbard Model)", "applies_to", 4),
        
        # Key milestone events (as concepts)
        ("量子优势 (Quantum Advantage)", "Willow", "enables", 5),
        ("量子优势 (Quantum Advantage)", "祖冲之三号", "enables", 4),
        ("量子计算产业化", "Quantum_Dawn_Global_Strategy", "related_to", 3),
        
        # More dense interconnections
        ("谐振腔", "Circuit QED", "part_of", 4),
        ("谐振腔", "超导量子比特 (Transmon)", "related_to", 3),
        ("量子比特读取", "超导量子比特 (Transmon)", "applies_to", 4),
        ("量子比特操控", "超导量子比特 (Transmon)", "applies_to", 4),
        ("量子比特操控", "门保真度 (Gate Fidelity)", "determines", 4),
        ("量子比特读取", "读取保真度 (Readout Fidelity)", "determines", 4),
        ("相干时间 (Coherence Time)", "超导量子比特 (Transmon)", "related_to", 4),
        ("相干时间 (Coherence Time)", "离子阱量子比特", "related_to", 4),
        ("迪文森佐准则 (DiVincenzo Criteria)", "门保真度 (Gate Fidelity)", "defines_requirements", 3),
        ("量子比特制备 (Qubit Fabrication)", "超导量子比特 (Transmon)", "enables", 4),
        ("量子比特制备 (Qubit Fabrication)", "良品率 (Yield)", "determines", 4),
    ]
    
    for src_label, tgt_label, rel, weight in dense_rels:
        src_id = label_to_id.get(src_label)
        tgt_id = label_to_id.get(tgt_label)
        if src_id and tgt_id:
            add_edge(edges, src_id, tgt_id, rel, weight)
        else:
            # Try partial match
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
            if src_id and tgt_id:
                add_edge(edges, src_id, tgt_id, rel, weight)
    
    # ============================================================
    # Update metadata and save
    # ============================================================
    
    data['metadata']['node_count'] = len(nodes)
    data['metadata']['edge_count'] = len(edges)
    data['metadata']['last_updated'] = '2026-06-13'
    data['metadata']['expansion_notes'] = 'Phase 2: 大幅扩展节点和密集交叉关系，目标300+节点800+边'
    
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
    print(f"\nEdge type distribution (top 15):")
    for t, c in sorted(edge_type_counts.items(), key=lambda x: -x[1])[:15]:
        print(f"  {t}: {c}")

if __name__ == '__main__':
    main()
