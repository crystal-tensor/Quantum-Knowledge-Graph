import json

# Initialize graph data structure
graph_data = {
    "metadata": {
        "title": "量子计算知识图谱",
        "description": "基于5个IMA知识库构建的量子计算知识图谱",
        "created_at": "2026-06-13",
        "node_count": 0,
        "edge_count": 0,
        "source_knowledge_bases": [
            "量子计算学习材料",
            "量子产业研究报告", 
            "金贻荣老师的直播课件",
            "量子计算",
            "李博士的项目"
        ]
    },
    "nodes": [],
    "edges": [],
    "categories": {
        "量子计算基础": [],
        "量子算法": [],
        "硬件技术路线": [],
        "产业链与企业": [],
        "应用场景": [],
        "市场与投资": [],
        "量子纠错": [],
        "量子软件与工具": [],
        "量子通信与安全": [],
        "量子传感与测量": []
    }
}

# Define nodes
nodes = []

# Core concepts (concept)
concepts = [
    ("node_001", "量子比特 (Qubit)", "concept", "量子计算的基本信息单位，可以处于0和1的叠加态", 5),
    ("node_002", "叠加态 (Superposition)", "concept", "量子系统可以同时处于多个状态的叠加", 5),
    ("node_003", "量子纠缠 (Entanglement)", "concept", "多个量子粒子之间的非局域关联现象", 5),
    ("node_004", "量子门 (Quantum Gate)", "concept", "对量子比特进行操作的基本单元", 4),
    ("node_005", "量子电路 (Quantum Circuit)", "concept", "由量子门组成的计算流程", 4),
    ("node_006", "量子测量 (Measurement)", "concept", "将量子态坍缩为经典信息的过程", 4),
    ("node_007", "布洛赫球 (Bloch Sphere)", "concept", "可视化单个量子比特状态的几何表示", 3),
    ("node_008", "量子退相干 (Decoherence)", "concept", "量子态因与环境相互作用而失去量子特性", 4),
    ("node_009", "量子噪声 (Quantum Noise)", "concept", "导致量子计算错误的随机扰动", 3),
    ("node_010", "量子优越性 (Quantum Supremacy)", "concept", "量子计算机在特定任务上超越最快经典计算机", 4),
    ("node_011", "容错量子计算 (FTQC)", "concept", "能够纠正错误的量子计算范式", 5),
    ("node_012", "NISQ (Noisy Intermediate-Scale Quantum)", "concept", "有噪声的中等规模量子计算时代", 4),
]

# Algorithms (algorithm)
algorithms = [
    ("node_101", "Shor算法", "algorithm", "用于整数分解的量子算法，可破解RSA加密", 5),
    ("node_102", "Grover算法", "algorithm", "量子搜索算法，平方加速", 4),
    ("node_103", "VQE (变分量子本征求解器)", "algorithm", "用于寻找哈密顿量基态的混合量子经典算法", 4),
    ("node_104", "QAOA (量子近似优化算法)", "algorithm", "用于组合优化问题的量子算法", 4),
    ("node_105", "量子傅里叶变换 (QFT)", "algorithm", "量子版本的离散傅里叶变换", 4),
    ("node_106", "量子相位估计 (QPE)", "algorithm", "估计酉算子特征相位的量子算法", 3),
    ("node_107", "HHL算法", "algorithm", "求解线性系统的量子算法", 3),
    ("node_108", "量子退火 (Quantum Annealing)", "algorithm", "基于绝热量子计算的优化方法", 3),
    ("node_109", "QOV (Quantum Optimization Variational)", "algorithm", "变分量子优化算法", 2),
]

