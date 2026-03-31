"""
银行股估值模型 - DDM（股息贴现模型）
"""

import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class DDMModel:
    """股息贴现模型 (Dividend Discount Model)"""
    
    def __init__(self, r: float = 0.10, g: float = 0.04):
        """
        初始化DDM模型
        
        Args:
            r: 股权成本（CAPM），通常9%-11%，默认10%
            g: 永续增长率，通常3%-5%，默认4%
        """
        self.r = r
        self.g = g
        
        if r <= g:
            logger.warning(f"股权成本({r:.2%}) 必须大于增长率({g:.2%})")
    
    def calculate_fair_value(self, 
                            dividend_per_share: float,
                            payout_ratio: float = None,
                            eps: float = None) -> Dict:
        """
        计算股票合理价值
        
        公式: P0 = D1 / (r - g)
        其中:
        - D1: 下一年预期每股股息 = 当前股息 * (1 + g) 或 EPS * 派息率
        - r: 股权成本
        - g: 永续增长率
        
        Args:
            dividend_per_share: 当前每股股息
            payout_ratio: 派息率（可选，用于预测下一年股息）
            eps: 每股收益（可选）
            
        Returns:
            包含估值结果的字典
        """
        
        if not dividend_per_share or dividend_per_share == 0:
            logger.warning("股息为0，无法使用DDM模型")
            return self._create_result(0, "无")
        
        # 计算下一年预期股息
        if eps and payout_ratio:
            # 使用EPS和派息率预测下一年股息
            d1 = eps * payout_ratio * (1 + self.g)
        else:
            # 使用当前股息按增长率计算
            d1 = dividend_per_share * (1 + self.g)
        
        # 计算合理价值
        fair_value = d1 / (self.r - self.g)
        
        return {
            "model": "DDM (股息贴现模型)",
            "fair_value": round(fair_value, 2),
            "d1": round(d1, 4),
            "r": self.r,
            "g": self.g,
            "formula": f"P0 = D1/(r-g) = {d1:.4f}/({self.r:.2%}-{self.g:.2%})",
        }
    
    def calculate_pb_from_ddm(self,
                             roe: float,
                             payout_ratio: float) -> Dict:
        """
        从DDM转化为PB估值
        
        公式: PB = (ROE × d) / (r - g)
        其中: d = 派息率，ROE = 净资产收益率
        
        Args:
            roe: 净资产收益率
            payout_ratio: 派息率
            
        Returns:
            PB估值结果
        """
        
        if roe <= self.g:
            logger.warning(f"ROE({roe:.2%}) 必须大于增长率({self.g:.2%})")
        
        pb = (roe * payout_ratio) / (self.r - self.g)
        
        return {
            "model": "DDM转PB表达式",
            "pb_value": round(pb, 3),
            "roe": roe,
            "payout_ratio": payout_ratio,
            "r": self.r,
            "g": self.g,
            "formula": f"PB = (ROE×d)/(r-g) = ({roe:.2%}×{payout_ratio:.2%})/({self.r:.2%}-{self.g:.2%})",
        }
    
    def calculate_dividend_yield(self, dividend_per_share: float, current_price: float) -> float:
        """
        计算股息率
        
        公式: 股息率 = 每股股息 / 股价
        """
        if current_price <= 0:
            return 0
        return dividend_per_share / current_price
    
    def sensitivity_analysis(self,
                            dividend_per_share: float,
                            r_range: tuple = (0.08, 0.12),
                            g_range: tuple = (0.02, 0.06)) -> Dict:
        """
        敏感性分析：在不同r和g组合下的估值
        
        Args:
            dividend_per_share: 每股股息
            r_range: 股权成本范围 (min, max)
            g_range: 增长率范围 (min, max)
            
        Returns:
            敏感性分析表
        """
        
        results = {}
        
        # 创建r和g的范围
        r_values = [round(r_range[0] + i * 0.01, 2) for i in range(int((r_range[1] - r_range[0]) / 0.01) + 1)]
        g_values = [round(g_range[0] + i * 0.005, 3) for i in range(int((g_range[1] - g_range[0]) / 0.005) + 1)]
        
        for r in r_values:
            for g in g_values:
                if r > g:
                    d1 = dividend_per_share * (1 + g)
                    fair_value = d1 / (r - g)
                    key = f"r={r:.2%},g={g:.2%}"
                    results[key] = round(fair_value, 2)
        
        return results
    
    def _create_result(self, value: float, model_type: str) -> Dict:
        """创建结果字典"""
        return {
            "model": model_type,
            "fair_value": value,
        }
