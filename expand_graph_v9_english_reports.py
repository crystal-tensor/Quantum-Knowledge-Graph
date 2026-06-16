#!/usr/bin/env python3
"""Phase 8: enrich graph with English reports visible in the IMA shared knowledge bases."""

import json
from pathlib import Path

GRAPH_PATH = Path("graph_data.json")
data = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
nodes = data["nodes"]
edges = data["edges"]

node_by_id = {n["id"]: n for n in nodes}
node_by_label = {n["label"]: n for n in nodes}
edge_set = {(e.get("source"), e.get("target"), e.get("label", "")) for e in edges}


def add_node(node_id, label, node_type, description, importance=3, source_documents=None, related_terms=None, source_kbs=None, difficulty=None, evidence=None):
    if node_id in node_by_id:
        return node_id
    existing = node_by_label.get(label)
    if existing:
        return existing["id"]

    props = {
        "importance": importance,
        "source_documents": source_documents or [],
        "related_terms": related_terms or [],
        "source_knowledge_bases": source_kbs or ["量子产业研究报告", "量子计算学习材料"],
    }
    if difficulty is not None:
        props["difficulty"] = difficulty
    if evidence:
        props["evidence"] = evidence
    node = {
        "id": node_id,
        "label": label,
        "type": node_type,
        "description": description,
        "properties": props,
    }
    nodes.append(node)
    node_by_id[node_id] = node
    node_by_label[label] = node
    return node_id


def add_edge(src, tgt, label, weight=2):
    if src not in node_by_id or tgt not in node_by_id or src == tgt:
        return False
    key = (src, tgt, label)
    if key in edge_set:
        return False
    edges.append({"source": src, "target": tgt, "label": label, "weight": weight})
    edge_set.add(key)
    return True


def find_node(text):
    text_l = text.lower()
    for n in nodes:
        hay = f"{n['label']} {n.get('description', '')}".lower()
        if text_l in hay:
            return n["id"]
    return None


SOURCE_KBS = ["量子产业研究报告", "量子计算学习材料"]

