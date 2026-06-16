import json

# Load existing graph data
with open("/Users/danielcrystal/WorkBuddy/2026-06-13-17-30-18/graph_data.json", "r", encoding="utf-8") as f:
    graph_data = json.load(f)

# Additional nodes from IMA knowledge bases
additional_nodes = [
    # More hardware concepts
    ("node_209", "Circuit QED (电路量子电动力学)", "concept", "研究超导电路中光与物质相互作用的学科，是超导量子计算的理论基础", 4),
    ("node_210", "量子比特读出 (Qubit Readout)", "concept", "测量量子比特状态的技术，频分复用等方案", 3),
    ("node_211", "参量放大器 (Parametric Amplifier)", "material", "用于量子信号放大的低噪声器件", 3),
    ("node_212", "人造原子 (Artificial Atom)", "concept", "超导量子比特的本质——由超导电路构成的人造原子系统", 3),
    ("node_213", "迪文森佐准则 (DiVincenzo Criteria)", "concept", "实现量子计算所需满足的7个基本条件", 4),
    ("node_214", "真空技术 (Vacuum Technology)", "material", "量子计算实验中的真空环境技术", 2),
    ("node_215", "低温物理 (Low Temperature Physics)", "theory", "研究极低温条件下物质性质的物理学分支", 3),
    
    # More hardware details
    ("node_216", "超导传输子 (Transmon)", "hardware", "目前最主流的超导量子比特设计，对电荷噪声不敏感", 4),
    ("node_217", "低温CMOS测控芯片", "material", "在极低温环境下工作的量子比特控制芯片", 3),
    ("node_218", "多量子芯片互连", "concept", "将多个QPU连接成更大规模量子计算机的技术", 3),
    ("node_219", "Willow量子处理器", "hardware", "Google于2024年发布的量子处理器", 5),
    ("node_220", "祖冲之三号", "hardware", "中国科学技术大学发布的量子处理器", 5),
    ("node_221", "费米-哈伯德模型 (Fermi-Hubbard Model)", "theory", "描述强关联电子系统的理论模型", 3),
    ("node_222", "马约拉纳零模 (Majorana Zero Mode)", "concept", "拓扑量子计算中的关键粒子态", 3),
    ("node_223", "非阿贝尔任意子 (Non-abelian Anyon)", "concept", "拓扑量子计算的核心信息载体", 3),
    
    # More companies from IMA knowledge bases
    ("node_314", "相干科技", "company", "中国超导量子计算公司，北京量子院孵化", 3),
    ("node_315", "中微达信", "company", "中国低温CMOS量子测控芯片公司", 3),
    ("node_316", "不筹量子", "company", "中国中性原子量子计算公司", 3),
    ("node_317", "瀚海量子", "company", "中国量子计算公司", 3),
    ("node_318", "Riverlane", "company", "英国量子纠错技术公司", 3),
    ("node_319", "Alice & Bob", "company", "法国量子计算公司", 3),
    ("node_320", "Oxford Quantum Circuits (OQC)", "company", "英国超导量子计算公司", 3),
    ("node_321", "本源量子 (Origin Quantum)", "company", "中国量子计算公司，郭国平创立", 4),
    ("node_322", "Quantonation", "company", "法国量子技术风投基金", 2),
    ("node_323", "微软 (Microsoft)", "company", "美国科技公司，投资拓扑量子计算", 4),
    ("node_324", "英伟达 (NVIDIA)", "company", "美国芯片公司，量子计算赋能者", 4),
    
    # More applications
    ("node_409", "量子传感 (Quantum Sensing)", "application", "利用量子特性实现超高精度测量", 4),
    ("node_410", "量子通信 (Quantum Communication)", "application", "利用量子力学原理实现安全通信", 4),
    ("node_411", "国防与安全", "application", "量子计算在国防领域的应用", 3),
    ("node_412", "能源优化", "application", "量子计算在能源领域的应用", 3),
    
    # More algorithms and protocols
    ("node_110", "变分量子算法 (VQA)", "algorithm", "NISQ时代最主流的量子算法框架", 4),
    ("node_111", "量子深度学习 (Quantum Deep Learning)", "algorithm", "量子计算与深度学习的交叉领域", 4),
    ("node_112", "量子随机行走 (Quantum Walk)", "algorithm", "量子版本的随机行走算法", 2),
    ("node_113", "量子支持向量机 (QSVM)", "algorithm", "量子版本的支持向量机", 2),
    ("node_606", "BB84协议", "protocol", "最早的量子密钥分发协议", 3),
    ("node_607", "NIST后量子密码标准", "protocol", "美国NIST制定的抗量子密码标准", 4),
    
    # More concepts
    ("node_013", "量子纠错 (Quantum Error Correction)", "concept", "保护量子信息免受噪声影响的技术", 5),
    ("node_014", "逻辑量子比特 (Logical Qubit)", "concept", "由多个物理量子比特编码的容错量子比特", 5),
    ("node_015", "物理量子比特 (Physical Qubit)", "concept", "实际硬件中的量子比特", 4),
    ("node_016", "量子体积 (Quantum Volume)", "concept", "衡量量子计算机整体性能的指标", 3),
    ("node_017", "量子云平台 (Quantum Cloud)", "concept", "通过云端提供量子计算服务的平台", 4),
    ("node_018", "量子比特保真度 (Fidelity)", "concept", "衡量量子操作精度的指标", 4),
    ("node_019", "量子比特相干时间 (Coherence Time)", "concept", "量子比特保持量子态的时间长度", 4),
    ("node_020", "量子隧穿 (Quantum Tunneling)", "concept", "量子粒子穿过经典不可逾越势垒的现象", 3),
    ("node_021", "魔术态蒸馏 (Magic State Distillation)", "concept", "实现通用量子计算的关键技术", 3),
    ("node_022", "量子线路编译 (Quantum Circuit Compilation)", "concept", "将高级量子算法映射到硬件指令的过程", 3),
    
    # More people
    ("node_507", "Isaac Chuang", "person", "《量子计算与量子信息》合著者", 3),
    ("node_508", "A.M. Zagoskin", "person", "《量子工程学》作者", 3),
    ("node_509", "Peter Shor", "person", "Shor算法发明者", 4),
    ("node_510", "Lov Grover", "person", "Grover算法发明者", 3),
    
    # Research institutions
    ("node_330", "北京量子信息科学研究院 (BAQIS)", "company", "北京市政府牵头的国家级量子研究机构", 4),
    ("node_331", "中国科学技术大学", "company", "中国量子计算研究的领军高校", 4),
    ("node_332", "中科院量子信息重点实验室", "company", "中国量子信息研究核心机构", 3),
    ("node_333", "中国计算机学会量子计算大会 (CQCC)", "company", "中国量子计算领域重要学术会议", 3),
    
    # Quantum error correction specific
    ("node_023", "阈值定理 (Threshold Theorem)", "concept", "若物理错误率低于阈值，则可实现任意精度的容错量子计算", 5),
    ("node_024", "稳定子码 (Stabilizer Code)", "concept", "一类重要的量子纠错码", 4),
    ("node_025", "LDPC码 (Low-Density Parity-Check)", "concept", "低密度奇偶校验码，有望实现更高效的量子纠错", 4),
    ("node_026", "AI驱动量子纠错", "concept", "利用机器学习改进量子纠错译码器", 4),
]

