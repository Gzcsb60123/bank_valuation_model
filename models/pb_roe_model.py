"""
银行股估值模型 - PB-ROE模型（市净率模型）
"""

import logging
from typing import Dict
import math

logger = logging.getLogger(__name__)


class PBROEModel:
    """PB-ROE模型 - 银行股最核心的估值模型"""
    
    def __init__(self, r: float = 0.10, g: float = 0.04, high_growth_years: int = 5):
        """
        初始化PB-ROE模型
        
        Args:
            r: 股权成本，默认10%
            g: 永续增长率，默认4%
            high_growth_years: 高增长期年限，默认5年
        """
        self.r = r
        self.g = g
        self.high_growth_years = high_growth_years
    
    def calculate_fair_pb(self, roe: float) -> Dict:
        """
        单阶段简化版PB计算
        
        公式: PB = (ROE - g) / (r - g)
        
        Args:
            roe: 净资产收益率（ROE）
            
        Returns:
            估值结果
        """
        
        if roe <= self.g:
            logger.warning(f"ROE({roe:.2%}) 应该大于增长率({self.g:.2%})")
        
        pb = (roe - self.g) / (self.r - self.g)
        
        # 评估
        assessment = self._assess_pb(pb)
        
        return {
            "model": "PB-ROE模型（单阶段）",
            "fair_pb": round(pb, 3),
            "roe": roe,
            "r": self.r,
            "g": self.g,
            "formula": f"PB = (ROE-g)/(r-g) = ({roe:.2%}-{self.g:.2%})/({self.r:.2%}-{self.g:.2%})",
            "assessment": assessment,
        }
    
    def calculate_two_stage_pb(self, 
                              roe_high: float,
                              roe_low: float = None,
                              high_growth_years: int = None) -> Dict:
        """
        两阶段PB-ROE模型
        
        公式: ln(PB0) = (ROE - r) × T + ln(PBT)
        其中: T为高ROE阶段时长，PBT为后期稳定PB
        
        Args:
            roe_high: 高增长期ROE
            roe_low: 稳定期ROE（如不指定，默认= g）
            high_growth_years: 高增长期年限
            
        Returns:
            估值结果
        """
        
        if roe_high <= self.r:
            logger.warning(f"高增长期ROE({roe_high:.2%}) 应该大于股权成本({self.r:.2%})")
        
        years = high_growth_years or self.high_growth_years
        
        # 稳定期ROE默认等于增长率
        if roe_low is None:
            roe_low = self.g
        
        # 后期稳定PB = 1
        pb_t = 1.0
        
        # 对数形式计算
        excess_return = roe_high - self.r
        log_pb = excess_return * years + math.log(pb_t)
        pb = math.exp(log_pb)
        
        assessment = self._assess_pb(pb)
        
        return {
            "model": "PB-ROE模型（两阶段）",
            "fair_pb": round(pb, 3),
            "roe_high": roe_high,
            "roe_low": roe_low,
            "high_growth_years": years,
            "pb_terminal": pb_t,
            "r": self.r,
            "g": self.g,
            "formula": f"ln(PB)=({roe_high:.2%}-{self.r:.2%})×{years}+ln({pb_t})",
            "assessment": assessment,
        }
    
    def calculate_fair_price(self, 
                            roe: float,
                            book_value: float,
                            use_two_stage: bool = False,
                            roe_high: float = None) -> Dict:
        """
        根据ROE和净资产计算股票合理价格
        
        公式: 合理价格 = PB × 每股净资产
        
        Args:
            roe: ROE
            book_value: 每股净资产
            use_two_stage: 是否使用两阶段模型
            roe_high: 两阶段模型中的高ROE
            
        Returns:
            估值结果（包括合理价格）
        """
        
        if use_two_stage and roe_high:
            pb_result = self.calculate_two_stage_pb(roe_high)
        else:
            pb_result = self.calculate_fair_pb(roe)
        
        fair_pb = pb_result["fair_pb"]
        fair_price = fair_pb * book_value
        
        return {
            **pb_result,
            "book_value": book_value,
            "fair_price": round(fair_price, 2),
            "price_formula": f"合理价格 = PB × 净资产 = {fair_pb:.3f} × {book_value:.2f}",
        }
    
    def compare_with_market(self, 
                           current_pb: float,
                           roe: float,
                           current_price: float = None,
                           book_value: float = None) -> Dict:
        """
        将市场PB与合理PB进行比较
        
        Args:
            current_pb: 当前市净率
            roe: ROE
            current_price: 当前股价（可选，用于输出信息）
            book_value: 每股净资产（可选）
            
        Returns:
            对比分析结果
        """
        
        pb_result = self.calculate_fair_pb(roe)
        fair_pb = pb_result["fair_pb"]
        
        difference = current_pb - fair_pb
        difference_pct = (difference / fair_pb) * 100 if fair_pb > 0 else 0
        
        # 判断估值状态
        if difference_pct > 15:
            status = "严重高估"
        elif difference_pct > 5:
            status = "小幅高估"
        elif difference_pct < -15:
            status = "严重低估"
        elif difference_pct < -5:
            status = "小幅低估"
        else:
            status = "合理估值"
        
        result = {
            "current_pb": current_pb,
            "fair_pb": fair_pb,
            "pb_difference": round(difference, 3),
            "pb_difference_pct": round(difference_pct, 2),
            "status": status,
        }
        
        if current_price and book_value:
            fair_price = fair_pb * book_value
            price_difference = current_price - fair_price
            price_difference_pct = (price_difference / fair_price) * 100
            
            result.update({
                "current_price": current_price,
                "fair_price": round(fair_price, 2),
                "price_difference": round(price_difference, 2),
                "price_difference_pct": round(price_difference_pct, 2),
            })
        
        return result
    
    def sensitivity_analysis(self,
                            roe: float,
                            r_range: tuple = (0.08, 0.12),
                            g_range: tuple = (0.02, 0.06)) -> Dict:
        """
        PB估值敏感性分析
        
        Args:
            roe: ROE
            r_range: 股权成本范围
            g_range: 增长率范围
            
        Returns:
            敏感性分析矩阵
        """
        
        results = {}
        
        r_values = [round(r_range[0] + i * 0.01, 2) for i in range(int((r_range[1] - r_range[0]) / 0.01) + 1)]
        g_values = [round(g_range[0] + i * 0.005, 3) for i in range(int((g_range[1] - g_range[0]) / 0.005) + 1)]
        
        for r in r_values:
            for g in g_values:
                if r > g and roe > g:
                    pb = (roe - g) / (r - g)
                    key = f"r={r:.2%},g={g:.2%}"
                    results[key] = round(pb, 3)
        
        return results
    
    def analyze_roe_impact(self,
                          base_roe: float,
                          current_pb: float,
                          book_value: float) -> Dict:
        """
        分析ROE变化对估值的影响
        
        Args:
            base_roe: 基础ROE
            current_pb: 当前PB
            book_value: 每股净资产
            
        Returns:
            ROE敏感性分析结果
        """
        
        roe_levels = [0.06, 0.08, 0.10, 0.12, 0.14, 0.16]
        results = {}
        
        for roe in roe_levels:
            pb_result = self.calculate_fair_pb(roe)
            fair_pb = pb_result["fair_pb"]
            fair_price = fair_pb * book_value
            
            results[f"ROE={roe:.2%}"] = {
                "fair_pb": round(fair_pb, 3),
                "fair_price": round(fair_price, 2),
                "premium": round((fair_pb / current_pb - 1) * 100, 1),
            }
        
        return results
    
    def _assess_pb(self, pb: float) -> str:
        """根据PB值评估估值状态"""
        if pb < 0.7:
            return "严重低估"
        elif pb < 0.85:
            return "低估"
        elif pb < 1.2:
            return "合理"
        elif pb < 1.5:
            return "高估"
        else:
            return "严重高估"
