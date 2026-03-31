#!/usr/bin/env python3
"""
相对估值法集成测试
验证第四个估值模型（PE/PB倍数法）是否正确集成
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from bank_valuation_model.calculator import ValuationCalculator
from bank_valuation_model.config import Config

def test_relative_valuation():
    """测试相对估值法是否被正确调用"""
    
    print("=" * 80)
    print("相对估值法（PE/PB倍数法）集成测试")
    print("=" * 80)
    
    # 初始化计算器
    config = Config()
    calculator = ValuationCalculator(config)
    
    # 测试数据：招商银行
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
    
    print("\n测试银行：招商银行（股份行代表）")
    print(f"  PB: {test_bank['pb']}, PE: {test_bank['pe']}, ROE: {test_bank['roe']}")
    
    # 执行完整估值
    print("\n执行四大估值模型计算...")
    results = calculator.calculate_all_models(test_bank)
    
    # 检查结果
    print("\n✓ 估值结果汇总:")
    print(f"\n  1. DDM模型: {'✓ 已执行' if results.get('ddm') else '✗ 未执行'}")
    if results.get('ddm'):
        print(f"     - 合理PB: {results['ddm_pb']:.3f}" if results.get('ddm_pb') else "")
    
    print(f"\n  2. PB-ROE模型: {'✓ 已执行' if results.get('pb_roe') else '✗ 未执行'}")
    if results.get('pb_roe'):
        fair_pb = results['pb_roe'].get('fair_pb')
        print(f"     - 合理PB: {fair_pb:.3f}" if fair_pb else "")
    
    print(f"\n  3. RIV模型: {'✓ 已执行' if results.get('riv') else '✗ 未执行'}")
    if results.get('riv'):
        intrinsic = results['riv'].get('intrinsic_value')
        print(f"     - 内在价值: {intrinsic:.3f}" if intrinsic else "")
    
    print(f"\n  4. 相对估值法（PE/PB倍数法）: {'✓ 已执行' if results.get('relative') else '✗ 未执行'}")
    if results.get('relative'):
        relative = results['relative']
        print("     ✓ 新增功能已成功集成！")
        
        # 显示相对估值详情
        if relative.get('pb_premium'):
            pb_premium = relative['pb_premium']
            print(f"\n     PB溢价分析:")
            print(f"       - 当前PB: {pb_premium['current_pb']:.3f}")
            print(f"       - 同行业PB中位数: {pb_premium['peer_pb_median']:.3f}")
            print(f"       - 相对中位数溢价: {pb_premium['premium_to_median_pct']:.2f}%")
        
        if relative.get('pb_comparison'):
            pb_cmp = relative['pb_comparison']
            print(f"\n     PB对比评价:")
            print(f"       - 评价: {pb_cmp.get('assessment', 'N/A')}")
            print(f"       - 建议: {pb_cmp.get('recommendation', 'N/A')}")
        
        if relative.get('fair_pb_by_peers'):
            fair_pb = relative['fair_pb_by_peers']
            print(f"\n     基于同行业的合理PB:")
            print(f"       - 合理PB: {fair_pb.get('fair_pb', 'N/A'):.3f}" 
                  if isinstance(fair_pb.get('fair_pb'), (int, float)) else f"       - {fair_pb}")
        
        if relative.get('percentile_analysis'):
            pct = relative['percentile_analysis']
            print(f"\n     分位数分析:")
            print(f"       - 分位数位置: {pct.get('percentile', 'N/A')}")
            print(f"       - 估值分类: {pct.get('valuation_percentile', 'N/A')}")
    
    # 总体评价
    print("\n" + "=" * 80)
    if results.get('relative'):
        print("✓ SUCCESS: 相对估值法（PE/PB倍数法）已成功集成到估值计算器中！")
        print("\n新增功能包括：")
        print("  • PB溢价/折价分析")
        print("  • 基于同行业中位数的PB/PE对比")
        print("  • 合理PB/PE计算")
        print("  • 分位数估值分析")
    else:
        print("✗ FAILED: 相对估值法未被正确调用！")
    print("=" * 80)

if __name__ == "__main__":
    test_relative_valuation()
