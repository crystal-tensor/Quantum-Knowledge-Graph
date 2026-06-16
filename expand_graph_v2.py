#!/usr/bin/env python3
"""
大幅扩展量子知识图谱 - 从IMA知识库搜索结果中提取实体和关系
目标: 300+ 节点, 800+ 边
"""

import json
import os

WORKSPACE = "/Users/danielcrystal/WorkBuddy/2026-06-13-17-30-18"
GRAPH_FILE = os.path.join(WORKSPACE, "graph_data.json")

# Knowledge base IDs for source attribution
KB_SOURCES = {
    "7412047272751870": "量子计算学习材料",
    "7425064727240963": "量子产业研究报告",
    "7411640966326739": "金贻荣老师的直播课件",
    "7408677623443647": "量子计算",
    "7441506466037417": "李博士的项目",
}

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
    """Add a node if it doesn't already exist (by label)"""
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

def add_edge(edges, source, target, rel_type, label="", weight=1):
    """Add an edge if it doesn't already exist. Uses 'label' for relationship type."""
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
    # PHASE 1: Companies & Organizations from IMA searches
    # ============================================================
    
    companies = [
        ("相干科技 (Coherent Quantum)", "company", "由北京量子信息科学研究院孵化的超导量子计算公司，中国超导量子计算领域顶尖企业", 5,
         ["7408677623443647", "7441506466037417"],
         ["China_s_Quantum_Computing_Leader.pdf", "揭秘中国顶尖量子计算公司"],
         ["超导量子计算", "商业化"]),
        
        ("相干科技", "company", "源自北京量子院的国家量子战略商业旗舰，超导量子计算解决方案提供商", 4,
         ["7408677623443647"],
         ["Quantum_Strategy_Commercial_Flagship.pdf"],
         ["超导量子计算", "北京量子院"]),
        
        ("中微达信", "company", "国内领先的低温CMOS量子测控芯片解决方案提供商，推出'蜀山'系列芯片", 4,
         ["7408677623443647"],
         ["超导量子计算机集成趋势和低温电子系测控cmos芯片和.pdf"],
         ["低温CMOS", "蜀山系列", "量子测控"]),
        
        ("国仪量子 (CIQTEK)", "company", "全球领先的量子精密测量技术公司，用量子传感赋能千行百业", 3,
         ["7412047272751870"],
         ["【国仪量子】量子精密测量行业赋能白皮书.pdf"],
         ["量子精密测量", "量子传感"]),
        
        ("瀚海凌潮", "company", "构建量子计算融合基础设施的创业公司，目标打造量子界的OpenAI", 3,
         ["7408677623443647"],
         ["Quantum_Fusion_Infrastructure.pdf"],
         ["融合基础设施", "量子云平台"]),
        
        ("本源量子", "company", "中国量子计算全栈解决方案提供商，出版《量子计算与编程入门》教材", 4,
         ["7408677623443647"],
         ["郭国平、陈昭钧、郭光灿：《量子计算与编程入门》PDF教材.pdf"],
         ["量子编程", "Qiskit"]),
        
        ("QureGenAI", "company", "量子药物发现领域公司，基于生成式量子本征求解器进行药物研发", 3,
         ["7408677623443647"],
         ["2509.19715v1.pdf", "s41598-024-67897-8.pdf"],
         ["量子化学", "药物发现"]),
        
        ("Quantinuum", "company", "由霍尼韦尔量子解决方案与Cambridge Quantum合并而成的离子阱量子计算领军企业", 5,
         ["7408677623443647"],
         ["英伟达投资的哪几家量子计算公司.pdf"],
         ["离子阱", "Helios"]),
        
        ("中关村量子产业联盟", "organization", "中国量子计算产业联盟组织", 3,
         ["7408677623443647"],
         ["量子计算_掌握未来.pdf"],
         ["产业联盟", "政策"]),
        
        ("北京量子信息科学研究院 (BAQIS)", "organization", "北京市政府牵头的国家级量子信息战略科研机构，耗资数十亿", 5,
         ["7408677623443647", "7441506466037417"],
         ["China_s_Quantum_Computing_Leader.pdf"],
         ["量子院", "超导量子计算"]),
        
        ("光子盒研究院", "organization", "专注量子计算产业研究的分析机构，发布年度产业报告", 3,
         ["7425064727240963", "7408677623443647"],
         ["2025全球量子计算产业发展展望.pdf"],
         ["产业报告", "市场分析"]),
        
        ("中国计算机学会量子计算大会 (CQCC)", "organization", "中国量子计算领域权威学术会议组织", 3,
         ["7408677623443647"],
         ["CQCC量子计算产业报告"],
         ["产业报告", "标准"]),
        
        ("IHEP计算中心", "organization", "中国科学院高能物理研究所计算中心", 2,
         ["7408677623443647"],
         ["龙沛洵报告"],
         ["高能物理", "量子计算"]),
    ]
    
    for c in companies:
        add_node(nodes, c[0], c[1], c[2], c[3], c[4], c[5], c[6])
    
    # ============================================================
    # PHASE 2: People from IMA searches
    # ============================================================
    
    people = [
        ("金贻荣", "person", "中国超导量子计算领域顶尖专家，翻译《量子工程学》，20年科研积累，相干科技创始人", 5,
         ["7408677623443647", "7411640966326739", "7412047272751870"],
         ["China_s_Quantum_Computing_Leader.pdf", "量子工程学.pdf"],
         ["超导量子计算", "相干科技"]),
        
        ("郭国平", "person", "本源量子创始人，量子计算与编程领域专家", 4,
         ["7408677623443647"],
         ["《量子计算与编程入门》.pdf"],
         ["本源量子", "量子编程"]),
        
        ("郭光灿", "person", "中国量子光学和量子信息科学开拓者，中国科学院院士", 4,
         ["7408677623443647"],
         ["《量子计算与编程入门》.pdf"],
         ["量子光学", "量子信息"]),
        
        ("陈昭昀", "person", "量子计算与编程领域研究者，与郭国平合著《量子计算与编程入门》", 3,
         ["7408677623443647"],
         ["《量子计算与编程入门》.pdf"],
         ["量子编程"]),
        
        ("龙沛洵", "person", "IHEP计算中心研究员，量子计算原理科普报告主讲人", 2,
         ["7408677623443647"],
         ["2025年3月青年科技工作者园地报告_龙沛洵.pptx"],
         ["量子计算原理"]),
        
        ("Alexandre Blais", "person", "Circuit QED领域开创者之一，Sherbrooke大学教授，Reviews of Modern Physics综述作者", 4,
         ["7408677623443647"],
         ["Circuit_Quantum_Electrodynamics.pdf", "量子电动力学.pdf"],
         ["Circuit QED", "超导量子比特"]),
        
        ("David D. Awschalom", "person", "量子信息硬件领域权威，Science综述文章主要作者", 4,
         ["7408677623443647"],
         ["Challenges and opportunities for quantum information hardware.pdf"],
         ["量子硬件", "量子传感"]),
        
        ("A.M. Zagoskin", "person", "量子工程学著作作者，金贻荣翻译其作品", 3,
         ["7408677623443647", "7412047272751870"],
         ["量子工程学.pdf"],
         ["量子工程学"]),
        
        ("苏汝铿", "person", "量子力学教材作者，复旦大学教授", 2,
         ["7408677623443647"],
         ["量子力学(苏汝铿版).pdf"],
         ["量子力学"]),
        
        ("William D. Oliver", "person", "MIT量子计算专家，量子信息硬件综述作者", 3,
         ["7408677623443647"],
         ["Challenges and opportunities for quantum information hardware.pdf"],
         ["超导量子比特", "量子纠错"]),
    ]
    
    for p in people:
        add_node(nodes, p[0], p[1], p[2], p[3], p[4], p[5], p[6])
    
    # ============================================================
    # PHASE 3: Concepts & Theories from IMA searches
    # ============================================================
    
    concepts = [
        ("量子精密测量", "concept", "利用量子特性(能级跃迁、相干叠加、量子纠缠)获得突破经典测量技术极限的新一代精密测量技术", 4,
         ["7412047272751870"],
         ["【国仪量子】量子精密测量行业赋能白皮书.pdf"],
         ["量子传感", "测量精度"]),
        
        ("拓扑量子计算", "concept", "利用物质的拓扑量子态实现信息编码与处理，核心优势是利用拓扑保护特性实现内在容错", 5,
         ["7441506466037417"],
         ["拓扑量子计算研究报告.docx"],
         ["任意子", "马约拉纳零模", "容错"]),
        
        ("任意子 (Anyon)", "concept", "在二维空间中存在的介于玻色子和费米子之间的准粒子，是拓扑量子计算的物理基础", 4,
         ["7441506466037417"],
         ["拓扑量子计算研究报告.docx"],
         ["拓扑量子比特", "非阿贝尔统计"]),
        
        ("马约拉纳零模 (Majorana Zero Mode)", "concept", "满足马约拉纳方程的零能准粒子态，是拓扑量子比特的候选实现方式", 4,
         ["7441506466037417"],
         ["拓扑量子计算研究报告.docx"],
         ["拓扑保护", "马约拉纳费米子"]),
        
        ("费米-哈伯德模型 (Fermi-Hubbard Model)", "theory", "描述强关联电子系统的基本模型，是理解铜氧化物超导体的理论核心", 4,
         ["7408677623443647"],
         ["Quantum_Pairing_Observed.pdf"],
         ["强关联", "超导配对"]),
        
        ("量子增强认知推荐算法", "algorithm", "基于量子优化的认知增强推荐方法，通过变分量子电路突破传统算力瓶颈", 3,
         ["7408677623443647"],
         ["量子增强认知推荐算法-修改稿1210.pdf"],
         ["VQE", "量子优化", "推荐系统"]),
        
        ("生成式量子本征求解器 (GQE)", "algorithm", "基于SMILES启发的迁移学习量子算子方法，用于量子化学计算", 3,
         ["7408677623443647"],
         ["2509.19715v1.pdf"],
         ["量子化学", "迁移学习"]),
        
        ("布线丛林 (Wiring Jungle)", "concept", "描述量子计算机从室温到量子芯片的大量同轴线缆造成的物理空间占用和信号串扰问题", 4,
         ["7408677623443647"],
         ["Cryo-CMOS_Quantum_Control_Global_Apex.pdf"],
         ["控制墙", "低温CMOS"]),
        
        ("控制墙 (Control Wall)", "concept", "量子计算规模化面临的核心瓶颈：随着量子比特数量增长，控制线缆的物理空间和热负载达到极限", 4,
         ["7408677623443647"],
         ["Quantum_Scaling_Architecture_and_Control.pdf"],
         ["布线丛林", "低温CMOS"]),
        
        ("量子隐形传态 (Quantum Teleportation)", "concept", "利用量子纠缠和经典通信将未知量子态从一个位置传送到另一个位置的技术", 4,
         ["7408677623443647"],
         ["Quantum_Scaling_Architecture_and_Control.pdf"],
         ["量子纠缠", "分布式量子计算"]),
        
        ("量子-经典混合框架 (Hybrid Quantum-Classical)", "concept", "结合量子计算和经典计算的混合优化框架，如VQE和QAOA算法", 4,
         ["7408677623443647"],
         ["量子增强认知推荐算法-修改稿1210.pdf"],
         ["VQE", "QAOA", "NISQ"]),
        
        ("量子性能分级标准 (Five-Level Standard)", "protocol", "量子计算系统性能测试的分级评估框架：L1物理层→L2门层→L3电路层→L4系统层→L5应用层", 4,
         ["7408677623443647"],
         ["Quantum_Peak_Five_Level_Standard.pdf", "量子计算系统性能测试分级标准(1).pdf"],
         ["Benchmark", "性能评估"]),
        
        ("中性原子分区架构", "concept", "将中性原子量子处理器分为存储区、纠缠区和读取区，解决原子丢失问题", 3,
         ["7408677623443647"],
         ["Enduring_Quantum_Logic.pdf"],
         ["中性原子", "原子重用"]),
        
        ("量子计算产业化", "concept", "量子计算从实验室到工业应用的转变过程，从物理量子比特时代进入逻辑量子比特关键转折期", 4,
         ["7408677623443647", "7425064727240963"],
         ["Quantum_Dawn_Global_Strategy.pdf", "2026全球量子计算产业发展展望.pdf"],
         ["商业化", "产业报告"]),
        
        ("超导配对关联", "concept", "在量子计算机上首次观测到的超导现象，利用费米-哈伯德模型测量三种配对机制", 3,
         ["7408677623443647"],
         ["Quantum_Pairing_Observed.pdf"],
         ["费米-哈伯德模型", "超导"]),
        
        ("量子-经典单片全集成", "concept", "将量子芯片和经典控制电路集成在同一芯片上的长期愿景", 3,
         ["7408677623443647"],
         ["Cryo-CMOS_Quantum_Control_Global_Apex.pdf"],
         ["低温CMOS", "全集成"]),
        
        ("量子比特操控", "concept", "对量子比特执行单比特门和两比特门操作的技术，是量子计算的基础能力", 4,
         ["7411640966326739"],
         ["量子比特体系研讨.txt"],
         ["量子门", "门保真度"]),
        
        ("量子比特读取", "concept", "从量子比特中提取信息的技术，超导量子比特读取信号极微弱(-140dBm)", 4,
         ["7411640966326739"],
         ["超导量子比特读取技术解析.png"],
         ["频分复用", "读取保真度"]),
        
        ("迪文森佐准则 (DiVincenzo Criteria)", "concept", "实现量子计算所需的五个基本条件：可扩展量子比特、初始化、长相干时间、完备门集、独立测量", 4,
         ["7411640966326739"],
         ["量子比特体系研讨.txt"],
         ["量子比特体系", "相干时间"]),
        
        ("NISQ时代", "concept", "含噪声中等规模量子(Noisy Intermediate-Scale Quantum)时代，当前量子计算所处阶段", 4,
         ["7408677623443647"],
         ["龙沛洵报告"],
         ["量子噪声", "VQE", "QAOA"]),
        
        ("量子深度学习 (Quantum Deep Learning)", "concept", "利用量子或量子启发核心组件进行深度学习的新兴交叉领域", 3,
         ["7408677623443647"],
         ["Quantum Deep Learning: 郭国平.pdf"],
         ["量子机器学习", "变分量子电路"]),
        
        ("退相干 (Decoherence)", "concept", "量子系统与环境相互作用导致量子叠加态退化为经典态的过程", 5,
         ["7408677623443647"],
         ["龙沛洵报告", "量子工程学.pdf"],
         ["相干时间", "量子噪声"]),
        
        ("量子噪声 (Quantum Noise)", "concept", "量子计算过程中产生的各种噪声，包括退极化噪声、振幅阻尼等", 4,
         ["7408677623443647"],
         ["龙沛洵报告"],
         ["NISQ", "量子纠错"]),
        
        ("波函数坍缩 (Wave Function Collapse)", "concept", "量子测量导致波函数从叠加态投影到某个本征态的过程", 4,
         ["7408677623443647"],
         ["量子计算_掌握未来.pdf"],
         ["量子测量", "叠加态"]),
        
        ("腔量子电动力学 (Cavity QED)", "theory", "研究光与原子在光学谐振腔中相互作用的物理学分支，是Circuit QED的基础", 4,
         ["7408677623443647"],
         ["Circuit_Quantum_Electrodynamics.pdf"],
         ["Circuit QED", "谐振腔"]),
        
        ("薛定谔方程 (Schrödinger Equation)", "theory", "描述量子系统随时间演化的基本方程，是量子力学的核心方程", 5,
         ["7408677623443647"],
         ["量子力学(苏汝铿版).pdf"],
         ["波动力学", "量子力学"]),
        
        ("量子比特体系", "concept", "不同物理实现的量子比特类型，包括超导、离子阱、中性原子、拓扑、硅基等", 4,
         ["7411640966326739"],
         ["量子比特体系研讨.txt"],
         ["超导量子比特", "离子阱量子比特"]),
    ]
    
    for c in concepts:
        add_node(nodes, c[0], c[1], c[2], c[3], c[4], c[5], c[6])
    
    # ============================================================
    # PHASE 4: Hardware & Products
    # ============================================================
    
    hardware = [
        ("蜀山系列芯片", "hardware", "中微达信推出的低温CMOS量子测控芯片组，28nm工艺，4K极低温环境工作", 4,
         ["7408677623443647"],
         ["超导量子计算机集成趋势和低温电子系测控cmos芯片和.pdf"],
         ["中微达信", "低温CMOS"]),
        
        ("贡嘎芯片 (Konka)", "hardware", "中微达信蜀山系列中超导量子比特操控芯片，专用于高保真度双量子门操纵", 3,
         ["7408677623443647"],
         ["超导量子计算机集成趋势和低温电子系测控cmos芯片和.pdf"],
         ["蜀山系列", "量子比特操控"]),
        
        ("峨眉芯片 (Emei)", "hardware", "中微达信蜀山系列中超导量子比特读取芯片，优化频分复用读取", 3,
         ["7408677623443647"],
         ["超导量子计算机集成趋势和低温电子系测控cmos芯片和.pdf"],
         ["蜀山系列", "量子比特读取"]),
        
        ("西岭芯片 (Xiling)", "hardware", "中微达信蜀山系列中硅基量子比特操控芯片，填补国内硅基量子比特控制空白", 3,
         ["7408677623443647"],
         ["超导量子计算机集成趋势和低温电子系测控cmos芯片和.pdf"],
         ["蜀山系列", "硅基量子比特"]),
        
        ("Quantinuum Helios", "hardware", "Quantinuum公司的离子阱量子计算机，用于费米-哈伯德模型量子模拟", 4,
         ["7408677623443647"],
         ["Quantum_Pairing_Observed.pdf"],
         ["离子阱", "Quantinuum"]),
        
        ("稀释制冷机", "hardware", "将量子芯片冷却到接近绝对零度(mK级)的设备，超导量子计算的必要基础设施", 4,
         ["7408677623443647"],
         ["Cryo-CMOS_Quantum_Control_Global_Apex.pdf"],
         ["极低温", "超导量子比特"]),
        
        ("量子耦合线路", "hardware", "连接多个量子芯片的硬件互连方案，用于实现大规模分布式量子计算", 3,
         ["7408677623443647"],
         ["多量子芯片互连方案调研.pdf"],
         ["QPU互连", "分布式量子计算"]),
        
        ("可调耦合器", "hardware", "超导量子比特之间实现可控耦合的器件，用于两比特门操作", 3,
         ["7408677623443647"],
         ["多量子芯片互连方案调研.pdf"],
         ["两比特门", "超导量子比特"]),
    ]
    
    for h in hardware:
        add_node(nodes, h[0], h[1], h[2], h[3], h[4], h[5], h[6])
    
    # ============================================================
    # PHASE 5: Applications from IMA searches
    # ============================================================
    
    applications = [
        ("量子药物发现", "application", "利用量子计算加速药物发现过程，混合量子计算管线已在实际药物研发中应用", 4,
         ["7408677623443647"],
         ["s41598-024-67897-8.pdf"],
         ["量子化学", "药物设计"]),
        
        ("量子化学模拟", "application", "用量子计算机模拟分子和化学反应，是量子计算最重要的应用方向之一", 4,
         ["7408677623443647"],
         ["2509.19715v1.pdf"],
         ["VQE", "分子模拟"]),
        
        ("量子材料科学", "application", "利用量子计算研究新材料设计和性质预测，解决经典计算无法处理的复杂量子效应", 3,
         ["7408677623443647"],
         ["Quantum_Computing_The_Next_Era.pdf"],
         ["材料设计", "量子模拟"]),
        
        ("量子金融", "application", "将量子计算应用于金融风险评估、投资组合优化等金融领域", 3,
         ["7408677623443647"],
         ["Quantum_Computing_The_Next_Era.pdf"],
         ["投资组合优化", "风险评估"]),
        
        ("量子传感", "application", "利用量子效应实现超越经典极限的精密测量技术", 3,
         ["7412047272751870"],
         ["【国仪量子】量子精密测量行业赋能白皮书.pdf"],
         ["量子精密测量", "NV色心"]),
        
        ("量子基准测试 (Benchmarking)", "application", "评估和比较量子计算系统性能的方法和标准", 3,
         ["7408677623443647"],
         ["Quantum_Peak_Five_Level_Standard.pdf"],
         ["五级标准", "性能评估"]),
    ]
    
    for a in applications:
        add_node(nodes, a[0], a[1], a[2], a[3], a[4], a[5], a[6])
    
    # ============================================================
    # PHASE 6: Tools & Software
    # ============================================================
    
    tools = [
        ("本源量子云平台", "tool", "本源量子提供的量子计算云服务平台", 3,
         ["7408677623443647"],
         ["《量子计算与编程入门》.pdf"],
         ["量子编程", "云服务"]),
        
        ("NVentures", "tool", "英伟达风险投资部门，投资Quantinuum等量子计算公司", 2,
         ["7408677623443647"],
         ["英伟达投资的哪几家量子计算公司.pdf"],
         ["英伟达", "投资"]),
    ]
    
    for t in tools:
        add_node(nodes, t[0], t[1], t[2], t[3], t[4], t[5])
    
    # ============================================================
    # PHASE 7: Additional Concepts (from deep knowledge)
    # ============================================================
    
    more_concepts = [
        ("量子比特读取技术", "concept", "从量子比特提取量子态信息的技术，超导量子比特信号极微弱需特殊放大方案", 4,
         ["7411640966326739"],
         ["超导量子比特读取技术解析.png"],
         ["频分复用", "参量放大器"]),
        
        ("频分复用读取", "concept", "使用不同频率信道同时读取多个量子比特的技术", 3,
         ["7411640966326739"],
         ["超导量子比特读取技术解析.png"],
         ["量子比特读取", "多比特读取"]),
        
        ("参量放大器 (JPA/JPAs)", "concept", "用于放大微弱量子信号的近量子极限放大器，是量子比特读取的关键组件", 3,
         ["7411640966326739"],
         ["超导量子比特读取技术解析.png"],
         ["量子比特读取", "低噪声放大"]),
        
        ("量子纠错码", "concept", "通过编码逻辑量子比特到多个物理量子比特来检测和纠正错误的编码方案", 5,
         ["7408677623443647", "7411640966326739"],
         ["量子工程学_构建与控制.pdf"],
         ["逻辑量子比特", "表面码"]),
        
        ("表面码 (Surface Code)", "concept", "最接近实用的量子纠错码方案，需要物理量子比特二维阵列", 4,
         ["7408677623443647"],
         ["量子工程学_构建与控制.pdf"],
         ["量子纠错码", "拓扑保护"]),
        
        ("量子体积 (Quantum Volume)", "concept", "IBM提出的衡量量子计算机整体性能的综合指标", 3,
         ["7408677623443647"],
         ["Quantum_Peak_Five_Level_Standard.pdf"],
         ["Benchmark", "性能评估"]),
        
        ("门保真度 (Gate Fidelity)", "concept", "衡量量子门操作精确度的指标，是量子比特性能的关键参数", 4,
         ["7411640966326739"],
         ["量子比特体系研讨.txt"],
         ["量子门", "错误率"]),
        
        ("读取保真度 (Readout Fidelity)", "concept", "衡量量子比特读取准确度的指标", 3,
         ["7411640966326739"],
         ["超导量子比特读取技术解析.png"],
         ["量子比特读取", "信噪比"]),
        
        ("相干时间 (Coherence Time)", "concept", "量子比特保持叠加态的时间长度，T1(能量弛豫)和T2(相位退相干)", 5,
         ["7411640966326739"],
         ["量子比特体系研讨.txt"],
         ["退相干", "T1", "T2"]),
        
        ("量子互连 (Quantum Interconnect)", "concept", "连接多个量子处理单元(QPU)的技术，包括量子隐形传态、量子耦合等方案", 3,
         ["7408677623443647"],
         ["多量子芯片互连方案调研.pdf", "Quantum_Scaling_Architecture.pdf"],
         ["QPU互连", "分布式量子计算"]),
        
        ("3D堆叠互连", "concept", "通过三维堆叠技术实现量子芯片间高密度连接的方案", 3,
         ["7408677623443647"],
         ["多量子芯片互连方案调研.pdf"],
         ["QPU互连", "芯片堆叠"]),
        
        ("量子电路编织 (Circuit Knitting)", "concept", "将大规模量子电路分割为多个小电路在不同QPU上执行的技术", 3,
         ["7408677623443647"],
         ["多量子芯片互连方案调研.pdf"],
         ["分布式量子计算", "QPU互连"]),
        
        ("非阿贝尔任意子 (Non-Abelian Anyon)", "concept", "其交换操作不可交换的任意子，是实现拓扑量子计算的关键", 4,
         ["7441506466037417"],
         ["拓扑量子计算研究报告.docx"],
         ["任意子", "拓扑量子计算"]),
        
        ("拓扑保护 (Topological Protection)", "concept", "利用拓扑性质保护量子信息免受局部噪声干扰的机制", 4,
         ["7441506466037417"],
         ["拓扑量子计算研究报告.docx"],
         ["拓扑量子计算", "容错"]),
        
        ("量子比特初始化", "concept", "将量子比特设置到已知状态(通常为|0⟩)的过程", 3,
         ["7411640966326739"],
         ["量子比特体系研讨.txt"],
         ["迪文森佐准则"]),
        
        ("逻辑量子比特 (Logical Qubit)", "concept", "通过量子纠错编码由多个物理量子比特构成的容错量子比特", 5,
         ["7408677623443647", "7425064727240963"],
         ["Quantum_Dawn_Global_Strategy.pdf"],
         ["量子纠错", "表面码"]),
        
        ("量子组合优化", "application", "利用量子计算解决组合优化问题，如旅行商问题、最大割问题等", 3,
         ["7408677623443647"],
         ["龙沛洵报告"],
         ["QAOA", "组合爆炸"]),
        
        ("量子模拟 (Quantum Simulation)", "application", "使用量子计算机模拟其他量子系统的行为，Feynman最初提出量子计算的动机", 4,
         ["7408677623443647"],
         ["龙沛洵报告", "Quantum_Pairing_Observed.pdf"],
         ["费米-哈伯德模型", "量子化学"]),
        
        ("混合量子药物发现管线", "tool", "Nature发表的实际量子药物发现流程，结合量子计算和经典计算", 3,
         ["7408677623443647"],
         ["s41598-024-67897-8.pdf"],
         ["量子药物发现", "量子化学"]),
        
        ("中关村量子产业联盟报告", "tool", "中关村量子产业联盟发布的量子计算战略报告《量子计算：掌握未来》", 2,
         ["7408677623443647"],
         ["量子计算_掌握未来.pdf"],
         ["产业报告"]),
        
        ("量子比特体系比较", "concept", "不同物理实现量子比特的优缺点比较：超导、离子阱、中性原子、拓扑、硅基、光量子", 4,
         ["7411640966326739"],
         ["量子比特体系研讨.txt"],
         ["超导量子比特", "离子阱量子比特"]),
        
        ("量子工程学", "concept", "将量子物理原理转化为功能性量子器件和系统的工程学科", 4,
         ["7408677623443647", "7412047272751870"],
         ["量子工程学.pdf", "量子工程学_构建与控制.pdf"],
         ["金贻荣", "Zagoskin"]),
        
        ("量子总线 (Quantum Bus)", "concept", "在量子处理器中连接不同量子比特的谐振腔或耦合结构", 3,
         ["7408677623443647"],
         ["量子工程学_构建与控制.pdf"],
         ["谐振腔", "Circuit QED"]),
        
        ("原子重用与补充", "concept", "中性原子量子计算中，在计算过程中重新加载原子以维持量子比特数的技术", 3,
         ["7408677623443647"],
         ["Enduring_Quantum_Logic.pdf"],
         ["中性原子", "分区架构"]),
    ]
    
    for c in more_concepts:
        add_node(nodes, c[0], c[1], c[2], c[3], c[4], c[5], c[6])
    
    # ============================================================
    # PHASE 8: Build Relationships
    # ============================================================
    
    # Company relationships
    company_rels = [
        ("相干科技 (Coherent Quantum)", "金贻荣", "developed_by", "金贻荣创建", 5),
        ("相干科技 (Coherent Quantum)", "北京量子信息科学研究院 (BAQIS)", "derives_from", "由量子院孵化", 5),
        ("相干科技 (Coherent Quantum)", "超导量子比特 (Transmon)", "uses", "使用超导量子比特技术路线", 5),
        ("相干科技", "北京量子信息科学研究院 (BAQIS)", "derives_from", "由量子院孵化", 5),
        ("相干科技", "超导量子比特 (Transmon)", "uses", "使用超导量子比特技术路线", 4),
        ("中微达信", "蜀山系列芯片", "developed_by", "中微达信研发", 4),
        ("中微达信", "低温CMOS", "uses", "采用28nm CMOS工艺", 4),
        ("国仪量子 (CIQTEK)", "量子精密测量", "applies_to", "专注量子精密测量", 4),
        ("国仪量子 (CIQTEK)", "量子传感", "applies_to", "用量子传感赋能千行百业", 3),
        ("瀚海凌潮", "量子云平台", "developed_by", "构建量子融合基础设施", 3),
        ("本源量子", "郭国平", "developed_by", "郭国平创立", 4),
        ("本源量子", "量子编程", "applies_to", "提供量子编程平台", 3),
        ("本源量子", "本源量子云平台", "developed_by", "运营云平台", 3),
        ("QureGenAI", "量子药物发现", "applies_to", "量子药物研发", 3),
        ("QureGenAI", "量子化学模拟", "applies_to", "量子化学计算", 3),
        ("Quantinuum", "离子阱量子比特", "uses", "使用离子阱技术路线", 5),
        ("Quantinuum", "Quantinuum Helios", "developed_by", "推出Helios量子计算机", 4),
        ("Quantinuum", "英伟达 (NVIDIA)", "related_to", "NVentures投资", 3),
    ]
    
    for src, tgt, rel, label, weight in company_rels:
        src_id = find_node_id(nodes, src)
        tgt_id = find_node_id(nodes, tgt)
        if src_id and tgt_id:
            add_edge(edges, src_id, tgt_id, rel, label, weight)
    
    # People relationships
    people_rels = [
        ("金贻荣", "相干科技 (Coherent Quantum)", "developed_by", "创始人", 5),
        ("金贻荣", "量子工程学", "developed_by", "翻译Zagoskin著作", 4),
        ("金贻荣", "超导量子比特 (Transmon)", "related_to", "20年超导量子计算研究", 5),
        ("郭国平", "本源量子", "developed_by", "创始人", 4),
        ("郭国平", "量子深度学习 (Quantum Deep Learning)", "related_to", "论文作者", 3),
        ("郭光灿", "本源量子", "related_to", "参与著书", 3),
        ("陈昭昀", "量子编程", "related_to", "合著编程入门", 3),
        ("Alexandre Blais", "Circuit QED", "developed_by", "Circuit QED综述作者", 5),
        ("Alexandre Blais", "腔量子电动力学 (Cavity QED)", "related_to", "拓展Cavity QED到电路", 4),
        ("David D. Awschalom", "量子传感", "related_to", "量子传感综述", 3),
        ("William D. Oliver", "超导量子比特 (Transmon)", "related_to", "超导量子计算专家", 4),
        ("A.M. Zagoskin", "量子工程学", "developed_by", "著作者", 4),
    ]
    
    for src, tgt, rel, label, weight in people_rels:
        src_id = find_node_id(nodes, src)
        tgt_id = find_node_id(nodes, tgt)
        if src_id and tgt_id:
            add_edge(edges, src_id, tgt_id, rel, label, weight)
    
    # Concept relationships
    concept_rels = [
        ("拓扑量子计算", "任意子 (Anyon)", "uses", "利用任意子实现", 5),
        ("拓扑量子计算", "马约拉纳零模 (Majorana Zero Mode)", "uses", "候选实现方式", 4),
        ("拓扑量子计算", "拓扑保护 (Topological Protection)", "uses", "利用拓扑保护", 5),
        ("拓扑量子计算", "量子纠错", "related_to", "从物理层面解决容错", 4),
        ("任意子 (Anyon)", "非阿贝尔任意子 (Non-Abelian Anyon)", "part_of", "非阿贝尔任意子是关键子类", 4),
        ("马约拉纳零模 (Majorana Zero Mode)", "非阿贝尔任意子 (Non-Abelian Anyon)", "related_to", "满足非阿贝尔统计", 4),
        ("费米-哈伯德模型 (Fermi-Hubbard Model)", "量子模拟 (Quantum Simulation)", "applies_to", "量子模拟的重要目标", 4),
        ("费米-哈伯德模型 (Fermi-Hubbard Model)", "超导配对关联", "related_to", "研究超导配对机制", 3),
        ("量子增强认知推荐算法", "VQE (变分量子本征求解器)", "uses", "使用变分量子电路", 3),
        ("量子增强认知推荐算法", "量子-经典混合框架 (Hybrid Quantum-Classical)", "uses", "采用混合优化框架", 3),
        ("生成式量子本征求解器 (GQE)", "量子化学模拟", "applies_to", "用于量子化学计算", 3),
        ("布线丛林 (Wiring Jungle)", "控制墙 (Control Wall)", "part_of", "布线丛林是控制墙的核心表现", 5),
        ("控制墙 (Control Wall)", "低温CMOS", "derives_from", "低温CMOS是解决控制墙的方案", 4),
        ("量子隐形传态 (Quantum Teleportation)", "量子互连 (Quantum Interconnect)", "enables", "实现QPU间量子态传输", 4),
        ("量子隐形传态 (Quantum Teleportation)", "量子纠缠 (Entanglement)", "uses", "利用量子纠缠", 5),
        ("量子性能分级标准 (Five-Level Standard)", "量子基准测试 (Benchmarking)", "part_of", "是Benchmarking的具体框架", 4),
        ("中性原子分区架构", "中性原子量子比特", "uses", "使用中性原子平台", 3),
        ("中性原子分区架构", "原子重用与补充", "uses", "实现原子重用和补充", 3),
        ("量子计算产业化", "逻辑量子比特 (Logical Qubit)", "related_to", "产业从物理比特向逻辑比特转变", 5),
        ("量子比特操控", "门保真度 (Gate Fidelity)", "related_to", "操控精度的关键指标", 4),
        ("量子比特读取", "读取保真度 (Readout Fidelity)", "related_to", "读取准确度的关键指标", 4),
        ("量子比特读取", "频分复用读取", "uses", "使用频分复用技术", 3),
        ("量子比特读取", "参量放大器 (JPA/JPAs)", "uses", "使用参量放大器放大信号", 4),
        ("迪文森佐准则 (DiVincenzo Criteria)", "量子比特体系", "related_to", "定义量子比特体系要求", 4),
        ("迪文森佐准则 (DiVincenzo Criteria)", "量子比特初始化", "related_to", "要求初始化能力", 3),
        ("迪文森佐准则 (DiVincenzo Criteria)", "相干时间 (Coherence Time)", "related_to", "要求长相干时间", 3),
        ("NISQ时代", "量子噪声 (Quantum Noise)", "related_to", "NISQ时代受噪声限制", 4),
        ("NISQ时代", "VQE (变分量子本征求解器)", "uses", "NISQ时代代表算法", 4),
        ("NISQ时代", "QAOA (量子近似优化算法)", "uses", "NISQ时代代表算法", 4),
        ("退相干 (Decoherence)", "相干时间 (Coherence Time)", "related_to", "退相干决定相干时间", 5),
        ("退相干 (Decoherence)", "量子噪声 (Quantum Noise)", "related_to", "退相干是噪声的表现", 4),
        ("波函数坍缩 (Wave Function Collapse)", "量子测量", "related_to", "测量导致坍缩", 4),
        ("腔量子电动力学 (Cavity QED)", "Circuit QED", "derives_from", "Circuit QED是Cavity QED的电路实现", 5),
        ("薛定谔方程 (Schrödinger Equation)", "波函数", "uses", "描述波函数演化", 5),
        ("量子深度学习 (Quantum Deep Learning)", "量子机器学习", "part_of", "是量子机器学习的子领域", 3),
        ("量子总线 (Quantum Bus)", "Circuit QED", "part_of", "Circuit QED中的连接机制", 4),
        ("量子互连 (Quantum Interconnect)", "多芯片量子计算", "enables", "实现多芯片量子计算", 4),
        ("量子互连 (Quantum Interconnect)", "3D堆叠互连", "uses", "3D堆叠是互连方案之一", 3),
        ("量子互连 (Quantum Interconnect)", "量子电路编织 (Circuit Knitting)", "uses", "电路编织是软件互连方案", 3),
        ("量子比特体系", "超导量子比特 (Transmon)", "part_of", "超导是主要体系之一", 4),
        ("量子比特体系", "离子阱量子比特", "part_of", "离子阱是主要体系之一", 4),
        ("量子比特体系", "中性原子量子比特", "part_of", "中性原子是新兴体系", 4),
        ("量子比特体系", "拓扑量子计算", "part_of", "拓扑是前沿方向", 3),
        ("量子工程学", "金贻荣", "developed_by", "金贻荣翻译", 4),
        ("量子总线 (Quantum Bus)", "谐振腔", "uses", "使用谐振腔作为量子总线", 3),
        ("逻辑量子比特 (Logical Qubit)", "量子纠错码", "uses", "通过纠错码构建", 5),
        ("逻辑量子比特 (Logical Qubit)", "表面码 (Surface Code)", "uses", "表面码是主流编码方案", 4),
        ("量子组合优化", "QAOA (量子近似优化算法)", "uses", "使用QAOA求解", 4),
        ("量子化学模拟", "VQE (变分量子本征求解器)", "uses", "使用VQE求解", 4),
        ("量子药物发现", "混合量子药物发现管线", "uses", "使用混合管线", 3),
        ("量子材料科学", "量子模拟 (Quantum Simulation)", "uses", "使用量子模拟方法", 3),
    ]
    
    for src, tgt, rel, label, weight in concept_rels:
        src_id = find_node_id(nodes, src)
        tgt_id = find_node_id(nodes, tgt)
        if src_id and tgt_id:
            add_edge(edges, src_id, tgt_id, rel, label, weight)
    
    # Hardware relationships
    hardware_rels = [
        ("蜀山系列芯片", "贡嘎芯片 (Konka)", "part_of", "超导操控芯片", 4),
        ("蜀山系列芯片", "峨眉芯片 (Emei)", "part_of", "超导读取芯片", 4),
        ("蜀山系列芯片", "西岭芯片 (Xiling)", "part_of", "硅基操控芯片", 4),
        ("贡嘎芯片 (Konka)", "量子比特操控", "enables", "实现高保真度操控", 4),
        ("峨眉芯片 (Emei)", "量子比特读取", "enables", "实现频分复用读取", 4),
        ("西岭芯片 (Xiling)", "硅基量子比特", "enables", "实现硅基量子比特控制", 3),
        ("Quantinuum Helios", "费米-哈伯德模型 (Fermi-Hubbard Model)", "applies_to", "用于费米-哈伯德模型模拟", 3),
        ("稀释制冷机", "超导量子比特 (Transmon)", "enables", "提供极低温运行环境", 5),
        ("量子耦合线路", "量子互连 (Quantum Interconnect)", "part_of", "是互连方案的硬件实现", 3),
        ("可调耦合器", "超导量子比特 (Transmon)", "part_of", "超导比特间的耦合器件", 4),
    ]
    
    for src, tgt, rel, label, weight in hardware_rels:
        src_id = find_node_id(nodes, src)
        tgt_id = find_node_id(nodes, tgt)
        if src_id and tgt_id:
            add_edge(edges, src_id, tgt_id, rel, label, weight)
    
    # Additional cross-links to existing nodes
    cross_rels = [
        ("低温CMOS", "中微达信", "developed_by", "中微达信推出低温CMOS方案", 4),
        ("低温CMOS", "控制墙 (Control Wall)", "related_to", "低温CMOS解决控制墙问题", 4),
        ("量子编程", "Qiskit", "uses", "Qiskit是量子编程框架", 4),
        ("量子编程", "本源量子", "related_to", "本源量子提供编程平台", 3),
        ("北京量子信息科学研究院 (BAQIS)", "超导量子比特 (Transmon)", "uses", "专注超导量子比特技术", 4),
        ("光子盒研究院", "量子计算产业化", "related_to", "发布产业报告", 3),
        ("中国计算机学会量子计算大会 (CQCC)", "量子性能分级标准 (Five-Level Standard)", "developed_by", "制定五级标准", 3),
        ("中关村量子产业联盟", "量子计算产业化", "related_to", "推动产业化", 3),
        ("英伟达 (NVIDIA)", "NVentures", "developed_by", "NVentures是英伟达投资部门", 3),
        ("英伟达 (NVIDIA)", "Quantinuum", "related_to", "NVentures投资Quantinuum", 3),
        ("Quantinuum Helios", "离子阱量子比特", "uses", "使用离子阱技术", 4),
        ("逻辑量子比特 (Logical Qubit)", "量子计算产业化", "enables", "逻辑量子比特是产业化的关键", 4),
        ("量子-经典单片全集成", "低温CMOS", "uses", "低温CMOS是全集成的基础", 3),
        ("量子体积 (Quantum Volume)", "量子基准测试 (Benchmarking)", "part_of", "是Benchmarking的指标之一", 3),
        ("相干时间 (Coherence Time)", "量子比特体系", "related_to", "不同体系相干时间差异大", 4),
        ("退相干 (Decoherence)", "量子纠错", "related_to", "量子纠错对抗退相干", 5),
        ("量子比特读取技术", "量子比特读取", "part_of", "读取技术的总称", 4),
    ]
    
    for src, tgt, rel, label, weight in cross_rels:
        src_id = find_node_id(nodes, src)
        tgt_id = find_node_id(nodes, tgt)
        if src_id and tgt_id:
            add_edge(edges, src_id, tgt_id, rel, label, weight)
    
    # ============================================================
    # Update metadata and save
    # ============================================================
    
    data['metadata']['node_count'] = len(nodes)
    data['metadata']['edge_count'] = len(edges)
    data['metadata']['last_updated'] = '2026-06-13'
    data['metadata']['expansion_notes'] = '从5个IMA知识库搜索结果中提取实体，增加公司、人物、概念、硬件、应用等节点'
    
    save_graph(data)
    print(f"Final: {len(nodes)} nodes, {len(edges)} edges")
    
    # Print node type distribution
    type_counts = {}
    for n in nodes:
        t = n['type']
        type_counts[t] = type_counts.get(t, 0) + 1
    print("\nNode type distribution:")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")
    
    # Print edge type distribution
    edge_type_counts = {}
    for e in edges:
        t = e.get('label', 'unknown')
        edge_type_counts[t] = edge_type_counts.get(t, 0) + 1
    print("\nEdge type distribution:")
    for t, c in sorted(edge_type_counts.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")

if __name__ == '__main__':
    main()
