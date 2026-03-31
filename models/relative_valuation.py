"""
银行股估值模型 - 相对估值法
"""

import logging
from typing import Dict, List
import statistics

logger = logging.getLogger(__name__)


class RelativeValuation:
    """相对估值法 - PB/PE倍数法"""
    
    def __init__(self):
        """初始化相对估值器"""
        pass
    
    def calculate_pb_premium(self,
                            current_pb: float,
                            peer_pb_median: float,
                            peer_pb_mean: float = None) -> Dict:
        """
        计算相对PB溢价/折价
        
        Args:
            current_pb: 当前PB
            peer_pb_median: 同行业中位数PB
            peer_pb_mean: 同行业平均PB
            
        Returns:
            PB溢价分析
        """
        
        premium_to_median = (current_pb / peer_pb_median - 1) * 100 if peer_pb_median > 0 else 0
        
        result = {
            "current_pb": current_pb,
            "peer_pb_median": peer_pb_median,
            "premium_to_median_pct": round(premium_to_median, 2),
        }
        
        if peer_pb_mean:
            premium_to_mean = (current_pb / peer_pb_mean - 1) * 100 if peer_pb_mean > 0 else 0
            result["peer_pb_mean"] = peer_pb_mean
            result["premium_to_mean_pct"] = round(premium_to_mean, 2)
        
        return result
    
    def calculate_fair_pb_by_peers(self,
                                  peer_pbs: List[float],
                                  use_median: bool = True) -> Dict:
        """
        基于同行业可比公司计算合理PB
        
        Args:
            peer_pbs: 同行业PB列表
            use_median: 是否使用中位数（True）或平均值（False）
            
        Returns:
            基准PB估值
        """
        
        if not peer_pbs:
            logger.warning("没有提供同行业PB数据")
            return {}
        
        if use_median:
            fair_pb = statistics.median(peer_pbs)
            method = "中位数"
        else:
            fair_pb = statistics.mean(peer_pbs)
            method = "平均值"
        
        return {
            "method": method,
            "fair_pb": round(fair_pb, 3),
            "peer_count": len(peer_pbs),
            "min_pb": round(min(peer_pbs), 3),
            "max_pb": round(max(peer_pbs), 3),
            "std_dev": round(statistics.stdev(peer_pbs), 3) if len(peer_pbs) > 1 else 0,
        }
    
    def calculate_fair_pe_by_peers(self,
                                  peer_pes: List[float],
                                  use_median: bool = True) -> Dict:
        """
        基于同行业可比公司计算合理PE
        
        Args:
            peer_pes: 同行业PE列表
            use_median: 是否使用中位数
            
        Returns:
            基准PE估值
        """
        
        if not peer_pes:
            logger.warning("没有提供同行业PE数据")
            return {}
        
        if use_median:
            fair_pe = statistics.median(peer_pes)
            method = "中位数"
        else:
            fair_pe = statistics.mean(peer_pes)
            method = "平均值"
        
        return {
            "method": method,
            "fair_pe": round(fair_pe, 2),
            "peer_count": len(peer_pes),
            "min_pe": round(min(peer_pes), 2),
            "max_pe": round(max(peer_pes), 2),
            "std_dev": round(statistics.stdev(peer_pes), 2) if len(peer_pes) > 1 else 0,
        }
    
    def compare_by_pb(self,
                     current_pb: float,
                     peer_pbs: List[float],
                     book_value: float = None) -> Dict:
        """
        基于PB的可比分析
        
        Args:
            current_pb: 当前PB
            peer_pbs: 同行业PB列表
            book_value: 每股净资产（可选，用于计算建议价格）
            
        Returns:
            PB可比分析结果
        """
        
        peer_median = statistics.median(peer_pbs)
        peer_mean = statistics.mean(peer_pbs)
        
        # 判断相对估值状态
        if current_pb < peer_median * 0.85:
            status = "相对低估"
        elif current_pb > peer_median * 1.15:
            status = "相对高估"
        else:
            status = "相对合理"
        
        result = {
            "current_pb": current_pb,
            "peer_pb_median": round(peer_median, 3),
            "peer_pb_mean": round(peer_mean, 3),
            "discount_to_median_pct": round((1 - current_pb / peer_median) * 100, 2),
            "status": status,
        }
        
        if book_value:
            fair_price_by_median = peer_median * book_value
            fair_price_by_mean = peer_mean * book_value
            current_price = current_pb * book_value
            
            result.update({
                "current_price": round(current_price, 2),
                "fair_price_by_median": round(fair_price_by_median, 2),
                "fair_price_by_mean": round(fair_price_by_mean, 2),
            })
        
        return result
    
    def compare_by_pe(self,
                     current_pe: float,
                     peer_pes: List[float],
                     eps: float = None) -> Dict:
        """
        基于PE的可比分析
        
        Args:
            current_pe: 当前PE
            peer_pes: 同行业PE列表
            eps: 每股收益（可选）
            
        Returns:
            PE可比分析结果
        """
        
        peer_median = statistics.median(peer_pes)
        peer_mean = statistics.mean(peer_pes)
        
        result = {
            "current_pe": current_pe,
            "peer_pe_median": round(peer_median, 2),
            "peer_pe_mean": round(peer_mean, 2),
            "discount_to_median_pct": round((1 - current_pe / peer_median) * 100, 2),
        }
        
        if eps:
            fair_price_by_median = peer_median * eps
            fair_price_by_mean = peer_mean * eps
            current_price = current_pe * eps
            
            result.update({
                "current_price": round(current_price, 2),
                "fair_price_by_median": round(fair_price_by_median, 2),
                "fair_price_by_mean": round(fair_price_by_mean, 2),
            })
        
        return result
    
    def dividend_yield_comparison(self,
                                 current_yield: float,
                                 peer_yields: List[float],
                                 current_price: float = None,
                                 annual_dividend: float = None) -> Dict:
        """
        股息率比较分析
        
        Args:
            current_yield: 当前股息率
            peer_yields: 同行业股息率列表
            current_price: 当前股价（可选）
            annual_dividend: 年度分红（可选，用于计算合理股价）
            
        Returns:
            股息率比较结果
        """
        
        peer_median_yield = statistics.median(peer_yields)
        peer_mean_yield = statistics.mean(peer_yields)
        
        result = {
            "current_yield": round(current_yield, 4),
            "peer_median_yield": round(peer_median_yield, 4),
            "peer_mean_yield": round(peer_mean_yield, 4),
            "yield_premium_pct": round((current_yield / peer_median_yield - 1) * 100, 2),
        }
        
        if current_price and annual_dividend:
            fair_price_by_median = annual_dividend / peer_median_yield
            fair_price_by_mean = annual_dividend / peer_mean_yield
            
            result.update({
                "current_price": current_price,
                "fair_price_by_median_yield": round(fair_price_by_median, 2),
                "fair_price_by_mean_yield": round(fair_price_by_mean, 2),
            })
        
        return result
    
    def percentile_analysis(self,
                           current_value: float,
                           peer_values: List[float],
                           value_type: str = "PB") -> Dict:
        """
        百分位分析 - 显示当前估值在同行业中的相对位置
        
        Args:
            current_value: 当前估值指标
            peer_values: 同行业估值指标列表
            value_type: 指标类型（PB/PE等）
            
        Returns:
            百分位分析结果
        """
        
        sorted_values = sorted(peer_values)
        percentile = (sum(1 for v in sorted_values if v <= current_value) / len(sorted_values)) * 100
        
        return {
            "value_type": value_type,
            "current_value": round(current_value, 3),
            "percentile": round(percentile, 1),
            "assessment": self._percentile_assessment(percentile),
            "peer_min": round(min(peer_values), 3),
            "peer_max": round(max(peer_values), 3),
            "peer_median": round(statistics.median(peer_values), 3),
        }
    
    def _percentile_assessment(self, percentile: float) -> str:
        """根据百分位评估"""
        if percentile < 20:
            return "显著低估（处于低位）"
        elif percentile < 40:
            return "相对低估"
        elif percentile < 60:
            return "接近中位数"
        elif percentile < 80:
            return "相对高估"
        else:
            return "显著高估（处于高位）"