reports = [
    ("node_1201", "IQM量子现状2024报告 (State of Quantum 2024 Report)", "IQM State-of-Quantum-2024-report.pdf", "IQM"),
    ("node_1202", "美国国家量子计划FY2025年度报告 (NQI Annual Report FY2025)", "NQI-Annual-Report-FY2025.pdf", "美国量子战略"),
    ("node_1203", "量子操作系统报告 (QOS Quantum Operating System)", "QOS Quantum Operating System.pdf", "QOS"),
    ("node_1204", "QOV算法与物理硬件桥接报告 (Bridging QOV Algorithms and Physical Hardware)", "Bridging_QOV_Algorithms_and_Physical_Hardware.pdf", "QOV"),
    ("node_1205", "AI驱动量子纠错报告 (AI-Driven Quantum Error Correction)", "AI_Driven_Quantum_Error_Correction.pdf", "AI驱动量子纠错"),
    ("node_1206", "量子安全技术蓝皮书2024 (Quantum Security Technology Blue Book 2024)", "【QIC】量子安全技术蓝皮书2024.pdf", "量子安全"),
    ("node_1207", "NQCC量子商业就绪报告 (Quantum Business Readiness Report)", "NQCC-2026-Quantum Business Readiness Report (Resilience in the quantum era).pdf", "NQCC"),
    ("node_1208", "NNSA量子计算战略2026 (Quantum Computing Strategy 2026)", "NNSA-2025-Quantum Computing Strategy 2026.pdf", "NNSA"),
    ("node_1209", "LuxQuanta量子安全部署报告 (Real World CV-QKD and KMS Deployments)", "Luxquanta-2026-Quantum Safe Solutions_Real World CV-QKD and KMS Deployments.pdf", "LuxQuanta"),
    ("node_1210", "德国高科技议程 (High-Tech Agenda Germany)", "BMFTR-2026-High-Tech Agenda Germany.pdf", "BMFTR"),
    ("node_1211", "Q-CTRL战场信息优势报告 (Quantum Computing for Battlefield Information Dominance)", "Q-CTRL-2026-Quantum computing for battlefield information dominance.pdf", "Q-CTRL"),
    ("node_1212", "Alice & Bob逻辑量子比特定义报告 (Defining the Logical Qubit)", "Alice&Bob-2026-Defining the Logical Qubit_Five Criteria to Benchmark Logical Qubit Claims.pdf", "Alice & Bob"),
    ("node_1213", "EERA净零转型量子计算报告 (Quantum Computing in the Net-Zero Transition)", "EERA-2026-Quantum computing in the net-zero transition_energy production, management, and efficiency.pdf", "EERA"),
    ("node_1214", "Kiutra量子产业循环性报告 (Circularity in the Quantum Industry)", "Kiutra-2026-Circularity in the Quantum Industry.pdf", "Kiutra"),
    ("node_1215", "英国量子十年行动报告 (Seizing the UK’s Quantum Decade)", "TYI-2026-Seizing the UK’s Quantum Decade_A Call for Action.pdf", "The Quantum Insider"),
    ("node_1216", "UNESCO量子时刻全球报告 (The Quantum Moment Global Report)", "UNESCO-2026-The Quantum Moment_A Global Report.pdf", "UNESCO"),
    ("node_1217", "QED-C全球量子产业状态报告 (State of the Global Quantum Industry)", "QED-C-2026-State of the Global Quantum Industry.pdf", "QED-C"),
    ("node_1218", "Coinbase量子计算与区块链报告 (Quantum Computing and Blockchain)", "Coinbase-2026-Quantum Computing & Blockchain.pdf", "Coinbase"),
    ("node_1219", "QuEra量子就绪调查 (Quantum Readiness Survey Part 2)", "QuEra-2026-Quantum Readiness Survey (Part 2).pdf", "QuEra"),
    ("node_1220", "Riverlane量子纠错路线图 (QEC Technology Roadmap)", "Riverlane-2026-The Riverlane QEC Technology Roadmap.pdf", "Riverlane"),
    ("node_1221", "QuIC欧洲量子市场整合报告 (European Quantum Market Consolidation)", "QuIC-2026-QuIC Inputs on European Quantum Market Consolidation.pdf", "QuIC"),
    ("node_1222", "麦肯锡量子技术监测报告 (Quantum Technology Monitor)", "McKinsey-2026-Quantum Technology Monitor.pdf", "McKinsey"),
    ("node_1223", "GAO美国量子战略更新报告 (Updating the National Strategy)", "GAO-2026-Quantum Computing_Updating the National Strategy Could Promote U.S. Leadership.pdf", "GAO"),
    ("node_1224", "CSIS芝加哥量子创新集群报告 (Chicago Quantum Innovation Cluster)", "CSIS-2026-Chicago’s Emerging Quantum Innovation Cluster.PDF", "CSIS"),
    ("node_1225", "Bruegel前沿关键技术公司比较报告 (Critical Technologies Company Comparison)", "Bruegel-2025-Which companies are ahead in frontier innovation on critical technologies.pdf", "Bruegel"),
    ("node_1226", "标普能源计算与量子时代报告 (Energy Compute and the Quantum Era)", "S&P Global Energy-2026-Energy Compute and the Quantum Era.pdf", "S&P Global Energy"),
    ("node_1227", "Dealroom欧洲深科技报告 (European Deeptech Report)", "Dealroom-2026-The 2026 European Deeptech Report.pdf", "Dealroom"),
    ("node_1228", "EuroQuIC量子专利图景报告 (Global Patent Landscape in Quantum Technologies)", "EuroQuIC-2026-A Portrait of the Global Patent Landscape in Quantum Technologies.pdf", "EuroQuIC"),
    ("node_1229", "CQE中西部量子人才战略 (Midwest Quantum Talent Strategy)", "CQE-2026-Advancing Together_A Unified Strategy for Scaling Midwest Quantum Talent.pdf", "Chicago Quantum Exchange"),
]

for node_id, label, doc, org in reports:
    add_node(
        node_id,
        label,
        "report",
        f"来自 IMA 共享知识库的英文研究报告来源节点：{doc}。",
        importance=4,
        source_documents=[doc],
        related_terms=[org],
        source_kbs=SOURCE_KBS,
        difficulty=2,
        evidence=f"IMA 共享知识库可见报告条目：{doc}",
    )

