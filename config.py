"""
银行股估值模型 - 全局配置
"""

import os
from datetime import datetime
from pathlib import Path


class Config:
    """全局配置类"""
    
    # 项目路径
    PROJECT_ROOT = Path(__file__).parent.parent
    MODEL_DIR = Path(__file__).parent
    DATA_DIR = MODEL_DIR / "data"
    REPORT_DIR = MODEL_DIR / "reports"
    LOG_DIR = PROJECT_ROOT / "logs"
    
    # 确保目录存在
    DATA_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)
    
    # 银行分类
    BANK_CATEGORIES = {
        "国有大型银行": [
            "工商银行", "农业银行", "中国银行", "建设银行", "交通银行", "邮储银行"
        ],
        "全国性股份制银行": [
            "招商银行", "浦发银行", "中信银行", "兴业银行", "平安银行", "民生银行",
            "光大银行", "华夏银行"
        ],
        "城商行": [
            "北京银行", "上海银行", "杭州银行", "成都银行", "西安银行", "长沙银行", 
            "重庆银行", "江苏银行", "苏州银行", "厦门银行", "贵阳银行", "郑州银行", 
            "南京银行", "宁波银行", "青岛银行"
        ]
    }
    
    # 估值参数（2026年参考值）
    VALUATION_PARAMS = {
        "risk_free_rate": 0.024,          # 10年国债收益率，约2.4%
        "equity_cost_base": 0.10,         # 股权成本（CAPM）基础值，约10%
        "market_risk_premium": 0.07,      # 市场风险溢价，约7%
        "perpetual_growth_rate": 0.04,    # 永续增长率（GDP增速），约4%
        "inflation_rate": 0.02,           # 预期通胀率，约2%
    }
    
    # 估值模型参数
    MODEL_PARAMS = {
        "ddm": {
            "name": "股息贴现模型",
            "r": 0.10,                    # 股权成本
            "g": 0.04,                    # 永续增长率
        },
        "pb_roe": {
            "name": "PB-ROE模型",
            "r": 0.10,
            "g": 0.04,
            "high_growth_years": 5,       # 高增长期年限
        },
        "riv": {
            "name": "剩余收益模型",
            "r": 0.10,
            "forecast_years": 10,         # 预测年限
        },
        "relative": {
            "name": "相对估值法",
            "use_median": True,           # 使用中位数作为基准
            # 行业基准数据（2026年市场参考值）
            "industry_benchmarks": {
                "国有大型银行": {
                    "pb_median": 0.54,
                    "pe_ttm_median": 6.5,
                },
                "全国性股份制银行": {
                    "pb_median": 0.70,
                    "pe_ttm_median": 8.5,
                },
                "城商行": {
                    "pb_median": 0.85,
                    "pe_ttm_median": 9.0,
                }
            }
        }
    }
    
    # 警告阈值
    THRESHOLDS = {
        "overvalued_pb": 1.5,            # PB > 1.5倍认为高估
        "undervalued_pb": 0.7,           # PB < 0.7倍认为低估
        "low_dividend_yield": 0.03,      # 股息率 < 3%为低
        "high_dividend_yield": 0.05,     # 股息率 > 5%为高
        "low_roe": 0.08,                 # ROE < 8%为低
        "high_roe": 0.13,                # ROE > 13%为高
        "high_npl_ratio": 0.02,          # 不良率 > 2%为高
        "low_capital_ratio": 0.11,       # 核心一级资本充足率 < 11%为低
    }
    
    # 数据源配置
    DATA_SOURCES = {
        "tushare": {
            "enabled": True,
            "token": os.getenv("TUSHARE_TOKEN", ""),
        },
        "sina": {
            "enabled": True,
        },
        "netease": {
            "enabled": True,
        }
    }
    
    # 日志配置
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    
    # 输出配置
    REPORT_FORMAT = {
        "excel": True,
        "json": True,
        "html": True,
        "csv": True,
    }
    
    # 当前日期时间戳
    TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    @classmethod
    def get_bank_list(cls, category=None):
        """获取银行列表"""
        if category:
            return cls.BANK_CATEGORIES.get(category, [])
        else:
            all_banks = []
            for banks in cls.BANK_CATEGORIES.values():
                all_banks.extend(banks)
            return all_banks
    
    @classmethod
    def get_category(cls, bank_name):
        """获取银行所属分类"""
        for category, banks in cls.BANK_CATEGORIES.items():
            if bank_name in banks:
                return category
        return "未分类"
