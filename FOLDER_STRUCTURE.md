# 银行股估值模型 (Bank Valuation Model) - 文件夹结构

**模块名**: bank_valuation_model  
**功能**: A股银行股票的四大估值模型计算和综合评估  
**更新日期**: 2026年3月30日

---

## 📁 文件夹结构说明

```
bank_valuation_model/
├── __init__.py                    # 模块初始化文件
├── README.md                      # 模块说明文档
├── FOLDER_STRUCTURE.md           # 本文件 - 文件夹结构说明
├── config.py                      # 配置文件（参数、阈值、基准数据）
├── main.py                        # 主程序入口
│
├── 核心模块 (Core Modules)
│   ├── calculator.py              # 估值计算引擎（四大模型集成）
│   ├── data_fetcher.py            # 数据获取和管理
│   ├── analyzer.py                # 分析模块
│
├── 测试和辅助脚本 (Testing Scripts)
│   ├── check_all_models.py        # 四大模型完整性检查
│   ├── test_relative_valuation.py # 相对估值法测试
│   ├── comprehensive_valuation_report.py  # 综合报告生成脚本
│   ├── update_bank_data.py        # 银行数据更新脚本
│
├── models/                        # 估值模型实现文件夹
│   ├── __init__.py
│   ├── ddm_model.py               # DDM模型（股息贴现）
│   ├── pb_roe_model.py            # PB-ROE模型
│   ├── riv_model.py               # RIV模型（剩余收益）
│   └── relative_valuation.py      # 相对估值法模型
│
├── data/                          # 数据存放文件夹
│   ├── DATA_UPDATE_REFERENCE_20260329.py  # 数据更新参考脚本
│   └── （其他数据文件）
│
├── reports/                       # 报告和结果输出文件夹
│   ├── comprehensive_valuation_20260330_122251.md    # 综合评估报告
│   ├── valuation_results_20260330_122251.json        # 详细数据JSON
│   ├── BANK_DATA_STATISTICS.md    # 银行数据统计报告
│   ├── BANK_UPDATE_STATUS_20260329.md  # 数据更新状态
│   ├── COMPLETION_REPORT.md       # 完成报告
│   ├── DATA_FORMAT_STANDARDIZATION_20260330.md  # 数据格式标准化报告
│   ├── DATA_UPDATE_*.md           # 数据更新指南和日志
│   └── GENERATED_BANK_UPDATE_DATA.txt  # 生成的银行数据
│
├── docs/                          # 文档和说明文件夹
│   ├── COMPREHENSIVE_ASSESSMENT_REPORT.md  # 完整执行报告
│   ├── INVESTMENT_DECISION_GUIDE.md        # 投资决策快速指南
│   ├── RELATIVE_VALUATION_INTEGRATION.md   # 相对估值法集成说明
│   └── QUICKSTART.md              # 快速开始指南
│
└── __pycache__/                   # Python缓存（可忽略）
```

---

## 📋 文件分类说明

### 核心脚本 (Core Scripts)
- **config.py**: 全局配置，包含参数、模型参数、行业基准数据
- **calculator.py**: 核心估值引擎，整合四大模型的计算逻辑
- **data_fetcher.py**: 银行基本面数据获取，包含29家银行的样本数据
- **analyzer.py**: 数据分析和图表生成

### 模型实现 (models/)
- **ddm_model.py**: 股息贴现模型实现
- **pb_roe_model.py**: PB-ROE模型实现
- **riv_model.py**: 剩余收益模型实现
- **relative_valuation.py**: 相对估值法（PE/PB倍数法）实现

### 测试脚本 (Testing)
- **check_all_models.py**: 验证四大模型的完整性和一致性
- **test_relative_valuation.py**: 测试新增的相对估值法功能
- **comprehensive_valuation_report.py**: 批量生成29家银行的估值报告

### 数据文件 (data/)
- 银行基本面数据
- 数据更新参考脚本

### 报告输出 (reports/)
- 自动生成的Markdown和JSON格式报告
- 数据统计和更新日志

### 文档说明 (docs/)
- 功能设计和集成说明
- 投资决策指南和快速开始教程

---

## 🚀 快速使用指南

### 1. 对所有银行进行估值
```bash
cd /home/deploy/investment_agent
source venv/bin/activate
python bank_valuation_model/comprehensive_valuation_report.py
```

### 2. 验证模型完整性
```bash
python bank_valuation_model/check_all_models.py
```

### 3. 查看报告
```bash
cat bank_valuation_model/reports/comprehensive_valuation_*.md
cat bank_valuation_model/docs/INVESTMENT_DECISION_GUIDE.md
```

### 4. 在Python中调用
```python
from bank_valuation_model.calculator import ValuationCalculator
from bank_valuation_model.data_fetcher import DataFetcher

fetcher = DataFetcher()
calc = ValuationCalculator()

# 估值单个银行
data = fetcher.fetch_bank_fundamentals("招商银行")
results = calc.calculate_all_models(data)
```

---

## 📊 关键文件说明

### config.py
```python
# 配置了以下内容
- BANK_CATEGORIES: 29家A股银行的分类
- VALUATION_PARAMS: 估值基础参数（无风险率、股权成本等）
- MODEL_PARAMS: 四大模型的参数和行业基准数据
- THRESHOLDS: 风险警告阈值
```

### calculator.py
```python
# 主要方法
- calculate_all_models(bank_data): 对单个银行执行四大模型估值
- calculate_for_multiple_banks(banks_data): 批量估值
- rank_by_model(): 按模型排序推荐
- identify_opportunities(): 识别投资机会
```

### data_fetcher.py
```python
# 主要方法
- fetch_bank_fundamentals(bank_name): 获取单个银行数据
- fetch_all_banks(): 获取所有29家银行数据
- fetch_by_category(category): 按分类获取数据
```

---

## ✅ 数据完整性检查

- [x] 29家A股上市银行数据完整
- [x] 四大估值模型全部实现且相互独立
- [x] 估值结果经过验证和合理性检查
- [x] 报告和文档完整清晰

---

## 📝 最近更新

**2026年3月30日**: 
- 相对估值法（PE/PB倍数法）成功集成
- 完成29家银行的四大模型综合估值
- 生成完整的评估报告和投资建议
- 整理文件结构，将文档和报告分类保存

---

## 📞 文件位置索引

| 需求 | 查看位置 |
|-----|--------|
| 模块说明 | `bank_valuation_model/README.md` |
| 快速开始 | `bank_valuation_model/docs/QUICKSTART.md` |
| 投资建议 | `bank_valuation_model/docs/INVESTMENT_DECISION_GUIDE.md` |
| 完整报告 | `bank_valuation_model/reports/comprehensive_valuation_*.md` |
| 详细数据 | `bank_valuation_model/reports/valuation_results_*.json` |
| 模型说明 | `bank_valuation_model/docs/RELATIVE_VALUATION_INTEGRATION.md` |
| 项目配置 | `bank_valuation_model/config.py` |
| 核心计算 | `bank_valuation_model/calculator.py` |

---

**模块状态**: ✅ 完整、可用、已优化  
**最后验证**: 2026年3月30日 12:22  
*更多信息请查看各文件夹内的README.md*
