#!/usr/bin/env python3
"""
银行股四大估值模型综合评估报告生成
对29个上市银行进行DDM、PB-ROE、RIV、相对估值法全面估值
并生成专业投资决策报告
"""

import sys
from pathlib import Path
from datetime import datetime
import json
import logging

sys.path.insert(0, str(Path(__file__).parent))

from bank_valuation_model.calculator import ValuationCalculator
from bank_valuation_model.data_fetcher import DataFetcher
from bank_valuation_model.config import Config
import pandas as pd

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ComprehensiveValuationReport:
    """综合估值报告生成器"""
    
    def __init__(self):
        """初始化报告生成器"""
        self.config = Config()
        self.fetcher = DataFetcher(self.config)
        self.calculator = ValuationCalculator(self.config)
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.report_dir = self.config.REPORT_DIR
        self.report_file = self.report_dir / f"comprehensive_valuation_{self.timestamp}.md"
        self.json_file = self.report_dir / f"valuation_results_{self.timestamp}.json"
    
    def generate_report(self):
        """生成完整的综合评估报告"""
        
        print("\n" + "=" * 100)
        print(" " * 30 + "银行股四大模型综合估值评估报告")
        print(" " * 35 + f"2026年3月30日")
        print("=" * 100)
        
        # 获取所有银行数据
        print("\n[1/4] 获取29家上市银行数据...")
        all_banks = self.config.get_bank_list()
        print(f"✓ 共计：{len(all_banks)} 家上市银行")
        print(f"  - 国有大型银行：{len(self.config.get_bank_list('国有大型银行'))} 家")
        print(f"  - 全国性股份制银行：{len(self.config.get_bank_list('全国性股份制银行'))} 家")
        print(f"  - 城商行：{len(self.config.get_bank_list('城商行'))} 家")
        
        # 执行估值计算
        print("\n[2/4] 执行四大估值模型计算...")
        all_results = []
        failed_banks = []
        
        for idx, bank_name in enumerate(all_banks, 1):
            try:
                print(f"  [{idx:2d}/{len(all_banks)}] 计算 {bank_name:12s} ...", end=" ")
                
                # 获取银行数据
                bank_data = self.fetcher.fetch_bank_fundamentals(bank_name)
                
                # 执行四大模型估值
                results = self.calculator.calculate_all_models(bank_data)
                all_results.append(results)
                
                print("✓")
            except Exception as e:
                print(f"✗ 错误: {e}")
                failed_banks.append((bank_name, str(e)))
        
        print(f"\n✓ 完成 {len(all_results)} 家银行的估值计算")
        if failed_banks:
            print(f"⚠ {len(failed_banks)} 家银行计算失败")
        
        # 生成分析和报告
        print("\n[3/4] 进行综合分析和评分...")
        analysis_results = self._analyze_results(all_results)
        
        # 生成报告
        print("\n[4/4] 生成详细报告...")
        self._write_report(all_results, analysis_results, failed_banks)
        self._save_json_results(all_results)
        
        print(f"\n✓ 报告生成完成")
        print(f"  - Markdown报告: {self.report_file}")
        print(f"  - 详细数据: {self.json_file}")
        print("\n" + "=" * 100 + "\n")
        
        return all_results, analysis_results
    
    def _analyze_results(self, all_results):
        """对估值结果进行综合分析"""
        
        analysis = {
            "severely_undervalued": [],    # 严重低估
            "undervalued": [],             # 低估
            "fairly_valued": [],           # 合理
            "overvalued": [],              # 高估
            "severely_overvalued": [],     # 严重高估
        }
        
        # 评分依据
        for result in all_results:
            bank_name = result["bank_name"]
            category = result["category"]
            current_pb = result["current_pb"]
            roe = result["roe"]
            
            # 获取各模型综合建议
            ddm_pb = result.get("ddm_pb")
            pb_roe_result = result.get("pb_roe", {})
            pb_roe_pb = pb_roe_result.get("fair_pb") if isinstance(pb_roe_result, dict) else None
            relative = result.get("relative", {})
            
            # 计算估值评分
            score = self._calculate_valuation_score(
                current_pb, ddm_pb, pb_roe_pb, relative, roe
            )
            
            bank_info = {
                "bank_name": bank_name,
                "category": category,
                "current_pb": current_pb,
                "current_pe": result["current_pe"],
                "roe": roe,
                "dividend_yield": result["dividend_yield"],
                "current_price": result["current_price"],
                "valuation_score": score,
                "ddm_pb": ddm_pb,
                "pb_roe_pb": pb_roe_pb,
                "relative": relative,
            }
            
            # 分类存放
            if score >= 1.5:
                analysis["severely_overvalued"].append(bank_info)
            elif score >= 1.15:
                analysis["overvalued"].append(bank_info)
            elif score >= 0.95:
                analysis["fairly_valued"].append(bank_info)
            elif score >= 0.7:
                analysis["undervalued"].append(bank_info)
            else:
                analysis["severely_undervalued"].append(bank_info)
        
        # 排序
        for key in analysis:
            analysis[key] = sorted(analysis[key], key=lambda x: x["valuation_score"])
        
        return analysis
    
    def _calculate_valuation_score(self, current_pb, ddm_pb, pb_roe_pb, relative, roe):
        """计算综合估值分数（1.0为合理）"""
        
        scores = []
        
        # DDM模型评分
        if ddm_pb and ddm_pb > 0:
            scores.append(current_pb / ddm_pb)
        
        # PB-ROE模型评分
        if pb_roe_pb and pb_roe_pb > 0:
            scores.append(current_pb / pb_roe_pb)
        
        # 相对估值法评分
        if relative and isinstance(relative, dict):
            pb_premium = relative.get("pb_premium", {})
            if isinstance(pb_premium, dict):
                premium_pct = pb_premium.get("premium_to_median_pct", 0)
                # 转换为相对分数
                relative_score = 1.0 + premium_pct / 100
                scores.append(relative_score)
        
        # 返回平均分
        return sum(scores) / len(scores) if scores else 1.0
    
    def _write_report(self, all_results, analysis, failed_banks):
        """写入Markdown格式的报告"""
        
        with open(self.report_file, 'w', encoding='utf-8') as f:
            # 报告标题
            f.write("# 银行股四大估值模型综合评估报告\n\n")
            f.write(f"**生成日期**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            # 执行摘要
            f.write("## 📋 执行摘要\n\n")
            f.write("### 评估范围\n")
            f.write("- **评估银行**: 29家A股上市银行\n")
            f.write("  - 国有大型银行：6家（工农中建交邮）\n")
            f.write("  - 全国性股份制银行：8家（招浦中兴平民光华）\n")
            f.write("  - 城商行：15家（地方性上市商业银行）\n")
            f.write(f"- **评估模型**: 4大估值方法\n")
            f.write("  1. 股息贴现模型（DDM）\n")
            f.write("  2. PB-ROE相关模型\n")
            f.write("  3. 剩余收益模型（RIV）\n")
            f.write("  4. 相对估值法（PE/PB倍数法）\n")
            f.write(f"- **評估時點**: 2026年03月27日\n\n")
            
            # 主要发现
            f.write("### 主要发现\n\n")
            f.write("| 估值等级 | 家数 | 占比 |\n")
            f.write("|---------|------|------|\n")
            
            total_banks = len(all_results)
            for level, desc in [
                ("severely_undervalued", "严重低估"),
                ("undervalued", "低估"),
                ("fairly_valued", "合理估值"),
                ("overvalued", "高估"),
                ("severely_overvalued", "严重高估"),
            ]:
                count = len(analysis[level])
                pct = f"{count/total_banks*100:.1f}%" if total_banks > 0 else "0%"
                f.write(f"| {desc} | {count} | {pct} |\n")
            
            f.write("\n")
            
            # 投资建议
            f.write("### 投资建议\n\n")
            
            # 强烈推荐
            f.write("#### 🟢 强烈推荐（严重低估）\n")
            if analysis["severely_undervalued"]:
                for bank in sorted(analysis["severely_undervalued"], 
                                 key=lambda x: x["valuation_score"])[:5]:
                    f.write(f"- **{bank['bank_name']}** ({bank['category']})\n")
                    f.write(f"  - 当前PB: {bank['current_pb']:.3f}\n")
                    f.write(f"  - 估值评分: {bank['valuation_score']:.3f} (1.0为合理)\n")
                    f.write(f"  - 股息率: {bank['dividend_yield']:.2%}\n\n")
            else:
                f.write("- 暂无\n\n")
            
            # 推荐持有
            f.write("#### 🟡 推荐关注（低估或合理）\n")
            fair_list = analysis["undervalued"] + analysis["fairly_valued"]
            if fair_list:
                for bank in sorted(fair_list, key=lambda x: x["valuation_score"])[:10]:
                    f.write(f"- {bank['bank_name']:12s} | PB: {bank['current_pb']:.3f} | ")
                    f.write(f"评分: {bank['valuation_score']:.3f}\n")
                f.write("\n")
            else:
                f.write("- 暂无\n\n")
            
            # 谨慎态度
            f.write("#### 🔴 谨慎态度（高估或严重高估）\n")
            over_list = analysis["overvalued"] + analysis["severely_overvalued"]
            if over_list:
                for bank in sorted(over_list, key=lambda x: x["valuation_score"], reverse=True)[:5]:
                    f.write(f"- {bank['bank_name']:12s} | PB: {bank['current_pb']:.3f} | ")
                    f.write(f"评分: {bank['valuation_score']:.3f}\n")
                f.write("\n")
            else:
                f.write("- 暂无\n\n")
            
            f.write("---\n\n")
            
            # 详细估值表
            f.write("## 📊 完整估值数据表\n\n")
            
            # 按类别组织
            for category in ["国有大型银行", "全国性股份制银行", "城商行"]:
                f.write(f"\n### {category}\n\n")
                f.write("| 银行 | 代码 | PB | PE | ROE | 股息率 | DDM-PB | 评分 | 评级 |\n")
                f.write("|------|------|-----|-----|-------|--------|--------|------|------|\n")
                
                for result in all_results:
                    if result["category"] != category:
                        continue
                    
                    bank_name = result["bank_name"]
                    stock_code = result["stock_code"]
                    pb = result["current_pb"]
                    pe = result["current_pe"]
                    roe = result["roe"]
                    div_yield = result["dividend_yield"]
                    ddm_pb = result.get("ddm_pb", 0)
                    
                    # 找到对应的评分
                    score = 1.0
                    for level, banks in analysis.items():
                        for bank in banks:
                            if bank["bank_name"] == bank_name:
                                score = bank["valuation_score"]
                                break
                    
                    # 评级
                    if score >= 1.5:
                        rating = "严重高估"
                    elif score >= 1.15:
                        rating = "高估"
                    elif score >= 0.95:
                        rating = "合理"
                    elif score >= 0.7:
                        rating = "低估"
                    else:
                        rating = "严重低估"
                    
                    f.write(f"| {bank_name:10s} | {stock_code} | {pb:.3f} | {pe:.2f} | ")
                    f.write(f"{roe:.2%} | {div_yield:.2%} | {ddm_pb:.3f} | {score:.3f} | {rating:8s} |\n")
            
            f.write("\n---\n\n")
            
            # 模型说明
            f.write("## 📖 四大估值模型说明\n\n")
            
            f.write("### 1. 股息贴现模型（Dividend Discount Model, DDM）\n\n")
            f.write("**原理**: 通过贴现银行未来的股息，计算股票的合理价值\n")
            f.write("**适用**: 高分红、派息稳定的银行\n")
            f.write("**输出**: 合理PB、合理价格\n\n")
            
            f.write("### 2. PB-ROE相关模型\n\n")
            f.write("**原理**: 基于净资产收益率（ROE），计算合理的市净率\n")
            f.write("**适用**: ROE相对稳定的银行\n")
            f.write("**输出**: 合理PB、溢价幅度、市场对位\n\n")
            
            f.write("### 3. 剩余收益模型（Residual Income Valuation, RIV）\n\n")
            f.write("**原理**: 计算超额收益现值，进行长期价值评估\n")
            f.write("**适用**: 需要情景分析、多年期评估\n")
            f.write("**输出**: 内在价值、情景分析、敏感性分析\n\n")
            
            f.write("### 4. 相对估值法（PE/PB倍数法）\n\n")
            f.write("**原理**: 直接对比同业或历史分位，应用市场化工具\n")
            f.write("**适用**: 最实用、最市场化（直观对标）\n")
            f.write("**关键指标**:\n")
            f.write("  - **PB中位数**: A股银行当前0.54倍（历史低位20%分位）\n")
            f.write("  - **城商行PB**: 约1.0倍（宁波银行参考）\n")
            f.write("  - **PE（TTM）**: 招商银行≈8-9倍，国有大行6-7倍\n\n")
            
            f.write("---\n\n")
            
            # 风险提示
            f.write("## ⚠️ 重要提示\n\n")
            f.write("1. **数据时点**: 本报告基于2026年3月27日的市场数据\n")
            f.write("2. **模型局限**: 任何估值模型都有局限性，应多模型综合参考\n")
            f.write("3. **政策风险**: 监管政策、资本要求等可能影响估值\n")
            f.write("4. **市场风险**: 市场整体下跌会影响所有银行估值\n")
            f.write("5. **周期风险**: 经济周期变化影响银行盈利能力\n\n")
            
            f.write("---\n\n")
            f.write(f"*本报告由自动化估值系统生成于 {datetime.now().strftime('%Y年%m月%d日')}*\n")
    
    def _save_json_results(self, all_results):
        """保存完整的JSON格式数据"""
        
        # 简化数据以便JSON序列化
        simplified_results = []
        for result in all_results:
            simplified = {
                "bank_name": result["bank_name"],
                "stock_code": result["stock_code"],
                "category": result["category"],
                "current_price": result["current_price"],
                "current_pb": result["current_pb"],
                "current_pe": result["current_pe"],
                "roe": result["roe"],
                "dividend_yield": result["dividend_yield"],
                "ddm_pb": result.get("ddm_pb"),
                "pb_roe": result.get("pb_roe"),
                "riv": result.get("riv"),
                "relative": result.get("relative"),
            }
            simplified_results.append(simplified)
        
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(simplified_results, f, ensure_ascii=False, indent=2, default=str)


def main():
    """主程序"""
    try:
        reporter = ComprehensiveValuationReport()
        all_results, analysis = reporter.generate_report()
        
        # 展示总结
        print("\n【综合评估结果摘要】\n")
        total = sum(len(analysis[key]) for key in analysis)
        print(f"严重低估（评分<0.7）: {len(analysis['severely_undervalued']):2d} 家 | 推荐强烈关注")
        print(f"低估（评分0.7-0.95）: {len(analysis['undervalued']):2d} 家 | 推荐持有")
        print(f"合理值（评分0.95-1.15）: {len(analysis['fairly_valued']):2d} 家 | 可适度配置")
        print(f"高估（评分1.15-1.5）: {len(analysis['overvalued']):2d} 家 | 建议观望")
        print(f"严重高估（评分>1.5）: {len(analysis['severely_overvalued']):2d} 家 | 建议回避")
        print(f"\n{'總計':12s}: {total:2d} 家\n")
        
    except Exception as e:
        logger.error(f"报告生成失败: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
