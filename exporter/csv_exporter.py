"""
CSV导出器模块
负责将词频统计结果导出为CSV格式文件
"""

import csv
import os
from typing import Dict, List, Tuple
from pathlib import Path


class CSVExporter:
    """CSV导出器类"""
    
    def __init__(self):
        """初始化CSV导出器"""
        self.default_headers = ['word', 'count']
        
    def export_word_frequency(self, word_counts: Dict[str, int], 
                             filename: str, 
                             sort_by_count: bool = True,
                             headers: List[str] = None) -> bool:
        """
        导出词频统计结果到CSV文件
        
        Args:
            word_counts (Dict[str, int]): 词频统计字典
            filename (str): 输出文件名（包含路径）
            sort_by_count (bool): 是否按频次排序，默认True
            headers (List[str], optional): 自定义表头，默认为['word', 'count']
            
        Returns:
            bool: 导出是否成功
        """
        if not word_counts:
            print("词频数据为空，无法导出")
            return False
            
        try:
            # 确保输出目录存在
            output_path = Path(filename)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 准备数据
            if sort_by_count:
                # 按词频降序排序
                sorted_items = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
            else:
                # 按词汇字母顺序排序
                sorted_items = sorted(word_counts.items(), key=lambda x: x[0])
            
            # 设置表头
            if headers is None:
                headers = self.default_headers
            
            # 写入CSV文件
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # 写入表头
                writer.writerow(headers)
                
                # 写入数据
                for word, count in sorted_items:
                    writer.writerow([word, count])
            
            print(f"词频数据已成功导出到: {filename}")
            print(f"共导出 {len(sorted_items)} 个词汇")
            return True
            
        except Exception as e:
            print(f"导出CSV文件失败: {e}")
            return False
    
    def export_top_words(self, word_counts: Dict[str, int], 
                        filename: str, 
                        top_n: int = 50,
                        headers: List[str] = None) -> bool:
        """
        导出前N个高频词汇到CSV文件
        
        Args:
            word_counts (Dict[str, int]): 词频统计字典
            filename (str): 输出文件名
            top_n (int): 导出的词汇数量，默认50
            headers (List[str], optional): 自定义表头
            
        Returns:
            bool: 导出是否成功
        """
        if not word_counts:
            return False
            
        # 获取前N个高频词
        sorted_items = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        top_words = dict(sorted_items[:top_n])
        
        return self.export_word_frequency(top_words, filename, sort_by_count=True, headers=headers)
    
    def export_with_statistics(self, word_counts: Dict[str, int], 
                              filename: str,
                              total_words: int = None,
                              unique_words: int = None) -> bool:
        """
        导出词频数据并包含统计信息
        
        Args:
            word_counts (Dict[str, int]): 词频统计字典
            filename (str): 输出文件名
            total_words (int, optional): 总词数
            unique_words (int, optional): 不重复词数
            
        Returns:
            bool: 导出是否成功
        """
        if not word_counts:
            return False
            
        try:
            output_path = Path(filename)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 计算统计信息
            if total_words is None:
                total_words = sum(word_counts.values())
            if unique_words is None:
                unique_words = len(word_counts)
            
            # 按频次排序
            sorted_items = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # 写入统计信息
                writer.writerow(['统计信息'])
                writer.writerow(['总词数', total_words])
                writer.writerow(['不重复词数', unique_words])
                writer.writerow([''])  # 空行分隔
                
                # 写入词频数据
                writer.writerow(['词汇', '出现次数', '频率%'])
                for word, count in sorted_items:
                    frequency_percent = (count / total_words) * 100 if total_words > 0 else 0
                    writer.writerow([word, count, f"{frequency_percent:.2f}"])
            
            print(f"带统计信息的词频数据已导出到: {filename}")
            return True
            
        except Exception as e:
            print(f"导出带统计信息的CSV文件失败: {e}")
            return False
    
    def export_filtered_words(self, word_counts: Dict[str, int], 
                             filename: str,
                             min_frequency: int = 2,
                             min_length: int = 3) -> bool:
        """
        导出过滤后的词频数据
        
        Args:
            word_counts (Dict[str, int]): 词频统计字典
            filename (str): 输出文件名
            min_frequency (int): 最小出现频次，默认2
            min_length (int): 最小词长，默认3
            
        Returns:
            bool: 导出是否成功
        """
        if not word_counts:
            return False
            
        # 过滤词汇
        filtered_words = {
            word: count for word, count in word_counts.items()
            if count >= min_frequency and len(word) >= min_length
        }
        
        if not filtered_words:
            print("过滤后没有符合条件的词汇")
            return False
        
        return self.export_word_frequency(filtered_words, filename)
    
    def get_export_summary(self, word_counts: Dict[str, int]) -> Dict[str, any]:
        """
        获取导出数据的摘要信息
        
        Args:
            word_counts (Dict[str, int]): 词频统计字典
            
        Returns:
            Dict[str, any]: 摘要信息
        """
        if not word_counts:
            return {}
            
        frequencies = list(word_counts.values())
        
        return {
            'total_unique_words': len(word_counts),
            'total_word_count': sum(frequencies),
            'max_frequency': max(frequencies),
            'min_frequency': min(frequencies),
            'avg_frequency': sum(frequencies) / len(frequencies),
            'most_common_word': max(word_counts.items(), key=lambda x: x[1])
        }


def main():
    """测试函数"""
    # 测试数据
    test_word_counts = {
        'python': 25,
        'data': 20,
        'analysis': 15,
        'machine': 12,
        'learning': 12,
        'science': 10,
        'programming': 8,
        'statistics': 6,
        'visualization': 5,
        'algorithm': 4
    }
    
    exporter = CSVExporter()
    
    print("测试CSV导出功能")
    print(f"测试数据: {test_word_counts}")
    print("\n" + "="*50 + "\n")
    
    # 测试基本导出
    success = exporter.export_word_frequency(
        test_word_counts, 
        'test_output/word_frequency.csv'
    )
    print(f"基本导出结果: {'成功' if success else '失败'}")
    
    # 测试导出前5个高频词
    success = exporter.export_top_words(
        test_word_counts, 
        'test_output/top_words.csv', 
        top_n=5
    )
    print(f"Top5导出结果: {'成功' if success else '失败'}")
    
    # 测试带统计信息的导出
    success = exporter.export_with_statistics(
        test_word_counts,
        'test_output/word_frequency_with_stats.csv'
    )
    print(f"带统计信息导出结果: {'成功' if success else '失败'}")
    
    # 显示摘要信息
    summary = exporter.get_export_summary(test_word_counts)
    print(f"\n数据摘要:")
    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main() 