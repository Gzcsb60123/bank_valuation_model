#!/usr/bin/env python3
"""
银行股估值模型 - 主程序
集成DDM、PB-ROE、RIV和相对估值法四大估值模型
"""

import logging
import sys
from pathlib import Path
from typing import Optional

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from data_fetcher import DataFetcher
from calculator import ValuationCalculator
from analyzer import ValuationAnalyzer


def setup_logging():
    """配置日志"""
    config = Config()
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # 清除已有处理器
    logger.handlers.clear()
    
    # 文件处理器
    file_handler = logging.FileHandler(
        config.LOG_DIR / f"bank_valuation_{config.TIMESTAMP}.log",
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # 格式
    formatter = logging.Formatter(
        config.LOG_FORMAT,
        datefmt=config.LOG_DATE_FORMAT
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def main(categories: Optional[list] = None, export_format: str = "all"):
    """
    主程序
    
    Args:
        categories: 要分析的银行分类列表。如果为None，则分析所有
        export_format: 导出格式 ("csv", "json", "txt", "all")
    """
    
    logger = setup_logging()
    config = Config()
    
    logger.info("=" * 80)
    logger.info("银行股估值模型分析开始")
    logger.info("=" * 80)
    
    try:
        # 步骤1: 数据获取
        logger.info("【步骤1】数据获取...")
        fetcher = DataFetcher(config)
        
        if categories:
            # 获取特定分类的银行数据
            all_banks_data = []
            for category in categories:
                logger.info(f"获取 {category} 数据...")
                category_df = fetcher.fetch_by_category(category)
                all_banks_data.extend(category_df.to_dict('records'))
        else:
            # 获取所有银行数据
            logger.info("获取所有银行数据...")
            all_banks_df = fetcher.fetch_all_banks()
            all_banks_data = all_banks_df.to_dict('records')
        
        logger.info(f"成功获取 {len(all_banks_data)} 家银行的数据")
        
        # 步骤2: 估值计算
        logger.info("")
        logger.info("【步骤2】估值计算...")
        calculator = ValuationCalculator(config)
        
        results_list = []
        for bank_data in all_banks_data:
            try:
                result = calculator.calculate_all_models(bank_data)
                results_list.append(result)
            except Exception as e:
                logger.error(f"计算 {bank_data.get('bank_name')} 失败: {e}")
        
        logger.info(f"完成 {len(results_list)} 家银行的估值计算")
        
        # 转换为DataFrame便于分析
        import pandas as pd
        results_df = pd.DataFrame(results_list)
        
        # 步骤3: 机会识别
        logger.info("")
        logger.info("【步骤3】机会识别...")
        opportunities = calculator.identify_opportunities(results_df)
        
        logger.info(f"  严重低估: {len(opportunities['severely_undervalued'])} 家")
        logger.info(f"  低估: {len(opportunities['undervalued'])} 家")
        logger.info(f"  合理: {len(opportunities['fairly_valued'])} 家")
        logger.info(f"  高估: {len(opportunities['overvalued'])} 家")
        logger.info(f"  严重高估: {len(opportunities['severely_overvalued'])} 家")
        
        # 步骤4: 报告生成
        logger.info("")
        logger.info("【步骤4】报告生成...")
        analyzer = ValuationAnalyzer(config)
        
        # 生成汇总报告
        summary_report = analyzer.generate_summary_report(results_df, opportunities)
        logger.info("汇总报告已生成")
        
        # 生成详细报告
        detailed_report = analyzer.generate_detail_report(results_list)
        logger.info("详细报告已生成")
        
        # 步骤5: 导出结果
        logger.info("")
        logger.info("【步骤5】导出结果...")
        
        if export_format in ("csv", "all"):
            analyzer.export_to_csv(results_df, config.REPORT_DIR)
        
        if export_format in ("json", "all"):
            analyzer.export_to_json(results_list, config.REPORT_DIR)
        
        if export_format in ("txt", "all"):
            analyzer.export_to_txt(summary_report, config.REPORT_DIR, "summary_report")
            analyzer.export_to_txt(detailed_report, config.REPORT_DIR, "detailed_report")
        
        # 打印汇总结果
        logger.info("")
        logger.info("="*80)
        logger.info("分析完成，汇总结果:")
        logger.info("="*80)
        print(summary_report)
        
        logger.info("")
        logger.info(f"结果已导出到: {config.REPORT_DIR}")
        
        return {
            "success": True,
            "banks_analyzed": len(results_list),
            "opportunities": opportunities,
            "results_df": results_df
        }
        
    except Exception as e:
        logger.error(f"程序执行失败: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e)
        }
    
    finally:
        logger.info("")
        logger.info("="*80)
        logger.info("银行股估值模型分析结束")
        logger.info("="*80)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="银行股估值模型分析工具")
    parser.add_argument(
        "--categories",
        nargs="+",
        help="指定要分析的银行分类 (国有大型银行, 全国性股份制银行, 城商行)",
        default=None
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json", "txt", "all"],
        default="all",
        help="输出格式"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="日志级别"
    )
    
    args = parser.parse_args()
    
    result = main(
        categories=args.categories,
        export_format=args.format
    )
    
    if not result["success"]:
        sys.exit(1)