# Hardware (hardware)
hardware = [
    ("node_201", "超导量子计算", "hardware", "使用超导电路实现量子比特的技术路线", 5),
    ("node_202", "离子阱 (Ion Trap)", "hardware", "使用囚禁离子作为量子比特的技术路线", 4),
    ("node_203", "光量子计算 (Photonic)", "hardware", "使用光子作为量子比特的技术路线", 4),
    ("node_204", "中性原子 (Neutral Atom)", "hardware", "使用中性原子作为量子比特的技术路线", 4),
    ("node_205", "拓扑量子计算", "hardware", "利用拓扑保护实现容错量子计算", 3),
    ("node_206", "量子点 (Quantum Dot)", "hardware", "使用半导体量子点实现量子比特", 2),
    ("node_207", "核磁共振 (NMR)", "hardware", "早期量子计算实现方式", 2),
    ("node_208", "里德堡原子 (Rydberg Atom)", "hardware", "用于中性原子量子计算的特殊原子态", 3),
]

# Companies (company)
companies = [
    ("node_301", "IBM", "company", "美国科技公司，IBM Quantum的开发者", 5),
    ("node_302", "Google", "company", "美国科技公司，Willow量子处理器的开发者", 5),
    ("node_303", "IQM", "company", "欧洲超导量子计算公司", 4),
    ("node_304", "Rigetti", "company", "美国超导量子计算公司", 3),
    ("node_305", "IonQ", "company", "美国离子阱量子计算公司", 4),
    ("node_306", "PsiQuantum", "company", "美国光量子计算公司", 3),
    ("node_307", "本源量子", "company", "中国量子计算公司", 3),
    ("node_308", "国盾量子", "company", "中国量子通信公司", 3),
    ("node_309", "图灵量子", "company", "中国量子计算公司", 2),
    ("node_310", "中科量枢", "company", "中国量子软件公司", 2),
    ("node_311", "相干科技 (Coherent Quantum)", "company", "中国超导量子计算公司，金贻荣博士创立", 4),
    ("node_312", "QuEra", "company", "美国中性原子量子计算公司", 3),
    ("node_313", "Quantinuum", "company", "美国离子阱量子计算公司（霍尼韦尔与Cambridge Quantum合并）", 4),
]

# Applications (application)
applications = [
    ("node_401", "密码学 (Cryptography)", "application", "量子计算在密码学的应用", 4),
    ("node_402", "药物发现 (Drug Discovery)", "application", "量子计算在药物发现的应用", 4),
    ("node_403", "金融优化 (Financial Optimization)", "application", "量子计算在金融优化的应用", 3),
    ("node_404", "机器学习 (Machine Learning)", "application", "量子机器学习", 4),
    ("node_405", "材料科学 (Materials Science)", "application", "量子计算在材料科学的应用", 3),
    ("node_406", "化学模拟 (Chemical Simulation)", "application", "量子计算在化学模拟的应用", 4),
    ("node_407", "物流优化 (Logistics)", "application", "量子计算在物流优化的应用", 3),
    ("node_408", "人工智能 (AI)", "application", "量子计算与人工智能的结合", 4),
]

# People (person)
people = [
    ("node_501", "金贻荣", "person", "相干科技创始人，中国超导量子计算专家", 4),
    ("node_502", "郭光灿", "person", "中国量子信息学家，中国科学院院士", 4),
    ("node_503", "郭国平", "person", "本源量子创始人", 3),
    ("node_504", "Michael Nielsen", "person", "《量子计算与量子信息》作者", 3),
    ("node_505", "John Preskill", "person", "美国理论物理学家，提出NISQ概念", 4),
    ("node_506", "David Deutsch", "person", "量子计算理论奠基人之一", 3),
]

# Protocols (protocol)
protocols = [
    ("node_601", "量子密钥分发 (QKD)", "protocol", "利用量子力学原理实现安全密钥分发", 4),
    ("node_602", "抗量子密码 (PQC)", "protocol", "能够抵抗量子计算攻击的密码算法", 4),
    ("node_603", "量子隐形传态 (Teleportation)", "protocol", "利用纠缠实现量子态传输", 3),
    ("node_604", "表面码 (Surface Code)", "protocol", "最常用的量子纠错码之一", 4),
    ("node_605", "色码 (Color Code)", "protocol", "另一种量子纠错码", 3),
]

