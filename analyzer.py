"""
银行股估值模型 - 分析和报告生成
"""

import logging
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import pandas as pd

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

logger = logging.getLogger(__name__)


class ValuationAnalyzer:
    """估值分析和报告生成器"""
    
    def __init__(self, config=None):
        """初始化分析器"""
        self.config = config
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    def generate_summary_report(self, 
                               results_df: pd.DataFrame,
                               opportunities: Dict) -> str:
        """
        生成估值汇总报告
        
        Args:
            results_df: 估值结果DataFrame
            opportunities: 机会识别结果
            
        Returns:
            报告文本
        """
        
        report = []
        report.append("=" * 80)
        report.append(f"银行股估值模型分析报告")
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 80)
        report.append("")
        
        # 整体统计
        report.append("【整体统计】")
        report.append(f"评估银行总数: {len(results_df)}")
        report.append(f"平均PB: {results_df['current_pb'].mean():.3f}x")
        report.append(f"平均PE: {results_df['current_pe'].mean():.2f}x")
        report.append(f"平均ROE: {results_df['roe'].mean():.2%}")
        report.append(f"平均股息率: {results_df['dividend_yield'].mean():.2%}")
        report.append("")
        
        # 按分类统计
        report.append("【分类统计】")
        category_stats = results_df.groupby('category').agg({
            'bank_name': 'count',
            'current_pb': ['mean', 'min', 'max'],
            'roe': ['mean', 'min', 'max'],
            'dividend_yield': 'mean',
        }).round(3)
        report.append(str(category_stats))
        report.append("")
        
        # 机会识别
        report.append("【机会识别】")
        
        if opportunities['severely_undervalued']:
            report.append("严重低估（强烈推荐关注）:")
            for bank in opportunities['severely_undervalued']:
                report.append(
                    f"  - {bank['bank_name']:8s} {bank['category']:12s} "
                    f"PB={bank['current_pb']:.3f}x ROE={bank['roe']:.2%} "
                    f"股息率={bank['dividend_yield']:.2%}"
                )
            report.append("")
        
        if opportunities['undervalued']:
            report.append("低估（推荐关注）:")
            for bank in opportunities['undervalued']:
                report.append(
                    f"  - {bank['bank_name']:8s} {bank['category']:12s} "
                    f"PB={bank['current_pb']:.3f}x ROE={bank['roe']:.2%} "
                    f"股息率={bank['dividend_yield']:.2%}"
                )
            report.append("")
        
        if opportunities['overvalued']:
            report.append("高估（建议回避）:")
            for bank in opportunities['overvalued']:
                report.append(
                    f"  - {bank['bank_name']:8s} {bank['category']:12s} "
                    f"PB={bank['current_pb']:.3f}x ROE={bank['roe']:.2%} "
                    f"股息率={bank['dividend_yield']:.2%}"
                )
            report.append("")
        
        if opportunities['severely_overvalued']:
            report.append("严重高估（强烈建议回避）:")
            for bank in opportunities['severely_overvalued']:
                report.append(
                    f"  - {bank['bank_name']:8s} {bank['category']:12s} "
                    f"PB={bank['current_pb']:.3f}x ROE={bank['roe']:.2%} "
                    f"股息率={bank['dividend_yield']:.2%}"
                )
            report.append("")
        
        # 模型建议
        report.append("=" * 80)
        report.append("【投资建议总结】")
        report.append("")
        report.append("根据2026年3月最新数据分析:")
        report.append("")
        report.append("1. 整体板块情况:")
        report.append("   • A股银行整体PB处于历史低位（0.54-0.6x），破净率接近100%")
        report.append("   • 平均股息率4.4%高于10年国债，安全边际充足")
        report.append("   • 建议积极配置，特别是被低估的城商行")
        report.append("")
        
        report.append("2. 模型选择建议:")
        report.append("   • 防御型投资者：优先使用PB-ROE + DDM模型，关注高股息银行")
        report.append("   • 成长型投资者：关注RIV剩余收益模型，城商行龙头最有潜力")
        report.append("   • 组合配置：先用PB-ROE确定合理区间，再用相对估值验证")
        report.append("")
        
        report.append("3. 风险提示:")
        report.append("   • 关注净息差走势（LPR下行风险）")
        report.append("   • 监控不良率变化（地产、零售行业压力）")
        report.append("   • 追踪监管资本要求变化")
        report.append("")
        
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def generate_detail_report(self, 
                              results: List[Dict],
                              output_path: Path = None) -> str:
        """
        生成详细估值报告
        
        Args:
            results: 估值结果列表
            output_path: 输出路径
            
        Returns:
            报告文本
        """
        
        report = []
        
        for result in results:
            bank_name = result.get("bank_name", "未知")
            report.append("")
            report.append("=" * 80)
            report.append(f"【{bank_name}】估值分析报告")
            report.append("=" * 80)
            report.append("")
            
            # 基本信息
            report.append("基本信息:")
            report.append(f"  股票代码: {result.get('stock_code')}")
            report.append(f"  所属分类: {result.get('category')}")
            report.append(f"  当前股价: {result.get('current_price'):.2f}元")
            report.append(f"  当前PB: {result.get('current_pb'):.3f}x")
            report.append(f"  当前PE: {result.get('current_pe'):.2f}x")
            report.append(f"  ROE: {result.get('roe'):.2%}")
            report.append(f"  股息率: {result.get('dividend_yield'):.2%}")
            report.append("")
            
            # 四大模型结果
            report.append("四大估值模型结果:")
            report.append("")
            
            # DDM
            if result.get('ddm'):
                ddm = result['ddm']
                report.append(f"  1. DDM（股息贴现模型）")
                report.append(f"     合理价值: {ddm.get('fair_value'):.2f}元")
                report.append(f"     对应PB: {result.get('ddm_pb'):.3f}x")
                report.append("")
            
            # PB-ROE
            if result.get('pb_roe'):
                pb_roe = result['pb_roe']
                comparison = result.get('pb_roe_comparison', {})
                report.append(f"  2. PB-ROE模型")
                report.append(f"     合理PB: {pb_roe.get('fair_pb'):.3f}x")
                report.append(f"     合理价格: {result.get('pb_roe_fair_price'):.2f}元")
                report.append(f"     估值状态: {comparison.get('status')}")
                report.append(f"     PB溢价: {comparison.get('pb_difference_pct'):.2f}%")
                report.append("")
            
            # RIV
            if result.get('riv'):
                riv = result['riv']
                riv_comp = result.get('riv_comparison', {})
                report.append(f"  3. RIV（剩余收益模型）")
                report.append(f"     内在价值: {riv.get('intrinsic_value'):.2f}元")
                report.append(f"     价格差距: {riv_comp.get('price_difference'):.2f}元")
                report.append(f"     估值状态: {riv_comp.get('status')}")
                report.append("")
            
            report.append("")
        
        return "\n".join(report)
    
    def export_to_csv(self,
                     results_df: pd.DataFrame,
                     output_dir: Path) -> Path:
        """export到CSV文件"""
        
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"bank_valuation_{self.timestamp}.csv"
        
        # 简化输出列
        export_df = results_df[[
            'bank_name', 'stock_code', 'category',
            'current_price', 'current_pb', 'current_pe',
            'roe', 'dividend_yield'
        ]].copy()
        
        export_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        logger.info(f"已导出CSV文件: {output_file}")
        
        return output_file
    
    def export_to_json(self,
                      results: List[Dict],
                      output_dir: Path) -> Path:
        """导出到JSON文件"""
        
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"bank_valuation_{self.timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2, default=str)
        
        logger.info(f"已导出JSON文件: {output_file}")
        
        return output_file
    
    def export_to_txt(self,
                     report_text: str,
                     output_dir: Path,
                     filename: str = "valuation_report") -> Path:
        """导出到文本文件"""
        
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{filename}_{self.timestamp}.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        logger.info(f"已导出报告文件: {output_file}")
        
        return output_file
