"""
银行股估值模型 - RIV（剩余收益模型）
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class RIVModel:
    """剩余收益模型 (Residual Income Valuation)"""
    
    def __init__(self, r: float = 0.10, forecast_years: int = 10):
        """
        初始化RIV模型
        
        Args:
            r: 股权成本，默认10%
            forecast_years: 预测年限，默认10年
        """
        self.r = r
        self.forecast_years = forecast_years
    
    def calculate_intrinsic_value(self,
                                 book_value: float,
                                 roe_forecast: List[float],
                                 terminal_roe: float = None) -> Dict:
        """
        计算股票内在价值
        
        公式: V0 = BV0 + Σ(ROE_t - r) × BV_{t-1} / (1+r)^t
        
        其中:
        - BV0: 当前每股净资产
        - (ROE_t - r): 剩余收益（超额回报）
        - BV_{t-1}: 上一期净资产
        - r: 股权成本
        
        Args:
            book_value: 当前每股净资产
            roe_forecast: 预测期ROE列表
            terminal_roe: 终端年ROE（如不指定则等于r）
            
        Returns:
            估值结果
        """
        
        if not roe_forecast:
            logger.warning("需要提供ROE预测")
            return {}
        
        bv = book_value
        residual_income_pv = 0  # 剩余收益现值总和
        forecast_pv_details = []
        
        # 预测期剩余收益现值
        for t, roe in enumerate(roe_forecast, 1):
            residual_income = (roe - self.r) * bv
            pv = residual_income / ((1 + self.r) ** t)
            
            residual_income_pv += pv
            
            # 假设未来净资产按ROE增长
            bv = bv * (1 + roe)
            
            forecast_pv_details.append({
                "year": t,
                "roe": roe,
                "residual_income": round(residual_income, 4),
                "pv": round(pv, 4),
            })
        
        # 终端值处理
        terminal_roe = terminal_roe or self.r
        terminal_pv = self._calculate_terminal_value(
            bv, terminal_roe, len(roe_forecast)
        )
        
        # 内在价值 = 当前净资产 + 预测期剩余收益PV + 终端值PV
        intrinsic_value = book_value + residual_income_pv + terminal_pv
        
        return {
            "model": "剩余收益模型 (RIV)",
            "book_value": round(book_value, 2),
            "forecast_years": len(roe_forecast),
            "terminal_roe": terminal_roe,
            "residual_income_pv": round(residual_income_pv, 2),
            "terminal_pv": round(terminal_pv, 2),
            "intrinsic_value": round(intrinsic_value, 2),
            "forecast_details": forecast_pv_details,
            "formula": "V0 = BV0 + Σ(ROE_t - r)×BV_{t-1}/(1+r)^t + 终端值",
        }
    
    def calculate_with_uniform_roe(self,
                                  book_value: float,
                                  roe: float,
                                  forecast_years: int = None) -> Dict:
        """
        用统一ROE进行预测（简化版）
        
        Args:
            book_value: 当前每股净资产
            roe: 未来稳定ROE
            forecast_years: 预测年限
            
        Returns:
            估值结果
        """
        
        years = forecast_years or self.forecast_years
        roe_forecast = [roe] * years
        
        return self.calculate_intrinsic_value(book_value, roe_forecast, roe)
    
    def compare_with_market_price(self,
                                 book_value: float,
                                 roe: float,
                                 current_price: float) -> Dict:
        """
        将RIV模型计算的内在价值与市场价格进行对比
        
        Args:
            book_value: 每股净资产
            roe: ROE
            current_price: 当前股价
            
        Returns:
            对比分析结果
        """
        
        riv_result = self.calculate_with_uniform_roe(book_value, roe)
        intrinsic_value = riv_result["intrinsic_value"]
        
        difference = intrinsic_value - current_price
        difference_pct = (difference / current_price) * 100 if current_price > 0 else 0
        
        # 判断估值状态
        if difference_pct > 20:
            status = "严重低估"
        elif difference_pct > 10:
            status = "低估"
        elif difference_pct > -10:
            status = "合理"
        elif difference_pct > -20:
            status = "高估"
        else:
            status = "严重高估"
        
        return {
            **riv_result,
            "current_price": current_price,
            "price_difference": round(difference, 2),
            "price_difference_pct": round(difference_pct, 2),
            "margin_of_safety": round(difference / intrinsic_value * 100, 2) if intrinsic_value > 0 else 0,
            "status": status,
        }
    
    def multiple_scenario_analysis(self,
                                  book_value: float,
                                  pessimistic_roe: float,
                                  base_roe: float,
                                  optimistic_roe: float,
                                  forecast_years: int = None) -> Dict:
        """
        三种情景分析
        
        Args:
            book_value: 每股净资产
            pessimistic_roe: 悲观ROE
            base_roe: 基础ROE
            optimistic_roe: 乐观ROE
            forecast_years: 预测年限
            
        Returns:
            三种情景的估值结果
        """
        
        years = forecast_years or self.forecast_years
        
        results = {}
        
        for scenario_name, roe in [
            ("悲观", pessimistic_roe),
            ("基础", base_roe),
            ("乐观", optimistic_roe),
        ]:
            result = self.calculate_with_uniform_roe(book_value, roe, years)
            results[scenario_name] = {
                "roe": roe,
                "intrinsic_value": result["intrinsic_value"],
            }
        
        # 计算概率加权价值
        pessimistic_value = results["悲观"]["intrinsic_value"]
        base_value = results["基础"]["intrinsic_value"]
        optimistic_value = results["乐观"]["intrinsic_value"]
        
        # 权重：悲观30%, 基础40%, 乐观30%
        probability_weighted_value = (
            pessimistic_value * 0.3 +
            base_value * 0.4 +
            optimistic_value * 0.3
        )
        
        return {
            "scenarios": results,
            "pessimistic_value": round(pessimistic_value, 2),
            "base_value": round(base_value, 2),
            "optimistic_value": round(optimistic_value, 2),
            "probability_weighted_value": round(probability_weighted_value, 2),
        }
    
    def sensitivity_to_roe(self,
                          book_value: float,
                          base_roe: float,
                          roe_range: tuple = (0.06, 0.16)) -> Dict:
        """
        对ROE的敏感性分析
        
        Args:
            book_value: 每股净资产
            base_roe: 基础ROE
            roe_range: ROE范围
            
        Returns:
            ROE敏感性分析结果
        """
        
        results = {}
        
        step = 0.01
        roe_values = [round(roe_range[0] + i * step, 2) for i in range(int((roe_range[1] - roe_range[0]) / step) + 1)]
        
        for roe in roe_values:
            if roe > 0:
                result = self.calculate_with_uniform_roe(book_value, roe)
                results[f"ROE={roe:.2%}"] = result["intrinsic_value"]
        
        return results
    
    def _calculate_terminal_value(self,
                                  bv_end: float,
                                  terminal_roe: float,
                                  forecast_years: int) -> float:
        """
        计算终端值
        
        假设终端期永续增长
        """
        
        if terminal_roe <= self.r:
            # 终端ROE不高于股权成本时，终端值 ≈ 0
            return 0
        
        residual_income_terminal = (terminal_roe - self.r) * bv_end
        # 假设永续增长率为2%
        terminal_growth = 0.02
        terminal_value = residual_income_terminal / (self.r - terminal_growth)
        
        # 现值
        pv_terminal = terminal_value / ((1 + self.r) ** forecast_years)
        
        return pv_terminal