# Additional edges
additional_edges = [
    # New concept relationships
    ("node_013", "node_011", "enables", 0.9),
    ("node_013", "node_014", "enables", 0.9),
    ("node_014", "node_015", "composed_of", 0.9),
    ("node_013", "node_604", "uses", 0.8),
    ("node_013", "node_023", "based_on", 0.9),
    ("node_023", "node_018", "depends_on", 0.8),
    ("node_016", "node_017", "related_to", 0.7),
    ("node_019", "node_018", "determines", 0.8),
    ("node_019", "node_008", "related_to", 0.7),
    ("node_020", "node_801", "related_to", 0.7),
    ("node_021", "node_011", "enables", 0.8),
    ("node_022", "node_005", "part_of", 0.7),
    ("node_024", "node_013", "part_of", 0.8),
    ("node_025", "node_013", "part_of", 0.8),
    ("node_026", "node_013", "improves", 0.8),
    ("node_026", "node_408", "uses", 0.7),
    
    # Hardware details
    ("node_216", "node_201", "part_of", 0.9),
    ("node_216", "node_801", "uses", 0.8),
    ("node_217", "node_201", "enables", 0.7),
    ("node_217", "node_315", "developed_by", 0.8),
    ("node_218", "node_201", "enables", 0.7),
    ("node_219", "node_302", "developed_by", 0.9),
    ("node_219", "node_201", "implemented_by", 0.8),
    ("node_220", "node_331", "developed_by", 0.9),
    ("node_220", "node_201", "implemented_by", 0.8),
    ("node_209", "node_201", "theoretical_basis", 0.9),
    ("node_209", "node_804", "uses", 0.8),
    ("node_210", "node_211", "uses", 0.8),
    ("node_210", "node_006", "part_of", 0.8),
    ("node_212", "node_216", "related_to", 0.8),
    ("node_212", "node_001", "is_type_of", 0.7),
    ("node_213", "node_001", "defines_requirements", 0.8),
    
    # Company relationships
    ("node_314", "node_201", "develops", 0.7),
    ("node_314", "node_330", "spun_off_from", 0.8),
    ("node_315", "node_217", "develops", 0.8),
    ("node_316", "node_204", "develops", 0.8),
    ("node_316", "node_208", "uses", 0.8),
    ("node_317", "node_201", "develops", 0.6),
    ("node_318", "node_013", "develops", 0.8),
    ("node_319", "node_201", "develops", 0.6),
    ("node_320", "node_201", "develops", 0.7),
    ("node_321", "node_201", "develops", 0.8),
    ("node_321", "node_503", "founded_by", 0.8),
    ("node_323", "node_205", "develops", 0.7),
    ("node_323", "node_222", "researches", 0.6),
    ("node_324", "node_201", "enables", 0.7),
    ("node_324", "node_202", "enables", 0.6),
    ("node_324", "node_204", "enables", 0.6),
    
    # People relationships
    ("node_507", "node_504", "coauthored", 0.9),
    ("node_508", "node_901", "contributes_to", 0.6),
    ("node_509", "node_101", "invented", 0.9),
    ("node_510", "node_102", "invented", 0.9),
    ("node_501", "node_508", "translated", 0.7),
    
    # Algorithm relationships
    ("node_110", "node_103", "includes", 0.8),
    ("node_110", "node_104", "includes", 0.8),
    ("node_110", "node_109", "includes", 0.7),
    ("node_111", "node_408", "related_to", 0.9),
    ("node_111", "node_404", "related_to", 0.8),
    
    # Topological quantum computing
    ("node_205", "node_222", "uses", 0.8),
    ("node_205", "node_223", "uses", 0.8),
    ("node_222", "node_223", "related_to", 0.8),
    ("node_221", "node_406", "used_in", 0.6),
    
    # Application relationships
    ("node_409", "node_901", "uses", 0.8),
    ("node_410", "node_601", "uses", 0.9),
    ("node_411", "node_401", "related_to", 0.8),
    ("node_412", "node_108", "uses", 0.7),
    ("node_412", "node_104", "uses", 0.6),
    
    # Protocol relationships
    ("node_606", "node_601", "part_of", 0.8),
    ("node_607", "node_602", "part_of", 0.9),
    ("node_605", "node_013", "part_of", 0.8),
    
    # New theory relationships
    ("node_215", "node_802", "enables", 0.8),
    ("node_214", "node_202", "enables", 0.6),
    ("node_214", "node_204", "enables", 0.6),
    
    # Quantum cloud platforms
    ("node_017", "node_301", "developed_by", 0.8),
    ("node_017", "node_302", "developed_by", 0.7),
    ("node_017", "node_307", "developed_by", 0.6),
    
    # Competing hardware
    ("node_201", "node_202", "competes_with", 0.7),
    ("node_201", "node_204", "competes_with", 0.7),
    ("node_202", "node_204", "competes_with", 0.6),
    ("node_203", "node_201", "competes_with", 0.5),
    
    # Qubit types
    ("node_216", "node_015", "is_type_of", 0.8),
    ("node_803", "node_015", "is_type_of", 0.8),
]