# Tools (tool)
tools = [
    ("node_701", "Qiskit", "tool", "IBM的量子计算软件开发框架", 4),
    ("node_702", "Cirq", "tool", "Google的量子计算软件开发框架", 4),
    ("node_703", "Q#", "tool", "微软的量子编程语言", 3),
    ("node_704", "PennyLane", "tool", "Xanadu的量子机器学习框架", 3),
    ("node_705", "QuTiP", "tool", "量子光学和量子信息处理的Python库", 3),
]

# Materials (material)
materials = [
    ("node_801", "约瑟夫森结 (Josephson Junction)", "material", "超导量子比特的核心元件", 4),
    ("node_802", "稀释制冷机 (Dilution Refrigerator)", "material", "将量子芯片冷却到mK温度的设备", 4),
    ("node_803", "超导传输子 (Transmon)", "material", "一种超导量子比特设计", 3),
    ("node_804", "微波谐振器 (Microwave Resonator)", "material", "用于读取和控制超导量子比特", 3),
]

# Theories (theory)
theories = [
    ("node_901", "量子力学 (Quantum Mechanics)", "theory", "描述微观世界物理规律的理论", 5),
    ("node_902", "量子信息论 (Quantum Information Theory)", "theory", "研究量子系统信息处理能力的理论", 4),
    ("node_903", "量子场论 (Quantum Field Theory)", "theory", "结合量子力学和狭义相对论的理论", 3),
    ("node_904", "量子纠错理论 (Quantum Error Correction Theory)", "theory", "研究如何保护和纠正量子信息的理论", 4),
]

# Combine all nodes
all_nodes = concepts + algorithms + hardware + companies + applications + people + protocols + tools + materials + theories

# Add nodes to graph_data
for node_id, label, node_type, description, importance in all_nodes:
    graph_data["nodes"].append({
        "id": node_id,
        "label": label,
        "type": node_type,
        "description": description,
        "properties": {
            "importance": importance,
            "source_documents": [],
            "related_terms": []
        }
    })
    # Add to category
    if node_type == "concept":
        graph_data["categories"]["量子计算基础"].append(node_id)
    elif node_type == "algorithm":
        graph_data["categories"]["量子算法"].append(node_id)
    elif node_type == "hardware":
        graph_data["categories"]["硬件技术路线"].append(node_id)
    elif node_type == "company":
        graph_data["categories"]["产业链与企业"].append(node_id)
    elif node_type == "application":
        graph_data["categories"]["应用场景"].append(node_id)
    elif node_type == "protocol":
        graph_data["categories"]["量子通信与安全"].append(node_id)
    elif node_type == "tool":
        graph_data["categories"]["量子软件与工具"].append(node_id)
    elif node_type == "theory":
        graph_data["categories"]["量子计算基础"].append(node_id)

