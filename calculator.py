"""
银行股估值模型 - 计算引擎
集成四大估值模型
"""

import logging
from typing import Dict, List, Optional
import pandas as pd

import sys
from pathlib import Path

# 添加models目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from models.ddm_model import DDMModel
from models.pb_roe_model import PBROEModel
from models.riv_model import RIVModel
from models.relative_valuation import RelativeValuation

logger = logging.getLogger(__name__)


class ValuationCalculator:
    """估值计算引擎"""
    
    def __init__(self, config: Config = None):
        """初始化计算引擎"""
        self.config = config or Config()
        
        # 初始化各个模型
        ddm_params = self.config.MODEL_PARAMS["ddm"]
        pb_roe_params = self.config.MODEL_PARAMS["pb_roe"]
        riv_params = self.config.MODEL_PARAMS["riv"]
        
        self.ddm = DDMModel(
            r=ddm_params["r"],
            g=ddm_params["g"]
        )
        
        self.pb_roe = PBROEModel(
            r=pb_roe_params["r"],
            g=pb_roe_params["g"],
            high_growth_years=pb_roe_params["high_growth_years"]
        )
        
        self.riv = RIVModel(
            r=riv_params["r"],
            forecast_years=riv_params["forecast_years"]
        )
        
        self.relative = RelativeValuation()
    
    def calculate_all_models(self, bank_data: Dict) -> Dict:
        """
        对单个银行进行四大模型估值
        
        Args:
            bank_data: 银行基本面数据字典
            
        Returns:
            包含所有模型估值结果的字典
        """
        
        bank_name = bank_data.get("bank_name", "未知银行")
        logger.info(f"计算 {bank_name} 的估值...")
        
        results = {
            "bank_name": bank_name,
            "stock_code": bank_data.get("stock_code"),
            "category": bank_data.get("category"),
            "current_price": bank_data.get("current_price"),
            "current_pb": bank_data.get("pb"),
            "current_pe": bank_data.get("pe"),
            "roe": bank_data.get("roe"),
            "dividend_yield": bank_data.get("dividend_yield"),
        }
        
        # 1. DDM估值
        try:
            ddm_result = self.ddm.calculate_fair_value(
                dividend_per_share=bank_data.get("dividend_per_share", 0),
                payout_ratio=bank_data.get("dividend_payout_ratio"),
                eps=bank_data.get("eps")
            )
            results["ddm"] = ddm_result
            
            # DDM转PB
            ddm_pb_result = self.ddm.calculate_pb_from_ddm(
                roe=bank_data.get("roe", 0),
                payout_ratio=bank_data.get("dividend_payout_ratio", 0)
            )
            results["ddm_pb"] = ddm_pb_result.get("pb_value")
        except Exception as e:
            logger.error(f"DDM计算失败: {e}")
            results["ddm"] = None
        
        # 2. PB-ROE模型
        try:
            pb_roe_result = self.pb_roe.calculate_fair_pb(
                roe=bank_data.get("roe", 0)
            )
            results["pb_roe"] = pb_roe_result
            
            # 计算合理价格
            fair_price_result = self.pb_roe.calculate_fair_price(
                roe=bank_data.get("roe", 0),
                book_value=bank_data.get("book_value", 0)
            )
            results["pb_roe_fair_price"] = fair_price_result.get("fair_price")
            
            # 与市场进行对比
            comparison = self.pb_roe.compare_with_market(
                current_pb=bank_data.get("pb", 0),
                roe=bank_data.get("roe", 0),
                current_price=bank_data.get("current_price"),
                book_value=bank_data.get("book_value")
            )
            results["pb_roe_comparison"] = comparison
        except Exception as e:
            logger.error(f"PB-ROE计算失败: {e}")
            results["pb_roe"] = None
        
        # 3. RIV模型
        try:
            riv_result = self.riv.calculate_with_uniform_roe(
                book_value=bank_data.get("book_value", 0),
                roe=bank_data.get("roe", 0)
            )
            results["riv"] = riv_result
            
            # RIV与市场价格对比
            riv_comparison = self.riv.compare_with_market_price(
                book_value=bank_data.get("book_value", 0),
                roe=bank_data.get("roe", 0),
                current_price=bank_data.get("current_price", 0)
            )
            results["riv_comparison"] = riv_comparison
            
            # 多情景分析
            scenario_result = self.riv.multiple_scenario_analysis(
                book_value=bank_data.get("book_value", 0),
                pessimistic_roe=bank_data.get("roe", 0) * 0.85,
                base_roe=bank_data.get("roe", 0),
                optimistic_roe=bank_data.get("roe", 0) * 1.15
            )
            results["riv_scenarios"] = scenario_result
        except Exception as e:
            logger.error(f"RIV计算失败: {e}")
            results["riv"] = None
        
        # 4. 相对估值法（PE/PB倍数法）
        try:
            category = bank_data.get("category", "未分类")
            industry_benchmarks = self.config.MODEL_PARAMS["relative"].get("industry_benchmarks", {})
            benchmarks = industry_benchmarks.get(category, {})
            
            peer_pb_median = benchmarks.get("pb_median")
            peer_pe_median = benchmarks.get("pe_ttm_median")
            
            relative_results = {}
            
            # 基于PB的相对估值
            if peer_pb_median:
                # 1. 计算PB溢价/折价
                pb_premium = self.relative.calculate_pb_premium(
                    current_pb=bank_data.get("pb", 0),
                    peer_pb_median=peer_pb_median
                )
                relative_results["pb_premium"] = pb_premium
                
                # 2. 构造PB列表用于对比分析（中位数±5%的范围）
                peer_pbs = [
                    peer_pb_median * 0.90,
                    peer_pb_median * 0.95,
                    peer_pb_median,
                    peer_pb_median * 1.05,
                    peer_pb_median * 1.10,
                ]
                
                pb_comparison = self.relative.compare_by_pb(
                    current_pb=bank_data.get("pb", 0),
                    peer_pbs=peer_pbs,
                    book_value=bank_data.get("book_value", 0)
                )
                relative_results["pb_comparison"] = pb_comparison
                
                # 3. 基于同行业PB的合理估值
                fair_pb_result = self.relative.calculate_fair_pb_by_peers(
                    peer_pbs=peer_pbs,
                    use_median=True
                )
                relative_results["fair_pb_by_peers"] = fair_pb_result
            
            # 基于PE的相对估值
            if peer_pe_median and bank_data.get("pe"):
                # 构造PE列表用于对比分析
                peer_pes = [
                    peer_pe_median * 0.90,
                    peer_pe_median * 0.95,
                    peer_pe_median,
                    peer_pe_median * 1.05,
                    peer_pe_median * 1.10,
                ]
                
                pe_comparison = self.relative.compare_by_pe(
                    current_pe=bank_data.get("pe", 0),
                    peer_pes=peer_pes,
                    eps=bank_data.get("eps", 0)
                )
                relative_results["pe_comparison"] = pe_comparison
                
                # 基于同行业PE的合理估值
                fair_pe_result = self.relative.calculate_fair_pe_by_peers(
                    peer_pes=peer_pes,
                    use_median=True
                )
                relative_results["fair_pe_by_peers"] = fair_pe_result
            
            # 同行业分位数分析
            if peer_pb_median:
                percentile = self.relative.percentile_analysis(
                    current_value=bank_data.get("pb", 0),
                    peer_values=peer_pbs,
                    value_type="PB"
                )
                relative_results["percentile_analysis"] = percentile
            
            results["relative"] = relative_results
            
        except Exception as e:
            logger.error(f"相对估值法计算失败: {e}")
            results["relative"] = None
        
        return results
    
    def calculate_for_multiple_banks(self, 
                                    banks_data: List[Dict]) -> pd.DataFrame:
        """
        对多个银行进行批量估值
        
        Args:
            banks_data: 银行数据字典列表
            
        Returns:
            包含所有估值结果的DataFrame
        """
        
        all_results = []
        
        for bank_data in banks_data:
            result = self.calculate_all_models(bank_data)
            all_results.append(result)
        
        return pd.DataFrame(all_results)
    
    def rank_by_model(self,
                     results_df: pd.DataFrame,
                     model_type: str = "pb_roe",
                     ascending: bool = True) -> pd.DataFrame:
        """
        按某个模型的估值进行排序推荐
        
        Args:
            results_df: 估值结果DataFrame
            model_type: 模型类型（pb_roe, ddm, riv, relative）
            ascending: 是否升序排列
            
        Returns:
            排序后的推荐列表
        """
        
        # 提取相关列进行排序
        recommendation_df = results_df[[
            "bank_name",
            "category",
            "current_pb",
            "roe",
            "dividend_yield"
        ]].copy()
        
        # 根据模型类型添加估值指标
        if model_type == "pb_roe":
            recommendation_df["pb_roe_fair_pb"] = results_df["pb_roe"].apply(
                lambda x: x.get("fair_pb") if isinstance(x, dict) else None
            )
            recommendation_df["valuation_gap"] = (
                recommendation_df["current_pb"] - 
                recommendation_df["pb_roe_fair_pb"]
            )
            sort_column = "valuation_gap"
        elif model_type == "ddm":
            recommendation_df["ddm_fair_pb"] = results_df["ddm_pb"]
            recommendation_df["valuation_gap"] = (
                recommendation_df["current_pb"] - 
                recommendation_df["ddm_fair_pb"]
            )
            sort_column = "valuation_gap"
        elif model_type == "relative":
            # 相对估值法：基于PB溢价排序
            recommendation_df["pb_premium"] = results_df["relative"].apply(
                lambda x: x.get("pb_premium", {}).get("premium_to_median_pct") 
                if isinstance(x, dict) else None
            )
            recommendation_df["valuation_gap"] = recommendation_df["pb_premium"]
            sort_column = "valuation_gap"
        else:
            recommendation_df["riv_fair_price"] = results_df["riv"].apply(
                lambda x: x.get("intrinsic_value") if isinstance(x, dict) else None
            )
            recommendation_df["price_gap"] = (
                recommendation_df["current_pb"] - 
                recommendation_df["riv_fair_price"]
            )
            sort_column = "price_gap"
        
        return recommendation_df.sort_values(by=sort_column, ascending=ascending)
    
    def identify_opportunities(self,
                              results_df: pd.DataFrame) -> Dict:
        """
        从估值结果中识别投资机会
        
        Returns:
            分类的投资机会列表
        """
        
        opportunities = {
            "severely_undervalued": [],      # 严重低估
            "undervalued": [],               # 低估
            "fairly_valued": [],             # 合理
            "overvalued": [],                # 高估
            "severely_overvalued": [],       # 严重高估
        }
        
        for _, row in results_df.iterrows():
            pb_comparison = row.get("pb_roe_comparison")
            
            if isinstance(pb_comparison, dict):
                status = pb_comparison.get("status")
                
                bank_info = {
                    "bank_name": row["bank_name"],
                    "category": row["category"],
                    "current_pb": row["current_pb"],
                    "roe": row["roe"],
                    "dividend_yield": row["dividend_yield"],
                    "status": status,
                }
                
                if status == "严重低估":
                    opportunities["severely_undervalued"].append(bank_info)
                elif status == "低估":
                    opportunities["undervalued"].append(bank_info)
                elif status == "合理估值":
                    opportunities["fairly_valued"].append(bank_info)
                elif status == "高估":
                    opportunities["overvalued"].append(bank_info)
                elif status == "严重高估":
                    opportunities["severely_overvalued"].append(bank_info)
        
        return opportunities