# Add additional nodes
for node_id, label, node_type, description, importance in additional_nodes:
    # Check if node already exists
    existing_ids = [n["id"] for n in graph_data["nodes"]]
    if node_id not in existing_ids:
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
            cat = "量子计算基础"
            if "纠错" in label or "码" in label:
                cat = "量子纠错"
            graph_data["categories"].setdefault(cat, []).append(node_id)
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
        elif node_type == "material":
            graph_data["categories"]["硬件技术路线"].append(node_id)
        elif node_type == "person":
            pass  # People don't need category

# Add additional edges
for source, target, label, weight in additional_edges:
    # Check if source and target nodes exist
    existing_ids = [n["id"] for n in graph_data["nodes"]]
    if source in existing_ids and target in existing_ids:
        graph_data["edges"].append({
            "source": source,
            "target": target,
            "label": label,
            "weight": weight
        })

# Update metadata
graph_data["metadata"]["node_count"] = len(graph_data["nodes"])
graph_data["metadata"]["edge_count"] = len(graph_data["edges"])

# Save updated graph data
with open("/Users/danielcrystal/WorkBuddy/2026-06-13-17-30-18/graph_data.json", "w", encoding="utf-8") as f:
    json.dump(graph_data, f, ensure_ascii=False, indent=2)

print(f"Updated graph data: {len(graph_data['nodes'])} nodes and {len(graph_data['edges'])} edges")
print(f"Categories: {', '.join(f'{k}({len(v)})' for k, v in graph_data['categories'].items())}")