orgs = [
    ("node_1230", "NQCC英国国家量子计算中心 (National Quantum Computing Centre)", "英国国家量子计算中心，推动企业量子就绪、量子应用验证和国家量子计算能力建设。", "organization", ["node_1207"]),
    ("node_1231", "NNSA美国国家核安全管理局 (National Nuclear Security Administration)", "美国能源部下属机构，关注量子计算对国家安全、模拟和任务系统的战略影响。", "organization", ["node_1208"]),
    ("node_1232", "LuxQuanta公司 (LuxQuanta)", "面向量子安全通信的连续变量量子密钥分发与密钥管理部署公司。", "company", ["node_1209"]),
    ("node_1233", "BMFTR德国联邦研究技术与航天部 (BMFTR)", "德国高科技政策与科研创新议程相关机构。", "organization", ["node_1210"]),
    ("node_1234", "Q-CTRL公司 (Q-CTRL)", "量子控制、误差抑制和量子软件基础设施公司，强调任务级量子优势。", "company", ["node_1211"]),
    ("node_1235", "EERA欧洲能源研究联盟 (European Energy Research Alliance)", "欧洲能源研究协作组织，关注量子计算在净零转型中的能源系统应用。", "organization", ["node_1213"]),
    ("node_1236", "Kiutra公司 (Kiutra)", "低温制冷与量子产业可持续硬件相关公司。", "company", ["node_1214"]),
    ("node_1237", "The Quantum Insider (TYI)", "量子产业情报与生态研究机构，发布英国量子生态和资金报告。", "organization", ["node_1215"]),
    ("node_1238", "UNESCO联合国教科文组织 (UNESCO)", "联合国教科文组织，推动国际量子科学年、量子教育和全球协作。", "organization", ["node_1216"]),
    ("node_1239", "QED-C量子经济发展联盟 (Quantum Economic Development Consortium)", "美国量子产业联盟，跟踪全球量子产业状态与供应链。", "organization", ["node_1217"]),
    ("node_1240", "QuIC欧洲量子产业联盟 (European Quantum Industry Consortium)", "欧洲量子产业联盟，关注欧洲市场整合、标准和产业竞争力。", "organization", ["node_1221"]),
    ("node_1241", "GAO美国政府问责局 (Government Accountability Office)", "美国政府问责局，评估国家量子战略和公共政策执行。", "organization", ["node_1223"]),
    ("node_1242", "CSIS战略与国际研究中心 (Center for Strategic and International Studies)", "美国智库，研究量子创新集群、国家安全和区域科技政策。", "organization", ["node_1224"]),
    ("node_1243", "Chicago Quantum Exchange芝加哥量子交易所 (CQE)", "美国中西部量子创新、产业和人才协作网络。", "organization", ["node_1229"]),
]

for node_id, label, desc, typ, report_ids in orgs:
    add_node(node_id, label, typ, desc, importance=3, source_documents=[node_by_id[r]["properties"]["source_documents"][0] for r in report_ids], source_kbs=SOURCE_KBS)
    for report_id in report_ids:
        add_edge(report_id, node_id, "published_by", 3)