# Define edges (relationships)
edges = [
    # Concepts relationships
    ("node_001", "node_002", "related_to", 0.9),
    ("node_001", "node_003", "related_to", 0.9),
    ("node_002", "node_003", "related_to", 0.8),
    ("node_001", "node_004", "part_of", 0.7),
    ("node_004", "node_005", "part_of", 0.8),
    ("node_005", "node_006", "related_to", 0.6),
    ("node_001", "node_008", "related_to", 0.8),
    ("node_008", "node_009", "caused_by", 0.7),
    ("node_001", "node_010", "enables", 0.6),
    ("node_010", "node_011", "related_to", 0.7),
    ("node_011", "node_012", "related_to", 0.8),
    
    # Algorithms using concepts
    ("node_101", "node_105", "uses", 0.9),
    ("node_101", "node_106", "uses", 0.8),
    ("node_102", "node_005", "uses", 0.7),
    ("node_103", "node_405", "applies_to", 0.8),
    ("node_104", "node_403", "applies_to", 0.8),
    ("node_105", "node_005", "part_of", 0.7),
    
    # Hardware implements qubits
    ("node_201", "node_001", "implements", 0.9),
    ("node_202", "node_001", "implements", 0.9),
    ("node_203", "node_001", "implements", 0.8),
    ("node_204", "node_001", "implements", 0.8),
    ("node_205", "node_001", "implements", 0.7),
    
    # Hardware uses materials
    ("node_201", "node_801", "uses", 0.9),
    ("node_201", "node_802", "uses", 0.9),
    ("node_201", "node_803", "uses", 0.8),
    ("node_201", "node_804", "uses", 0.8),
    
    # Companies develop hardware/software
    ("node_301", "node_201", "develops", 0.8),
    ("node_301", "node_701", "develops", 0.9),
    ("node_302", "node_201", "develops", 0.8),
    ("node_302", "node_702", "develops", 0.7),
    ("node_303", "node_201", "develops", 0.8),
    ("node_304", "node_201", "develops", 0.7),
    ("node_305", "node_202", "develops", 0.8),
    ("node_306", "node_203", "develops", 0.7),
    ("node_311", "node_201", "develops", 0.8),
    ("node_311", "node_501", "founded_by", 0.9),
    ("node_313", "node_202", "develops", 0.8),
    ("node_312", "node_204", "develops", 0.8),
    
    # Applications use algorithms
    ("node_401", "node_101", "uses", 0.9),
    ("node_401", "node_602", "related_to", 0.8),
    ("node_402", "node_103", "uses", 0.8),
    ("node_402", "node_406", "related_to", 0.9),
    ("node_403", "node_104", "uses", 0.8),
    ("node_404", "node_103", "uses", 0.8),
    ("node_404", "node_102", "uses", 0.7),
    ("node_405", "node_103", "uses", 0.8),
    ("node_406", "node_005", "uses", 0.7),
    ("node_408", "node_404", "related_to", 0.9),
    
    # Theories derive concepts
    ("node_901", "node_001", "derives_from", 0.9),
    ("node_901", "node_002", "derives_from", 0.9),
    ("node_901", "node_003", "derives_from", 0.9),
    ("node_902", "node_901", "derives_from", 0.8),
    ("node_904", "node_902", "derives_from", 0.9),
    
    # Protocols use concepts
    ("node_601", "node_003", "uses", 0.9),
    ("node_601", "node_901", "uses", 0.8),
    ("node_602", "node_101", "addresses", 0.9),
    ("node_604", "node_904", "part_of", 0.9),
    
    # People contribute to field
    ("node_501", "node_201", "contributes_to", 0.9),
    ("node_501", "node_311", "founded", 0.9),
    ("node_502", "node_901", "contributes_to", 0.8),
    ("node_503", "node_307", "founded", 0.9),
    ("node_504", "node_902", "contributes_to", 0.7),
    ("node_505", "node_012", "coined", 0.9),
    ("node_506", "node_901", "contributes_to", 0.8),
    
    # Tools enable development
    ("node_701", "node_301", "developed_by", 0.9),
    ("node_702", "node_302", "developed_by", 0.9),
    ("node_703", "node_301", "developed_by", 0.6),
    ("node_704", "node_404", "enables", 0.7),
    ("node_705", "node_406", "enables", 0.7),
]

# Add edges to graph_data
for source, target, label, weight in edges:
    graph_data["edges"].append({
        "source": source,
        "target": target,
        "label": label,
        "weight": weight
    })

# Update metadata
graph_data["metadata"]["node_count"] = len(graph_data["nodes"])
graph_data["metadata"]["edge_count"] = len(graph_data["edges"])

# Save to file
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GRAPH_FILE = os.environ.get("GRAPH_DATA_PATH", os.path.join(BASE_DIR, "graph", "graph_data.json"))
os.makedirs(os.path.dirname(GRAPH_FILE), exist_ok=True)

with open(GRAPH_FILE, "w", encoding="utf-8") as f:
    json.dump(graph_data, f, ensure_ascii=False, indent=2)

print(f"Graph data created with {len(graph_data['nodes'])} nodes and {len(graph_data['edges'])} edges")
