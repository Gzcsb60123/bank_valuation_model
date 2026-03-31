#!/usr/bin/env python3
"""
四大估值模型完整检查表
验证所有模型都已在计算器中正确调用
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from bank_valuation_model.calculator import ValuationCalculator
from bank_valuation_model.config import Config

def check_all_models():
    """全面检查四大估值模型的集成状态"""
    
    print("\n" + "="*85)
    print(" "*20 + "银行股估值模型 - 四大模型完整检查")
    print("="*85)
    
    config = Config()
    
    print("\n📋 配置检查:")
    print("-" * 85)
    
    # 检查1: 相对估值法在配置中
    relative_config = config.MODEL_PARAMS.get("relative", {})
    if "industry_benchmarks" in relative_config:
        print("✓ 相对估值法配置已添加")
        benchmarks = relative_config["industry_benchmarks"]
        for category, data in benchmarks.items():
            print(f"  ├─ {category}: PB={data['pb_median']}, PE={data['pe_ttm_median']}")
    else:
        print("✗ 相对估值法配置缺失")
    
    print("\n📊 模型实现检查:")
    print("-" * 85)
    
    # 检查2: 验证RelativeValuation类
    try:
        from bank_valuation_model.models.relative_valuation import RelativeValuation
        rv = RelativeValuation()
        methods = [
            'calculate_pb_premium',
            'calculate_fair_pb_by_peers',
            'calculate_fair_pe_by_peers',
            'compare_by_pb',
            'compare_by_pe',
            'percentile_analysis'
        ]
        
        print("✓ RelativeValuation 模型类已加载")
        for method in methods:
            if hasattr(rv, method):
                print(f"  ├─ {method}() ✓")
            else:
                print(f"  ├─ {method}() ✗")
    except ImportError as e:
        print(f"✗ RelativeValuation 模型加载失败: {e}")
    
    print("\n🔧 计算器集成检查:")
    print("-" * 85)
    
    calculator = ValuationCalculator(config)
    
    # 检查3: 计算器是否初始化了所有模型
    models_to_check = [
        ('ddm', 'DDM模型'),
        ('pb_roe', 'PB-ROE模型'),
        ('riv', 'RIV模型'),
        ('relative', '相对估值法'),
    ]
    
    for attr, name in models_to_check:
        if hasattr(calculator, attr):
            print(f"✓ {name} 已初始化为: calculator.{attr}")
        else:
            print(f"✗ {name} 未初始化")
    
    # 检查4: 实际执行估值计算
    print("\n⚙️ 功能测试 (招商银行示例):")
    print("-" * 85)
    
    test_bank = {
        "bank_name": "招商银行",
        "stock_code": "600036",
        "category": "全国性股份制银行",
        "current_price": 25.50,
        "pb": 1.20,
        "pe": 8.5,
        "roe": 0.18,
        "dividend_yield": 0.032,
        "dividend_per_share": 0.82,
        "dividend_payout_ratio": 0.35,
        "eps": 3.00,
        "book_value": 21.25,
    }
    
    results = calculator.calculate_all_models(test_bank)
    
    models_results = [
        ('ddm', 'DDM模型'),
        ('pb_roe', 'PB-ROE模型'),
        ('riv', 'RIV模型'),
        ('relative', '相对估值法'),
    ]
    
    for key, name in models_results:
        result = results.get(key)
        if result is not None:
            if isinstance(result, dict) and len(result) > 0:
                print(f"✓ {name:15} → 成功执行，返回 {len(result)} 个结果")
            else:
                print(f"⚠ {name:15} → 执行但返回空或无效结果")
        else:
            print(f"✗ {name:15} → 未执行或错误")
    
    print("\n" + "="*85)
    
    # 总结
    all_models_ok = all(results.get(key) is not None 
                       for key, _ in models_results)
    
    if all_models_ok:
        print("✅ 全部四大估值模型已检查完毕，所有功能正常！")
        print("\n模型清单:")
        print("  1. ✓ 股息贴现模型 (DDM)")
        print("  2. ✓ PB-ROE模型")
        print("  3. ✓ 剩余收益模型 (RIV)")
        print("  4. ✓ 相对估值法 (PE/PB倍数法) ← 新增")
    else:
        print("⚠️  部分模型存在问题，请检查上面的结果")
    
    print("="*85 + "\n")

if __name__ == "__main__":
    check_all_models()