concepts = [
    ("node_1250", "量子商业就绪 (Quantum Business Readiness)", "企业为量子计算冲击和机会做准备的能力，包括用例组合、人才、数据、风险治理和采购路径。", "concept", 4, ["node_1207", "node_1219", "node_1222"], ["量子产业化", "企业采用"]),
    ("node_1251", "量子安全迁移清单 (Quantum-safe Migration Inventory)", "对密码资产、数据寿命、系统接口和迁移优先级进行盘点，是抗量子迁移的第一步。", "security", 4, ["node_1206", "node_1209", "node_1218"], ["后量子密码", "QKD"]),
    ("node_1252", "先收集后解密威胁 (Harvest Now Decrypt Later)", "攻击者提前收集加密数据，等待未来量子计算破解传统公钥密码后再解密的长期安全风险。", "security", 4, ["node_1206", "node_1218"], ["PQC", "量子安全"]),
    ("node_1253", "连续变量QKD (Continuous-variable QKD)", "使用连续变量光场正交分量实现量子密钥分发，适合与现有光通信和密钥管理系统集成。", "protocol", 4, ["node_1209"], ["CV-QKD", "KMS"]),
    ("node_1254", "密钥管理系统集成 (KMS Integration)", "把 QKD/PQC 产生或保护的密钥接入企业密钥管理和业务系统的工程层。", "tool", 3, ["node_1209"], ["QKD", "企业安全"]),
    ("node_1255", "逻辑量子比特基准五要素 (Logical Qubit Benchmark Criteria)", "用于判断逻辑量子比特声明是否可信的指标框架，包括物理资源、逻辑错误率、寿命、门操作和可扩展性。", "qec", 5, ["node_1212"], ["逻辑量子比特", "容错"]),
    ("node_1256", "量子纠错解码器路线图 (QEC Decoder Roadmap)", "从综合征提取到实时解码、反馈控制和容错逻辑门的工程路线。", "qec", 5, ["node_1205", "node_1220"], ["解码器", "表面码"]),
    ("node_1257", "综合征提取流水线 (Syndrome Extraction Pipeline)", "周期性测量稳定子、收集错误综合征并输入解码器的容错量子计算基础流程。", "qec", 4, ["node_1205", "node_1220"], ["稳定子码", "表面码"]),
    ("node_1258", "猫量子比特路线 (Cat Qubit Architecture)", "利用玻色子猫态编码和偏置噪声抑制错误的逻辑量子比特路线。", "hardware", 5, ["node_1212"], ["Alice & Bob", "玻色子编码"]),
    ("node_1259", "玻色子纠错码 (Bosonic Code)", "在谐振腔等连续变量体系中编码量子信息，可与猫码、GKP码等路线连接。", "qec", 4, ["node_1212"], ["猫码", "逻辑量子比特"]),
    ("node_1260", "硬件感知QOV (Hardware-aware QOV)", "把变分优化算法的线路结构、噪声模型和硬件约束共同纳入设计的 QOV 工程路线。", "algorithm", 4, ["node_1204"], ["QOV", "硬件映射"]),
    ("node_1261", "量子控制栈 (Quantum Control Stack)", "从脉冲、校准、误差抑制到编译器反馈的硬件控制软件栈。", "software", 4, ["node_1203", "node_1211", "node_1204"], ["控制系统", "量子软件"]),
    ("node_1262", "量子操作系统编排器 (Quantum OS Orchestrator)", "在量子任务、资源、编译、校准和运行时之间进行调度的系统层。", "software", 4, ["node_1203"], ["QOS", "运行时"]),
    ("node_1263", "量子资源估计 (Quantum Resource Estimation)", "估算容错算法所需物理量子比特、逻辑量子比特、门深度、运行时间和纠错开销。", "software", 5, ["node_1220", "node_1222", "node_1212"], ["FTQC", "成本模型"]),
    ("node_1264", "战场信息优势 (Battlefield Information Dominance)", "国防场景中以量子计算、传感和优化提升态势感知、决策和任务规划的信息优势概念。", "application", 4, ["node_1211"], ["国防", "优化"]),
    ("node_1265", "量子PNT能力 (Quantum PNT)", "利用量子传感提升定位、导航和授时能力，尤其适用于 GPS 受限或对抗环境。", "application", 4, ["node_1211"], ["量子传感", "国防"]),
    ("node_1266", "能源系统量子优化 (Quantum Optimization for Energy Systems)", "把量子优化、仿真和机器学习用于电网调度、能源生产、储能和效率提升。", "application", 4, ["node_1213", "node_1226"], ["净零", "能源"]),
    ("node_1267", "净零转型量子模拟 (Quantum Simulation for Net-zero Transition)", "用量子模拟探索催化、材料、化学和能源过程，为净零技术路径提供候选方案。", "application", 4, ["node_1213"], ["材料", "化学模拟"]),
    ("node_1268", "区块链抗量子迁移 (Quantum-resistant Blockchain Migration)", "区块链系统从 ECDSA 等传统签名迁移到抗量子签名、钱包轮换和治理升级的路径。", "security", 4, ["node_1218"], ["区块链", "PQC"]),
    ("node_1269", "量子产业循环性 (Quantum Industry Circularity)", "围绕低温设备、稀缺材料、能耗和供应链回收的量子产业可持续性议题。", "concept", 3, ["node_1214"], ["低温", "供应链"]),
    ("node_1270", "无液氦低温制冷 (Cryogen-free Cooling)", "降低低温基础设施对液氦和高维护成本依赖的制冷路线。", "hardware", 4, ["node_1214"], ["稀释制冷机", "低温系统"]),
    ("node_1271", "主权量子生态 (Sovereign Quantum Ecosystem)", "围绕国家能力、供应链、人才、基础设施和资金形成的量子主权战略。", "concept", 4, ["node_1215", "node_1223", "node_1210"], ["国家战略", "产业政策"]),
    ("node_1272", "量子人才管线 (Quantum Talent Pipeline)", "从教育、实训、跨学科转化到产业岗位的量子人才供给系统。", "concept", 3, ["node_1216", "node_1229", "node_1215"], ["教育", "人才"]),
    ("node_1273", "量子专利图景 (Quantum Patent Landscape)", "通过专利族、申请主体和地区分布观察量子技术竞争位置。", "concept", 3, ["node_1228", "node_1225"], ["知识产权", "竞争"]),
    ("node_1274", "欧洲量子市场整合 (European Quantum Market Consolidation)", "欧洲量子企业、投资、标准和采购机制走向规模化整合的产业议题。", "concept", 4, ["node_1221", "node_1227"], ["欧洲", "市场"]),
    ("node_1275", "全球量子产业状态 (Global Quantum Industry State)", "从资本、公司、供应链、应用成熟度和政策支持综合观察全球量子产业阶段。", "concept", 4, ["node_1217", "node_1222"], ["产业报告", "市场"]),
    ("node_1276", "深科技融资缺口 (Deeptech Funding Gap)", "量子等深科技在长期研发、资本周期和规模化验证之间面临的融资断层。", "concept", 3, ["node_1227", "node_1215"], ["投融资", "产业化"]),
    ("node_1277", "量子创新集群 (Quantum Innovation Cluster)", "由大学、国家实验室、初创公司、资本和政府共同构成的区域量子创新网络。", "organization", 3, ["node_1224", "node_1229"], ["芝加哥", "生态"]),
    ("node_1278", "量子标准与互操作性 (Quantum Standards and Interoperability)", "围绕接口、性能指标、软件栈、通信协议和安全迁移形成的标准体系。", "standard", 4, ["node_1221", "node_1217", "node_1206"], ["标准", "互操作"]),
    ("node_1279", "量子应用组合管理 (Quantum Use-case Portfolio)", "企业以价值、时间、硬件成熟度和风险维度管理量子应用候选项目。", "application", 3, ["node_1207", "node_1222", "node_1219"], ["企业采用", "应用落地"]),
    ("node_1280", "纠错优先路线 (QEC-first Roadmap)", "把容错、逻辑量子比特和可扩展纠错作为通向实用量子计算主路径的路线图。", "qec", 5, ["node_1220", "node_1212"], ["容错", "逻辑量子比特"]),
    ("node_1281", "中性原子企业就绪 (Neutral-atom Enterprise Readiness)", "围绕中性原子平台的可编程阵列、应用试点和企业认知成熟度形成的采用路径。", "hardware", 4, ["node_1219"], ["中性原子", "QuEra"]),
    ("node_1282", "国家量子战略更新 (National Quantum Strategy Refresh)", "在全球竞争、供应链、安全和应用落地压力下重新校准国家量子计划。", "concept", 4, ["node_1202", "node_1223", "node_1208"], ["政策", "国家战略"]),
    ("node_1283", "前沿关键技术竞争 (Frontier Critical Technology Competition)", "以量子、AI、半导体等关键技术为对象比较国家和企业创新领先位置。", "concept", 4, ["node_1225"], ["竞争", "地缘科技"]),
]

