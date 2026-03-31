#!/usr/bin/env python3
"""
自动更新bank_data字典中的所有银行数据
"""
import re
from DATA_UPDATE_REFERENCE_20260329 import BANK_DATA_UPDATE

def generate_updated_data_dict():
    """生成更新后的Python字典代码文本"""
    
    output = []
    output.append("# 已更新的银行数据（2026年3月29日）")
    output.append("# 数据来源：官方平台（同花顺、SSE、SZSE）参考值")
    output.append("# *** 关键说明：以下数据仍为参考值，建议从官方渠道核实 ***\n")
    
    updated_banks = BANK_DATA_UPDATE.keys()
    
    for bank_name in sorted(updated_banks):
        data = BANK_DATA_UPDATE[bank_name]
        
        output.append(f'            "{bank_name}": {{')
        output.append(f'                "stock_code": "{data["stock_code"]}", ')
        output.append(f'                "current_price": {data["current_price"]},')
        output.append(f'                "pb": {data["pb"]},')
        output.append(f'                "pe": {data["pe"]},')
        output.append(f'                "roe": {data["roe"]},')
        output.append(f'                "dividend_yield": {data["dividend_yield"]},')
        output.append(f'                # 其他字段自动计算（EPS、book_value等）')
        output.append('            },')
        output.append('')
    
    return '\n'.join(output)

if __name__ == "__main__":
    # 生成更新的数据
    generated = generate_updated_data_dict()
    
    # 输出到文件供参考
    with open('GENERATED_BANK_UPDATE_DATA.txt', 'w', encoding='utf-8') as f:
        f.write(generated)
    
    print("✓ 已生成更新数据参考文件：GENERATED_BANK_UPDATE_DATA.txt")
    print(f"✓ 共包含{len(BANK_DATA_UPDATE)}家银行的数据")
    print("\n接下来的步骤：")
    print("1. 查看 GENERATED_BANK_UPDATE_DATA.txt 中的数据")
    print("2. 手动或使用脚本替换 data_fetcher.py 中的数据")
    print("3. 运行 python main.py --format all 验证")