for node_id, label, desc, typ, importance, report_ids, terms in concepts:
    docs = [node_by_id[r]["properties"]["source_documents"][0] for r in report_ids]
    add_node(node_id, label, typ, desc, importance=importance, source_documents=docs, related_terms=terms, source_kbs=SOURCE_KBS, difficulty=min(5, max(2, importance)), evidence=f"由英文报告条目抽取并结构化：{'；'.join(docs[:3])}")
    for report_id in report_ids:
        add_edge(report_id, node_id, "covers", 3)
        add_edge(node_id, report_id, "sourced_from", 1)

existing_links = [
    ("node_1250", "node_929", "supports_commercialization", 3),
    ("node_1250", "node_012", "translates_nisq_to_business", 2),
    ("node_1251", "node_607", "implements", 4),
    ("node_1251", "node_1033", "implements", 4),
    ("node_1251", "node_601", "complements", 3),
    ("node_1252", "node_401", "threatens", 4),
    ("node_1252", "node_607", "mitigated_by", 4),
    ("node_1253", "node_601", "is_type_of", 4),
    ("node_1253", "node_606", "extends_qkd_family", 2),
    ("node_1254", "node_1253", "integrates", 3),
    ("node_1255", "node_014", "benchmarks", 5),
    ("node_1255", "node_011", "enables", 4),
    ("node_1256", "node_013", "implements", 5),
    ("node_1256", "node_604", "targets", 4),
    ("node_1257", "node_024", "measures", 4),
    ("node_1257", "node_604", "used_by", 4),
    ("node_1258", "node_319", "developed_by", 4),
    ("node_1258", "node_014", "encodes", 4),
    ("node_1259", "node_1258", "includes", 3),
    ("node_1259", "node_014", "protects", 3),
    ("node_1260", "node_109", "extends", 4),
    ("node_1260", "node_104", "related_to", 3),
    ("node_1260", "node_018", "optimizes_under", 3),
    ("node_1261", "node_022", "feeds_back_to", 3),
    ("node_1261", "node_018", "calibrates", 3),
    ("node_1262", "node_015", "is_system_layer_of", 3),
    ("node_1262", "node_701", "orchestrates_tools_like", 2),
    ("node_1263", "node_011", "estimates_resources_for", 4),
    ("node_1263", "node_101", "resource_estimates", 3),
    ("node_1264", "node_412", "uses_optimization_for", 2),
    ("node_1264", "node_409", "combined_with", 3),
    ("node_1265", "node_409", "is_application_of", 4),
    ("node_1266", "node_412", "extends", 3),
    ("node_1266", "node_104", "may_use", 3),
    ("node_1267", "node_406", "extends", 3),
    ("node_1267", "node_405", "applies_to", 3),
    ("node_1268", "node_607", "requires", 4),
    ("node_1268", "node_401", "protects", 3),
    ("node_1269", "node_802", "concerns", 3),
    ("node_1270", "node_802", "alternative_to", 3),
    ("node_1271", "node_1073", "compares_with", 3),
    ("node_1271", "node_1074", "compares_with", 3),
    ("node_1272", "node_331", "requires_universities_like", 2),
    ("node_1273", "node_1070", "maps_region", 2),
    ("node_1273", "node_1068", "maps_region", 2),
    ("node_1273", "node_1069", "maps_region", 2),
    ("node_1274", "node_1070", "regional_focus", 3),
    ("node_1274", "node_1072", "policy_context", 3),
    ("node_1275", "node_929", "tracks", 3),
    ("node_1276", "node_929", "bottleneck_for", 3),
    ("node_1277", "node_991", "includes_university", 2),
    ("node_1278", "node_607", "standardizes", 3),
    ("node_1278", "node_015", "standardizes", 2),
    ("node_1279", "node_402", "contains_use_case", 2),
    ("node_1279", "node_403", "contains_use_case", 2),
    ("node_1279", "node_406", "contains_use_case", 2),
    ("node_1280", "node_011", "roadmap_to", 5),
    ("node_1280", "node_014", "requires", 5),
    ("node_1281", "node_204", "is_adoption_path_for", 4),
    ("node_1281", "node_312", "associated_with", 3),
    ("node_1282", "node_1073", "refreshes", 3),
    ("node_1282", "node_1074", "benchmarks_against", 2),
    ("node_1283", "node_1070", "compares", 2),
    ("node_1283", "node_1069", "compares", 2),
    ("node_1283", "node_1068", "compares", 2),
]

for src, tgt, label, weight in existing_links:
    add_edge(src, tgt, label, weight)

report_org_links = [
    ("node_1201", "node_303"),
    ("node_1204", "node_109"),
    ("node_1205", "node_026"),
    ("node_1212", "node_319"),
    ("node_1219", "node_312"),
    ("node_1220", "node_318"),
]
for report_id, target_id in report_org_links:
    add_edge(report_id, target_id, "features", 3)

data.setdefault("metadata", {})
data["metadata"]["node_count"] = len(nodes)
data["metadata"]["edge_count"] = len(edges)
data["metadata"]["last_updated"] = "2026-06-16"
data["metadata"]["expansion_notes"] = (
    "Phase 8: English IMA report enrichment. Added report provenance nodes and extracted "
    "quantum-readiness, QEC, quantum-safe, energy, national-strategy, talent, patent, and ecosystem nodes."
)
for kb in SOURCE_KBS:
    if kb not in data["metadata"].setdefault("source_knowledge_bases", []):
        data["metadata"]["source_knowledge_bases"].append(kb)

GRAPH_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"nodes={len(nodes)} edges={len(edges)}")
